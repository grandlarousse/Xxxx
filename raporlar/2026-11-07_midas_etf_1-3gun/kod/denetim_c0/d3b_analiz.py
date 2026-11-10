"""Görev 3b analiz: d3_null.npz -> seçim düzeltmeli p değerleri."""
import os, sys, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
d = np.load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "d3_null.npz"))
obs = d["obs"]; combos = [c.split("|") for c in d["combos"]]; TG = list(d["targets"])
ntg = np.sum(~np.isnan(obs), 1)
med_obs = np.nanmedian(obs, 1); pos_obs = np.nansum(obs > 0, 1) / np.maximum(ntg, 1); pos_obs[ntg == 0] = np.nan
ci_tlt = [i for i, c in enumerate(combos) if c == ["TLT", "L_UP", "3"]][0]
order = np.argsort(-np.nan_to_num(med_obs, nan=-9))
print("Gözlenen sıralama (ilk 5):", [(" ".join(combos[i]), round(float(med_obs[i]), 3), int(ntg[i])) for i in order[:5]])
print("dolu kombinasyon:", int((ntg > 0).sum()), "/", len(combos), "; >=150 hedefli:", int((ntg >= 150).sum()))
omax = np.nanmax(med_obs)
out = []
for v in "ABC":
    N = d[v]                                  # (combo, target, P)
    P = N.shape[2]
    medN = np.nanmedian(N, 1)                 # (combo, P)
    mx = np.nanmax(medN, 0)
    sub = ntg >= 150
    mx150 = np.nanmax(medN[sub], 0)
    posN = np.nansum(N > 0, 1) / np.maximum(ntg, 1)[:, None]; posN[ntg == 0] = np.nan
    pmx = np.nanmax(posN[sub], 0)          # yalnız >=150 hedefli kombinasyonlar (az hedefte %100 kolay)
    cnt_obs = int(np.nansum(obs > 2.5)); cnt_N = np.nansum(N > 2.5, (0, 1))
    tmax_obs = float(np.nanmax(obs)); tmax_N = np.nanmax(N, (0, 1))
    i_q, i_s = TG.index("QQQ"), TG.index("SMH")
    rec = {"null": v, "P": P,
           "gözlenen_max_medyan_t": round(float(omax), 3),
           "null_max_medyan_t_q50": round(float(np.quantile(mx, .5)), 3), "q90": round(float(np.quantile(mx, .9)), 3),
           "q95": round(float(np.quantile(mx, .95)), 3), "q99": round(float(np.quantile(mx, .99)), 3),
           "p_secim_duzeltmeli": float((np.sum(mx >= omax) + 1) / (P + 1)),
           "p_secim_duz_>=150hedef": float((np.sum(mx150 >= omax) + 1) / (P + 1)),
           "p_tek_TLT_LUP_h3_medyan_t": float((np.sum(medN[ci_tlt] >= med_obs[ci_tlt]) + 1) / (P + 1)),
           "TLT_null_medyan_t_ort": round(float(np.nanmean(medN[ci_tlt])), 3),
           "pozitif_oran_gozlenen": round(float(pos_obs[ci_tlt]), 3),
           "p_tek_TLT_pozitif_oran": float((np.sum(posN[ci_tlt] >= pos_obs[ci_tlt]) + 1) / (P + 1)),
           "null_max_pozitif_oran_q95(>=150hedef)": round(float(np.quantile(pmx, .95)), 3),
           "p_secim_pozitif_oran": float((np.sum(pmx >= np.nanmax(pos_obs[ntg >= 150])) + 1) / (P + 1)),
           "p_tek_QQQ_h3_t": float((np.sum(N[ci_tlt, i_q] >= obs[ci_tlt, i_q]) + 1) / (P + 1)),
           "p_tek_SMH_h3_t": float((np.sum(N[ci_tlt, i_s] >= obs[ci_tlt, i_s]) + 1) / (P + 1)),
           "t>2.5_sayisi_gozlenen": cnt_obs, "t>2.5_null_medyan": float(np.median(cnt_N)), "p_t>2.5_sayisi": float((np.sum(cnt_N >= cnt_obs) + 1) / (P + 1)),
           "max_t_gozlenen": round(tmax_obs, 3), "max_t_null_q50": round(float(np.median(tmax_N)), 3), "p_max_t": float((np.sum(tmax_N >= tmax_obs) + 1) / (P + 1))}
    out.append(rec)
o = pd.DataFrame(out).set_index("null").T
print(o.to_string())
o.to_csv(os.path.join(HERE, "d3_sonuc.csv"))
print("\nmax pozitif oran gözlenen (>=150 hedef):", round(float(np.nanmax(pos_obs[ntg >= 150])), 3),
      " kombinasyon:", " ".join(combos[int(np.nanargmax(np.where(ntg >= 150, pos_obs, np.nan)))]))
