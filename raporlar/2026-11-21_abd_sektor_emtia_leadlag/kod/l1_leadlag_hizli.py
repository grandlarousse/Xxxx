"""L1 hızlı ön test (literatür notunu desteklemek için; resmi backtest değildir).

A) ETF çiftleri: büyük/likit öncü (t) -> küçük/az likit takipçi (t+1), takipçinin kendi t getirisi kontrol.
   t+1 getirisi gece (open/prevclose) ve gün içi (close/open) olarak da ayrılır.
B) Grup içi yayılım (Hou 2007 / Moskowitz-Grinblatt günlük sürümü): Fama-MacBeth
   r_{i,t+1} = a + b1 r_{i,t} + b2 grup_haric_i_{t} ; ayrıca 'geride kalan' L/S kantil yayılımı.
Dönemler: 2005-09, 2010-14, 2015-19, 2020-26. Çıktı: ek/backtest/l1_hizli_*.csv
"""
import os
import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(KOK, "veri")
OUT = os.path.join(KOK, "ek", "backtest")
os.makedirs(OUT, exist_ok=True)

ac = pd.read_parquet(os.path.join(V, "panel_adjclose.parquet"))
ao = pd.read_parquet(os.path.join(V, "panel_ao.parquet"))
vol = pd.read_parquet(os.path.join(V, "panel_volume.parquet"))
cl = pd.read_parquet(os.path.join(V, "panel_close.parquet"))
cal = ac["SPY"].dropna().index
ac, ao, vol, cl = [x.reindex(cal) for x in (ac, ao, vol, cl)]
r = ac.pct_change(fill_method=None)
night = ao / ac.shift(1) - 1
day = ac / ao - 1
r = r.where(r.abs() < 0.4)
DON = [("2005-09", "2005", "2009"), ("2010-14", "2010", "2014"), ("2015-19", "2015", "2019"), ("2020-26", "2020", "2026"), ("2024-26", "2024", "2026")]


def ols_t(y, X):
    X = np.column_stack([np.ones(len(y))] + X)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return b, b / se


# A) ETF çiftleri
CIFT = [("SPY", "IWM"), ("QQQ", "IWM"), ("SPY", "IJR"), ("XLE", "XOP"), ("XLF", "KRE"), ("SMH", "XSD"),
        ("IBB", "XBI"), ("XLY", "XRT"), ("ITB", "XHB"), ("XLK", "IGV"), ("GLD", "GDXJ"), ("GDX", "GDXJ"),
        ("XLI", "IYT"), ("SPY", "XBI")]
satir = []
for L, F in CIFT:
    for ad, a, b in DON:
        d = pd.DataFrame({"L": r[L], "F": r[F], "F1": r[F].shift(-1), "N1": night[F].shift(-1),
                          "D1": day[F].shift(-1), "L1": r[L].shift(-1)}).loc[a:b].dropna()
        if len(d) < 200:
            continue
        out = {"oncu": L, "hedef": F, "donem": ad, "n": len(d),
               "corr_L_Fnext": d.L.corr(d.F1), "corr_F_Lnext": d.F.corr(d.L1)}
        for k in ("F1", "N1", "D1"):
            bb, tt = ols_t(d[k].values, [d.L.values, d.F.values])
            out[f"b_{k}"], out[f"t_{k}"] = bb[1], tt[1]
        # basit kural: öncü - beta*takipçi farkının işaretine göre takipçide 1 gün pozisyon (göreli bps)
        sig = np.sign(d.L - d.F)
        out["kural_bps_gun"] = 1e4 * (sig * (d.F1 - d.L1)).mean()
        satir.append(out)
A = pd.DataFrame(satir)
A.to_csv(os.path.join(OUT, "l1_hizli_etf_cift.csv"), index=False, float_format="%.4f")

