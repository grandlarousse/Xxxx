"""s4: Ortak faktor kontrolleri (NW t). intra_t ~ comp_t + [acilista bilinen kontroller] ; ayrica es-zamanli (islenemez) faktor kontrolleri
ve mekanizma: kompozit Avrupa/ABD celik gun-ici getirisini de ongoruyor mu?"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
c = vb.cal()
cA, _ = vb.comp(vb.JP_AU)
def onc(r): return r.reindex(c)
def lagUS(sym):
    """ABD/vadeli kapanisi t-1 (BIST takviminde: BIST gunu t icin, yerel tarihi < t olan son getiri)."""
    r = vb.dret(sym)
    s = pd.Series(np.nan, index=c)
    pos = r.index.searchsorted(c, side="left") - 1  # yerel tarihi < t olan son gun
    ok = pos >= 0
    s[ok] = r.values[pos[ok]]
    return s
XU = vb.bist("XU100.IS"); XS = vb.bist("XUSIN.IS")
ctrl_open = pd.DataFrame({
    "XU100_gap_t": XU.gap.reindex(c), "XU100_intra_t1": XU.intra.reindex(c).shift(1),
    "SPY_t1": lagUS("SPY"), "EEM_t1": lagUS("EEM"), "ES_t1": lagUS("ES=F"), "SLX_t1": lagUS("SLX"), "HG_t1": lagUS("HG=F"),
    "USDTRY_preopen": onc(vb.dret("TRY=X")),  # Yahoo '=X' ldate t kapanisi = t gunu 00:00 UTC -> BIST acilisindan ONCE bilinir
    "N225_z_t": onc(vb.zpast(vb.dret("^N225"))), "KS11_z_t": onc(vb.zpast(vb.dret("^KS11"))), "AXJO_z_t": onc(vb.zpast(vb.dret("^AXJO"))),
})
rows = []
def reg(y, X, lab, s, per):
    m = (X.index >= per[0]) & (X.index < per[1])
    res, n = vb.nwreg(y[m] if hasattr(y, "index") else y, X[m])
    rows.append(dict(stock=s, model=lab, period=per[2], b_comp=res.loc["comp", "b"] * 1e4, t_comp=res.loc["comp", "t"], n=n,
                     others=";".join(f"{k}:{v:.2f}" for k, v in res.t.items() if k != "comp")))
PER = [("2014-01-01", "2027-01-01", "ALL"), ("2014-01-01", "2021-01-01", "IS"), ("2021-01-01", "2027-01-01", "OOS")]
for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
    b = vb.bist(s); y = b.intra.reindex(c)
    own = pd.DataFrame({"own_gap_t": b.gap.reindex(c), "own_intra_t1": b.intra.reindex(c).shift(1), "own_cc_t1": b.cc.reindex(c).shift(1)})
    base = pd.DataFrame({"comp": cA})
    for per in PER:
        reg(y, base, "yalin", s, per)
        reg(y, pd.concat([base, own, ctrl_open], axis=1), "acilista bilinen tum kontroller", s, per)
        reg(y, pd.concat([base, own, ctrl_open[["XU100_gap_t", "XU100_intra_t1", "SPY_t1", "EEM_t1", "ES_t1", "USDTRY_preopen"]]], axis=1), "kontroller (genis Asya haric)", s, per)
        # es-zamanli (islenemez) faktorler: hisseye ozgu mu?
        reg(y, pd.concat([base, pd.DataFrame({"XU100_intra_t": XU.intra.reindex(c)})], axis=1), "es-zamanli XU100 intra_t kontrolu", s, per)
        reg(y, pd.concat([base, pd.DataFrame({"XU100_intra_t": XU.intra.reindex(c), "XUSIN_intra_t": XS.intra.reindex(c)})], axis=1), "es-zamanli XU100+XUSIN intra_t", s, per)
# mekanizma: kompozit -> yabanci celik gun-ici (o->c) ayni gun t ve XU100/XU030 gun-ici
def intra_foreign(sym):
    d = vb.by_ldate(sym); d = d[(d.o > 0) & (d.c > 0)]
    r = np.log(d.c / d.o); r[r.abs() > 0.2] = np.nan
    return r.reindex(c)
mech = []
for sym in ["MT.AS", "SZG.DE", "TKA.DE", "VOE.VI", "SSAB-A.ST", "SLX", "NUE", "VALE", "CLF", "^GDAXI", "^FCHI", "SPY", "XU100.IS", "XU030.IS"]:
    try:
        y = intra_foreign(sym) if not sym.endswith(".IS") else vb.bist(sym).intra.reindex(c)
    except Exception as e:
        print("yok", sym, e); continue
    for per in PER:
        m = (c >= per[0]) & (c < per[1])
        r, t, n = vb.corr_t(cA[m], y[m])
        mech.append(dict(target=sym, period=per[2], corr=r, t=t, n=n))
R = pd.DataFrame(rows); M = pd.DataFrame(mech)
R.to_csv(os.path.join(vb.OUT, "res_s4_controls.csv"), index=False); M.to_csv(os.path.join(vb.OUT, "res_s4_mechanism.csv"), index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 200)
print(R.drop(columns="others").round(3).to_string())
print(R[R.model == "acilista bilinen tum kontroller"][["stock", "period", "others"]].to_string())
print(M.pivot(index="target", columns="period", values="t").round(2).to_string())
print(M.pivot(index="target", columns="period", values="corr").round(3).to_string())
