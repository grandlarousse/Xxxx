"""(2) komşuluk ızgarası k × q × H ; (3) rejim / yoğunlaşma."""
import numpy as np, pandas as pd
from adv_lib import *
R = us_returns(); e, B = rolling_resid(R); pv = viop(); r = pv.v_ret
bh = (np.exp(r) - 1).iloc[1:]
Ek = {k: e.rolling(k).sum() for k in (3, 5, 6, 8, 10, 12, 15, 20)}
def sigkq(k, q, hi="2017-12-31"):
    th = Ek[k][:hi].dropna().quantile(q); x, _ = map_us_to_viop(Ek[k], pv.index); return (x > th).astype(float)
print("=== IZGARA: fark NW t (lag max(h,10)); dönem 2018–2026 (eşik dışı) ve 2018–2024 ===")
for per, a, b in [("2018-2026", "2018", None), ("2018-2024", "2018", "2024"), ("2017-03..2026", None, None)]:
    for h in (1, 3, 5, 10):
        rows = {}
        for k in (3, 5, 6, 8, 10, 12, 15, 20):
            rows[f"k{k}"] = {f"q{int(q*100)}": round(nw_diff(fwd(r, h)[a:b], sigkq(k, q)[a:b], max(h, 10))["t"], 2) for q in (.6, .7, .75, .8, .85, .9)}
        D = pd.DataFrame(rows).T
        print(f"\n[{per}] h={h}  (medyan t {np.nanmedian(D.values):.2f}, >2 olan hücre {int((D.values>2).sum())}/{D.size}, seçilen k10/q80: {D.loc['k10','q80']})"); print(D.to_string())
print("\n=== SADE İŞLEM IZGARASI (5 bps): Sharpe / B&H alfa t ; 2018–2026 ===")
for metric in ("sharpe", "alpha_t", "ort_islem"):
    for q in (.7, .8, .9):
        rows = {}
        for k in (5, 8, 10, 12, 15, 20):
            s = sigkq(k, q); d = {}
            for H in (1, 2, 3, 4, 5, 7, 10):
                pos = position(s, H); p = pnl(pos, r, 5)["2018":]
                if metric == "sharpe": d[f"H{H}"] = round(sharpe(p), 2)
                elif metric == "alpha_t": d[f"H{H}"] = round(alpha(p, bh["2018":])[1], 2)
                else:
                    t = trades(pos["2018":], r["2018":], 5); d[f"H{H}"] = round(t[~t.open_].ret.mean() * 100, 2)
            rows[f"k{k}"] = d
        print(f"\n{metric}  q{int(q*100)}:"); print(pd.DataFrame(rows).T.to_string())
print("  B&H Sharpe 2018–2026:", round(sharpe(bh["2018":]), 2), "| tam:", round(sharpe(bh), 2))
# ---------- rejim
thr = Ek[10][:"2017-12-31"].dropna().quantile(.8); x, _ = map_us_to_viop(Ek[10], pv.index); sig = (x > thr).astype(float)
print("\n=== YIL YIL (k10,q80) ===")
f3, f5 = fwd(r, 3) * 100, fwd(r, 5) * 100
yy = pd.DataFrame({"sinyal_gun": sig.groupby(sig.index.year).sum().astype(int), "gun": sig.groupby(sig.index.year).size(),
                   "h3_sin": f3[sig > 0].groupby(f3[sig > 0].index.year).mean(), "h3_diger": f3[sig == 0].groupby(f3[sig == 0].index.year).mean(),
                   "h5_sin": f5[sig > 0].groupby(f5[sig > 0].index.year).mean(), "h5_diger": f5[sig == 0].groupby(f5[sig == 0].index.year).mean(),
                   "BH_yil%": (r.groupby(r.index.year).sum() * 100)})
