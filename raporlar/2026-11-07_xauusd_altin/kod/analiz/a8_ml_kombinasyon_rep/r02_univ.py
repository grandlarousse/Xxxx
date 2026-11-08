"""Adım 2: A8-2 (−rt_nom2_d5, h1), A8-3 (+seg_last1h, h5), A8-4 (+rt_curve_2s10s_d5, h1) bağımsız yeniden hesap.
Öngörücüler kendi ham as-of serilerimden (r00_data): ust_* (t-1 22:00 UTC), spot p14/p15 (Dukascopy bar kapanışı).
VİOP hedefi kendi viop_long türevim. IC NW t (Bartlett, lag max(h,5)), kademeli geri test 5/10 bps.
Ek kontroller: yarım gün (arife) dışlama, VİOP endeksinde doğrudan hesap, placebo kaydırma, spot 2011–16 / 2011–26."""
import numpy as np, pandas as pd, json
from rep_stats import split_ic, ic_test, bt_full, bt
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
v = pd.read_parquet(f"{OUT}/base_viop.parquet"); sp = pd.read_parquet(f"{OUT}/base_spot.parquet")
hd = pd.read_parquet(f"{OUT}/halfday_flag.parquet").index

# spot endeksinde öznitelikler
F = pd.DataFrame(index=sp.index)
F["rt_nom2_d5"] = sp.ust_nom2.diff(5)
F["rt_curve_2s10s_d5"] = (sp.ust_nom10 - sp.ust_nom2).diff(5)
F["seg_last1h"] = np.log(sp.p15 / sp.p14)
# VİOP günlerine as-of (yalnız geçmiş; en fazla 2 satır ileri taşı)
FV = F.reindex(F.index.union(v.index)).ffill(limit=2).reindex(v.index)
# alternatif: doğrudan VİOP günü saatlik spot (spot kapalıysa NaN) ve VİOP satırlarında 5 satır fark
h = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet").c; h.index = h.index + pd.Timedelta(hours=1)
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
alt_last1h = np.log(pv.xau_p15 / pv.xau_p14)  # panel VİOP günü snap'i (r00'da spot için birebir doğrulandı)
SIG = {"A8-2": ("rt_nom2_d5", -1, 1), "A8-3": ("seg_last1h", +1, 5), "A8-4": ("rt_curve_2s10s_d5", +1, 1)}
per = {"FULL": ("2017-03-01", "2026-12-31"), "IS": ("2017-03-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31")}
res = {}
for cid, (f, sg, H) in SIG.items():
    x = FV[f] * sg; pos = np.sign(x).fillna(0)
    R = {"feature": f, "sign": sg, "h": H}
    for hh in (1, 3, 5):
        st = split_ic(x, v[f"fwd{hh}"], hh)
        R[f"ic_h{hh}"] = {k: (round(val, 4) if isinstance(val, float) else val) for k, val in st.items() if k != "by_year"}
        bts = {}
        for pn, (a, b) in per.items():
            rr = v.ret.loc[a:b]
            bts[pn] = bt_full(pos.loc[a:b], rr, hh)
        R[f"bt_h{hh}"] = bts
    R["by_year_h"] = split_ic(x, v[f"fwd{H}"], H)["by_year"]
    # yarım gün dışlama
    x_nohd = x.copy(); x_nohd[x_nohd.index.isin(hd)] = np.nan
    st = split_ic(x_nohd, v[f"fwd{H}"], H)
    R["ic_no_halfday"] = {k: round(st[k], 4) for k in ("ic", "t", "t_is", "t_oos")}
    pos_nohd = np.sign(x_nohd).fillna(0)
    R["bt_no_halfday_OOS"] = bt_full(pos_nohd.loc["2022":], v.ret.loc["2022":], H)
    R["bt_no_halfday_FULL"] = bt_full(pos_nohd, v.ret, H)
    # alternatif hesap
    if f == "seg_last1h":
        xa = alt_last1h * sg
    elif f == "rt_nom2_d5":
        xa = (pv.ust_nom2.diff(5)) * sg  # VİOP satırlarında 5 satır fark
    else:
        xa = ((pv.ust_nom10 - pv.ust_nom2).diff(5)) * sg
    st = split_ic(xa, v[f"fwd{H}"], H); R["ic_alt_viop_index"] = {k: round(st[k], 4) for k in ("ic", "t", "t_is", "t_oos")}
    R["bt_alt_OOS"] = bt_full(np.sign(xa).fillna(0).loc["2022":], v.ret.loc["2022":], H)
    # placebo: x'i kaydır (negatif = gelecek bilgi)
    R["placebo"] = {s_: round(ic_test(x.shift(s_), v[f"fwd{H}"], max(H, 5))["ic"], 4) for s_ in (-2, -1, 0, 1, 2)}
    # spot uzun örneklem (hedef sfwd, 15:00→15:00)
    xs = F[f] * sg
    e = ic_test(xs.loc["2011":"2016"], sp[f"sfwd{H}"].loc["2011":"2016"], max(H, 5))
    l = ic_test(xs.loc["2011":], sp[f"sfwd{H}"].loc["2011":], max(H, 5))
    dd = pd.concat([xs.rename("x"), sp[f"sfwd{H}"].rename("y")], axis=1).loc["2011":].dropna()
    yr = dd.groupby(dd.index.year).apply(lambda g: g.x.rank().corr(g.y.rank()))
    R["spot_2011_16"] = dict(ic=round(e["ic"], 4), t=round(e["t"], 3), bt=bt_full(np.sign(xs).fillna(0).loc["2011":"2016"], sp.s_ret.loc["2011":"2016"], H))
    R["spot_2011_26"] = dict(ic=round(l["ic"], 4), t=round(l["t"], 3), yrs=f"{int((np.sign(yr) == np.sign(l['ic'])).sum())}/{len(yr)}")
    # IS alt dönem 2017-21 Sharpe ayrıca
    res[cid] = R

# seg_last1h için h=1 OOS t ve uzun/kısa
x = FV.seg_last1h
res["A8-3"]["h1_oos_t"] = round(split_ic(x, v.fwd1, 1)["t_oos"], 3)

json.dump(res, open(f"{OUT}/univ_rep.json", "w"), indent=1, default=str)
for cid, R in res.items():
    H = R["h"]
    print("=====", cid, R["feature"], "sign", R["sign"], "h", H)
    print(" IC:", R[f"ic_h{H}"])
    for pn in per: print(f" BT {pn}:", R[f"bt_h{H}"][pn])
    print(" yarım gün hariç IC:", R["ic_no_halfday"], " OOS BT:", R["bt_no_halfday_OOS"])
    print(" alternatif (VİOP endeksi) IC:", R["ic_alt_viop_index"], " OOS BT:", R["bt_alt_OOS"])
    print(" placebo:", R["placebo"])
    print(" spot 2011-16:", R["spot_2011_16"]); print(" spot 2011-26:", R["spot_2011_26"])
    print(" yıllık IC:", R["by_year_h"])
    for hh in (1, 3, 5):
        if hh != H: print(f" diğer ufuk h={hh}: IC", {k: R[f'ic_h{hh}'][k] for k in ('ic', 't', 't_is', 't_oos')}, "OOS sh", R[f"bt_h{hh}"]["OOS"]["sh"])
print("A8-3 h1 OOS t:", res["A8-3"]["h1_oos_t"])
