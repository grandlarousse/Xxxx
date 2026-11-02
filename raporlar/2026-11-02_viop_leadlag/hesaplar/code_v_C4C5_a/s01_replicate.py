"""Adim 1: iddialarin gunluk veriden bagimsiz yeniden uretimi (orijinal tanimlarla)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
pd.set_option("display.width", 220)
C = V.cal()
TR = V.bist_daily("TRALT.IS"); KR = V.bist_daily("KRDMD.IS")
def rep(stock, sig, lab, start=None):
    y = stock["intra"]
    df = pd.concat([y.rename("y"), sig.rename("s")], axis=1).dropna()
    if start: df = df[df.index >= start]
    c, t, n = V.zt(df.y, df.s)
    res, _ = V.bt(df.s, df.y, 10); res0, _ = V.bt(df.s, df.y, 0)
    print(f"{lab:38s} n={n:5d} corr={c:+.3f} t={t:+.2f} | BT10 IS sh={res['IS'].get('sharpe',np.nan):+.2f} OOS sh={res['OOS'].get('sharpe',np.nan):+.2f} "
          f"OOS net={res['OOS'].get('mean_bps',np.nan):+.1f} brut={res0['OOS'].get('mean_bps',np.nan):+.1f} bps (n_oos={res['OOS'].get('n')}) ALL net={res['ALL'].get('mean_bps',np.nan):+.1f}")
    return res
print("== (a) HK/SS -> TRALT gun-ici (orijinal tanim: surucu kapanis t, BIST acilis->kapanis t) ==")
for s in ["1787.HK", "600547.SS", "2899.HK", "601899.SS"]:
    r, fr = V.sig_close(s, C)
    st = "2018-10-01" if s == "1787.HK" else "2010-02-15"
    rep(TR, r, s + " D_t", st)
    rep(TR, r.shift(1), s + " D_{t-1} (bayat)", st)
print("== (b) SHFE HC -> KRDMD gun-ici ==")
for code in ["HC", "RB"]:
    m = V.shfe_main(code)
    lp = m["r_cc"].fillna(0).cumsum()  # seviye
    lv, fr = V.on_cal(lp, C); r = lv.diff()
    nanidx = m.index[m["r_cc"].isna()]; r[r.index.isin(nanidx)] = np.nan
    print(code, "baslangic", m.index[0].date(), "n", len(m))
    rep(KR, r, f"SHFE {code} D_t")
    rep(KR, r.shift(1), f"SHFE {code} D_t-1")
    for stck, nm in [(V.bist_daily("EREGL.IS"), "EREGL")]:
        rep(stck, r, f"  -> {nm} SHFE {code} D_t")
