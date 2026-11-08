"""Hakem: HSI h3, VİOP OI5×trend h5, GPR z250 h5, Çin artık sum5 h1 — bağımsız yeniden kurulum ve saldırılar."""
import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import load_viop, load_spot, fwd, nw_ols, ic, split_stats, backtest, IS_END
D = load_viop(); SP = load_spot(); R = D["v_ret"]
print("fwd5 tutarlılık:", float((D.fwd5 - fwd(R, 5)).abs().max()))
for _h in (2, 4, 6, 7):
    D[f"fwd{_h}"] = fwd(R, _h)
PER = {"2017-19": ("2017-01-01", "2019-12-31"), "2020-21": ("2020-01-01", "2021-12-31"), "2022-23": ("2022-01-01", "2023-12-31"), "2024-26": ("2024-01-01", "2026-12-31")}
EXT = ((D.index >= "2020-03-01") & (D.index <= "2020-04-30")) | ((D.index >= "2026-01-01") & (D.index <= "2026-02-28"))
ROLL = (D.v_code != D.v_code.shift(1)); ROLLN = (ROLL | ROLL.shift(1, fill_value=False) | ROLL.shift(-1, fill_value=False)).values
s_r1 = np.log(D.xau_p15 / D.xau_p15_prev); s_r5 = np.log(D.xau_p15 / D.xau_p15.shift(5)); s_715 = np.log(D.xau_p15 / D.xau_p07)
CTRL = pd.concat([s_r1.rename("r1"), s_r5.rename("r5"), s_715.rename("r715"), R.shift(1).rename("v1")], axis=1)

def sub_ic(x, h):
    y = D[f"fwd{h}"]; o = {}
    for k, (a, b) in PER.items():
        m = (D.index >= a) & (D.index <= b); r = ic(x[m], y[m], max(h, 5)); o[k] = f"{r['ic']:+.3f}({r['t']:+.2f})"
    return o

def sh_sub(pos, h, cost=5, demean=False):
    o = {}
    for k, (a, b) in list(PER.items()) + [("IS", ("2017", "2021-12-31")), ("OOS", ("2022", "2027")), ("full", ("2010", "2027"))]:
        m = (R.index >= a) & (R.index <= b); bt = backtest(pos[m], R[m], h, cost, demean=demean); o[k] = round(bt["sharpe"], 2) if bt else np.nan
    return o

def full_report(name, x, h, sgn):
    st = split_stats(x, D[f"fwd{h}"], h)
    print(f"\n### {name} h={h}: ic={st['ic']:+.3f} t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f} yrs {st['yrs_same_sign']}/{st['yrs']}")
    print("  alt dönem IC:", sub_ic(x, h))
    xz = (x - x.mean()) / x.std()
    for lab, m in [("tam", slice(None)), ("IS", D.index <= IS_END), ("OOS", D.index > IS_END)]:
        r_ = nw_ols(D[f"fwd{h}"][m], pd.concat([xz.rename("x"), CTRL], axis=1)[m], lags=max(h, 5)); print(f"  kontrollü {lab}: t={r_['t']:+.2f}", end=";")
    m = ~EXT & ~ROLLN; r = ic(x[m], D[f"fwd{h}"][m], max(h, 5)); print(f"\n  uç+roll hariç t={r['t']:+.2f}")
    pos = (sgn * np.sign(x)).fillna(0)
    print("  kural net5 :", sh_sub(pos, h)); print("  kural net10:", sh_sub(pos, h, 10)); print("  kural dm   :", sh_sub(pos, h, 5, True))
    print("  uzun  :", sh_sub(pos.clip(lower=0), h), " dm:", sh_sub(pos.clip(lower=0), h, 5, True))
    print("  kısa  :", sh_sub(pos.clip(upper=0), h), " dm:", sh_sub(pos.clip(upper=0), h, 5, True))
    print("  uzun oranı:", round((pos > 0).sum() / max((pos != 0).sum(), 1), 3))
    return pos

