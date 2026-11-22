"""F4: aracın kendi fiyatından hesaplanan dönüş ve momentum kuralları (YONTEM.md bölüm 4, F4).

Önceden sabit kurallar (her bacak ayrı sinyal; parametre taraması yok):
  IBS < 0,2 AL / > 0,8 SAT; RSI(2) < 10 AL / > 90 SAT; 3 gün üst üste düşük kapanış AL / yükseliş SAT;
  günlük getiri z <= -1,5 AL / >= +1,5 SAT; 5 günlük getiri z <= -1,5 AL / >= +1,5 SAT;
  kapanış 20 günlük zirvede AL (momentum) / dipte SAT; MAC(5) s = -(4r_t+3r_{t-1}+2r_{t-2}+r_{t-3}) > 0 AL.
Koşullar: yok, VIX>20, VIX<=20, VIX>25, hedef 200 günlük ortalamanın üstü / altı. Ufuk h = 1, 2, 3.
Hedefler: geniş, sektör, alt sektör, ülke, emtia, tahvil/kredi ETF'leri tek tek (islem_testi); h_* hisse grupları
portföy olarak (havuz_testi); kesitsel kurallar (havuz_testi).

Kullanım: python3 kod/f4_kendi.py      (tek çalıştırma <= ~5 dk; bitmediyse tekrar çalıştır, kaldığı yerden sürer)
Çıktı   : ek/backtest/f4_kendi/{sonuclar.csv, ayakta_kalanlar.csv, gece_primi.csv, bugun.csv, ozet.txt, ...}
"""
import os
import sys
import time
import pickle
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

CIK = os.path.join(o.KOK, "ek", "backtest", "f4_kendi")
ARA = os.path.join(CIK, "ara")
BUTCE = 260  # saniye
T0 = time.time()

KURALLAR = [("IBS_AL", 1), ("IBS_SAT", -1), ("RSI2_AL", 1), ("RSI2_SAT", -1), ("UC_DUSUS_AL", 1), ("UC_YUKSELIS_SAT", -1),
            ("Z1_AL", 1), ("Z1_SAT", -1), ("Z5_AL", 1), ("Z5_SAT", -1), ("MOM20_AL", 1), ("MOM20_SAT", -1), ("MAC5_AL", 1)]
DONUS_AL = {"IBS_AL", "RSI2_AL", "UC_DUSUS_AL", "Z1_AL", "Z5_AL", "MAC5_AL"}
KOSULLAR = ["yok", "vix_gt20", "vix_le20", "vix_gt25", "ust200", "alt200"]
UFUK = (1, 2, 3)
ETF_GRUP = ["genis_etf", "sektor_etf", "ulke_etf", "emtia_etf", "tahvil_kredi", "alt_enerji", "alt_finans",
            "alt_gayrimenkul_altyapi", "alt_malzeme", "alt_saglik", "alt_sanayi", "alt_teknoloji", "alt_tuketim"]
EMTIA8 = ["GLD", "SLV", "USO", "UNG", "DBA", "DBB", "CPER", "DBC"]
KRIZ = [("2008-09-01", "2009-06-30"), ("2020-02-01", "2020-04-30")]


# ------------------------------------------------------------------------------------------------ evren
def etf_hedefler():
    return sorted(set(s for g in ETF_GRUP for s in o.grup(g) if not o.kaldiracli(s)))


def alt_etfler():
    return sorted(set(s for g in ETF_GRUP if g.startswith("alt_") for s in o.grup(g) if not o.kaldiracli(s)))


def hisse_gruplari():
    m = o.meta()
    gs = sorted(set(x for y in m.gruplar.astype(str) for x in y.split(";") if x.startswith("h_")))
    abd = set(o.abd_semboller("EQUITY"))
    return {g: [s for s in o.grup(g) if s in abd] for g in gs}


