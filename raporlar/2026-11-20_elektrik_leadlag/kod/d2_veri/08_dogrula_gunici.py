"""Gün içi veri doğrulaması (Yahoo h1/m5, İş Yatırım endeks, snap). Çıktı: RAW/dogrulama_gunici.txt.  Kullanım: python3 -I 08_dogrula_gunici.py"""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, FULL, STOCKS, ISY_IDX
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)
def load(kind, syms):
    X = pd.concat([pd.read_parquet(f"{FULL}/{kind}/{s}.parquet").assign(sym=s) for s in syms if os.path.exists(f"{FULL}/{kind}/{s}.parquet")])
    X["date"] = X["ts_tr"].dt.normalize(); X["hm"] = X["ts_tr"].dt.strftime("%H:%M"); return X
H = load("h1", STOCKS + ["XU030", "XU100"]); M = load("m5", STOCKS + ["XU030", "XU100"]); S = pd.read_parquet(f"{FULL}/snap.parquet")
P("== 1. Kapsam")
c = H.groupby("sym").agg(ilk=("date", "min"), son=("date", "max"), gun=("date", "nunique"), bar=("c", "size"))
P("h1 sembol", len(c), "| ilk tarih dağılımı:", c["ilk"].dt.strftime("%Y-%m-%d").value_counts().head(4).to_dict(), "| son:", c["son"].max().date(), "| gün medyan", c["gun"].median())
P("h1 geç başlayanlar (halka arz):", c[c["ilk"] > c["ilk"].min()]["ilk"].dt.strftime("%Y-%m-%d").to_dict())
c5 = M.groupby("sym").agg(ilk=("date", "min"), son=("date", "max"), gun=("date", "nunique"))
P("m5 sembol", len(c5), "| ilk:", c5["ilk"].min().date(), "son:", c5["son"].max().date(), "| gün medyan", c5["gun"].median())
P("== 2. Saatlik bar ızgarası (TSİ bar başlangıcı -> bar sayısı)"); P(H["hm"].value_counts().sort_index().to_dict())
hs = H[H["sym"].isin(STOCKS)]; last = hs.groupby(["sym", "date"])["hm"].max()
P("günün son saatlik barı:", last.value_counts().to_dict())
m_ = (last == "17:30").groupby(last.index.get_level_values("date").to_period("Q")).mean().round(2)
P("17:30 barı olan hisse-gün oranı (çeyrek):", {str(k): v for k, v in m_.items()})
P("== 3. Saatlik bar hangi 5 dk'ları kapsıyor? (örtüşen dönem, hisseler)")
m = M[M["sym"].isin(STOCKS)].copy(); m["hmn"] = m["ts_tr"].dt.hour * 60 + m["ts_tr"].dt.minute
def m5_last(hm_max, exact=False):
    x = m[m["hmn"] == hm_max] if exact else m[m["hmn"] <= hm_max]
    return x.groupby(["sym", "date"])["c"].last()
piv = hs.pivot_table(index=["sym", "date"], columns="hm", values="c")
for hb, m5b, lab in (("15:30", 16 * 60 + 25, "h1 15:30 barı kapanışı vs m5 16:25 barı kapanışı"), ("16:30", 17 * 60 + 25, "h1 16:30 barı kapanışı vs m5 17:25 barı kapanışı"),
                     ("17:30", 17 * 60 + 55, "h1 17:30 barı kapanışı vs m5 17:55 barı kapanışı")):
    j = pd.concat([piv[hb], m5_last(m5b)], axis=1, keys=["h", "m"]).dropna()
    P(lab, "| n", len(j), "| birebir aynı oran", round(((j["h"] / j["m"] - 1).abs() < 1e-5).mean(), 4), "| medyan |fark| bps", round(1e4 * (j["h"] / j["m"] - 1).abs().median(), 2))
