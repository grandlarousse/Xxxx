"""Bağımsız yeniden üretim (ortak.py / cift_motoru.py / f*.py kullanılmadan, sıfırdan).

Çalıştır: python3 kod/yeniden_uretim.py
Çıktı: ek/dogrulama/yeniden_uretim.csv, yeniden_uretim_yillik.csv, yeniden_uretim_uc_islemler.csv
"""
import ast
import os
import sys
import time

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAM = os.path.join(KOK, "veri", "ham")
CIKTI = os.path.join(KOK, "ek", "dogrulama")
os.makedirs(CIKTI, exist_ok=True)
T0 = time.time()

BAS = pd.Timestamp("2005-01-01")
IS_SON = pd.Timestamp("2018-12-31")
OOS_BAS = pd.Timestamp("2019-01-01")
SON_BAS = pd.Timestamp("2024-01-01")


def dosya(sym):
    return os.path.join(HAM, sym.replace("^", "_idx_").replace("=", "_eq_") + ".csv")


_CACHE = {}


def oku(sym):
    if sym not in _CACHE:
        p = dosya(sym)
        if not os.path.exists(p):
            _CACHE[sym] = None
        else:
            d = pd.read_csv(p, usecols=["date", "open", "high", "low", "close", "adjclose", "volume", "split"])
            d["date"] = pd.to_datetime(d["date"].astype(str).str[:10])
            d = d.dropna(subset=["adjclose"]).drop_duplicates("date", keep="last").set_index("date").sort_index()
            _CACHE[sym] = d
    return _CACHE[sym]


SPY = oku("SPY")
B2005 = os.environ.get("TAM_GECMIS") != "1"  # ana yorum: göstergeler de 2005-01-01'den başlar; TAM_GECMIS=1 -> 2000+ geçmiş
SPY = SPY[SPY.index >= BAS] if B2005 else SPY
TAKVIM_TAM = SPY.index  # NYSE günleri, göstergeler için
TAKVIM = TAKVIM_TAM[TAKVIM_TAM >= BAS]


def hizala(sym):
    d = oku(sym)
    if d is None:
        return None
    return d.reindex(TAKVIM_TAM)


EK = "" if B2005 else "_tamgecmis"


def grup(ad):
    """evren.py'den yalnız grup listesini (ast ile) al; modülü içe aktarmadan."""
    src = open(os.path.join(KOK, "kod", "evren.py"), encoding="utf-8").read()
    agac = ast.parse(src)
    for dugum in ast.walk(agac):
        if isinstance(dugum, ast.Dict):
            for k, v in zip(dugum.keys, dugum.values):
                if isinstance(k, ast.Constant) and k.value == ad:
                    return ast.literal_eval(v).split()
    raise KeyError(ad)


def maliyet(d):
    dv = (d["close"] * d["volume"]).rolling(60, min_periods=20).median().shift(1)
    c = pd.Series(20.0, index=d.index)
    c[dv >= 20e6] = 10.0
    c[dv >= 100e6] = 5.0
    return c / 1e4


def ileri(p, h):
    return p.shift(-h) / p - 1


def hac_t(x, lag):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    T = len(x)
    if T < 10:
        return np.nan
    m = x.mean()
    e = x - m
    v = e @ e / T
    for k in range(1, lag + 1):
        v += 2 * (e[k:] @ e[:-k]) / T
    if v <= 0:  # düz ağırlık negatif verirse Bartlett'e düş
        v = e @ e / T + sum(2 * (1 - k / (lag + 1)) * (e[k:] @ e[:-k]) / T for k in range(1, lag + 1))
    return m / np.sqrt(v / T)


DONEM = {
    "tum": lambda ix: ix >= BAS,
    "IS": lambda ix: (ix >= BAS) & (ix <= IS_SON),
    "OOS": lambda ix: ix >= OOS_BAS,
    "SON": lambda ix: ix >= SON_BAS,
}


