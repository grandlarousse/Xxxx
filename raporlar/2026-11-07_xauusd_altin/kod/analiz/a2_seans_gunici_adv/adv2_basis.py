"""İddia 2 (ebres_{t-1} -> VİOP - spot göreli getiri) saldırısı."""
from adv_common import *
v = load_viop()
carry = v.ust_nom3m / 100 * v.v_dte / 365
braw = np.log(v.v_settle / v.xau_p15); eb = braw - carry
isd = pd.concat([eb, v.v_dte], axis=1).dropna(); isd = isd[isd.index <= IS_END]
b = np.polyfit(isd.iloc[:, 1], isd.iloc[:, 0], 1); ebr = eb - (b[0] * v.v_dte + b[1])
s15 = np.log(v.xau_p15 / v.xau_p15_prev); relret = v.v_ret - s15
rel = {h: fwd(relret, h) for h in (1, 3, 5, 10)}
x = ebr.shift(1)
# 0) yeniden üretim
for h in (1, 3, 5):
    r = ic(x, rel[h], max(h, 5)); ri = ic(x[x.index <= IS_END], rel[h][rel[h].index <= IS_END], max(h, 5)); ro = ic(x[x.index > IS_END], rel[h][rel[h].index > IS_END], max(h, 5))
    print(f"h={h}: IC {r['ic']:.4f} t {r['t']:.2f} | IS {ri['t']:.2f} | OOS {ro['t']:.2f} n {r['n']}")
# 1) NW lag duyarlılığı (h=5)
print("\nNW lag duyarlılığı h=5:", {L: round(ic(x, rel[5], L)["t"], 2) for L in (5, 10, 20, 40)})
print("NW lag duyarlılığı h=3:", {L: round(ic(x, rel[3], L)["t"], 2) for L in (5, 10, 20, 40)})
# örtüşmesiz (her 5. gün) alt örneklem
for off in range(5):
    idx = x.index[off::5]; r = ic(x.reindex(idx), rel[5].reindex(idx), 2)
    print(f"  örtüşmesiz h=5 ofset {off}: IC {r['ic']:.4f} t {r['t']:.2f} n {r['n']}")
# 2) alt dönemler
print("\nAlt dönem h=5:", sub_ic(x, rel[5], 5)); print("Alt dönem h=3:", sub_ic(x, rel[3], 3))
# 3) yıl yıl
d = pd.concat([x.rename("x"), rel[5].rename("y")], axis=1).dropna()
print("Yıl yıl IC h=5:", d.groupby(d.index.year).apply(lambda g: round(g.x.corr(g.y, method="spearman"), 3)).to_dict())
# 4) gecikme (eski bilgi) ve placebo
print("\nGecikme duyarlılığı h=5 (ebr_{t-k}):", {k: round(ic(ebr.shift(k), rel[5], 5)["t"], 2) for k in (1, 2, 3, 5, 10)})
# 5) stale / düşük hacim: t-1 hacmi
vol1 = v.v_volume.shift(1)
for nm, m in [("t-1 hacim > medyan", vol1 > vol1.median()), ("t-1 hacim <= medyan", vol1 <= vol1.median()), ("t-1 hacim > q25", vol1 > vol1.quantile(.25))]:
    r = ic(x[m], rel[5][m], 5); print(f"  {nm}: IC {r['ic']:.4f} t {r['t']:.2f} n {r['n']}")
