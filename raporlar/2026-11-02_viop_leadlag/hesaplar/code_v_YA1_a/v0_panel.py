"""v_YA1_a — bağımsız panel (ll.py KULLANILMAZ).
Temizlik:
 - index = ldate (BIST yerel tarihi); yinelenen tarih -> son kayıt.
 - bayat gün = v==0 VE h==l  -> satır atılır (işlem yok). (v==0 ama h!=l -> korunur; SASA 2025-06+ Yahoo hacim eksikliği)
 - o<=0, NaN veya o, [l,h] dışında -> açılış NaN (gün-içi/gap hesaplanmaz).
 - R = adj_t/adj_{t-1} (kendi işlem takviminde önceki satır). Kurumsal işlem eşiği rejime bağlı: <2020-03-13 |R-1|>0,205, sonrası >0,105 -> 'ca' bayrağı (getiri NaN).
 - Bölünmesiz (gerçek) fiyat: c_unadj = c * (t'den sonraki bölünme oranlarının çarpımı) (Yahoo c bölünme-düzeltilmiş).
Çıktı: _panel.parquet (uzun format: stock,date,o,h,l,c,adj,v,c_unadj)
"""
import os, json, numpy as np, pandas as pd
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
END = pd.Timestamp('2026-10-30')

def stocks():
    c = pd.read_csv(SCR + '/data/catalog.csv')
    b = c[c.group.isin(['VIOP', 'BIST_other']) & ~c.sym.str.startswith('X')]
    return sorted(b.sym.tolist())

def load(sym):
    d = pd.read_parquet(f'{SCR}/data/daily/{sym}.parquet')
    d.index = pd.DatetimeIndex(pd.to_datetime(d['ldate']).values).normalize()
    d = d[~d.index.duplicated(keep='last')].sort_index()
    d = d[(d.index <= END)]
    d = d.dropna(subset=['c', 'adj'])
    d = d[(d.c > 0) & (d.adj > 0)]
    stale = (d.v.fillna(0) == 0) & (d.h == d.l)
    d = d[~stale].copy()
    bad_o = (d.o <= 0) | d.o.isna() | (d.o > d.h * 1.001) | (d.o < d.l * 0.999)
    d.loc[bad_o, 'o'] = np.nan
    # bölünmesiz fiyat
    sf = pd.Series(1.0, index=d.index)
    mp = f'{SCR}/data/meta/{sym}.json'
    if os.path.exists(mp):
        m = json.load(open(mp))
        for dt, ratio in (m.get('splits') or {}).items():
            try:
                a, b = ratio.split(':'); rr = float(a) / float(b)
            except Exception:
                continue
            sf[d.index < pd.Timestamp(dt)] *= rr
    d['c_unadj'] = d.c * sf
    return d[['o', 'h', 'l', 'c', 'adj', 'v', 'c_unadj']]

def build():
    out = []
    for s in stocks():
        d = load(s); d['stock'] = s.replace('.IS', ''); out.append(d)
    P = pd.concat(out); P.index.name = 'date'; P = P.reset_index()
    P.to_parquet(HERE + '/_panel.parquet')
    return P

def index_ret(sym='XU100'):
    d = pd.read_parquet(f'{SCR}/data/daily/{sym}.IS.parquet')
    d.index = pd.DatetimeIndex(pd.to_datetime(d['ldate']).values).normalize()
    d = d[~d.index.duplicated(keep='last')].sort_index(); d = d[d.index <= END]
    d = d.dropna(subset=['c'])
    out = pd.DataFrame({'lc': np.log(d.adj), 'cc': np.log(d.adj).diff(), 'intra': np.log(d.c / d.o)})
    out['gap'] = out.cc - out.intra
    return out

if __name__ == '__main__':
    P = build()
    print(P.shape, P.stock.nunique(), P.date.min(), P.date.max())