yy["h3_fark"] = yy.h3_sin - yy.h3_diger; yy["h5_fark"] = yy.h5_sin - yy.h5_diger
print(yy.round(2).to_string()); print("h3 farkı pozitif yıl:", int((yy.h3_fark > 0).sum()), "/", len(yy), "| h5:", int((yy.h5_fark > 0).sum()), "/", len(yy))
for H in (3, 5):
    pos = position(sig, H)
    for c in (5,):
        p = pnl(pos, r, c); t = trades(pos, r, c); tc = t[~t.open_].copy(); tc["yil"] = tc.entry.dt.year
        g = tc.groupby("yil").ret.agg(["size", "mean", "sum", "min", lambda z: (z > 0).mean()]); g.columns = ["n", "ort", "toplam", "enkotu", "kazanan"]
        g["strateji_yil%"] = p.groupby(p.index.year).apply(lambda z: (1 + z).prod() - 1) * 100; g["BH_yil%"] = bh.groupby(bh.index.year).apply(lambda z: (1 + z).prod() - 1) * 100
        g["piyasada%"] = pos.groupby(pos.index.year).mean() * 100
        g[["ort", "toplam", "enkotu"]] *= 100
        print(f"\n--- H={H}, {c} bps: işlemler yıl yıl ---"); print(g.round(2).to_string())
        tot = tc.ret.sum()
        print(f"  {len(tc)} işlem, toplam (basit toplam) %{tot*100:.1f}; ort %{tc.ret.mean()*100:.2f}; medyan %{tc.ret.median()*100:.2f}; kazanan %{(tc.ret>0).mean()*100:.0f}; en kötü %{tc.ret.min()*100:.1f}")
        srt = tc.sort_values("ret", ascending=False)
        for n in (3, 5, 10):
            rest = srt.iloc[n:]
            print(f"  en iyi {n} işlem çıkarılınca: kalan {len(rest)} işlem ort %{rest.ret.mean()*100:.2f} (t {rest.ret.mean()/rest.ret.std()*np.sqrt(len(rest)):.2f}), toplamın %{srt.iloc[:n].ret.sum()/tot*100:.0f}'i bu {n} işlemde")
        print("  en iyi 5:", [(str(a.date()), int(d), round(b * 100, 1)) for a, d, b in srt.head(5)[["entry", "days", "ret"]].values])
        print("  en kötü 5:", [(str(a.date()), int(d), round(b * 100, 1)) for a, d, b in srt.tail(5)[["entry", "days", "ret"]].values])
        print("  2025–26 payı: toplam getirinin %", round(tc[tc.yil >= 2025].ret.sum() / tot * 100), "| 2017+2020:", round(tc[tc.yil.isin([2017, 2020])].ret.sum() / tot * 100), "| 2018–2024 toplam %", round(tc[(tc.yil >= 2018) & (tc.yil <= 2024)].ret.sum() * 100, 1), "n", int(((tc.yil >= 2018) & (tc.yil <= 2024)).sum()))
        for nm, a, b in [("tam", None, None), ("2017-21", None, "2021"), ("2018-26", "2018", None), ("2018-24", "2018", "2024"), ("2022-24", "2022", "2024"), ("2025-26", "2025", None), ("2026 hariç", None, "2025")]:
            al = alpha(p[a:b], bh[a:b])
            print(f"   {nm:10s} Sharpe {sharpe(p[a:b]):5.2f} | B&H {sharpe(bh[a:b]):5.2f} | alfa %{al[0]:5.1f} t {al[1]:5.2f} beta {al[2]:.2f} | piyasada %{pos[a:b].mean()*100:.0f}")
# rejim: altın oynaklığı / trend ile koşullu
vol20 = r.rolling(20).std().shift(1) * np.sqrt(252) * 100
print("\n=== REJİM: önceki 20 günlük gerçekleşen oynaklık üçte birlik dilimlerine göre h5 fark ===")
qs = vol20.quantile([1/3, 2/3]).values
for nm, m in [("düşük vol", vol20 <= qs[0]), ("orta", (vol20 > qs[0]) & (vol20 <= qs[1])), ("yüksek vol", vol20 > qs[1])]:
    q5 = nw_diff(fwd(r, 5)[m], sig[m], 10); q3 = nw_diff(fwd(r, 3)[m], sig[m], 10)
    print(f"  {nm:10s} n_sin {q5['n1']:4d}/{q5['N']}  h3 fark {q3['diff']:+.3f}% (t {q3['t']:.2f})  h5 fark {q5['diff']:+.3f}% (t {q5['t']:.2f})")
print("  yıllık medyan vol20:", vol20.groupby(vol20.index.year).median().round(1).to_dict())
# 2022-24 etkisi tam örneklem etkisinden istatistiksel olarak farklı mı?
import statsmodels.api as sm
for h in (3, 5):
    d = pd.DataFrame({"y": fwd(r, h), "s": sig}).dropna(); d["m"] = ((d.index.year >= 2022) & (d.index.year <= 2024)).astype(float); d["sm"] = d.s * d.m
    m = sm.OLS(d.y, sm.add_constant(d[["s", "m", "sm"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
    print(f"  h{h}: etkileşim (2022–24'te fark eksi diğer yıllarda fark) {m.params['sm']*100:+.3f}% t {m.tvalues['sm']:.2f} | diğer yıllarda fark {m.params['s']*100:+.3f}% t {m.tvalues['s']:.2f}")
    d["m2"] = (d.index.year >= 2025).astype(float); d["sm2"] = d.s * d.m2
    m = sm.OLS(d.y, sm.add_constant(d[["s", "m2", "sm2"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
    print(f"  h{h}: 2025–26 dışı fark {m.params['s']*100:+.3f}% t {m.tvalues['s']:.2f} | 2025–26 ek fark {m.params['sm2']*100:+.3f}% t {m.tvalues['sm2']:.2f}")
