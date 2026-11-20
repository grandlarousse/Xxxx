"""scan.py — A2 önceden yazılı ızgara taraması (yalnız IS paneli).
Kullanım: python3 -I scan.py <panel_is klasörü> <çıktı klasörü>
Çıktı: scan_raw.csv (bütün eşikli kural satırları, elib.evaluate), regresyon.csv (T1/T3/T4 doğrusal)."""
import os, sys, time, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a2lib
from a2lib import elib
import statsmodels.api as sm
warnings.filterwarnings('ignore')

PANEL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.IS_END, 'KÖR PROTOKOL: bu betik yalnız IS paneliyle çalışır'
C = a2lib.context(P)
sc = C['sc']
THR = [1.0, 1.5, 2.0, -1.0, -1.5, -2.0]
HS = [1, 2, 3]
rows = []
t0 = time.time()


def add(sig, blok, inp, thr, hedef, h, kosul='', side='long', arac='spot'):
    if sig is None or sig.shape[1] == 0:
        return
    ad = f"{blok}|{inp}|z{'>=' if thr > 0 else '<='}{thr:g}|{hedef}|{kosul or '-'}|h{h}|{side}|{arac}"
    ex = {'blok': blok, 'girdi': inp, 'esik_z': thr, 'hedef_tur': hedef, 'kosul': kosul, }
    r = elib.evaluate(sig, P, h=h, side=side, name=ad, family='A2', measure='own', instrument=arac, extra=ex)
    s2 = sig
    if arac == 'viop':
        s2 = sig.copy()
        for c in s2.columns:
            s2.loc[s2.index < pd.Timestamp(elib.VIOP_START[c]), c] = False
    r.update(a2lib.halves(s2, P, h, side))
    rows.append(r)


# ---- T2: eşikli; hedef (a) bütün dolabilir sektör, (b) gecikenler, (c) AKSEN/ENJSA/ODAS (AL spot; SAT viop)
for inp in a2lib.INPUTS:
    for thr in THR:
        for h in HS:
            add(a2lib.make_sig(C, inp, thr, 'all'), 'T2a', inp, thr, 'all', h)
            add(a2lib.make_sig(C, inp, thr, 'lag'), 'T2b', inp, thr, 'lag', h)
            for s in elib.VIOP:
                sg = a2lib.make_sig(C, inp, thr, s)
                add(sg, 'T2c', inp, thr, s, h)
                add(sg, 'T2c', inp, thr, s, h, side='short', arac='viop')
            # bayat fiyat kontrolü: en likit 10 (adv60) ve kalanlar ("sığ")
            add(a2lib.make_sig(C, inp, thr, 'liq10'), 'BAYAT', inp, thr, 'liq10', h)
            add(a2lib.make_sig(C, inp, thr, 'sig'), 'BAYAT', inp, thr, 'sig', h)
            add(a2lib.make_sig(C, inp, thr, 'lagliq10'), 'BAYAT', inp, thr, 'lagliq10', h)
print('T2+BAYAT', len(rows), round(time.time() - t0), 's', flush=True)

# ---- T3: büyük hisse tek tek → sektörün geri kalanı
for src in elib.BIG:
    for thr in THR:
        for h in HS:
            add(a2lib.make_sig_src(C, src, thr), 'T3', 'SRC_' + src, thr, 'all_ex_src', h)
print('T3', len(rows), round(time.time() - t0), 's', flush=True)

# ---- T4: koşullu (XU030 20g getiri işareti; XU030 20g oynaklık yüksek/düşük) — |z| >= 1,5; hedef (a) ve (b)
for inp in a2lib.INPUTS:
    for thr in [1.5, -1.5]:
        for h in HS:
            for k in ['tr_up', 'tr_dn', 'vol_hi', 'vol_lo']:
                add(a2lib.make_sig(C, inp, thr, 'all', k), 'T4', inp, thr, 'all', h, kosul=k)
                add(a2lib.make_sig(C, inp, thr, 'lag', k), 'T4', inp, thr, 'lag', h, kosul=k)
print('T4', len(rows), round(time.time() - t0), 's', flush=True)
df = elib.to_csv(rows, os.path.join(OUT, 'scan_raw.csv'))

