"""(a) E3 iddiasının ham veriden yeniden üretimi + (d) IS/OOS/yıllar + (e) maliyet.
Tanımlar kaynak koddan (code_enerji/02_tuprs.py, 06b_bt_extra.py, 03_scan.py):
  US_REF = eşit ağırlıklı ortalama log getiri (VLO, MPC, PSX, PBF), BIST takviminde, shift(1)
  y = TUPRS gün-içi log(c/o); y_h = TUPRS intra - XU100 intra
  reg: y_h ~ US_REF_lag1 + ES_lag1 + BZ_lag1 (HAC 5), 2014+
  BT: |z|>1 (250g, min 60, shift1), tek bacak TUPRS intra, sinyal 2014-01-01'den başlar.
"""
import numpy as np, pandas as pd, json
import vlib as V

out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)

cal = V.bist_cal()
tu = V.bist_decomp("TUPRS.IS"); xu = V.bist_decomp("XU100.IS"); x30 = V.bist_decomp("XU030.IS")
tu = tu.reindex(cal); xu = xu.reindex(cal); x30 = x30.reindex(cal)

# veri sağlığı
P("== VERİ SAĞLIĞI")
for nm, d in [("TUPRS", tu), ("XU100", xu), ("XU030", x30)]:
    dd = d[d.index >= "2014-01-01"]
    P(nm, "2014+ gün:", dd.cc.notna().sum(), "intra NaN:", int(dd.intra.isna().sum()), "o==önceki c oranı (yıllık):",
      dd.groupby(dd.index.year).stale_open.mean().round(3).to_dict())
raw_tu = V.by_ldate("TUPRS.IS"); r_raw = np.log(raw_tu.adj).diff(); pc = np.expm1(r_raw)
P("TUPRS ±%10,5 dışı (fiyat bazlı) gün sayısı 2014+:", int(((pc > .105) | (pc < -.105))[raw_tu.index >= "2014"].sum()),
  "| -%10,5 altı:", int((pc < -.105)[raw_tu.index >= "2014"].sum()), "| +%10,5 üstü:", int((pc > .105)[raw_tu.index >= "2014"].sum()))

US = ["VLO", "MPC", "PSX", "PBF"]
A = pd.concat({s: V.map_A(s, cal) for s in US}, axis=1)
B = pd.concat({s: V.map_B(s, cal) for s in US}, axis=1)
for s in US:
    _, _, nb = V.us_close(s); P(f"{s}: 12σ temizliğiyle atılan gün={nb}")
usA = A.mean(axis=1)            # BIST takviminde günlük sepet getirisi (t_önceki, t]
sigA = usA.shift(1)             # t-1 -> t: BIST açılışından ÖNCE biliniyor (ABD kapanışı t-1 ~20-21 UTC < 07:00 UTC t)
sigB = B.mean(axis=1)           # taze bilgi: açılışta bilinen tüm ABD kapanışları
es = V.map_A("ES=F", cal).shift(1); bz = V.map_A("BZ=F", cal).shift(1)
xle = V.map_A("XLE", cal).shift(1); crak = V.map_A("CRAK", cal).shift(1)
vlo = A["VLO"].shift(1)
P("sigA vs sigB: eşit gün oranı", round(float((sigA - sigB).abs().lt(1e-12)[sigA.index >= "2014"].mean()), 3),
  "| corr", round(sigA.corr(sigB), 4))

y = tu.intra; y_h = tu.intra - xu.intra; y_h30 = tu.intra - x30.intra
X = pd.DataFrame({"y": y, "y_h": y_h, "y_h30": y_h30, "gap": tu.gap, "cc": tu.cc, "US": sigA, "USB": sigB, "VLO": vlo, "ES": es, "BZ": bz,
                  "XLE": xle, "CRAK": crak, "tu_cc1": tu.cc.shift(1), "xu_cc1": xu.cc.shift(1), "xu_gap": xu.gap, "xu_intra": xu.intra,
                  "tu_intra1": tu.intra.shift(1)}, index=cal)
X = X[X.index >= "2014-01-01"]
X.to_parquet(V.RES + "/panel_E3.parquet")

def reg(yv, cols, sub, lab):
    m = V.hac(sub[yv], sub[cols])
    return f"{lab:4s} {yv:6s} ~ {'+'.join(cols):40s} | " + ", ".join(f"{c}: b={m.params[c]*100:.2f}e-2 t={m.tvalues[c]:.2f}" for c in cols[:3]) + f" | n={int(m.nobs)} R2={m.rsquared:.4f}"

