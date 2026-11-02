"""GÖREV 2: Günlük öncülük.
A) endeks_{t-1} -> hisse_t (cc, gap, intra); KONTROL: hisse cc_{t-1}, XU100_{t-1}. Ham ve hisse-hariç (ex) endeks.
B) hisse_{t-1} -> endeks_t; KONTROL: endeks_{t-1}, XU100_{t-1}.
C) Sektörler/ulusal endeksler arası: I_j,{t-1} -> I_k,t; KONTROL: I_k,{t-1}, XU100_{t-1}.
Hepsi z-skorlu değişkenlerle (katsayı ~ kısmi korelasyon ölçeği), NW(5) t. Dönemler: full 2014-2026, IS <2021, OOS >=2021.
Null: endeks serisini dairesel kaydırarak (>=250 gün) aynı testler -> |t|>3 oranı.
"""
from ye_common import *
IDXS = [k for k in IDX_DESC if os.path.exists(f"{ISY}/d/{k}.parquet")]
m = idx_ret("XU100")
IR = {I: idx_ret(I) for I in IDXS}
PER = {"full": (START, END), "IS": (START, SPLIT - pd.Timedelta(days=1)), "OOS": (SPLIT, END)}
rng = np.random.default_rng(7)

CAL = cal(); CAL = CAL[(CAL >= START) & (CAL <= END)]
PM = {p: ((CAL >= a) & (CAL <= b)) for p, (a, b) in PER.items()}
def A_(x): return pd.Series(x).reindex(CAL).values.astype(float)
def reg(y, x, ctr, per):
    """y, x, ctr: numpy (CAL hizalı). z-skorlu OLS + NW."""
    M = np.column_stack([y, x] + list(ctr)); ok = PM[per] & np.isfinite(M).all(1); M = M[ok]
    if len(M) < 120: return np.nan, np.nan, len(M)
    M = (M - M.mean(0)) / M.std(0)
    bb, tt, n, _ = ols_nw(M[:, 0], M[:, 1:]); return bb[1], tt[1], n
rowsA = []; rowsB = []; nullA = []
mA = A_(m); mL = A_(m.shift(1)); IRA = {I: A_(IR[I]) for I in IDXS}; IRL = {I: A_(IR[I].shift(1)) for I in IDXS}
for s in VIOP:
    d = stk_dec(s); ccS = stk_ret(s)
    cc = A_(ccS); own = A_(ccS.shift(1)); TG = {"cc": cc, "gap": A_(d["gap"]), "intra": A_(d["intra"])}
    for I in IDXS:
        ri = IR[I]; ctrl = [own] if I == "XU100" else [own, mL]
        w = weight_series(I, s, ri.index)
        variants = [("raw", IRL[I])]
        if w.max() > 0.005: variants.append(("ex", A_(ex_ret(I, s, ri, ccS).shift(1))))
        for var, x in variants:
            for tgt in ["cc", "gap", "intra"]:
                y = TG[tgt]
                r = {"stock": s, "idx": I, "var": var, "target": tgt, "w": float(w.iloc[-1])}
                for per in PER:
                    b, t, n = reg(y, x, ctrl, per); r[f"b_{per}"] = b; r[f"t_{per}"] = t; r[f"n_{per}"] = n
                rowsA.append(r)
        # null (dairesel kaydırma): sadece raw, full, intra ve cc
        for k in range(3):
            sh = int(rng.integers(250, 2500))
            xs = np.roll(IRL[I], sh)
            for tgt in ["cc", "intra"]:
                b, t, n = reg(TG[tgt], xs, ctrl, "full"); nullA.append((s, I, tgt, k, b, t))
        # B: hisse -> endeks
        ctrlB = [IRL[I]] if I == "XU100" else [IRL[I], mL]
        r = {"stock": s, "idx": I}
        for per in PER:
            b, t, n = reg(IRA[I], own, ctrlB, per); r[f"b_{per}"] = b; r[f"t_{per}"] = t; r[f"n_{per}"] = n
        rowsB.append(r)
    print(s, flush=True)
A = pd.DataFrame(rowsA); A.to_csv(RES + "/lead_idx_to_stock.csv", index=False)
B = pd.DataFrame(rowsB); B.to_csv(RES + "/lead_stock_to_idx.csv", index=False)
N = pd.DataFrame(nullA, columns=["stock", "idx", "target", "k", "b", "t"]); N.to_csv(RES + "/lead_null.csv", index=False)

# C: endeksler arası
rowsC = []
for j in IDXS:
    for k in IDXS:
        if j == k: continue
        ctrl = [IRL[k]] if "XU100" in (j, k) else [IRL[k], mL]
        r = {"leader": j, "follower": k}
        for per in PER:
            b, t, n = reg(IRA[k], IRL[j], ctrl, per); r[f"b_{per}"] = b; r[f"t_{per}"] = t; r[f"n_{per}"] = n
        rowsC.append(r)
C = pd.DataFrame(rowsC); C.to_csv(RES + "/lead_idx_to_idx.csv", index=False)
print("done", len(A), len(B), len(C))
