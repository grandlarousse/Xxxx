"""Holding <-> iştirak lead-lag ve NAV sepeti analizi.
(a) günlük: iştirak_t -> holding_{t+1} (holding_t ve XU100_t kontrollü) ve ters yön
(b) NAV sepeti (sabit ağırlık ~ şirket NAV dağılımı) ve kayan regresyon sepeti (look-ahead yok)
(c) açılış gap ayrışması: (NAVgap_t - holding_gap_t) -> holding intra_t
(d) kapanış ayrışması: (NAVcc_t - holding_cc_t) -> holding gap_{t+1}, intra_{t+1}
(e) dış sürücü: sürücü_{t-1} -> iştirak gap vs holding gap (yansıma oranı) ve holding intra yakalama
Çıktı: res_subs_daily.csv, res_subs_nav.csv, res_subs_ext.csv, nav_series.parquet"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hc, ll, numpy as np, pandas as pd

SUBS = {'KCHOL': {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03},
        'SAHOL': {'AKBNK': .45, 'ENJSA': .10, 'CIMSA': .03, 'BRISA': .03, 'KORDS': .03, 'AKGRT': .03},
        'DOHOL': {'KAREL': .10, 'GWIND': .10},
        'ALARK': {'ALCAR': .10}}

def dec(s):
    try: return ll.decomp(s)
    except Exception: return None

M = ll.decomp('XU100')
rows = []
for h, subs in SUBS.items():
    H = ll.decomp(h)
    for s in subs:
        S = dec(s)
        if S is None: continue
        for direction in ['sub->hold', 'hold->sub']:
            A, B = (H, S) if direction == 'sub->hold' else (S, H)  # A hedef, B sinyal
            y = A['cc']; x = B['cc'].shift(1)
            o = {'holding': h, 'sub': s, 'dir': direction}
            o['c'], o['t'], o['n'] = hc.corr_t(y, x)
            o['pc'], o['pc_t'], _ = hc.pcorr_t(y, x, [A['cc'].shift(1), M['cc'].shift(1)])
            o['pc_IS'], o['pc_IS_t'], _ = hc.pcorr_t(y, x, [A['cc'].shift(1), M['cc'].shift(1)], hc.IS0, hc.SPLIT)
            o['pc_OOS'], o['pc_OOS_t'], _ = hc.pcorr_t(y, x, [A['cc'].shift(1), M['cc'].shift(1)], hc.SPLIT)
            # hedefin gün-içi kısmı (işlenebilir): B_cc_{t-1} -> A_intra_t (A_cc_{t-1}, XU100 intra_t değil, XU100_cc_{t-1} kontrollü)
            o['intra_pc'], o['intra_pc_t'], _ = hc.pcorr_t(A['intra'], x, [A['cc'].shift(1), M['cc'].shift(1)])
            o['gap_pc'], o['gap_pc_t'], _ = hc.pcorr_t(A['gap'], x, [A['cc'].shift(1), M['cc'].shift(1)])
            rows.append(o)
pd.DataFrame(rows).to_csv(os.path.join(hc.CODE, 'res_subs_daily.csv'), index=False)

# ---------- NAV sepeti ----------
def basket(h, kind='fixed', col='cc', win=250):
    subs = SUBS[h]
    D = {s: dec(s) for s in subs}
    X = pd.DataFrame({s: D[s][col] for s in subs if D[s] is not None})
    if kind == 'fixed':
        w = pd.Series(subs)[X.columns]
        Wm = X.notna().mul(w, axis=1)  # eksik iştirak (ör. ENJSA 2018 öncesi) ağırlığı 0
        return (X.fillna(0) * w).sum(axis=1).where(X.notna().any(axis=1)) / Wm.sum(axis=1) * w.sum()
    # kayan regresyon sepeti: geçmiş 250g cc üzerinden holding ~ iştirakler (ağırlıklar t-1'e kadar bilgiyle)
    Hc = ll.decomp(h)['cc']; Xc = pd.DataFrame({s: D[s]['cc'] for s in subs if D[s] is not None})
    out = pd.Series(np.nan, index=X.index)
    df = pd.concat([Hc.rename('y'), Xc], axis=1)
    idx = df.index; Wt = {}
    for i in range(win, len(idx), 21):  # aylık yeniden tahmin
        g = df.iloc[i - win:i].dropna(axis=1, thresh=int(win * .8))
        if 'y' not in g: continue
        g = g.dropna()
        if len(g) < 150 or g.shape[1] < 2: continue
        cols = [c for c in g.columns if c != 'y']
        b = np.linalg.lstsq(np.column_stack([np.ones(len(g)), g[cols].values]), g['y'].values, rcond=None)[0][1:]
        Wt[idx[i]] = pd.Series(b, index=cols)
    W = pd.DataFrame(Wt).T.reindex(idx).ffill()
    W = W.reindex(columns=X.columns).fillna(0)
    return (X.fillna(0) * W).sum(axis=1).where(W.abs().sum(axis=1) > 0)

M_cc = M['cc']
navrows = []; NAVS = {}
for h in ['KCHOL', 'SAHOL']:
    H = ll.decomp(h)
    for kind in ['fixed', 'roll']:
        nav = {c: basket(h, kind, c) for c in ['cc', 'gap', 'intra']}
        NAVS[(h, kind)] = pd.DataFrame(nav)
        # (c) açılış ayrışması -> holding intra_t
        sig_open = nav['gap'] - H['gap']
        # (d) kapanış ayrışması -> ertesi gün
        sig_close = nav['cc'] - H['cc']
        # 5 günlük birikmiş ayrışma (iskonto değişimi) -> ertesi gün
        sig5 = sig_close.rolling(5).sum()
        for nm, sig, tgt in [('open_div->intra_t', sig_open, H['intra']),
                             ('close_div->gap_t+1', sig_close.shift(1), H['gap']),
                             ('close_div->intra_t+1', sig_close.shift(1), H['intra']),
                             ('close_div->cc_t+1', sig_close.shift(1), H['cc']),
                             ('div5->cc_t+1', sig5.shift(1), H['cc']),
                             ('div5->intra_t+1', sig5.shift(1), H['intra'])]:
            o = {'holding': h, 'basket': kind, 'test': nm}
            o['c'], o['t'], o['n'] = hc.corr_t(tgt, sig)
            o['c_IS'], o['t_IS'], _ = hc.corr_t(tgt, sig, hc.IS0, hc.SPLIT)
            o['c_OOS'], o['t_OOS'], _ = hc.corr_t(tgt, sig, hc.SPLIT)
            # XU100 aynı bileşen kontrollü
            mc = {'intra': M['intra'], 'gap': M['gap'], 'cc': M['cc']}[nm.split('->')[1].split('_')[0]]
            o['pc_mkt'], o['pc_mkt_t'], _ = hc.pcorr_t(tgt, sig, [mc])
            # yıllık işaret tutarlılığı
            ys, o['yr_same'] = hc.yr_sign(tgt, sig, 0, None, np.sign(o['c']))
            o['by_year'] = ys.round(3).to_dict()
            navrows.append(o)
        # NAV sepetinin holdinge senkron korelasyonu / beta
        o = {'holding': h, 'basket': kind, 'test': 'sync_nav_vs_hold'}
        o['c'], o['t'], o['n'] = hc.corr_t(H['cc'], nav['cc']); o['beta'] = hc.beta(H['cc'], nav['cc'])
        navrows.append(o)
NR = pd.DataFrame(navrows); NR.to_csv(os.path.join(hc.CODE, 'res_subs_nav.csv'), index=False)
pd.concat({f'{h}_{k}': v for (h, k), v in NAVS.items()}, axis=1).to_parquet(os.path.join(hc.CODE, 'nav_series.parquet'))

# ---------- (e) dış sürücü: iştirak mi holding mi önce/güçlü? ----------
EXT = {'KCHOL': [('BZ=F', ['TUPRS', 'AYGAZ']), ('CRACK', ['TUPRS']), ('F', ['FROTO']), ('STLAM.MI', ['TOASO']), ('EURUSD=X', ['FROTO', 'TOASO', 'ARCLK']),
                 ('ES=F', list(SUBS['KCHOL'])), ('TUR', list(SUBS['KCHOL'])), ('EUFN', ['YKBNK']), ('WHR', ['ARCLK']), ('^STOXX50E', list(SUBS['KCHOL']))],
       'SAHOL': [('EUFN', ['AKBNK']), ('EEM', ['AKBNK']), ('TUR', list(SUBS['SAHOL'])), ('ES=F', list(SUBS['SAHOL'])), ('TTF=F', ['ENJSA']), ('SBK.JO', ['AKBNK'])]}
erows = []
for h, lst in EXT.items():
    H = ll.decomp(h); w = pd.Series(SUBS[h])
    for drv, subs in lst:
        b = hc.dret(drv)
        o = {'holding': h, 'driver': drv, 'subs': '+'.join(subs)}
        # holding gap & intra tepkisi (b_{t-1})
        o['hold_gap_beta'] = ll.nw_t(H['gap'], b.shift(1))[0]; o['hold_gap_t'] = ll.nw_t(H['gap'], b.shift(1))[1]
        o['hold_intra_beta'] = ll.nw_t(H['intra'], b.shift(1))[0]; o['hold_intra_t'] = ll.nw_t(H['intra'], b.shift(1))[1]
        o['hold_sync_beta'] = ll.nw_t(H['cc'], b)[0]
        # NAV-ima: iştiraklerin ağırlıklı gap betası
        sg = 0; si = 0; ss = 0; tl = []
        for s in SUBS[h]:
            S = dec(s)
            if S is None: continue
            bg, tg, _ = ll.nw_t(S['gap'], b.shift(1)); bi, ti, _ = ll.nw_t(S['intra'], b.shift(1)); bs, _, _ = ll.nw_t(S['cc'], b)
            sg += w[s] * bg; si += w[s] * bi; ss += w[s] * bs
            if s in subs: tl.append(f'{s}:gap_t={tg:.1f},intra_t={ti:.1f}')
        o['nav_gap_beta'] = sg; o['nav_intra_beta'] = si; o['nav_sync_beta'] = ss
        o['gap_reflect_ratio'] = o['hold_gap_beta'] / sg if sg else np.nan
        o['sync_reflect_ratio'] = o['hold_sync_beta'] / ss if ss else np.nan
        o['sub_detail'] = '; '.join(tl)
        erows.append(o)
pd.DataFrame(erows).to_csv(os.path.join(hc.CODE, 'res_subs_ext.csv'), index=False)
print('OK')
