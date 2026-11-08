"""Hakem: C3 (gram prim dönüşü) — roll/ay değişimi, vade sonu yakınsaması, bayat (düşük hacimli) uzlaşma, uç değer, işlem edilebilirlik."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
import numpy as np, pandas as pd
import lib_altin as L
pd.set_option("display.width", 250)
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
p = L.load_viop(); isx = p.index <= L.IS_END
pr = p.tr_prem_matched; ym = p.tr_prem_ym
dev = pr - pr.rolling(60, min_periods=20).mean()
x = dev.shift(1)

# matched kontratların hacimleri ve vadeye kalan gün
Lg = pd.read_parquet(f"{S}/panel/viop_long.parquet")
Lg["ym"] = Lg["expiry"].dt.to_period("M").astype(str)
def leg(root, nm):
    d = Lg[Lg.root == root][["date", "ym", "settle", "volume", "expiry", "vwap", "trades"]].copy()
    d.columns = ["date", "ym", f"{nm}_s", f"{nm}_v", f"{nm}_exp", f"{nm}_vwap", f"{nm}_tr"]
    return d
m = leg("XAUTRYM", "g").merge(leg("XAUUSD", "x"), on=["date", "ym"]).merge(leg("USDTRY", "u"), on=["date", "ym"])
m["date"] = pd.to_datetime(m["date"])
key = pd.DataFrame({"date": p.index, "ym": ym.values})
mm = key.merge(m, on=["date", "ym"], how="left").set_index("date")
dte_m = (mm.g_exp - mm.index.to_series()).dt.days
print("matched ay ile gram hacmi=0 olan gün sayısı:", int((mm.g_v == 0).sum()), " ons hacmi=0:", int((mm.x_v == 0).sum()), " usdtry hacmi=0:", int((mm.u_v == 0).sum()), " toplam", len(mm))
print("gram matched hacim dağılımı (kontrat):", mm.g_v.describe().round(0).to_dict())
print("ons matched hacim dağılımı:", mm.x_v.describe().round(0).to_dict())
# matched ay aktif (en yüksek OI) kontrat mı?
print("matched ons kontratı aktif ons kontratıyla aynı ay mı:", round((pd.to_datetime(p.v_expiry).dt.to_period('M').astype(str) == ym).mean(), 3))

def rep(lab, mask, h=3):
    y = pr.shift(-h) - pr
    q = L.ic(x[mask], y[mask], max(h, 5))
    qi = L.ic(x[mask & isx], y[mask & isx], max(h, 5)); qo = L.ic(x[mask & ~isx], y[mask & ~isx], max(h, 5))
    print(f"  {lab:48s} h={h}: IC {q['ic']:+.3f} t {q['t']:+.2f} n {q['n']} | IS t {qi['t']:+.2f} | OOS t {qo['t']:+.2f}")

all_ = pd.Series(True, index=p.index)
print("\n=== C3 yeniden üretim ve dışlamalar ===")
for h in (1, 3, 5):
    rep("tam", all_, h)
# matched ayın t-1..t+h içinde değişmediği pencereler
for h in (3, 5):
    same = pd.Series(True, index=p.index)
    for k in range(-1, h + 1):
        same &= (ym.shift(-k) == ym)
    rep("matched ay t-1..t+h sabit", same, h)
    rep("matched vade >h+5 gün", dte_m > h + 7, h)
    rep("tüm bacak hacmi > 0 (t-1, t, t+h)", (mm.g_v > 0) & (mm.g_v.shift(1) > 0) & (mm.g_v.shift(-h) > 0) & (mm.x_v > 0) & (mm.x_v.shift(1) > 0), h)
    hv = mm.g_v > mm.g_v.rolling(250, min_periods=50).median()
    rep("gram hacmi (t-1) medyan üstü", hv.shift(1, fill_value=False), h)
    rep("gram hacmi (t-1) medyan altı", ~hv.shift(1, fill_value=True), h)
    rep("|prem|<1% ve |dev|<50bps", (pr.abs() < 0.01) & (dev.abs().shift(1) < 0.005), h)
    rep("2018-08..09 ve 2022-05 hariç", ~(((p.index >= "2018-08-01") & (p.index <= "2018-09-30")) | ((p.index >= "2022-05-15") & (p.index <= "2022-06-15"))), h)
    for a, b in [("2017", "2019"), ("2020", "2021"), ("2022", "2023"), ("2024", "2026")]:
        rep(f"alt dönem {a}-{b}", (p.index.year >= int(a)) & (p.index.year <= int(b)), h)
# Bayat fiyat testi: gecikme boşluğu büyüdükçe (dev(t-k), k=1..5) IC nasıl azalıyor
print("\n  dev(t-k) -> Δprem(t→t+3) (bayat/ölçüm hatası gürültüsü daha uzun boşlukta söner mi?):")
for k in (1, 2, 3, 5, 10):
    y = pr.shift(-3) - pr; q = L.ic(dev.shift(k), y, 5)
    print(f"    k={k}: IC {q['ic']:+.3f} t {q['t']:+.2f}")
# Δprem otokorelasyonu (ölçüm gürültüsü imzası: -0.5'e yakın lag1 otokor)
dp = pr.diff()
print("  Δprem otokorelasyon lag1..5:", [round(dp.autocorr(k), 3) for k in range(1, 6)])
# Uzlaşma yerine VWAP ile prim (farklı fiyat ölçüsü): VWAP'la kurulan prim de dönüyor mu?
prv = np.log(mm.g_vwap) - np.log(mm.x_vwap * mm.u_vwap / 31.1035)
prv = prv.where((mm.g_vwap > 0) & (mm.x_vwap > 0) & (mm.u_vwap > 0))
devv = prv - prv.rolling(60, min_periods=20).mean()
for h in (3, 5):
    # sinyal VWAP primi, hedef uzlaşma primi değişimi (ölçüm hatası çapraz)
    q = L.ic(devv.shift(1), pr.shift(-h) - pr, max(h, 5)); q2 = L.ic(devv.shift(1), prv.shift(-h) - prv, max(h, 5))
    print(f"  VWAP-prim dev(t-1) -> uzlaşma Δprem h={h}: IC {q['ic']:+.3f} t {q['t']:+.2f} | -> VWAP Δprem: IC {q2['ic']:+.3f} t {q2['t']:+.2f}")
print("  corr(prem uzlaşma, prem VWAP):", round(pr.corr(prv), 3), " corr(Δ):", round(pr.diff().corr(prv.diff()), 3))
# Vade sonu yakınsama: matched vadeye kalan gün gruplarına göre ortalama |prem|
print("\n  ortalama |prem| (bps) vadeye kalan güne göre:")
gr = pd.cut(dte_m, [-1, 0, 3, 7, 15, 30, 60, 400])
print((pr.abs() * 1e4).groupby(gr).agg(["mean", "count"]).round(1).to_string())

# İşlem: 3 bacak getirisiyle, maliyet duyarlılığı
print("\n=== C3 işlem (t-1 ve K), bacak başına 0/2/5/10 bps ===")
res = (p.vo_xautry_ret - p.v_ret - p.vo_usdtry_ret).fillna(0)
z = (pr - pr.rolling(60, min_periods=20).mean()) / pr.rolling(60, min_periods=20).std()
for lab, zz in [("t-1", z.shift(1)), ("K", z)]:
    for k in (1.0, 1.5, 2.0):
        pos = -(zz > k).astype(float) + (zz < -k).astype(float)
        for h in (3, 5):
            out = []
            for c in (0, 6, 15, 30):
                a = L.backtest(pos, res, h, c); ao = L.backtest(pos[~isx], res[~isx], h, c)
                out.append(f"{c}bps: {a['sharpe']:+.2f}/{ao['sharpe']:+.2f}")
            print(f"  {lab} k={k} h={h}: tam/OOS Sharpe  " + "  ".join(out))
# bacak getirisi kalıntısı vs Δprem
print("  corr(res, Δprem)=", round(res.corr(pr.diff()), 3), " res std bps", round(res.std() * 1e4, 1), " Δprem std bps", round(pr.diff().std() * 1e4, 1))
