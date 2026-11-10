"""Görev 3b ek null (D): olay günlerinin oynaklığını koruyan 'wild bootstrap'.
Dairesel kaydırma olayları sakin günlere taşıyıp t dağılımını genişletebilir (olay günleri yüksek oynaklıklı).
D: her işlemin net getirisi, hedefin koşulsuz net ortalaması mu etrafında, GİRİŞ TAKVİM GÜNÜNE ortak Rademacher
işaretiyle çevrilir: null = mu + s_gün * (net - mu). Aynı gün giren tüm hedef/kombinasyonlar aynı işareti alır
(hedefler arası ve kombinasyonlar arası bağımlılık korunur), olay günü oynaklığı korunur, koşullu ortalama = koşulsuz.
Çıktı: kompakt (kombinasyon x P medyan t) -> d7_wild.npz"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
P = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
KINDS = ["L_UP", "L_DN", "GERIDE", "ONDE"]
t0 = time.time()
spy = px("SPY").index
X = leaders(spy); LEAD = list(X.columns)
combos = [(L, k, h) for L in LEAD for k in KINDS for h in (1, 2, 3)]
cix = {c: i for i, c in enumerate(combos)}
TG = targets()
rng = np.random.default_rng(11)
S = (rng.integers(0, 2, size=(len(spy), P), dtype=np.int8) * 2 - 1).astype(np.float32)
obs = np.full((len(combos), len(TG)), np.nan, np.float32)
nul = np.full((len(combos), len(TG), P), np.nan, np.float32)
def tvec(G):
    n = G.shape[0]; m = G.mean(0); s = G.std(0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        return m / (s / np.sqrt(n))
for ti, T in enumerate(TG):
    sg, c, df = signals_for(T, X, kinds=tuple(KINDS))
    n = len(c); cost = my_cost(df) / 1e4
    calpos = spy.get_indexer(df.index)
    mu = {h: float(np.mean((c[h:] / c[:-h] - 1)[80:]) - cost) for h in (1, 2, 3)}
    for (L, k), sig in sg.items():
        if sig.sum() < 30: continue
        for h in (1, 2, 3):
            ent, g = sim_greedy(sig, c, h)
            if len(ent) < 30: continue
            ci = cix[(L, k, h)]; net = (g - cost).astype(np.float32)
            obs[ci, ti] = tstat(net)
            sp = S[calpos[ent]]                          # (n_e, P)
            nul[ci, ti] = tvec(mu[h] + sp * (net - mu[h])[:, None])
    if ti % 40 == 0: print(ti, T, round(time.time() - t0, 1), flush=True)
ntg = np.sum(~np.isnan(obs), 1)
med_obs = np.nanmedian(obs, 1); medN = np.nanmedian(nul, 1)
mx = np.nanmax(medN, 0); omax = np.nanmax(med_obs)
ci_tlt = cix[("TLT", "L_UP", 3)]
cnt_obs = int(np.nansum(obs > 2.5)); cnt_N = np.nansum(nul > 2.5, (0, 1))
tmax_N = np.nanmax(nul, (0, 1))
print("D (wild, P=%d): gözlenen max medyan t %.3f; null max q50 %.3f q90 %.3f q95 %.3f q99 %.3f; p_seçim=%.3f" % (
    P, omax, *np.quantile(mx, [.5, .9, .95, .99]), (np.sum(mx >= omax) + 1) / (P + 1)))
print("  TLT L_UP h3 tek başına: null medyan t ort %.3f, p=%.4f" % (np.nanmean(medN[ci_tlt]), (np.sum(medN[ci_tlt] >= med_obs[ci_tlt]) + 1) / (P + 1)))
iq, ism = TG.index("QQQ"), TG.index("SMH")
print("  QQQ h3 tek p=%.3f, SMH h3 tek p=%.3f" % ((np.sum(nul[ci_tlt, iq] >= obs[ci_tlt, iq]) + 1) / (P + 1), (np.sum(nul[ci_tlt, ism] >= obs[ci_tlt, ism]) + 1) / (P + 1)))
print("  t>2.5 sayısı gözlenen %d, null medyan %.0f, p=%.3f; max t gözlenen %.2f, null q50 %.2f, p=%.3f" % (
    cnt_obs, np.median(cnt_N), (np.sum(cnt_N >= cnt_obs) + 1) / (P + 1), np.nanmax(obs), np.median(tmax_N), (np.sum(tmax_N >= np.nanmax(obs)) + 1) / (P + 1)))
print("  medyan t'lerin genel ortalaması: gözlenen %.3f, null %.3f" % (np.nanmean(med_obs), np.nanmean(medN)))
np.savez_compressed(os.path.join(HERE, "d7_wild.npz"), med_obs=med_obs, medN=medN, ntg=ntg, combos=np.array(["|".join(map(str, c)) for c in combos]))
print("bitti", round(time.time() - t0, 1))
