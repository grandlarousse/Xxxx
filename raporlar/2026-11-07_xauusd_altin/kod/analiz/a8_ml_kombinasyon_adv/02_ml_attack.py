"""Hakem: A8-1 (ML genel), A8-5 (C1), A8-6 (V2 RF h3) saldırıları — analistin walk-forward tahmin dosyalarından (preds_V*.parquet)
yeniden değerlendirme: alt dönemler, drift (demeaned, yıl-içi demeaned, demeaned uzun/kısa), 10 bps, uç dönem dışlama, roll dışlama,
komşu model/ufuk, aylık/çeyreklik demeaned IC. Ayrıca C1 sabit (genişleyen z) kuralı bağımsız yeniden kurulur."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon")
from lib_altin import load_viop, load_spot, ic, backtest, fwd
A8 = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon"
OUT = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon_adv"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 500)
d = load_viop(); ret = d.v_ret
roll = (d.v_code != d.v_code.shift(1))
ext = ((d.index >= "2020-03-01") & (d.index <= "2020-03-31")) | ((d.index >= "2026-01-01") & (d.index <= "2026-02-28"))


def sh(pos, r, h, cost=5.0, demean=False):
    b = backtest(pos.reindex(r.index).fillna(0), r, h, cost, demean=demean)
    return np.nan if b is None else round(b["sharpe"], 2)


PER = {"2017-19": ("2017-03-01", "2019-12-31"), "2020-21": ("2020-01-01", "2021-12-31"), "2022-23": ("2022-01-01", "2023-12-31"),
       "2024-26": ("2024-01-01", "2026-12-31"), "OOS": ("2022-01-01", "2026-12-31"), "ALL20": ("2020-01-01", "2026-12-31")}


def evaluate(x, h, tag):
    pos = np.sign(x)
    y = fwd(ret, h); row = dict(tag=tag, h=h)
    for pn, (a, b) in PER.items():
        rr = ret.loc[a:b].dropna()
        if x.loc[a:b].notna().sum() < 100: continue
        row[f"t_{pn}"] = round(ic(x.loc[a:b], y.loc[a:b], max(h, 5))["t"], 2)
        row[f"sh_{pn}"] = sh(pos, rr, h)
    ro = ret.loc["2022":].dropna(); rdm = ro - ro.mean()
    row["oos_dm"] = sh(pos, ro, h, demean=True); row["oos_10"] = sh(pos, ro, h, 10.0)
    row["oos_long_dm"] = sh(pos.clip(lower=0), rdm, h); row["oos_short_dm"] = sh(pos.clip(upper=0), rdm, h)
    row["oos_long"] = sh(pos.clip(lower=0), ro, h); row["oos_short"] = sh(pos.clip(upper=0), ro, h)
    ryd = ro - ro.groupby(ro.index.year).transform("mean"); row["oos_yrdm"] = sh(pos, ryd, h)
    rqd = ro - ro.groupby(ro.index.to_period("Q")).transform("mean"); row["oos_qdm"] = sh(pos, rqd, h)
    row["oos_exext"] = sh(pos, ro[~ext[d.index > "2021-12-31"]], h)
    # roll içeren tutuşları sıfırla
    rollwin = sum(roll.shift(-k).fillna(False).astype(int) for k in range(1, h + 1)) > 0
    row["oos_noroll"] = sh(pos.where(~rollwin, 0), ro, h)
    row["frac_long_oos"] = round(float((pos.loc["2022":] > 0).mean()), 2)
    # aylık demeaned IC (hem x hem y ay ortalamasından arındırılmış; trend/rejim etkisini ayıklar)
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna().loc["2022":]
    g = dd.index.to_period("M")
    dm = dd - dd.groupby(g).transform("mean")
    row["t_oos_mdm"] = round(ic(dm.x, dm.y, max(h, 5))["t"], 2)
    return row


rows = []
# A8-1 / A8-6 / ML: analistin tahminleri
for V in ("V1", "V2"):
    P_ = pd.read_parquet(f"{A8}/preds_{V}.parquet"); P_["date"] = pd.to_datetime(P_["date"])
    ML = ["ridge", "lasso", "enet", "hgb", "rf"]
    ens = P_[P_.model.isin(ML)].groupby(["date", "h"]).agg(yhat=("yhat", "mean"), ybar=("ybar", "first"), ybar_w=("ybar_w", "first")).reset_index(); ens["model"] = "ens_ml"
    P_ = pd.concat([P_, ens], ignore_index=True)
    for m in ML + ["ens_ml", "c1_apriori", "c2_icsign_sel"]:
        for h in (1, 3, 5):
            q = P_[(P_.model == m) & (P_.h == h)].set_index("date")
            if m.startswith("c"):
                x = P_[(P_.model == m + "_score") & (P_.h == h)].set_index("date").yhat
            else:
                x = q.yhat - q.ybar_w
            x = x.where(x.abs() > 1e-9, 0.0)
            rows.append(evaluate(x.reindex(d.index), h, f"{V}_{m}"))
R = pd.DataFrame(rows)
# C1 sabit (genişleyen z), bağımsız yeniden kurulum — analistin öznitelikleri features.py'den
from features import build
from models import C1
Xs, XV, info, s, dd_ = build()
for h in (1, 3, 5):
    zs = []
    for c in C1:
        x = XV[c] * C1[c]; mu = x.expanding(250).mean().shift(1); sd = x.expanding(250).std().shift(1)
        zs.append(((x - mu) / sd).clip(-3, 3))
    z = pd.concat(zs, axis=1).mean(axis=1)
    r = evaluate(z, h, "C1_sabit_expanding")
    y = fwd(ret, h)
    r["t_full17"] = round(ic(z.loc["2017-03":], y.loc["2017-03":], max(h, 5))["t"], 2)
    r["sh_full17"] = sh(np.sign(z), ret.loc["2017-03":].dropna(), h)
    rows.append(r)
    # C1 komşu: eşit ağırlık yerine yalnız momentum (r20+r250) ve yalnız r250
    for nm, cols in {"C1_yavas": ["px_r20", "px_r250"], "C1_hizli": ["xa_dxy_d5", "rt_real10_d5", "sh_prem_d5", "cot_mm_z52"], "C1_eksi_cot": [c for c in C1 if c != "cot_mm_z52"]}.items():
        zs = []
        for c in cols:
            x = XV[c] * C1[c]; mu = x.expanding(250).mean().shift(1); sd = x.expanding(250).std().shift(1)
            zs.append(((x - mu) / sd).clip(-3, 3))
        zz = pd.concat(zs, axis=1).mean(axis=1)
        rr = evaluate(zz, h, nm); rr["t_full17"] = round(ic(zz.loc["2017-03":], y.loc["2017-03":], max(h, 5))["t"], 2)
        rr["sh_full17"] = sh(np.sign(zz), ret.loc["2017-03":].dropna(), h); rows.append(rr)
R = pd.DataFrame(rows)
R.to_csv(f"{OUT}/ml_attack.csv", index=False)
c1 = ["tag", "h", "t_2017-19", "t_2020-21", "t_2022-23", "t_2024-26", "t_OOS", "t_oos_mdm", "sh_2017-19", "sh_2020-21", "sh_2022-23", "sh_2024-26", "sh_OOS", "oos_dm", "oos_yrdm", "oos_qdm", "oos_10", "oos_long", "oos_short", "oos_long_dm", "oos_short_dm", "oos_exext", "oos_noroll", "frac_long_oos", "t_full17", "sh_full17"]
print(R[[c for c in c1 if c in R]].to_string(index=False))

# V2 RF h3: yıllık katkı ve en iyi 20 günün etkisi
P2 = pd.read_parquet(f"{A8}/preds_V2.parquet"); P2["date"] = pd.to_datetime(P2["date"])
q = P2[(P2.model == "rf") & (P2.h == 3)].set_index("date"); x = (q.yhat - q.ybar_w).reindex(d.index)
pos = np.sign(x); ro = ret.loc["2022":].dropna()
b = backtest(pos.reindex(ro.index).fillna(0), ro, 3, 5.0); pnl = b["pnl"]
print("RF h3 OOS yıllık Sharpe:", pnl.groupby(pnl.index.year).apply(lambda v: round(v.mean() / v.std() * np.sqrt(252), 2)).to_dict())
print("RF h3 OOS toplam log pnl:", round(pnl.sum(), 3), "yıllık:", pnl.groupby(pnl.index.year).sum().round(3).to_dict())
top = pnl.abs().sort_values(ascending=False).index[:20]
p2 = pnl.drop(top); print("en büyük |pnl| 20 gün atılınca Sharpe:", round(p2.mean() / p2.std() * np.sqrt(252), 2))
# 2023 hariç
p3 = pnl[pnl.index.year != 2023]; print("2023 hariç OOS Sharpe:", round(p3.mean() / p3.std() * np.sqrt(252), 2))
# C1 walk-forward h1 aynı tanılar
q = P_ = pd.read_parquet(f"{A8}/preds_V1.parquet"); q["date"] = pd.to_datetime(q["date"])
sc = q[(q.model == "c1_apriori_score") & (q.h == 1)].set_index("date").yhat.reindex(d.index)
b = backtest(np.sign(sc).reindex(ro.index).fillna(0), ro, 1, 5.0); pnl = b["pnl"]
print("C1 WF h1 OOS yıllık Sharpe:", pnl.groupby(pnl.index.year).apply(lambda v: round(v.mean() / v.std() * np.sqrt(252), 2)).to_dict())
print("C1 WF h1 OOS uzun oranı yıllık:", (np.sign(sc).loc["2022":] > 0).groupby(sc.loc["2022":].index.year).mean().round(2).to_dict())
p3 = pnl[pnl.index.year != 2025]; print("2025 hariç C1 OOS Sharpe:", round(p3.mean() / p3.std() * np.sqrt(252), 2))
