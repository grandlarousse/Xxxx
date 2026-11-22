"""MU -> WDC kuralı (yalnız AL, korumasız, 3 gün) için kontrol göstergeleri: önceden yazılı 14 süzgecin iki yanı.
Çıktı: ek/backtest/cift/mu_wdc_suzgec.csv. Uyarı: 28 kesit; birkaçı şansla anlamlı görünür. IS ve OOS'ta aynı yönde olanlara bak."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

H = 3
spy = o.hizali_getiri("SPY", bilinen=False)
def artik_z(sym, fak=spy):
    x = o.hizali_getiri(sym, bilinen=False)
    return o.zskor(x - o.kayan_beta(x, fak) * fak, 60), x
zmu, rmu = artik_z("MU")
taban = (zmu >= 1).astype(float)
c = o.panel("adjclose"); cl = o.panel("close"); hi = o.panel("high"); lo = o.panel("low")
sma = lambda s, n: c[s].rolling(n, min_periods=n).mean()
vix = cl["^VIX"]
zwdc, rwdc = artik_z("WDC"); zstx, _ = artik_z("STX")
smh = o.hizali_getiri("SMH", bilinen=False)
zmu_smh = o.zskor(rmu - o.kayan_beta(rmu, smh) * smh, 60)
hynix = o.hizali_getiri("000660.KS")
ibs_wdc = (cl["WDC"] - lo["WDC"]) / (hi["WDC"] - lo["WDC"])
# MU bilanço tepki günleri (takvim tarihi ve sonraki işlem günü)
bt = pd.read_csv(os.path.join(o.VERI, "bilanco_takvimi.csv")); bt = pd.to_datetime(bt[bt.sembol == "MU"].tarih)
tk = c.index; bil = pd.Series(False, index=tk)
for d in bt:
    i = tk.searchsorted(d)
    for j in (i, i + 1):
        if j < len(tk): bil.iloc[j] = True

SUZGEC = {
 "SMH 50 gün ort. üstünde": c["SMH"] > sma("SMH", 50),
 "SMH 200 gün ort. üstünde": c["SMH"] > sma("SMH", 200),
 "QQQ 200 gün ort. üstünde": c["QQQ"] > sma("QQQ", 200),
 "WDC 50 gün ort. üstünde": c["WDC"] > sma("WDC", 50),
 "VIX <= 20": vix <= 20,
 "MU o gün yükseldi (ham getiri > 0)": rmu > 0,
 "SPY o gün yükseldi": spy > 0,
 "MU sinyali güçlü (z >= 1,5)": zmu >= 1.5,
 "MU'ya özgü (SMH'den arındırılmış z >= 1)": zmu_smh >= 1,
 "WDC o gün zaten sıçradı (artık z >= 1)": zwdc >= 1,
 "WDC günün zirvesine yakın kapandı (IBS >= 0,8)": ibs_wdc >= 0.8,
 "STX o gün piyasadan güçlü (artık z > 0)": zstx > 0,
 "SK Hynix o gün yükseldi": hynix > 0,
 "MU bilanço tepki günü": bil,
}
def satir(ad, sig):
    d = o.donemli_test(sig, "WDC", H)
    return dict(kesit=ad, n=d.get("tum_n"), net_bps=d.get("tum_net_bps"), anormal_bps=d.get("tum_anormal_net_bps"), isabet=d.get("tum_isabet"),
                t_is=d.get("is_t_anormal"), t_oos=d.get("oos_t_anormal"), is_bps=d.get("is_anormal_net_bps"), oos_bps=d.get("oos_anormal_net_bps"),
                son_n=d.get("son_n"), son_net=d.get("son_net_bps"))
rows = [satir("TABAN: MU artık z >= 1 -> WDC AL, 3 gün", taban)]
for ad, m in SUZGEC.items():
    m = m.reindex(taban.index).fillna(False).astype(bool)
    rows.append(satir("EVET | " + ad, taban.where(m, 0.0)))
    rows.append(satir("HAYIR | " + ad, taban.where(~m, 0.0)))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(o.KOK, "ek", "backtest", "cift", "mu_wdc_suzgec.csv"), index=False)
pd.set_option("display.width", 250)
print(df.to_string(index=False))

# ---- Birleşik kesitler (22.11.2026): A = MU o gün yükseldi ve bilanço tepki günü değil; B = A + SPY o gün düştü; C = A + SPY yükseldi
temiz = taban.where((rmu > 0) & (~bil), 0.0)
ek = [satir("A: MU yükseldi + bilanço günü değil", temiz), satir("B: A + SPY o gün düştü", temiz.where(spy < 0, 0.0)),
      satir("C: A + SPY o gün yükseldi", temiz.where(spy >= 0, 0.0)),
      satir("KIYAS: SPY düştü, MU sinyali yok -> WDC al", ((spy < 0) & (taban == 0)).astype(float)),
      satir("KIYAS: SPY düştü, MU yükseldi ama z < 1", ((spy < 0) & (rmu > 0) & (zmu < 1)).astype(float))]
pd.DataFrame(ek).to_csv(os.path.join(o.KOK, "ek", "backtest", "cift", "mu_wdc_birlesik.csv"), index=False)
print(pd.DataFrame(ek).to_string(index=False))