# ------------------------------------------------------------------------------------------------ sinyaller
def kural_sinyalleri(sem):
    """Her kural için DataFrame (+1 AL / -1 SAT / 0). t değeri yalnız t kapanışına kadarki fiyatla."""
    c = o.panel("adjclose", sem)
    hi, lo = o.panel("ah", sem), o.panel("al", sem)
    r = c.pct_change(fill_method=None)
    rng = (hi - lo)
    ibs = ((c - lo) / rng).where(rng > 0)
    d = c.diff()
    au = d.clip(lower=0).ewm(alpha=0.5, adjust=False, min_periods=2).mean()
    ad = (-d).clip(lower=0).ewm(alpha=0.5, adjust=False, min_periods=2).mean()
    rsi = 100 - 100 / (1 + au / ad)
    rsi = rsi.where(c.notna() & d.notna())  # ad == 0 ve au > 0 ise 100; ikisi 0 ise NaN
    sd = r.rolling(60, min_periods=40).std().shift(1)
    z1 = r / sd
    z5 = r.rolling(5).sum() / (sd * np.sqrt(5))
    mx, mn = c.rolling(20, min_periods=20).max(), c.rolling(20, min_periods=20).min()
    mac = -(4 * r + 3 * r.shift(1) + 2 * r.shift(2) + r.shift(3))
    k = {
        "IBS_AL": ibs < 0.2, "IBS_SAT": ibs > 0.8,
        "RSI2_AL": rsi < 10, "RSI2_SAT": rsi > 90,
        "UC_DUSUS_AL": (r < 0) & (r.shift(1) < 0) & (r.shift(2) < 0),
        "UC_YUKSELIS_SAT": (r > 0) & (r.shift(1) > 0) & (r.shift(2) > 0),
        "Z1_AL": z1 <= -1.5, "Z1_SAT": z1 >= 1.5,
        "Z5_AL": z5 <= -1.5, "Z5_SAT": z5 >= 1.5,
        "MOM20_AL": c >= mx, "MOM20_SAT": c <= mn,
        "MAC5_AL": mac > 0,
    }
    yon = dict(KURALLAR)
    return {a: ((v & c.notna()).astype(np.float32) * yon[a]).astype(np.float32) for a, v in k.items()}


def kosul_maskeleri(sem, vix_gecikme=0):
    c = o.panel("adjclose", sem)
    vix = o.panel("close", ["^VIX"])["^VIX"].reindex(c.index).shift(vix_gecikme)
    ma = c.rolling(200, min_periods=200).mean()
    bos = pd.DataFrame(True, index=c.index, columns=c.columns)
    vx = lambda m: bos.mul(m.fillna(False).values, axis=0).astype(bool)  # noqa: E731
    return {"yok": bos, "vix_gt20": vx(vix > 20), "vix_le20": vx(vix <= 20), "vix_gt25": vx(vix > 25),
            "ust200": (c > ma).fillna(False), "alt200": (c < ma).fillna(False)}


def kesitsel_sinyaller(vix_gecikme=0):
    """Önceden sabit kesitsel kurallar: dict ad -> (DataFrame sinyal, aciklama)."""
    vix = o.panel("close", ["^VIX"])["^VIX"].shift(vix_gecikme)
    out = {}

    def sec(c, gun, k, en_kotu, min_n):
        g = c / c.shift(gun) - 1
        rk = g.rank(axis=1, ascending=en_kotu, method="first")
        say = g.notna().sum(axis=1)
        return ((rk <= k) & g.notna()).astype(float).where(say >= min_n, 0.0)

    sek = o.grup("sektor_etf")
    c = o.panel("adjclose", sek)
    s = sec(c, 5, 2, True, 9)
    out["KES_SEK5_KOTU2"] = s
    out["KES_SEK5_KOTU2_VIX25"] = s.mul((vix.reindex(s.index) > 25).astype(float).values, axis=0)
    out["KES_SEK1_KOTU3"] = sec(c, 1, 3, True, 9)
    alt = alt_etfler()
    out["KES_ALT21_IYI3"] = sec(o.panel("adjclose", alt), 21, 3, False, 10)
    out["KES_EMT63_IYI2"] = sec(o.panel("adjclose", EMTIA8), 63, 2, False, 6)
    return out


# ------------------------------------------------------------------------------------------------ yardımcılar
def on_eleme(d):
    return (d.get("is_t_anormal") or 0) >= 2.0 and (d.get("oos_t_anormal") or 0) >= 1.5 and (d.get("is_anormal_net_bps") or 0) > 0


