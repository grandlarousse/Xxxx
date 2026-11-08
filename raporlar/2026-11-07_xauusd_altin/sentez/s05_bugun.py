"""s05: Pazartesi 2026-11-09 için sinyal durumu (veri 2026-11-06 Cuma kapanışına kadar) + 2026 etkinliği + iki dilimli rejim tablosu."""
import json, numpy as np, pandas as pd
from sl import *
OUT = f"{S}/out/sentez"
VR = pd.read_parquet(f"{OUT}/sinyal_viop_ham.parquet"); ER = pd.read_parquet(f"{OUT}/sinyal_etf_ham.parquet")
T = pd.Timestamp("2026-11-09")
B = {}

# ---- VİOP
p, q, rvA = sig_lowmom()
lp = np.log(SP.s_p15); hist = SP.s_p15.pct_change()
rv_hist = (np.log(SP.s_p15).diff().rolling(20).std() * np.sqrt(252)).dropna()
thr = float(rv_hist.quantile(1 / 3))
x5 = float(lp.iloc[-1] - lp.iloc[-6])
B["V_LOWMOM_h1"] = dict(durum="PASİF", neden=f"rv20 (spot 15:00 UTC) = %{rvA.iloc[-1]*100:.1f}, 2010'dan beri yüzdeliği {q.iloc[-1]:.2f} ≥ 1/3; eşik ≈ %{thr*100:.1f}. 2026'da hiç tetiklenmedi (2026 en düşük rv20 %{rvA[rvA.index>='2026-01-01'].min()*100:.1f}).",
                        son_5g_spot_getiri_pct=round(x5 * 100, 2), eksik="Pazartesi 15:00 UTC spot (rv20 ve 5 günlük getiri güncellenir; rejim değişmesi için oynaklığın yarıdan fazla düşmesi gerekir)")
# QEND: bir sonraki olay
bd = pd.bdate_range("2026-12-01", "2026-12-31")
B["V_QEND_h3"] = dict(durum="PASİF", neden="Takvim: bir sonraki giriş Aralık 2026'nın sondan 2. VİOP günü = 2026-12-30 Çarşamba uzlaşması (31 Aralık işlem günü varsayımıyla), çıkış 3 VİOP günü sonra (≈2027-01-05).",
                      eksik="yok (takvim)")
# GDXJ artığı (VİOP takvimi): Pazartesi satırı = Cuma 11-06 ABD kapanışı
v2 = V[["y_GDXJ", "y_GLD"]].copy()
v2.loc[T] = [float(E.c_GDXJ.loc["2026-11-06"]), float(E.c_GLD.loc["2026-11-06"])]
rm = np.log(v2.y_GDXJ).diff(); rg = np.log(v2.y_GLD).diff()
b = rm.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
e = rm - b * rg; z = e / e.rolling(120, min_periods=60).std().shift(1)
zT = float(z.loc[T]); posT = float(np.sign(zT) if abs(zT) > 0.43 else 0.0)
prev = VR.V_GDXJRES_h3.iloc[-2:]
effT = (prev.sum() + posT) / 3
B["V_GDXJRES_h3"] = dict(durum="AKTİF" if posT != 0 else "NÖTR", yeni_dilim=posT, z=round(zT, 2), r_GDXJ_cuma_pct=round(float(rm.loc[T]) * 100, 2), r_GLD_cuma_pct=round(float(rg.loc[T]) * 100, 2),
                         beta60=round(float(b.loc[T]), 2), acik_dilimler={str(k.date()): float(v) for k, v in prev.items()}, etkin_poz_pazartesi_sonrasi=round(effT, 3),
                         eksik="yok (Cuma ABD kapanışı biliniyor)")
# LAST1H: Pazartesi 14→15 UTC bilinmiyor; açık dilimler
prev5 = VR.V_LAST1H_h5.iloc[-4:]
B["V_LAST1H_h5"] = dict(durum="KOŞULLU", kural="Pazartesi 15:00 UTC'de ln(spot15/spot14)>0 ise yeni 1/5 dilim UZUN, <0 ise KISA",
                        acik_dilimler={str(k.date()): float(v) for k, v in prev5.items()}, acik_dilim_toplami_bes_te=round(float(prev5.sum()) / 5, 2),
                        cuma_14_15_pct=round(float(np.log(V.xau_p15.iloc[-1] / V.xau_p14.iloc[-1])) * 100, 3),
                        eksik="Pazartesi 14:00 ve 15:00 UTC spot fiyatı")
