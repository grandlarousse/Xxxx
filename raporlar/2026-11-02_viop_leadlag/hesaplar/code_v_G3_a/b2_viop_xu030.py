"""B2: VİOP F_XU030 (en yakın vade, vade günü hariç -> bir sonraki) gece/gün-içi.
Tanımlar (aynı sözleşme içinde, roll yok):
  f_gap   = ln(ACILIS_T / UZLASMA_{T-1})   [ONCEKI UZLASMA aynı satırda]
  f_gapc  = ln(ACILIS_T / KAPANIS_{T-1})
  f_intra = ln(KAPANIS_T / ACILIS_T) ; f_intra_s = ln(UZLASMA_T / ACILIS_T) ; f_intra_os = ln(KAPANIS_T / ACILIS SEANSI_T)
Spot: Yahoo XU030 o/c. Önce ACILIS'in hangi saat olduğunu (sabah 09:30 mı, akşam seansı 19:00 T-1 mi) test eder."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)
UND = sys.argv[1] if len(sys.argv) > 1 else "XU030"
SPOT = {"XU030": "XU030.IS", "XLBNK": "XLBNK.IS"}.get(UND, UND + ".IS")
d = pd.read_parquet(R + "/viop_fut.parquet")
pre = f"F_{UND}"
x = d[d["SOZLESME KODU"].str.match(rf"^F_{UND}\d{{4}}$")].copy()
x = x[(x["VADE TARIHI"] > x["TARIH"])]
x = x.sort_values(["TARIH", "VADE TARIHI"])
front = x.groupby("TARIH").head(1).set_index("TARIH")
# en hacimli ile aynı mı?
mv = x.loc[x.groupby("TARIH")["ISLEM MIKTARI"].idxmax()].set_index("TARIH")
print(UND, "gün", len(front), "front==en hacimli oranı", round((front["SOZLESME KODU"] == mv["SOZLESME KODU"]).mean(), 3))
# önceki gün kapanışı aynı sözleşme
allk = x.set_index(["TARIH", "SOZLESME KODU"])
dates = sorted(x.TARIH.unique()); prevd = dict(zip(dates[1:], dates[:-1]))
pk = [(prevd.get(t), c) for t, c in zip(front.index, front["SOZLESME KODU"])]
front["KAP_prev"] = [allk["KAPANIS FIYATI"].get(k, np.nan) if k[0] is not None else np.nan for k in pk]
front["prev_date"] = [k[0] for k in pk]
F = pd.DataFrame(index=front.index)
O = front["ACILIS FIYATI"]; OS = front["ACILIS SEANSI FIYATI"]; C = front["KAPANIS FIYATI"]; U = front["UZLASMA FIYATI"]; UP = front["ONCEKI UZLASMA FIYATI"]
F["f_gap"] = np.log(O / UP); F["f_gapc"] = np.log(O / front.KAP_prev); F["f_intra"] = np.log(C / O); F["f_intra_s"] = np.log(U / O)
F["f_intra_os"] = np.log(C / OS); F["f_cc"] = np.log(U / UP); F["has_os"] = OS.notna(); F["vol"] = front["ISLEM MIKTARI"]; F["n_trades"] = front["ISLEM SAYISI"]
F["os_qty"] = front["ACILIS SEANSI ISLEM MIKTARI"]
# boşluklu günleri (önceki bülten günü != önceki BIST günü) atma: prev_date kontrolü yeterli; ayrıca |f_cc|>10.5% NaN
for c in ["f_gap", "f_gapc", "f_intra", "f_intra_s", "f_intra_os", "f_cc"]:
    F.loc[F[c].abs() > LIM, c] = np.nan
sp = decomp(SPOT, start="2017-01-01")
F = F.join(sp[["gap", "intra", "cc_p", "o", "c"]].rename(columns={"o": "s_o", "c": "s_c"}), how="left")
F["basis_open"] = np.log(O / F.s_o); F["basis_close"] = np.log(U / F.s_c)
F["prev_gap_ok"] = pd.Series(front.prev_date, index=front.index).notna()
F.to_parquet(R + f"/b2_{UND}.parquet")
# --- ACILIS hangi saat? ---
z = F.dropna(subset=["f_gap", "gap"])
print("corr(f_gap, spot gap)", round(z.f_gap.corr(z.gap), 3), " corr(f_gap, spot cc)", round(z.f_gap.corr(z.cc_p), 3), " sd f_gap", round(1e4*z.f_gap.std(), 1), "sd spot gap", round(1e4*z.gap.std(), 1))
z = F.dropna(subset=["f_intra", "intra"])
print("corr(f_intra, spot intra)", round(z.f_intra.corr(z.intra), 3), " sd", round(1e4*z.f_intra.std(), 1), round(1e4*z.intra.std(), 1))
print("ACILIS == ACILIS SEANSI (varken):", round((np.abs(O / OS - 1) < 1e-9)[OS.notna()].mean(), 3), " açılış seansı olan gün oranı", round(F.has_os.mean(), 3))
print("sd(basis_open - basis_close) bps", round(1e4*(F.basis_open - F.basis_close).std(), 1), "medyan |..|", round(1e4*(F.basis_open - F.basis_close).abs().median(), 1))
# --- Ortalamalar ---
def row(nm, s):
    s = s.dropna(); return dict(seri=nm, n=len(s), bps=1e4*s.mean(), t=tstat(s), medyan=1e4*s.median())
out = []
for per, sl in [("all", slice(None)), ("2017-2019", slice("2017", "2019")), ("2020-2022", slice("2020", "2022")), ("2023-2024", slice("2023", "2024")), ("2025-2026", slice("2025", "2026"))]:
    z = F.loc[sl]; zz = z.dropna(subset=["f_intra", "intra"])
    for nm in ["f_gap", "f_intra", "f_intra_s", "f_intra_os", "gap", "intra"]:
        r = row(nm, z[nm] if nm in ["f_gap", "gap"] else zz[nm]); r["per"] = per; out.append(r)
T = pd.DataFrame(out); print(T.pivot_table(index="seri", columns="per", values=["bps", "t", "n"], sort=False).round(2).to_string())
print("\nYıllık f_intra vs spot intra (ortak günler):")
zz = F.dropna(subset=["f_intra", "intra"])
Y = zz.groupby(zz.index.year).agg(n=("f_intra", "size"), f_gap=("f_gap", lambda s: 1e4*s.mean()), f_intra=("f_intra", lambda s: 1e4*s.mean()),
                                  f_intra_s=("f_intra_s", lambda s: 1e4*s.mean()), s_gap=("gap", lambda s: 1e4*s.mean()), s_intra=("intra", lambda s: 1e4*s.mean()),
                                  t_f=("f_intra", tstat))
print(Y.round(2).to_string())
T.to_csv(R + f"/b2_{UND}_summary.csv", index=False); Y.to_csv(R + f"/b2_{UND}_years.csv")