def degerlendir(sig, R, c, h, drift="tam"):
    """sig, R, c: DataFrame (gün x hedef). sig ∈ {+1,-1,0}. Portföy = gün içi eşit ağırlık.
    drift: 'tam' -> hedefin 2005+ tüm koşulsuz h-gün ortalaması; 'donem' -> IS/OOS ayrı ortalama."""
    sig = sig.reindex(TAKVIM).fillna(0)
    R = R.reindex(TAKVIM)
    c = c.reindex(TAKVIM).fillna(0.002)
    if drift == "tam":
        mu = pd.DataFrame(np.repeat(R.mean().values[None, :], len(R), 0), index=R.index, columns=R.columns)
    else:
        mIS = R[R.index <= IS_SON].mean()
        mO = R[R.index >= OOS_BAS].mean()
        mu = pd.DataFrame(index=R.index, columns=R.columns, dtype=float)
        mu.loc[R.index <= IS_SON] = mIS.values
        mu.loc[R.index >= OOS_BAS] = mO.values
    aktif = (sig != 0) & R.notna()
    brut = (sig * R).where(aktif)
    net = (sig * R - c).where(aktif)
    dadj = (sig * (R - mu) - c).where(aktif)
    gun = aktif.any(axis=1)
    pb = brut.mean(axis=1)
    pn = net.mean(axis=1)
    pd_ = dadj.mean(axis=1)
    veri_var = R.notna().any(axis=1)
    seri = pd_.where(gun, 0.0).where(veri_var)
    seri_net = pn.where(gun, 0.0).where(veri_var)
    out = {"n": int(gun.sum()), "n_islem": int(aktif.values.sum())}
    for ad, f in DONEM.items():
        m = f(TAKVIM) & gun.values
        out[f"n_{ad}"] = int(m.sum())
        out[f"brut_{ad}"] = pb[m].mean() * 1e4
        out[f"net_{ad}"] = pn[m].mean() * 1e4
        out[f"dadj_{ad}"] = pd_[m].mean() * 1e4
        out[f"t_{ad}"] = hac_t(seri[f(TAKVIM)], h - 1)
        out[f"tnet_{ad}"] = hac_t(seri_net[f(TAKVIM)], h - 1)
    yil = pd.DataFrame({"net": pn[gun], "dadj": pd_[gun]})
    yil = yil.groupby(yil.index.year).agg(n=("net", "size"), net=("net", "mean"), dadj=("dadj", "mean"))
    yil[["net", "dadj"]] *= 1e4
    islem = net.stack().dropna().rename("net").to_frame()
    islem.index.names = ["tarih", "hedef"]
    return out, yil, islem


def veri_kontrol(sym, t, h):
    d = oku(sym)
    if d is None:
        return ""
    ix = d.index.searchsorted(t)
    w = d.iloc[max(ix - 1, 0): ix + h + 1]
    bayrak = []
    if w["split"].notna().any() and (w["split"].astype(str).str.strip() != "").any():
        bayrak.append("bolunme")
    r = w["adjclose"].pct_change().abs()
    rc = w["close"].pct_change().abs()
    if (rc - r).abs().max() > 0.05:
        bayrak.append("adj/close_uyumsuz")
    if (w["high"] < w["low"]).any() or ((w["close"] > w["high"] * 1.001) | (w["close"] < w["low"] * 0.999)).any():
        bayrak.append("OHLC_bozuk")
    if (w["volume"] <= 0).any():
        bayrak.append("hacim0")
    if r.max() > 0.25:
        bayrak.append(f"gunluk_{r.max():.0%}")
    return ";".join(bayrak)


SONUC, YILLIK, UC = [], [], []


