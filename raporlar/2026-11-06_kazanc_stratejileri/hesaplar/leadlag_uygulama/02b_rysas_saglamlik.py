#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02b_rysas_saglamlik.py - Aile P'de FDR'den gecen tek yeni aday: RYGYO_t -> RYSAS r(t -> t+1).
Curutme denemeleri (onceden yazildi, sonuca bakmadan):
  1) yil yil brut/net; en iyi 10 islem haric; 2026 fon krizi (Agu-Eki 2026) haric
  2) yalniz uzun (spot aciga satis yok varsayimi); hedge'siz surum
  3) bir gun gec giris: RYGYO_t -> RYSAS r(t+1 -> t+2)
  4) ters yon: RYSAS_t -> RYGYO r(t -> t+1)
  5) fark bicimi: (r_RYGYO - r_RYSAS)_t -> RYSAS r(t -> t+1)
  6) plasebo: diger GYO'lar (RYGYO yerine) -> RYSAS; ayni regresyon t dagilimi
  7) RYGYO limit (|r|>%9,5) gunleri haric
Plasebo GYO verisi: <scratch>/data/bist_test/hisse/*.parquet (Is Yatirim HisseTekil) -> leadlag2/plasebo/ kopyalanir.
"""
import argparse, os, sys, shutil
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

PLASEBO = ["ISGYO", "SNGYO", "EKGYO", "TRGYO", "ALGYO", "AKFGY", "PSGYO", "VKGYO", "OZKGY", "KLGYO", "AVGYO", "MRGYO",
           "DGGYO", "NUGYO", "YGGYO", "HLGYO", "ZRGYO", "MSGYO", "IDGYO", "AGYO"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cikti", required=True); ap.add_argument("--plasebo-kaynak", required=True)
    a = ap.parse_args()
    cal = o.takvim()
    R = pd.DataFrame({k: o.bist_getiri(k, cal) for k in ["RYSAS", "RYGYO", "XU100"]})
    bx = o.rolling_beta(R["RYSAS"], R["XU100"])
    hed = R["RYSAS"].shift(-1) - bx * R["XU100"].shift(-1)
    ham = R["RYSAS"].shift(-1)
    L = R["RYGYO"]
    sd = L.rolling(250, min_periods=100).std().shift(1); z = (L / sd).clip(-5, 5)
    BAS = pd.Timestamp("2014-01-01")
    m = R.index >= BAS
    out = []

    def kural(sig, y, maliyet, etiket, mask=None):
        pos = pd.Series(np.where(sig.abs() > 1, np.sign(sig), 0.0), index=R.index)
        pnl = (pos * y).where(pos != 0) * 1e4
        if mask is not None:
            pnl = pnl[mask]
        pnl = pnl[pnl.index >= BAS].dropna()
        net = pnl - maliyet
        t = net.mean() / (net.std(ddof=1) / np.sqrt(len(net))) if len(net) > 10 else np.nan
        out.append(f"{etiket}: n {len(net)}, brut {pnl.mean():+.1f}, net {net.mean():+.1f} bps (t {t:+.2f})")
        return pnl

    p = kural(z, hed, 28, "TEMEL (hedge'li, iki yon, 25+3 bps)")
    yil = p.groupby(p.index.year).agg(["count", "mean"]).round(1)
    out.append("Yil yil brut (n, ort bps):\n" + yil.T.to_string())
    s = p.sort_values(ascending=False)
    s10 = s.iloc[10:]; net10 = s10 - 28
    out.append(f"En iyi 10 islem haric: n {len(s10)}, brut {s10.mean():+.1f}, net {net10.mean():+.1f} (t {net10.mean()/(net10.std(ddof=1)/np.sqrt(len(net10))):+.2f})")
    kriz = (p.index >= pd.Timestamp("2026-08-01")) & (p.index <= pd.Timestamp("2026-10-31"))
    pk = p[~kriz] - 28
    out.append(f"Agu-Eki 2026 haric: n {len(pk)}, net {pk.mean():+.1f} (t {pk.mean()/(pk.std(ddof=1)/np.sqrt(len(pk))):+.2f})")
    for a0, a1 in [("2014", "2020"), ("2021", "2023"), ("2024", "2026")]:
        q = p[a0:a1] - 28
        out.append(f"  {a0}-{a1}: n {len(q)}, net {q.mean():+.1f} (t {q.mean()/(q.std(ddof=1)/np.sqrt(len(q))):+.2f})")
    uzun = z.where(z > 0)
    kural(uzun.fillna(0), hed, 28, "YALNIZ UZUN (z>+1), hedge'li")
    kural(uzun.fillna(0), ham, 25, "YALNIZ UZUN, hedge'siz (25 bps)")
    kural(z, ham, 25, "Iki yon, hedge'siz (25 bps)")
    kural(z.shift(1), hed, 28, "BIR GUN GEC GIRIS (RYGYO_t -> RYSAS t+1->t+2)")
    lim = L.abs() > np.log(1.095)
    kural(z.where(~lim, 0), hed, 28, "RYGYO limit gunleri haric")
    # ters yon
    bxg = o.rolling_beta(R["RYGYO"], R["XU100"])
    hedg = R["RYGYO"].shift(-1) - bxg * R["XU100"].shift(-1)
    zr = (R["RYSAS"] / R["RYSAS"].rolling(250, min_periods=100).std().shift(1)).clip(-5, 5)
    kural(zr, hedg, 28, "TERS YON (RYSAS_t -> RYGYO t->t+1)")
    # fark bicimi
    dd = R["RYGYO"] - R["RYSAS"]
    zd = (dd / dd.rolling(250, min_periods=100).std().shift(1)).clip(-5, 5)
    kural(zd, hed, 28, "FARK (RYGYO-RYSAS)_t -> RYSAS")
    # regresyonlar
    def reg(x, y, ad):
        X = np.column_stack([x.values, R["RYSAS"].values, R["XU100"].values])
        yy = y.values.copy(); yy[~m] = np.nan
        b, t, n = o.ols_nw(yy, X)
        out.append(f"REG {ad}: b*sd {b[1]*np.nanstd(x[m])*1e4:+.1f} bps, t {t[1]:+.2f}, own t {t[2]:+.2f}, n {n}")
        return t[1]
    reg(L, ham, "RYGYO_t -> RYSAS_t+1 (temel)")
    reg(L, R["RYSAS"].shift(-2), "RYGYO_t -> RYSAS_t+2 (bir gun gec)")
    reg(dd, ham, "fark_t -> RYSAS_t+1")
    # plasebo
    pdir = os.path.join(o.V, "plasebo"); os.makedirs(pdir, exist_ok=True)
    ts = []
    for k in PLASEBO:
        f = os.path.join(a.plasebo_kaynak, k + ".parquet")
        if not os.path.exists(f):
            continue
        d = pd.read_parquet(f)[["adj", "vol_tl"]]
        d.index = pd.to_datetime(d.index).normalize(); d.index.name = "tarih"
        d.to_csv(os.path.join(o.V, "isy", "_pl_" + k + ".csv"))
        x = o.bist_getiri("_pl_" + k, cal)
        if x[m].notna().sum() < 1000:
            continue
        X = np.column_stack([x.values, R["RYSAS"].values, R["XU100"].values])
        yy = ham.values.copy(); yy[~m] = np.nan
        b, t, n = o.ols_nw(yy, X)
        ts.append((k, round(t[1], 2), n))
    out.append("PLASEBO GYO -> RYSAS (t, n): " + ", ".join(f"{k} {t:+.2f} ({n})" for k, t, n in ts))
    tt = np.array([t for _, t, _ in ts])
    out.append(f"Plasebo t: medyan {np.median(tt):+.2f}, |t|>2 orani {np.mean(np.abs(tt)>2):.2f}, en yuksek {tt.max():+.2f}")
    # guncel
    out.append(f"GUNCEL: son tarih {z.dropna().index[-1].date()}, RYGYO r {L.iloc[-1]*100:+.2f}%, sd250 {sd.iloc[-1]*100:.2f}%, z {z.iloc[-1]:+.2f}; "
               f"esik |z|>1 -> RYGYO gunluk hareket > {sd.iloc[-1]*100:.2f}%")
    txt = "\n".join(out)
    open(os.path.join(a.cikti, "rysas_saglamlik.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
