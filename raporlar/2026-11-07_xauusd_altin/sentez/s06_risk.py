"""s06: (7) Risk ve boyut. 1/3/5 günlük VaR ve ES (2026 rejimi ve 2017–2026), ±%10 fiyat limiti, ~%10 teminat;
stop kullanımı için veri temelli test: büyük (2σ) günlerden sonra devam mı dönüş mü; uzun pozisyonda 2σ ters günden sonra çıkma kuralı."""
import json, numpy as np, pandas as pd
from sl import *
OUT = f"{S}/out/sentez"
pd.set_option("display.width", 220)
R = {"VIOP_F_XAUUSD": RV.dropna(), "GLD": ret_of("GLD").dropna(), "GDX": ret_of("GDX").dropna(), "GDXJ": ret_of("GDXJ").dropna(), "NUGT": ret_of("NUGT").dropna()}
rows = []
for nm, r in R.items():
    rs = np.expm1(r)
    for per, a in [("2026", "2026-01-01"), ("2017-2026", "2017-03-01"), ("2008-2026", "2008-01-01")]:
        if nm == "VIOP_F_XAUUSD" and per == "2008-2026": continue
        x = r[r.index >= a]
        for h in (1, 3, 5):
            sh = x.rolling(h).sum().dropna()  # örtüşen h günlük log getiri
            loss = -np.expm1(sh)
            sig = x.std() * np.sqrt(h)
            rows.append(dict(arac=nm, donem=per, h=h, n=len(sh), vol_yillik_pct=round(x.std() * np.sqrt(252) * 100, 1),
                             VaR95_tarihsel_pct=round(np.percentile(loss, 95) * 100, 2), VaR99_tarihsel_pct=round(np.percentile(loss, 99) * 100, 2),
                             ES975_pct=round(loss[loss >= np.percentile(loss, 97.5)].mean() * 100, 2),
                             VaR99_normal_pct=round(2.326 * sig * 100, 2), en_kotu_pct=round(loss.max() * 100, 2), en_iyi_pct=round(-loss.min() * 100, 2)))
VaR = pd.DataFrame(rows); VaR.to_csv(f"{OUT}/risk_var.csv", index=False); print(VaR.to_string())
# 2026 rejimi parametrik (yıllık %29)
par = {h: round(2.326 * 0.29 * np.sqrt(h / 252) * 100, 2) for h in (1, 3, 5)}
par95 = {h: round(1.645 * 0.29 * np.sqrt(h / 252) * 100, 2) for h in (1, 3, 5)}
print("Parametrik %29 yıllık: VaR99", par, "VaR95", par95)
# fiyat limiti: VİOP günlük |getiri| dağılımı
r = RV.dropna(); a = r.abs()
lim = dict(gun=len(r), en_buyuk_dusus_pct=round(float(np.expm1(r.min()) * 100), 2), tarih_dusus=str(r.idxmin().date()), en_buyuk_artis_pct=round(float(np.expm1(r.max()) * 100), 2), tarih_artis=str(r.idxmax().date()),
           gun_abs_gt3=int((a > 0.03).sum()), gun_abs_gt5=int((a > 0.05).sum()), gun_abs_gt7=int((a > 0.07).sum()), gun_abs_gt9=int((a > 0.09).sum()),
           gun_abs_gt3_2026=int((a[a.index >= "2026-01-01"] > 0.03).sum()), gun_abs_gt5_2026=int((a[a.index >= "2026-01-01"] > 0.05).sum()))
# spot (2010–2026) 15:00→15:00 en uç günler
sr = np.log(SP.s_p15).diff().dropna()
lim.update(spot_en_buyuk_dusus_pct=round(float(np.expm1(sr.min()) * 100), 2), spot_tarih=str(sr.idxmin().date()), spot_gun_abs_gt5=int((sr.abs() > 0.05).sum()), spot_gun_abs_gt9=int((sr.abs() > 0.09).sum()))
print(lim)
# teminat: PSR %10 → 1 sözleşme (1 ons) başlangıç teminatı; kaldıraç L = nominal/özsermaye için 99% kayıp
v26 = VaR[(VaR.arac == "VIOP_F_XAUUSD") & (VaR.donem == "2026")].set_index("h")
v17 = VaR[(VaR.arac == "VIOP_F_XAUUSD") & (VaR.donem == "2017-2026")].set_index("h")
tem = []
for L in (1, 2, 3, 5, 10):
    tem.append(dict(kaldirac=L, ozsermaye_pay_teminat_pct=round(10 * L, 0),
                    kayip99_1g_2026_pct=round(L * v26.loc[1, "VaR99_tarihsel_pct"], 1), kayip99_5g_2026_pct=round(L * v26.loc[5, "VaR99_tarihsel_pct"], 1),
                    enkotu5g_2026_pct=round(L * v26.loc[5, "en_kotu_pct"], 1), kayip99_5g_2017_pct=round(L * v17.loc[5, "VaR99_tarihsel_pct"], 1)))
TEM = pd.DataFrame(tem); TEM.to_csv(f"{OUT}/risk_teminat.csv", index=False); print(TEM.to_string())

