"""v8: (a) kesit sırası IS ve OOS ayrı; (b) volatilite rejimi (ex-ante 60g gün-içi vol tercile) — etki kriz dönemine mi yığılı?"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
A = pd.read_csv(RES + "/v2a_crosssection.csv")
for p in ["IS", "OOS"]:
    A[f"rk_{p}"] = A[f"{p}_gross"].rank(ascending=False)
    n = A[f"{p}_gross"].notna().sum()
    print(p, "brüt sırası (n=%d):" % n, A[A.sym.isin(["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS"])][["sym", f"rk_{p}", f"{p}_gross", f"{p}_t"]].round(1).to_string(index=False))
    v = A[A.viop]; v = v.assign(r=v[f"{p}_gross"].rank(ascending=False))
    print("   VİOP-47 içinde:", v[v.sym.isin(["THYAO.IS", "PGSUS.IS", "TAVHL.IS"])][["sym", "r"]].values.tolist())
SG = pd.read_parquet(RES + "/signals.parquet"); AIR = SG.AIR_C
print("\n== Volatilite rejimi: ex-ante 60g gün-içi vol tercile'leri (tüm 2014-26) ==")
for st in ["THYAO", "PGSUS", "TAVHL"]:
    d = bist_day(st + ".IS"); y = d.intra
    vol = y.rolling(60, min_periods=40).std().shift(1)
    df = pd.concat([AIR.rename("s"), y.rename("y"), vol.rename("v")], axis=1).dropna(); df = df[df.s.abs() > 1]
    df["g"] = np.sign(df.s) * df.y
    df["q"] = pd.qcut(df.v, 3, labels=["düşük", "orta", "yüksek"])
    out = df.groupby("q").apply(lambda x: pd.Series({"n": len(x), "brüt_bps": 1e4 * x.g.mean(), "t": x.g.mean() / x.g.std() * np.sqrt(len(x)), "vol_bps": 1e4 * x.v.mean(), "net8": 1e4 * (x.g.mean() - 8e-4)}))
    # vol-normalize edilmiş getiri: g/v
    df["gn"] = df.g / df.v
    print(st); print(out.round(2).to_string())
    print(f"   vol-ölçekli (g/vol) ort {df.gn.mean():.3f} t {df.gn.mean()/df.gn.std()*np.sqrt(len(df)):.2f}; düşük-vol tercile'de vol-ölçekli t {df[df.q=='düşük'].gn.mean()/df[df.q=='düşük'].gn.std()*np.sqrt((df.q=='düşük').sum()):.2f}")
