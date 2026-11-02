"""A5: Backtestler (look-ahead yok; IS 2014-2020 / OOS 2021-2026; maliyet 8/15 bps gidiş-dönüş, çift bacakta x2).
B1 kakao -> ULKER (günlük gün-içi, haftalık, büyük hareket)
B2 ABD risk-off (SPX_{t-1}<=-1.5% veya VIX_{t-1}>=+15%) -> defansif sepet (BIMAS,MGROS,SOKM,ULKER) long / XU030 short, açılışta gir
B2b BIST sert düşüş günü (XU100<=-3%, kapanışta bilinir) -> ertesi 5 gün defansif short / XU030 long (göreli geri verme)
B3 CCOLA -> AEFES: (i) CCOLA_{t-1} -> AEFES gün-içi; (ii) AEFES-β·CCOLA spread geri dönüşü
Çıktı: a5_backtests.csv"""
from common import *
rows = []
def rec(name, sig, tgt, cost, mode="sign", thr=0.0, legs=1, note=""):
    res, pnl = ll.backtest(sig, tgt, cost_bps=cost * legs, mode=mode, thr=thr, split=SPLIT)
    o = {"bt": name, "cost_bps_rt": cost * legs, "mode": mode, "thr": thr, "note": note}
    for k in ["IS", "OOS", "ALL"]:
        for f in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]:
            o[f"{k}_{f}"] = res[k].get(f, np.nan)
    o["by_year_bps"] = str(res["by_year_bps"]); rows.append(o); return res
X = DEC("XU100"); X30 = DEC("XU030"); xu = R("XU100")
dU = DEC("ULKER"); cc = zero_mask(R("CC=F"))
# ---- B1 kakao -> ULKER
for cost in (8, 15):
    rec("B1a kakao_{t-1} -> ULKER intra_t (short if cocoa up)", -cc.shift(1), dU["intra"], cost, note="tek bacak")
    rec("B1a' kakao_{t-1} z>1 -> ULKER intra_t", -cc.shift(1), dU["intra"], cost, mode="z", thr=1.0)
    rec("B1b kakao_{t-1} -> ULKER-XU030 intra_t (çift)", -cc.shift(1), dU["intra"] - X30["intra"], cost, legs=2)
# haftalık: kakao son 5 BIST günü toplamı (t-1'de biter) -> ULKER-XU100 göreli t..t+4 (açılıştan: intra_t + cc t+1..t+4)
ul = R("ULKER"); rel_fwd = (dU["intra"] - X["intra"]).reindex(ul.index) + sum((ul - xu).shift(-k) for k in range(1, 5))
cc5 = cc.fillna(0).rolling(5).sum().shift(1)
wk = rel_fwd.index[::5]
for cost in (8, 15):
    rec("B1c kakao 5g -> ULKER göreli 5g (haftalık, örtüşmesiz)", -cc5.reindex(wk), rel_fwd.reindex(wk), cost, legs=2)
    big = (cc.shift(1) >= np.log(1.08)).astype(float) * -1.0
    rec("B1d kakao_{t-1}>=+8% -> ULKER göreli short t..t+4", big.reindex(ul.index), rel_fwd, cost, legs=2, note="çok az olay")
# ---- B2 risk-off -> defansif rotasyon
DEF = ["BIMAS", "MGROS", "SOKM", "ULKER"]
bi = pd.concat([DEC(s)["intra"] for s in DEF], axis=1).mean(axis=1, skipna=True)
bcc = pd.concat([R(s) for s in DEF], axis=1).mean(axis=1, skipna=True)
x30 = R("XU030")
spx = zero_mask(R("^GSPC")); vix = zero_mask(R("^VIX"))
ro = ((spx.shift(1) <= np.log(0.985)) | (vix.shift(1) >= np.log(1.15))).astype(float)
tgt1 = bi - X30["intra"]
tgt5 = tgt1.reindex(bcc.index) + sum((bcc - x30).shift(-k) for k in range(1, 5))
for cost in (8, 15):
    rec("B2a ABD risk-off_{t-1} -> defansif-XU030 intra_t", ro, tgt1, cost, legs=2)
    rec("B2b ABD risk-off_{t-1} -> defansif-XU030 t..t+4 (açılıştan)", ro, tgt5, cost, legs=2, note="örtüşen pozisyon mümkün")
# B2c BIST sert düşüş (kapanışta bilinir; VİOP kapanışına yakın gir) -> t+1..t+5 göreli: defansif SHORT
sell = (xu <= np.log(0.97)).astype(float) * -1.0
fwd5 = sum((bcc - x30).shift(-k) for k in range(1, 6))
for cost in (8, 15):
    rec("B2c XU100_t<=-3% -> defansif-XU030 short t+1..t+5", sell, fwd5, cost, legs=2)
# referans: kalıcı defansif-XU030 long (koşulsuz) intra
rec("REF defansif-XU030 her gün long intra", pd.Series(1.0, index=tgt1.index), tgt1, 8, legs=2, note="koşulsuz referans")
# ---- B3 CCOLA -> AEFES
dA = DEC("AEFES"); dC = DEC("CCOLA"); ae = R("AEFES"); co = R("CCOLA")
for cost in (8, 15):
    rec("B3a CCOLA_{t-1} -> AEFES intra_t", co.shift(1), dA["intra"], cost)
    # spread: AEFES - b*CCOLA, b kayan 250g (geçmiş) ; dünkü spread getirisi ters -> bugün spread gün-içi
    bb = ae.rolling(250, min_periods=120).cov(co) / co.rolling(250, min_periods=120).var()
    sp = ae - bb.shift(1) * co
    sp_intra = dA["intra"] - bb.shift(1).reindex(dA.index) * dC["intra"].reindex(dA.index)
    rec("B3b AEFES-βCCOLA spread_{t-1} geri dönüş -> spread intra_t", -sp.shift(1), sp_intra, cost, mode="z", thr=1.0, legs=2)
B = pd.DataFrame(rows); B.to_csv(CODE + "/a5_backtests.csv", index=False)
pd.set_option("display.width", 250)
print(B[["bt", "cost_bps_rt", "IS_n", "IS_mean_bps", "IS_t", "IS_sharpe", "OOS_n", "OOS_mean_bps", "OOS_t", "OOS_sharpe"]].round(2).to_string(index=False))
