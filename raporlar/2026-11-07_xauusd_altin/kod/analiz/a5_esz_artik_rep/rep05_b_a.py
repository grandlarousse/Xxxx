"""Adım 5: B1 (altın/gümüş 5g göreli dönüş), oran z-skorları, A ailesi (15→15 artık) ızgarası."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/spot_snaps.parquet"); D = D[D.index >= "2010-01-01"]
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
V = lambda s: s.reindex(va.index)
Y = {h: va[f"fwd{h}"] for h in (1, 3, 5)}
pd.set_option("display.width", 220)
# ---------- B1 ----------
lr = np.log(D.XAU_p15 / D.XAG_p15)
dlr = lr.diff()
print("en büyük |Δlog oran|:", dlr.abs().nlargest(5).round(3).to_dict())
sd = dlr.rolling(120, min_periods=96).std().shift(1)
for k in (1, 3, 5):
    z = dlr.rolling(k).sum() / (sd * np.sqrt(k))
    for h in (1, 3, 5):
        st = stats(V(z), Y[h], h)
        if (k, h) in [(5, 1), (3, 3), (5, 3), (5, 5)]:
            print(f"GSRD k{k} h{h}: ic {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} yıl {st['yrs']} n {st['n']}")
z5 = V(dlr.rolling(5).sum() / (sd * np.sqrt(5)))
st = stats(z5, Y[1], 1); print("B1 yıllık IC:", st["by_year"])
st = stats(z5, Y[1], 1, method="pearson"); print("B1 Pearson t:", round(st["t"], 2))
pos = -np.sign(z5).fillna(0)
r = bt_split(pos, va.ret, 1, 5.0)
for k, d in r.items(): print("  B1 sign", k, {a: round(b, 2) for a, b in d.items()})
# spot hedef ve atlamalı
z5s = dlr.rolling(5).sum() / (sd * np.sqrt(5))
sf1 = np.log(D.XAU_p15).diff().shift(-1); sk1 = np.log(D.XAU_p15.shift(-1) / D.XAU_p16)
for nm, yy in [("spot", sf1), ("skip1h", sk1)]:
    st = stats(z5s[z5s.index >= "2016-01-01"], yy, 1); print(f"  B1 {nm} 2016+: t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f}")
# OOS içinde B1 net getirinin bacak ayrımı ve buy&hold'a göre: 'uzun' oranı
print("  B1 OOS uzun gün oranı:", round((pos[pos.index > IS_END] > 0).mean(), 2))
# ---------- B oran z ----------
for L in (20, 60, 120):
    z = (lr - lr.rolling(L, min_periods=int(0.8 * L)).mean()) / lr.rolling(L, min_periods=int(0.8 * L)).std()
    out = []
    for h in (1, 3, 5):
        st = stats(V(z), Y[h], h); out.append(f"h{h}: t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} ({st['yrs']})")
    print(f"GSRZ L{L}:", " | ".join(out))
# ---------- A ailesi ----------
syms = dict(XAG="XAGUSD", DXY="DOLLARIDXUSD", TBOND="USTBONDTRUSD", SPX="USA500IDXUSD", USDJPY="USDJPY", USDCNH="USDCNH", BTC="BTCUSD",
            EURUSD="EURUSD", COPPER="COPPERCMDUSD")
X = {}
for k, s in syms.items():
    X[k] = np.log(snap(s, 15).reindex(D.index)).diff() if k not in D else None
X = pd.DataFrame({k: (np.log(D[f"{k}_p15"]).diff() if f"{k}_p15" in D else v) for k, v in X.items()})
print("A x kapsama:", X.notna().sum().to_dict())
print("A en büyük |x|:", X.abs().max().round(3).to_dict(), {k: str(v.date()) for k, v in X.abs().idxmax().items()})
g = np.log(D.XAU_p15).diff()
models = {"XAG": ["XAG"], "DXY": ["DXY"], "TBOND": ["TBOND"], "SPX": ["SPX"], "USDJPY": ["USDJPY"], "USDCNH": ["USDCNH"], "BTC": ["BTC"],
          "EURUSD": ["EURUSD"], "MACRO3": ["DXY", "TBOND", "SPX"], "FX3": ["EURUSD", "USDJPY", "USDCNH"], "ALL7": ["XAG", "DXY", "TBOND", "SPX", "USDJPY", "USDCNH", "COPPER"]}
rows = []; keep = {}
for m, cols in models.items():
    for W in (60, 120, 250):
        rr = rolling_ols(g, X[cols], W)
        for k in (1, 3, 5):
            z = rr.e.rolling(k, min_periods=k).sum() / (rr.sig * np.sqrt(k))
            keep[f"R_{m}_W{W}_k{k}"] = z
            for h in (1, 3, 5):
                st = stats(V(z), Y[h], h)
                rows.append(dict(test=f"A_{m}_W{W}_k{k}_h{h}", m=m, W=W, k=k, h=h, **{a: b for a, b in st.items() if a != "by_year"}))
A = pd.DataFrame(rows); A.to_csv(f"{OUT}/rep_agrid.csv", index=False)
print("A testleri:", len(A), " |t|>2:", int((A.t.abs() > 2).sum()), f"({(A.t.abs() > 2).mean():.1%})", " maks |t|:", round(A.t.abs().max(), 2),
      " IS->OOS aynı işaret:", round((np.sign(A.t_is) == np.sign(A.t_oos)).mean(), 2), " IC>0:", round((A.ic > 0).mean(), 2))
for h in (1, 3, 5):
    s = A[A.h == h].loc[lambda d: d.t_is.abs().idxmax()]; print(f"  IS seçimi h{h}: {s.test} t_is {s.t_is:.2f} -> OOS {s.t_oos:.2f}, full {s.t:.2f}")
print(A.reindex(A.t.abs().sort_values(ascending=False).index).head(8)[["test", "ic", "t", "t_is", "t_oos", "yrs"]].round(2).to_string())
s = A[A.test == "A_EURUSD_W60_k1_h1"].iloc[0]; print("A3 EURUSD W60 k1 h1:", round(s.ic, 3), round(s.t, 2), round(s.t_is, 2), round(s.t_oos, 2), s.yrs)
z = V(keep["R_EURUSD_W60_k1"]); r = bt_split(np.sign(z).fillna(0), va.ret, 1, 5.0)
print("  A3 sign OOS SR", round(r["oos"]["sr"], 2), "dm", round(r["oos"]["sr_dm"], 2), "IS", round(r["is"]["sr"], 2), "turn", round(r["full"]["turn"], 0))
can = A[(A.W == 120) & (A.k == 1)]; print("kanonik W120 k1 maks |t|:", round(can.t.abs().max(), 2))
