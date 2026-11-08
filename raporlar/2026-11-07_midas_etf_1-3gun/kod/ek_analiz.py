"""Eleştiri sonrası ek analizler (ana ajan):
 (1) Şu anki rejim: 20 günlük gerçekleşen oynaklık ve 52 haftalık zirveden düşüş, 10 yıllık dağılımdaki yüzdeliği.
 (2) A1/A2'nin oynaklık rejimine göre (sinyal günü 20g oynaklık üçte birlikleri) performansı.
 (3) Portföy simülasyonu: 10.000 $ hesap, A1 (QQQ, C1, 3 gün) ve A2 (SMH, C0, 1 gün), günlük kapanışla değerleme.
Çıktı: sonuclar/ek_rejim.csv, sonuclar/ek_rejim_performans.csv, sonuclar/ek_portfoy.csv, sonuclar/ek_portfoy_yillik.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import lib
from lib import ibs
OUT = os.path.join(lib.ROOT, "sonuclar")

def regime():
    rows = []
    for s in ["SPY", "QQQ", "SMH", "SOXL", "TQQQ", "GDXJ", "GLD", "EWY", "IBIT", "UNG", "NVDL"]:
        d = lib.load(s); r = np.log(d["c"]).diff()
        v20 = r.rolling(20).std() * math.sqrt(252)
        dd = d["c"] / d["c"].rolling(252, min_periods=50).max() - 1
        rows.append({"sym": s, "tarih": str(d.index[-1].date()), "vol20_yillik": v20.iloc[-1], "vol20_10y_medyan": v20.median(),
                     "vol20_yuzdelik": (v20.dropna() < v20.iloc[-1]).mean(), "zirveden_dusus": dd.iloc[-1],
                     "gunluk_1sd_bp": r.rolling(20).std().iloc[-1] * 1e4})
    vix = lib.vol_index("VIX"); v3 = lib.vol_index("VIX3M")
    rows.append({"sym": "VIX", "tarih": str(vix.index[-1].date()), "vol20_yillik": vix.iloc[-1], "vol20_10y_medyan": vix[vix.index >= "2016-11-01"].median(),
                 "vol20_yuzdelik": (vix[vix.index >= "2016-11-01"] < vix.iloc[-1]).mean(), "zirveden_dusus": np.nan, "gunluk_1sd_bp": (vix / v3).iloc[-1]})
    df = pd.DataFrame(rows); df.to_csv(os.path.join(OUT, "ek_rejim.csv"), index=False); return df

def rule_trades(sym, thr, down, h, mode, pos=2500):
    d = lib.load(sym)
    sig = (ibs(d) < thr) & (d["h"] > d["l"])
    if down: sig &= d["c"] < d["c"].shift(1)
    sig.iloc[:60] = False
    cost = 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(d)
    return d, lib.trades(d, sig, h, mode, None, cost)

def regime_perf():
    out = []
    for name, sym, thr, down, h, mode in [("A1", "QQQ", 0.10, True, 3, "C1"), ("A2", "SMH", 0.20, False, 1, "C0")]:
        d, tr = rule_trades(sym, thr, down, h, mode)
        v20 = np.log(d["c"]).diff().rolling(20).std()
        tr["v20"] = v20.reindex(tr["sig_date"]).values
        q = v20.dropna().quantile([1 / 3, 2 / 3]).values
        tr["rejim"] = np.where(tr["v20"] <= q[0], "düşük", np.where(tr["v20"] <= q[1], "orta", "yüksek"))
        for rj, g in tr.groupby("rejim"):
            x = g["net"].values
            out.append({"kural": name, "rejim_20g_oynaklik": rj, "n": len(x), "net_bp": x.mean() * 1e4, "t": x.mean() / (x.std(ddof=1) / math.sqrt(len(x))),
                        "std_bp": x.std(ddof=1) * 1e4, "en_kotu_bp": x.min() * 1e4, "kazanma": (x > 0).mean(), "getiri_risk": x.mean() / x.std(ddof=1)})
        y26 = tr[tr["sig_date"].dt.year == 2026]["net"]
        out.append({"kural": name, "rejim_20g_oynaklik": "yalnız 2026", "n": len(y26), "net_bp": y26.mean() * 1e4 if len(y26) else np.nan,
                    "t": y26.mean() / (y26.std(ddof=1) / math.sqrt(len(y26))) if len(y26) > 2 else np.nan, "std_bp": y26.std(ddof=1) * 1e4 if len(y26) > 1 else np.nan,
                    "en_kotu_bp": y26.min() * 1e4 if len(y26) else np.nan, "kazanma": (y26 > 0).mean() if len(y26) else np.nan, "getiri_risk": np.nan})
    df = pd.DataFrame(out); df.to_csv(os.path.join(OUT, "ek_rejim_performans.csv"), index=False); return df

def portfolio(cap=10000.0, w1=0.5, w2=0.25):
    """A1: QQQ C1 3 gün, sermayenin w1'i; A2: SMH C0 1 gün, w2'si. Pozisyon tutarı işlem anındaki özsermayeye göre.
    Komisyon 1,5 $/emir + makas (yarısı girişte, yarısı çıkışta). Nakit faizsiz."""
    q, t1 = rule_trades("QQQ", 0.10, True, 3, "C1")
    m, t2 = rule_trades("SMH", 0.20, False, 1, "C0")
    idx = q.index.union(m.index)
    eq = pd.Series(np.nan, index=idx); cash = cap
    events = []
    for name, d, tr, w in (("A1", q, t1, w1), ("A2", m, t2, w2)):
        sp = lib.spread_bp_tier(d) / 1e4
        for _, t in tr.iterrows():
            events.append((t["entry_date"], t["exit_date"], name, w, d, sp))
    # günlük değerleme
    open_pos = []; equity = cap; rows = []; ntr = {"A1": 0, "A2": 0}; comm = 0.0
    ev = sorted(events, key=lambda e: e[0])
    j = 0
    for day in idx:
        # pozisyonların günlük değerlemesi
        for p in open_pos:
            d = p["d"]
            if day in d.index and day > p["entry"]:
                prev = p["last"]; px = d.at[day, "c"]; equity += p["sh"] * (px - prev); p["last"] = px
        # çıkışlar
        still = []
        for p in open_pos:
            if day == p["exit"]:
                cost = 1.5 + p["sh"] * p["last"] * p["sp"] / 2; equity -= cost; comm += cost
            else:
                still.append(p)
        open_pos = still
        # girişler (t kapanışında)
        while j < len(ev) and ev[j][0] <= day:
            e = ev[j]; j += 1
            if e[0] != day: continue
            if any(p["name"] == e[2] for p in open_pos): continue
            d = e[4]; px = d.at[day, "c"]; amt = equity * e[3]
            sh = amt / px; cost = 1.5 + amt * e[5] / 2; equity -= cost; comm += cost
            open_pos.append({"name": e[2], "d": d, "entry": day, "exit": e[1], "sh": sh, "last": px, "sp": e[5]}); ntr[e[2]] += 1
        rows.append((day, equity, sum(p["sh"] * p["last"] for p in open_pos)))
    E = pd.DataFrame(rows, columns=["tarih", "ozsermaye", "pozisyon_degeri"]).set_index("tarih")
    E = E[E.index >= q.index[60]]
    r = E["ozsermaye"].pct_change().dropna()
    yr = E["ozsermaye"].groupby(E.index.year).agg(["first", "last"])
    yr["getiri_%"] = (yr["last"] / yr["first"] - 1) * 100
    dd = E["ozsermaye"] / E["ozsermaye"].cummax() - 1
    yrs = (E.index[-1] - E.index[0]).days / 365.25
    summ = {"baslangic": str(E.index[0].date()), "bitis": str(E.index[-1].date()), "son_ozsermaye": E["ozsermaye"].iloc[-1],
            "yillik_bilesik_%": ((E["ozsermaye"].iloc[-1] / cap) ** (1 / yrs) - 1) * 100, "yillik_oynaklik_%": r.std() * math.sqrt(252) * 100,
            "maxDD_%": dd.min() * 100, "maxDD_tarih": str(dd.idxmin().date()), "A1_islem": ntr["A1"], "A2_islem": ntr["A2"],
            "islem_yil": (ntr["A1"] + ntr["A2"]) / yrs, "toplam_maliyet_$": comm, "piyasada_gun_orani": (E["pozisyon_degeri"] > 0).mean(),
            "w_A1": w1, "w_A2": w2}
    # karşılaştırma: QQQ al-tut
    qq = q["c"][q.index >= E.index[0]]
    summ["QQQ_al_tut_yillik_%"] = ((qq.iloc[-1] / qq.iloc[0]) ** (1 / yrs) - 1) * 100
    summ["QQQ_al_tut_maxDD_%"] = ((qq / qq.cummax()) - 1).min() * 100
    return summ, yr

def main():
    reg = regime(); print(reg.round(3).to_string(index=False))
    rp = regime_perf(); print(rp.round(2).to_string(index=False))
    out = []; yy = None
    for w1, w2 in [(0.5, 0.25), (1.0, 0.0), (0.0, 1.0), (0.25, 0.25)]:
        s, yr = portfolio(10000, w1, w2); out.append(s)
        if (w1, w2) == (0.5, 0.25): yy = yr
    P = pd.DataFrame(out); P.to_csv(os.path.join(OUT, "ek_portfoy.csv"), index=False)
    yy.to_csv(os.path.join(OUT, "ek_portfoy_yillik.csv"))
    print(P.round(2).T.to_string()); print(yy.round(1).to_string())

if __name__ == "__main__":
    main()
