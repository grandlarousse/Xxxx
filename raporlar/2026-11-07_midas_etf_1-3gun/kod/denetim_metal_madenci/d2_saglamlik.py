"""D2: S1-S5 istatistiksel sağlamlık: parametre komşuluğu, h/mod, yıl yıl, 2020/2022 hariç, en iyi 5 işlem hariç,
rastgele giriş permütasyonu (düz ve yıl tabakalı, 5000 tekrar), maliyet (1.000/2.500/10.000$), C0 kayması, en büyük 5 kazanç.
Çalıştır: python3 -I kod/denetim_metal_madenci/d2_saglamlik.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M
from d1_yeniden import ibs_sig, month_end, bb_sig

WARM = 200

def warm(s, w=WARM):
    s = s.copy(); s.iloc[:w] = False; return s

def tom_sig(d, k_end=1):
    """Ayın sondan k. işlem günü (k=1 son gün)."""
    idx = d.index; ym = pd.Series(idx.year * 100 + idx.month, index=idx)
    pos = ym.groupby(ym).cumcount(ascending=False)  # 0 = son gün
    s = pos == (k_end - 1); s.iloc[-1] = False
    return s

def block(name, d, s, h, mode, cost, out, extra=None):
    tr = M.sim(d, s, h, mode, cost); r = M.summ(tr, name)
    if extra: r.update(extra)
    out.append(r); return tr, r

def line(r):
    if r.get("n", 0) == 0: return f"{r['label']}: n=0"
    return (f"{r['label']}: n={r['n']} brüt={r['gross_bp']:.0f} net={r['net_bp']:.0f} t={r['t']:.2f} "
            f"IS={r['is_net_bp']:.0f}(t{r['is_t']:.2f}) OOS={r['oos_net_bp']:.0f}(t{r['oos_t']:.2f}) yıl+={r['yil_poz']:.2f}")

def robust(tag, d, s, h, mode, cost, out, top=True):
    tr = M.sim(d, s, h, mode, cost)
    base = M.summ(tr, f"{tag} ana"); out.append(base); print("  " + line(base))
    yr = tr.groupby(tr["sig"].dt.year)["net"].agg(["size", "mean", "sum"])
    print("  yıl yıl (n, ort net bp):", " ".join(f"{y}:{int(a)}/{b*1e4:.0f}" for y, (a, b, c) in yr.iterrows()))
    for ex in ([2020], [2022], [2020, 2022], [2024, 2025, 2026]):
        m = ~tr["sig"].dt.year.isin(ex); x = tr.loc[m, "net"].values
        r = {"label": f"{tag} hariç {ex}", "n": len(x), "net_bp": x.mean() * 1e4, "t": M.tstat(x)}; out.append(r)
        print(f"  {ex} hariç: n={len(x)} net={x.mean()*1e4:.1f} t={M.tstat(x):.2f}")
    srt = tr.sort_values("net", ascending=False)
    x = srt["net"].values[5:]
    out.append({"label": f"{tag} en iyi 5 hariç", "n": len(x), "net_bp": x.mean() * 1e4, "t": M.tstat(x)})
    print(f"  en iyi 5 işlem hariç: n={len(x)} net={x.mean()*1e4:.1f} t={M.tstat(x):.2f}")
    if top:
        print("  en büyük 5 kazanç:")
        for _, rr in srt.head(5).iterrows():
            print(f"    {rr['sig'].date()} giriş {rr['entry'].date()} @ {rr['ep']:.2f} -> {rr['exit'].date()} @ {rr['xp']:.2f}: {rr['gross']*1e4:.0f} bp")
    a, mu, p = M.perm_test(d, tr, h, mode, reps=5000, start=tr["sig"].min())
    a2, mu2, p2 = M.perm_test(d, tr, h, mode, reps=5000, by_year=True)
    out.append({"label": f"{tag} permütasyon", "n": len(tr), "gross_bp": a, "rastgele_ort_bp": mu, "p_perm": p,
                "rastgele_yil_ort_bp": mu2, "p_perm_yil": p2})
    print(f"  permütasyon (5000): gerçek brüt {a:.1f} bp; rastgele ort {mu:.1f} bp, p={p:.4f} | yıl tabakalı: rastgele ort {mu2:.1f}, p={p2:.4f}")
    g = tr["gross"].values
    for pos in (1000, 2500, 10000):
        cst = 2 * 1.5 / pos * 1e4 + (cost - 12.0)
        x = g - cst / 1e4
        print(f"  maliyet {pos}$ ({cst:.1f} bp): net={x.mean()*1e4:.1f} t={M.tstat(x):.2f}", end=";")
    x = g - (cost + 10) / 1e4
    print(f"\n  +10 bp ek kayma (C0 MOC yok): net={x.mean()*1e4:.1f} t={M.tstat(x):.2f}")
    return tr

def main():
    out = []
    # ---------------- S3 / S4 : IBS
    for tag, sym in (("S3", "GDXJ"), ("S4", "GLD")):
        d = M.px(sym); cst = M.cost_static(d)
        print("=" * 100); print(tag, sym, "IBS<0.10 & düşüş, C0 h3")
        robust(tag, d, warm(ibs_sig(d)), 3, "C0", cst, out)
        print("  -- eşik komşuluğu (C0 h3) [düşüş koşullu | koşulsuz]:")
        for thr in (0.05, 0.075, 0.10, 0.125, 0.15, 0.20, 0.25):
            ra = M.summ(M.sim(d, warm(ibs_sig(d, thr, True)), 3, "C0", cst), f"{tag} thr{thr} düşüş"); out.append(ra)
            rb = M.summ(M.sim(d, warm(ibs_sig(d, thr, False)), 3, "C0", cst), f"{tag} thr{thr} koşulsuz"); out.append(rb)
            print(f"    thr={thr}: n={ra['n']} net={ra['net_bp']:.0f} t={ra['t']:.2f} IS t{ra['is_t']:.2f} OOS t{ra['oos_t']:.2f} | "
                  f"n={rb['n']} net={rb['net_bp']:.0f} t={rb['t']:.2f} IS t{rb['is_t']:.2f} OOS t{rb['oos_t']:.2f}")
        print("  -- h ve mod (thr 0.10, düşüş):")
        for mode in ("C0", "O1", "C1"):
            txt = []
            for h in (1, 2, 3, 4, 5):
                r = M.summ(M.sim(d, warm(ibs_sig(d)), h, mode, cst), f"{tag} {mode} h{h}"); out.append(r)
                txt.append(f"h{h}: {r['net_bp']:.0f}bp t{r['t']:.2f} (IS t{r['is_t']:.1f}/OOS t{r['oos_t']:.1f})")
            print(f"    {mode}: " + " | ".join(txt))
    # ---------------- S1 / S2 : ay dönümü
    for tag, sym in (("S1", "GDX"), ("S2", "GLD")):
        d = M.px(sym); cst = M.cost_static(d)
        print("=" * 100); print(tag, sym, "ay sonu son gün C0 -> 3. gün")
        robust(tag, d, warm(month_end(d)), 3, "C0", cst, out)
        print("  -- giriş günü (sondan k.) x tutuş h (C0) net bp / t:")
        for k in (1, 2, 3, 4):
            txt = []
            for h in (1, 2, 3, 4, 5, 6):
                r = M.summ(M.sim(d, warm(tom_sig(d, k)), h, "C0", cst), f"{tag} k{k} h{h}"); out.append(r)
                txt.append(f"h{h}:{r['net_bp']:.0f}/t{r['t']:.2f}")
            print(f"    sondan {k}. gün: " + " ".join(txt))
        for mode in ("O1", "C1"):
            txt = []
            for h in (1, 2, 3, 4, 5):
                r = M.summ(M.sim(d, warm(month_end(d)), h, mode, cst), f"{tag} {mode} h{h}"); out.append(r)
                txt.append(f"h{h}:{r['net_bp']:.0f}/t{r['t']:.2f}")
            print(f"    {mode}: " + " ".join(txt))
    # ---------------- S5 : Bollinger SILJ C1
    d = M.px("SILJ"); cst = M.cost_static(d)
    print("=" * 100); print("S5 SILJ BB20/2 C1 h3")
    robust("S5", d, warm(bb_sig(d)), 3, "C1", cst, out)
    print("  ısınma 20 gün (BB20 için yeterli):", line(M.summ(M.sim(d, warm(bb_sig(d), 20), 3, "C1", cst), "S5 warm20")))
    print("  -- n x k komşuluğu (C1 h3):")
    for n in (10, 15, 20, 25, 30):
        txt = []
        for k in (1.5, 2.0, 2.5):
            r = M.summ(M.sim(d, warm(bb_sig(d, n, k)), 3, "C1", cst), f"S5 n{n} k{k}"); out.append(r)
            txt.append(f"k{k}: n={r['n']} {r['net_bp']:.0f}bp t{r['t']:.2f}")
        print(f"    n={n}: " + " | ".join(txt))
    for mode in ("C0", "O1", "C1"):
        txt = []
        for h in (1, 2, 3, 4, 5):
            r = M.summ(M.sim(d, warm(bb_sig(d)), h, mode, cst), f"S5 {mode} h{h}"); out.append(r)
            txt.append(f"h{h}:{r['net_bp']:.0f}/t{r['t']:.2f}")
        print(f"    {mode}: " + " ".join(txt))
    # 'C1' = sinyal + 1 gün bekleme. Bekleme süresi komşuluğu: C0 girişini 0..3 gün kaydır
    print("  -- bekleme süresi (sinyal sonrası w gün kapanışında gir, 3 gün tut):")
    s0 = warm(bb_sig(d)); txt = []
    for w in (0, 1, 2, 3):
        r = M.summ(M.sim(d, s0.shift(w).fillna(False).astype(bool), 3, "C0", cst), f"S5 bekle{w}"); out.append(r)
        txt.append(f"w{w}: n={r['n']} {r['net_bp']:.0f}bp t{r['t']:.2f}")
    print("    " + " | ".join(txt))
    pd.DataFrame(out).to_csv(os.path.join(M.OUTD, "d2_saglamlik.csv"), index=False)

if __name__ == "__main__":
    main()
