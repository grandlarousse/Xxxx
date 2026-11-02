"""B4: Tüm VİOP endeks vadelileri (XU030, XLBNK, X10XB, XSD25) + 47 pay vadelisi: en yakın vade (vade günü hariç) gün-içi
f_intra = ln(KAPANIS/ACILIS) (09:30->18:10 TSİ), f_gap = ln(ACILIS/ÖNCEKİ UZLAŞMA). Likidite filtresi: işlem sayısı >= MINTR.
Spot (Yahoo) ile aynı günlerde karşılaştırma. Çıktı res/b4_all.csv ve res/b4_panel.parquet"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
import warnings; warnings.filterwarnings("ignore")
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)
MINTR = 20
d = pd.read_parquet(R + "/viop_fut.parquet")
def front(und):
    x = d[d["SOZLESME KODU"].str.match(rf"^F_{und}\d{{4}}$")].copy()
    x = x[x["VADE TARIHI"] > x["TARIH"]].sort_values(["TARIH", "VADE TARIHI"])
    f = x.groupby("TARIH").head(1).set_index("TARIH")
    o = f["ACILIS FIYATI"]; c = f["KAPANIS FIYATI"]; u = f["UZLASMA FIYATI"]; up = f["ONCEKI UZLASMA FIYATI"]
    out = pd.DataFrame({"f_gap": np.log(o / up), "f_intra": np.log(c / o), "f_intra_vwap": np.log(f["AGIRLIKLI ORTALAMA FIYAT"] / o),
                        "f_cc": np.log(u / up), "ntr": f["ISLEM SAYISI"], "qty": f["ISLEM MIKTARI"], "tl": f["ISLEM HACMI"]})
    for k in ["f_gap", "f_intra", "f_intra_vwap", "f_cc"]:
        out.loc[(out[k].abs() > LIM) | ~np.isfinite(out[k]), k] = np.nan
    out.loc[out.ntr < 1, ["f_intra", "f_intra_vwap"]] = np.nan
    return out
rows = []; panel = {}
for und in ["XU030", "XLBNK", "X10XB", "XSD25"] + STOCKS:
    try:
        f = front(und)
    except Exception as e:
        print("yok", und, e); continue
    if len(f) == 0: print("yok", und); continue
    try:
        sp = decomp(und + ".IS", start="2017-01-01")
    except Exception:
        sp = pd.DataFrame(columns=["gap", "intra"])
    z = f.join(sp[["gap", "intra"]], how="left"); panel[und] = z
    for nm, sl in [("all", slice(None)), ("IS<=2020", slice(None, "2020")), ("OOS>=2021", slice("2021", None)), ("2023+", slice("2023", None))]:
        zz = z.loc[sl]; liq = zz[zz.ntr >= MINTR]
        both = liq.dropna(subset=["f_intra", "intra"])
        rows.append(dict(und=und, per=nm, n_days=len(zz), n_liq=liq.f_intra.notna().sum(), med_ntr=zz.ntr.median(), med_tl_mn=zz.tl.median() / 1e6,
                         f_intra=1e4 * liq.f_intra.mean(), t_f=tstat(liq.f_intra), f_gap=1e4 * liq.f_gap.mean(),
                         f_intra_both=1e4 * both.f_intra.mean(), s_intra_both=1e4 * both.intra.mean(), s_gap_both=1e4 * both.gap.mean(),
                         corr=both.f_intra.corr(both.intra), n_both=len(both)))
A = pd.DataFrame(rows); A.to_csv(R + "/b4_all.csv", index=False); pd.to_pickle(panel, R + "/b4_panel.pkl")
for per in ["all", "IS<=2020", "OOS>=2021", "2023+"]:
    a = A[A.per == per].set_index("und")
    print(f"\n== {per}: endeks vadelileri"); print(a.loc[["XU030", "XLBNK", "X10XB", "XSD25"]].drop(columns="per").round(2).to_string())
    s = a.loc[[u for u in STOCKS if u in a.index]]; s = s[s.n_liq >= 100]
    print(f"   pay vadelileri (n_liq>=100: {len(s)}): f_intra<0 {int((s.f_intra < 0).sum())}, t<-2 {int((s.t_f < -2).sum())}, medyan f_intra {s.f_intra.median():.1f}, "
          f"medyan spot aynı gün {s.s_intra_both.median():.1f}, medyan f_gap {s.f_gap.median():.1f}, medyan spot gap {s.s_gap_both.median():.1f}, medyan corr {s['corr'].median():.2f}, medyan işlem# {s.med_ntr.median():.0f}")
# EW pay vadelisi sepeti (likit günler)
FI = pd.DataFrame({u: p.f_intra.where(p.ntr >= MINTR) for u, p in panel.items() if u in STOCKS})
ew = -FI.mean(axis=1)
for nm, sl in [("all", slice(None)), ("IS<=2020", slice(None, "2020")), ("OOS>=2021", slice("2021", None))]:
    s = ew.loc[sl].dropna(); print("EW SSF aç-sat", nm, "n", len(s), "brüt", round(1e4 * s.mean(), 2), "t", round(tstat(s), 2))