def kaydet(ad, yorum, sig, R, c, h, rap, drift_ikisi=True, uc_detay=True):
    for dr in (["tam", "donem"] if drift_ikisi else ["tam"]):
        out, yil, islem = degerlendir(sig, R, c, h, dr)
        satir = {"sinyal": ad, "yorum": yorum, "drift": dr, "h": h}
        satir.update(out)
        satir.update({f"rap_{k}": v for k, v in rap.items()})
        SONUC.append(satir)
        if dr == "tam":
            y = yil.reset_index().rename(columns={"index": "yil", "date": "yil"})
            y.insert(0, "sinyal", f"{ad}|{yorum}")
            YILLIK.append(y)
            if uc_detay:
                s = islem.reset_index().sort_values("net")
                for etiket, parca in (("kayip", s.head(10)), ("kazanc", s.tail(10).iloc[::-1])):
                    for _, r in parca.iterrows():
                        UC.append({"sinyal": f"{ad}|{yorum}", "tur": etiket, "tarih": r["tarih"].date(),
                                   "hedef": r["hedef"], "net_bps": r["net"] * 1e4,
                                   "veri_bayragi": veri_kontrol(r["hedef"], r["tarih"], h)})


def tek(df_or_s, ad):
    return df_or_s.to_frame(ad) if isinstance(df_or_s, pd.Series) else df_or_s


VIX = hizala("^VIX")["close"]
r_spy = SPY["adjclose"].pct_change()


# ---------------- S1 / S2 ----------------
def ibs_sinyal(sym, esik):
    d = hizala(sym)
    rng = d["high"] - d["low"]
    ibs = ((d["close"] - d["low"]) / rng).where(rng > 0)
    return ((ibs < 0.2) & (VIX > esik)).astype(float), d


S1_RAP = {("IBB", 25, 2): (238, 79.1, 2.70, 2.59), ("IJR", 20, 1): (479, 37.2, 3.26, 2.20),
          ("EEM", 20, 1): (438, 50.0, 3.38, 2.09), ("IBB", 20, 2): (446, 47.7, 2.58, 2.23),
          ("XBI", 20, 2): (456, 64.5, 2.15, 3.39)}
for (sym, es, h), (n, m, ti, to) in S1_RAP.items():
    s, d = ibs_sinyal(sym, es)
    kaydet(f"S1_{sym}_VIX{es}_h{h}", "ana", tek(s, sym), tek(ileri(d["adjclose"], h), sym), tek(maliyet(d), sym), h,
           {"n": n, "dadj": m, "tIS": ti, "tOOS": to})
# İZLE sınıfı: tüm eşik/h kombinasyonları (raporlananla sonra eşleştirilecek)
for sym in "QQQ XLK SMH SOXX IWM IWO KRE XRT".split():
    for es in (20, 25, 30):
        for h in (1, 2, 3):
            s, d = ibs_sinyal(sym, es)
            kaydet(f"S1izle_{sym}_VIX{es}_h{h}", "ana", tek(s, sym), tek(ileri(d["adjclose"], h), sym),
                   tek(maliyet(d), sym), h, {}, drift_ikisi=False, uc_detay=False)


def panel(syms):
    A, C = {}, {}
    for s in syms:
        d = hizala(s)
        if d is not None and d["adjclose"].notna().sum() > 300:
            A[s] = d
    return A


YI = panel(grup("h_yariiletken"))
for es, h, rap in ((25, 1, (742, 61.6, 2.70, 2.83)), (20, 1, (1525, 34.4, 2.73, 2.65)), (20, 2, (1524, 49.5, 2.54, 2.42))):
    sig = pd.DataFrame({s: ibs_sinyal(s, es)[0] for s in YI})
    R = pd.DataFrame({s: ileri(d["adjclose"], h) for s, d in YI.items()})
    c = pd.DataFrame({s: maliyet(d) for s, d in YI.items()})
    kaydet(f"S2_yariiletken_VIX{es}_h{h}", "ana", sig, R, c, h,
           {"n": rap[0], "dadj": rap[1], "tIS": rap[2], "tOOS": rap[3]})


# ---------------- S3 / S4 ----------------
def zpanel(P):
    r = pd.DataFrame({s: d["adjclose"].pct_change() for s, d in P.items()})
    sd = r.rolling(60, min_periods=40).std().shift(1)
    return r, sd


