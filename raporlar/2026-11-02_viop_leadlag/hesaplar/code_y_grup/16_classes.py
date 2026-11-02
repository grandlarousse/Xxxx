"""Pay grubu fiyat oranları: KRDMA/KRDMD, KRDMB/KRDMD, KRDMB/KRDMA, ISBTR/ISCTR, ISATR/ISCTR. Seviye, aralık, ADF, AR(1) yarı ömür, yıllık ortalama; ve lead-lag (D -> A/B ertesi gün)."""
from gx import *
from statsmodels.tsa.stattools import adfuller
rows = []
for a, b in [('KRDMA', 'KRDMD'), ('KRDMB', 'KRDMD'), ('KRDMB', 'KRDMA'), ('ISBTR', 'ISCTR'), ('ISATR', 'ISCTR')]:
    pa, pb = px(a)['c'], px(b)['c']
    va = px(a)['v']
    df = pd.concat([pa.rename('a'), pb.rename('b'), va.rename('va')], axis=1).dropna(); df = df[(df.index >= '2010-01-01') & (df['va'] > 0)]
    lr = np.log(df['a'] / df['b'])
    x = lr - lr.rolling(60).mean(); x = x.dropna(); phi = np.corrcoef(x[:-1], x[1:])[0, 1]
    yr = np.exp(lr.groupby(lr.index.year).mean()).round(2)
    o = dict(pair=f'{a}/{b}', n=len(lr), ratio_last=float(np.exp(lr.iloc[-1])), ratio_1y_min=float(np.exp(lr[lr.index >= '2025-10-30'].min())), ratio_1y_max=float(np.exp(lr[lr.index >= '2025-10-30'].max())),
             ratio_med_all=float(np.exp(lr.median())), adf_p=adfuller(lr, maxlag=10, autolag=None)[1], adf_p_2021=adfuller(lr[lr.index >= '2021-01-01'], maxlag=10, autolag=None)[1],
             hl_dev60=np.log(.5) / np.log(phi) if 0 < phi < 1 else np.nan, sd_daily_bps=1e4 * lr.diff().std(), yearly_ratio=yr.to_dict())
    rows.append(o)
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_classes.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 400)
print(D.round(3).to_string())