st = S[S["sym"].isin(STOCKS)].copy()
P("== 4. Kapanış seansı hangi barda? p_son (17:30 saatlik / 17:55 5 dk barı) ile resmi günlük kapanış")
j = st.dropna(subset=["p_son", "p_close"]); r = j["p_close"] / j["p_son"] - 1
P("n", len(j), "| p_son == p_close oranı", round((r.abs() < 1e-5).mean(), 3), "| medyan |fark| bps", round(1e4 * r.abs().median(), 1), "| p95", round(1e4 * r.abs().quantile(.95), 1), "| |fark|>%3:", int((r.abs() > 0.03).sum()))
P("== 4b. Ham baza çevirme (yahoo_carpan) denetimi")
kk = pd.read_csv(f"{RAW}/yahoo_carpan_kirilmalar.csv"); ca = pd.read_parquet(f"{FULL}/ca_day.parquet")
ca_set = set((c, d_) for c in ca.columns for d_ in ca.index[ca[c].fillna(0).astype(float) != 0])
near = [any((s_, pd.Timestamp(d_) + pd.Timedelta(days=o)) in ca_set for o in range(-4, 5)) for s_, d_ in zip(kk["sym"], kk["date"])]
P("kırılma sayısı", len(kk), "| D1 ca_day ile ±4 gün içinde eşleşen", int(sum(near)), "| eşleşmeyen:", kk[~np.array(near)].values.tolist())
P("çarpanı 1 olmayan hisse-gün oranı", round((st["yahoo_carpan"] != 1).mean(), 4), "| hisse sayısı", st.loc[st["yahoo_carpan"] != 1, "sym"].nunique(), "| çarpan aralığı", round(st["yahoo_carpan"].min(), 4), round(st["yahoo_carpan"].max(), 4))
for c in ("p_1630", "p_1730", "p_son"):
    r = (st[c] / st["p_close"] - 1).dropna()
    P(c, "/ p_close - 1: n", len(r), "| medyan |.| bps", round(1e4 * r.abs().median(), 1), "| p99 |.| %", round(100 * r.abs().quantile(.99), 2), "| |.|>%10,5:", int((r.abs() > 0.105).sum()), "| |.|>%6:", int((r.abs() > 0.06).sum()))
r = st["p_1730"] / st["p_close"] - 1
P("en büyük 8 sapma:", st.assign(r=r).reindex(r.abs().sort_values(ascending=False).index).head(8)[["date", "sym", "p_1730", "p_close", "yahoo_carpan", "r"]].round(4).astype(str).values.tolist())
P("== 4c. Zaman damgası hizası: Yahoo XU030 saatlik barı [15:30,16:30) İş Yatırım'ın 16:00 değerini (15:00 barı) kapsıyor mu? (kış/yaz, ±1 saat kaydırma ile)")
iy = pd.read_parquet(f"{FULL}/h1_isy/XU030.parquet"); iy["date"] = iy["ts_tr"].dt.normalize(); iy["hm"] = iy["ts_tr"].dt.strftime("%H:%M")
y = H[H["sym"] == "XU030"]
for shift, lab in ((0, "doğru hiza"), (-60, "Yahoo 1 saat erken sayılırsa"), (60, "Yahoo 1 saat geç sayılırsa")):
    yb = y[y["hm"] == "15:30"].set_index("date"); tgt = pd.Timestamp("2000-01-01 15:00") + pd.Timedelta(minutes=shift)
    v = iy[iy["hm"] == tgt.strftime("%H:%M")].set_index("date")["c"].reindex(yb.index)
    ok = ((v >= yb["l"] * (1 - 2e-4)) & (v <= yb["h"] * (1 + 2e-4)))[v.notna()]; kis = ok.index.month.isin([11, 12, 1, 2, 3])
    P(lab, "| kapsama oranı kış", round(ok[kis].mean(), 3), "yaz", round(ok[~kis].mean(), 3), "| n", len(ok))
P("== 5. Bayatlık: 17:50 / 17:00 fiyatı yerine saatlik veri kullanmanın bedeli (m5 dönemi, hisseler)")
k = st[st["kaynak"] == "m5"]
for a, b, lab in (("p_1730", "p_1750", "p_1730 (h1) vs p_1750 (m5)"), ("p_1630", "p_1700", "p_1630 (h1) vs p_1700 (m5)"), ("p_1750", "p_close", "p_1750 (m5) vs p_close"), ("p_1700", "p_close", "p_1700 (m5) vs p_close"), ("p_1730", "p_close", "p_1730 vs p_close")):
    r = (k[a] / k[b] - 1).dropna(); P(lab, "| n", len(r), "| medyan |fark| bps", round(1e4 * r.abs().median(), 1), "| p90", round(1e4 * r.abs().quantile(.9), 1))