SB = panel(grup("h_sigorta_borsa"))
r, sd = zpanel(SB)
z5 = r.rolling(5, min_periods=5).sum() / (sd * np.sqrt(5))
sig = -((z5 >= 1.5) & (VIX.values[:, None] > 20)).astype(float)
R = pd.DataFrame({s: ileri(d["adjclose"], 2) for s, d in SB.items()})
c = pd.DataFrame({s: maliyet(d) for s, d in SB.items()})
kaydet("S3_sigorta_SAT_h2", "ana", sig, R, c, 2, {"n": 485, "dadj": 80.3, "tIS": 2.58, "tOOS": 2.52})
# yorum B: sd gecikmesiz
sd0 = r.rolling(60, min_periods=40).std()
sigB = -(((r.rolling(5).sum() / (sd0 * np.sqrt(5))) >= 1.5) & (VIX.values[:, None] > 20)).astype(float)
kaydet("S3_sigorta_SAT_h2", "sd_gecikmesiz", sigB, R, c, 2, {"n": 485, "dadj": 80.3, "tIS": 2.58, "tOOS": 2.52},
       drift_ikisi=False, uc_detay=False)

TT = panel(grup("h_temel_tuketim"))
r, sd = zpanel(TT)
px = pd.DataFrame({s: d["adjclose"] for s, d in TT.items()})
ma = px.rolling(200, min_periods=200).mean()
sig = ((r / sd <= -1.5) & (px < ma)).astype(float)
R = pd.DataFrame({s: ileri(d["adjclose"], 1) for s, d in TT.items()})
c = pd.DataFrame({s: maliyet(d) for s, d in TT.items()})
kaydet("S4_temel_tuketim_AL_h1", "ana", sig, R, c, 1, {"n": 1354, "dadj": 41.6, "tIS": 3.00, "tOOS": 2.06})


# ---------------- S5–S8 (öncü -> hedef) ----------------
def nyse_topla(s):
    """Kendi takvimindeki seriyi NYSE gününe hizala: aynı gün ya da sonraki ilk NYSE günü; toplanır."""
    s = s.dropna()
    s = s[s.index >= TAKVIM_TAM[0]]
    pos = TAKVIM_TAM.searchsorted(s.index, side="left")
    ok = pos < len(TAKVIM_TAM)
    hedef_gun = TAKVIM_TAM[pos[ok]]
    return pd.Series(s.values[ok], index=hedef_gun).groupby(level=0).sum().reindex(TAKVIM_TAM)


def kayan_beta(y, x, w=250, mp=120):
    df = pd.concat([y, x], axis=1).dropna()
    cov = df.iloc[:, 0].rolling(w, min_periods=mp).cov(df.iloc[:, 1])
    var = df.iloc[:, 1].rolling(w, min_periods=mp).var()
    return (cov / var).reindex(TAKVIM_TAM).shift(1)


def z_arindir(x, arindir=True):
    if arindir:
        b = kayan_beta(x, r_spy)
        xr = x - b * r_spy
    else:
        xr = x
    return xr / xr.rolling(60, min_periods=40).std().shift(1)


def hedge_R(sym, h, hedge=True):
    d = hizala(sym)
    Rt = ileri(d["adjclose"], h)
    if hedge:
        rt = d["adjclose"].pct_change()
        b = kayan_beta(rt, r_spy)
        Rt = Rt - b * ileri(SPY["adjclose"], h)
    return Rt, maliyet(d)


def fut(sym):
    c = oku(sym)["close"]
    return c[c.index >= TAKVIM_TAM[0]] if B2005 else c


cr = pd.concat([fut("RB=F"), fut("HO=F"), fut("CL=F")], axis=1, keys=["RB", "HO", "CL"]).dropna()
crack = (2 * cr["RB"] * 42 + cr["HO"] * 42 - 3 * cr["CL"]) / 3
d_crack = nyse_topla(crack.diff())


def ikiyon(z, k=1.0):
    return (z >= k).astype(float) - (z <= -k).astype(float)


