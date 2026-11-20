"""V4 — T1/T2 (seçim) ve K1/K2 (kaçınma) çürütme. Kullanım: python3 -I tk.py <panel_full>"""
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import elib, pm, tt, hac, add, save, load_rules  # noqa: E402

D = sys.argv[1]
P = elib.load(D)
sc = sorted(elib.sector_cols(P))
idx = P['ret_cc'].index
R = P['ret_cc'][sc]
U = P['fill_long'][sc]
tr = P['tradable'][sc]
ld, lu, td, tu = P['lim_dn'][sc], P['lim_up'][sc], P['lim_dn_touch'][sc], P['lim_up_touch'][sc]
f_ex, _, _ = elib.fwd_exec(P, 1, 'long', sc)
f_pl = R.shift(-1)                                   # düz ertesi gün kapanış getirisi (çıkış ertelemesi yok)
g_n = P['ret_co'][sc].shift(-1)                      # gece: t kapanışı → t+1 açılışı
g_d = P['ret_oc'][sc].shift(-1)                      # gün içi: t+1 açılışı → t+1 kapanışı
CR = [c for c in ['BIGEN', 'LYDYE', 'MAGEN', 'ESEN'] if c in sc]
PERS = ['IS', 'OOS1', 'KASA', 'HAVUZ']
seri5 = ld.astype(float).rolling(5, min_periods=1).max().astype(bool)      # son 5 günde (t dâhil) tabanda kapanış var


def nocr(M):
    M = M.copy()
    M[CR] = False
    return M


def sec_ex(F, Ub):
    """Hisse getirisi − kıyas evrenindeki DİĞER hisselerin eşit ağırlıklı ortalaması (en az 4 diğer hisse)."""
    X = F.where(Ub)
    S = X.sum(axis=1, min_count=1)
    N = X.notna().sum(axis=1)
    num = (-X.fillna(0)).add(S, axis=0)
    dn = (-X.notna().astype(int)).add(N, axis=0)
    return F - num / dn.where(dn >= 4)


def ev(bulgu, test, E, sig, pers=PERS, notu=''):
    for per in pers:
        m = pm(idx, per)
        X = E[m].where(sig[m])
        p = X.mean(axis=1)
        mu, t, n = tt(p)
        v = X.values[np.isfinite(X.values)]
        add(bulgu, test, per, n, mu, t, (f'islem={len(v)}; islem ort={1e4 * v.mean():.1f}; isabet={(v > 0).mean():.2f}; medyan={1e4 * np.median(v):.0f}; gunde={len(v) / max(n, 1):.1f} ' if len(v) else '') + notu)


def day_diff(bulgu, test, F, sig, Ub, kind='mean', pers=PERS):
    """Gün düzeyi: seçilenlerin ortalaması − evrenin (seçilenler dâhil) ortalaması / medyanı."""
    a = F.where(sig).mean(axis=1)
    b = F.where(Ub).mean(axis=1) if kind == 'mean' else F.where(Ub).median(axis=1)
    d = (a - b)
    for per in pers:
        m = pm(idx, per)
        mu, t, n = tt(d[m])
        add(bulgu, test, per, n, mu, t, f'gun isabeti={(d[m].dropna() > 0).mean():.2f}')


w3b, a8, a3, w3a = load_rules('w3b_damitma'), load_rules('a8_model'), load_rules('a3_kesit'), load_rules('w3a_kacinma')
RL = {}
for mod in (w3b, a8, a3, w3a):
    for rl in mod.build(P):
        RL[rl['ad']] = rl['sig'].reindex(index=idx, columns=sc).fillna(False).astype(bool)
T1 = RL['A8_kesit_lgbm_d3_m500_h1_ust20'] & U
T2 = RL['W3B_sade_sakin_guclu_h1'] & U
K1 = RL['A3_rel1_alt5_h1_RED'] & U
K2 = RL['W3A_sektorden_5puan_geride_KACIN_h1'] & U

