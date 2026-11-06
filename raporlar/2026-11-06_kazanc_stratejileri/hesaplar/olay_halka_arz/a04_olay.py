"""Adım 4: halka arz olay çalışması. Girdi: out/ipo_tablo.csv, px/cd_*.parquet (düzeltilmiş kapanış, birincil),
px/ht_*.parquet (düzeltilmemiş kapanış/min/max/AOF). Çıktı: out/ipo_olay.csv (arz başına ölçüler) ve ekrana tablolar.
Tanımlar (önceden belirlendi, ızgaranın tamamı raporlanır):
  gün1 getirisi  = düzeltilmemiş gün1 kapanış / arz fiyatı - 1 (gün1 baz fiyatı = arz fiyatı)
  tavan günü     = kapanış >= önceki kapanış*1.10'un fiyat adımına aşağı yuvarlanmışı (1 adım tolerans)
  kilitli tavan  = tavan ve (düzeltilmemiş) gün içi min == max  -> tavandan alış emri dolmaz
  seri uzunluğu  = gün1'den itibaren ardışık tavan kapanış sayısı; E = serinin ardından ilk tavan olmayan gün
  seri sonrası   = giriş E kapanışı (ya da E AOF'u, ya da E+1 kapanışı), ufuk h = 5/21/63/126 işlem günü,
                   ham getiri, XU100'e göre BHAR, toplam AR (CAR) ve beta-düzeltilmiş CAR (beta: E+1..E+250 günlük)
  katılımcı      = arz fiyatından alınan lot; satış kuralları: gün1 kapanış / E AOF / E kapanış / E+21 / E+63 kapanış
  lock-up        = ilk işlem + satmama süresi (yoksa 365 gün varsayımı); CAR[-10,-1], [0,+5], [0,+20], [-20,+20]
İstatistik: ortalama, medyan, t (iid) ve t_küme (giriş ayına göre kümelenmiş SE), isabet, %5/%95."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import PX, OUT

SON = pd.Timestamp("2026-11-05")  # 06.11 seansı tamamlanmadı -> dahil değil
H = [5, 21, 63, 126]
MALIYET = 0.0025  # gidiş-dönüş 25 bp


def tick(p):
    for lim, t in ((20, 0.01), (50, 0.02), (100, 0.05), (250, 0.10), (500, 0.25), (1000, 0.50), (2500, 1.0)):
        if p < lim:
            return t
    return 2.5


def tavan_fiyat(base):
    x = base * 1.10
    t = tick(x)
    return math.floor(x / t + 1e-9) * t


def taban_fiyat(base):
    x = base * 0.90
    t = tick(x)
    return math.ceil(x / t - 1e-9) * t


def load_xu():
    x = pd.read_parquet(os.path.join(PX, "cd_XU100.parquet"))["px"]
    return x[x.index <= SON]


def load_stock(kod, start):
    p = os.path.join(PX, f"cd_{kod}.parquet")
    if not os.path.exists(p):
        return None
    c = pd.read_parquet(p)["px"]
    c = c[(c.index >= start) & (c.index <= SON)]
    if len(c) == 0:
        return None
    df = c.rename("adj").to_frame()
    ph = os.path.join(PX, f"ht_{kod}.parquet")
    if os.path.exists(ph):
        h = pd.read_parquet(ph)
        df = df.join(h[["HG_KAPANIS", "HG_MIN", "HG_MAX", "HG_AOF", "HG_HACIM", "HGDG_KAPANIS"]], how="left")
    else:
        for k in ["HG_KAPANIS", "HG_MIN", "HG_MAX", "HG_AOF", "HG_HACIM", "HGDG_KAPANIS"]:
            df[k] = np.nan
    return df


def summ(x, cl=None):
    x = pd.Series(x, dtype=float)
    m = x.notna()
    x = x[m]
    n = len(x)
    if n == 0:
        return dict(n=0)
    mu = x.mean(); sd = x.std(ddof=1) if n > 1 else np.nan
    t = mu / (sd / math.sqrt(n)) if n > 1 and sd > 0 else np.nan
    tcl = np.nan
    if cl is not None and n > 2:
        g = pd.Series(cl)[m.values].values
        e = (x - mu).values
        s = pd.Series(e).groupby(g).sum()
        G = len(s)
        if G > 2:
            se = math.sqrt((s ** 2).sum() * G / (G - 1)) / n
            tcl = mu / se if se > 0 else np.nan
    return dict(n=n, ort=mu, med=x.median(), t=t, t_kume=tcl, isabet=(x > 0).mean(), p5=x.quantile(.05), p95=x.quantile(.95))


def fmt_tab(rows, pct=True):
    out = pd.DataFrame(rows)
    for c in ["ort", "med", "p5", "p95"]:
        if c in out:
            out[c] = (out[c] * 100).round(1) if pct else out[c].round(3)
    for c in ["t", "t_kume"]:
        if c in out:
            out[c] = out[c].round(2)
    if "isabet" in out:
        out["isabet"] = (out["isabet"] * 100).round(0)
    return out


def analyze_one(r, xu):
    kod = r.kod
    hz = r.ilk_islem_hz if pd.notna(r.ilk_islem_hz) else pd.Timestamp(int(r.arz_yili), 1, 1)
    df = load_stock(kod, hz - pd.Timedelta(days=7))
    if df is None or len(df) < 2:
        return None, None
    d1 = df.index[0]
    out = dict(kod=kod, d1=d1, d1_fark_hz=(d1 - hz).days if pd.notna(r.ilk_islem_hz) else np.nan)
    # düzeltilmemiş seri: HT varsa doğrudan, yoksa ilk ortak gündeki oranla CD'den
    com = df["HG_KAPANIS"].dropna()
    f = (com.iloc[0] / df.loc[com.index[0], "adj"]) if len(com) else np.nan
    raw = df["HG_KAPANIS"].copy()
    if not np.isfinite(f):
        f = 1.0  # HT yok: düzeltme faktörünü 1 varsay (yalnız erken pencere; uyarı bayrağı)
        out["ht_yok"] = True
    raw = raw.fillna(df["adj"] * f)
    offer = r.fiyat
    out["f_raw_adj"] = f
    adj = df["adj"]
    ret = adj.pct_change()
    ret.iloc[0] = raw.iloc[0] / offer - 1
    out["gun1"] = ret.iloc[0]
    # tavan/taban bayrakları
    base = pd.Series([offer] + list(raw.iloc[:-1].values), index=df.index)
    tav = pd.Series([tavan_fiyat(b) for b in base], index=df.index)
    tab = pd.Series([taban_fiyat(b) for b in base], index=df.index)
    tol_up = (tav / base - 1) - 0.0005
    is_tav = ret >= tol_up
    is_tab = ret <= (tab / base - 1) + 0.0005
    locked = (df["HG_MAX"] - df["HG_MIN"]).abs() < 1e-6
    has_ht = df["HG_MAX"].notna()
    n = 0
    while n < len(df) and bool(is_tav.iloc[n]):
        n += 1
    out["seri"] = n
    out["sansur"] = n >= len(df)  # seri hâlâ sürüyor / veri bitti
    out["gun1_tavan"] = bool(is_tav.iloc[0])
    out["gun1_kilit"] = bool(is_tav.iloc[0] and locked.iloc[0]) if has_ht.iloc[0] else np.nan
    if n > 0:
        hh = has_ht.iloc[:n]
        out["seri_kilit_oran"] = locked.iloc[:n][hh].mean() if hh.any() else np.nan
    gross = (raw.iloc[0] / offer) * (adj / adj.iloc[0])  # arz fiyatından toplam getiri çarpanı (bedelsiz düzeltmeli)
    out["arz_tepe"] = gross.iloc[n - 1] - 1 if n > 0 else gross.iloc[0] - 1
    out["max_arz_63"] = gross.iloc[:63].max() - 1
    daily = []
    if out["sansur"]:
        return out, None
    E = n  # 0-index: ilk tavan olmayan gün
    eD = df.index[E]
    out["E"] = eD
    out["E_getiri"] = ret.iloc[E]
    out["E_taban"] = bool(is_tab.iloc[E])
    out["E_taban_kilit"] = bool(is_tab.iloc[E] and locked.iloc[E]) if has_ht.iloc[E] else np.nan
    # E günü AOF (düzeltilmemiş) -> düzeltilmiş ölçeğe
    aof = df["HG_AOF"].iloc[E]
    aof_adj = aof * adj.iloc[E] / raw.iloc[E] if pd.notna(aof) and raw.iloc[E] > 0 else np.nan
    out["E_aof_kapanis"] = aof_adj / adj.iloc[E] - 1 if pd.notna(aof_adj) else np.nan
    # katılımcı getirileri (arz fiyatından)
    out["kat_gun1"] = gross.iloc[0] - 1
    out["kat_E_aof"] = (gross.iloc[E] * aof_adj / adj.iloc[E] - 1) if pd.notna(aof_adj) else gross.iloc[E] - 1
    out["kat_E_kap"] = gross.iloc[E] - 1
    for h in (21, 63, 126, 250):
        out[f"kat_E{h}"] = gross.iloc[E + h] - 1 if E + h < len(df) else np.nan
    # piyasa
    xr = xu.reindex(df.index).ffill()
    mret = xr.pct_change()
    # beta: E+1..E+250
    win = slice(E + 1, min(E + 251, len(df)))
    y = ret.iloc[win]; xm = mret.iloc[win]
    ok = y.notna() & xm.notna()
    beta = np.nan
    if ok.sum() >= 60:
        beta = np.cov(y[ok], xm[ok])[0, 1] / np.var(xm[ok], ddof=1)
    out["beta"] = beta
    b = beta if np.isfinite(beta) else 1.0
    # seri sonrası: girişler
    entries = {"Ekap": (E, adj.iloc[E]), "Eaof": (E, aof_adj if pd.notna(aof_adj) else np.nan), "E1kap": (E + 1, adj.iloc[E + 1] if E + 1 < len(df) else np.nan)}
    if E + 1 < len(df):
        out["E1_kilit_tavan"] = bool(is_tav.iloc[E + 1] and locked.iloc[E + 1]) if has_ht.iloc[E + 1] else np.nan
    for nm, (i0, p0) in entries.items():
        for h in H:
            i1 = i0 + h
            if i1 >= len(df) or not np.isfinite(p0):
                continue
            Ri = adj.iloc[i1] / p0 - 1
            Rm = xr.iloc[i1] / xr.iloc[i0] - 1
            ar = (ret.iloc[i0 + 1:i1 + 1] - mret.iloc[i0 + 1:i1 + 1])
            arb = (ret.iloc[i0 + 1:i1 + 1] - b * mret.iloc[i0 + 1:i1 + 1])
            if nm == "Eaof":  # AOF girişte ilk gün getirisi kapanışa göre ayrıca eklenir
                ar = pd.concat([pd.Series([adj.iloc[i0] / p0 - 1]), ar])
                arb = pd.concat([pd.Series([adj.iloc[i0] / p0 - 1]), arb])
            out[f"{nm}_R{h}"] = Ri
            out[f"{nm}_BH{h}"] = Ri - Rm
            out[f"{nm}_CAR{h}"] = ar.sum()
            out[f"{nm}_CARb{h}"] = arb.sum()
    # gün1 kapanışından alan (ikincil piyasa) — kilitliyse dolmaz
    for h in (5, 21, 63):
        if h < len(df):
            out[f"G1_BH{h}"] = (adj.iloc[h] / adj.iloc[0] - 1) - (xr.iloc[h] / xr.iloc[0] - 1)
            out[f"G1_R{h}"] = adj.iloc[h] / adj.iloc[0] - 1
    # seri içi kilitsiz tavan kapanışından alış -> ertesi gün
    for i in range(0, n):
        if i + 1 < len(df) and has_ht.iloc[i]:
            daily.append(dict(kod=kod, gun=i + 1, tarih=df.index[i], kilit=bool(locked.iloc[i]), ertesi=ret.iloc[i + 1],
                              ertesi_tavan=bool(is_tav.iloc[i + 1])))
    # lock-up
    L0 = d1 + pd.Timedelta(days=int(r.lockup_gun))
    idxL = df.index.searchsorted(L0)
    out["L"] = df.index[idxL] if idxL < len(df) else pd.NaT
    if idxL < len(df) and idxL - 20 >= 0:
        ar = ret - mret
        arb = ret - b * mret
        for nm, a0, a1 in (("m10m1", -10, -1), ("0p5", 0, 5), ("0p20", 0, 20), ("m20p20", -20, 20)):
            if idxL + a1 < len(df):
                out[f"LU_{nm}"] = ar.iloc[idxL + a0: idxL + a1 + 1].sum()
                out[f"LUb_{nm}"] = arb.iloc[idxL + a0: idxL + a1 + 1].sum()
        out["LU_fiyat_vs_arz"] = gross.iloc[idxL - 1] - 1  # lock-up öncesi fiyat arz fiyatının ne kadar üstünde
    return out, daily


def adjustment_check(kods):
    """Düzeltme kontrolü: düzeltilmemiş seride |getiri|>11% sıçrama günleri vs düzeltilmiş seri."""
    rows = []
    for k in kods:
        df = load_stock(k, pd.Timestamp("2019-01-01"))
        if df is None or df["HG_KAPANIS"].isna().all():
            continue
        rr = df["HG_KAPANIS"].pct_change(); ra = df["adj"].pct_change()
        j = rr[(rr.abs() > 0.11)].index
        for d in j[1:] if len(j) and j[0] == df.index[0] else j:
            rows.append(dict(kod=k, tarih=d, ham=rr.loc[d], duz=ra.loc[d]))
        big = ra[(ra.abs() > 0.105)].iloc[1:] if len(ra) > 1 else ra.iloc[0:0]
        for d in big.index:
            if not (rr.abs() > 0.11).get(d, False):
                rows.append(dict(kod=k, tarih=d, ham=rr.get(d), duz=ra.loc[d], tip="duz_buyuk"))
    return pd.DataFrame(rows)


def main():
    ipo = pd.read_csv(os.path.join(OUT, "ipo_tablo.csv"), parse_dates=["ilk_islem_hz"])
    ipo = ipo[(ipo.haric.isna()) | (ipo.haric == "")].copy()
    xu = load_xu()
    res, dl = [], []
    for r in ipo.itertuples():
        o, d = analyze_one(r, xu)
        if o is None:
            print("veri yok", r.kod); continue
        res.append(o)
        if d:
            dl += d
    ev = pd.DataFrame(res).merge(ipo, on="kod", how="left")
    ev["yil"] = ev["d1"].dt.year
    ev.to_csv(os.path.join(OUT, "ipo_olay.csv"), index=False)
    pd.DataFrame(dl).to_csv(os.path.join(OUT, "seri_ici_gunler.csv"), index=False)
    adj = adjustment_check(ev.kod.tolist())
    adj.to_csv(os.path.join(OUT, "duzeltme_kontrol.csv"), index=False)
    print("arz:", len(ev), "seri sansürlü:", int(ev.sansur.sum()), "HT yok:", int(ev.get("ht_yok", pd.Series(dtype=bool)).fillna(False).sum()))
    print("ilk işlem tarihi farkı (veri - halkarz) gün dağılımı:", ev.d1_fark_hz.value_counts().to_dict())


if __name__ == "__main__":
    main()
