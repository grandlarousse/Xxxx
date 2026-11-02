"""5) Önceden bilinen takvim olayları -> fiyat yolu.
 a) Ay sonu = VİOP vade sonu (ayın son iş günü) ve ay dönümü (TOM: -1..+3)
 b) Bayram öncesi (arife/yarım gün) ve tatil öncesi günler
 c) MSCI (Şub/May/Ağu/Kas son iş günü) ve FTSE (Mar/Haz/Eyl/Ara 3. Cuma) yeniden dengeleme günleri, BIST çeyrek sonu (endeks dönem değişikliği yürürlük arifesi)
 d) Kapanış seansı (h1, 2023-11+): vade sonu günü kapanış seansı getirisi ve ertesi gün geri dönüşü (47 hisse + XU030)
 e) Temettü hak kullanım (ex) günü: adj/c oranı sıçramasından; bedelsiz (Yahoo split olayları)
Çıktılar: res_cal_*.csv, log_c.txt
"""
import numpy as np, pandas as pd, json, glob, os, alib
from alib import ll
END = pd.Timestamp('2026-10-30')
cal = ll.bist_cal(); cal = cal[(cal >= '2005-01-01') & (cal <= END)]
X = alib.xu('XU100'); X30 = alib.xu('XU030')
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
s = pd.Series(cal, index=cal)
me = s.groupby([cal.year, cal.month]).transform('max') == s           # ayın son iş günü
fd = s.groupby([cal.year, cal.month]).transform('min') == s           # ilk iş günü
rank_in_m = s.groupby([cal.year, cal.month]).cumcount() + 1
rank_from_end = s.groupby([cal.year, cal.month]).cumcount(ascending=False)
D = pd.DataFrame(index=cal)
D['me'] = me.values; D['tom'] = (rank_from_end.values == 0) | (rank_in_m.values <= 3)
D['d1'] = rank_in_m.values == 1; D['d2'] = rank_in_m.values == 2; D['d3'] = rank_in_m.values == 3
nxt_gap = pd.Series(cal[1:] - cal[:-1], index=cal[:-1]).dt.days.reindex(cal)  # bir sonraki işlem gününe kadar takvim günü
wd_closed = pd.Series([np.busday_count((a + pd.Timedelta(days=1)).date(), b.date()) for a, b in zip(cal[:-1], cal[1:])], index=cal[:-1]).reindex(cal)
D['pre_hol'] = wd_closed >= 1           # ardından en az 1 hafta içi kapalı gün
D['pre_rel'] = wd_closed >= 2           # dini bayram (çok günlük kapanış) arifesi ~ yarım gün
D['post_hol'] = D.pre_hol.shift(1).fillna(False).astype(bool)
D['msci'] = D.me & cal.month.isin([2, 5, 8, 11])
D['qend'] = D.me & cal.month.isin([3, 6, 9, 12])
fri3 = (cal.dayofweek == 4) & (cal.day >= 15) & (cal.day <= 21) & cal.month.isin([3, 6, 9, 12]); D['ftse'] = fri3
for c in ['cc', 'gap', 'intra']: D['x' + c] = X[c].reindex(cal).values; D['x30' + c] = X30[c].reindex(cal).values
D['xcc_next'] = D.xcc.shift(-1); D['xgap_next'] = D.xgap.shift(-1); D['xintra_next'] = D.xintra.shift(-1)
D.loc[D.index < '2014-01-01', ['xgap', 'xintra', 'xgap_next', 'xintra_next', 'x30gap', 'x30intra']] = np.nan
def cmp(flag, col, d=D):
    a = d.loc[d[flag], col].dropna(); b = d.loc[~d[flag], col].dropna()
    import scipy.stats as st
    t = st.ttest_ind(a, b, equal_var=False).statistic if len(a) > 5 else np.nan
    return dict(flag=flag, col=col, n=len(a), mean_bps=round(1e4 * a.mean(), 1), other_bps=round(1e4 * b.mean(), 1), t_diff=round(t, 2),
                hit=round((a > 0).mean(), 3), IS_bps=round(1e4 * a[a.index < '2021'].mean(), 1), OOS_bps=round(1e4 * a[a.index >= '2021'].mean(), 1),
                yrs_pos=f"{int((a.groupby(a.index.year).mean() > 0).sum())}/{a.index.year.nunique()}")
rows = []
for flag in ['me', 'tom', 'd1', 'd2', 'd3', 'pre_hol', 'pre_rel', 'post_hol', 'msci', 'qend', 'ftse']:
    for col in ['xcc', 'xgap', 'xintra', 'xcc_next', 'xgap_next', 'xintra_next']:
        rows.append(cmp(flag, col))
C = pd.DataFrame(rows); C.to_csv('res_cal_index.csv', index=False)
print(C.to_string())
# 47 hisse kesitinde ay sonu / TOM (hisse - XU100)
P = alib.panel(); adj = P['adj'][alib.VIOP].loc[:END]; r = np.log(adj).diff(); r = r.where(~((r > alib.ll.LIM_UP) | (r < alib.ll.LIM_DN)))
ex = r.sub(X['cc'].reindex(r.index), axis=0)
o = P['o'][alib.VIOP].loc[:END]; c_ = P['c'][alib.VIOP].loc[:END]; intra = np.log(c_ / o); gap = r - intra
rows = []
for flag in ['me', 'tom', 'pre_rel', 'msci', 'qend']:
    for nm, M in [('cc', r), ('excess_cc', ex), ('intra', intra.loc['2014':]), ('gap_next', gap.shift(-1).loc['2014':]), ('excess_next', ex.shift(-1))]:
        mm = M.mean(axis=1)
        f = D[flag].reindex(mm.index).fillna(False).astype(bool).values
        a = mm[f]; b = mm[~f]
        rows.append(dict(flag=flag, var=nm, n=a.notna().sum(), mean_bps=round(1e4 * a.mean(), 1), other_bps=round(1e4 * b.mean(), 1), t=round(alib.tstat(a)[0], 2)))
print(pd.DataFrame(rows).to_string()); pd.DataFrame(rows).to_csv('res_cal_viop47.csv', index=False)
D.to_parquet('_cal_flags.parquet')