def havuz_plasebo(S, h, n=1000, min_k=60, tohum=0):
    """plasebo_dairesel'in portföy karşılığı (kütüphanede yok): sinyal matrisinin satırları dairesel kaydırılır,
    gün bazlı eşit ağırlıklı sürüklenme düzeltilmiş (maliyetsiz) ortalama karşılaştırılır."""
    cols = list(S.columns)
    F = o.ileri_getiri(cols, h)
    Sv = S[cols].reindex(F.index).fillna(0.0).values
    A = (F - F.mean()).values
    ok = ~np.isnan(A)
    A0 = np.nan_to_num(A)

    def stat(X):
        act = (X != 0) & ok
        k = act.sum(1)
        pr = (X * A0 * act).sum(1)
        m = k > 0
        return (pr[m] / k[m]).mean() if m.any() else np.nan

    gercek = stat(Sv)
    T = len(Sv)
    if (Sv != 0).any(axis=1).sum() < 20 or T < 2 * min_k + 10:
        return {"plasebo_p": np.nan, "plasebo_ort_bps": np.nan}
    ks = np.random.default_rng(tohum).integers(min_k, T - min_k, n)
    st = np.array([stat(np.roll(Sv, int(k), axis=0)) for k in ks])
    return {"plasebo_p": round(float((np.sum(st >= gercek) + 1) / (n + 1)), 4), "plasebo_ort_bps": round(float(np.nanmean(st)) * 1e4, 2)}


def havuz_ek(S, h):
    """Portföy testleri için F, E, H, I ölçütleri (kütüphanenin havuz araçlarıyla)."""
    hg = o.havuz_gunluk(S, h)
    v = hg.dropna()
    yil = v.groupby(v.index.year).agg(["mean", "size"])
    yil = yil[yil["size"] >= 3]
    kal = v.sort_values(ascending=False).iloc[10:]
    z = pd.Series(0.0, index=hg.index)
    z[kal.index] = kal
    ac = o.havuz_testi(S, h, giris="acilis")
    er = o.havuz_testi(S, h, giris="ertesi")
    out = {"yil_pozitif_oran": round(float((yil["mean"] > 0).mean()), 2) if len(yil) else np.nan, "yil_sayisi": len(yil),
           "tum_net_bps_ust10_haric": round(float(kal.mean()) * 1e4, 1), "tum_t_ust10_haric": round(float(o.hac_t(z.values, h - 1)), 2),
           "acilis_anormal_bps": ac.get("anormal_net_bps"), "acilis_net_bps": ac.get("net_bps"), "acilis_t_anormal": ac.get("t_anormal"),
           "ertesi_anormal_bps": er.get("anormal_net_bps"), "ertesi_t_anormal": er.get("t_anormal")}
    out.update(havuz_plasebo(S, h))
    return out


def havuz_satir(S, h):
    d = o.havuz_donemli(S, h)
    for p in ("tum", "is", "oos", "son"):
        d[f"{p}_n"] = d.get(f"{p}_n_gun", 0)
    return d


# ------------------------------------------------------------------------------------------------ işçiler
SIG = MASK = GRUP = KES = BAYAT = None


def etf_is(hedef):
    rows = []
    bayat = hedef in BAYAT
    giris = "acilis" if bayat else "kapanis"
    for kural, yon in KURALLAR:
        base = SIG[kural][hedef]
        for kos in KOSULLAR:
            sig = base.where(MASK[kos][hedef], 0.0)
            if (sig != 0).sum() < 30:
                continue
            for h in UFUK:
                d = o.donemli_test(sig, hedef, h, giris=giris)
                if d.get("tum_n", 0) < 30:
                    continue
                row = {"aile": "F4", "sinyal_id": f"{kural}|{kos}|{hedef}|h{h}", "oncu": "KENDI", "hedef": hedef, "bicim": kural,
                       "kosul": kos, "yon": "AL" if yon > 0 else "SAT", "h": h, "havuz": "tek hedef", "bayat_isaret": bayat,
                       "tur": "ETF", **d}
                if on_eleme(d):
                    row.update(o.ek_olcutler(sig, hedef, h))
                row.update(o.son_sinyal(sig))
                rows.append(row)
    return rows


def grup_is(ad):
    rows = []
    if ad.startswith("KES_"):
        S0 = KES[ad]
        isler = [(ad, "yok", S0)]
        tur = "kesitsel"
    else:
        cols = GRUP[ad]
        isler = []
        for kural, _ in KURALLAR:
            base = SIG[kural][cols]
            for kos in KOSULLAR:
                isler.append((kural, kos, base.where(MASK[kos][cols], 0.0)))
        tur = "hisse_grubu"
    for kural, kos, S in isler:
        if (S != 0).values.sum() < 30:
            continue
        yon = "SAT" if kural.endswith("SAT") else "AL"
        for h in UFUK:
            d = havuz_satir(S, h)
            if d.get("tum_n", 0) < 30:
                continue
            row = {"aile": "F4", "sinyal_id": f"{kural}|{kos}|{ad}|h{h}", "oncu": "KENDI", "hedef": ad, "bicim": kural, "kosul": kos,
                   "yon": yon, "h": h, "havuz": "portföy", "bayat_isaret": False, "tur": tur, **d}
            if on_eleme(d):
                row.update(havuz_ek(S, h))
            son = S.iloc[-1]
            row.update({"son_gun": str(S.index[-1].date()), "son_sinyal": float((son != 0).mean()) * (1 if yon == "AL" else -1),
                        "son_acik_hedef": ";".join(son[son != 0].index)})
            rows.append(row)
    return rows


