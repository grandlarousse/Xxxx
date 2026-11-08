"""Adım 4: aynı ızgara SPOT hedefle (sfwd{h} = 15:00 UTC -> 15:00 UTC Dukascopy, 2016+; IS = 2016-01..2021-12).
Not: sfwd'nin başlangıcı (p15_t) sinyalin bitiş fiyatıyla aynı görüntü -> BID görüntü gürültüsü artık sinyallerinde
mekanik negatif IC (sahte dönüş) yaratabilir; adaylar için 1 saat atlamalı hedef a5_03'te. Kayda ekler. Çıktı: grid_spot.csv"""
from a5_lib import *

sig = pd.read_parquet(f"{OUT}/signals_spot.parquet")
rows = []


def run(fam, tid, col, x, h, note=""):
    st = split_stats(x, sig[f"sfwd{h}"], h)
    register(AGENT, fam, tid, col, h, st, note)
    rows.append(dict(fam=fam, test_id=tid, col=col, h=h, **{k: v for k, v in st.items() if k != "by_year"}, by_year=st["by_year"]))


models = ["XAG", "DXY", "TBOND", "SPX", "USDJPY", "USDCNH", "BTC", "EURUSD", "MACRO3", "FX3", "ALL7"]
for m in models:
    for W in (60, 120, 250):
        for k in (1, 3, 5):
            c = f"R_{m}_W{W}_k{k}"
            for h in (1, 3, 5):
                run("A_resid_spot", f"As_{m}_W{W}_k{k}_h{h}", c, sig[c], h)
    for h in (1, 3, 5):
        run("A_fitted_spot", f"AFs_{m}_W120_h{h}", f"F_{m}_W120", sig[f"F_{m}_W120"], h)
for k in (1, 3, 5):
    for h in (1, 3, 5):
        run("A_own_spot", f"AOs_g_k{k}_h{h}", f"g_sum{k}", sig.g.rolling(k).sum(), h)
for L in (20, 60, 120):
    for h in (1, 3, 5):
        run("B_ratio_spot", f"Bs_GSRZ_L{L}_h{h}", f"GSRZ_L{L}", sig[f"GSRZ_L{L}"], h)
        run("B_ratio_spot", f"Bs_GPTZ_L{L}_h{h}", f"GPTZ_L{L}", sig[f"GPTZ_L{L}"], h)
for k in (1, 3, 5):
    for h in (1, 3, 5):
        run("B_ratio_spot", f"Bs_GSRD_k{k}_h{h}", f"GSRD_k{k}", sig[f"GSRD_k{k}"], h)
        run("B_ratio_spot", f"Bs_GPTD_k{k}_h{h}", f"GPTD_k{k}", sig[f"GPTD_k{k}"], h)
for m in ("DXY", "TBOND", "SPX", "MACRO3"):
    for W in (60, 120, 250):
        for h in (1, 3, 5):
            run("C_intraday_spot", f"Cs_I12_{m}_W{W}_h{h}", f"I12_{m}_W{W}", sig[f"I12_{m}_W{W}"], h)
for W in (60, 120, 250):
    f = sig[f"I12F_MACRO3_W{W}"]; thr = f.abs()[f.index <= IS_END].quantile(0.8)
    for h in (1, 3, 5):
        run("C_intraday_spot", f"Cs_I07_MACRO3_W{W}_h{h}", f"I07_MACRO3_W{W}", sig[f"I07_MACRO3_W{W}"], h)
        run("C_intraday_spot", f"Cs_I12c_MACRO3_W{W}_h{h}", f"I12_MACRO3_W{W}|fit>q80", sig[f"I12_MACRO3_W{W}"].where(f.abs() > thr), h)
        run("C_intraday_spot", f"Cs_I12F_MACRO3_W{W}_h{h}", f"I12F_MACRO3_W{W}", f, h)
G = pd.DataFrame(rows); G.to_csv(f"{OUT}/grid_spot.csv", index=False)
print("spot ızgara test sayısı:", len(G))
print(G.groupby("fam").agg(n=("t", "size"), n_abs_t_gt2=("t", lambda s: int((s.abs() > 2).sum())), mean_t=("t", "mean")).round(2))
gv = pd.read_csv(f"{OUT}/grid_viop.csv")
gv["key"] = gv.test_id.str.replace("^(A|AF|AO|B|C)_", "", regex=True); G["key"] = G.test_id.str.replace("^(As|AFs|AOs|Bs|Cs)_", "", regex=True)
M = gv.merge(G[["key", "t", "t_is", "t_oos"]], on="key", suffixes=("_viop", "_spot"))
print("VİOP vs spot t korelasyonu:", round(M.t_viop.corr(M.t_spot), 2), "| aynı işaret oranı:", round((np.sign(M.t_viop) == np.sign(M.t_spot)).mean(), 2), "| n eşleşen:", len(M))
print(M.reindex(M.t_spot.abs().sort_values(ascending=False).index).head(15)[["key", "t_viop", "t_spot", "t_is_spot", "t_oos_spot"]].round(2).to_string())
