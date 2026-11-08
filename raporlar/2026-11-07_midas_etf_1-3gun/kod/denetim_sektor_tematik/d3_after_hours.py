"""Denetim: C0'ın Midas'ta uygulanabilirliği — kapanış sonrası (after-hours) limit emriyle resmî kapanışa yakın fiyat
alınabiliyor mu? Yahoo saatlik + uzatılmış seans barları (2023-12..2026-11) ve 5 dk (son ~60 gün).
python3 -I kod/denetim_sektor_tematik/d3_after_hours.py <yahoo_raw_dizini>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *

RAW = sys.argv[1]


def yahoo(f):
    j = json.load(open(os.path.join(RAW, f)))["chart"]["result"][0]
    ts = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    q = j["indicators"]["quote"][0]
    return pd.DataFrame({k: pd.to_numeric(pd.Series(q[k]), errors="coerce").values for k in ("open", "high", "low", "close", "volume")}, index=ts).dropna(subset=["open"])


rc = raw("SMH")["c"]; sig_off = (my_ibs(raw("SMH")) < 0.2)
cst = cost("SMH")
out = {}
h = yahoo("SMH_60m_pp.json")
day = h.index.tz_localize(None).normalize(); tm = h.index.time
ah = h[(tm == pd.Timestamp("16:00").time())].copy(); ah.index = ah.index.tz_localize(None).normalize()
ah2 = h[(tm == pd.Timestamp("17:00").time())].copy(); ah2.index = ah2.index.tz_localize(None).normalize()
idx = ah.index[ah.index.isin(rc.index)]
S = sig_off.reindex(idx).fillna(False)
C = rc.reindex(idx); nxt = rc.shift(-1).reindex(idx)
rows = []
for nm, m in (("tum_gunler", pd.Series(True, index=idx)), ("sinyal_gunleri", S)):
    a = ah.reindex(idx)[m]; c = C[m]
    rows.append({"kume": nm, "n": int(m.sum()),
                 "AH_ilk_islem_vs_kapanis_bp": float((a["open"] / c - 1).mean() * 1e4),
                 "AH_16_17_kapanis_vs_kapanis_bp": float((a["close"] / c - 1).mean() * 1e4),
                 "AH_16_17_dusuk_le_kapanis_orani": float((a["low"] <= c).mean()),
                 "AH_16_17_hacim_medyan": float(a["volume"].median())})
r = pd.DataFrame(rows); print("Saatlik AH (16:00-17:00 ET) barı:"); print(r.round(3).to_string()); out["ah_ozet"] = r.round(3).to_dict("records")
# Senaryolar: resmî IBS sinyali; giriş (i) resmî kapanış, (ii) kapanışa eşit limit (AH 16-17 barında low<=C ise C'den dolar; değilse işlem yok),
# (iii) 17:00 ET civarı AH fiyatı (16-17 barının kapanışı); çıkış ertesi resmî kapanış.
a = ah.reindex(idx)
res = []
for nm, ep, ok in (("resmi kapanis (backtest)", C, S),
                   ("AH limit = resmi kapanis (dolarsa)", C, S & (a["low"] <= C)),
                   ("AH limit = kapanis + 5 bp (dolarsa)", C * 1.0005, S & (a["low"] <= C * 1.0005)),
                   ("AH 17:00 ET fiyati", a["close"], S)):
    g = (nxt / ep - 1)[ok].dropna()
    res.append({"senaryo": nm, "n": len(g), "doluluk": len(g) / max(int(S.sum()), 1), "brut_bp": g.mean() * 1e4, "net_bp": g.mean() * 1e4 - cst, "t": tt(g.values - cst / 1e4)})
# dolmayan sinyallerin ertesi gün getirisi (seçilim yanlılığı: dolmayanlar mı kazandırıyor?)
miss = S & ~(a["low"] <= C)
gm = (nxt / C - 1)[miss].dropna()
res.append({"senaryo": "dolmayan sinyaller (resmi kapanistan olsaydi)", "n": len(gm), "doluluk": np.nan, "brut_bp": gm.mean() * 1e4 if len(gm) else np.nan, "net_bp": np.nan, "t": np.nan})
rr = pd.DataFrame(res); print("\nC0 uygulama senaryoları (2023-12..2026-11, sinyal: resmî IBS<0.2):"); print(rr.round(2).to_string())
out["senaryolar"] = rr.round(3).to_dict("records")

# 5 dk: kapanıştan önceki son dakikalar ve AH ilk 15 dk
m5 = yahoo("SMH_5m_pp.json"); t5 = m5.index.time; d5 = m5.index.tz_localize(None).normalize()
rows = []
for d in sorted(set(d5)):
    if d not in rc.index: continue
    g = m5[d5 == d]; tt_ = pd.Series(g.index.time, index=g.index)
    def px(hhmm, col="open"):
        x = g[tt_ == pd.Timestamp(hhmm).time()]
        return float(x[col].iloc[0]) if len(x) else np.nan
    post = g[(tt_ >= pd.Timestamp("16:00").time()) & (tt_ < pd.Timestamp("16:15").time())]
    rows.append({"date": d, "sig": bool(sig_off.get(d, False)), "C": float(rc[d]), "p1545": px("15:45"), "p1550": px("15:50"), "p1555": px("15:55"),
                 "ah_low_15dk": float(post["low"].min()) if len(post) else np.nan, "ah_vol_15dk": float(post["volume"].sum()) if len(post) else np.nan})
f5 = pd.DataFrame(rows).set_index("date")
for col in ("p1545", "p1550", "p1555"):
    f5[col + "_vs_C_bp"] = (f5[col] / f5["C"] - 1) * 1e4
f5["ah_low_le_C"] = f5["ah_low_15dk"] <= f5["C"]
summ = f5.groupby("sig")[["p1545_vs_C_bp", "p1550_vs_C_bp", "p1555_vs_C_bp", "ah_low_le_C", "ah_vol_15dk"]].agg(["mean", "count"])
print("\n5 dk (son ~60 gün): kapanış öncesi fiyat - resmî kapanış (bp) ve AH ilk 15 dk'da kapanış fiyatından dolma:")
print(summ.round(2).to_string())
out["bes_dk"] = {str(k): v for k, v in summ.round(3).to_dict().items()}
json.dump(out, open(os.path.join(OUT, "d3_after_hours.json"), "w"), ensure_ascii=False, indent=1, default=str)
