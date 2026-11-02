"""S4: ek şüpheci testler.
(1) E1: CRAK, TUPRS'u ~%4 ağırlıkla içeriyor (MarketXLS 01.10.2026: %3,91) -> mekanik içerme: CRAK_ex = (CRAK - w*TUPRS_usd)/(1-w).
(2) A1: Avrupa havayolu t-1 -> THYAO/PGSUS gap / intra ayrıştırması, dönemlere göre; Brent+STOXX kontrolü.
(3) M3/E4 yarıyıllık kırılım."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal")
import vlib as V
from s2_hourly_windows import windows
RES = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal/res"
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
R = {}
def r(s):
    if s not in R: R[s] = V.ret(s)
    return R[s]
xu, fx, eem, es, sx, bz = r("XU100.IS"), r("TRY=X"), r("EEM"), r("ES=F"), r("^STOXX"), r("BZ=F")
# (1) CRAK mekanik içerme
tu = r("TUPRS.IS"); tu_usd = tu - fx; crak = r("CRAK")
P("== E1 CRAK ex-TUPRS (ağırlık w varsayımı)")
for w in [0.0, 0.03, 0.04, 0.05, 0.08]:
    cx = (crak - w * tu_usd) / (1 - w)
    o = {k: V.pcorr(tu, cx, [xu], s, e)[0] for k, (s, e) in V.PER.items()}
    o3 = V.pcorr(tu, cx, [xu, fx, eem, es], "2010-01-01")[0]
    W_ = V.pcorr(V.wk(tu), V.wk(cx), [V.wk(xu)], "2010-01-01")[0]
    P(f"  w={w:.2f}: pc|XU100 tam={o['tam']:.3f} IS={o['IS']:.3f} OOS={o['OOS']:.3f} 1y={o['1y']:.3f} | pc|XU100+USDTRY+EEM+ES={o3:.3f} | haftalık pc={W_:.3f}")
# CRAK'ın TUPRS_usd yüklemesi (diğer rafineriler kontrollü) — içerme ağırlığının kaba tahmini
peers = ["VLO", "MPC", "PSX", "PBF", "DK", "DINO", "NESTE.HE", "RELIANCE.NS", "010950.KS", "096770.KS", "PKN.WA", "MOL.BD", "MOH.AT", "ELPE.AT", "GALP.LS", "REP.MC", "OMV.VI"]
X = [tu_usd] + [r(p) for p in peers] + [es, eem]
b, t, n = V.nw_reg(crak[crak.index >= "2016-01-01"], X)
P(f"  CRAK ~ TUPRS_usd + {len(peers)} rafineri + ES + EEM: TUPRS_usd katsayı={b[0]:.3f} (NW-t {t[0]:.2f}), n={n}  [beklenen ≈ ağırlık ~0,04]")
# plasebo: aynı regresyonda PETKM_usd (CRAK'ta yok)
pk_usd = r("PETKM.IS") - fx
b2, t2, _ = V.nw_reg(crak[crak.index >= "2016-01-01"], [pk_usd] + X[1:])
P(f"  plasebo PETKM_usd katsayı={b2[0]:.3f} (NW-t {t2[0]:.2f})")
# TUPRS ~ diğer rafineri sepeti (CRAK yerine, mekanik içerme yok)
eu = pd.concat([r(p) for p in ["NESTE.HE", "PKN.WA", "MOL.BD", "MOH.AT", "ELPE.AT", "GALP.LS", "REP.MC", "OMV.VI"]], axis=1).mean(axis=1)
us = pd.concat([r(p) for p in ["VLO", "MPC", "PSX", "PBF"]], axis=1).mean(axis=1)
for nm, bb in [("AB rafineri sepeti", eu), ("ABD rafineri sepeti", us)]:
    o = {k: V.pcorr(tu, bb, [xu], s, e)[0] for k, (s, e) in V.PER.items()}
    P(f"  TUPRS ~ {nm}: pc|XU100 tam={o['tam']:.3f} IS={o['IS']:.3f} OOS={o['OOS']:.3f} 1y={o['1y']:.3f}; +USDTRY+EEM+bölge={V.pcorr(tu, bb, [xu, fx, eem, sx if 'AB' in nm else es], '2010-01-01')[0]:.3f}")
# (2) A1 gecikme ayrıştırması
P("\n== A1 Avrupa havayolu (t-1) -> hisse gap_t / intra_t (2014+), XU100 gap/intra kontrollü; ve hisse t-1 -> sürücü t")
xd = V.dec("XU100.IS")
for st in ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"]:
    d = V.dec(st)
    for dr in ["LHA.DE", "EZJ.L", "IAG.L", "ADP.PA"]:
        b_ = r(dr).shift(1)
        row = []
        for tg, ct in [("gap", xd.gap), ("intra", xd.intra)]:
            for lab, (s, e) in [("tam", ("2014-01-01", None)), ("IS", ("2014-01-01", "2020-12-31")), ("OOS", ("2021-01-01", None))]:
                pc, n, _ = V.pcorr(d[tg], b_, [ct, r(st).shift(1), xu.shift(1)], s, e)
                row.append(f"{tg}-{lab}={pc:.3f}")
        tnw = V.pc_nwt(d.intra, b_, [xd.intra, r(st).shift(1), xu.shift(1)], "2014-01-01")
        P(f"  {st} <- {dr}(t-1): " + " ".join(row) + f" | intra NW-t={tnw:.2f}")
# Brent + STOXX kontrolü (havayolu ortak faktörü petrol mü?)
P("\n== A1/A3 senkron pc: XU100+USDTRY+EEM+STOXX+Brent kontrollü (2010+), IS/OOS")
for st, dr in [("THYAO.IS", "LHA.DE"), ("THYAO.IS", "EZJ.L"), ("THYAO.IS", "IAG.L"), ("PGSUS.IS", "EZJ.L"), ("TAVHL.IS", "ADP.PA")]:
    c5 = [xu, fx, eem, sx, bz]
    o = {k: V.pcorr(r(st), r(dr), c5, s, e)[0] for k, (s, e) in V.PER.items()}
    P(f"  {st}~{dr}: tam={o['tam']:.3f} IS={o['IS']:.3f} OOS={o['OOS']:.3f} 1y={o['1y']:.3f}")
# (3) yarıyıllık kırılım M3 / E4
P("\n== M3/E4 gece hareketi -> gap: yarıyıllık corr ve pc|XU100 gap")
for st, dr in [("TRALT.IS", "GC=F"), ("TRMET.IS", "GC=F"), ("TUPRS.IS", "BZ=F")]:
    Wd = windows(dr); d = V.dec(st)
    x = pd.concat([d.gap.rename("g"), d.intra.rename("i"), xd.gap.rename("xg"), Wd.on07, Wd.sess], axis=1, sort=True).dropna(); x = x[x.index >= "2024-06-12"]
    g = x.groupby([x.index.year, (x.index.month - 1) // 6])
    tab = g.apply(lambda q: pd.Series({"n": len(q), "c_gap": q.g.corr(q.on07), "pc_gap": V.pcorr(q.g, q.on07, [q.xg], minn=20)[0], "c_intra": q.i.corr(q.on07), "sd_gece_bps": 1e4 * q.on07.std()}))
    P(f"-- {st} ~ {dr}\n" + tab.round(3).to_string())
open(f"{RES}/s4_extra.txt", "w").write("\n".join(out))