def calis(birim):
    yol = os.path.join(ARA, birim + ".pkl")
    rows = grup_is(birim) if (birim.startswith("h_") or birim.startswith("KES_")) else etf_is(birim)
    pickle.dump(rows, open(yol, "wb"))
    return birim, len(rows)


# ------------------------------------------------------------------------------------------------ sınıflandırma
def sinifla(df):
    """ortak.siniflandir + kütüphanede eksik iki kural (YONTEM.md bölüm 6):
    D: SAT bacağında ham net >= 0; I: 20 bps sınıfındaki hedefte ertesi açılış girişinin neti > 0."""
    x = df.copy()
    sat_kotu = (x.yon == "SAT") & (pd.to_numeric(x.tum_net_bps, errors="coerce") < 0)
    x.loc[sat_kotu, "tum_anormal_net_bps"] = np.nan
    pahali = pd.to_numeric(x.get("tum_maliyet_ort_bps"), errors="coerce") >= 15
    if "acilis_net_bps" in x.columns:
        kotu_ac = pahali & ~(pd.to_numeric(x.acilis_net_bps, errors="coerce") > 0)
        x.loc[kotu_ac, "acilis_anormal_bps"] = np.nan
    tavan = (x.tur == "hisse_grubu") & x.bicim.isin(DONUS_AL)
    x = o.siniflandir(x, tavan_kosullu=tavan)
    for c in x.columns:
        if c.startswith("k_") or c in ("sinif", "p_oos", "bh_oos"):
            df[c] = x[c]
    df["tavan_kosullu"] = tavan
    return df


# ------------------------------------------------------------------------------------------------ ana akış
def sinyal_getir(row, sig=None, mask=None, kes=None):
    """Satırın sinyalini yeniden üret (Series ya da DataFrame)."""
    sig, mask, kes = sig or SIG, mask or MASK, kes or KES
    if row["tur"] == "kesitsel":
        return kes[row["bicim"]]
    cols = row["hedef"] if row["tur"] == "ETF" else GRUP[row["hedef"]]
    return sig[row["bicim"]][cols].where(mask[row["kosul"]][cols], 0.0)


