"""A3 kesit taraması (yalnız IS paneli). Kullanım: python3 -I scan.py <panel_is> <cikti_klasoru>
Çıktı: <cikti>/scan_rows.csv (elib.evaluate satırları), <cikti>/regresyon.csv (Fama–MacBeth ve zaman serisi regresyonları)."""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ortak'))
import elib  # noqa: E402
import rules as RL  # noqa: E402

panel, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
t0 = time.time()
P = elib.load(panel)
assert P['ret_cc'].index.max() <= elib.IS_END, 'IS dışı veri!'
F = RL.feats(P)
sc = F['sc']
H1_END = pd.Timestamp('2019-12-31')
G_CO = P['ret_co'][sc].shift(-1)
G_OC = P['ret_oc'][sc].shift(-1)
FILL = P['fill_long'][sc]


def extras(sig, h, measure):
    M, fl = elib.excess_measures(P, h, 'long', list(sig.columns))
    p, ntr, X = elib.day_series(sig, M[measure], fl, 1)
    a, b = p[p.index <= H1_END].dropna(), p[p.index > H1_END].dropna()
    ex = {'yari1_bps': 1e4 * a.mean() if len(a) else np.nan, 'yari1_n': len(a),
          'yari2_bps': 1e4 * b.mean() if len(b) else np.nan, 'yari2_n': len(b)}
    d = p.dropna().sort_values()
    ex['top10gun_haric_bps'] = 1e4 * d.iloc[:-10].mean() if len(d) > 20 else np.nan   # yalnız en iyi 10 gün hariç
    if h == 1:  # f_1'in gece / gün içi ayrımı, sektör (dolabilir EW) farkı olarak
        S = sig & fl
        for nm, G in (('gece', G_CO), ('gunici', G_OC)):
            Gx = G.sub(G.where(FILL).mean(axis=1), axis=0)
            ex[f'{nm}_sec_bps'] = 1e4 * Gx.where(S).mean(axis=1).dropna().mean()
    return ex


rows = []


def ev(sig, h, name, measure='sec', tarama=''):
    sig = sig.reindex(columns=sc).fillna(False).astype(bool)
    ex = extras(sig, h, measure)
    ex['tarama'] = tarama
    r = elib.evaluate(sig, P, h=h, side='long', name=name, family='A3', measure=measure, extra=ex)
    rows.append(r)
    return r


# ---------------------------------------------------------------- T1 Fama–MacBeth
reg = []


def fm(tag, xs, h, fillable=True):
    M, fl = elib.excess_measures(P, h, 'long', sc)
    y = M['raw'].where(fl) if fillable else M['raw'].where(P['tradable'][sc])
    summ, B = elib.fama_macbeth(y, xs, min_n=8, lag=h - 1)
    for k in summ.index:
        d = {'test': tag, 'h': h, 'degisken': k, 'katsayi': summ.loc[k, 'katsayi'], 't': summ.loc[k, 't'],
             'n': int(summ.loc[k, 'n_gun']), 'hedef': 'dolabilir' if fillable else 'hepsi'}
        for lab, m in (('yari1', B.index <= H1_END), ('yari2', B.index > H1_END)):
            x = B.loc[m, k].values
            mu, t = elib._hac_mean(x, np.ones(len(x)), h - 1)
            d[f'{lab}_katsayi'] = mu; d[f'{lab}_t'] = t; d[f'{lab}_n'] = len(x)
        reg.append(d)


LD = P['lim_dn'][sc].astype(float).where(F['T'])
LU = P['lim_up'][sc].astype(float).where(F['T'])
uni = {'rel1': F['rel1'], 'rel3': F['rel3'], 'rel5': F['rel5'], 'hacim_soku': F['vs'], 'taban': LD}
for h in (1, 2, 3):
    for k, X in uni.items():
        fm(f'T1_FM_tek_{k}', {k: X}, h)
    fm('T1_FM_birlikte', {'rel1': F['rel1'], 'rel5': F['rel5'], 'hacim_soku': F['vs'], 'taban': LD}, h)
    fm('T1_FM_tek_tavan_bilgi', {'tavan': LU}, h, fillable=False)   # tavanda kapanan dolmaz: yalnız bilgi
print('T1 bitti', round(time.time() - t0), 's', flush=True)

