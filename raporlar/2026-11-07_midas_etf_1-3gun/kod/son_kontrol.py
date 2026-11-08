"""Ana ajanın son kontrolü: denetimden sağ çıkan (doğrulandı + zayıf) tüm kuralları, Yahoo dağıtımlarıyla düzeltilmiş
veriyle TEK bir tutarlı motorda yeniden hesaplar. Aile ajanlarının ve denetçilerin kodundan bağımsızdır (lib.trades
motoru + kendi sinyal tanımları). Çıktı: sonuclar/son_kontrol.csv, sonuclar/son_kontrol_yillik.csv,
sonuclar/son_kontrol_korelasyon.csv. Kullanım: python3 -I kod/son_kontrol.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import lib
from lib import ibs, sma

OUT = os.path.join(lib.ROOT, "sonuclar")
EV = os.path.join(lib.DATA, "events")

def ibs_down(sym, thr):
    d = lib.load(sym); return (ibs(d) < thr) & (d["c"] < d["c"].shift(1)) & (d["h"] > d["l"])

def ibs_only(sym, thr):
    d = lib.load(sym); return (ibs(d) < thr) & (d["h"] > d["l"])

def month_last(sym):
    d = lib.load(sym); idx = d.index; s = pd.Series(idx, index=idx)
    return s.groupby([idx.year, idx.month]).transform("max") == s

def asia_basket_sig(sym):
    spy = lib.load("SPY")["c"].pct_change(); d = lib.load(sym)["c"].pct_change()
    spy = spy.reindex(d.index)
    return (spy <= -0.015) & (d <= spy)

def auction_sig(sym):
    a = pd.read_csv(os.path.join(EV, "hazine_ihale_10y30y.csv"))
    a = a[a["event"].str.contains("10Y", case=False)]
    dates = pd.to_datetime(a["date"])
    d = lib.load(sym); idx = d.index; sig = pd.Series(False, index=idx)
    for A in dates:
        pos = idx.searchsorted(A)
        if pos < len(idx) and idx[pos] == A and pos - 3 >= 0:
            sig.iloc[pos - 3] = True
    return sig

def eia_winter_sig(sym):
    e = pd.read_csv(os.path.join(EV, "eia_ng_storage.csv")); dates = pd.to_datetime(e["date"])
    d = lib.load(sym); idx = d.index; sig = pd.Series(False, index=idx)
    for R in dates:
        if R.month not in (11, 12, 1, 2, 3): continue
        pos = idx.searchsorted(R)
        if pos < len(idx) and idx[pos] == R and pos - 1 >= 0:
            sig.iloc[pos - 1] = True
    return sig

def bb_low(sym):
    d = lib.load(sym); c = d["c"]; return c < sma(c, 20) - 2 * c.rolling(20).std()

def trend_10_50(sym):
    d = lib.load(sym); c = d["c"]; return (c > sma(c, 10)) & (sma(c, 10) > sma(c, 50))

# (id, ad, sinyal fonksiyonu, sinyal ETF, işlem ETF'leri, h, ana mod, aile kararı)
RULES = [
    ("abd_endeks_S2", "QQQ IBS<0,10 & düşüş → 3 gün", lambda: ibs_down("QQQ", 0.10), "QQQ", ["QQQ", "QLD", "TQQQ"], 3, "C1", "dogrulandi"),
    ("abd_endeks_S1", "SPY IBS<0,10 & düşüş → 3 gün", lambda: ibs_down("SPY", 0.10), "SPY", ["SPY", "SSO", "SPXL"], 3, "C1", "zayif"),
    ("sektor_tematik_S1", "SMH IBS<0,20 → 1 gün", lambda: ibs_only("SMH", 0.20), "SMH", ["SMH", "SOXX", "SOXL"], 1, "C0", "dogrulandi"),
    ("metal_madenci_S3", "GDXJ IBS<0,10 & düşüş → 3 gün", lambda: ibs_down("GDXJ", 0.10), "GDXJ", ["GDXJ", "JNUG"], 3, "C0", "zayif"),
    ("metal_madenci_S1", "Ay sonu GDX (son gün → 3. gün)", lambda: month_last("GDX"), "GDX", ["GDX", "NUGT"], 3, "C0", "zayif"),
    ("metal_madenci_S2", "Ay sonu GLD (son gün → 3. gün)", lambda: month_last("GLD"), "GLD", ["GLD"], 3, "C0", "zayif"),
    ("uluslararasi_S2", "EWY IBS<0,10 & düşüş → 1 gün", lambda: ibs_down("EWY", 0.10), "EWY", ["EWY", "KORU"], 1, "C0", "zayif"),
    ("tahvil_doviz_S1", "10Y ihale A-3 → A-1 TMV", lambda: auction_sig("TMV"), "takvim", ["TMV", "TBT"], 2, "C0", "zayif"),
    ("enerji_tarim_S1", "EIA öncesi KOLD (Kas-Mar)", lambda: eia_winter_sig("KOLD"), "takvim", ["KOLD"], 1, "C0", "zayif"),
    ("enerji_tarim_S2", "USO alt Bollinger → C1 2 gün", lambda: bb_low("USO"), "USO", ["USO"], 2, "C1", "zayif"),
    ("kripto_S2", "IBIT trend (C>SMA10>SMA50) → 3 gün", lambda: trend_10_50("IBIT"), "IBIT", ["IBIT"], 3, "C0", "zayif"),
]
ASIA = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]

def cost_for(df, pos):
    return 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(df)

def summarize(tr, df, h, mode, label):
    s = lib.stats(tr, df, h, mode, label)
    if len(tr) > 6:
        x = tr["net"].sort_values().values[:-5]
        s["t_en_iyi5_haric"] = x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))
        s["net_en_iyi5_haric_bp"] = x.mean() * 1e4
        ex = tr[~tr["sig_date"].dt.year.isin([2020, 2022])]["net"].values
        s["t_2020_2022_haric"] = ex.mean() / (ex.std(ddof=1) / math.sqrt(len(ex))) if len(ex) > 3 else np.nan
    return s

def main():
    rows, yearly, daily = [], [], {}
    for rid, ad, fn, sig_etf, tools, h, mode0, karar in RULES:
        sig = fn()
        for tool in tools:
            try:
                df = lib.load(tool)
            except Exception:
                continue
            sg = sig.reindex(df.index).fillna(False).astype(bool)
            sg.iloc[:60] = False
            for mode in ("C0", "O1", "C1"):
                for pos in (1000, 2500, 10000):
                    c = cost_for(df, pos)
                    tr = lib.trades(df, sg, h, mode, None, c)
                    s = summarize(tr, df, h, mode, ad)
                    s.update({"id": rid, "ad": ad, "sinyal": sig_etf, "arac": tool, "h": h, "mode": mode, "pos_usd": pos,
                              "cost_bp": c, "ana_mod": mode == mode0, "aile_karar": karar, "baslangic": str(df.index[0].date())})
                    rows.append(s)
                    if pos == 2500 and mode == mode0 and tool == tools[0] and len(tr):
                        y = tr.groupby(tr["sig_date"].dt.year)["net"].agg(["count", "mean", "sum"])
                        for yr, r in y.iterrows():
                            yearly.append({"id": rid, "arac": tool, "yil": yr, "n": int(r["count"]), "ort_net_bp": r["mean"] * 1e4, "toplam_net_%": r["sum"] * 100})
                        # günlük getiri serisi (korelasyon için): pozisyondaki günlerin getirisi
                        ret = df["c"].pct_change(); pos_mask = pd.Series(0.0, index=df.index)
                        for _, t in tr.iterrows():
                            a = df.index.get_loc(t["entry_date"]); b = df.index.get_loc(t["exit_date"])
                            pos_mask.iloc[a + 1:b + 1] = 1.0
                        daily[rid] = (ret * pos_mask).fillna(0)
    # Asya sepeti (uluslararasi_S1): ETF başına sinyal, h=1, eşit ağırlık
    for mode in ("C0", "O1", "C1"):
        for pos in (1000, 2500, 10000):
            alltr = []
            for sym in ASIA:
                df = lib.load(sym); sg = asia_basket_sig(sym).fillna(False); sg.iloc[:60] = False
                tr = lib.trades(df, sg, 1, mode, None, cost_for(df, pos)); tr["sym"] = sym; alltr.append(tr)
            tr = pd.concat(alltr).sort_values("sig_date")
            s = summarize(tr, None, 1, mode, "Asya sepeti")
            s.update({"id": "uluslararasi_S1", "ad": "SPY ≤ -%1,5 günü SPY'dan çok düşen Asya ETF'leri → 1 gün", "sinyal": "SPY+ETF", "arac": "sepet(6)",
                      "h": 1, "mode": mode, "pos_usd": pos, "cost_bp": np.nan, "ana_mod": mode == "C0", "aile_karar": "zayif", "baslangic": "2016-11-07"})
            rows.append(s)
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(OUT, "son_kontrol.csv"), index=False)
    pd.DataFrame(yearly).to_csv(os.path.join(OUT, "son_kontrol_yillik.csv"), index=False)
    D = pd.DataFrame(daily); D = D[D.index >= "2017-01-01"]
    D.corr().round(2).to_csv(os.path.join(OUT, "son_kontrol_korelasyon.csv"))
    cols = ["id", "arac", "mode", "n", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac", "win", "worst_bp", "t_en_iyi5_haric", "t_2020_2022_haric", "edge_bp"]
    v = res[(res.pos_usd == 2500)]
    pd.set_option("display.width", 250)
    print(v[cols].round(2).to_string(index=False))
    print("\n1.000$ / 10.000$ ana mod:")
    w = res[res.ana_mod & res.pos_usd.isin([1000, 10000])][["id", "arac", "pos_usd", "mean_net_bp", "t"]]
    print(w.round(2).to_string(index=False))
    print("\nKorelasyon (pozisyondaki günlük getiriler):"); print(D.corr().round(2).to_string())

if __name__ == "__main__":
    main()
