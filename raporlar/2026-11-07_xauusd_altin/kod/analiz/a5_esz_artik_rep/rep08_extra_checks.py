"""Ek kontroller: C4 eşik duyarlılığı ve spot hedef; C1 sabit-IS-beta sürümü; A erken dönem; B1 vekili 2010 başı alt dönemi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
D = pd.read_parquet(f"{OUT}/spot_snaps.parquet"); D = D[D.index >= "2010-01-01"]
va = pd.read_parquet(f"{OUT}/viop_rep.parquet"); V = lambda s: s.reindex(va.index); Y = {h: va[f"fwd{h}"] for h in (1, 3, 5)}
# ---- C4 ----
g07 = np.log(D.XAU_p15 / D.XAU_p07)
X07 = pd.DataFrame({k: np.log(D[f"{k}_p15"] / D[f"{k}_p07"]) for k in ("DXY", "TBOND", "SPX")})
rr = rolling_ols(g07, X07, 60); e07s = rr.e / rr.sig; e07 = V(e07s)
print("C4 eşik duyarlılığı (h1, 5 bps):")
for th in (0, 0.5, 1.0, 1.5, 2.0):
    pos = np.sign(e07).where(e07.abs() > th, 0).fillna(0); r = bt_split(pos, va.ret, 1, 5.0)
    print(f"  |e|>{th}: SR IS {r['is']['sr']:.2f} OOS {r['oos']['sr']:.2f} (dm {r['oos']['sr_dm']:.2f}) maruziyet OOS {r['oos']['expo']:.2f} P&L t OOS {r['oos']['t_pnl']:.2f}")
pc = sp.reindex(D.index)
for nm, yy in [("spot", np.log(sp.xau_p15).diff().shift(-1)), ("skip1h", np.log(sp.xau_p15.shift(-1) / sp.xau_p16))]:
    st = stats(e07s.reindex(sp.index), yy, 1); print(f"  C4 {nm}: t {st['t']:.2f} OOS {st['t_oos']:.2f}")
# ---- C1 sabit (IS) beta sürümü: beta yalnız 2019-05..2021-12'den tek sefer; OOS'ta sabit ----
c1 = pd.read_parquet(f"{OUT}/c1_signal_rep.parquet")
g12 = np.log(D.XAU_p15 / D.XAU_p12); X12 = pd.DataFrame({k: np.log(D[f"{k}_p15"] / D[f"{k}_p12"]) for k in ("DXY", "TBOND", "SPX")})
ok = g12.notna() & X12.notna().all(1)
F = c1.f12.reindex(va.index); thr = F.abs()[F.index <= IS_END].dropna().quantile(0.8)
cond = V(c1.f12.abs() > thr)
# basit: koşul aynı; artık işareti yerine ham g12 - (IS sabit beta) x12
isd = ok & (g12.index <= IS_END) & (g12.index >= "2018-03-01")
A = np.column_stack([np.ones(isd.sum()), X12[isd].values]); b = np.linalg.lstsq(A, g12[isd].values, rcond=None)[0]
efix = g12 - b[0] - X12 @ b[1:]
st = stats(V(efix).where(cond), Y[3], 3); print(f"\nC1 IS-sabit beta artığı (koşul aynı) h3: t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f}  beta {np.round(b[1:], 3)}")
# ---- A erken dönem 2016-01..2017-03 (spot skip hedef) ----
g = np.log(sp.xau_p15).diff(); sk1 = np.log(sp.xau_p15.shift(-1) / sp.xau_p16)
pre = (sp.index >= "2016-01-01") & (sp.index < "2017-03-06")
for m, s, k in [("EURUSD", "EURUSD", 1), ("USDJPY", "USDJPY", 3)]:
    x = np.log(sp[f"dk_{s}_p15"]).diff(); r_ = rolling_ols(g, x.to_frame(), 60)
    z = r_.e.rolling(k, min_periods=k).sum() / (r_.sig * np.sqrt(k))
    st = ic_t(z[pre], sk1[pre], 5); print(f"A {m} W60 k{k} 2016-01..2017-03 skip hedef: ic {st['ic']:.3f} t {st['t']:.2f} n {st['n']}")
# ---- B1 Yahoo vekili: 2010 Oca-May alt dönemi tek başına ----
gc = pd.read_parquet(f"{P}/yahoo/GC_F.parquet"); si = pd.read_parquet(f"{P}/yahoo/SI_F.parquet")
y = pd.concat([gc.close.rename("gc"), si.close.rename("si")], axis=1).dropna(); y.index = pd.to_datetime(y.index)
dr = np.log(y.gc / y.si).diff(); sdr = dr.rolling(120, min_periods=96).std().shift(1)
zz = dr.rolling(5).sum() / (sdr * np.sqrt(5))
idx = zz.index.searchsorted(sp.index, side="left") - 1; zs = pd.Series(zz.values[idx], index=sp.index)
for a, b_ in [("2010-01-01", "2010-06-01"), ("2010-06-01", "2017-03-06"), ("2010-01-01", "2017-03-06")]:
    m_ = (sp.index >= a) & (sp.index < b_)
    out = [f"h{h} t {ic_t(zs[m_], sp[f'sfwd{h}'][m_], max(h, 5))['t']:.2f}" for h in (1, 3, 5)]
    print(f"B1 vekili GSY k5 {a}..{b_}:", " | ".join(out))

# ---- B1 vekili, daha uzun erken dönem: Dukascopy XAU 15:00 hedefi 2008+ (benim takvim), Yahoo GC/SI t-1 ----
Dall = pd.read_parquet(f"{OUT}/spot_snaps.parquet")
lpa = np.log(Dall.XAU_p15)
idx = zz.index.searchsorted(Dall.index, side="left") - 1; zsa = pd.Series(zz.values[idx], index=Dall.index)
print("XAU 15:00 doluluk yıl başına:", Dall.XAU_p15.notna().groupby(Dall.index.year).sum().loc[2008:2011].to_dict())
for a, b_ in [("2008-06-01", "2010-01-01"), ("2008-06-01", "2017-03-06"), ("2017-03-06", "2026-11-07")]:
    m_ = (Dall.index >= a) & (Dall.index < b_)
    out = []
    for h in (1, 3, 5):
        yy = sum(lpa.diff().shift(-k) for k in range(1, h + 1)); st = ic_t(zsa[m_], yy[m_], max(h, 5)); out.append(f"h{h} ic {st['ic']:.3f} t {st['t']:.2f} n {st['n']}")
    print(f"B1 vekili GSY k5 spot {a}..{b_}:", " | ".join(out))
# Dukascopy XAG 15:00 sürümü (B1'in kendisi) spot hedef 2016+ yıllık IC
