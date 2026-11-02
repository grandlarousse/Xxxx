"""TVF (Türkiye Varlık Fonu) ortak faktörü:
(1) 47 VİOP hissesi arası XU100-kontrollü kısmi korelasyon matrisi -> pc_ij ~ aynı_sektör + ikisi_de_TVF + ikisi_de_banka ... (OLS, çift düzeyi; klasik SE iyimser -> yıllık tekrar ile kontrol)
(2) Fark-içinde-fark: hisse TVF'ye girince (THYAO/HALKB 2017-02, TCELL 2020-10, TTKOM 2022-03, VAKBN 2023?, TRALT/TRMET 2024-08) mevcut TVF üyeleriyle pc arttı mı (kontrol: TVF dışı aynı sektör)?
(3) Stres günlerinde (XU100 < -%3) TVF sepeti vs TVF dışı: aynı gün ve ertesi gün göreli getiri (devlet desteği hipotezi)
(4) Öncülük: TVF sepeti artığı_{t-1} -> üye artığı gün-içi_t"""
from gx import *
V = ll.VIOP
SECT = {'AKBNK':'bank','GARAN':'bank','HALKB':'bank','ISCTR':'bank','VAKBN':'bank','YKBNK':'bank','TSKB':'bank',
 'KCHOL':'hold','SAHOL':'hold','DOHOL':'hold','ALARK':'hold','AGHOL':'hold','TKFEN':'hold','ENKAI':'cons',
 'THYAO':'air','PGSUS':'air','TAVHL':'air','TCELL':'tel','TTKOM':'tel','EREGL':'steel','KRDMD':'steel','BRSAN':'steel',
 'TUPRS':'oil','PETKM':'chem','SASA':'chem','HEKTS':'chem','GUBRF':'chem','AKSEN':'util','ENJSA':'util','ODAS':'util','ASTOR':'util',
 'CIMSA':'cem','OYAKC':'cem','SISE':'glass','BIMAS':'retail','MGROS':'retail','SOKM':'retail','AEFES':'food','ULKER':'food',
 'FROTO':'auto','TOASO':'auto','DOAS':'auto','ARCLK':'dur','VESTL':'dur','ASELS':'def','EKGYO':'re','TRALT':'gold','TRMET':'gold'}
TVFJOIN = {'THYAO':'2017-02-06','HALKB':'2017-02-06','TCELL':'2020-10-22','TTKOM':'2022-03-11','VAKBN':'2023-03-01','TRALT':'2024-08-20','TRMET':'2024-08-20'}
# VAKBN: TVF payı (Hazine->TVF) tarihi kesin değil (~2023); TURSG VİOP'ta değil -> ayrı.
rets = pd.concat({s: R(s) for s in V}, axis=1); m = R('XU100')
rets = rets[rets.index >= '2014-01-01']
def resid(df, mm):
    out = {}
    for c in df:
        x = pd.concat([df[c], mm], axis=1).dropna()
        if len(x) < 250: continue
        b = x.iloc[:, 0].rolling(250, min_periods=120).cov(x.iloc[:, 1]) / x.iloc[:, 1].rolling(250, min_periods=120).var()
        out[c] = x.iloc[:, 0] - b.shift(1) * x.iloc[:, 1]
    return pd.DataFrame(out)
E = resid(rets, m)
E.to_parquet(HERE + '/tvf_resid.parquet')
def pcmat(E, lo, hi):
    X = E[(E.index >= lo) & (E.index < hi)]
    return X.corr(min_periods=200)