# 6) kontroller: dte, faiz, eb_t-1'in kendi değişimi
X = pd.concat([x.rename("ebr"), v.v_dte.shift(1).rename("dte"), v.ust_nom3m.shift(1).rename("r")], axis=1)
import statsmodels.api as sm
dd = pd.concat([rel[5].rename("y"), X], axis=1).dropna()
m = sm.OLS(dd.y, sm.add_constant(dd[["ebr", "dte", "r"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
print("\nOLS rel5 ~ ebr + dte + r (NW10): t", m.tvalues.round(2).to_dict(), "b_ebr", round(m.params["ebr"], 3))
# winsor & uç dönemler & 2026 hariç
w = x.clip(x.quantile(.01), x.quantile(.99)); rw = rel[5].clip(rel[5].quantile(.01), rel[5].quantile(.99))
print("Winsor (x ve y) Pearson h=5:", round(ic(w, rw, 5, "pearson")["t"], 2), " | 2026 hariç:", round(ic(x[x.index < "2026-01-01"], rel[5][rel[5].index < "2026-01-01"], 5)["t"], 2),
      " | 2020-03 & 2026-01/02 hariç:", round(ic(x[~(((x.index >= "2020-03-01") & (x.index <= "2020-03-31")) | ((x.index >= "2026-01-01") & (x.index <= "2026-02-28")))], rel[5], 5)["t"], 2))
# roll içermeyen pencereler
ch = v.v_code.ne(v.v_code.shift()).astype(int); ch.iloc[0] = 0
noroll = sum(ch.shift(-k).fillna(0) for k in range(0, 6)) == 0
print("Roll penceresi (t..t+5) hariç:", round(ic(x[noroll], rel[5][noroll], 5)["t"], 2), "n", int(noroll.sum()))
# 7) parametre duyarlılığı: işlem kuralı, eşikler, h; göreli getiri; iki bacak maliyet
print("\nGöreli değer kuralı (pos = -1 eb yüksek / +1 eb düşük), maliyet iki bacak 10 bps (20 stres):")
rows = []
for qq in (0.2, 1 / 3, 0.4, 0.5):
    lo, hi = ebr[ebr.index <= IS_END].quantile([qq, 1 - qq]).values
    pos = pd.Series(np.where(x > hi, -1.0, np.where(x < lo, 1.0, 0.0)), index=v.index)
    for h in (1, 3, 5, 10):
        for c in (0, 10, 20):
            bs = bt_summary(pos, relret.dropna(), h, c)
            rows.append(dict(q=round(qq, 2), h=h, cost=c, full=bs["full"]["sharpe"], IS=bs["is"]["sharpe"], OOS=bs["oos"]["sharpe"], OOS_dm=bs["oos"]["sharpe_demeaned"], full_dm=bs["full"]["sharpe_demeaned"], ann_oos=bs["oos"]["ann"], turn=bs["full"]["turnover"]))
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(f"{OUT}/adv2_rv_grid.csv", index=False)
# sürekli pozisyon (z, IS std ile, clip)
z = (x / ebr[ebr.index <= IS_END].std()).clip(-1, 1) * -1
for h in (3, 5):
    for c in (0, 10):
        bs = bt_summary(z, relret.dropna(), h, c); print(f"  sürekli z h={h} cost {c}: full {bs['full']['sharpe']} IS {bs['is']['sharpe']} OOS {bs['oos']['sharpe']} OOS_dm {bs['oos']['sharpe_demeaned']}")
# bacaklar (q=1/3, h=5, cost 10): kısa-VİOP bacak (eb yüksek) / uzun-VİOP bacak (eb düşük)
lo, hi = ebr[ebr.index <= IS_END].quantile([1 / 3, 2 / 3]).values
pos = pd.Series(np.where(x > hi, -1.0, np.where(x < lo, 1.0, 0.0)), index=v.index)
for nm, p in [("kısa VİOP/uzun spot (eb yüksek)", pos.clip(upper=0)), ("uzun VİOP/kısa spot (eb düşük)", pos.clip(lower=0))]:
    bs = bt_summary(p, relret.dropna(), 5, 10); print(f"  {nm}: full {bs['full']['sharpe']} (dm {bs['full']['sharpe_demeaned']}) IS {bs['is']['sharpe']} OOS {bs['oos']['sharpe']} (dm {bs['oos']['sharpe_demeaned']})")
print("relret drift bps/gün: tam", round(relret.mean() * 1e4, 2), " IS", round(relret[relret.index <= IS_END].mean() * 1e4, 2), " OOS", round(relret[relret.index > IS_END].mean() * 1e4, 2))
print("pozisyon ortalaması (net kısa eğilimi) tam/IS/OOS:", round(pos.mean(), 3), round(pos[pos.index <= IS_END].mean(), 3), round(pos[pos.index > IS_END].mean(), 3))
# çıplak VİOP (yalnız VİOP bacağı, kullanıcı için tek uygulanabilir şey) h=5
for c in (5, 10):
    bs = bt_summary(pos, v.v_ret, 5, c); print(f"  Çıplak VİOP (aynı kural) h=5 cost {c}: full {bs['full']['sharpe']} IS {bs['is']['sharpe']} OOS {bs['oos']['sharpe']} OOS_dm {bs['oos']['sharpe_demeaned']}")