# ---- ETF
ses = nyse_sessions()
pt, ev = sig_gdx_tatil()
nxt = ev[ev > pd.Timestamp("2026-11-06")][:2]
B["E_GDXTATIL_h1"] = dict(durum="PASİF", neden=f"Bir sonraki olay günü {nxt[0].date()} (Şükran Günü öncesi); giriş bir önceki kapanış {ses[ses < nxt[0]][-1].date()}, çıkış {nxt[0].date()} kapanışı.", eksik="yok (takvim)")
th = json.load(open(f"{OUT}/esikler.json"))["e2_esik"]
for key, (y, k) in {"E_C2J_h3": ("GDXJ", 1), "E_C2_h3": ("GDX", 3), "E_C1_h5": ("GDX", 10)}.items():
    eres = miner_resid(y)
    xT = float(eres.rolling(k, min_periods=k).sum().iloc[-1])  # Cuma'ya kadar → Pazartesi kararında bilinen
    hi, lo = th[key.split("_")[1]]
    pT = 1.0 if xT > hi else 0.0
    h = int(key[-1])
    prevE = ER[key].iloc[-(h - 1):] if h > 1 else ER[key].iloc[0:0]
    B[key] = dict(durum="AKTİF (UZUN)" if pT > 0 else ("NAKİT (kısa bölge)" if xT < lo else "NAKİT"), x=round(xT * 100, 3), esik_ust_pct=round(hi * 100, 3), esik_alt_pct=round(lo * 100, 3),
                  acik_dilimler={str(kk.date()): float(vv) for kk, vv in prevE.items()}, etkin_poz_pazartesi_sonrasi=round((float(prevE.clip(lower=0).sum()) + pT) / h, 3),
                  eksik="yok (Cuma ABD kapanışı biliniyor)")
xc = float(E.xau_close.loc["2026-11-06"])
B["E_M_GDXJ_h1"] = dict(durum="KOŞULLU", kural=f"Pazartesi 15:00 ET'de spot altın < Cuma 16:00 ET fiyatı ({xc:.2f} USD) ise GDXJ'yi kapanışta al, Salı kapanışında sat; değilse nakit.",
                        cuma_m_pct=round(float(np.log(E.xau_cut.iloc[-1] / E.xau_close.iloc[-2])) * 100, 2), cuma_pozisyon=float(ER.E_M_GDXJ_h1.iloc[-1]), eksik="Pazartesi 15:00 ET (20:00 UTC) spot altın")

# ---- 2026 etkinliği: aktif gün payı, 2026 YTD net getiri
VN = pd.read_parquet(f"{OUT}/pnl_viop.parquet"); EN = pd.read_parquet(f"{OUT}/pnl_etf.parquet")
A = []
for k in VR.columns:
    m = VR.index >= "2026-01-01"
    A.append(dict(sinyal=k, aktif_gun_pay_2026=round(float((VR[k][m] != 0).mean()), 2), aktif_gun_pay_tum=round(float((VR[k] != 0).mean()), 2),
                  net_2026_pct=round(float(np.expm1(0) + VN[k][VN.index >= "2026-01-01"].sum()) * 100, 2) if k in VN else np.nan))
for k in ER.columns:
    m = ER.index >= "2026-01-01"
    A.append(dict(sinyal=k, aktif_gun_pay_2026=round(float((ER[k][m] != 0).mean()), 2), aktif_gun_pay_tum=round(float((ER[k] != 0).mean()), 2),
                  net_2026_pct=round(float(EN[k][EN.index >= "2026-01-01"].sum()) * 100, 2) if k in EN else np.nan))
A = pd.DataFrame(A); A.to_csv(f"{OUT}/etkinlik_2026.csv", index=False)
# iki dilimli rejim: rv20 < %18 / ≥ %18 (tüm örneklem), PnL basit getiri
rv_v = to_viop(rvA); rv_e = rvA.reindex(E.index, method="ffill")
RG = []
for k in VN.columns:
    n = VN[k].dropna(); rg = rv_v.shift(1).reindex(n.index); hh = int(k[-1])
    act = (eff_of(VR[k], hh).shift(1).reindex(n.index) != 0)
    for nm, msk in [("rv<%18", rg < 0.18), ("rv>=%18", rg >= 0.18)]:
        x = n[msk]; na = int((act & msk).sum())
        RG.append(dict(sinyal=k, rejim=nm, gun=len(x), aktif_gun=na, sharpe=per_stats(x)["sharpe"] if na >= 30 else np.nan, yillik_pct=round(x.mean() * 252 * 100, 2)))
for k in EN.columns:
    n = EN[k].dropna(); rg = rv_e.shift(1).reindex(n.index); hh = int(k[-1])
    act = (eff_of(ER[k], hh).shift(1).reindex(n.index) != 0)
    for nm, msk in [("rv<%18", rg < 0.18), ("rv>=%18", rg >= 0.18)]:
        x = n[msk]; na = int((act & msk).sum())
        RG.append(dict(sinyal=k, rejim=nm, gun=len(x), aktif_gun=na, sharpe=per_stats(x)["sharpe"] if na >= 30 else np.nan, yillik_pct=round(x.mean() * 252 * 100, 2)))
RG = pd.DataFrame(RG); RG.to_csv(f"{OUT}/rejim_iki_dilim.csv", index=False)
pd.set_option("display.width", 200)
print(json.dumps(B, indent=1, ensure_ascii=False, default=str))
print(A.to_string()); print(RG.pivot(index="sinyal", columns="rejim", values="sharpe").to_string()); print(RG.pivot(index="sinyal", columns="rejim", values="gun").to_string())
json.dump(dict(bugun=B, lowmom_esik=thr), open(f"{OUT}/bugun_2026_11_09.json", "w"), indent=1, ensure_ascii=False, default=str)