def oncu(ad, yorum, x, hedef, h, rap, arindir=True, hedge=True, ikisi=True, uc=True):
    z = z_arindir(x, arindir)
    Rt, c = hedge_R(hedef, h, hedge)
    kaydet(ad, yorum, tek(ikiyon(z), hedef), tek(Rt, hedef), tek(c, hedef), h, rap, drift_ikisi=ikisi, uc_detay=uc)


oncu("S5_crack_VLO_h2", "ana", d_crack, "VLO", 2, {"n": 1365, "dadj": 28.4, "tIS": 2.51, "tOOS": 2.11})
# yorum B: NYSE'de vadeli işlem olmayan günü 0 say
oncu("S5_crack_VLO_h2", "bos_gun_0", d_crack.fillna(0), "VLO", 2, {"n": 1365, "dadj": 28.4, "tIS": 2.51, "tOOS": 2.11},
     ikisi=False, uc=False)

lmu = np.log(hizala("MU")["adjclose"]).diff()
oncu("S6_MU_WDC_h3", "ana", lmu, "WDC", 3, {"n": 1444, "dadj": 50.9, "tIS": 3.74, "tOOS": 2.43})

zl = fut("ZL=F")
lzl = nyse_topla(np.log(zl).diff())
oncu("S7_ZL_BG_h1", "ana", lzl, "BG", 1, {"dadj": 8.2, "dadj_OOS": 26.0, "tIS": -0.47, "tOOS": 3.63})
oncu("S7_ZL_ADM_h1", "ana", lzl, "ADM", 1, {"dadj_OOS": 24.8, "tOOS": 3.44})

oncu("S8_crack_PBF_h3", "ana", d_crack, "PBF", 3, {"n": 890, "dadj": 73.9, "dadj_OOS": 108.7, "tIS": 1.12, "tOOS": 2.82},
     arindir=False, hedge=False)
# yorum B: z için d'nin std'si yalnız min 40
# (ana tanımda zaten 60/40; ek yorum: yalnız AL bacağı)
z8 = z_arindir(d_crack, False)
R8, c8 = hedge_R("PBF", 3, False)
kaydet("S8_crack_PBF_h3", "yalniz_AL", tek((z8 >= 1).astype(float), "PBF"), tek(R8, "PBF"), tek(c8, "PBF"), 3,
       {"n": 890, "dadj": 73.9, "dadj_OOS": 108.7, "tIS": 1.12, "tOOS": 2.82}, drift_ikisi=False, uc_detay=False)


# ---------------- sağlamlık: likidite filtresi / tek olay dışlama ----------------
def likit(P, esik=5e6):
    """60 günlük medyan dolar hacmi (1 gün gecikmeli) >= esik. (Yahoo close bölünmeye göre düzeltilmiş
    olduğundan fiyat eşiği kullanılmaz; close x volume bölünmeden etkilenmez.)"""
    out = {}
    for s_, d in P.items():
        dv = (d["close"] * d["volume"]).rolling(60, min_periods=20).median().shift(1)
        out[s_] = dv >= esik
    return pd.DataFrame(out)


for es, h, rap in ((25, 1, (742, 61.6, 2.70, 2.83)), (20, 1, (1525, 34.4, 2.73, 2.65)), (20, 2, (1524, 49.5, 2.54, 2.42))):
    sig0 = pd.DataFrame({s_: ibs_sinyal(s_, es)[0] for s_ in YI})
    R = pd.DataFrame({s_: ileri(d["adjclose"], h) for s_, d in YI.items()})
    c = pd.DataFrame({s_: maliyet(d) for s_, d in YI.items()})
    for esik, et in ((5e6, "dv_5mn"), (20e6, "dv_20mn")):
        kaydet(f"S2_yariiletken_VIX{es}_h{h}", et, sig0.where(likit(YI, esik), 0), R, c, h, {}, uc_detay=False)