base = X.dropna(subset=["y", "y_h", "US", "ES", "BZ"])
P("\n== (a1) İDDİA: y_h ~ US_REF + ES + BZ (HAC5). İddia: ALL t=4,53 (02_tuprs: IS 2,04 / OOS 3,91)")
for lab, sub in [("ALL", base), ("IS", base[base.index < "2021"]), ("OOS", base[base.index >= "2021"])]:
    P(reg("y_h", ["US", "ES", "BZ"], sub, lab)); P(reg("y", ["US", "ES", "BZ"], sub, lab)); P(reg("y_h30", ["US", "ES", "BZ"], sub, lab))
    P(reg("gap", ["US", "ES", "BZ"], sub, lab))

P("\n== (a2) Ek kontroller: kendi gecikmesi, XU100 gecikmesi, açılış gap'i (açılışta biliniyor), XU100 gap")
ctl = ["US", "ES", "BZ", "tu_cc1", "xu_cc1", "gap", "xu_gap", "tu_intra1"]
b2 = X.dropna(subset=["y", "y_h"] + ctl)
for lab, sub in [("ALL", b2), ("IS", b2[b2.index < "2021"]), ("OOS", b2[b2.index >= "2021"])]:
    m = V.hac(sub["y_h"], sub[ctl]); P(lab, "y_h ~ +kontroller | t:", {c: round(m.tvalues[c], 2) for c in ctl}, "n=", int(m.nobs))
    m = V.hac(sub["y"], sub[ctl]); P(lab, "y   ~ +kontroller | t:", {c: round(m.tvalues[c], 2) for c in ctl})

P("\n== (a3) Sektör-özgüllüğü: US_REF vs XLE vs CRAK yarışı (y_h)")
b3 = X.dropna(subset=["y_h", "US", "XLE", "ES", "BZ"])
for lab, sub in [("ALL", b3), ("IS", b3[b3.index < "2021"]), ("OOS", b3[b3.index >= "2021"])]:
    m = V.hac(sub["y_h"], sub[["US", "XLE", "ES", "BZ"]]); P(lab, "y_h ~ US+XLE+ES+BZ | t:", {c: round(m.tvalues[c], 2) for c in ["US", "XLE", "ES", "BZ"]})
    m = V.hac(sub["y_h"], sub[["XLE", "ES", "BZ"]]); P(lab, "y_h ~ XLE+ES+BZ | t:", {c: round(m.tvalues[c], 2) for c in ["XLE", "ES", "BZ"]})

P("\n== (a4) VLO tek başına: corr(VLO_t-1, y_h). İddia (tarama, iid t): tam 5,98; IS t=3,76 (c=0,095) / OOS t=4,48 (c=0,119)")
for lab, sub in [("ALL", X), ("IS", X[X.index < "2021"]), ("OOS", X[X.index >= "2021"])]:
    for tgt in ["y_h", "y"]:
        r, ti, tn, n = V.corr_t(sub[tgt], sub["VLO"]); P(f"{lab} VLO->{tgt}: corr={r:.3f} t_iid={ti:.2f} t_NW={tn:.2f} n={n}")
    r, ti, tn, n = V.corr_t(sub["y_h"], sub["US"]); P(f"{lab} US_REF->y_h: corr={r:.3f} t_iid={ti:.2f} t_NW={tn:.2f} n={n}")
    r, ti, tn, n = V.corr_t(sub["y_h"], sub["USB"]); P(f"{lab} US_REF(B taze)->y_h: corr={r:.3f} t_iid={ti:.2f} t_NW={tn:.2f} n={n}")

P("\n== (a5) Gap vs gün-içi payı (iddia: gap beta 0,034, intra beta 0,057 -> %62 gün-içi)")
b5 = X.dropna(subset=["y", "gap", "US"])
for lab, sub in [("ALL", b5), ("IS", b5[b5.index < "2021"]), ("OOS", b5[b5.index >= "2021"])]:
    mg = V.hac(sub.gap, sub[["US"]]); mi = V.hac(sub.y, sub[["US"]]); mc = V.hac(sub.gap + sub.y, sub[["US"]])
    P(f"{lab}: gap b={mg.params.US:.3f} (t {mg.tvalues.US:.2f}) | intra b={mi.params.US:.3f} (t {mi.tvalues.US:.2f}) | cc b={mc.params.US:.3f} (t {mc.tvalues.US:.2f}) | intra payı={mi.params.US/(mg.params.US+mi.params.US):.2f}")
# senkron bağlam: aynı gün (t) ABD sepeti ile TUPRS cc_t (ABD t kapanışı BIST'ten sonra)
P("Bağlam: corr(TUPRS cc_t, US_REF_t aynı gün)=", round(X.cc.corr(usA.reindex(X.index)), 3), "| corr(TUPRS cc_t, US_REF_t-1)=", round(X.cc.corr(X.US), 3))

