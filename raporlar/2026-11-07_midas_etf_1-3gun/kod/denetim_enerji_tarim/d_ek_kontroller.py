"""Denetim ek kontroller: UCO kendi bandı (ajanın aile tablosunda yok), XOP ufuk duyarlılığı, UCO kaldıraç geçmişi,
yakın S1 uygulama tarihleri (takvim + NYSE erken kapanış), S2 güncel durum.
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_ek_kontroller.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D, lib
from d_s2_uso_bb import bb_sig

pd.set_option("display.width", 250)
uso = lib.load("USO"); sig = bb_sig(uso)
# UCO kendi bandı
uco = lib.load("UCO"); su = bb_sig(uco)
for mode in ("C0", "O1", "C1"):
    for h in (1, 2, 3):
        s = D.st(D.sim(uco, su, h, mode), D.cost("UCO"))
        print(f"UCO kendi bandı {mode} h{h}: n={s['n']} net={s['net_bp']:.0f} t={s['t']:.2f} IS={s['is_net_bp']:.0f} ({s['is_t']:.2f}) OOS={s['oos_net_bp']:.0f} ({s['oos_t']:.2f})")
tr = D.sim(uco, su, 2, "C1"); cu = D.cost("UCO")
print("UCO kendi bandı C1 h2 yıl yıl:", D.yearly(tr, cu)["ort_bp"].round(0).to_dict())
print("  en iyi 5:", tr.nlargest(5, "brut")[["giris", "cikis", "brut"]].assign(brut=lambda x: (x.brut * 1e4).round(0)).to_dict("records"))
for lab, m in (("2020 hariç", tr["sig"].dt.year != 2020), ("en iyi 5 hariç", ~tr.index.isin(tr["brut"].nlargest(5).index))):
    s = D.st(tr[m.to_numpy() if hasattr(m, 'to_numpy') else m].reset_index(drop=True), cu); print(f"  {lab}: n={s['n']} net={s['net_bp']:.0f} t={s['t']:.2f}")
# Sinyal günleri ne kadar örtüşüyor?
s_u = pd.Series(sig, index=uso.index); s_c = pd.Series(su, index=uco.index).reindex(uso.index).fillna(False)
print("USO ve UCO sinyal günleri: USO %d, UCO %d, ortak %d" % (s_u.sum(), s_c.sum(), (s_u & s_c).sum()))
# UCO ~ USO beta yıl yıl
r = pd.DataFrame({"u": uso["c"].pct_change(), "c": uco["c"].pct_change()}).dropna()
print("UCO~USO yıllık beta:", r.groupby(r.index.year).apply(lambda g: np.polyfit(g["u"], g["c"], 1)[0]).round(2).to_dict())
# XOP USO sinyaliyle ufuk/mod
xop = lib.load("XOP"); sx = pd.Series(sig, index=uso.index).reindex(xop.index).fillna(False).to_numpy()
for mode in ("C0", "O1", "C1"):
    print("XOP (USO sinyali) " + mode + ": " + " | ".join(f"h{h} net {D.st(D.sim(xop, sx, h, mode), D.cost('XOP'))['net_bp']:.0f} t {D.st(D.sim(xop, sx, h, mode), D.cost('XOP'))['t']:.2f}" for h in (1, 2, 3)))
# S2 güncel durum
c = uso["raw_c"]; m = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=1)
print("USO son 3 gün: ", pd.DataFrame({"kapanis": c, "alt_bant": m - 2 * sd}).tail(3).round(2).to_dict("index"))
# S1 yakın tarihler
ev = pd.read_csv(os.path.join(lib.ROOT, "data", "events", "eia_ng_storage.csv"), parse_dates=["date"])
fut = ev[(ev["date"] >= "2026-11-07") & (ev["date"] <= "2027-01-15")][["date", "detail", "source"]]
print("EIA NG takvimi (yakın):"); print(fut.to_string(index=False))
ny = pd.read_csv(os.path.join(lib.ROOT, "data", "events", "nyse_tatil.csv"), parse_dates=["date"])
print("NYSE tatil/erken kapanış (Kas 2026-Oca 2027):"); print(ny[(ny["date"] >= "2026-11-01") & (ny["date"] <= "2027-01-31")].to_string(index=False))
