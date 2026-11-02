"""Saatlik (2023-12+) keskin testler.
post(TUR)_d = log(TUR US kapanışı_d / TUR 15:30 UTC_d)  -> BIST kapanışından SONRA ABD seansındaki Türkiye hareketi (BIST d+1 açılıştan önce biliniyor)
  (TUR saatlik barları :30'da başlar; 15:30 = 14:30 barının kapanışı ≈ BIST kapanış seansından 20 dk sonra. Kış aylarında ABD 14:30'da açılır.)
ES_ovn_t = log(ES 06:00 UTC_t / ES 15:00 UTC_{t-1})  -> BIST açılışından önce bilinen gece hareketi
Hedef: banka gap_t, intra_t (BIST günü t; sinyal önceki BIST gününün ABD seansı).
"""
import bk, ll, numpy as np, pandas as pd
cal = bk.D.index
def on_prev_bist(s):
    """UTC tarihli seriyi BIST günü t'ye 'önceki BIST günü' değeri olarak yerleştir."""
    s = s.reindex(cal); return s.shift(1)
def post_close(sym, ref="15:30", close="22:30"):
    a = ll.snap_daily(sym, ref); b = ll.snap_daily(sym, close)
    x = np.log(b / a); x.index = pd.DatetimeIndex(x.index); return x
rows = []
sig = {}
sig["TUR_post"] = on_prev_bist(post_close("TUR"))
sig["BBVA_post"] = on_prev_bist(post_close("BBVA"))
sig["EEM_post"] = on_prev_bist(post_close("EEM"))
es15 = ll.snap_daily("ES=F", "15:00"); es06 = ll.snap_daily("ES=F", "06:00")
es15.index = pd.DatetimeIndex(es15.index); es06.index = pd.DatetimeIndex(es06.index)
sig["ES_ovn"] = np.log(es06.reindex(cal) / es15.reindex(cal).shift(1))
sig["ES_post"] = on_prev_bist(post_close("ES=F", "15:00", "21:00"))
try:
    t15 = ll.snap_daily("TRY=X", "15:00"); t06 = ll.snap_daily("TRY=X", "06:00"); t15.index = pd.DatetimeIndex(t15.index); t06.index = pd.DatetimeIndex(t06.index)
    sig["USDTRY_ovn"] = np.log(t06.reindex(cal) / t15.reindex(cal).shift(1))
except Exception as e: print("TRY", e)
# TUR'un BIST kapanışına kadarki kısmı (bilgi BIST'te zaten fiyatlı olmalı) -> kontrol
tcl = ll.snap_daily("TUR", "22:30"); tcl.index = pd.DatetimeIndex(tcl.index); t1530 = ll.snap_daily("TUR", "15:30"); t1530.index = pd.DatetimeIndex(t1530.index)
pre = np.log(t1530 / tcl.shift(1))  # takvim günü kaydırması; kabaca
S = pd.DataFrame(sig); S = S[S.index >= "2023-12-05"]
S.to_parquet(bk.RES + "/hourly_signals.parquet")
print("sinyal n:", S.notna().sum().to_dict())
for st in bk.ALL + ["XU030", "XU100"]:
    g = bk.dec(st, "gap"); it = bk.dec(st, "intra")
    for sn in S.columns:
        for tn, y in [("gap", g), ("intra", it)]:
            df = pd.concat([y.rename("y"), S[sn].rename("s")], axis=1).dropna()
            if len(df) < 100: continue
            c, t, n = bk.hc_t(df.y, df.s)
            b = np.polyfit(df.s, df.y, 1)[0]
            h1 = df[df.index < "2025-05-01"]; h2 = df[df.index >= "2025-05-01"]
            c1, t1, _ = bk.hc_t(h1.y, h1.s); c2, t2, _ = bk.hc_t(h2.y, h2.s)
            rows.append((st, sn, tn, c, t, b, n, c1, t1, c2, t2))
R = pd.DataFrame(rows, columns=["stock", "signal", "target", "corr", "t", "beta", "n", "h1_corr", "h1_t", "h2_corr", "h2_t"]).round(3)
R.to_csv(bk.RES + "/hourly_tests.csv", index=False)
pd.set_option("display.width", 200)
print(R[R.stock.isin(["XBANK", "GARAN", "AKBNK", "HALKB", "XU030"])].to_string(index=False))
# XBANK vs XLBNK (saatlik) uyumu
try:
    a = ll.raw("XBANK.IS", "h1")["c"]; b = ll.raw("XLBNK.IS", "h1")["c"]
    x = pd.concat([np.log(a).diff(), np.log(b).diff()], axis=1).dropna(); print("XBANK~XLBNK saatlik corr:", round(x.corr().iloc[0, 1], 3), len(x))
except Exception as e: print("XLBNK", e)