E_ex = sec_ex(f_ex, U)
E_pl = sec_ex(f_pl, U)
E_pl_nocr = sec_ex(f_pl, nocr(U))
U_cl = U & ~ld & ~td                       # bugün tabana değmemiş
U_s5 = U & ~seri5 & ~td                    # son 5 günde taban kapanışı yok, bugün tabana değmemiş
E_cl = sec_ex(f_pl, U_cl)
E_s5 = sec_ex(f_pl, U_s5)
Fw = f_pl.clip(-0.05, 0.05)
E_w = sec_ex(Fw, U)
lu1 = lu.shift(-1, fill_value=False)
ld1 = ld.shift(-1, fill_value=False)

print('== 7. T1/T2: secim suzgeci olarak deger')
for nm, S in [('T1', T1), ('T2', T2)]:
    ev(nm, 'yineleme: sec, elib dolum (cikis ertelemeli)', E_ex, S)
    ev(nm, 'duz f1, kiyas=diger dolabilirler', E_pl, S)
    ev(nm, 'duz f1, cokus hisseleri (BIGEN LYDYE MAGEN ESEN) kiyas ve secimden cikarildi', E_pl_nocr, nocr(S))
    ev(nm, 'duz f1, kiyas=bugun tabana degmemisler', E_cl, S & U_cl)
    ev(nm, 'duz f1, kiyas=son 5 gunde taban kapanisi olmayanlar', E_s5, S & U_s5)
    day_diff(nm, 'rastgele dolabilir hisseye gore (secilen ort − evren ort), duz f1', f_pl, S, U)
    day_diff(nm, 'rastgele hisseye gore, cokus hisseleri haric', f_pl, nocr(S), nocr(U))
    day_diff(nm, 'rastgele hisseye gore, kiyas=son 5 gunde tabansiz', f_pl, S & U_s5, U_s5)
    day_diff(nm, 'MEDYAN hisseye gore (secilen ort − evren medyani), duz f1', f_pl, S, U, 'median')
    dm = f_pl.where(S).median(axis=1) - f_pl.where(U).median(axis=1)
    umed = f_pl.where(U).median(axis=1)
    for per in PERS:
        m = pm(idx, per)
        mu, t, n = tt(dm[m])
        above = f_pl[m].gt(umed[m], axis=0).where(S[m] & f_pl[m].notna())
        add(nm, 'secilenlerin MEDYANI − evren medyani, duz f1', per, n, mu, t,
            f'gun isabeti={(dm[m].dropna() > 0).mean():.2f}; secilen islemlerin evren medyanini gecme orani={np.nanmean(above.values.astype(float)):.3f}')
    ev(nm, 'getiriler +-%5 kirpilmis (kuyruksuz), kiyas=diger dolabilirler', E_w, S)
    ev(nm, 'ertesi gun tavanda kapanan secilenler haric', E_pl, S & ~lu1)
    ev(nm, 'ertesi gun tavan (secilen) ve taban (kiyas) kapananlar haric', sec_ex(f_pl, U & ~ld1 & ~lu1), S & ~lu1 & ~ld1)
    for per in PERS:
        m = pm(idx, per)
        X = E_pl[m].where(S[m])
        v = np.sort(X.values[np.isfinite(X.values)])
        k = max(int(0.05 * len(v)), 1)
        st_ = S[m].values.sum()
        add(nm, 'kuyruk: en iyi %5 islem cikinca islem ort.', per, len(v), 1e4 * v[:-k].mean(), None,
            f'tum islem ort={1e4 * v.mean():.1f}; en kotu %5 de cikinca={1e4 * v[k:-k].mean():.1f}; secilenlerde ertesi gun tavan orani={(lu1[m] & S[m]).values.sum() / st_:.3f}, evrende={(lu1[m] & U[m]).values.sum() / U[m].values.sum():.3f}; '
            f'secilenlerde ertesi gun taban orani={(ld1[m] & S[m]).values.sum() / st_:.3f}, evrende={(ld1[m] & U[m]).values.sum() / U[m].values.sum():.3f}')
    ev(nm, 'gece (t kapanis -> t+1 acilis), kiyas=diger dolabilirler', sec_ex(g_n, U), S)
    ev(nm, 'gun ici (t+1 acilis -> kapanis)', sec_ex(g_d, U), S)

