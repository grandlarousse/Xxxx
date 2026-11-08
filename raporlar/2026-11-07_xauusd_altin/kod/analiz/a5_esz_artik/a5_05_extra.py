"""Adım 5: en güçlü aday (C1: büyük makro hareketli günlerde 12-15 UTC altın artığı, h=3) ve B1 (altın/gümüş 5 günlük göreli hareket) için
ek çürütme testleri. Kayda ekler. Çıktı: extra.csv, c1_trades_by_year.csv"""
from a5_lib import *
import statsmodels.api as sm

sig = pd.read_parquet(f"{OUT}/signals_spot.parquet")
vp = load_viop(); V = lambda s: s.reindex(vp.index)
Y = {h: vp[f"fwd{h}"] for h in (1, 3, 5)}
rows = []


def run(tid, pred, x, h, note=""):
    st = split_stats(x, Y[h], h); register(AGENT, "X_extra", tid, pred, h, st, note)
    rows.append(dict(test_id=tid, pred=pred, h=h, note=note, **{k: v for k, v in st.items() if k != "by_year"}, by_year=st["by_year"]))
    return st


f = V(sig.I12F_MACRO3_W60); e = V(sig.I12_MACRO3_W60); g12 = V(sig.g12)
isq = lambda s, q: s.abs()[s.index <= IS_END].quantile(q)
# 1) eşik duyarlılığı
for q in (0.7, 0.9):
    for h in (1, 3, 5):
        run(f"X_C1_q{int(q*100)}_h{h}", f"I12_MACRO3_W60 | |fit|>q{int(q*100)}", e.where(f.abs() > isq(f, q)), h, "eşik duyarlılığı")
# 2) aynı günlerde altının kendi 12-15 getirisi (kontrol) ve kısmi regresyon
m80 = f.abs() > isq(f, 0.8)
for h in (1, 3, 5):
    run(f"X_C1_g12own_h{h}", "g12 | |fit|>q80", g12.where(m80), h, "kontrol: kendi getirisi aynı günler")
part = []
for h in (1, 3, 5):
    d = pd.concat([Y[h].rename("y"), e.rename("resid"), g12.rename("g12"), f.rename("fit")], axis=1)[m80].dropna()
    Z = (d - d.mean()) / d.std()
    mm = sm.OLS(Z.y, sm.add_constant(Z[["resid", "fit"]])).fit(cov_type="HAC", cov_kwds={"maxlags": max(h, 5)})
    part.append(dict(h=h, n=len(d), b_resid=round(mm.params.resid, 3), t_resid=round(mm.tvalues.resid, 2), b_fit=round(mm.params.fit, 3), t_fit=round(mm.tvalues.fit, 2)))
    register(AGENT, "X_extra", f"X_C1_partial_resid_fit_h{h}", "resid | fit (q80 günleri)", h, dict(ic=mm.params.resid, t=mm.tvalues.resid, n=len(d)), "kısmi")
# 3) koşul altının KENDİ büyük hareketi (|g12| q80) — makro günü mü yoksa sadece büyük altın günü mü?
mg = g12.abs() > isq(g12, 0.8)
for h in (1, 3, 5):
    run(f"X_C1_condg12_h{h}", "I12_MACRO3_W60 | |g12|>q80", e.where(mg), h, "koşul: büyük altın hareketi")
    run(f"X_C1_notcond_h{h}", "I12_MACRO3_W60 | |fit|<=q80", e.where(~m80 & f.notna()), h, "tamamlayıcı: sakin makro günleri")
# 4) tek faktörlü koşullu sürümler
for m in ("DXY", "TBOND", "SPX"):
    fm = V(sig[f"I12F_{m}_W60"]); em = V(sig[f"I12_{m}_W60"])
    for h in (1, 3, 5):
        run(f"X_C1_{m}_q80_h{h}", f"I12_{m}_W60 | |fit|>q80", em.where(fm.abs() > isq(fm, 0.8)), h, "tek faktör koşullu")
# 5) en iyi yıl (2020) ve son dönem (2026) hariç; Pearson (getiri ağırlıklı) sürüm
c1 = e.where(m80)
run("X_C1_ex2020_h3", "C1 2020 hariç", c1.where(c1.index.year != 2020), 3, "en iyi yıl hariç")
run("X_C1_ex2020_2026_h3", "C1 2020 ve 2026 hariç", c1.where(~c1.index.year.isin([2020, 2026])), 3, "iki en iyi yıl hariç")
st = split_stats(c1, Y[3], 3, method="pearson"); register(AGENT, "X_extra", "X_C1_pearson_h3", "C1 Pearson", 3, st, "Pearson IC")
rows.append(dict(test_id="X_C1_pearson_h3", pred="C1 Pearson", h=3, note="Pearson", **{k: v for k, v in st.items() if k != "by_year"}, by_year=st["by_year"]))
st = split_stats(c1.clip(-3, 3), Y[3], 3, method="pearson"); register(AGENT, "X_extra", "X_C1_pearson_clip3_h3", "C1 Pearson |z|<=3", 3, st, "Pearson, sinyal ±3'te kırpılmış")
rows.append(dict(test_id="X_C1_pearson_clip3_h3", pred="C1 Pearson clip3", h=3, note="Pearson clip", **{k: v for k, v in st.items() if k != "by_year"}, by_year=st["by_year"]))
X = pd.DataFrame(rows); X.to_csv(f"{OUT}/extra.csv", index=False)
pd.DataFrame(part).to_csv(f"{OUT}/c1_partial.csv", index=False)
# 5) C1 işlem sayıları ve yıllık net getiri (sign kuralı, h=3, 5 bps)
pos = np.sign(e.where(m80)).fillna(0)
bt = backtest(pos, vp.v_ret, 3, COST_BPS)
pnl = bt["pnl"]; yr = pd.DataFrame(dict(signals=pos.ne(0).groupby(pos.index.year).sum(), longs=pos.gt(0).groupby(pos.index.year).sum(),
                                       net_ret_pct=(pnl.groupby(pnl.index.year).sum() * 100).round(2)))
# işlem başı (3 gün tutuş) ortalama getiri, bps
r3 = (pos * Y[3])[pos != 0]
yr["avg_trade_bps"] = (r3.groupby(r3.index.year).mean() * 1e4).round(1)
yr.to_csv(f"{OUT}/c1_trades_by_year.csv")
pd.set_option("display.width", 250)
print(X[["test_id", "ic", "t", "t_is", "t_oos", "ic_oos", "yrs_same_sign", "yrs", "n"]].round(3).to_string())
print(pd.DataFrame(part).to_string())
print(yr.to_string())
print("işlem başı ort (bps, brüt):", round(r3.mean() * 1e4, 1), "IS:", round(r3[r3.index <= IS_END].mean() * 1e4, 1), "OOS:", round(r3[r3.index > IS_END].mean() * 1e4, 1), "n", len(r3))
print("long işlemler ort bps:", round((Y[3][pos > 0]).mean() * 1e4, 1), "short işlemler ort bps (short getirisi):", round((-Y[3][pos < 0]).mean() * 1e4, 1), "koşulsuz 3g ort bps:", round(Y[3].mean() * 1e4, 1))
