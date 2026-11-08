"""Hakem: A8-2 (rt_nom2_d5), A8-3 (seg_last1h), A8-4 (rt_curve_2s10s_d5) saldırıları.
Öznitelikleri ham panel sütunlarından BAĞIMSIZ yeniden kurar (analistin features.py'sini kullanmaz), sonra:
alt dönem, komşu parametre, 10 bps, uç dönem dışlama, roll dışlama, demeaned / uzun / kısa, spot 2010-16, placebo."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
from lib_altin import load_viop, load_spot, ic, backtest, fwd, IS_END

OUT = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon_adv"
d = load_viop(); s = load_spot()
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 50)


def feats(df):
    F = {}
    for k in (1, 2, 3, 5, 7, 10, 15, 20):
        F[f"nom2_d{k}"] = df.ust_nom2.diff(k)
        F[f"curve_d{k}"] = (df.ust_nom10 - df.ust_nom2).diff(k)
    F["nom2_lag_d5"] = df.ust_nom2.shift(1).diff(5)  # bir gün daha eski
    F["seg_last1h"] = np.log(df.xau_p15 / df.xau_p14)
    F["seg_13_15"] = np.log(df.xau_p15 / df.xau_p13)
    F["seg_12_15"] = np.log(df.xau_p15 / df.xau_p12)
    F["seg_13_14"] = np.log(df.xau_p14 / df.xau_p13)
    return pd.DataFrame(F)


# VİOP: spot panelinde hesapla, VİOP günlerine as-of taşı (analistle aynı mantık) ve ayrıca doğrudan VİOP panelinde
FS = feats(s)
FV_asof = FS.reindex(FS.index.union(d.index)).ffill(limit=2).reindex(d.index)
FV_direct = feats(d)
ret = d.v_ret
roll = (d.v_code != d.v_code.shift(1))

PER = {"2017-19": ("2017-03-01", "2019-12-31"), "2020-21": ("2020-01-01", "2021-12-31"), "2022-23": ("2022-01-01", "2023-12-31"),
       "2024-26": ("2024-01-01", "2026-12-31"), "IS": ("2017-03-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31"), "FULL": ("2017-03-01", "2026-12-31")}


def sh(pos, r, h, cost=5.0, demean=False):
    b = backtest(pos.reindex(r.index).fillna(0), r, h, cost, demean=demean)
    return np.nan if b is None else round(b["sharpe"], 2)


def evaluate(x, sg, h, r=ret, F=None, tag=""):
    x = x * sg; pos = np.sign(x)
    y = fwd(r, h)
    row = dict(tag=tag, h=h)
    for pn, (a, b) in PER.items():
        rr = r.loc[a:b].dropna()
        st = ic(x.loc[a:b], y.loc[a:b], max(h, 5))
        row[f"t_{pn}"] = round(st["t"], 2)
        row[f"sh_{pn}"] = sh(pos, rr, h)
    rr = r.loc["2022":].dropna()
    row["oos_dm"] = sh(pos, rr, h, demean=True); row["oos_10bps"] = sh(pos, rr, h, 10.0)
    row["oos_long"] = sh(pos.clip(lower=0), rr, h); row["oos_short"] = sh(pos.clip(upper=0), rr, h)
    rf = r.loc["2017-03":].dropna()
    row["full_dm"] = sh(pos, rf, h, demean=True); row["full_long"] = sh(pos.clip(lower=0), rf, h); row["full_short"] = sh(pos.clip(upper=0), rf, h)
    row["full_10bps"] = sh(pos, rf, h, 10.0)
    # uç dönem dışlama: Mart 2020, Ocak-Şubat 2026 getirileri sıfırlanır (pozisyon yok)
    ex = r.copy(); m = ((ex.index >= "2020-03-01") & (ex.index <= "2020-03-31")) | ((ex.index >= "2026-01-01") & (ex.index <= "2026-02-28"))
    exr = ex[~m].loc["2022":].dropna()
    row["oos_ex_ext"] = sh(pos, exr, h)
    st_ex = ic(x[~m], y[~m], max(h, 5)); row["t_full_ex_ext"] = round(st_ex["t"], 2)
    # roll günü içeren pencereleri at (IC için)
    rollwin = sum(roll.shift(-k).fillna(False).astype(int) for k in range(1, h + 1)) > 0
    st_r = ic(x[~rollwin], y[~rollwin], max(h, 5)); row["t_full_noroll"] = round(st_r["t"], 2)
    # demeaned hedefle IC zaten rank korelasyonu; drift'ten bağımsız. yıl-içi demeaned getirili backtest:
    rd = rf - rf.groupby(rf.index.year).transform("mean")
    row["full_yr_dm"] = sh(pos, rd, h)
    # yıllar
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna().loc["2017-03":]
    yr = dd.groupby(dd.index.year).apply(lambda g: g.x.corr(g.y, method="spearman"))
    row["yrs_ic_pos"] = f"{int((yr > 0).sum())}/{len(yr)}"
    row["yr_ic"] = " ".join(f"{k%100}:{v:+.2f}" for k, v in yr.items())
    return row


rows = []
# A8-2 rt_nom2_d5, işaret -1
for k in (1, 2, 3, 5, 7, 10, 15, 20):
    for h in (1, 3, 5):
        rows.append(evaluate(FV_asof[f"nom2_d{k}"], -1, h, tag=f"-nom2_d{k}"))
rows.append(evaluate(FV_asof["nom2_lag_d5"], -1, 1, tag="-nom2_lag1_d5"))
rows.append(evaluate(FV_direct["nom2_d5"], -1, 1, tag="-nom2_d5_direct"))
# A8-4 curve
for k in (1, 2, 3, 5, 7, 10, 15, 20):
    for h in (1, 3, 5):
        rows.append(evaluate(FV_asof[f"curve_d{k}"], +1, h, tag=f"+curve_d{k}"))
rows.append(evaluate(FV_direct["curve_d5"], +1, 1, tag="+curve_d5_direct"))
# A8-3 seans
for f in ("seg_last1h", "seg_13_15", "seg_12_15", "seg_13_14"):
    for h in (1, 2, 3, 4, 5, 7, 10):
        rows.append(evaluate(FV_asof[f], +1, h, tag=f"+{f}"))
rows.append(evaluate(FV_direct["seg_last1h"], +1, 5, tag="+seg_last1h_direct"))
R = pd.DataFrame(rows)
R.to_csv(f"{OUT}/univ_attack.csv", index=False)
cols1 = ["tag", "h", "t_FULL", "t_IS", "t_OOS", "t_2017-19", "t_2020-21", "t_2022-23", "t_2024-26", "t_full_ex_ext", "t_full_noroll", "yrs_ic_pos"]
cols2 = ["tag", "h", "sh_FULL", "sh_IS", "sh_OOS", "sh_2017-19", "sh_2020-21", "sh_2022-23", "sh_2024-26", "oos_dm", "oos_10bps", "oos_long", "oos_short", "full_dm", "full_yr_dm", "full_long", "full_short", "full_10bps", "oos_ex_ext"]
print(R[cols1].to_string(index=False))
print(R[cols2].to_string(index=False))
print(R[["tag", "h", "yr_ic"]].to_string(index=False))

# Spot paneli: 2010-2016 ve 2017-2026 (s_ret, 15:00->15:00)
sp = []
for tag, x, sg, h in [("-nom2_d5", FS.nom2_d5, -1, 1), ("-nom2_d5", FS.nom2_d5, -1, 3), ("-nom2_d3", FS.nom2_d3, -1, 1), ("-nom2_d10", FS.nom2_d10, -1, 1),
                      ("+curve_d5", FS.curve_d5, 1, 1), ("+curve_d3", FS.curve_d3, 1, 1), ("+curve_d10", FS.curve_d10, 1, 1),
                      ("+seg_last1h", FS.seg_last1h, 1, 5), ("+seg_last1h", FS.seg_last1h, 1, 1), ("+seg_last1h", FS.seg_last1h, 1, 3), ("+seg_13_15", FS.seg_13_15, 1, 5)]:
    xx = x * sg; pos = np.sign(xx); y = fwd(s.s_ret, h)
    row = dict(tag=tag, h=h)
    for pn, (a, b) in {"2010-16": ("2010-01-01", "2016-12-31"), "2010-13": ("2010-01-01", "2013-12-31"), "2014-16": ("2014-01-01", "2016-12-31"), "2017-26": ("2017-01-01", "2026-12-31")}.items():
        st = ic(xx.loc[a:b], y.loc[a:b], max(h, 5)); rr = s.s_ret.loc[a:b].dropna()
        row[f"t_{pn}"] = round(st["t"], 2); row[f"ic_{pn}"] = round(st["ic"], 3); row[f"sh_{pn}"] = sh(pos, rr, h)
        row[f"shdm_{pn}"] = sh(pos, rr, h, demean=True)
    sp.append(row)
SP = pd.DataFrame(sp); SP.to_csv(f"{OUT}/univ_attack_spot.csv", index=False)
print(SP.to_string(index=False))

# placebo: geleceğe/geçmişe kaydırma
for tag, x, sg, h in [("nom2_d5", FV_asof.nom2_d5, -1, 1), ("curve_d5", FV_asof.curve_d5, 1, 1), ("seg_last1h", FV_asof.seg_last1h, 1, 5)]:
    y = fwd(ret, h)
    print(tag, {k: round(ic((x * sg).shift(k), y, max(h, 5))["t"], 2) for k in (-2, -1, 0, 1, 2, 3, 5)})
