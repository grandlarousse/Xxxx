"""b0_bilanco.py'nin 2. geçişi: 'tahmini' işaretli çeyrekler için, aynı hissenin doğrulanmış duyurularının yılın gününe göre
medyanı (aynı çeyrek) etrafında ±6 takvim günü içindeki işlem günleri yakınlık sırasıyla takvimde sorgulanır (önbellek ortak;
çeyrek başına en fazla 9 istek). Bulunursa kaynak='takvim_pencere2', bulunamazsa 'tahmini' kalır.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/b0b_bilanco_pencere.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, b0_bilanco as b0

P = os.path.join(thk.OUT, "bilanco_tarihleri.csv")
B = pd.read_csv(P, parse_dates=["date"])
def qkey(d):  # rapor penceresi: Oca-Mar -> 1, Nis-Haz -> 2, Tem-Eyl -> 3, Eki-Ara -> 4
    return (d.month - 1) // 3 + 1
out = []
for s in thk.STOCKS:
    sb = B[B.sym == s].copy()
    idx = thk.load_stock(s).index
    conf = sb[~sb.kaynak.str.startswith("tahmini")]
    med = {q: int(np.median([d.dayofyear for d in conf.date if qkey(d) == q])) for q in range(1, 5)
           if any(qkey(d) == q for d in conf.date)}
    for _, r in sb.iterrows():
        if not r.kaynak.startswith("tahmini"):
            out.append(r.to_dict()); continue
        q = qkey(r.date); y = r.date.year
        if q not in med:
            out.append(r.to_dict()); continue
        center = pd.Timestamp(y, 1, 1) + pd.Timedelta(days=med[q] - 1)
        cands = [d for d in idx if abs((d - center).days) <= 6]
        cands = sorted(cands, key=lambda d: abs((d - center).days))[:9]
        hit = None
        for d in cands:
            m = b0.cal(d)
            if m is not None and s in m:
                hit = (d, m[s]); break
        if hit:
            d, x = hit
            out.append({"sym": s, "date": d, "time": x.get("time"), "fq": x.get("fiscalQuarterEnding"), "eps": x.get("eps"),
                        "eps_fc": x.get("epsForecast"), "kaynak": "takvim_pencere2"})
        else:
            out.append(r.to_dict())
    print(s, "tahmini kalan:", sum(1 for o in out if o["sym"] == s and str(o["kaynak"]).startswith("tahmini")), "istek", b0.NCALL[0], flush=True)
R = pd.DataFrame(out)
R["date"] = pd.to_datetime(R["date"]).dt.date
R = R.drop_duplicates(["sym", "date"]).sort_values(["sym", "date"])
R.to_csv(P, index=False)
print(R.groupby(["sym", "kaynak"]).size())

# 3. adım (ağsız): kalan 'tahmini' satırlar için önbellekteki takvim günlerinde ±10 takvim günü içinde aynı hisse varsa onu kullan
ci = b0.cached_index()
R = pd.read_csv(P, parse_dates=["date"])
fix = 0
for i, r in R[R.kaynak.str.startswith("tahmini")].iterrows():
    near = [d for d in ci.get(r.sym, {}) if abs((d - r.date).days) <= 10]
    if near:
        d = min(near, key=lambda x: abs((x - r.date).days)); x = ci[r.sym][d]
        R.loc[i, ["date", "time", "fq", "eps", "eps_fc", "kaynak"]] = [d, x.get("time"), x.get("fiscalQuarterEnding"), x.get("eps"), x.get("epsForecast"), "takvim_onbellek"]
        fix += 1
R["date"] = pd.to_datetime(R["date"]).dt.date
R = R.drop_duplicates(["sym", "date"]).sort_values(["sym", "date"])
R.to_csv(P, index=False)
print("önbellekten düzeltilen:", fix, "| kalan tahmini:", int(R.kaynak.str.startswith("tahmini").sum()))
