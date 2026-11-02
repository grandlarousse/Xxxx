"""v1: İddia A4'ün bağımsız yeniden üretimi (varyant A = kaynak hizalama mantığı, kendi kodu) + varyant B (zaman damgası temelli).
Çıktı: res/v1_*.csv, v1.log"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_a")
from vcore import *

TG = ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "XU100.IS", "XU030.IS"]
D = {s: bist_day(s) for s in TG}

def row(lab, sym, o, cost, thr):
    r = []
    for per in ["IS", "OOS", "ALL"]:
        d = o[per]; r.append({"test": lab, "target": sym.replace(".IS", ""), "cost": cost, "thr": thr, "per": per, **d})
    return r

if __name__ == "__main__":
    SA = build_signals(drv_ret_cal); SA.to_parquet(OUTD + "/v1_signals_A.parquet")
    SB = build_signals(drv_ret_open); SB.to_parquet(OUTD + "/v1_signals_B.parquet")
    # kaynakla sayısal karşılaştırma (sadece okuma)
    try:
        SG = pd.read_parquet(S + "/out/code_havacilik/res/signals.parquet")
        for a, b in [("EU_X", "EUAIR_X"), ("US_X", "USAIR_X"), ("TUR", "TUR")]:
            j = pd.concat([SA[a], SG[b]], axis=1).dropna()
            print(f"karşılaştırma {a} vs kaynak {b}: n={len(j)} corr={j.iloc[:,0].corr(j.iloc[:,1]):.6f} max|fark|={np.abs(j.iloc[:,0]-j.iloc[:,1]).max():.2e}")
    except Exception as e:
        print("kaynak sinyal okunamadı", e)
    jb = pd.concat([SA.AIR.shift(1).rename("A"), SB.AIR.rename("B")], axis=1).dropna()
    print(f"Varyant A(shift1) vs B: n={len(jb)} corr={jb.A.corr(jb.B):.4f}, işaret uyumu |.|>1: {(np.sign(jb.A).where(jb.A.abs()>1,0)==np.sign(jb.B).where(jb.B.abs()>1,0)).mean():.3f}")
    rows = []; yrs = []
    for nm, sA, sB in [("AIR", SA.AIR, SB.AIR), ("COMBO", SA.COMBO, SB.COMBO), ("minusTUR", -SA.zTUR, -SB.zTUR)]:
        for s in TG:
            for cost in [8, 15]:
                o, pnl, pos = bt(sA.shift(1), D[s].intra, cost, 1.0)
                rows += row(nm + "_A", s, o, cost, 1.0)
                if cost == 8: yrs.append({"test": nm + "_A", "target": s, **o["years"]})
                o, pnl, pos = bt(sB, D[s].intra, cost, 1.0)
                rows += row(nm + "_B", s, o, cost, 1.0)
                if cost == 8: yrs.append({"test": nm + "_B", "target": s, **o["years"]})
    # placebo: daha bayat sinyal
    for lag in [2, 3, 5]:
        for s in TG[:3]:
            o, _, _ = bt(SA.AIR.shift(lag), D[s].intra, 8, 1.0); rows += row(f"AIR_A_placebo_lag{lag}", s, o, 8, 1.0)
            o, _, _ = bt(SA.COMBO.shift(lag), D[s].intra, 8, 1.0); rows += row(f"COMBO_A_placebo_lag{lag}", s, o, 8, 1.0)
    # gap'te (açılışta) ne kadar fiyatlanıyor? (işlenemez kısım) — sign pnl gap üzerinde
    for s in TG[:3]:
        o, _, _ = bt(SA.AIR.shift(1), D[s].gap, 0, 1.0); rows += row("AIR_A_on_GAP(not tradable)", s, o, 0, 1.0)
        o, _, _ = bt(SA.AIR.shift(1), D[s].cc, 0, 1.0); rows += row("AIR_A_on_CC(not tradable)", s, o, 0, 1.0)
    R = pd.DataFrame(rows); R.to_csv(OUTD + "/v1_bt.csv", index=False)
    Y = pd.DataFrame(yrs); Y.to_csv(OUTD + "/v1_years.csv", index=False)
    pd.set_option("display.width", 250)
    cols = ["n", "bps", "t_nw", "t_iid", "SR", "gross_bps", "t_gross", "hit"]
    print("\n=== Backtest (thr=1) ===")
    print(R[R.per != "ALL"].set_index(["test", "target", "cost", "per"])[cols].round(2).to_string())
    print("\n=== Yıllar (8 bps net, bps/işlem) ===")
    print(Y.set_index(["test", "target"]).round(1).to_string())
    # TUR t-1 -> THYAO intra corr (NW t)
    print("\n=== TUR_{t-1} -> gün-içi_t corr (NW t, standardize) ===")
    for s in TG[:3]:
        for lab, sig in [("A", SA.TUR.shift(1)), ("B", SB.TUR)]:
            for per, a, b in [("ALL", "2014", "2027"), ("IS", "2014", "2021-01-01"), ("OOS", "2021-01-01", "2027")]:
                j = pd.concat([D[s].intra.rename("y"), sig.rename("x")], axis=1).dropna(); j = j[(j.index >= a) & (j.index < b)]
                zy = (j.y - j.y.mean()) / j.y.std(); zx = (j.x - j.x.mean()) / j.x.std()
                c = j.y.corr(j.x)
                # NW t of slope: regress zy on zx
                e = zy - c * zx; u = (zx * e).values; n = len(u)
                g = (u @ u) / n
                for L in range(1, 6): g += 2 * (1 - L / 6) * (u[L:] @ u[:-L]) / n
                se = np.sqrt(g / n) / ((zx.values @ zx.values) / n)
                print(f"{s:9s} {lab} {per:3s} n={n} corr={c:+.3f} t_nw={c/se:+.2f}")
    print("ok")
