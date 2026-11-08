"""Denetim: S1'in uygulama düzeltmeli (giriş fiyatı cezası) sayıları.
Cezalar d2/d3'ten: AH (kapanış sonrası ~17:00 ET) girişi +6 bp; AH + makas varsayımı +11 bp; kapanış öncesi (15:30-15:55)
giriş ~+19 bp (saatlik testte A-B brüt farkı 18.6 bp; 5 dk örnekte 15:45-15:55 fiyatı kapanışın 16-22 bp üstünde).
Ayrıca oynaklıkla ölçeklenmiş ceza: 18.6 bp * (vol20_t / saatlik penceredeki sinyal günü ort vol20).
python3 -I kod/denetim_sektor_tematik/d6_duzeltilmis.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *

pd.set_option("display.width", 250)
smh = D("SMH"); sig = my_ibs(smh) < 0.2
vol20 = np.log(smh["c"]).diff().rolling(20).std()
out = []
for pos in (1000, 2500, 10000):
    base = sim(smh, sig, 1, "C0", cost("SMH", pos))
    vw = vol20.reindex(base.sig_date).values
    ref = np.nanmean(vol20.reindex(base.sig_date[base.sig_date >= "2023-12-11"]).values)
    for nm, pen in (("backtest (resmi kapanis)", 0.0), ("AH girisi +6 bp", 6.0), ("AH + makas +11 bp", 11.0), ("kapanis oncesi +19 bp", 19.0),
                    ("kapanis oncesi, oynaklikla olcekli", None)):
        tr = base.copy()
        p = (18.6 * vw / ref) if pen is None else np.full(len(tr), pen)
        p = np.where(np.isfinite(p), p, 18.6)
        tr["gross"] = tr["gross"] - p / 1e4; tr["net"] = tr["net"] - p / 1e4
        s = st(tr)
        out.append({"poz": pos, "senaryo": nm, "ort_ceza_bp": float(np.nanmean(p)), "n": s["n"], "net_bp": s["net_bp"], "t": s["t"],
                    "is_net": s["is_net_bp"], "oos_net": s["oos_net_bp"], "is_t": s["is_t"], "oos_t": s["oos_t"], "yil_poz": s["yil_poz"],
                    "pf": s["pf"], "maxdd": s["maxdd"]})
R = pd.DataFrame(out); print(R.round(2).to_string())
R.to_csv(os.path.join(OUT, "d6_duzeltilmis.csv"), index=False)
# tut kuralı + AH cezası
th = sim_hold(smh, sig, cost("SMH"))
for pen in (0, 6, 11):
    t2 = th.copy(); t2["net"] -= pen / 1e4; s = st(t2)
    print(f"TUT kuralı, ceza {pen} bp: n={s['n']} net={s['net_bp']:.1f} t={s['t']:.2f} IS={s['is_net_bp']:.1f} OOS={s['oos_net_bp']:.1f} yıl+={s['yil_poz']:.2f}")
