"""(2b) Sinyal kapanış yerine 17:40 / 17:50 / 17:55 (m5, 2026-08+) ya da 17:30 (h1, 2025-11+) fiyatıyla hesaplanırsa ne değişir?
Yalnız BUGÜNÜN getirisi değişir: r'_t = r_t − ε_t, ε_t = log(kapanış_t / P_saat,t). Önceki günler tam kapanışla bilinir.
(a) Pencere içi doğrudan karşılaştırma (sinyal uyumu + P0L işlemleri).
(b) Tam geçmiş Monte Carlo: pencereden ölçülen standartlaştırılmış ε_u (= ε_M − β_g·ort(ε_A, ε_E)) / σ60 gün bazında
    yeniden örneklenip z3'e eklenir; P0L kuralı 300 kez koşulur (gürültü bağımsız varsayımı — kapanış müzayedesi hareketinin
    ileri getiriyle ilişkisi (a)'da ayrıca ölçülür)."""
import numpy as np, pandas as pd
import kl
from kl import C


cal = kl.use_ext_panel()
R = pd.DataFrame({s: kl.spot_ret_fresh(s) for s in ['TRMET', 'TRALT', 'TRENJ', 'XU030']})
SIG = kl.koza_signal(R, 'TRMET')
SYM = ['TRMET', 'TRALT', 'TRENJ']
CL = pd.DataFrame({s: kl.spot_fresh(s)['c'] for s in SYM})


def intraday_px(kind, hhmm_start):
    out = {}
    for s in SYM:
        m = pd.read_parquet(f'{kl.DL}/{kind}/{s}.IS.parquet'); t = m.index.tz_convert('Europe/Istanbul')
        m = m[t.strftime('%H:%M') == hhmm_start]; m.index = pd.DatetimeIndex(t[t.strftime('%H:%M') == hhmm_start].date)
        out[s] = m['c']
    return pd.DataFrame(out)


VAR = {'17:40 (m5, TV 15 dk gecikmeli 17:55 görünümü)': ('m5', '17:35'), '17:50 (m5)': ('m5', '17:45'), '17:55 (m5)': ('m5', '17:50'),
       '17:30 (h1)': ('h1', '16:30')}
# P0L simülatörünü k2'den al (aynı kod)
src = open(kl.OUT + '/kod/k2_pratik.py').read().split('RES = []')[0]
g = {}; exec(compile(src, 'k2', 'exec'), g)
simulate, report, tstat = g['simulate'], g['report'], g['tstat']
rows = []; EPS = {}
for name, (kind, hh) in VAR.items():
    P = intraday_px(kind, hh).reindex(CL.index).dropna()
    eps = np.log(CL.reindex(P.index) / P)  # kapanış / saat fiyatı
    eu = eps.TRMET - SIG.b_g.reindex(P.index) * (eps.TRALT + eps.TRENJ) / 2
    q = (eu / SIG.sd60.reindex(P.index)).dropna(); EPS[name] = q
    s2 = SIG.copy()
    u2 = s2.u.copy(); u2.loc[q.index] = u2.loc[q.index] - eu.loc[q.index]
    # z3' = (u_{t-2}+u_{t-1}+u'_t)/(σ60_t√3)
    s2['z3'] = (SIG.u.shift(1) + SIG.u.shift(2) + u2) / (SIG.sd60 * np.sqrt(3))
    s2.loc[~s2.index.isin(q.index), 'z3'] = SIG.z3[~SIG.index.isin(q.index)]
    w = q.index
    a0 = np.where(SIG.z3.reindex(w).abs() > 1.5, np.sign(SIG.z3.reindex(w)), 0); a1 = np.where(s2.z3.reindex(w).abs() > 1.5, np.sign(s2.z3.reindex(w)), 0)
    corr = np.corrcoef(SIG.z3.reindex(w), s2.z3.reindex(w))[0, 1]
    # kapanış müzayedesi hareketi (ε_u) ile ileri 2 günlük çift getirisi ilişkisi (pencere içi)
    fwd = (C.fut('TRMET').fwd(w, 2, 'E0') - SIG.bH.reindex(w).values * C.fut('TRALT').fwd(w, 2, 'E0')) / (1 + SIG.bH.reindex(w).values)
    ok = np.isfinite(fwd) & np.isfinite(eu.reindex(w).values)
    ce = np.corrcoef(eu.reindex(w).values[ok], fwd[ok])[0, 1] if ok.sum() > 10 else np.nan
    T0 = simulate(SIG, lock=True); T1 = simulate(s2, lock=True)
    T0w = T0[(T0.entry >= w.min()) & T0.gross.notna()]; T1w = T1[(T1.entry >= w.min()) & T1.gross.notna()]
    same = len(set(T0w.entry) & set(T1w.entry))
    rows.append(dict(var=name, gun=len(w), ilk=str(w.min().date()), son=str(w.max().date()), sd_q=q.std(), corr_z=corr,
                     uyum=(a0 == a1).mean(), sinyal_kapanis=int((a0 != 0).sum()), sinyal_saat=int((a1 != 0).sum()),
                     yalniz_kapanis=int(((a0 != 0) & (a1 == 0)).sum()), yalniz_saat=int(((a1 != 0) & (a0 == 0)).sum()), ters=int((a0 * a1 < 0).sum()),
                     islem_kapanis=len(T0w), islem_saat=len(T1w), ortak_giris=same,
                     brut_kapanis=T0w.gross.mean(), brut_saat=T1w.gross.mean(), corr_eps_fwd=ce))
pd.set_option('display.width', 250)
D = pd.DataFrame(rows); print(D.round(3).to_string(index=False))
D.to_csv(kl.OUT + '/kod/res_1755_pencere.csv', index=False)
# (b) Monte Carlo — tam geçmiş
rng = np.random.default_rng(7)
mc = []
base = report('P0L kapanış sinyali (karşılaştırma tabanı)', simulate(SIG, lock=True))
for name in ['17:55 (m5)', '17:40 (m5, TV 15 dk gecikmeli 17:55 görünümü)', '17:30 (h1)']:
    q = EPS[name].values; res = []
    for rep in range(300):
        s2 = SIG.copy()
        qq = rng.choice(q, len(s2))
        s2['z3'] = SIG.z3 - qq / np.sqrt(3)
        T = simulate(s2, lock=True).dropna(subset=['gross'])
        res.append((len(T), T.gross.mean(), T.net15t.mean(), tstat(T.gross), T[T.entry >= '2024-01-01'].gross.mean()))
    res = np.array(res)
    mc.append(dict(var=name, sd_q=q.std(), n_ort=res[:, 0].mean(), brut_ort=res[:, 1].mean(), brut_p05=np.percentile(res[:, 1], 5),
                   brut_p95=np.percentile(res[:, 1], 95), net15t_ort=res[:, 2].mean(), t_ort=res[:, 3].mean(), y2426_ort=res[:, 4].mean()))
M = pd.DataFrame(mc); print('\nMonte Carlo (300 tekrar, P0L kuralı, 2019–2026):'); print(M.round(2).to_string(index=False))
print(f"Taban (kapanış): n {base['n']}, brüt {base['gross']:+.1f}, net15+tik {base['net15t']:+.1f}, t {base['t']:.2f}, 2024–26 {base['y2426']:+.1f}")
M.to_csv(kl.OUT + '/kod/res_1755_mc.csv', index=False)
