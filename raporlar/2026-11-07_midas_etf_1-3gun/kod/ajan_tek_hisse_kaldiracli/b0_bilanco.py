"""Geçmiş bilanço (kazanç duyurusu) tarihleri — Nasdaq takvim API'si (https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD),
dürüst istemci adı 'etf-research-script/1.0' ile, istek arası bekleme, sonuçlar önbelleğe (ham_bilanco/<tarih>.json).
Yöntem: (1) Her dayanak hissede hacim sıçraması (v / önceki 50 gün medyanı) en yüksek günler, aralarında >=25 işlem günü olacak
şekilde aday 'tepki günü' R seçilir. (2) Takvimde R-1 ve R tarihleri sorgulanır; hisse listede ise duyuru tarihi E bulunur.
(3) Ardışık doğrulanmış duyurular arasında >75 işlem günü boşluk varsa beklenen pencere (E+55..E+70) günü gün taranır (sınırlı).
Bulunamayan çeyrekler 'tahmini' (hacim+boşluk) olarak işaretlenir. Çıktı: sonuclar/aile_tek_hisse_kaldiracli/bilanco_tarihleri.csv
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/b0_bilanco.py  (önbellekle tekrar çalıştırılabilir; ağ yalnız eksik günler için)
"""
import os, sys, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, requests
import thk

CACHE = os.path.join(thk.OUT, "ham_bilanco")
os.makedirs(CACHE, exist_ok=True)
UA = "etf-research-script/1.0"
S = requests.Session(); S.headers["User-Agent"] = UA; S.headers["Accept"] = "application/json"
NCALL = [0]

def cal(d):
    """d: Timestamp -> {sym: time} (önbellekli)."""
    ds = d.strftime("%Y-%m-%d"); p = os.path.join(CACHE, ds + ".json")
    if os.path.exists(p):
        js = json.load(open(p))
    else:
        js = None
        for a in range(4):
            try:
                r = S.get("https://api.nasdaq.com/api/calendar/earnings", params={"date": ds}, timeout=40)
                NCALL[0] += 1
                if r.status_code == 200:
                    js = r.json(); break
                time.sleep(2 ** a + random.random())
            except Exception:
                time.sleep(2 ** a + random.random())
        time.sleep(0.6)
        if js is None:
            return None
        rows = ((js.get("data") or {}).get("rows")) or []
        js = {"date": ds, "rows": [{"symbol": x.get("symbol"), "time": x.get("time"), "eps": x.get("eps"),
                                    "epsForecast": x.get("epsForecast"), "surprise": x.get("surprise"),
                                    "fiscalQuarterEnding": x.get("fiscalQuarterEnding")} for x in rows]}
        json.dump(js, open(p, "w"))
    return {x["symbol"]: x for x in js["rows"] if x.get("symbol")}

def cached_index():
    """Önbellekteki tüm takvim günlerinden {hisse: {tarih: satır}} (ek istek gerektirmez)."""
    out = {}
    for fn in os.listdir(CACHE):
        if not fn.endswith(".json"): continue
        js = json.load(open(os.path.join(CACHE, fn)))
        d = pd.Timestamp(js["date"])
        for x in js["rows"]:
            if x.get("symbol") in thk.STOCKS:
                out.setdefault(x["symbol"], {})[d] = x
    return out

def main():
    """Verimli sürüm: (i) önbellekteki tüm günler taranır; (ii) hacim+boşluk adayı R için yalnız R-1 sorgulanır (bu 9 şirket
    duyuruyu seans sonrası yapar); (iii) >75 işlem günlük boşluklarda beklenen penceredeki en iyi 2 aday için R-1 sorgulanır;
    (iv) hâlâ eksik çeyrekler hacim+boşluk sıçramasından 'tahmini' işaretlenir (E = R-1)."""
    out = []
    for s in thk.STOCKS:
        df = thk.load_stock(s)
        idx = df.index
        vr = df["v"] / df["v"].rolling(50, min_periods=20).median().shift(1)
        gap = (df["o"] / df["c"].shift(1) - 1).abs()
        score = (vr.rank(pct=True) + gap.rank(pct=True)).fillna(0)
        nyr = (idx[-1] - idx[0]).days / 365.25
        ncand = int(nyr * 4 + 6)
        pos = {d: i for i, d in enumerate(idx)}
        chosen = []
        for d in score.sort_values(ascending=False).index:
            i = pos[d]
            if i < 1: continue
            if all(abs(i - j) >= 25 for j in chosen):
                chosen.append(i)
            if len(chosen) >= ncand: break
        found = {}
        ci = cached_index().get(s, {})
        for d, x in ci.items():
            if idx[0] <= d <= idx[-1]:
                found[d] = (x.get("time"), x.get("fiscalQuarterEnding"), x.get("eps"), x.get("epsForecast"), "takvim")
        def near(i, lo=-3, hi=1):
            return any((pos.get(d, -999) - i) in range(lo, hi + 1) for d in found)
        for i in sorted(chosen):
            if near(i): continue
            d = idx[i - 1]; m = cal(d)
            if m is not None and s in m:
                found[d] = (m[s].get("time"), m[s].get("fiscalQuarterEnding"), m[s].get("eps"), m[s].get("epsForecast"), "takvim")
        # boşluk doldurma (sınırlı)
        def gaps():
            fe = sorted(d for d in found if d in pos)
            pts = [-1] + [pos[d] for d in fe] + [len(idx) + 10]
            return [(a, b) for a, b in zip(pts[:-1], pts[1:]) if b - a > 75]
        tried = set()
        for a, b in gaps():
            lo = max(1, a + 50 if a >= 0 else 1); hi = min(len(idx) - 1, a + 75 if a >= 0 else b - 50)
            if hi <= lo: continue
            cand = score.iloc[lo:hi + 1].sort_values(ascending=False).index[:2]
            for R in cand:
                i = pos[R]
                if i in tried: continue
                tried.add(i)
                d = idx[i - 1]; m = cal(d)
                if m is not None and s in m:
                    found[d] = (m[s].get("time"), m[s].get("fiscalQuarterEnding"), m[s].get("eps"), m[s].get("epsForecast"), "takvim_pencere"); break
        # kalan boşluklar: tahmini
        for a, b in gaps():
            st_i = a
            while b - st_i > 75:
                lo = max(1, st_i + 50 if st_i >= 0 else 1); hi = min(len(idx) - 1, st_i + 72 if st_i >= 0 else b - 50)
                if hi <= lo or hi >= len(idx): break
                R = score.iloc[lo:hi + 1].idxmax(); i = pos[R]
                found[idx[i - 1]] = ("tahmini", None, None, None, "tahmini_hacim_bosluk")
                st_i = i
        for d, v in sorted(found.items()):
            out.append({"sym": s, "date": d.date(), "time": v[0], "fq": v[1], "eps": v[2], "eps_fc": v[3], "kaynak": v[4]})
        print(s, "aday", len(chosen), "bulunan", len(found), "tahmini", sum(1 for v in found.values() if v[4].startswith("tahmini")), "cagri", NCALL[0], flush=True)
    res = pd.DataFrame(out)
    res.to_csv(os.path.join(thk.OUT, "bilanco_tarihleri.csv"), index=False)
    print(res.groupby(["sym", "kaynak"]).size())
    print(res.groupby(["sym", pd.to_datetime(res["date"]).dt.year]).size().unstack().fillna(0).astype(int))

if __name__ == "__main__":
    main()
