"""Adım 4: C ailesi (gün içi) ızgarası, IS seçimi, C4 ve yetişme (gap = -artık) iddiaları; C1 için dairesel kaydırma null dağılımı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/spot_snaps.parquet"); D = D[D.index >= "2010-01-01"]
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
V = lambda s: s.reindex(va.index)
Y = {h: va[f"fwd{h}"] for h in (1, 3, 5)}
g12 = np.log(D.XAU_p15 / D.XAU_p12); g07 = np.log(D.XAU_p15 / D.XAU_p07)
X12 = pd.DataFrame({k: np.log(D[f"{k}_p15"] / D[f"{k}_p12"]) for k in ("DXY", "TBOND", "SPX")})
X07 = pd.DataFrame({k: np.log(D[f"{k}_p15"] / D[f"{k}_p07"]) for k in ("DXY", "TBOND", "SPX")})
mods = {"DXY": ["DXY"], "TBOND": ["TBOND"], "SPX": ["SPX"], "MACRO3": ["DXY", "TBOND", "SPX"]}
rows = []; SIG = {}
for win, gg, XX in [("I12", g12, X12), ("I07", g07, X07)]:
    for m, cols in mods.items():
        if win == "I07" and m != "MACRO3": continue
        for W in (60, 120, 250):
            rr = rolling_ols(gg, XX[cols], W)
            e = V(rr.e / rr.sig); f = V(rr.fit / rr.sig)
            SIG[f"{win}_{m}_W{W}"] = e; SIG[f"{win}F_{m}_W{W}"] = f
            for h in (1, 3, 5):
                st = stats(e, Y[h], h); rows.append(dict(test=f"C_{win}_{m}_W{W}_h{h}", kind="resid_uncond", h=h, **{k: v for k, v in st.items() if k != "by_year"}))
            if win == "I12" and m == "MACRO3":
                thr = f.abs()[f.index <= IS_END].dropna().quantile(0.8)
                for h in (1, 3, 5):
                    st = stats(e.where(f.abs() > thr), Y[h], h); rows.append(dict(test=f"C_I12c_MACRO3_W{W}_h{h}", kind="resid_cond", h=h, **{k: v for k, v in st.items() if k != "by_year"}))
                    st = stats(f, Y[h], h); rows.append(dict(test=f"C_I12F_MACRO3_W{W}_h{h}", kind="fitted", h=h, **{k: v for k, v in st.items() if k != "by_year"}))
G = pd.DataFrame(rows)
G.to_csv(f"{OUT}/rep_cgrid.csv", index=False)
pd.set_option("display.width", 220)
print(G[["test", "kind", "ic", "t", "t_is", "t_oos", "yrs", "n"]].round(3).to_string())
u = G[G.kind == "resid_uncond"]
print("koşulsuz artık testleri:", len(u), " IC>0:", int((u.ic > 0).sum()), " |t|>2:", int((u.t.abs() > 2).sum()))
cc = G[G.kind != "fitted"]
print("IS seçimi (artık testleri; koşulsuz+koşullu) her h için |t_is| maks:")
for h in (1, 3, 5):
    s = cc[cc.h == h].loc[lambda d: d.t_is.abs().idxmax()]; print("  h", h, s.test, round(s.t_is, 2), "->", round(s.t_oos, 2))
    s = G[G.h == h].loc[lambda d: d.t_is.abs().idxmax()]; print("    (fitted dahil)", s.test, round(s.t_is, 2), "->", round(s.t_oos, 2))
sm = G[G.kind != "fitted"]; print("C artık IS->OOS aynı işaret oranı:", round((np.sign(sm.t_is) == np.sign(sm.t_oos)).mean(), 2), " IC>0 oranı:", round((sm.ic > 0).mean(), 2))

# ---- C4: I07 MACRO3 W60, |e|>1, h1 ----
e07 = SIG["I07_MACRO3_W60"]
st = stats(e07, Y[1], 1); print(f"\nC4 IC h1: ic {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} yıl {st['yrs']} n {st['n']}")
pos = np.sign(e07).where(e07.abs() > 1, 0).fillna(0)
r = bt_split(pos, va.ret, 1, 5.0)
for k, d in r.items(): print("  C4 thr1", k, {a: round(b, 2) for a, b in d.items()})
print("  C4 sinyal günü/yıl:", round(pos.ne(0).sum() / ((va.index[-1] - e07.dropna().index[0]).days / 365.25), 1))
pos_s = np.sign(e07).fillna(0); r = bt_split(pos_s, va.ret, 1, 5.0); print("  C4 sign OOS SR", round(r["oos"]["sr"], 2))
# spot ve atlamalı hedef C4
e07s = None
# ---- Yetişme: gap = -artık; 12-15 MACRO3 W60 h1 ----
e12 = SIG["I12_MACRO3_W60"]
st = stats(-e12, Y[1], 1); print(f"\nYetişme gap (=-e12) h1: ic {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} yıl(gap yönünde aynı işaret) {st['yrs']}")
gp = np.sign(-e12).fillna(0)
r = bt_split(gp, va.ret, 1, 5.0); print("  gap sign kuralı (yetişme yönü) OOS SR net", round(r["oos"]["sr"], 2), "dm", round(r["oos"]["sr_dm"], 2), " IS", round(r["is"]["sr"], 2))
r0 = bt_split(gp, va.ret, 1, 0.0); print("  gap sign kuralı brüt OOS SR", round(r0["oos"]["sr"], 2))
r = bt_split(np.sign(e12).fillna(0), va.ret, 1, 5.0); print("  sürme sign kuralı (C3 sign) OOS SR net", round(r["oos"]["sr"], 2), " turn", round(r["oos"]["turn"], 0))

# ---- C1 için dairesel kaydırma null (otokorelasyonu koruyan) ----
thr = SIG["I12F_MACRO3_W60"].abs()[SIG["I12F_MACRO3_W60"].index <= IS_END].dropna().quantile(0.8)
x = e12.where(SIG["I12F_MACRO3_W60"].abs() > thr)
y = Y[3]
d = pd.concat([x.rename("x"), y.rename("y")], axis=1)
obs = d.dropna().corr(method="spearman").iloc[0, 1]
rng = np.random.default_rng(0); N = len(d); nul = []
yv = d.y.values
for s in rng.integers(30, N - 30, 2000):
    dd = pd.DataFrame(dict(x=d.x.values, y=np.roll(yv, s))).dropna()
    nul.append(dd.x.corr(dd.y, method="spearman"))
nul = np.array(nul)
print(f"\nC1 h3 dairesel kaydırma null: gözlenen IC {obs:.3f}, null sd {nul.std():.3f}, z {obs/nul.std():.2f}, p(|null|>=|obs|) {np.mean(np.abs(nul) >= abs(obs)):.4f}")
# işaret isabeti
tr = (np.sign(x) * y).dropna()
print("C1 isabet oranı:", round((tr > 0).mean(), 3), "n", len(tr))