r, sd = zpanel(TT)
px = pd.DataFrame({s_: d["adjclose"] for s_, d in TT.items()})
sig = ((r / sd <= -1.5) & (px < px.rolling(200, min_periods=200).mean())).astype(float)
R = pd.DataFrame({s_: ileri(d["adjclose"], 1) for s_, d in TT.items()})
c = pd.DataFrame({s_: maliyet(d) for s_, d in TT.items()})
for esik, et in ((5e6, "dv_5mn"), (20e6, "dv_20mn")):
    kaydet("S4_temel_tuketim_AL_h1", et, sig.where(likit(TT, esik), 0), R, c, 1, {}, uc_detay=False)
kaydet("S4_temel_tuketim_AL_h1", "CELH_haric", sig.drop(columns="CELH"), R.drop(columns="CELH"), c.drop(columns="CELH"), 1, {},
       uc_detay=False)

r, sd = zpanel(SB)
z5 = r.rolling(5, min_periods=5).sum() / (sd * np.sqrt(5))
sig = -((z5 >= 1.5) & (VIX.values[:, None] > 20)).astype(float)
R = pd.DataFrame({s_: ileri(d["adjclose"], 2) for s_, d in SB.items()})
c = pd.DataFrame({s_: maliyet(d) for s_, d in SB.items()})
kaydet("S3_sigorta_SAT_h2", "AIG_haric", sig.drop(columns="AIG"), R.drop(columns="AIG"), c.drop(columns="AIG"), 2, {},
       uc_detay=False)

z7 = z_arindir(lzl)
R7, c7 = hedge_R("ADM", 1)
s7 = ikiyon(z7)
s7.loc[pd.Timestamp("2024-01-19")] = 0
kaydet("S7_ZL_ADM_h1", "2024-01-19_haric", tek(s7, "ADM"), tek(R7, "ADM"), tek(c7, "ADM"), 1, {}, uc_detay=False)

# ---------------- çıktı ----------------
df = pd.DataFrame(SONUC)


def fark(r):
    if pd.isna(r.get("rap_dadj")) and pd.isna(r.get("rap_tOOS")):
        return ""
    sorun = []
    if pd.notna(r.get("rap_n")) and abs(r["n"] / r["rap_n"] - 1) > 0.05:
        sorun.append("n")
    for mk, rk in (("dadj_tum", "rap_dadj"), ("dadj_OOS", "rap_dadj_OOS")):
        if rk in r and pd.notna(r[rk]):
            dlt = abs(r[mk] - r[rk])
            if dlt > 5 and dlt > 0.2 * abs(r[rk]):
                sorun.append(mk)
    for mk, rk in (("t_IS", "rap_tIS"), ("t_OOS", "rap_tOOS")):
        if rk in r and pd.notna(r[rk]) and abs(r[mk] - r[rk]) > 0.4:
            sorun.append(mk)
    return "UYUSUYOR" if not sorun else "UYUSMUYOR:" + ",".join(sorun)


df["durum"] = df.apply(fark, axis=1)
for a, b in (("n", "rap_n"), ("dadj_tum", "rap_dadj"), ("t_IS", "rap_tIS"), ("t_OOS", "rap_tOOS")):
    if b in df:
        df["fark_" + a] = df[a] - df[b]
df.round(3).to_csv(os.path.join(CIKTI, "yeniden_uretim" + EK + ".csv"), index=False)
pd.concat(YILLIK).round(2).to_csv(os.path.join(CIKTI, "yeniden_uretim_yillik" + EK + ".csv"), index=False)
pd.DataFrame(UC).round(1).to_csv(os.path.join(CIKTI, "yeniden_uretim_uc_islemler" + EK + ".csv"), index=False)
kol = ["sinyal", "yorum", "drift", "n", "n_islem", "brut_tum", "net_tum", "dadj_tum", "dadj_OOS", "net_SON",
       "t_tum", "t_IS", "t_OOS", "t_SON", "rap_n", "rap_dadj", "rap_tIS", "rap_tOOS", "durum"]
with pd.option_context("display.width", 250, "display.max_columns", 30, "display.max_rows", 200):
    print(df[~df.sinyal.str.startswith("S1izle")][kol].round(2).to_string(index=False))
print(f"süre {time.time() - T0:.0f} sn", file=sys.stderr)
