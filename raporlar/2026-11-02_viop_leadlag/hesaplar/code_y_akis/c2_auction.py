"""Kapanış seansı (18:00-18:10 TSİ) getirisi: auc = log(günlük kapanış / 15:00 UTC sürekli işlem sonu fiyatı) (h1, 2023-11+).
Soru: vade sonu (ay sonu) / MSCI / çeyrek sonu günlerinde auc büyür mü, yönlü mü, ertesi gün geri döner mi?
İşlenebilirlik: auc 18:10'da bilinir; VİOP normal seansı 18:15'e kadar açık (pay vadelisi) -> kapanışa yakın fiyattan pozisyon, ertesi gün açılış/kapanışta çık.
"""
import numpy as np, pandas as pd, alib
from alib import ll
D = pd.read_parquet('_cal_flags.parquet')
P = alib.panel()
syms = [s for s in alib.VIOP] + ['XU030']
rows = []
for s in syms:
    try:
        p15 = ll.snap_daily(s + '.IS', '15:00')
    except Exception as e:
        continue
    if s == 'XU030':
        d = ll.raw('XU030.IS').copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
        c = d['c']; o = d['o']; adj = d['adj']
    else:
        c = P['c'][s]; o = P['o'][s]; adj = P['adj'][s]
    c = c.dropna(); idx = c.index[(c.index >= '2023-11-01') & (c.index <= '2026-10-30')]
    auc = np.log(c.reindex(idx) / p15.reindex(idx))
    cc = np.log(adj).diff(); intra = np.log(c / o); gap = cc - intra
    df = pd.DataFrame({'auc': auc, 'gap1': gap.shift(-1).reindex(idx), 'intra1': intra.shift(-1).reindex(idx), 'cc1': cc.shift(-1).reindex(idx)})
    df = df[(df.auc.abs() < 0.05)]
    df['stock'] = s
    rows.append(df)
A = pd.concat(rows); A.index.name = 'date'; A = A.reset_index()
for f in ['me', 'msci', 'qend', 'pre_rel', 'ftse']:
    A[f] = D[f].reindex(A.date).fillna(False).astype(bool).values
A['cls'] = np.where(A.me, 'me', 'other')
out = []
for nm, sub in [('all_days', A), ('me', A[A.me]), ('msci', A[A.msci]), ('qend', A[A.qend]), ('non_me', A[~A.me]), ('ftse', A[A.ftse])]:
    for grp, ss in [('47', sub[sub.stock != 'XU030']), ('XU030', sub[sub.stock == 'XU030'])]:
        if len(ss) < 10: continue
        r = dict(set=nm, grp=grp, n=len(ss), n_days=ss.date.nunique(), abs_auc_bps=round(1e4 * ss.auc.abs().mean(), 1), mean_auc_bps=round(1e4 * ss.auc.mean(), 1))
        for y in ['gap1', 'intra1', 'cc1']:
            z = ss[['auc', y]].dropna()
            # geri dönüş katsayısı: y = a + b*auc (tarih kümelenmiş yerine basit + gün ortalaması)
            b = np.polyfit(z.auc, z[y], 1)[0] if len(z) > 10 else np.nan
            r['b_' + y] = round(b, 3); r['corr_' + y] = round(z.corr().iloc[0, 1], 3)
        # işaret stratejisi: -sign(auc) ile kapanışta gir, ertesi gün açılışta çık (gap) / kapanışta çık (cc)
        for y in ['gap1', 'cc1']:
            z = ss[['auc', y, 'date']].dropna(); z = z[z.auc.abs() > 0.002]
            pnl = -np.sign(z.auc) * z[y]
            g = pnl.groupby(z.date).mean()
            r['rev_' + y + '_bps'] = round(1e4 * pnl.mean(), 1); r['rev_' + y + '_t'] = round(alib.tstat(g)[0], 2); r['n_trades_' + y] = len(z)
        out.append(r)
S = pd.DataFrame(out); pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print(S.to_string()); S.to_csv('res_auction.csv', index=False)
A.to_parquet('_auction_panel.parquet')