# ---------------------------------------------------------------------------------------------
# T1 doğrusal: f_h(i) ~ girdi(t) + r_cc(i,t) (+ XU100(t)); hisse bazında NW, havuz (Driscoll–Kraay), sepet hedef
# ---------------------------------------------------------------------------------------------
reg = []
R = P['ret_cc'][sc]
xu100 = P['idx_ret']['XU100'].reindex(R.index)


def fit(y, X, lag):
    d = pd.concat([y.rename('y'), X], axis=1).dropna()
    if len(d) < 250:
        return None
    m = sm.OLS(d['y'], sm.add_constant(d.drop(columns='y'))).fit(cov_type='HAC', cov_kwds={'maxlags': lag})
    return m.params, m.tvalues, len(d)


def pooled(Y, G, fl, lag, mask=None, split=False):
    """Havuz: y[t,i] ~ g[t,i] + r[t,i] (+xu100[t]); SE: tarihe göre kümelenmiş HAC (Driscoll–Kraay, gecikme lag)."""
    parts = []
    tix = pd.Series(np.arange(len(Y)), index=Y.index)
    for c in sc:
        ok = fl[c] if mask is None else (fl[c] & mask[c])
        d = pd.DataFrame({'y': Y[c], 'g': G[c], 'r': R[c], 'm': xu100, 't': tix})[ok].dropna()
        parts.append(d)
    d = pd.concat(parts).sort_values('t')
    X = d[['g', 'r', 'm']]
    if G is C['raw']['XU100']:
        X = d[['g', 'r']]
    if split:
        X = X.assign(g_pos=d['g'].clip(lower=0), g_neg=d['g'].clip(upper=0)).drop(columns='g')
    X = sm.add_constant(X)
    try:
        m = sm.OLS(d['y'], X).fit(cov_type='hac-groupsum', cov_kwds={'time': d['t'].values, 'maxlags': lag})
    except Exception:
        m = sm.OLS(d['y'], X).fit(cov_type='cluster', cov_kwds={'groups': d['t'].values})
    return m.params, m.tvalues, len(d)


