"""Adv4: C6 gece/gün içi — varyans payıyla orantılı beklentiye karşı test, açılış verisi kalitesi; çoklu test (Bonferroni/BH, sepet seçimi);
öncesi-2008 madenci sepeti altın (GC=F) + SPX kontrollü; hit-rate kalite kontrolü."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_adv")
from adv_common import *
from scipy import stats
pd.set_option("display.width", 250)
print("=== C6: gece/gün içi, varyans-orantılı beklenti ===")
for t in ["GLD", "GDX", "GDXJ", "SLV"]:
    y = yahoo(t).reindex(idx)
    tot = np.log(y.adjclose).diff(); intra = np.log(y.close / y.open); night = tot - intra
    dd = pd.DataFrame({"n": night, "i": intra, "t": tot}).dropna()
    stale = (y.open == y.close.shift(1)).mean()
    for sub, q in [("tam", dd), ("IS", dd[:IS_END]), ("OOS", dd[IS_END:])]:
        vn, vi = q.n.var(), q.i.var(); share_n = vn / (vn + vi)
        exp_i = q.t.mean() * (1 - share_n)          # varyans payıyla orantılı beklenen gün içi ortalama
        diff = q.i - (1 - share_n) * q.t            # gün içi - beklenen pay
        b, tt, _ = nwt(diff, pd.Series(1.0, index=diff.index) * 0 + 1) if False else (None, None, None)
        se = diff.std() / np.sqrt(len(diff)); tdiff = diff.mean() / se
        print(f"{t} {sub}: gece {q.n.mean()*252*100:.1f}%/y gün içi {q.i.mean()*252*100:.1f}%/y | gece varyans payı {share_n:.2f} | beklenen gün içi {exp_i*252*100:.1f}%/y | (gün içi - beklenen) t={tdiff:.2f} | open==önceki close oranı {stale:.3f}")

print("\n=== Çoklu test ===")
K = pd.read_csv(f"{S}/out/e1_etf_zaman_takvim/kayit_fdr_ongorucu.csv")
K["p2"] = 2 * stats.norm.sf(K.t.abs())
n = len(K); print("test sayısı", n, "| Bonferroni %5 eşiği |t| >", round(stats.norm.isf(0.025 / n), 2), "| en büyük |t|", round(K.t.abs().max(), 2))
for tid in ["c_tom|GDXJ|ayin_ilk_gunu|h1", "c_hol|GDX|tatil_oncesi_gun|h1", "c_hol|GDXJ|tatil_oncesi_gun|h1", "a3_os|GDX|streak<=-5|h1", "c_month|GLD|ay=01|h1", "a_boll|GLD|strict|Boll2_revert|h5"]:
    r = K[K.test_id == tid]
    if len(r): r = r.iloc[0]; print(f"{tid}: t={r.t:.2f} p={r.p2:.4f} Bonf={min(1, r.p2*n):.3f} q_pred={r.q_pred:.3f}")
# sepet t=4.25 sanki ek test: p ve Bonferroni (n+1), ve takvim ailesi içinde (195 test) Bonferroni
for tv, lab in [(4.25, "sepet GDXJ t=4.25"), (2.62, "sepet GDXJ IS t=2.62")]:
    p = 2 * stats.norm.sf(tv); print(f"{lab}: p={p:.2e} Bonf(1047)={min(1,p*1047):.3f} Bonf(195 takvim)={min(1,p*195):.3f}")
# null altında 1046 testte beklenen en büyük |t| (bağımsız varsayım)
sim = np.abs(np.random.default_rng(0).standard_normal((2000, n))).max(axis=1)
print("bağımsız null altında max|t| medyan", round(np.median(sim), 2), "%95", round(np.quantile(sim, 0.95), 2))
# takvim ailesinde (c_*) ikili birleşim seçimi: 168 getiri günü testinden en iyi ikisinin birleşimi null dağılımı (yaklaşık) — permütasyon
C = pd.read_csv(f"{S}/out/e1_etf_zaman_takvim/c_takvim_testleri.csv")
print("takvim h=1 testleri:", (C.h == 1).sum(), " |t|>=2:", int((C[C.h == 1].t.abs() >= 2).sum()), " beklenen ~", round((C.h == 1).sum() * 0.0455, 1))

print("\n=== Öncesi-2008 madenci EW: GC=F + ^GSPC kontrollü (2001-2007) ve isabet kalite kontrolü ===")
gs = yahoo("_GSPC"); NY = gs.index[gs.index >= "1981-01-01"]; Mn = cal_masks(NY)
RR = {}
for t in ["NEM", "AEM", "GFI", "KGC", "CDE", "HL", "RGLD", "HMY", "AU", "PAAS", "SSRM"]:
    y = yahoo(t).reindex(NY); r = np.log(y.adjclose).diff(); r[(y.volume.fillna(0) <= 0)] = np.nan; r[r.abs() > 0.5] = np.nan; RR[t] = r
RR = pd.DataFrame(RR); EW = RR.mean(axis=1).where(RR.notna().sum(axis=1) >= 3)
zero = (RR == 0).sum(axis=1) / RR.notna().sum(axis=1)
print("tek hisse sıfır getiri oranı (yıllık ort):", zero.groupby(NY.year).mean().round(2).loc[1983:2008:5].to_dict())
gc = np.log(yahoo("GC_F").adjclose).diff().reindex(NY); spx = np.log(gs.adjclose.reindex(NY)).diff()
dd = pd.concat([EW.rename("y"), gc.rename("g"), spx.rename("s"), Mn["first"].astype(float).rename("first"), Mn["pre"].astype(float).rename("pre"), (Mn["first"] | Mn["pre"]).astype(float).rename("bsk")], axis=1).dropna()
for a, b in [("2001", "2007"), ("2008", "2026")]:
    q = dd.loc[a:b]
    for cols in [["bsk"], ["s", "bsk"], ["g", "s", "bsk"], ["g", "s", "first", "pre"]]:
        m = sm.OLS(q.y, sm.add_constant(q[cols])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        print(a, b, cols, {c: (round(m.params[c] * (1e4 if c in ('bsk', 'first', 'pre') else 1), 2), round(m.tvalues[c], 2)) for c in cols})
q = dd.loc["1983":"2007"]
for c in ["first", "pre", "bsk"]:
    on = q.y[q[c] == 1]; off = q.y[q[c] == 0]
    print(f"1983-2007 EW {c}: isabet {(on>0).mean():.3f} vs diğer {(off>0).mean():.3f} | ort {on.mean()*1e4:.1f} vs {off.mean()*1e4:.1f} | medyan {on.median()*1e4:.1f} vs {off.median()*1e4:.1f} | MW p(büyük)={stats.mannwhitneyu(on, off, alternative='greater').pvalue:.3f}")
# 1983-2007 yıl yıl EW sepet olay ort (bps)
e = q.y[q.bsk == 1]; print("EW sepet olay günleri yıllık ort bps:", (e.groupby(e.index.year).mean() * 1e4).round(0).to_dict())
e = q.y[q.pre == 1]; print("EW tatil öncesi yıllık ort bps:", (e.groupby(e.index.year).mean() * 1e4).round(0).to_dict(), "pozitif yıl", int((e.groupby(e.index.year).mean() > 0).sum()), "/", e.index.year.nunique())