# ---------------- (A) HSI
def ret_known(P, tk):
    y = P[f"y_{tk}"]; a = pd.to_datetime(P[f"y_{tk}_avail"]); r = np.log(y).diff(); r[a == a.shift(1)] = np.nan; return r
hsi = ret_known(D, "_HSI")
for h in (1, 2, 3, 4, 5):
    st = split_stats(hsi, D[f"fwd{h}"], h); print(f"HSI h={h}: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}")
full_report("HSI", hsi, 3, 1)
hsis = ret_known(SP, "_HSI")
for h in (1, 3, 5):
    for a, b in [("2010", "2016-12-31"), ("2017", "2021-12-31"), ("2022", "2026-12-31")]:
        m = (SP.index >= a) & (SP.index <= b); r = ic(hsis[m], SP[f"sfwd{h}"][m], max(h, 5)); print(f"  spot HSI h={h} {a}-{b[:4]}: ic={r['ic']:+.3f} t={r['t']:+.2f}", end=" |")
    print()
# HSI ile S&P (ES, t-1 ABD kapanışı) ve Asya'da risk iştahı bileşkesi — HSI artığı spot gold 08:00 sonrası?
print("  corr(HSI_t, spot 07->15 aynı gün):", round(hsi.corr(s_715), 3), "corr(HSI, spot r1):", round(hsi.corr(s_r1), 3))

# ---------------- (B) VİOP OI5 × trend (bağımsız)
L = pd.read_parquet(f"{S}/panel/viop_long.parquet"); L["date"] = pd.to_datetime(L["date"]); L["expiry"] = pd.to_datetime(L["expiry"])
x = L[L.root == "XAUUSD"].copy()
# oi_chg doğrulama: kontrat içinde oi farkı
x = x.sort_values(["code", "date"]); x["oi_diff"] = x.groupby("code").oi.diff()
print("\noi_chg == oi farkı oranı:", round(((x.oi_chg - x.oi_diff).abs() < 1)[x.oi_diff.notna()].mean(), 3))
live = x[x.expiry > x.date]
g = live.groupby("date").agg(doi=("oi_chg", "sum"), oi=("oi", "sum")).reindex(D.index)
doi_rel = g.doi / (g.oi - g.doi).replace(0, np.nan)
for w in (3, 5, 10):
    for rw in (3, 5, 10):
        f = (doi_rel.rolling(w).sum() * np.sign(R.rolling(rw).sum())).shift(1)
        st = split_stats(f, D["fwd5"], 5)
        print(f"  OI{w}×sign(r{rw}) h5: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}", end=" ||")
    print()
oix = (doi_rel.rolling(5).sum() * np.sign(R.rolling(5).sum())).shift(1)
Ea = pd.read_csv(f"{S}/out/a6_akis_konum_cin/e_viop_features_t1.csv", index_col=0, parse_dates=True)["oi_d5_x_sgnret5"].reindex(D.index)
print("  analist özelliğiyle korelasyon:", round(oix.corr(Ea), 4))
full_report("OI5×sign(r5)", oix, 5, -1)
# r5 tek başına (kısa vadeli dönüş) ve OI'siz
r5l = R.rolling(5).sum().shift(1)
st = split_stats(r5l, D["fwd5"], 5); print(f"  VİOP r5 (t-1) tek başına h5: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}")
st = split_stats(np.sign(R.rolling(5).sum()).shift(1), D["fwd5"], 5); print(f"  sign(r5) tek başına h5: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}")
for h in (1, 3, 5, 10):
    st = split_stats(oix, D[f"fwd{h}"], h); print(f"  OI5×trend h={h}: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}")

# ---------------- (C) GPR z250 — yayın gecikmesi duyarlılığı
GR = pd.read_excel(f"{S}/data/misc/gpr_daily.xls"); GR["d"] = pd.to_datetime(GR["DAY"].astype(str), format="%Y%m%d"); GR = GR.set_index("d").sort_index()
def gpr_lag(days, lag):
    days = pd.DatetimeIndex(days); q = days - pd.Timedelta(days=lag)
    s = GR["GPRD"].astype(float).reindex(GR.index.union(q)).ffill().reindex(q); s.index = days; return s
