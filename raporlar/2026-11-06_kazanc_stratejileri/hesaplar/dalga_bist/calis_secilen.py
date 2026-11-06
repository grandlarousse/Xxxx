"""Seçilen kurallar: yıllık tablo (TL, USD, rf, XU100, EW), VİOP ile XU030-hedge'li sürüm, tutma dönemi istatistikleri,
son tarih itibarıyla tutulan kümeler.  Hedge: getiri + maruz*(rf - d - r_XU100) - maruz*hedge_maliyeti;
d = XU100 temettü verimi ~%3/yıl (vadeli fiyatı rf-d taşır), hedge maliyeti ~%0.6/yıl (2 ayda bir devir, makas)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
SON = os.environ.get("SON", "2026-11-05")
P, R, sup = panel(SON)
C, NU = kume_getiri(R); rf, _ = rf_gunluk(C.index)
V = M.Veri(P, R, C, NU, rf, KUMELER); usd = P["USDTRY"].ffill()
rfs = pd.Series(V.rf, index=V.cal); xu = pd.Series(V.Rm, index=V.cal)
D_DIV, H_COST = 0.03 / 252, 0.006 / 252
KUR = {"A_rot12_K3_M": dict(skor="r252", K=3, freq="M", absf=False, mktf=False),
       "B_rot12_K3_M_abs_mkt": dict(skor="r252", K=3, freq="M", absf=True, mktf=True),
       "C_rot12-1_K3_M": dict(skor="r252s21", K=3, freq="M", absf=False, mktf=False),
       "D_rot6_K3_M": dict(skor="r126", K=3, freq="M", absf=False, mktf=False)}
res = {}; holds = {}
for ad, kw in KUR.items():
    r, inv, to, We = M.rotasyon(V, lider=False, buf=0, L=1, c=0.0025, **kw)
    res[ad] = (r, inv); holds[ad] = We
S = M.durum_makinesi(V, "rs126", "rstr10", 1)
r, inv, to, We = M.slot_portfoy(V, S, nslot=3, L=1, c=0.0025, lider=False); res["E_olay_rs126_rstr10_f1"] = (r, inv); holds["E_olay_rs126_rstr10_f1"] = We
ok = V.elig & (V.yas >= 130); Wb = np.where(ok, 1.0, 0.0); Wb = Wb / np.maximum(Wb.sum(1, keepdims=True), 1)
Wx = np.zeros_like(Wb); Wx[2:] = Wb[:-2]
res["EW_tum_kumeler"] = (pd.Series((Wx * np.nan_to_num(V.C)).sum(1), index=V.cal), pd.Series(1.0, index=V.cal))
def hedge(r, inv): return r + inv * (rfs - D_DIV - xu) - inv * H_COST
def yil(r): x = r.loc["2012":]; return x.groupby(x.index.year).apply(lambda z: (1 + z).prod() - 1)
def cagr(r): r = r.dropna(); return (1 + r).prod() ** (252 / len(r)) - 1
def mdd(r): n = (1 + r).cumprod(); return (n / n.cummax() - 1).min()
Y = pd.DataFrame({"rf": yil(rfs), "XU100": yil(xu), "USDTRY": usd.groupby(usd.index.year).last().pct_change().loc[2012:]})
for ad, (r, inv) in res.items():
    Y[ad] = yil(r); Y[ad + "_H"] = yil(hedge(r, inv))
Y.loc["CAGR_2012-26"] = [cagr(s.loc["2012":]) for s in [rfs, xu]] + [np.nan] + sum([[cagr(r.loc["2012":]), cagr(hedge(r, i).loc["2012":])] for r, i in res.values()], [])
Y.loc["CAGR_2024-26"] = [cagr(s.loc["2024":]) for s in [rfs, xu]] + [np.nan] + sum([[cagr(r.loc["2024":]), cagr(hedge(r, i).loc["2024":])] for r, i in res.values()], [])
Y.loc["MaxDD_2012-26"] = [np.nan, mdd(xu.loc["2012":]), np.nan] + sum([[mdd(r.loc["2012":]), mdd(hedge(r, i).loc["2012":])] for r, i in res.values()], [])
print(Y.round(3).to_string())
Y.to_csv(os.path.join(OUT, "secilen_yillik.csv"), float_format="%.4f")
# USD CAGR
for ad, (r, inv) in res.items():
    for a in ("2012", "2024"):
        x = r.loc[a:]; u = usd.loc[x.index]; xh = hedge(r, inv).loc[a:]
        print(ad, a, "USD CAGR=%.3f  hedge USD CAGR=%.3f" % (((1 + x).prod() / (u.iloc[-1] / u.iloc[0])) ** (252 / len(x)) - 1,
                                                             ((1 + xh).prod() / (u.iloc[-1] / u.iloc[0])) ** (252 / len(x)) - 1))
# tutma dönemleri (küme bazında kesintisiz ağırlık>0)
for ad, We in holds.items():
    sp = []
    for k in range(We.shape[1]):
        w = We[:, k] > 0; d = np.diff(np.r_[0, w.astype(int), 0]); st = np.where(d == 1)[0]; en = np.where(d == -1)[0] - 1
        for a, b in zip(st, en):
            if V.cal[a] < pd.Timestamp("2012-01-02"): continue
            g = V.I[b, k] / V.I[a - 1, k] - 1; gm = V.Im[b] / V.Im[a - 1] - 1; grf = V.Irf[b] / V.Irf[a - 1] - 1
            sp.append(dict(kume=V.kumeler[k], bas=V.cal[a], gun=b - a + 1, tl=g, rel=(1 + g) / (1 + gm) - 1, rf=grf))
    sp = pd.DataFrame(sp)
    print(f"\n{ad}: tutma dönemi n={len(sp)} ({len(sp) / 14.85:.1f}/yıl), medyan gün={sp.gun.median():.0f}, "
          f"XU100'ü yenen={(sp.rel > 0).mean():.2f}, rf'yi yenen={(sp.tl > sp.rf).mean():.2f}, ort rel={sp.rel.mean():.3f}, medyan rel={sp.rel.median():.3f}, "
          f"en iyi 10% dönemin rel katkı payı={sp.rel.clip(lower=0).nlargest(max(1, len(sp) // 10)).sum() / sp.rel.clip(lower=0).sum():.2f}")
    print("  en sık tutulan:", sp.groupby("kume").gun.sum().sort_values(ascending=False).head(8).to_dict())
    # 2024-26 tutma dönemleri
    s24 = sp[sp.bas >= "2024-01-01"].sort_values("bas")
    print("  2024+ dönemleri:\n", s24.assign(bas=s24.bas.dt.date).round(3).to_string(index=False))
    sp.to_csv(os.path.join(OUT, f"tutma_{ad}.csv"), index=False, float_format="%.4f")
# son tarih itibarıyla hedef portföy (son kapanış sinyali; uygulanacak)
print("\n=== SON SİNYAL", V.cal[-1].date(), "===")
for ad, kw in KUR.items():
    r, inv, to, We = M.rotasyon(V, lider=False, buf=0, L=-1 if False else 1, c=0.0025, **kw)
    # We kaydırılmış: son sinyalin hedefi = kaydırma öncesi -> yeniden hesapla: son ay sonu seçimi
    rb = sorted(M.rebal_gunleri(V.cal, kw["freq"])); last_rb = [t for t in rb if t <= len(V.cal) - 1][-1]
    print(ad, "son yeniden dengeleme günü:", V.cal[last_rb].date(), "-> şu an tutulan (uygulanmış):",
          [V.kumeler[k] for k in range(We.shape[1]) if We[-1, k] > 0], " XU100>200GHO:", bool(V.mkt200[-1]))
print("E_olay durum (açık sinyaller):", [V.kumeler[k] for k in range(S.shape[1]) if S[-1, k] == 1],
      "slotta:", [V.kumeler[k] for k in range(We.shape[1]) if holds['E_olay_rs126_rstr10_f1'][-1, k] > 0])