# ---------------------------------------------------------------- T2 sıralama sepetleri
for k in (1, 3, 5):
    for side, lab in (('bottom', 'alt5'), ('top', 'ust5')):
        for h in (1, 2, 3):
            ev(RL.sig_quint(F, k, side), h, f'T2_rel{k}_{lab}_h{h}', tarama='T2')
            for cond in ('up', 'dn'):
                ev(RL.sig_quint(F, k, side, cond), h, f'T2_rel{k}_{lab}_sek{cond}2_h{h}', tarama='T2_kosullu')
print('T2 bitti', round(time.time() - t0), 's', flush=True)

# ---------------------------------------------------------------- T3 / T4 çapraz otokorelasyon
def xreg(tag, src, dst, FF=F):
    for h in (1, 2, 3):
        M, fl = elib.excess_measures(P, h, 'long', sc)
        Y = M['raw'].where(FF[dst] & fl)
        y = Y.mean(axis=1).where(Y.notna().sum(axis=1) >= 2)
        X = pd.DataFrame({'R_' + src: FF['R_' + src], 'R_' + dst: FF['R_' + dst]})
        for lab, m in (('tum', X.index >= X.index[0]), ('yari1', X.index <= H1_END), ('yari2', X.index > H1_END)):
            res = elib.ts_reg(y[m], X[m], lag=h - 1)
            if res is None:
                continue
            for v in X.columns:
                reg.append({'test': tag, 'h': h, 'degisken': v, 'katsayi': res.loc[v, 'katsayi'], 't': res.loc[v, 't'],
                            'n': int(res.loc[v, 'n']), 'hedef': f'{dst} sepeti f_h (dolabilir)', 'donem': lab})


def xrules(tag, src, dst, FF=F, suffix='', post=None, tarama=None):
    for z in (1.0, 1.5, 2.0):
        for h in (1, 2, 3):
            s = RL.sig_xgroup(FF, src, dst, z, +1)
            if post is not None:
                s = s & post
            zl = str(z).replace('.', '')
            for ms in ('sec', 'own'):
                ev(s, h, f'{tag}_{src}_z{zl}_yukari_{dst}_h{h}{suffix}_{ms}', measure=ms, tarama=tarama or tag)
            if not suffix:
                s2 = RL.sig_xgroup(FF, src, dst, z, -1)
                ev(s2, h, f'{tag}_{src}_z{zl}_asagi_{dst}_h{h}_own', measure='own', tarama=tag + '_asagi')


xreg('T3_LM_buyuk>kucuk', 'big', 'small'); xreg('T3_LM_kucuk>buyuk', 'small', 'big')
xrules('T3', 'big', 'small')
xreg('T4_CS_yuksek>dusuk', 'vhi', 'vlo'); xreg('T4_CS_dusuk>yuksek', 'vlo', 'vhi')
xrules('T4', 'vhi', 'vlo')
print('T3/T4 bitti', round(time.time() - t0), 's', flush=True)

# ---------------------------------------------------------------- sahte etki kontrolleri
PX5 = (F['px'] >= 5.0)
F15 = RL.feats(P, univ=RL.top_liquid(P, 15))
for k in (1, 3, 5):
    for side, lab in (('bottom', 'alt5'), ('top', 'ust5')):
        for h in (1, 2, 3):
            ev(RL.sig_quint(F, k, side) & PX5, h, f'T2_rel{k}_{lab}_h{h}_px5', tarama='kontrol_c_px5')
            ev(RL.sig_quint(F15, k, side), h, f'T2_rel{k}_{lab}_h{h}_lik15', tarama='kontrol_d_lik15')
xrules('T3', 'big', 'small', suffix='_px5', post=PX5, tarama='kontrol_c_px5')
xrules('T3', 'big', 'small', FF=F15, suffix='_lik15', tarama='kontrol_d_lik15')
xrules('T4', 'vhi', 'vlo', suffix='_px5', post=PX5, tarama='kontrol_c_px5')
xrules('T4', 'vhi', 'vlo', FF=F15, suffix='_lik15', tarama='kontrol_d_lik15')

df = elib.to_csv(rows, os.path.join(out, 'scan_rows.csv'))
pd.DataFrame(reg).to_csv(os.path.join(out, 'regresyon.csv'), index=False)
print('satır:', len(df), 'regresyon satırı:', len(reg), 'süre', round(time.time() - t0), 's')
