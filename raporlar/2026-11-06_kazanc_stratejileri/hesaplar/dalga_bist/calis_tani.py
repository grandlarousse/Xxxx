"""Tanı testleri: (1) kümeler arası momentum sıra-IC (aylık), (2) olay çalışması: taze RS kırılımı sonrası ileri getiri
EW-tüm-kümelere ve XU100'e göre, (3) yıl yıl. Sinyal t kapanışı, ileri getiri t+1 kapanışından (1 gün gecikme)."""
import os, sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
P, R, sup = panel("2026-11-05")
C, NU = kume_getiri(R); rf, _ = rf_gunluk(C.index)
V = M.Veri(P, R, C, NU, rf, KUMELER)
T, K = V.C.shape; cal = V.cal
ok = V.elig & (V.yas >= 130)
Wb = np.where(ok, 1.0, 0.0); Wb = Wb / np.maximum(Wb.sum(1, keepdims=True), 1)
ew = np.cumprod(1 + (np.r_[np.zeros((1, K)), Wb[:-1]] * np.nan_to_num(V.C)).sum(1))  # EW endeks (dünkü uygunluk)
lI = np.log(V.I); lew = np.log(ew); lm = np.log(V.Im)
def ileri(t, h):
    a, b = t + 1, min(t + 1 + h, T - 1)
    return lI[b] - lI[a], lew[b] - lew[a], lm[b] - lm[a], b - a
# (1) aylık IC
me = sorted(M.rebal_gunleri(cal, "M"))
rows = []
for t in me:
    if t < V.t0 or t + 23 >= T: continue
    m = ok[t]
    if m.sum() < 8: continue
    fI, fE, fM, n = ileri(t, 21)
    fwd = fI - fE
    d = dict(tarih=cal[t], n=int(m.sum()))
    for L in (21, 63, 126, 252):
        if L == 252:
            past = np.log(V.Rel[t] / pd.DataFrame(V.Rel).shift(252).values[t])
        else:
            past = np.log(V.Rel[t] / V.lag[L][t])
        mm = m & np.isfinite(past) & np.isfinite(fwd)
        d[f"ic{L}"] = spearmanr(past[mm], fwd[mm]).correlation if mm.sum() >= 8 else np.nan
        o = np.argsort(-np.where(mm, past, -np.inf)); top = o[:3]; bot = [i for i in np.argsort(np.where(mm, past, np.inf)) if mm[i]][:3]
        d[f"top3_{L}"] = np.mean(fwd[top]); d[f"bot3_{L}"] = np.mean(fwd[bot])
    rows.append(d)
IC = pd.DataFrame(rows).set_index("tarih")
def ozet(df):
    o = {}
    for L in (21, 63, 126, 252):
        x = df[f"ic{L}"].dropna(); o[f"IC{L}_ort"] = x.mean(); o[f"IC{L}_t"] = x.mean() / x.std() * np.sqrt(len(x))
        o[f"IC{L}_poz"] = (x > 0).mean()
        o[f"top3-EW_{L}_yil"] = df[f"top3_{L}"].mean() * 12; o[f"bot3-EW_{L}_yil"] = df[f"bot3_{L}"].mean() * 12
    return pd.Series(o)
per = {"2012-26": IC, "2012-18": IC.loc[:"2018"], "2019-23": IC.loc["2019":"2023"], "2024-26": IC.loc["2024":]}
S1 = pd.DataFrame({k: ozet(v) for k, v in per.items()})
print("=== (1) Kümeler arası momentum (aylık, ileri 21g, log, EW'ye göre) ===\n", S1.round(3).to_string())
S1.to_csv(os.path.join(OUT, "tani_ic.csv"), float_format="%.4f")
yIC = IC.groupby(IC.index.year)[["ic21", "ic63", "ic126", "ic252"]].mean()
print(yIC.round(2).T.to_string())
# (2) olay çalışması: taze kırılım (son 63 günde yeni yüksek yokken) - RS 63/126 yeni yüksek; genişlik itkisi; DM girişi
def olaylar(sig, bos=63):
    ev = []
    for k in range(K):
        last = -10 ** 9
        for t in range(V.t0, T - 2):
            if sig[t, k] and ok[t, k]:
                if t - last > bos: ev.append((t, k))
                last = t
    return ev
with np.errstate(invalid="ignore"):
    sigs = {"RS63_yeni_yuksek": V.Rel >= V.hi63 - 1e-12, "RS126_yeni_yuksek": V.Rel >= V.hi126 - 1e-12,
            "genislik>=70%": (V.br >= 0.7) & (V.Rel > V.ma50rel),
            "DM6_giris": (V.I / V.lagI[126] - 1 > V.rfL[126][:, None]) & (V.Rel / V.lag[126] > 1),
            "RS126_kirilim+XU100>200GHO": (V.Rel >= V.hi126 - 1e-12) & V.mkt200[:, None]}
rows = []; evrows = []
for ad, sg in sigs.items():
    ev = olaylar(sg)
    for h in (21, 63, 126):
        x = []
        for t, k in ev:
            if t + 1 + h >= T: continue
            fI, fE, fM, n = ileri(t, h); x.append((fI[k] - fE, fI[k] - fM, cal[t].year))
            if h == 63: evrows.append(dict(sinyal=ad, tarih=cal[t], kume=V.kumeler[k], f63_ew=fI[k] - fE, f63_xu=fI[k] - fM))
        x = np.array([(a, b) for a, b, _ in x]); yrs = np.array([y for _, _, y in [(0, 0, 0)] * 0] + [0])
        rows.append(dict(sinyal=ad, ufuk=h, n=len(x), ort_vs_EW=np.mean(x[:, 0]), med_vs_EW=np.median(x[:, 0]),
                         isabet_vs_EW=(x[:, 0] > 0).mean(), ort_vs_XU=np.mean(x[:, 1]), isabet_vs_XU=(x[:, 1] > 0).mean(),
                         t_vs_EW=np.mean(x[:, 0]) / np.std(x[:, 0]) * np.sqrt(len(x))))
# koşulsuz (tüm küme-günleri) kıyas
for h in (21, 63, 126):
    xs = []; xm = []
    for t in range(V.t0, T - 1 - h, 5):
        fI, fE, fM, n = ileri(t, h); m = ok[t]
        xs += list(fI[m] - fE); xm += list(fI[m] - fM)
    rows.append(dict(sinyal="KOSULSUZ(her 5 gün)", ufuk=h, n=len(xs), ort_vs_EW=np.mean(xs), med_vs_EW=np.median(xs),
                     isabet_vs_EW=np.mean(np.array(xs) > 0), ort_vs_XU=np.mean(xm), isabet_vs_XU=np.mean(np.array(xm) > 0), t_vs_EW=np.nan))
E = pd.DataFrame(rows)
print("\n=== (2) Olay çalışması (log ileri getiri; taze sinyal = önceki 63 günde sinyal yok) ===\n", E.round(3).to_string(index=False))
E.to_csv(os.path.join(OUT, "tani_olay.csv"), index=False, float_format="%.4f")
EV = pd.DataFrame(evrows)
EV["yil"] = EV.tarih.dt.year
yy = EV.groupby(["sinyal", "yil"]).f63_ew.mean().unstack(0)
print("\nYıl bazında 63g ileri getiri - EW (ortalama, log):\n", yy.round(3).to_string())
yy.to_csv(os.path.join(OUT, "tani_olay_yillik.csv"), float_format="%.4f")