def sagamlik(ak):
    """Ayakta kalanlar için: SPY'dan arındırma, gece/gün içi ayrışması, VIX 1 gün gecikme, maliyet x2, kriz hariç."""
    mask_g = kosul_maskeleri(list(SIG["IBS_AL"].columns), vix_gecikme=1)
    kes_g = kesitsel_sinyaller(vix_gecikme=1)
    out = []
    for _, r in ak.iterrows():
        s = sinyal_getir(r)
        h = int(r.h)
        e = {"sinyal_id": r.sinyal_id}
        tek = r.tur == "ETF"
        giris = "acilis" if (tek and r.bayat_isaret) else "kapanis"
        if tek:
            if r.hedef != "SPY":
                d = o.donemli_test(s, r.hedef, h, giris=giris, hedge="SPY")
            else:
                d = {}
            g = o.islem_testi(s, r.hedef, h, 0, "gece")
            a = o.islem_testi(s, r.hedef, h, 0, "acilis")
            k = o.islem_testi(s, r.hedef, h, 0, "kapanis")
            m2 = o.donemli_test(s, r.hedef, h, o.maliyet_serisi(r.hedef) * 2, giris=giris)
            sk = s.copy()
            for b, t in KRIZ:
                sk[(sk.index >= b) & (sk.index <= t)] = 0.0
            kr = o.islem_testi(sk, r.hedef, h, None, giris)
            vg = o.donemli_test(sinyal_getir(r, mask=mask_g, kes=kes_g), r.hedef, h, giris=giris) if r.kosul.startswith("vix") else {}
        else:
            d = o.havuz_donemli(s, h, hedge="SPY")
            g = o.havuz_testi(s, h, 0, "gece")
            a = o.havuz_testi(s, h, 0, "acilis")
            k = o.havuz_testi(s, h, 0, "kapanis")
            m2 = {}
            sk = s.copy()
            for b, t in KRIZ:
                sk[(sk.index >= b) & (sk.index <= t)] = 0.0
            kr = o.havuz_testi(sk, h)
            vg = (o.havuz_donemli(sinyal_getir(r, mask=mask_g, kes=kes_g), h)
                  if (r.kosul.startswith("vix") or "VIX" in r.bicim) else {})
        e["spy_is_t"], e["spy_oos_t"] = d.get("is_t_anormal"), d.get("oos_t_anormal")
        e["spy_tum_bps"], e["spy_son_bps"] = d.get("tum_anormal_net_bps"), d.get("son_net_bps")
        e["sektore_ozgu"] = bool((d.get("is_t_anormal") or 0) >= 2 and (d.get("oos_t_anormal") or 0) >= 2)
        e["brut_kapanis_bps"] = k.get("brut_bps", k.get("net_bps"))
        e["brut_gece_bps"] = g.get("brut_bps", g.get("net_bps"))
        e["brut_sonrasi_bps"] = a.get("brut_bps", a.get("net_bps"))
        bk = e["brut_kapanis_bps"]
        e["gece_payi"] = round(e["brut_gece_bps"] / bk, 2) if bk else np.nan
        e["maliyet2x_tum_bps"], e["maliyet2x_oos_t"] = m2.get("tum_anormal_net_bps"), m2.get("oos_t_anormal")
        e["kriz_haric_bps"], e["kriz_haric_t"] = kr.get("anormal_net_bps"), kr.get("t_anormal")
        e["vix_gec1_is_t"], e["vix_gec1_oos_t"] = vg.get("is_t_anormal"), vg.get("oos_t_anormal")
        e["vix_gec1_tum_bps"] = vg.get("tum_anormal_net_bps")
        out.append(e)
    return pd.DataFrame(out)


def gece_primi(hedefler):
    sat = []
    for hd in hedefler:
        bir = pd.Series(1.0, index=o.takvim())
        row = {"hedef": hd}
        for ad, gir in (("gece", "gece"), ("gunici", "acilis")):
            d = o.donemli_test(bir, hd, 1, 0, gir)
            for p in ("is", "oos", "son"):
                row[f"{ad}_{p}_bps"] = d.get(f"{p}_brut_bps")
                row[f"{ad}_{p}_t"] = d.get(f"{p}_t_net")
        sat.append(row)
    return pd.DataFrame(sat)


def bugun_tablosu():
    sat = []
    son = SIG["IBS_AL"].index[-1]
    for hd in etf_hedefler():
        row = {"hedef": hd, "tarih": str(son.date())}
        for kural, _ in KURALLAR:
            row[kural] = SIG[kural].at[son, hd]
        for kos in KOSULLAR[1:]:
            row[kos] = bool(MASK[kos].at[son, hd])
        sat.append(row)
    for g, cols in GRUP.items():
        row = {"hedef": g, "tarih": str(son.date())}
        for kural, _ in KURALLAR:
            row[kural] = round(float((SIG[kural].loc[son, cols] != 0).mean()), 2)
        sat.append(row)
    for k, S in KES.items():
        sat.append({"hedef": k, "tarih": str(son.date()), "secilen": ";".join(S.columns[S.iloc[-1] != 0])})
    return pd.DataFrame(sat)