# B) Grup içi yayılım: yalnız h_ (hisse) grupları
m = pd.read_csv(os.path.join(V, "meta.csv"))
m = m[(m.tur == "EQUITY") & m.gruplar.fillna("").str.contains("h_")]
m = m[~m.sembol.str.contains(r"\.")]  # yalnız ABD
m["grup"] = m.gruplar.str.split("|").apply(lambda g: [x for x in g if x.startswith("h_")][0])
gr = m.set_index("sembol")["grup"]
syms = [s for s in gr.index if s in r.columns]
R = r[syms]
dv = (cl[syms] * vol[syms]).rolling(60, min_periods=40).mean()
G = pd.DataFrame(index=R.index, columns=syms, dtype=float)
for g, ss in gr[syms].groupby(gr[syms]):
    ss = list(ss.index)
    sub = R[ss]
    n = sub.notna().sum(axis=1)
    tot = sub.sum(axis=1)
    G[ss] = ((-sub).add(tot, axis=0)).div((n - 1).where(n > 2), axis=0)
R1, N1, D1 = R.shift(-1), night[syms].shift(-1), day[syms].shift(-1)
R2 = (1 + R).rolling(2).apply(np.prod, raw=True).shift(-2) - 1
R3 = (1 + R).rolling(3).apply(np.prod, raw=True).shift(-3) - 1
# küçük (az dolar hacimli) yarı: grup içinde dolar hacmi medyanının altı
med = dv.T.groupby(gr[syms]).transform("median").T
kucuk = dv < med

fm = []
for t in R.index[61:-1]:
    y, x1, x2 = R1.loc[t], R.loc[t], G.loc[t]
    ok = y.notna() & x1.notna() & x2.notna()
    if ok.sum() < 100:
        continue
    row = {"date": t}
    for k, Y in (("cc", R1), ("gece", N1), ("gun", D1)):
        yy = Y.loc[t][ok]
        o2 = yy.notna()
        X = np.column_stack([np.ones(o2.sum()), x1[ok][o2], x2[ok][o2]])
        b, *_ = np.linalg.lstsq(X, yy[o2].values, rcond=None)
        row[f"b_grup_{k}"], row[f"b_kendi_{k}"] = b[2], b[1]
    # 'geride kalan' kuralı: gap = grup_haric - kendi; grup içi değil tüm kesitte quintile L/S, ertesi gün
    gap = (x2 - x1)[ok]
    q = gap.rank(pct=True)
    yy = R1.loc[t][ok]
    row["ls_gap_bps"] = 1e4 * (yy[q > 0.8].mean() - yy[q <= 0.2].mean())
    for hh, RR in ((2, R2), (3, R3)):
        y2 = RR.loc[t][ok]
        row[f"ls_gap_h{hh}_bps"] = 1e4 * (y2[q > 0.8].mean() - y2[q <= 0.2].mean())
    yn = N1.loc[t][ok]
    row["ls_gap_gece_bps"] = 1e4 * (yn[q > 0.8].mean() - yn[q <= 0.2].mean())
    row["devir_gap"] = np.nan
    # saf grup sinyali: kendi getirisi nötr; grup_haric quintile
    q2 = x2[ok].rank(pct=True)
    row["ls_grup_bps"] = 1e4 * (yy[q2 > 0.8].mean() - yy[q2 <= 0.2].mean())
    ks = kucuk.loc[t][ok].fillna(False)
    row["ls_grup_kucuk_bps"] = 1e4 * (yy[(q2 > 0.8) & ks].mean() - yy[(q2 <= 0.2) & ks].mean())
    row["ls_grup_buyuk_bps"] = 1e4 * (yy[(q2 > 0.8) & ~ks].mean() - yy[(q2 <= 0.2) & ~ks].mean())
    fm.append(row)
FM = pd.DataFrame(fm).set_index("date")
oz = []
for ad, a, b in DON:
    s = FM.loc[a:b]
    o = {"donem": ad, "gun": len(s)}
    for c in s.columns:
        mu, sd = s[c].mean(), s[c].std()
        o[c] = mu
        o["t_" + c] = mu / sd * np.sqrt(len(s))
    oz.append(o)
B = pd.DataFrame(oz)
B.to_csv(os.path.join(OUT, "l1_hizli_grup_ici.csv"), index=False, float_format="%.4f")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
print(A[["oncu", "hedef", "donem", "corr_L_Fnext", "corr_F_Lnext", "b_F1", "t_F1", "t_N1", "t_D1", "kural_bps_gun"]].round(3).to_string())
print(B.round(3).T.to_string())
print("hisse sayisi", len(syms))