fl_all = {}
for h in HS:
    f, fl, _ = elib.fwd_exec(P, h, 'long', sc)
    fl_all[h] = (f, fl)
    for inp in a2lib.INPUTS:
        G = C['raw'][inp]
        # hisse bazında
        res = []
        for c in sc:
            X = pd.DataFrame({'g': G[c], 'r': R[c]})
            if inp != 'XU100':
                X['m'] = xu100
            out = fit(f[c].where(fl[c]), X, h)
            if out:
                res.append((c, out[0]['g'], out[1]['g'], out[2]))
        if res:
            tt = np.array([x[2] for x in res]); bb = np.array([x[1] for x in res])
            reg.append({'test': 'T1_hisse', 'girdi': inp, 'h': h, 'n_hisse': len(res), 'medyan_katsayi': np.median(bb),
                        'poz_t2': int((tt > 2).sum()), 'neg_t2': int((tt < -2).sum()), 'medyan_t': np.median(tt),
                        'ayrinti': ';'.join(f'{c}:{b:.3f}({t:.1f})' for c, b, t, n in res)})
        pr, tv, n = pooled(f, G, fl, h)
        reg.append({'test': 'T1_havuz', 'girdi': inp, 'h': h, 'katsayi': pr['g'], 't': tv['g'], 'n': n,
                    'kats_r_i': pr['r'], 't_r_i': tv['r']})
        pr, tv, n = pooled(f, G, fl, h, split=True)
        reg.append({'test': 'T4_havuz_asimetri', 'girdi': inp, 'h': h, 'katsayi_poz': pr['g_pos'], 't_poz': tv['g_pos'],
                    'katsayi_neg': pr['g_neg'], 't_neg': tv['g_neg'], 'n': n})
        # hedef = dolabilir üyelerin EW sepeti (>= MIN_UNIV)
        Xb = f.where(fl); nb = Xb.notna().sum(axis=1)
        yb = Xb.mean(axis=1).where(nb >= a2lib.MIN_UNIV)
        gb = G.where(fl).mean(axis=1)
        rb = R.where(fl).mean(axis=1)
        X = pd.DataFrame({'g': gb, 'r': rb})
        if inp == 'EWx':
            X = X.drop(columns='r')                                   # sepetin kendi getirisi = girdi
        if inp != 'XU100':
            X['m'] = xu100
        out = fit(yb, X, h)
        reg.append({'test': 'T1_sepet', 'girdi': inp, 'h': h, 'katsayi': out[0]['g'], 't': out[1]['g'], 'n': out[2]})
        # koşullu havuz (T4): XU030 trend / oynaklık rejimleri
        for k, ks in C['kosul'].items():
            mk = a2lib._bc(ks.reindex(R.index).fillna(False), sc)
            pr, tv, n = pooled(f, G, fl, h, mask=mk)
            reg.append({'test': 'T4_havuz_' + k, 'girdi': inp, 'h': h, 'katsayi': pr['g'], 't': tv['g'], 'n': n})
        # dönem ayrımı
        for lab, a, b in [('<=2019', None, '2019-12-31'), ('2020-22', '2020-01-01', None)]:
            mk = pd.DataFrame(True, index=R.index, columns=sc)
            if a: mk[mk.index < pd.Timestamp(a)] = False
            if b: mk[mk.index > pd.Timestamp(b)] = False
            pr, tv, n = pooled(f, G, fl, h, mask=mk)
            reg.append({'test': 'T1_havuz_' + lab, 'girdi': inp, 'h': h, 'katsayi': pr['g'], 't': tv['g'], 'n': n})
        if h == 1:
            # bayat fiyat: f1'i gece / gün içi ayır; yalnız en likit 10; likidite sırası > 10
            g1 = P['ret_co'][sc].shift(-1); d1 = P['ret_oc'][sc].shift(-1)
            for lab, Y in [('gece', g1), ('gunici', d1)]:
                pr, tv, n = pooled(Y, G, fl, 1)
                reg.append({'test': 'BAYAT_havuz_f1_' + lab, 'girdi': inp, 'h': 1, 'katsayi': pr['g'], 't': tv['g'], 'n': n})
            for lab, mk in [('liq10', C['liq_rank'] <= 10), ('sig', C['liq_rank'] > 10)]:
                pr, tv, n = pooled(f, G, fl, 1, mask=mk)
                reg.append({'test': 'BAYAT_havuz_' + lab, 'girdi': inp, 'h': 1, 'katsayi': pr['g'], 't': tv['g'], 'n': n})
                for lab2, Y in [('gece', g1), ('gunici', d1)]:
                    pr, tv, n = pooled(Y, G, fl, 1, mask=mk)
                    reg.append({'test': f'BAYAT_havuz_{lab}_f1_{lab2}', 'girdi': inp, 'h': 1, 'katsayi': pr['g'], 't': tv['g'], 'n': n})
    # T3 doğrusal: büyük hisse j r_cc(t) → EW sektör (j hariç) f_h
    for src in [c for c in elib.BIG if c in sc]:
        others = [c for c in sc if c != src]
        Xb = f[others].where(fl[others]); nb = Xb.notna().sum(axis=1)
        yb = Xb.mean(axis=1).where(nb >= a2lib.MIN_UNIV - 1)
        X = pd.DataFrame({'g': R[src].where(P['tradable'][src]), 'r': R[others].where(fl[others]).mean(axis=1), 'm': xu100})
        out = fit(yb, X, h)
        if out:
            reg.append({'test': 'T3_ters', 'girdi': 'SRC_' + src, 'h': h, 'katsayi': out[0]['g'], 't': out[1]['g'], 'n': out[2]})
    # endeks düzeyi (yalnız bilgi)
    ix = P['idx_ret'].reindex(R.index)
    for a, b in [('XELKT', 'XU030'), ('XU030', 'XELKT')]:
        y = elib.fwd_simple(ix[[b]], h)[b]
        out = fit(y, pd.DataFrame({'g': ix[a], 'r': ix[b]}), h)
        reg.append({'test': f'ENDEKS_{a}->{b}', 'girdi': a, 'h': h, 'katsayi': out[0]['g'], 't': out[1]['g'], 'n': out[2]})
    print('reg h', h, round(time.time() - t0), 's', flush=True)
pd.DataFrame(reg).to_csv(os.path.join(OUT, 'regresyon.csv'), index=False)
print('satır:', len(df), 'regresyon:', len(reg))