rows = []
for per, lo, hi in [('2014-2016', '2014-01-01', '2017-02-06'), ('2017-2020', '2017-02-06', '2020-10-22'), ('2020-2022', '2020-10-22', '2022-03-11'), ('2022-2024', '2022-03-11', '2024-08-20'), ('2024-2026', '2024-08-20', '2026-11-01'), ('ALL', '2014-01-01', '2026-11-01')]:
    C = pcmat(E, lo, hi); mid = pd.Timestamp(lo) + (pd.Timestamp(hi) - pd.Timestamp(lo)) / 2
    tv = {s for s, d in TVFJOIN.items() if pd.Timestamp(d) <= pd.Timestamp(lo) + pd.Timedelta(days=1)} if per != 'ALL' else {'THYAO','HALKB','TCELL','TTKOM','VAKBN'}
    for i, a in enumerate(C.index):
        for b in C.columns[i + 1:]:
            v = C.loc[a, b]
            if np.isnan(v): continue
            rows.append(dict(per=per, a=a, b=b, pc=v, same_sec=int(SECT.get(a) == SECT.get(b)), both_tvf=int(a in tv and b in tv), one_tvf=int((a in tv) ^ (b in tv)),
                             both_bank=int(SECT.get(a) == 'bank' and SECT.get(b) == 'bank'), state_bank=int({a, b} <= {'HALKB', 'VAKBN'}), ntvf=len(tv)))
P = pd.DataFrame(rows); P.to_csv(HERE + '/res_tvf_pairs.csv', index=False)
import statsmodels.formula.api as smf
print('--- pc ~ same_sec + both_bank + both_tvf + one_tvf (pair-level OLS, cluster-robust by stock a) ---')
for per in P.per.unique():
    X = P[P.per == per]
    if X.both_tvf.sum() == 0:
        mm_ = smf.ols('pc ~ same_sec + both_bank', X).fit(); print(per, 'TVF üye çifti yok; n', len(X)); continue
    mm_ = smf.ols('pc ~ same_sec + both_bank + both_tvf + one_tvf', X).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(X['a'])[0]})
    print(per, 'n', len(X), 'nTVF', X.ntvf.iloc[0], 'both_tvf b=%.3f t=%.2f | one_tvf b=%.3f t=%.2f | same_sec %.3f | both_bank %.3f' % (mm_.params['both_tvf'], mm_.tvalues['both_tvf'], mm_.params['one_tvf'], mm_.tvalues['one_tvf'], mm_.params['same_sec'], mm_.params['both_bank']))
# TVF-dışı cross-sector örnek: TVF-TVF çiftleri (farklı sektör) vs ortalama farklı-sektör çift
X = P[P.per == 'ALL']
print('ALL: TVF-TVF farklı sektör çiftleri:'); print(X[(X.both_tvf == 1)][['a', 'b', 'pc', 'same_sec']].round(3).to_string())
print('ALL: farklı sektör ortalama pc (TVF dışı):', round(X[(X.both_tvf == 0) & (X.same_sec == 0)].pc.mean(), 3), ' TVF-TVF farklı sektör:', round(X[(X.both_tvf == 1) & (X.same_sec == 0)].pc.mean(), 3))
# (2) DiD: katılan hisse ile mevcut TVF üyeleri arası pc: önce/sonra (±2 yıl), kontrol = aynı hissenin TVF dışı farklı sektör hisselerle pc'si
print('--- DiD (katılım ±500 gün) ---')
did = []
for s, d in TVFJOIN.items():
    d = pd.Timestamp(d); pre = E[(E.index >= d - pd.Timedelta(days=730)) & (E.index < d)]; post = E[(E.index >= d) & (E.index < d + pd.Timedelta(days=730))]
    mem = [k for k, dd in TVFJOIN.items() if pd.Timestamp(dd) < d and k != s and k in E]
    if s in ('THYAO', 'HALKB'): mem = ['HALKB' if s == 'THYAO' else 'THYAO']
    ctrl = [k for k in E.columns if k not in TVFJOIN and SECT.get(k) != SECT.get(s) and k not in mem]
    if not mem or s not in E: continue
    f = lambda X, L: np.nanmean([X[s].corr(X[k]) for k in L])
    o = dict(stock=s, date=d.date(), members=','.join(mem), pc_mem_pre=f(pre, mem), pc_mem_post=f(post, mem), pc_ctrl_pre=f(pre, ctrl), pc_ctrl_post=f(post, ctrl))
    o['did'] = (o['pc_mem_post'] - o['pc_mem_pre']) - (o['pc_ctrl_post'] - o['pc_ctrl_pre']); did.append(o)