# ---- stop testleri
def cond_after_big(r, k=2.0, hs=(1, 3, 5), win=20, start=None):
    r = r.dropna(); sd = r.rolling(win).std().shift(1); z = r / sd
    out = {}
    for side, m in [("yukari_2s", z > k), ("asagi_2s", z < -k)]:
        for h in hs:
            f = sum(r.shift(-j) for j in range(1, h + 1))
            x = f[m]; x = x[x.index >= start] if start else x
            out[f"{side}_h{h}_bps"] = round(float(x.mean() * 1e4), 1); out[f"{side}_h{h}_n"] = int(x.notna().sum())
            out[f"{side}_h{h}_t"] = round(float(x.mean() / (x.std() / np.sqrt(max(1, x.notna().sum() / h)))), 2) if x.notna().sum() > 5 else np.nan
    # koşulsuz ortalama
    for h in hs:
        f = sum(r.shift(-j) for j in range(1, h + 1)); f = f[f.index >= start] if start else f
        out[f"kosulsuz_h{h}_bps"] = round(float(f.mean() * 1e4), 1)
    return out
ST = {}
ST["VIOP_2017_2026"] = cond_after_big(RV)
ST["spot_2010_2026"] = cond_after_big(np.log(SP.s_p15).diff())
ST["spot_2010_2016"] = cond_after_big(np.log(SP.s_p15).diff()[:"2016-12-31"])
ST["GDX_2008_2026"] = cond_after_big(ret_of("GDX")); ST["GDXJ_2010_2026"] = cond_after_big(ret_of("GDXJ"))
ST["GLD_2008_2026"] = cond_after_big(ret_of("GLD"))
print(json.dumps(ST, indent=1))
# uzun pozisyonda stop: 2σ ters (aşağı) günün ardından k gün nakitte bekle; B&H ile karşılaştır (basit getiri, 5 bps / 10 bps)
def stop_overlay(r, k=2.0, wait=1, cost=5.0, win=20):
    r = r.dropna(); sd = r.rolling(win).std().shift(1); z = r / sd
    out_flag = pd.Series(0.0, index=r.index)
    for j in range(wait): out_flag = np.maximum(out_flag, (z < -k).shift(j).fillna(False).astype(float))
    pos = 1 - out_flag  # gün t kapanışında karar: z_t< -k ise sonraki 'wait' gün nakit
    n, t = bt_eff(pos, r, cost); bh, _ = bt_eff(pd.Series(1.0, index=r.index), r, 0)
    return dict(stop_sharpe=per_stats(n)["sharpe"], stop_yillik=per_stats(n)["ann_pct"], bh_sharpe=per_stats(bh)["sharpe"], bh_yillik=per_stats(bh)["ann_pct"], nakit_gun_pay=round(float(out_flag.mean()), 3),
                fark_yillik_pct=round(per_stats(n)["ann_pct"] - per_stats(bh)["ann_pct"], 2))
SO = []
for nm, r_, c in [("VIOP", RV, 5.0), ("spot2010", np.log(SP.s_p15).diff(), 5.0), ("GLD", ret_of("GLD"), 10.0), ("GDX", ret_of("GDX"), 10.0), ("GDXJ", ret_of("GDXJ"), 10.0)]:
    for k in (2.0, 3.0):
        for w in (1, 3, 5):
            SO.append(dict(arac=nm, esik_sigma=k, nakit_gun=w, **stop_overlay(r_, k, w, c)))
SO = pd.DataFrame(SO); SO.to_csv(f"{OUT}/risk_stop.csv", index=False); print(SO.to_string())
# sinyal pozisyonu içinde stop: aktif sinyal günü ters yönde 2σ hareket olursa kalan dilimleri kapat → basit yaklaşım: sonraki gün pozisyonu 0
VR = pd.read_parquet(f"{OUT}/sinyal_viop_ham.parquet")
SS = []
z = RV / RV.rolling(20).std().shift(1)
for kk, h in {"V_LOWMOM_h1": 1, "V_GDXJRES_h3": 3, "V_LAST1H_h5": 5}.items():
    eff = eff_of(VR[kk], h)
    adverse = (np.sign(eff.shift(1)) * z < -2.0)  # dün taşınan pozisyon bugün 2σ ters
    eff_s = eff.where(~adverse, 0.0)
    n0, _ = bt_eff(eff, RV.dropna(), 5.0); n1, _ = bt_eff(eff_s, RV.dropna(), 5.0)
    SS.append(dict(sinyal=kk, stopsuz_sharpe=per_stats(n0)["sharpe"], stoplu_sharpe=per_stats(n1)["sharpe"], stopsuz_yillik=per_stats(n0)["ann_pct"], stoplu_yillik=per_stats(n1)["ann_pct"], stop_gun=int(adverse.sum())))
SS = pd.DataFrame(SS); SS.to_csv(f"{OUT}/risk_stop_sinyal.csv", index=False); print(SS.to_string())
json.dump(dict(limit=lim, parametrik_VaR99_29=par, parametrik_VaR95_29=par95, kosullu=ST), open(f"{OUT}/risk_ozet.json", "w"), indent=1, ensure_ascii=False)
