"""s01: iddia (a) ve (b)'nin bağımsız yeniden üretimi (kendi hizalamam)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
tr = bist_dec("TRALT.IS"); kr = bist_dec("KRDMD.IS")
print("TRALT intra n", tr.intra.notna().sum(), "first", tr.intra.dropna().index[0].date())
for sym in ["1787.HK", "2899.HK", "600547.SS", "601899.SS"]:
    for fld in ["adj", "c"]:
        for mode in ["zero", "nan"]:
            Dt = to_bist(loc_ret(sym, fld), mode)
            b, t, n = nw_t(tr.intra, Dt)
            r, _, _ = bt(Dt, tr.intra, 10)
            print(f"{sym:10s} {fld:3s} {mode:4s} r={b:.3f} t={t:.2f} n={n} | {fmt(r)}")
print("--- SHFE HC/RB roll (benim) -> KRDMD intra")
for prod in ["HC", "RB"]:
    R = sina_roll(prod)
    print(prod, "roll gün", len(R), R.index[0].date(), R.index[-1].date(), "kontrat sayısı", R.ctr.nunique())
    for col in ["cc", "gapD", "ocD"]:
        for mode in ["zero", "nan"]:
            Dt = to_bist(R[col], mode)
            b, t, n = nw_t(kr.intra, Dt)
            r, _, _ = bt(Dt, kr.intra, 10)
            print(f"  {prod} {col:4s} {mode:4s} r={b:.3f} t={t:.2f} n={n} | {fmt(r)}")