DID = pd.DataFrame(did); print(DID.round(3).to_string()); DID.to_csv(HERE + '/res_tvf_did.csv', index=False)
# (3) Stres günleri
tv_now = ['THYAO', 'HALKB', 'TCELL', 'TTKOM', 'VAKBN']
non = [k for k in E.columns if k not in TVFJOIN and SECT.get(k) not in ('gold',)]
def basket(names, since_join=True):
    cols = []
    for k in names:
        x = rets[k].copy()
        if since_join and k in TVFJOIN: x[x.index < pd.Timestamp(TVFJOIN[k])] = np.nan
        cols.append(x)
    return pd.concat(cols, axis=1).mean(axis=1)
tvb = basket(tv_now); nb = rets[non].mean(axis=1)
# sektör eşlemeli kontrol: GARAN/AKBNK/YKBNK/ISCTR (HALKB/VAKBN için), PGSUS (THYAO), TCELL<->TTKOM yok -> ASELS? (yok) => basit: banka kontrolü + PGSUS
ctrlb = pd.concat([rets[['GARAN','AKBNK','YKBNK','ISCTR']].mean(axis=1), rets['PGSUS']], axis=1).mean(axis=1)
dd = pd.concat([tvb.rename('tvf'), nb.rename('non'), ctrlb.rename('ctrl'), m.rename('m')], axis=1).dropna()
dd = dd[dd.index >= '2017-02-06']
dd['rel'] = dd.tvf - dd.non; dd['rel_c'] = dd.tvf - dd.ctrl
for thr in [-0.03, -0.05]:
    S0 = dd[dd.m < thr]; S1 = dd.shift(-1)[dd.m < thr]
    print(f'XU100<{thr}: n={len(S0)} aynı gün TVF-diğer {1e4*S0.rel.mean():.0f} bps (t={ll.nw_t(S0.rel)[1]:.2f}); TVF-sektör kontrol {1e4*S0.rel_c.mean():.0f} bps (t={ll.nw_t(S0.rel_c)[1]:.2f}) | ertesi gün TVF-diğer {1e4*S1.rel.mean():.0f} bps (t={ll.nw_t(S1.rel)[1]:.2f}), TVF-sektör {1e4*S1.rel_c.mean():.0f} (t={ll.nw_t(S1.rel_c)[1]:.2f})')
# aşağı/yukarı beta
for nm, sub in [('down', dd[dd.m < 0]), ('up', dd[dd.m > 0])]:
    print(nm, 'beta TVF %.3f, diğer %.3f, sektör kontrol %.3f' % tuple(np.polyfit(sub.m, sub[c], 1)[0] for c in ['tvf', 'non', 'ctrl']))
dd.to_parquet(HERE + '/tvf_basket.parquet')
# (4) Öncülük: TVF sepet artığı_{t-1} (üye hariç) -> üye artığı (cc / gün içi)
print('--- TVF sepeti (üye hariç) artığı t-1 -> üye t ---')
for s in tv_now:
    oth = [k for k in tv_now if k != s]
    eb = E[oth].mean(axis=1); d1 = DC(s)
    X = pd.concat([E[s].rename('y'), d1['intra'].rename('yi'), eb.shift(1).rename('x1'), E[s].shift(1).rename('y1'), m.shift(1).rename('m1')], axis=1)
    X = X[X.index >= TVFJOIN[s]]
    r1 = nwreg(X['y'], X[['x1', 'y1', 'm1']]); r2 = nwreg(X['yi'], X[['x1', 'y1', 'm1']])
    pcs = E[[s] + oth][E.index >= TVFJOIN[s]].corr().loc[s, oth].mean()
    print(s, 'pc(üye, diğer TVF artık) ort %.3f | cc t=%.2f | intra t=%.2f | n=%d' % (pcs, r1[0].tvalues[1], r2[0].tvalues[1], len(r1[1])))