ka = st.dropna(subset=["p_1730", "p_close"]); r = ka["p_1730"] / ka["p_close"] - 1
P("tüm h1 dönemi p_1730 vs p_close | n", len(r), "| medyan |fark| bps", round(1e4 * r.abs().median(), 1), "| p90", round(1e4 * r.abs().quantile(.9), 1))
P("snap kullanılan barlar: bar_1700", st.groupby("kaynak")["bar_1700"].value_counts().groupby(level=0).head(3).to_dict(), "| bar_1750", st.groupby("kaynak")["bar_1750"].value_counts().groupby(level=0).head(3).to_dict())
P("snap eksik oranı (hisse):", st[["p_open", "p_1630", "p_1700", "p_1730", "p_1750", "p_son", "p_close"]].isna().mean().round(4).to_dict())
P("== 6. İş Yatırım endeks gün içi")
for kind in ("h1", "m5", "m15", "m30"):
    for code in ISY_IDX:
        fn = f"{RAW}/isy/{kind}/{code}.parquet"
        if not os.path.exists(fn): continue
        x = pd.read_parquet(fn); x["tr"] = x["ts_utc"] + pd.Timedelta(hours=3); x["date"] = x["tr"].dt.normalize()
        bpd = x.groupby("date").size(); yr = x.groupby(x["date"].dt.year)["date"].nunique()
        P(kind, code, "n", len(x), "ilk", x["tr"].min(), "son", x["tr"].max(), "| gün", len(bpd), "| bar/gün medyan", bpd.median(), "| az barlı gün (<medyan*0,6)", int((bpd < bpd.median() * .6).sum()), "| yıl->gün", yr.to_dict())
aux = pd.read_parquet(f"{RAW}/snap_endeks_kapanis_kontrol.parquet"); ix = pd.read_parquet(f"{FULL}/idx.parquet").stack().rename("d1").rename_axis(["date", "sym"]).reset_index()
aux = aux.merge(ix, on=["date", "sym"], how="left")
for code, g in aux.groupby("sym"):
    r1 = (g["p_close_isy"] / g["d1"] - 1).dropna(); r2 = (g["p_close_isy"] / g["p_close_yahoo"] - 1).dropna()
    P(code, "İşY günün son 5 dk değeri vs D1 idx kapanış: n", len(r1), "| <1 bps oranı", round((r1.abs() < 1e-4).mean(), 4), "| |fark|>%0,5:", int((r1.abs() > 0.005).sum()),
      "| vs Yahoo günlük: n", len(r2), "<1 bps", round((r2.abs() < 1e-4).mean(), 4) if len(r2) else None)
si = S[S["sym"].isin(ISY_IDX)]
P("endeks snap:", si.groupby("sym").agg(ilk=("date", "min"), gun=("date", "size"), p1700_nan=("p_1700", lambda s: s.isna().mean()), p1750_nan=("p_1750", lambda s: s.isna().mean())).round(4).to_dict("index"))
P("endeks bar_1750:", si["bar_1750"].value_counts().head(5).to_dict(), "| bar_1700:", si["bar_1700"].value_counts().head(5).to_dict())
# Yahoo XU030 h1 vs İşY m5 aynı saat
for code in ("XU030", "XU100"):
    fn = f"{RAW}/isy/m5/{code}.parquet"
    if not os.path.exists(fn): continue
    y = H[(H["sym"] == code) & (H["hm"] == "16:30")].set_index("date")["c"]; z = si[si["sym"] == code].set_index("date")["p_1730"]
    r = (y / z - 1).dropna(); P(code, "Yahoo h1 16:30 barı kapanışı vs İşY 17:25 barı: n", len(r), "medyan |fark| bps", round(1e4 * r.abs().median(), 2))
open(f"{RAW}/dogrulama_gunici.txt", "w").write("\n".join(out) + "\n")
