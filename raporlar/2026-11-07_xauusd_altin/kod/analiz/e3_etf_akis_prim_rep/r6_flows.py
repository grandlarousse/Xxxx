"""E3-6: GLD pay akışları -> GLD getirisi (bağımsız)."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)
days = nyse_days("2008-01-01")
nh = pd.read_parquet(f"{P}/etf_gld_navhist.parquet"); nh.index = pd.to_datetime(nh.index).normalize()
nh = nh[~nh.index.duplicated(keep="last")].sort_index()
# --- tarih etiketi kontrolü: NAV(D) LBMA PM (15:00 Londra) spotu ile mi hizalı?
xs = xau_hourly()
lon = pd.DatetimeIndex([pd.Timestamp(f"{d.date()} 15:00", tz="Europe/London").tz_convert("UTC") for d in nh.index])
sp, _ = snap(xs, lon); sp.index = nh.index
dn = np.log(nh.nav).diff(); dsp = np.log(sp).diff()
print("corr(ΔlnNAV_D, Δln spot_LBMA): D-1/D/D+1:", [round(dn.corr(dsp.shift(k)), 3) for k in (1, 0, -1)])
# --- özellikler (SSGA günü D)
S_ = np.log(nh.shares.where(nh.shares > 0))
F = pd.DataFrame({"f1": S_.diff(), "f5": S_.diff(5), "f20": S_.diff(20)})
for k in ["f1", "f5", "f20"]:
    F["z" + k] = F[k] / F[k].rolling(250, min_periods=120).std().shift(1)
def align(F, idx, lag):
    """ETF günü t için SSGA günü D < t olan son değer (lag1); bir önceki (lag2)."""
    pos = F.index.searchsorted(idx, side="left") - 1 - (lag - 1)
    v = np.where(pos[:, None] >= 0, F.values[np.clip(pos, 0, None)], np.nan)
    return pd.DataFrame(v, index=idx, columns=F.columns)
rG = np.log(yh("GLD").reindex(days)).diff(); rI = np.log(yh("IAU").reindex(days)).diff()
rows = []
for lag in (1, 2):
    A = align(F, days, lag)
    for k in ["f1", "f5", "f20", "zf1", "zf5", "zf20"]:
        for h in (1, 3, 5, 10):
            st = stats(A[k], fwd(rG, h), h); st.update(pred=k, lag=lag, h=h, tgt="GLD"); rows.append(st)
    for k in ["zf1", "zf5", "zf20"]:
        for h in (1, 5):
            st = stats(A[k], fwd(rI, h), h); st.update(pred=k, lag=lag, h=h, tgt="IAU"); rows.append(st)
res = pd.DataFrame(rows)[["tgt", "pred", "lag", "h", "n", "ic", "t", "ic_is", "t_is", "ic_oos", "t_oos", "t_22", "yrs"]]
res.to_csv(f"{OUT}/r6_flows.csv", index=False)
print(res[res.tgt == "GLD"].to_string())
g = res[res.tgt == "GLD"]
both = g[(g.t_is.abs() > 1.96) & (g.t_oos.abs() > 1.96) & (np.sign(g.t_is) == np.sign(g.t_oos))]
print("GLD testleri:", len(g), "| IS ve OOS'ta aynı işaretle |t|>1.96:", len(both))
print("|t_oos|>1.96 olanlar:", g[g.t_oos.abs() > 1.96][["pred", "lag", "h", "t_is", "t_oos"]].to_dict("records"))
# --- IS seçimi: GLD hedefli testlerde en büyük |t_IS|
pk = g.loc[g.t_is.abs().idxmax()]; print("IS seçimi:", pk.to_dict())
k = pk.pred; lag = int(pk.lag); h = min(int(pk.h), 5); sg = np.sign(pk.t_is)
A = align(F, days, lag)
z = A[k] if k.startswith("z") else A[k] / A[k].rolling(250, min_periods=120).std().shift(1)
pos = (sg * np.sign(z)).fillna(0)
R = np.expm1(rG).dropna(); Ri = np.expm1(np.log(yh("GLL").reindex(days)).diff())
net, wl, _ = run_bt(pos, R, h, 10)
dm, _, _ = run_bt(pos, R - R.mean(), h, 10)
Rr = R[R.index >= Ri.first_valid_index()]
neti, _, _ = run_bt(pos, Rr, h, 10, inv=dict(R=Ri, L=pd.Series(2.0, index=Rr.index), cost=20))
print(f"strateji ({k} lag{lag} h{h}, işaret {sg:+.0f}×z): yalnız uzun", seg_sh(net), "| demeaned", seg_sh(dm), "| ters GLL'li", seg_sh(neti), "| B&H", seg_sh(R), "| maruziyet", round(wl.mean(), 3))
# --- ters yön: f1_D ~ r_D, r_{D-1}, r_{D-5..D-2} (SSGA günü bazında; tek değişkenli Spearman IC t)
rr = np.log(yh("GLD")).diff().reindex(F.index)
X = pd.DataFrame({"r0": rr, "r1": rr.shift(1), "r2_5": rr.shift(2).rolling(4).sum(), "r6_20": rr.shift(6).rolling(15).sum(), "f1_l1": F.f1.shift(1)})
for c in ["r0", "r1", "r2_5"]:
    print("ters yön IC", c, ic(X[c][X.index >= "2008-01-01"], F.f1[F.index >= "2008-01-01"], 5), "| 2005+:", ic(X[c][X.index >= "2005-01-01"], F.f1[F.index >= "2005-01-01"], 5))
dd = pd.concat([F.f1.rename("y"), X], axis=1).dropna(); dd = dd[dd.index >= "2005-01-01"]
Z = (dd - dd.mean()) / dd.std()
import statsmodels.api as sm
m = sm.OLS(Z.y, sm.add_constant(Z[["r0", "r1", "r2_5", "r6_20", "f1_l1"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
print("çok değişkenli t:", m.tvalues.round(2).to_dict())
