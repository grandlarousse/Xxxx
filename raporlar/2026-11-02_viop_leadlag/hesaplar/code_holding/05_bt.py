"""Backtestler (look-ahead yok; IS 2014-2020 / OOS 2021-2026; maliyet 8 ve 15 bps gidiş-dönüş).
BT1 KCHOL/SAHOL açılış NAV ayrışması: s_t = NAVgap_t - holding_gap_t (açılış seansı sonrası bilinir) -> holding intra_t
BT2 KCHOL/SAHOL 5g NAV-holding ayrışması (iskonto dönüşü): s = sum_{t-4..t}(NAVcc - Hcc) -> holding intra_{t+1} (muhafazakâr) ve cc_{t+1}
BT3 ENKAI: -TUR_{t-1} (ABD seansı Türkiye ETF, açılıştan önce bilinir) -> ENKAI intra_t ; ve piyasa-nötr (ENKAI intra - XU100 intra)
BT4 SAHOL: AKBNK_cc_{t-1} -> SAHOL intra_t
BT5 (negatif kontrol) EKGYO: ^TNX_{t-1} -> intra_t ; ALARK: MTF=F_{t-1} -> intra_t ; ENKAI: TRY=X_{t-1} -> intra_t
Çıktı: res_bt.csv"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hc, ll, numpy as np, pandas as pd

NAV = pd.read_parquet(os.path.join(hc.CODE, 'nav_series.parquet'))
M = ll.decomp('XU100')
tests = []
for h in ['KCHOL', 'SAHOL']:
    H = ll.decomp(h); n = NAV[f'{h}_fixed']
    tests.append((f'BT1 {h} open NAV-div -> intra_t', n['gap'] - H['gap'], H['intra'], 'z', 0.5))
    tests.append((f'BT1b {h} open NAV-div -> intra_t (sign)', n['gap'] - H['gap'], H['intra'], 'sign', 0.0))
    d5 = (n['cc'] - H['cc']).rolling(5).sum().shift(1)
    tests.append((f'BT2 {h} div5_(t-1) -> intra_t', d5, H['intra'], 'z', 1.0))
    tests.append((f'BT2b {h} div5_(t-1) -> cc_t (kapanışta giriş)', d5, H['cc'], 'z', 1.0))
E = ll.decomp('ENKAI')
tur = hc.dret('TUR')
tests.append(('BT3 ENKAI -TUR_(t-1) -> intra_t', -tur.shift(1), E['intra'], 'z', 1.0))
tests.append(('BT3b ENKAI -TUR_(t-1) -> intra_t - XU100 intra_t (nötr)', -tur.shift(1), E['intra'] - M['intra'], 'z', 1.0))
S = ll.decomp('SAHOL'); A = ll.decomp('AKBNK')
tests.append(('BT4 SAHOL AKBNK_(t-1) -> intra_t', A['cc'].shift(1) - S['cc'].shift(1), S['intra'], 'z', 1.0))
tests.append(('BT5 EKGYO ^TNX_(t-1) -> intra_t', -hc.dret('^TNX').shift(1), ll.decomp('EKGYO')['intra'], 'z', 1.0))
tests.append(('BT5 ALARK MTF=F_(t-1) -> intra_t', hc.dret('MTF=F').shift(1), ll.decomp('ALARK')['intra'], 'z', 1.0))
tests.append(('BT5 ENKAI TRY=X_(t-1) -> intra_t', hc.dret('TRY=X').shift(1), E['intra'], 'z', 1.0))
rows = []
for name, sig, tgt, mode, thr in tests:
    sig = sig[sig.index >= hc.IS0]
    for cost in [8.0, 15.0]:
        res, pnl = ll.backtest(sig, tgt, cost_bps=cost, mode=mode, thr=thr)
        o = {'test': name, 'cost_bps': cost, 'mode': mode, 'thr': thr}
        o.update({k: v for k, v in hc.bt_summary(res).items() if k != 'by_year'})
        o['by_year_bps'] = json.dumps(res.get('by_year_bps', {}))
        rows.append(o)
R = pd.DataFrame(rows); R.to_csv(os.path.join(hc.CODE, 'res_bt.csv'), index=False)
pd.set_option('display.width', 250)
print(R[['test', 'cost_bps', 'IS_n', 'IS_mean_bps', 'IS_t', 'IS_sharpe', 'OOS_n', 'OOS_mean_bps', 'OOS_t', 'OOS_sharpe', 'OOS_hit', 'OOS_maxdd_pct']].round(2).to_string())
for r in rows:
    if r['cost_bps'] == 8.0 and r['test'].startswith(('BT1 KCHOL', 'BT3 ENKAI', 'BT2 KCHOL')): print(r['test'], r['by_year_bps'])
