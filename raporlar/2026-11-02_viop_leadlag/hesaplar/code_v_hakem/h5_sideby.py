"""H5: Sektör ajanlarının BİREBİR tanımları ile tarama tanımı aynı (benim) veri üzerinde yan yana.
Backtest anlamı ll.backtest ile aynı (kendi kodum): pos=sign(sinyal) (|.|>thr) veya z-modu (geçmiş 250g, min 60, look-ahead yok) |z|>thr;
pnl = pos*y - maliyet*|pos|; istatistikler pozisyon günlerinde; Sharpe = (ort*252*aktif_oran)/(std_tüm_günler*sqrt252)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
cal = vh.bist_cal()
txt = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); txt.append(s)
_W = {}
def W(sym):
    """BIST günü penceresine atanmış emsal/endeks getirisi."""
    if sym not in _W: _W[sym] = vh.to_bist_window(vh.foreign_ret(sym), vh.bucket(sym))
    return _W[sym]
def basket(syms, minp=2):
    X = pd.concat([W(s) for s in syms], axis=1); return X.mean(axis=1).where(X.notna().sum(axis=1) >= minp)
def zs(x, w=250):
    mu = x.rolling(w, min_periods=60).mean().shift(1); sd = x.rolling(w, min_periods=60).std().shift(1); return (x - mu) / sd
def rresid(y, x):
    return y - vh.roll_beta(y, x) * x
D = {s: vh.bist_decomp(s) for s in ["TUPRS", "THYAO", "PGSUS", "TAVHL", "EREGL", "KRDMD", "XU100", "XU030"]}
xi = D["XU100"]["intra"]
def hedgeb(y):
    return y - vh.roll_beta(y, xi) * xi
def bt(sig, y, cost, mode="sign", thr=0.0):
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna(); df = df[(df.index >= vh.START) & (df.index <= vh.END)]
    if mode == "z":
        z = zs(df["s"]); pos = np.sign(z).where(z.abs() > thr, 0.0)
    else:
        pos = np.sign(df["s"]).where(df["s"].abs() > thr, 0.0)
    pos = pos.fillna(0.0); pnl = pos * df["y"] - cost / 1e4 * pos.abs()
    out = {}
    for per in ["IS", "OOS"]:
        m = vh.period_mask(df.index, per); st = vh.bt_stats(pnl[m], (pos[m] != 0))
        out.update({f"{per}_n": st.get("n"), f"{per}_bps": st.get("mean_bps"), f"{per}_t": st.get("t"), f"{per}_sh": st.get("sharpe")})
    return out
def ct(sig, y):
    """tarama: corr + HC t; enerji ajanı: iid t = r*sqrt(n-2)/sqrt(1-r^2)."""
    out = {}
    for per in ["ALL", "IS", "OOS"]:
        m = vh.period_mask(cal, per)
        c, t, n = vh.corr_hc(y.reindex(cal).values[m].astype(float), sig.reindex(cal).values[m].astype(float))
        out[f"{per}_c"] = c; out[f"{per}_tHC"] = t
        if per == "ALL": out["ALL_tiid"] = c * np.sqrt(n - 2) / np.sqrt(1 - c * c); out["n"] = n
    return out
rows = []
def add(claim, label, sig, y, extra=None):
    r = {"iddia": claim, "tanım": label, **ct(sig, y)}
    if extra: r.update(extra)
    rows.append(r)

# ===== ENERJİ: ABD rafinerileri -> TUPRS =====
tu = D["TUPRS"]["intra"]; tuh_b1 = tu - xi; tuh = hedgeb(tu)
US_REF = ["VLO", "MPC", "PSX", "PBF"]
add("E", "tarama: VLO_t-1 -> TUPRS ham gün-içi", W("VLO"), tu)
add("E", "enerji H1: VLO_t-1 -> TUPRS−XU100 gün-içi (β=1)", W("VLO"), tuh_b1)
add("E", "VLO_t-1 -> TUPRS β-hedge'li", W("VLO"), tuh)
usref = basket(US_REF)
add("E", "US_REF ham sepet -> TUPRS ham gün-içi", usref, tu, {**{"BT_sign_c8_" + k: v for k, v in bt(usref, tu, 8).items()}})
add("E", "US_REF ham sepet -> TUPRS−XU100 (β=1) [enerji BT1h]", usref, tuh_b1, {**{"BT_sign_c16_" + k: v for k, v in bt(usref, tuh_b1, 16).items()},
     **{"BT_z1_c0_" + k: v for k, v in bt(usref, tuh_b1, 0, "z", 1.0).items()}, **{"BT_z1_c16_" + k: v for k, v in bt(usref, tuh_b1, 16, "z", 1.0).items()}})
usref_x = rresid(usref, W("^GSPC"))
add("E", "US_REF − β·SPX -> TUPRS β-hedge'li", usref_x, tuh, {**{"BT_z1_c0_" + k: v for k, v in bt(usref_x, tuh, 0, "z", 1.0).items()}, **{"BT_z1_c16_" + k: v for k, v in bt(usref_x, tuh, 16, "z", 1.0).items()}})
add("E", "SPX_t-1 (piyasa) -> TUPRS β-hedge'li", W("^GSPC"), tuh)
add("E", "SPX_t-1 (piyasa) -> TUPRS ham gün-içi", W("^GSPC"), tu)

# ===== HAVACILIK =====
EU_AIR = ["LHA.DE", "AF.PA", "IAG.L", "RYA.IR", "EZJ.L", "WIZZ.L", "JET2.L"]; US_AIR = ["DAL", "UAL", "AAL", "LUV", "ALK", "JBLU"]
eu = basket(EU_AIR); us = basket(US_AIR)
eux = rresid(eu, W("^STOXX")); usx = rresid(us, W("^GSPC"))
air = zs(eux).clip(-3, 3) + zs(usx).clip(-3, 3)
tur = W("TUR"); combo = air - zs(tur).clip(-3, 3)
for st in ["THYAO", "PGSUS", "TAVHL", "XU100", "XU030"]:
    y = D[st]["intra"]; yh = hedgeb(y) if st not in ("XU100", "XU030") else y
    add("H", f"tarama: LHA.DE_t-1 -> {st} ham", W("LHA.DE"), y)
    add("H", f"havacılık AIR_only (z(EU−βSTOXX)+z(US−βSPX), |.|>1) -> {st} ham, 8bps", air, y, {**{"BT_c8_" + k: v for k, v in bt(air, y, 8, "sign", 1.0).items()},
        **{"BT_c15_" + k: v for k, v in bt(air, y, 15, "sign", 1.0).items()}})
    if st not in ("XU100", "XU030"):
        add("H", f"AIR_only -> {st} β-hedge'li (2 bacak 16bps)", air, yh, {**{"BT_c0_" + k: v for k, v in bt(air, yh, 0, "sign", 1.0).items()},
            **{"BT_c16_" + k: v for k, v in bt(air, yh, 16, "sign", 1.0).items()}})
        add("H", f"COMBO (AIR − z(TUR)) -> {st} ham, 8bps [TUR sonradan eklendi]", combo, y, {**{"BT_c8_" + k: v for k, v in bt(combo, y, 8, "sign", 1.0).items()}})
        add("H", f"ham AB+ABD sepeti (artıksız) -> {st} ham", (eu + us) / 2, y, {**{"BT_c8_" + k: v for k, v in bt((eu + us) / 2, y, 8, "z", 1.0).items()}})

# ===== METAL =====
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
compz = pd.concat([zs(W(s)) for s in JP_AU], axis=1).mean(axis=1)
comp_res = pd.concat([zs(rresid(W(s), W(vh.region_index(s)))) for s in JP_AU], axis=1).mean(axis=1)
asia_mkt = pd.concat([zs(W("^N225")), zs(W("^AXJO"))], axis=1).mean(axis=1)
for st in ["EREGL", "KRDMD", "XU100"]:
    y = D[st]["intra"]; yh = hedgeb(y) if st != "XU100" else y
    add("M", f"tarama/metal: FMG.AX_t (lag0) -> {st} ham", W("FMG.AX"), y, {**{"BT_z1_c15_" + k: v for k, v in bt(W("FMG.AX"), y, 15, "z", 1.0).items()}})
    add("M", f"metal JP/AU ham z-kompozit -> {st} ham, z>1, 15bps", compz, y, {**{"BT_z1_c15_" + k: v for k, v in bt(compz, y, 15, "z", 1.0).items()}, **{"BT_z1_c0_" + k: v for k, v in bt(compz, y, 0, "z", 1.0).items()}})
    add("M", f"JP/AU kompozit ARTIK (her bileşen − β·kendi endeksi) -> {st} ham", comp_res, y, {**{"BT_z1_c15_" + k: v for k, v in bt(comp_res, y, 15, "z", 1.0).items()}})
    add("M", f"Asya PİYASA (N225+AXJO z) -> {st} ham", asia_mkt, y, {**{"BT_z1_c15_" + k: v for k, v in bt(asia_mkt, y, 15, "z", 1.0).items()}})
    if st != "XU100":
        add("M", f"JP/AU kompozit ARTIK -> {st} β-hedge'li (2 bacak 30)", comp_res, yh, {**{"BT_z1_c0_" + k: v for k, v in bt(comp_res, yh, 0, "z", 1.0).items()}, **{"BT_z1_c30_" + k: v for k, v in bt(comp_res, yh, 30, "z", 1.0).items()}})
        add("M", f"metal JP/AU ham kompozit -> {st} β-hedge'li", compz, yh)
R = pd.DataFrame(rows); R.to_csv(vh.RES + "/h5_sideby.csv", index=False)
pd.set_option("display.width", 250)
for cl in ["E", "H", "M"]:
    q = R[R.iddia == cl]
    P(f"\n===== {cl} =====")
    P(q[["tanım", "n", "ALL_c", "ALL_tHC", "ALL_tiid", "IS_c", "IS_tHC", "OOS_c", "OOS_tHC"]].round(3).to_string(index=False))
    bcols = [c for c in q.columns if c.startswith("BT_") and q[c].notna().any() and (c.endswith("_bps") or c.endswith("_t") or c.endswith("_sh"))]
    if bcols:
        for _, r in q.iterrows():
            vals = {c: r[c] for c in bcols if pd.notna(r[c])}
            if vals: P("  BT", r["tanım"], "|", "; ".join(f"{k.replace('BT_','')}={v:.2f}" for k, v in vals.items()))
open(vh.RES + "/h5_summary.txt", "w").write("\n".join(txt))