P("\n== (b/e) BACKTEST yeniden üretim: |z|>1, tek bacak TUPRS intra (iddia: brüt IS 17,7 (t 2,4) OOS 25,6 (t 2,3); 8bps Sharpe IS 0,44 OOS 0,62; 15bps 0,12/0,37)")
sig = sigA[sigA.index >= "2014-01-01"]
rows = []
def runbt(name, s, tgt, legs=1, **kw):
    for c in (0, 8, 15):
        res, pnl, pos, df = V.backtest(s, tgt, cost_bps=c, legs=legs, **kw)
        for per in ["IS", "OOS", "ALL"]:
            r = res[per]; rows.append({"strateji": name, "maliyet_bps_bacak": c, "bacak": legs, "dönem": per, **r})
        if c == 0: yb = res["by_year_bps"]; yn = res["by_year_n"]
    return yb, yn
yb, yn = runbt("Z1_USREF_A->TUPRS_intra", sig, X.y)
P("yıllık brüt bps:", yb); P("yıllık n:", yn)
B_ = pd.DataFrame(rows)
P(B_[B_.strateji == "Z1_USREF_A->TUPRS_intra"][["maliyet_bps_bacak", "dönem", "n", "n_long", "n_short", "mean_bps", "t", "hit", "sharpe", "ann_pct", "maxdd_pct"]].round(2).to_string(index=False))

# varyantlar
var = {
 "Z1_USREF_B(taze)->intra": (sigB[sigB.index >= "2014"], X.y, 1, dict(mode="z", thr=1.0)),
 "SIGN_USREF_A->intra": (sig, X.y, 1, dict(mode="sign", thr=0.0)),
 "Z0.5_USREF_A->intra": (sig, X.y, 1, dict(mode="z", thr=0.5)),
 "Z1.5_USREF_A->intra": (sig, X.y, 1, dict(mode="z", thr=1.5)),
 "Z2_USREF_A->intra": (sig, X.y, 1, dict(mode="z", thr=2.0)),
 "Z1_VLO->intra": (vlo[vlo.index >= "2014"], X.y, 1, dict(mode="z", thr=1.0)),
 "Z1_USREF_A->TUPRS-XU030 (2 bacak)": (sig, X.y_h30, 2, dict(mode="z", thr=1.0)),
 "Z1_USREF_A->TUPRS-XU100 (2 bacak)": (sig, X.y_h, 2, dict(mode="z", thr=1.0)),
 "Z1_XLE->intra": (xle[xle.index >= "2014"], X.y, 1, dict(mode="z", thr=1.0)),
 "Z1_ES->intra (plasebo/piyasa)": (es[es.index >= "2014"], X.y, 1, dict(mode="z", thr=1.0)),
 "Z1_BZ->intra": (bz[bz.index >= "2014"], X.y, 1, dict(mode="z", thr=1.0)),
 "Z1_USREF_A->XU030 intra (piyasa?)": (sig, x30.intra.reindex(X.index), 1, dict(mode="z", thr=1.0)),
}
ybs = {"Z1_USREF_A->TUPRS_intra": yb}
for k, (s, t, legs, kw) in var.items():
    ybs[k], _ = runbt(k, s, t, legs, **kw)
B_ = pd.DataFrame(rows); B_.to_csv(V.RES + "/backtests_E3.csv", index=False)
pv = B_[B_.dönem.isin(["IS", "OOS"])].pivot_table(index="strateji", columns=["maliyet_bps_bacak", "dönem"], values="sharpe", aggfunc="first").round(2)
P("\nSharpe (maliyet/bacak, dönem):"); P(pv.to_string())
pv2 = B_[B_.dönem.isin(["IS", "OOS"]) & (B_.maliyet_bps_bacak == 0)].pivot_table(index="strateji", columns="dönem", values=["mean_bps", "t", "n"], aggfunc="first").round(1)
P("\nBrüt bps/işlem, t, n:"); P(pv2.to_string())
Y = pd.DataFrame(ybs).T; Y.to_csv(V.RES + "/bt_by_year_gross_bps.csv")
P("\nYıllık brüt bps/işlem:"); P(Y.round(0).to_string())

# long/short ayrıştırma ve sürüklenme katkısı
res, pnl, pos, df = V.backtest(sig, X.y, cost_bps=0)
P("\n== Long/short ayrıştırma (brüt, Z1 ana strateji)")
for per, m in [("IS", df.index < "2021"), ("OOS", df.index >= "2021")]:
    p = pos[m]; yy = df.y[m]
    lg = yy[p > 0]; sh = -yy[p < 0]
    P(f"{per}: long n={len(lg)} ort={1e4*lg.mean():.1f} bps (t {V.nw_mean(lg)[1]:.2f}) | short n={len(sh)} ort={1e4*sh.mean():.1f} bps (t {V.nw_mean(sh)[1]:.2f}) | "
      f"TUPRS intra ort (tüm günler)={1e4*yy.mean():.1f} bps | ort pos={p[p!=0].mean():.3f} -> sürüklenme katkısı≈{1e4*p[p!=0].mean()*yy.mean():.1f} bps")
open(V.RES + "/01_replicate.txt", "w").write("\n".join(out))
