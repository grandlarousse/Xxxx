"""(5) Güncel durum — bağımsız hesap (dlib + taze Yahoo 5 dk GCZ26.CMX)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/altin/denetim/kod")
import numpy as np, pandas as pd, dlib
c = dlib.cal(); gV, sdV, zV = dlib.viop_gold_z()
r18 = dlib.chg(dlib.snap("GC=F", "h1", 15, 0)); sd18 = r18.rolling(250, min_periods=100).std()
p1755 = dlib.snap("GCZ26.CMX", "m5", 14, 55, max_age_min=30)
now = pd.Timestamp.now(tz="UTC").tz_localize(None); today = pd.Timestamp("2026-11-04")
d5, _ = dlib.intraday("GCZ26.CMX", "m5"); last_t = (d5.index[-1] + pd.Timedelta(minutes=5)).tz_convert(None); live = float(d5["c"].iloc[-1])
sig_today = float(sd18.loc[c[-1]])          # bugün için σ = 03.11 dahil son 250 gün (bugün hariç)
ref = float(p1755.loc[c[-1]])
# arife kontrolü: önceki gün yarım gün mü? (03.11 değil)
print(f"çalışma {now:%Y-%m-%d %H:%M} UTC; son 5 dk bar bitişi {last_t:%H:%M} UTC, fiyat {live:.1f}")
for d in c[-4:]:
    print(f"  {d.date()}: VİOP g {gV[d]*100:+.2f}% σ {sdV[d]*100:.2f}% z {zV[d]:+.2f} | 17:55 GCZ26 {p1755[d]:.1f} | 18:00 z {(r18[d]/r18.rolling(250,min_periods=100).std().shift(1)[d]):+.2f}")
g = np.log(live / ref); z = g / sig_today
print(f"BUGÜN geçici: ref 03.11 17:55 = {ref:.1f}; g {g*100:+.2f}%; σ(betik tanımı) {sig_today*100:.2f}% -> z {z:+.2f}; VİOP σ ile z {g/float(gV.rolling(250,min_periods=100).std().iloc[-1]):+.2f}")
print(f"BUGÜN tetik (COMEX Ara): AL >= {ref*np.exp(sig_today):.1f} / SAT <= {ref*np.exp(-sig_today):.1f}  (yüzde: ±{sig_today*100:.2f}%)")
print(f"YARIN yaklaşık tetik (bugünkü fiyat referans): {live*np.exp(sig_today):.1f} / {live*np.exp(-sig_today):.1f}")
fT = dlib.front("TRALT"); fX = dlib.front("XU030"); bS = dlib.spot_beta(upto=c[-1]).loc[c[-1]]
bS_next = dlib.spot_beta()  # bugün için β: 03.11 dahil (shift sonrası 04.11 değeri yok çünkü takvim 03.11'de bitiyor)
ra = np.log(dlib.ydaily("TRALT.IS")["adj"]).diff(); rb = np.log(dlib.ydaily("XU030.IS")["adj"]).diff()
ra = ra[ra.index <= c[-1]].reindex(c); rb = rb[rb.index <= c[-1]].reindex(c); m = ra.notna() & rb.notna()
b_today = float((ra.where(m).rolling(250, min_periods=100).cov(rb.where(m)) / rb.where(m).rolling(250, min_periods=100).var()).iloc[-1])
pT, pX = fT.loc[c[-1], "settle"], fX.loc[c[-1], "settle"]
print(f"β(03.11'e kadar; 04.11 işlemi için) {b_today:.3f}; 03.11 uzlaşma {fT.loc[c[-1],'code']} {pT} / {fX.loc[c[-1],'code']} {pX} -> N = {10*pX/(b_today*100*pT):.2f} -> {round(10*pX/(b_today*100*pT))}")
td = dlib.ydaily("TRALT.IS"); xd = dlib.ydaily("XU030.IS")
print("Yahoo bugün TRALT.IS", td.index[-1].date(), td["c"].iloc[-1], f"({(td['c'].iloc[-1]/td['c'].iloc[-2]-1)*100:+.1f}%)", "XU030.IS", xd["c"].iloc[-1])
for pTl in (td["c"].iloc[-1] * 1.0, ):
    print(f"  güncel spotla N ≈ {10*xd['c'].iloc[-1]/(b_today*100*pTl):.1f}")
