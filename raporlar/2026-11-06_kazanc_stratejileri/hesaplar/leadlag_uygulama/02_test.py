#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_test.py - Onceden belirlenmis kucuk lead-lag test seti (BIST; kapanistan kapanisa, karar BIST kapanisinda).

ZAMANLAMA (ileriye bakma yok):
  * Yurt ici lider (BIST kapanisi t, 18:10'da bilinir): L_t -> hedef r(t -> t+1).
    Spot hedefte giris 18:10-18:15 'kapanis fiyatindan islemler' penceresinde (sig kapasite).
  * ABD/EIA tarihli lider (ABD gunu d): d'den sonraki ilk BIST gunu t'ye eslenir (t gunu 00:00 TSI'de kesin);
    L_t -> hedef r(t -> t+1)  [= ABD gunu d -> BIST kapanis d+1 -> d+2]; 2 gunluk surum r(t -> t+2).
    Ayni bilginin BIST t gunu (acilis gap'i dahil) ile iliskisi = RISK olcusu (aile S, 'gap gunu').
  * Is Yatirim USDTRY'nin damga saati belirsiz -> once tani (asagida); gec damgaliysa ABD tarihli gibi kaydirilir.

AILE P (ongoru, 38 test): r_T(t+1) = a + b*L_t + c*r_T(t) + d*r_XU100(t) + e ; NW(5) t; etki = b*sd(L) bps/1sd.
  IS 2014-2020 / OOS 2021-2026 (ENERY/AHGAZ: IS <=2024, OOS 2025+; SP500 2016-11+).
  Islem kurali (tek, onceden belirlenmis): z = L_t / sd250(L) (bir gun gecikmeli); |z|>1 -> yon = sign(b_IS)*sign(z),
  hedef - beta250*XU100 (hedge'li), 1 gun; maliyet spot 25 + hedge 3 bps, VIOP 12,5 + 3 bps (gidis-donus).
AILE S (senkron, kismi korelasyon XU100 kontrollu): yurt ici lider ayni gun; ABD tarihli lider 'gap gunu' t.
FDR: Benjamini-Hochberg, her aile icinde ayri.
Cikti: <cikti>/aile_P.csv, aile_S.csv, tani.txt, korelasyon_enerji.csv
"""
import argparse, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

SPOT = {"ENERY", "AHGAZ", "RYSAS"}
VIOP = {"ENJSA", "TUPRS", "KCHOL", "SAHOL", "AKBNK", "BRSAN", "TRMET", "TRALT"}

# (hedef, lider, tur, ufuk)  tur: d = yurt ici (BIST kapanisi), u = ABD/EIA tarihli, x = USDTRY (taniya gore)
TESTLER = [
    *[("ENERY", L, t, 1) for L, t in [("AHGAZ", "d"), ("ENJSA", "d"), ("AKSEN", "d"), ("AYGAZ", "d"), ("XELKT", "d"),
                                      ("XUTUMx", "d"), ("USDTRY", "x"), ("HH", "u"), ("BRENT", "u")]],
    *[("AHGAZ", L, t, 1) for L, t in [("ENERY", "d"), ("ENJSA", "d"), ("AKSEN", "d"), ("AYGAZ", "d"), ("XELKT", "d"),
                                      ("XUTUMx", "d"), ("USDTRY", "x"), ("HH", "u"), ("BRENT", "u")]],
    *[("RYSAS", L, t, 1) for L, t in [("RYGYO", "d"), ("XGMYO", "d"), ("XULAS", "d"), ("XUTUMx", "d"), ("USDTRY", "x"),
                                      ("BRENT", "u")]],
    ("ENJSA", "ENERY", "d", 1), ("ENJSA", "AHGAZ", "d", 1),
    ("TUPRS", "FF_OILx", "u", 1), ("TUPRS", "FF_OILx", "u", 2), ("TUPRS", "BRENT", "u", 1), ("TUPRS", "BRENT", "u", 2),
    ("KCHOL", "SP500", "u", 1), ("SAHOL", "SP500", "u", 1), ("SAHOL", "AKBNK", "d", 1), ("AKBNK", "VIX", "u", 1),
    ("BRSAN", "FF_STEELx", "u", 1), ("BRSAN", "BRYAT", "d", 1),
    ("TRMET", "KOZAGRP", "d", 1), ("TRALT", "FF_GOLDx", "u", 1),
]

IS_BAS, IS_SON, OOS_BAS = pd.Timestamp("2014-01-01"), pd.Timestamp("2020-12-31"), pd.Timestamp("2021-01-01")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cikti", required=True)
    a = ap.parse_args(); os.makedirs(a.cikti, exist_ok=True)
    cal = o.takvim()
    R = {}
    for k in ["ENERY", "AHGAZ", "RYSAS", "RYGYO", "ENJSA", "AKSEN", "AYGAZ", "TUPRS", "KCHOL", "SAHOL", "AKBNK", "BRSAN",
              "BRYAT", "TRMET", "TRALT", "TRENJ", "XU100", "XU030", "XUTUM", "XELKT", "XGMYO", "XULAS", "USDTRY"]:
        R[k] = o.bist_getiri(k, cal)
    R = pd.DataFrame(R)
    R["XUTUMx"] = R["XUTUM"] - R["XU100"]
    R["KOZAGRP"] = R[["TRALT", "TRENJ"]].mean(axis=1, skipna=False)
    tani = []

    # --- USDTRY damga tanisi: AKBNK ve XU100 ile ayni gun / ertesi gun iliskisi
    u = R["USDTRY"]
    pc0, n0 = o.partial_corr(R["AKBNK"], u, R[["XU100"]])
    pc1, n1 = o.partial_corr(R["AKBNK"].shift(-1), u, R[["XU100"]].shift(-1))
    c0 = R["XU100"].corr(u); c1 = R["XU100"].shift(-1).corr(u)
    b, t, n = o.ols_nw(R["XU100"].shift(-1).values, np.column_stack([u.values, R["XU100"].values]))
    tani.append(f"USDTRY (Is Yatirim) damga tanisi: corr(XU100_t, dUSD_t) {c0:+.3f}; corr(XU100_t+1, dUSD_t) {c1:+.3f}; "
                f"AKBNK kismi ayni gun {pc0:+.3f} / ertesi gun {pc1:+.3f}; XU100_t+1 ~ dUSD_t NW t {t[1]:+.2f}")
    gec = (abs(c1) > abs(c0) / 2) and abs(t[1]) > 3
    tani.append("Karar: " + ("GEC damgali -> ABD tarihli gibi bir gun kaydirildi" if gec else
                             "BIST kapanisiyla uyumlu kabul edildi (yurt ici lider gibi)"))

    # --- ABD/EIA tarihli liderler
    def logr(s):
        return np.log(s).diff()
    US = {}
    US["SP500"] = logr(o.fred("SP500"))
    US["VIX"] = logr(o.cboe_vix())
    US["BRENT"] = logr(o.fred("DCOILBRENTEU"))
    hh = logr(o.fred("DHHNGSP")); US["HH"] = hh
    f49 = o.french49(); ff = o.french_ff(); mkt = ff["MktRF"] + ff["RF"]
    for ad, kol in [("FF_OILx", "Oil"), ("FF_STEELx", "Steel"), ("FF_GOLDx", "Gold")]:
        y = f49[kol]; bt = o.rolling_beta(y, mkt)
        US[ad] = (y - bt * mkt)
    LU = {k: o.us_to_bist(v, cal) for k, v in US.items()}
    if gec:
        LU["USDTRY"] = R["USDTRY"].shift(1)  # t gunu damgali kur -> t+1 kapanisinda bilinir sayilir
    LU = pd.DataFrame(LU)
    tani.append("ABD tarihli seri son degerleri (BIST gunune eslenmis): " +
                ", ".join(f"{k} {LU[k].dropna().index[-1].date()}" for k in LU.columns))

    def lider(L, tur):
        if tur == "u" or (tur == "x" and gec):
            return LU[L]
        return R[L]

    beta_x = {k: o.rolling_beta(R[k], R["XU100"]) for k in set(x[0] for x in TESTLER)}

    rows = []
    for T, L, tur, h in TESTLER:
        y1 = R[T].shift(-1)
        yh = sum(R[T].shift(-j) for j in range(1, h + 1))
        x = lider(L, tur)
        # aykiri: lider z'si +-5'te kirpilir (HH spot sicramalari vb.)
        sd = x.rolling(250, min_periods=100).std().shift(1)
        z = (x / sd).clip(-5, 5)
        xw = z * sd
        X = np.column_stack([xw.values, R[T].values, R["XU100"].values])
        d0 = R[T].dropna().index[0]
        kisa = T in ("ENERY", "AHGAZ")
        if kisa:
            isb, iss, oosb = d0, pd.Timestamp("2024-12-31"), pd.Timestamp("2025-01-01")
        else:
            isb, iss, oosb = IS_BAS, IS_SON, OOS_BAS
        if L == "SP500":
            isb = max(isb, pd.Timestamp("2016-11-08"))
        idx = cal
        def sub(m):
            mm = m.values if hasattr(m, "values") else m
            yy = yh.values.copy(); yy[~mm] = np.nan
            return o.ols_nw(yy, X, lag=max(5, h + 3))
        mT = pd.Series(idx >= isb, index=idx)
        bF, tF, nF = sub(mT.values)
        bI, tI, nI = sub(((idx >= isb) & (idx <= iss)))
        bO, tO, nO = sub((idx >= oosb))
        b24, t24, n24 = sub((idx >= pd.Timestamp("2024-01-01")))
        sdL = np.nanstd(xw[idx >= isb])
        # islem kurali
        yon_is = np.sign(bI[1]) if np.isfinite(bI[1]) else np.sign(bF[1])
        hedge = sum(R[T].shift(-j) - beta_x[T] * R["XU100"].shift(-j) for j in range(1, h + 1))
        pos = pd.Series(np.where(z.abs() > 1, yon_is * np.sign(z), 0.0), index=idx)
        pnl = (pos * hedge).where(pos != 0)
        maliyet = (25.0 if T in SPOT else 12.5) + 3.0
        if h > 1:  # ortusmeyen: yalniz pozisyon yokken yeni giris (basit: her h gunde bir)
            keep = []; son = -10**9
            for i, v in enumerate(pnl.values):
                if np.isfinite(v) and i - son >= h:
                    keep.append(i); son = i
            pnl = pnl.iloc[keep]
        pnl_bps = pnl * 1e4 - maliyet

        def ozet(m):
            s = pnl_bps[m(pnl_bps.index)].dropna()
            if len(s) < 10:
                return np.nan, np.nan, len(s), np.nan
            return s.mean(), s.mean() / (s.std(ddof=1) / np.sqrt(len(s))), len(s), (s + maliyet).mean()
        nf, ntf, nnf, gf = ozet(lambda ix: ix >= isb)
        ni, nti, nni, gi = ozet(lambda ix: (ix >= isb) & (ix <= iss))
        no, nto, nno, go = ozet(lambda ix: ix >= oosb)
        n24_, nt24, nn24, g24 = ozet(lambda ix: ix >= pd.Timestamp("2024-01-01"))
        rows.append(dict(hedef=T, lider=L, tur=("ABD/EIA" if (tur == "u" or (tur == "x" and gec)) else "yurt ici"), ufuk=h,
                         n=nF, etki_bps_1sd=bF[1] * sdL * 1e4, t=tF[1], p=o.p_from_t(tF[1]),
                         etki_IS=bI[1] * sdL * 1e4, t_IS=tI[1], etki_OOS=bO[1] * sdL * 1e4, t_OOS=tO[1],
                         etki_2024=b24[1] * sdL * 1e4, t_2024=t24[1],
                         own_b=bF[2], own_t=tF[2], yon=yon_is, maliyet=maliyet,
                         islem_n=nnf, brut=gf, net=nf, net_t=ntf, net_IS=ni, net_IS_t=nti, net_OOS=no, net_OOS_t=nto,
                         net_2024=n24_, net_2024_t=nt24, islem_OOS_n=nno,
                         donem=f"{max(isb, d0).date()}..", is_son=str(iss.date()), son_z=float(z.dropna().iloc[-1]) if z.notna().any() else np.nan,
                         son_z_tarih=str(z.dropna().index[-1].date()) if z.notna().any() else ""))
    P = pd.DataFrame(rows)
    P["q_BH"] = o.bh(P["p"].values)
    P.to_csv(os.path.join(a.cikti, "aile_P.csv"), index=False, float_format="%.4f")

    # --- AILE S: senkron / gap gunu kismi korelasyonu (XU100 kontrollu)
    srows = []
    seen = set()
    for T, L, tur, h in TESTLER:
        if (T, L) in seen:
            continue
        seen.add((T, L))
        x = lider(L, tur)
        d0 = R[T].dropna().index[0]
        kisa = T in ("ENERY", "AHGAZ")
        oosb = pd.Timestamp("2025-01-01") if kisa else OOS_BAS
        isb = d0 if kisa else IS_BAS
        if L == "SP500":
            isb = max(isb, pd.Timestamp("2016-11-08"))
        def pc(m0, m1):
            m = (R.index >= m0) & (R.index <= m1)
            return o.partial_corr(R[T][m], x[m], R[["XU100"]][m])
        f, nf = pc(isb, pd.Timestamp("2030-01-01"))
        i_, _ = pc(isb, oosb - pd.Timedelta(days=1))
        oo, _ = pc(oosb, pd.Timestamp("2030-01-01"))
        y1, _ = pc(pd.Timestamp("2025-11-01"), pd.Timestamp("2030-01-01"))
        tt = f * np.sqrt(max(nf - 3, 1)) / np.sqrt(max(1 - f * f, 1e-9)) if np.isfinite(f) else np.nan
        srows.append(dict(hedef=T, lider=L, olcu=("gap gunu (ABD bilgisi BIST t)" if (tur == "u" or (tur == "x" and gec)) else "ayni gun"),
                          n=nf, pc=f, pc_IS=i_, pc_OOS=oo, pc_son1y=y1, t=tt, p=o.p_from_t(tt)))
    S = pd.DataFrame(srows); S["q_BH"] = o.bh(S["p"].values)
    S.to_csv(os.path.join(a.cikti, "aile_S.csv"), index=False, float_format="%.4f")

    # --- enerji dagitim kumesi korelasyonlari (K4 'tek kume / tek isim' kurali icin)
    E = R[["ENERY", "AHGAZ", "ENJSA", "AKSEN", "AYGAZ", "XU100"]].dropna()
    res = {}
    for k in ["ENERY", "AHGAZ", "ENJSA", "AKSEN", "AYGAZ"]:
        bb = np.polyfit(E["XU100"], E[k], 1); res[k] = E[k] - np.polyval(bb, E["XU100"])
    res = pd.DataFrame(res)
    C = pd.concat([E.drop(columns="XU100").corr().add_prefix("ham_"), res.corr().add_prefix("artik_")], axis=1)
    C.to_csv(os.path.join(a.cikti, "korelasyon_enerji.csv"), float_format="%.3f")
    w = (E.drop(columns="XU100").rolling(5).sum().dropna())
    C5 = w.corr()
    tani.append(f"Enerji kumesi ortak orneklem {E.index[0].date()}..{E.index[-1].date()} n={len(E)}; 5 gunluk ham korelasyon:\n" + C5.round(2).to_string())
    open(os.path.join(a.cikti, "tani.txt"), "w").write("\n".join(tani) + "\n")
    print("\n".join(tani))
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    print(P[["hedef", "lider", "tur", "ufuk", "n", "etki_bps_1sd", "t", "t_IS", "t_OOS", "t_2024", "q_BH", "yon", "islem_n", "brut", "net", "net_t", "net_OOS", "net_OOS_t", "net_2024", "son_z", "son_z_tarih"]].round(2).to_string())
    print(S.round(3).to_string())
    print(C.round(2).to_string())


if __name__ == "__main__":
    main()
