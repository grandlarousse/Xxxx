"""Adv3: C1/C2 aykırı değer ve dağılım sağlamlığı, GLD/SPY aynı gün kontrolü, uygulama zamanı (15:30 ET girişi, saatlik veri),
yıllık P&L, en iyi N olay çıkarılınca; C3 parametre komşuluğu; C4 Ocak (GC=F 2001-07, ay sıralaması); C5 Bollinger duyarlılığı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_adv")
from adv_common import *
from scipy import stats
pd.set_option("display.width", 250)
M = cal_masks(idx); first, pre = M["first"], M["pre"]; basket = first | pre
R = {t: np.log(d[f"c_{t}"]).diff() for t in ["GDX", "GDXJ", "GLD", "SPY", "NUGT", "JNUG", "SLV"]}

print("=== C1/C2 dağılım sağlamlığı ===")
for nm, m, t in [("C1", basket, "GDXJ"), ("C1", basket, "GDX"), ("C2", pre, "GDX"), ("ilk", first, "GDXJ")]:
    r = R[t].dropna(); x = m.reindex(r.index).fillna(False)
    on = r[x]; off = r[~x]
    lo, hi = r.quantile([0.01, 0.99]); rw = r.clip(lo, hi)
    bw, tw, _ = nwt(rw, x.astype(float))
    srt = on.sort_values(ascending=False)
    drop5 = on.drop(srt.index[:5]); drop10 = on.drop(srt.index[:10])
    mw = stats.mannwhitneyu(on, off, alternative="greater").pvalue
    bn = stats.binomtest(int((on > 0).sum()), len(on), (off > 0).mean(), alternative="greater").pvalue
    print(f"{nm} {t}: n={len(on)} ort={on.mean()*1e4:.1f} medyan={on.median()*1e4:.1f} (diğer medyan {off.median()*1e4:.1f}) | winsor t={tw:.2f} | "
          f"en iyi 5 hariç ort={drop5.mean()*1e4:.1f} t~{drop5.mean()/drop5.std()*np.sqrt(len(drop5)):.2f} | en iyi 10 hariç ort={drop10.mean()*1e4:.1f} | MW p={mw:.4f} | isabet {(on>0).mean():.3f} vs {(off>0).mean():.3f} binom p={bn:.3f}")
    print("   en iyi 8 olay:", [(str(i.date()), round(v * 1e4)) for i, v in srt.head(8).items()])

print("\n=== GLD + SPY aynı gün kontrolü (madenci etkisi altın etkisinin betası mı?) ===")
for t in ["GDXJ", "GDX"]:
    dd = pd.concat([R[t].rename("y"), R["GLD"].rename("g"), R["SPY"].rename("s"), first.astype(float).rename("first"), pre.astype(float).rename("pre"), basket.astype(float).rename("bsk")], axis=1).dropna()
    for sub, q in [("tam", dd), ("IS", dd[dd.index <= IS_END]), ("OOS", dd[dd.index > IS_END])]:
        m1 = sm.OLS(q.y, sm.add_constant(q[["g", "s", "bsk"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        m2 = sm.OLS(q.y, sm.add_constant(q[["g", "s", "first", "pre"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        print(f"{t} {sub}: sepet {m1.params.bsk*1e4:.1f} bps t={m1.tvalues.bsk:.2f} (beta_GLD {m1.params.g:.2f}) | ilk {m2.params['first']*1e4:.1f} t={m2.tvalues['first']:.2f} | tatil {m2.params.pre*1e4:.1f} t={m2.tvalues.pre:.2f}")
    # GLD'nin kendi sepet etkisi
for t in ["GLD", "SPY", "SLV"]:
    for sub, a, b in [("tam", None, None), ("IS", None, "2017-12-31"), ("OOS", "2018-01-01", None)]:
        print(t, "sepet", sub, ev(basket, R[t], a, b))

print("\n=== Yıllık P&L C1 GDXJ (10 bps) ve çeyreklik ===")
net = bt_day(basket, R["GDXJ"], 10)
yr = net.groupby(net.index.year).sum() * 100
print(yr.round(1).to_dict(), "pozitif", int((yr > 0).sum()), "/", int(yr.notna().sum()))
ev_r = R["GDXJ"][basket.reindex(R["GDXJ"].index).fillna(False)].dropna()
print("olay günleri yıllık ort (bps):", (ev_r.groupby(ev_r.index.year).mean() * 1e4).round(0).to_dict())

print("\n=== Uygulama: 15:30 ET (saatlik) girişli olay getirisi, son 730 gün ===")
for t in ["GDXJ", "GDX"]:
    h = pd.read_parquet(f"{S}/panel/yahoo_h/{t}.parquet")
    h.index = pd.to_datetime(h.index, utc=True); et = h.index.tz_convert("America/New_York")
    h["et"] = et; h["d"] = et.normalize().tz_localize(None); h["hm"] = et.strftime("%H:%M")
    p1530 = h[h.hm == "15:30"].groupby("d").open.first()       # 15:30 ET fiyatı
    pclose_h = h[h.hm == "15:30"].groupby("d").close.first()  # saatlik son bar kapanışı (~16:00)
    y = yahoo(t); cl = y.close.reindex(p1530.index)
    dd = pd.DataFrame({"p1530": p1530, "c": cl}).dropna()
    dd["r_cc"] = np.log(dd.c).diff(); dd["r_1530"] = np.log(dd.p1530).diff()
    dd["last30"] = np.log(dd.c / dd.p1530)       # gün içi son 30 dk (giriş günü)
    m = basket.reindex(dd.index).fillna(False)
    entry = m.shift(-1).fillna(False).astype(bool)  # giriş günleri
    print(f"{t}: n_olay={int(m.sum())} cc ort={dd.r_cc[m].mean()*1e4:.1f} bps | 15:30->15:30 ort={dd.r_1530[m].mean()*1e4:.1f} bps | "
          f"giriş günü son 30dk ort={dd.last30[entry].mean()*1e4:.1f} (diğer {dd.last30[~entry].mean()*1e4:.1f}) | olay günü son30 {dd.last30[m].mean()*1e4:.1f}")

print("\n=== C3 komşuluk: GDX seri eşiği x ufuk (giriş t kapanışı, t-1'e kadar seri) ===")
for t in ["GDX", "GDXJ"]:
    r = R[t]; s = np.sign(r); k = s.groupby((s != s.shift()).cumsum()).cumsum()
    out = {}
    for thr in [3, 4, 5, 6, 7]:
        for lagk in [0, 1]:     # lagk=1: iddiadaki (t-1'e kadar seri, t kapanışında giriş); lagk=0: t kapanışında seri biter, t kapanışında giriş (15:00 ET kuralına aykırı, yalnız kıyas)
            sig = (k.shift(lagk) <= -thr).astype(float)
            for h in [1, 3, 5]:
                y = sum(r.shift(-j) for j in range(1, h + 1))
                b, tt, n = nwt(y, sig, max(h, 5))
                out[(thr, lagk, h)] = (round(tt, 2), int(sig.sum()), round(b * 1e4, 0))
    print(t, pd.Series(out).unstack(level=2).to_string())

print("\n=== C4 Ocak: ay sıralaması GLD (2008-26) ve GC=F 2001-07 bağımsız ===")
for nm, r in [("GLD", R["GLD"]), ("GC=F", np.log(yahoo("GC_F").adjclose).diff())]:
    for a, b in [("2001-01-01", "2007-12-31"), ("2008-01-01", "2026-12-31")]:
        q = r.loc[a:b].dropna()
        mm = q.groupby(q.index.month).mean() * 1e4
        tj = ev(pd.Series(q.index.month == 1, index=q.index), q)
        print(nm, a[:4], b[:4], "Ocak ort", round(mm[1], 1), "sıra", int(mm.rank(ascending=False)[1]), "/12", "t", tj["t"], "| ay ort bps:", mm.round(1).to_dict())
gc = np.log(yahoo("GC_F").adjclose).diff()
jy = gc[gc.index.month == 1].groupby(gc[gc.index.month == 1].index.year).sum() * 100
print("GC=F Ocak yıllık %:", jy.round(1).to_dict())

print("\n=== C5 Bollinger duyarlılığı GLD (z_{t-1}<thr, t kapanışında giriş, h gün) ===")
c = d.c_GLD; r = R["GLD"]
res = {}
for w in [10, 20, 50]:
    z = (c - c.rolling(w).mean()) / c.rolling(w).std()
    for thr in [-1.5, -2.0, -2.5]:
        sig = (z.shift(1) < thr).astype(float)
        for h in [1, 3, 5, 10]:
            y = sum(r.shift(-j) for j in range(1, h + 1))
            dd = pd.concat([y.rename("y"), sig.rename("x")], axis=1).dropna()
            _, tf, _ = nwt(dd.y, dd.x, max(h, 5)); _, ti, _ = nwt(dd.y[:IS_END], dd.x[:IS_END], max(h, 5)); _, to, _ = nwt(dd.y[IS_END:], dd.x[IS_END:], max(h, 5))
            res[(w, thr, h)] = f"{tf:.2f}/{ti:.2f}/{to:.2f}"
print(pd.Series(res).unstack(level=2).to_string())
# IAU ve GC=F 2005-07 aynı kural
for nm, cc in [("GC=F", yahoo("GC_F").adjclose), ("GLD_2005_07", yahoo("GLD").adjclose)]:
    rr = np.log(cc).diff(); z = (cc - cc.rolling(20).mean()) / cc.rolling(20).std()
    sig = (z.shift(1) < -2).astype(float); y = sum(rr.shift(-j) for j in range(1, 6))
    for a, b in [("2001-01-01", "2007-12-31"), ("2008-01-01", "2026-12-31")]:
        dd = pd.concat([y.rename("y"), sig.rename("x")], axis=1).dropna().loc[a:b]
        bb, tt, n = nwt(dd.y, dd.x, 5); print(nm, a[:4], b[:4], "BollZ<-2 h5: t", round(tt, 2), "olay", int(dd.x.sum()), "fark bps", round(bb * 1e4, 1))
