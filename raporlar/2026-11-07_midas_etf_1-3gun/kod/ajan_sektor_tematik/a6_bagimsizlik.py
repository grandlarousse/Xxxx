"""MR_ibs_lt01_dusus (C1, h=3) '34 sektörün 33'ünde pozitif' iddiasının bağımsız kanıt sayısı.
(1) 34 sektör ETF'i ve 37 küme temsilcisi için günlük getiri korelasyon matrisinden etkin N=(Σλ)²/Σλ².
(2) Sektör sinyal günlerinin SPY'ın aynı sinyaliyle aynı güne düşme oranı.
(3) Havuz: işlem ortalaması, hafta/ay kümeli t, SPY beta-hedge'li kenar.
Çıktı: sonuclar/aile_sektor_tematik/bagimsizlik.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *
import universe
SECT = universe.U["sektor"]
out = []
for nm, uni in (("sektor34", SECT), ("kume_temsilci37", REPS)):
    ne, nd = neff_from_corr(uni)
    spy = D("SPY"); ss = (lib.ibs(spy) < 0.1) & (spy.c < spy.c.shift(1))
    co = []; trs = []
    for s in uni:
        df = D(s); sg = (lib.ibs(df) < 0.1) & (df.c < df.c.shift(1)); sg.iloc[:200] = False
        co.append(float((sg & ss.reindex(df.index).fillna(False)).sum() / max(1, sg.sum())))
        trs.append(run_sym(s, sg, 3, "C1"))
    tr = pd.concat(trs, ignore_index=True); r = summarize(tr, nm)
    ps = tr.groupby("sym")["net"].mean()
    out.append({"evren": nm, "etf_sayisi": len(uni), "etkin_N_getiri_korelasyonu": ne, "gun": nd,
                "pozitif_etf": int((ps > 0).sum()), "spy_sinyaliyle_ayni_gun_orani": np.mean(co),
                "havuz_net_bp": r["mean_net_bp"], "t_naive": r["t_naive"], "t_hafta_kumeli": r["t_cl"], "t_ay_kumeli": r["t_cl_ay"],
                "is_net_bp": r["is_net_bp"], "oos_net_bp": r["oos_net_bp"], "spy_hedge_bp": r["mean_hedged_bp"], "t_hedge": r["t_hedged_cl"]})
o = pd.DataFrame(out); o.to_csv(os.path.join(OUT, "bagimsizlik.csv"), index=False)
pd.set_option("display.width", 250); print(o.round(2).T.to_string())