def z250(s):
    l = np.log(s.clip(lower=1)); m = l.rolling(250, min_periods=200).mean(); sd = l.rolling(250, min_periods=200).std(); return (l - m) / sd
print()
for lag in (2, 4, 7, 10, 14, 21):
    gz = z250(gpr_lag(D.index, lag)); st = split_stats(gz, D["fwd5"], 5)
    pos = (-np.sign(gz)).fillna(0); b = sh_sub(pos, 5)
    print(f"GPR z250 lag={lag:2d}g h5: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f} | kural Sharpe IS={b['IS']} OOS={b['OOS']} dmOOS={sh_sub(pos,5,5,True)['OOS']}")
Ga = pd.read_csv(f"{S}/out/a6_akis_konum_cin/d_gpr_features.csv", index_col=0, parse_dates=True)["gpr_z250"].reindex(D.index)
gz2 = z250(gpr_lag(D.index, 2)); print("  analist özelliğiyle korelasyon:", round(gz2.corr(Ga), 4))
for w in (60, 120, 250, 500):
    l = np.log(gpr_lag(D.index, 2).clip(lower=1)); zz = (l - l.rolling(w, min_periods=int(w * .8)).mean()) / l.rolling(w, min_periods=int(w * .8)).std()
    st = split_stats(zz, D["fwd5"], 5); print(f"  GPR z{w} h5: t={st['t']:+.2f} IS={st['t_is']:+.2f} OOS={st['t_oos']:+.2f}")
full_report("GPR z250 (lag2)", Ga, 5, -1)
# spot erken
gzs = z250(gpr_lag(SP.index, 2))
for a, b in [("2010", "2013-12-31"), ("2014", "2016-12-31"), ("2010", "2016-12-31"), ("2017", "2026-12-31")]:
    m = (SP.index >= a) & (SP.index <= b); r = ic(gzs[m], SP["sfwd5"][m], 5); print(f"  spot GPR z250 h5 {a}-{b[:4]}: ic={r['ic']:+.3f} t={r['t']:+.2f}")
print("  GPR z250 > 0 gün oranı OOS:", round((Ga[D.index > IS_END] > 0).mean(), 3), " IS:", round((Ga[D.index <= IS_END] > 0).mean(), 3))

# ---------------- (D) Çin artık sum5 h1 (post-hoc)
F = pd.read_csv(f"{S}/out/a6_akis_konum_cin_adv/adv_cn_features.csv", index_col=0, parse_dates=True).reindex(D.index)
base = F["comp"]
print()
for k in (1, 2, 3, 5, 7, 10, 15):
    s = base.rolling(k, min_periods=max(1, int(k * 0.6))).sum()
    out = []
    for h in (1, 2, 3, 5):
        st = split_stats(s, D[f"fwd{h}"], h); out.append(f"h{h} t={st['t']:+.2f}/IS{st['t_is']:+.2f}/OOS{st['t_oos']:+.2f}")
    print(f"sum{k:2d}: " + " | ".join(out))
s5 = base.rolling(5, min_periods=3).sum()
full_report("comp sum5", s5, 1, 1)
FS = pd.read_csv(f"{S}/out/a6_akis_konum_cin_adv/adv_cn_features_spot.csv", index_col=0, parse_dates=True).reindex(SP.index)
s5s = FS["comp"].rolling(5, min_periods=3).sum()
for a, b in [("2010", "2016-12-31"), ("2017", "2021-12-31"), ("2022", "2026-12-31")]:
    m = (SP.index >= a) & (SP.index <= b); r = ic(s5s[m], SP["sfwd1"][m], 5); print(f"  spot sum5 h1 {a}-{b[:4]}: ic={r['ic']:+.3f} t={r['t']:+.2f}")
