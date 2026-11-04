"""Tüm testleri birleştir, BH-FDR (q=0,05) — tüm aile ve blok içi. Çıktı: res/tests_all.csv"""
import glob, pandas as pd, numpy as np
from klib import bh, bh_q, RES
D = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(RES + '/tests_*.csv')) if not f.endswith('tests_all.csv')], ignore_index=True)
# her betik kendi blok dosyasını tek çalıştırmada baştan yazar -> tekrar yok
from scipy import stats
D['p'] = 2 * (1 - stats.norm.cdf(D['t'].abs()))  # kayıtta p 2 haneye yuvarlanmıştı -> t'den yeniden
D['q_all'] = bh_q(D['p'].values); D['fdr_all'] = D['q_all'] <= 0.05
D['q_blk'] = np.nan
for b, g in D.groupby('block'): D.loc[g.index, 'q_blk'] = bh_q(g['p'].values)
D['fdr_blk'] = D['q_blk'] <= 0.05
D.to_csv(RES + '/tests_all.csv', index=False)
print('toplam test', len(D)); print(D.groupby('block').agg(n=('p', 'size'), fdr_all=('fdr_all', 'sum'), fdr_blk=('fdr_blk', 'sum'), tmax=('t', lambda x: x.abs().max())).to_string())
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
cols = ['block', 'name', 'inst', 'entry', 'h', 'n', 'gross', 'net8', 'net15', 't', 'IS_t', 'OOS_t', 'yrs_pos', 'q_all']
print(D[D.fdr_all].sort_values('t', key=lambda x: -x.abs())[cols].head(120).to_string())