print('== 8. T2 sadelestirme')
Rr = R.round(4)
valid = tr & Rr.notna()
vol20 = Rr.rolling(20, min_periods=10).std().round(8).where(valid)
A = ~w3b.flags(P, sc)
B = w3b.bucket(vol20, U, 2, 6) == 0
C = w3b.bucket(Rr.where(valid), U, 3, 6) == 2
C2 = w3b.bucket(Rr.where(valid), U, 2, 6) == 1
px = P['px']
ph = px.pivot_table(index='date', columns='sym', values='h', aggfunc='last')
pl_ = px.pivot_table(index='date', columns='sym', values='l', aggfunc='last')
ph.index = pd.to_datetime(ph.index)
pl_.index = pd.to_datetime(pl_.index)
rng = (ph / pl_ - 1).reindex(index=idx, columns=sc)
volTV = rng.rolling(21, min_periods=10).mean().where(valid)          # TradingView "Oynaklık (ay)" vekili: günlük (yüksek−düşük)/düşük ortalaması
Btv = w3b.bucket(volTV, U, 2, 6) == 0
chk = ((U & A & B & C) == T2).values.mean()
print('T2 yeniden kurulum eslesmesi:', chk)
VAR = {'a&b&c (dondurulmus)': A & B & C, 'b&c (limit kosulu yok)': B & C, 'a&c (oynaklik yok)': A & C, 'yalniz c (ust ucte bir)': C, 'yalniz b (sakin yari)': B,
       'a&b (getiri kosulu yok)': A & B, 'a&bTV&c (oynaklik=gun ici aralik vekili)': A & Btv & C, 'bTV&c': Btv & C, 'a&b&ust yari': A & B & C2,
       'c ama b DEGIL (oynak ve guclu)': A & ~B & C, 'a&b&c ve getiri>0': A & B & C & (Rr > 0)}
for k, S in VAR.items():
    ev('T2', 'sade: ' + k + ' | duz f1, kiyas=diger dolabilirler', E_pl, S & U, ['IS', 'OOS1', 'KASA'])
    ev('T2', 'sade: ' + k + ' | cokus hisseleri haric', E_pl_nocr, nocr(S & U), ['KASA'])

print('== 9. Birlesim (SONRADAN turetildi; dogrulanmadi)')
f3, fl3, _ = elib.fwd_exec(P, 3, 'long', sc)
r = P['idx_ret']['XELKT'].reindex(idx)
LE = P['idx']['XELKT'].reindex(idx)
zE = r / r.rolling(60, min_periods=40).std().shift(1)
S1d = (LE >= LE.rolling(20, min_periods=20).max()).fillna(False)
S2d = (zE >= 1).fillna(False)
bas = f3.where(U)
for nm, sd in [('S1 zirve20', S1d), ('S2 xelkt z>=1', S2d), ('tum gunler', pd.Series(True, index=idx))]:
    for sel_nm, Ssel in [('T2', T2), ('T1', T1)]:
        a = f3.where(Ssel).mean(axis=1)
        b = bas.mean(axis=1)
        nb = bas.notna().sum(axis=1)
        d = (a - b).where(sd & (nb >= 5))
        for per in ['IS', 'OOS1', 'KASA']:
            m = pm(idx, per)
            mu, t, n = hac(d[m], 3)
            add('T+S', f'DOGRULANMADI: {nm} gunu {sel_nm} secilenleri 3g − sepet 3g', per, n, mu, t,
                f'secilen ham={1e4 * a.where(d.notna())[m].mean():.0f}; sepet ham={1e4 * b.where(d.notna())[m].mean():.0f}; gun isabeti={(d[m].dropna() > 0).mean():.2f}; secilen/gun={Ssel[m].where(d[m].notna(), False).values.sum() / max(n, 1):.1f}')