def main():
    global SIG, MASK, GRUP, KES, BAYAT
    os.makedirs(ARA, exist_ok=True)
    hed = etf_hedefler()
    GRUP = hisse_gruplari()
    BAYAT = o.bayat_hedefler()
    sem = sorted(set(hed) | set(s for v in GRUP.values() for s in v) | {"SPY"})
    SIG = kural_sinyalleri(sem)
    MASK = kosul_maskeleri(sem)
    KES = kesitsel_sinyaller()
    birimler = sorted(GRUP) + sorted(KES) + hed
    bekleyen = [b for b in birimler if not os.path.exists(os.path.join(ARA, b + ".pkl"))]
    print(f"{len(birimler)} birim, bekleyen {len(bekleyen)}", flush=True)
    if bekleyen:
        with Pool(3) as p:
            for i, (b, n) in enumerate(p.imap_unordered(calis, bekleyen), 1):
                if i % 10 == 0:
                    print(f"  {i}/{len(bekleyen)} ({time.time() - T0:.0f} sn)", flush=True)
                if time.time() - T0 > BUTCE and i < len(bekleyen):
                    p.terminate()
                    print("Süre bütçesi doldu; tekrar çalıştır (kaldığı yerden sürer).")
                    return
    rows = []
    for b in birimler:
        rows += pickle.load(open(os.path.join(ARA, b + ".pkl"), "rb"))
    df = sinifla(pd.DataFrame(rows))
    on = ["aile", "sinyal_id", "oncu", "hedef", "bicim", "kosul", "yon", "h", "havuz", "bayat_isaret", "tur"]
    df = df[on + [c for c in df.columns if c not in on]]
    ak = df[df.sinif != "ELENDI"].copy()
    sy = os.path.join(CIK, "saglamlik.pkl")
    if os.path.exists(sy):
        sg = pd.read_pickle(sy)
    else:
        sg = sagamlik(ak)
        sg.to_pickle(sy)
    ak = ak.merge(sg, on="sinyal_id", how="left")
    sira = {"SAGLAM": 0, "KOSULLU": 1, "IZLE": 2}
    ak = ak.assign(_s=ak.sinif.map(sira)).sort_values(["_s", "oos_t_anormal"], ascending=[True, False]).drop(columns="_s")
    df.to_csv(os.path.join(CIK, "sonuclar.csv"), index=False)
    ak.to_csv(os.path.join(CIK, "ayakta_kalanlar.csv"), index=False)
    gp = os.path.join(CIK, "gece_primi.csv")
    if not os.path.exists(gp):
        gece_primi(hed).to_csv(gp, index=False)
    bugun_tablosu().to_csv(os.path.join(CIK, "bugun.csv"), index=False)
    # aynı gün açık sinyal sayısı ve korelasyon (tek hedefli ayakta kalanlar)
    tek = ak[ak.tur == "ETF"].drop_duplicates(["bicim", "kosul", "hedef"])
    ind = pd.DataFrame({r.sinyal_id: (sinyal_getir(r) != 0).astype(float) for _, r in tek.iterrows()})
    pnl = pd.DataFrame({r.sinyal_id: o.gunluk_pnl(sinyal_getir(r), r.hedef, int(r.h), 5) for _, r in tek.iterrows()})
    rapor = [f"TOPLAM TEST: {len(df)} (tek hedef {int((df.havuz == 'tek hedef').sum())}, portföy {int((df.havuz == 'portföy').sum())})",
             f"Beklenen yanlış pozitif (bağımsızlık varsayımıyla): SAGLAM {len(df) * o.P_SIFIR_SAGLAM:.2f}, KOSULLU {len(df) * o.P_SIFIR_KOSULLU:.2f}",
             "Sınıflar: " + str(df.sinif.value_counts().to_dict()),
             "Eleme basamakları: k_A %d; k_A&OOS t>=2: %d; k_A&OOS t>=2,5: %d; k_A&BH: %d" % (
                 df.k_A.sum(), (df.k_A & df.k_B_zayif).sum(), (df.k_A & df.k_B).sum(), (df.k_A & df.bh_oos).sum())]
    if len(ind.columns):
        say = ind.sum(axis=1)
        say = say[say > 0]
        rapor.append("Aynı gün açık tek hedefli ayakta kalan sinyal sayısı (en az 1 olan günler): " +
                     str(say.describe(percentiles=[.5, .9, .99]).round(1).to_dict()))
        for ad, M in (("gösterge", ind), ("günlük pnl", pnl)):
            cm = M.corr().values
            ust = cm[np.triu_indices_from(cm, 1)]
            rapor.append(f"Çiftler arası korelasyon ({ad}): ortalama {np.nanmean(ust):.2f}, medyan {np.nanmedian(ust):.2f}, "
                         f">0,5 oranı {np.nanmean(ust > 0.5):.2f} ({len(M.columns)} sinyal)")
        pnl.corr().round(2).to_csv(os.path.join(CIK, "korelasyon_pnl.csv"))
    rapor.append("Sınıf x kural:\n" + df[df.sinif != "ELENDI"].groupby(["bicim", "sinif"]).size().unstack(fill_value=0).to_string())
    open(os.path.join(CIK, "ozet.txt"), "w").write("\n".join(rapor))
    print("\n".join(rapor))
    print(f"bitti ({time.time() - T0:.0f} sn)")


if __name__ == "__main__":
    main()
