"""rehber_tuprs_kur — PRATİK kuralın backtest'i (VİOP uzlaşma fiyatlarıyla, tutulan kontratın kendi fiyatları).
Kural (araştırma c1_ref.py ile aynı sinyal; işlem mekaniği kullanıcının uygulayacağı biçimde):
  - z_t = araştırma z'si (ABD t-1 kapanışlarından; BIST t kapanışından ÖNCE tamamen bilinir).
  - Pozisyon yokken |z_t|>1 -> yön(z_t) ile, t'de vadeye >=3 BIST işlem günü kalan en yakın TUPRS kontratını t uzlaşmasında aç.
  - Çıkış günü e = t+2 (BIST işlem günü). e'de |z_e|>1 ve aynı yön -> UZAT (2 gün daha; kontratın e'de <3 iş günü kaldıysa roll),
    ters yön -> ÇEVİR (kapat + ters aç), aksi halde e uzlaşmasında KAPAT. Kapatılan günün ertesinden itibaren yeni sinyal aranır.
  - Uzatma sınırı yok (araştırmadaki trades() ile birebir aynı işlem dizisi).
Çıktılar: sonuc/pratik_bloklar.csv, sonuc/pratik_pozisyonlar.csv, sonuc/pratik_ozet.json (+ ekrana özet)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, cl_t as cl

H, THR, SPLIT = 2, 1.0, pd.Timestamp("2022-01-01")
z, Pb, P, RS = cl.signal_z()
c = cl.cal(); n = len(c); pos_of = {d: i for i, d in enumerate(c)}
X = cl.contracts("TUPRS").copy()
X = X[X["settle"] > 0].sort_values(["code", "date"])
X["prev_same"] = X.groupby("code")["settle"].shift(1)
X["pdate"] = X.groupby("code")["date"].shift(1)
ps = X["prev_settle"].where(X["prev_settle"] > 0)
# prev_settle eksikse aynı kontratın bir önceki uzlaşması (yalnız bir önceki BIST günüyse)
cal_prev = pd.Series(c[:-1], index=c[1:])
okprev = X["pdate"].values == cal_prev.reindex(X["date"]).values
ps = ps.fillna(pd.Series(np.where(okprev, X["prev_same"], np.nan), index=X.index))
X["lr"] = np.log(X["settle"] / ps)
K = X.set_index(["date", "code"])
FR = cl.front("TUPRS")
zv = z.reindex(c).values

def tick(d):  # VİOP TUPRS fiyat adımı: uzlaşma ondalıklarından çıkarıldı (2025 öncesi 0,01; 2025+ 0,05)
    return 0.05 if d >= pd.Timestamp("2025-01-01") else 0.01

def seg(code, i0, i1):
    """code kontratında c[i0] uzlaşmasından c[i1] uzlaşmasına log getiri; eksik gün varsa NaN."""
    s = 0.0
    for j in range(i0 + 1, i1 + 1):
        key = (c[j], code)
        if j >= n or key not in K.index: return np.nan
        v = K.at[key, "lr"]
        if not np.isfinite(v): return np.nan
        s += v
    return s

def px(code, i, col):
    key = (c[i], code)
    return float(K.at[key, col]) if key in K.index else np.nan

def td_left(code, i):
    key = (c[i], code)
    return int(K.at[key, "td_left"]) if key in K.index else -1

def run(zv, h=H, thr=THR):
    blocks = []; i = 0
    while i < n:
        zi = zv[i]
        if not (np.isfinite(zi) and abs(zi) > thr and c[i] in FR.index):
            i += 1; continue
        d = np.sign(zi); code = FR.at[c[i], "code"]; kind = "yeni"; pid = len(blocks)
        # açılış: bloğun verisi tam değilse (gelecekte eksik gün) araştırmadaki gibi atla — örneklem sonu hariç
        if i + h < n and not np.isfinite(seg(code, i, i + h)):
            i += 1; continue
        s = i
        while True:
            e = s + h
            if e >= n:  # açık pozisyon (örneklem sonu)
                blocks.append(dict(pid=pid, kind=kind, d=d, code=code, s=c[s], e=pd.NaT, i_s=s, i_e=np.nan, open=True)); i = n; break
            g = seg(code, s, e)
            blocks.append(dict(pid=pid, kind=kind, d=d, code=code, s=c[s], e=c[e], i_s=s, i_e=e, open=False, g=g,
                               entry=px(code, s, "settle"), exitp=px(code, e, "settle"), cls_s=px(code, s, "close"), cls_e=px(code, e, "close"),
                               td_s=td_left(code, s)))
            ze = zv[e]
            if np.isfinite(ze) and abs(ze) > thr and c[e] in FR.index:
                nd = np.sign(ze)
                if nd == d:
                    ncode = code if td_left(code, e) >= 3 else FR.at[c[e], "code"]
                    if e + h < n and not np.isfinite(seg(ncode, e, e + h)):
                        i = e + 1; break  # veri yok -> kapat
                    kind = "uzatma" if ncode == code else "uzatma+roll"; code = ncode; s = e; continue
                else:
                    i = e; break  # çevir: döngü başı e'de ters yönde yeni pozisyon açar
            i = e + 1; break
    B = pd.DataFrame(blocks)
    return B

def costs_block(B, base):
    tk = np.array([2 * tick(d) / p * 1e4 if p > 0 else np.nan for d, p in zip(B["s"], B["entry"])])
    return base + tk

def summarize(net, idx, label=""):
    net = pd.Series(np.asarray(net, float), index=pd.DatetimeIndex(idx)).dropna()
    yrs = max((net.index[-1] - net.index[0]).days / 365.25, 0.5)
    isd = net.index < SPLIT
    per = {}
    for lab, a, b in [("2017-19", "2017", "2019"), ("2020-21", "2020", "2021"), ("2022-23", "2022", "2023"), ("2024-26", "2024", "2026")]:
        x = net[(net.index >= a) & (net.index < str(int(b) + 1))]; per[lab] = (round(x.mean(), 1), round(cl.tstat(x), 2), len(x))
    srt = net.sort_values(); top10 = srt.iloc[:-10]
    return dict(n=len(net), per_yr=round(len(net) / yrs, 1), net=round(net.mean(), 1), t=round(cl.tstat(net), 2), hit=round((net > 0).mean(), 3),
                IS=(round(net[isd].mean(), 1), round(cl.tstat(net[isd]), 2), int(isd.sum())), OOS=(round(net[~isd].mean(), 1), round(cl.tstat(net[~isd]), 2), int((~isd).sum())),
                periods=per, by_year={int(k): int(round(v)) for k, v in net.groupby(net.index.year).mean().items()},
                drop_top10=(round(top10.mean(), 1), round(cl.tstat(top10), 2)), worst=(str(srt.index[0].date()), round(srt.iloc[0], 0)),
                maxdd_bps=round(float((net.cumsum() - net.cumsum().cummax()).min()), 0))

def _lc(cl_, st):  # kapanış fiyatı / uzlaşma (kapanış yoksa 0: uzlaşmadan dolum)
    return float(np.log(cl_ / st)) if (np.isfinite(cl_) and cl_ > 0 and st > 0) else 0.0

def positions(B, base, fill="settle"):
    rows = []
    for pid, g in B[~B["open"]].groupby("pid", sort=False):
        d = g["d"].iloc[0]; lr = g["g"].sum(); nroll = int((g["kind"] == "uzatma+roll").sum())
        e0 = g["entry"].iloc[0]
        if fill == "close":
            adj = _lc(g["cls_e"].iloc[-1], g["exitp"].iloc[-1]) - _lc(g["cls_s"].iloc[0], g["entry"].iloc[0])
            for k in range(1, len(g)):  # roll noktaları: eski kontrat kapanış fiyatından çık, yeni kontrata kapanış fiyatından gir
                if g["kind"].iloc[k] == "uzatma+roll":
                    adj += _lc(g["cls_e"].iloc[k - 1], g["exitp"].iloc[k - 1]) - _lc(g["cls_s"].iloc[k], g["entry"].iloc[k])
            lr = lr + adj
        cost = sum(base + 2 * tick(g["s"].iloc[k]) / g["entry"].iloc[k] * 1e4 for k in range(len(g)) if k == 0 or g["kind"].iloc[k] == "uzatma+roll")
        gross_bps = d * lr * 1e4
        # DÜZELTME (rehber_tuprs_denetim): vadeli kâr/zararı fiyatta DOĞRUSALDIR. Eski formül 100*e0*(exp(d*lr)-1) kısa
        # pozisyonda 100*e0*(exp(-lr)-1) veriyordu; doğrusu 100*e0*(1-exp(lr)). Fark ≈ 100*e0*lr^2 -> kısa TL kârı şişiyordu
        # (ort. +28 TL/kısa). Ayrıca roll'lu pozisyonda her kontrat kendi giriş fiyatıyla hesaplanır.
        if fill == "settle":
            gross_tl = 0.0; k = 0
            while k < len(g):
                ck = g["code"].iloc[k]; ent = g["entry"].iloc[k]; lrc = 0.0
                while k < len(g) and g["code"].iloc[k] == ck:
                    lrc += g["g"].iloc[k]; k += 1
                gross_tl += d * 100 * ent * (np.exp(lrc) - 1)
        else:
            gross_tl = d * 100 * e0 * (np.exp(lr) - 1)
        net_tl = gross_tl - cost / 1e4 * 100 * e0
        rows.append(dict(pid=pid, giris=g["s"].iloc[0], cikis=g["e"].iloc[-1], yon=int(d), kontrat=g["code"].iloc[0], son_kontrat=g["code"].iloc[-1],
                         blok=len(g), gun=int(g["i_e"].iloc[-1] - g["i_s"].iloc[0]), roll=nroll, giris_fiyat=e0, brut_bps=gross_bps, maliyet_bps=cost,
                         net_bps=gross_bps - cost, brut_tl=gross_tl, net_tl=net_tl, ilk_tur=g["kind"].iloc[0],
                         net_dog_bps=gross_tl / (100 * e0) * 1e4 - cost))
    return pd.DataFrame(rows).set_index("giris")

if __name__ == "__main__":
    out = {}
    B = run(zv)
    Bc = B[~B["open"]].copy()
    Bc["gross_bps"] = Bc["d"] * Bc["g"] * 1e4
    # --- araştırmayla karşılaştırma (blok bazında, her blok tam maliyet) ---
    rflag = cl.front("TUPRS")["roll"]
    y = cl.fwd(cl.fut_ret("TUPRS", "TUPRS.IS"), H); y = y[y.index >= "2017-03-06"]
    trR = cl.trades(z, y, H, THR, rflag)
    m = trR.index.isin(Bc["s"])
    out["arastirma_yeniden_uretim_ayni_veri_2026-11-03"] = summarize(trR["gross"] * 1e4 - 8, trR.index)
    out["blok_eslesme"] = dict(arastirma_n=len(trR), pratik_blok_n=len(Bc), ortak_giris=int(m.sum()),
                               yalniz_arastirma=[str(d.date()) for d in trR.index[~m]][:20],
                               yalniz_pratik=[str(d.date()) for d in Bc["s"][~Bc["s"].isin(trR.index)]][:20])
    J = Bc.set_index("s").join(trR[["gross"]], how="inner")
    out["blok_getiri_farki_bps"] = dict(ort=round(float((J["gross_bps"] - J["gross"] * 1e4).mean()), 2), maks_abs=round(float((J["gross_bps"] - J["gross"] * 1e4).abs().max()), 1),
                                       fark_olan_blok=int(((J["gross_bps"] - J["gross"] * 1e4).abs() > 0.5).sum()))
    for base in (8, 15):
        cb = costs_block(Bc, base)
        out[f"blok_tammaliyet_{base}+tik"] = summarize(Bc["gross_bps"].values - cb, Bc["s"])
    out["blok_brut_bps"] = round(Bc["gross_bps"].mean(), 1)
    out["blok_turleri"] = Bc["kind"].value_counts().to_dict()
    # --- pozisyon bazında (gerçek işlem maliyeti: aç+kapat = 1 tur, roll = +1 tur) ---
    for base in (8, 15):
        for fill in ("settle", "close"):
            Pz = positions(B, base, fill)
            s = summarize(Pz["net_bps"], Pz.index)
            s.update(brut_bps=round(Pz["brut_bps"].mean(), 1), ort_gun=round(Pz["gun"].mean(), 2), gun_dagilim=Pz["gun"].value_counts().sort_index().to_dict(),
                     roll_orani=round((Pz["roll"] > 0).mean(), 3), maliyet_ort=round(Pz["maliyet_bps"].mean(), 1),
                     net_tl_ort=round(Pz["net_tl"].mean(), 0), brut_tl_ort=round(Pz["brut_tl"].mean(), 0),
                     net_tl_2024_26=round(Pz.loc[Pz.index >= "2024-01-01", "net_tl"].mean(), 0),
                     maxdd_tl_1kontrat=round(float((Pz["net_tl"].cumsum() - Pz["net_tl"].cumsum().cummax()).min()), 0),
                     maxdd_tl_2024_26=round(float((Pz.loc[Pz.index >= "2024-01-01", "net_tl"].cumsum() - Pz.loc[Pz.index >= "2024-01-01", "net_tl"].cumsum().cummax()).min()), 0),
                     en_kotu_tl=round(float(Pz["net_tl"].min()), 0), en_kotu_tl_tarih=str(Pz["net_tl"].idxmin().date()), toplam_net_tl=round(float(Pz["net_tl"].sum()), 0),
                     dogrusal_net_bps=round(Pz["net_dog_bps"].mean(), 1), dogrusal_t=round(cl.tstat(Pz["net_dog_bps"]), 2),
                     dogrusal_en_kotu_bps=round(float(Pz["net_dog_bps"].min()), 0),
                     maxdd_tl_2024_26_tarih=(lambda s: (str(s[:(s - s.cummax()).idxmin()].idxmax().date()), str((s - s.cummax()).idxmin().date())))(Pz.loc[Pz.index >= "2024-01-01", "net_tl"].cumsum()),
                     long_net=round(Pz.loc[Pz["yon"] > 0, "net_bps"].mean(), 1), short_net=round(Pz.loc[Pz["yon"] < 0, "net_bps"].mean(), 1),
                     n_long=int((Pz["yon"] > 0).sum()), n_short=int((Pz["yon"] < 0).sum()),
                     q05_brut_bps=round(float(Pz["brut_bps"].quantile(0.05)), 0), q05_brut_bps_2024_26=round(float(Pz.loc[Pz.index >= "2024-01-01", "brut_bps"].quantile(0.05)), 0))
            out[f"pozisyon_{base}+tik_{fill}"] = s
            if base == 8 and fill == "settle":
                Pz.round(2).to_csv(cl.OUT + "/pratik_pozisyonlar.csv"); P8 = Pz
    B.to_csv(cl.OUT + "/pratik_bloklar.csv", index=False)
    # --- geç giriş (sinyal gününü kaçırıp ertesi uzlaşmada girmek) ---
    zl = pd.Series(zv, index=c).shift(1).values
    BL = run(zl); PL = positions(BL, 8, "settle"); out["gec_giris_t+1_8+tik"] = summarize(PL["net_bps"], PL.index)
    # --- roll içeren pozisyonlar ---
    out["roll_iceren_poz_net8"] = (round(P8.loc[P8["roll"] > 0, "net_bps"].mean(), 1), int((P8["roll"] > 0).sum()))
    out["uzatmali_poz_net8"] = (round(P8.loc[P8["blok"] > 1, "net_bps"].mean(), 1), int((P8["blok"] > 1).sum()))
    # --- |z| kovaları (yalnız bilgi; kural değişmez) ---
    zin = pd.Series(zv, index=c).reindex(P8.index).abs()
    kb = pd.cut(zin, [1, 1.5, 2, 3, 99]); out["z_kova_net8"] = {str(k): (round(v.mean(), 1), len(v)) for k, v in P8["net_bps"].groupby(kb)}
    # --- limit günleri: tutulan kontratta |günlük getiri| >= %9,4 (2020-03+ limit ±%10) ---
    lim = X[(X["date"] >= cl.REGIME) & (X["lr"].abs() >= 0.094)]
    hit = 0; hitd = []
    for _, r in Bc.iterrows():
        if not np.isfinite(r["i_e"]): continue
        ds = set(c[int(r["i_s"]) + 1:int(r["i_e"]) + 1])
        L = lim[(lim["code"] == r["code"]) & lim["date"].isin(ds)]
        if len(L): hit += 1; hitd.append(str(r["s"].date()))
    out["limit_gunu_iceren_blok"] = (hit, hitd[:15])
    out["limit_cikis_gunu"] = int(sum(((lim["code"] == r["code"]) & (lim["date"] == r["e"])).any() for _, r in Bc.iterrows() if isinstance(r["e"], pd.Timestamp)))
    out["acik_pozisyon"] = B[B["open"]].astype(str).to_dict("records")
    json.dump(out, open(cl.OUT + "/pratik_ozet.json", "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
