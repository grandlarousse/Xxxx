"""S2: saatlik hizalı zamanlama testleri.
(a) Tam senkron: sürücü fiyatı 15:00 UTC anında (BIST kapanışı) vs BIST günlük kapanış -> günlük getiriler; standart günlük hizalamayla aynı tarihlerde kıyas.
(b) BIST kapanışı sonrası pencere: sürücü 15:00(t-1) -> sürücü yerel kapanış / 21:00 / ertesi 06:00 / 07:00 -> hisse gap_t ve intra_t.
E4 (Brent gece -> TUPRS gap), M3 (altın gece -> TRALT gap) burada."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal")
import vlib as V
RES = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal/res"
cal = V.cal()
def on_cal(s):  # UTC günü değerlerini BIST günlerine (aynı tarih) oturt
    return s.reindex(cal)
xu = V.ret("XU100.IS"); xud = V.dec("XU100.IS")
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
# (a) tam senkron
P("== (a) 15:00 UTC senkron (sürücü h1 snap) vs standart günlük hizalama, aynı tarihler")
PAIRS = [("THYAO.IS", "LHA.DE"), ("THYAO.IS", "IAG.L"), ("PGSUS.IS", "IAG.L"), ("PGSUS.IS", "LHA.DE"), ("TAVHL.IS", "ADP.PA"),
         ("EREGL.IS", "VOE.VI"), ("EREGL.IS", "SZG.DE"), ("TUPRS.IS", "BZ=F"), ("TRALT.IS", "GC=F"), ("EREGL.IS", "SLX")]
rows = []
for st, dr in PAIRS:
    a = V.ret(st); bstd = V.ret(dr)
    p15 = on_cal(V.snap(dr, "15:00")); b15 = np.log(p15).diff()
    # 15:00'te bayat (Avrupa sabah açılmadan / ABD ETF 13:30 öncesi) -> ABD ETF için 15:00 snap = ABD seansı içi
    df = pd.concat([a.rename("a"), b15.rename("b15"), bstd.rename("bstd"), xu.rename("xu")], axis=1, sort=True).dropna()
    df = df[df.index >= "2024-01-01"]
    c15 = V.pcorr(df.a, df.b15, [df.xu]); cst = V.pcorr(df.a, df.bstd, [df.xu])
    r0 = {"stock": st, "driver": dr, "n": len(df), "c_15": df.a.corr(df.b15), "pc_15": c15[0], "c_std": df.a.corr(df.bstd), "pc_std": cst[0]}
    rows.append(r0)
    P(f"  {st}~{dr}: n={len(df)} | 15:00 senkron c={r0['c_15']:.3f} pc={r0['pc_15']:.3f} | standart c={r0['c_std']:.3f} pc={r0['pc_std']:.3f}")
pd.DataFrame(rows).to_csv(f"{RES}/s2_sync1500.csv", index=False)

# (b) gece/akşam pencereleri
def windows(dr):
    """BIST günü t için: post = sürücü 15:00(t-1)->21:00(t-1) ; night = 21:00(t-1)->06:00(t) ; pre5 = 06:00->07:00(t); on07 = 15:00(t-1)->07:00(t); on06 = 15:00(t-1)->06:00(t);
    sess = 07:00(t)->15:00(t)."""
    s15 = V.snap(dr, "15:00"); s21 = V.snap(dr, "21:00"); s06 = V.snap(dr, "06:00"); s07 = V.snap(dr, "07:00")
    d = pd.DataFrame({"p15": s15, "p21": s21, "p06": s06, "p07": s07})
    # her BIST günü t için önceki BIST günü (t-1)
    c = cal[cal >= d.index[0]]
    prev = pd.Series(c[:-1], index=c[1:])
    D = pd.DataFrame(index=c[1:])
    g = lambda col, idx: d[col].reindex(idx).values
    D["p15_prev"] = g("p15", prev.values); D["p21_prev"] = g("p21", prev.values)
    D["p06"] = g("p06", D.index); D["p07"] = g("p07", D.index); D["p15"] = g("p15", D.index)
    W = pd.DataFrame(index=D.index)
    W["post"] = np.log(D.p21_prev / D.p15_prev); W["night"] = np.log(D.p06 / D.p21_prev); W["pre"] = np.log(D.p07 / D.p06)
    W["on06"] = np.log(D.p06 / D.p15_prev); W["on07"] = np.log(D.p07 / D.p15_prev); W["sess"] = np.log(D.p15 / D.p07)
    return W
P("\n== (b) Gece hareketi -> açılış gap / gün-içi (hisse günlük o,c; XU100 gap/intra kontrol)")
NIGHT = [("TUPRS.IS", "BZ=F", "E4"), ("TRALT.IS", "GC=F", "M3"), ("TRMET.IS", "GC=F", "M3x"), ("THYAO.IS", "BZ=F", "x"), ("PETKM.IS", "BZ=F", "x"),
         ("TUPRS.IS", "ES=F", "kontrol"), ("TRALT.IS", "ES=F", "kontrol"), ("XU100.IS", "BZ=F", "piyasa"), ("XU100.IS", "GC=F", "piyasa")]
rows = []
for st, dr, cid in NIGHT:
    W = windows(dr); dd = V.dec(st)
    es = windows("ES=F") if dr != "ES=F" else None
    df = pd.concat([dd.gap.rename("gap"), dd.intra.rename("intra"), xud.gap.rename("xg"), xud.intra.rename("xi"), W], axis=1, sort=True)
    if es is not None: df["es_on07"] = es["on07"]; df["es_sess"] = es["sess"]
    df = df[df.index >= "2024-06-12"]
    for sig in ["on07", "on06", "post", "night", "sess"]:
        for tg in ["gap", "intra"]:
            x = df[[tg, sig, "xg", "xi"] + (["es_on07"] if es is not None else [])].dropna()
            if len(x) < 50: continue
            c = x[tg].corr(x[sig])
            ctrl = [x.xg] if tg == "gap" else [x.xi]
            pcx = V.pcorr(x[tg], x[sig], ctrl)
            pce = V.pcorr(x[tg], x[sig], ctrl + ([x.es_on07] if es is not None else [])) if st != "XU100.IS" else (np.nan,)
            t_nw = V.pc_nwt(x[tg], x[sig], None); t_nwx = V.pc_nwt(x[tg], x[sig], ctrl)
            # yıllık / yarı dönem
            h1 = x[x.index < "2025-08-01"]; h2 = x[x.index >= "2025-08-01"]
            rows.append({"claim": cid, "stock": st, "drv": dr, "sig": sig, "target": tg, "n": len(x), "corr": c, "t_nw": t_nw, "pc_xu": pcx[0], "t_nw_xu": t_nwx,
                         "pc_xu_es": pce[0], "c_h1": h1[tg].corr(h1[sig]), "c_h2": h2[tg].corr(h2[sig])})
R2 = pd.DataFrame(rows); R2.to_csv(f"{RES}/s2_night.csv", index=False)
pd.set_option("display.width", 250)
P(R2.round(3).to_string())
# M3: XU100-arındırılmış gap: gap - beta*XU100 gap (beta tam örneklem) ve 'hedge'li' (gap - xg)
for st, dr in [("TRALT.IS", "GC=F"), ("TUPRS.IS", "BZ=F")]:
    W = windows(dr); dd = V.dec(st)
    x = pd.concat([dd.gap.rename("g"), xud.gap.rename("xg"), W.on07, W.on06], axis=1, sort=True).dropna(); x = x[x.index >= "2024-06-12"]
    b = np.cov(x.g, x.xg)[0, 1] / x.xg.var(); res = x.g - b * x.xg
    for sig in ["on06", "on07"]:
        P(f"{st} gap-β·XU100gap (β={b:.2f}) ~ {dr} {sig}: corr={res.corr(x[sig]):.3f}, NW-t={V.pc_nwt(res, x[sig], None):.2f}; hedge'li (gap−XU100gap) corr={(x.g - x.xg).corr(x[sig]):.3f}; n={len(x)}")
# gece |hareket| > %1 alt örneklemi ve kuyruk etkisi
for st, dr in [("TUPRS.IS", "BZ=F"), ("TRALT.IS", "GC=F")]:
    W = windows(dr); dd = V.dec(st)
    x = pd.concat([dd.gap.rename("g"), dd.intra.rename("i"), W.on07], axis=1, sort=True).dropna(); x = x[x.index >= "2024-06-12"]
    big = x[x.on07.abs() > 0.01]; small = x[x.on07.abs() <= 0.01]
    beta = np.polyfit(x.on07, x.g, 1)[0]
    P(f"{st}~{dr}: gap beta={beta:.2f}; |gece|>%1 n={len(big)} corr={big.g.corr(big.on07):.3f}; küçük n={len(small)} corr={small.g.corr(small.on07):.3f}; Spearman tüm={x.g.corr(x.on07, method='spearman'):.3f}")
    # gün-içi devam: sign(on07) * intra
    pos = np.sign(x.on07); pnl = pos * x.i
    P(f"   gün-içi devam testi: ort sign(gece)*intra = {1e4*pnl.mean():.1f} bps (NW-t {V.pc_nwt(pnl, pd.Series(np.zeros(len(pnl)), index=pnl.index) + 0, None) if False else np.nan}); corr(gece, intra)={x.i.corr(x.on07):.3f}")
open(f"{RES}/s2_hourly.txt", "w").write("\n".join(out))