print('== 10. K1/K2')
rk = R.where(tr)
nn = rk.notna().sum(axis=1)
rel1 = rk.sub(rk.mean(axis=1).where(nn >= 8), axis=0)
relX = rk.sub(r, axis=0)
for nm, S in [('K1', K1), ('K2', K2)]:
    ev(nm, 'v0 yineleme: sec, elib dolum (cikis ertelemeli)', E_ex, S)
    ev(nm, 'v1 duz f1, kiyas=diger dolabilirler', E_pl, S)
    ev(nm, 'v2 tabanda kapananlar sinyalden cikarildi', E_pl, S & ~ld)
    ev(nm, 'v3 tabana degenler de cikarildi', E_pl, S & ~ld & ~td)
    ev(nm, 'v4 v3 + kiyas da temiz (tabana degmemis)', E_cl, S & U_cl)
    ev(nm, 'v5 son 5 gunde taban kapanisi olanlar da cikarildi (sinyal+kiyas)', E_s5, S & U_s5)
    ev(nm, 'v6 v5 + cokus hisseleri haric', sec_ex(f_pl, nocr(U_s5)), nocr(S & U_s5))
    ev(nm, 'v4 gece payi (t kapanis -> t+1 acilis)', sec_ex(g_n, U_cl), S & U_cl)
    ev(nm, 'v4 gun ici payi (t+1 acilis -> kapanis)', sec_ex(g_d, U_cl), S & U_cl)
    ev(nm, 'v4 getiriler +-%5 kirpilmis', sec_ex(Fw, U_cl), S & U_cl)
    ev(nm, 'v4 2. gun (t+1 kapanis -> t+2 kapanis)', sec_ex(R.shift(-2), U_cl), S & U_cl)
ev('K1', 'v4 hafif kaybedenler: en alt beste bir ama sektorden < 5 puan geride', E_cl, K1 & U_cl & (rel1 > -0.05))
ev('K1', 'v4 en alt beste bir ama sektorden < 3 puan geride', E_cl, K1 & U_cl & (rel1 > -0.03))
ev('K1', 'v4 en alt beste bir ve sektorden 3-5 puan geride', E_cl, K1 & U_cl & (rel1 <= -0.03) & (rel1 > -0.05))
PR = {'sektor EW ort.dan >=3 puan geride (taban dahil)': (rel1 <= -0.03) & U, 'sektor EW ort.dan >=5 puan geride (taban dahil)': (rel1 <= -0.05) & U,
      'XELKT endeksinden >=3 puan geride (taban dahil)': (relX <= -0.03) & U, 'XELKT endeksinden >=5 puan geride (taban dahil)': (relX <= -0.05) & U,
      'XELKT endeksinden >=3 puan geride, tabana degmemis': (relX <= -0.03) & U_cl, 'XELKT endeksinden >=5 puan geride, tabana degmemis': (relX <= -0.05) & U_cl,
      'gunluk getirisi <= -%5 (mutlak; taban dahil)': (R <= -0.05) & U, 'gunun en kotu 5 hissesi (taban dahil)': (rk.where(U).rank(axis=1, method='first') <= 5) & U & (nn.values[:, None] >= 15),
      'tabana degdi ya da tabanda kapandi': (td | ld) & U,
      'BIRLESIK: XELKT endeksinden >=3 puan geride YA DA tabana degdi': (((relX <= -0.03) | td | ld) & U)}
for k, S in PR.items():
    for per in ['IS', 'OOS1', 'KASA', 'HAVUZ']:
        m = pm(idx, per)
        X = E_pl[m].where(S[m])
        mu, t, n = tt(X.mean(axis=1))
        cov = S[m].values.sum() / max(U[m].values.sum(), 1)
        allm = f_pl[m].where(U[m]).mean(axis=1)
        keep = f_pl[m].where(U[m] & ~S[m]).mean(axis=1)
        imp, timp, _ = tt(keep - allm)
        Xc = E_cl[m].where(S[m] & U_cl[m])
        muc, tc, ncl = tt(Xc.mean(axis=1))
        add('K-pratik', k, per, n, mu, t, f'kapsam={cov:.3f} (hisse-gun payi); elenince rastgele alicinin ertesi gun ort. iyilesmesi={imp:.1f} bps (t {timp:.1f}); taban-disi alt kume (temiz kiyas)={muc:.0f} (t {tc:.1f}, n {ncl})')
save('tk.csv')
