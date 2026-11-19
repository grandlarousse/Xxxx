#!/usr/bin/env python3
"""Havacilik/savunma + DXY veri indirme. Calistir: python3 01_veri_indir.py  (cikti: ../veri/)"""
import os, io, json, re, subprocess, urllib.request, urllib.parse
import pandas as pd
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'veri')
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0'}
def get(url, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
    b = r.read()
    return b if binary else b.decode('utf-8', 'replace')

# 1) Yahoo
TICK = ['DX-Y.NYB','EURUSD=X','ITA','XAR','PPA','EUAD','^GSPC','URTH','BA','AIR.PA','GE','RTX','LMT','RHM.DE','SAF.PA','RR.L','BA.L','^DJUSAE','^DJSASD']
rows = []
for t in TICK:
    u = 'https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=0&period2=1900000000&interval=1d' % urllib.parse.quote(t, safe='=.-')
    try:
        j = json.loads(get(u))['chart']['result'][0]
        ts = j['timestamp']; q = j['indicators']['quote'][0]['close']
        ac = (j['indicators'].get('adjclose') or [{}])[0].get('adjclose', q)
        for a, c, d in zip(ts, q, ac):
            if c is not None:
                rows.append((pd.to_datetime(a, unit='s').normalize(), t, c, d))
        print('Yahoo OK', t, len(ts))
    except Exception as e:
        print('Yahoo FAIL', t, e)
y = pd.DataFrame(rows, columns=['tarih','ticker','close','adjclose']).drop_duplicates(['tarih','ticker'], keep='last').sort_values(['ticker','tarih'])
y.to_csv(f'{OUT}/yahoo_gunluk.csv', index=False)
w = y.pivot(index='tarih', columns='ticker', values='adjclose')
w.groupby(w.index.to_period('M')).last().rename_axis('ay').to_csv(f'{OUT}/yahoo_aylik.csv')

# 2) MSCI (World 990100, Europe 990500; A&D kodlari bulunursa ekle)
MSCI = {'990100':'MSCI World','990500':'MSCI Europe'}
MSCI.update(json.loads(os.environ.get('MSCI_EXTRA','{}')))
rows = []
for code, name in MSCI.items():
    for cur in ['USD','EUR']:
        for var in ['NETR','STRD']:
            u = ('https://app2.msci.com/products/service/index/indexmaster/getLevelDataForGraph?currency_symbol=%s&index_variant=%s'
                 '&start_date=19981231&end_date=20261118&data_frequency=END_OF_MONTH&index_codes=%s') % (cur, var, code)
            try:
                for d in json.loads(get(u))['indexes']['INDEX_LEVELS']:
                    rows.append((pd.to_datetime(str(d['calc_date'])), code, name, cur, var, d['level_eod']))
            except Exception as e:
                print('MSCI FAIL', code, cur, var, e)
pd.DataFrame(rows, columns=['tarih','kod','ad','para','varyant','seviye']).to_csv(f'{OUT}/msci_aylik.csv', index=False)

# 3) Fed G.17
txt = get('https://www.federalreserve.gov/releases/g17/ipdisk/ip_sa.txt')
rows = []
for ln in txt.splitlines():
    p = ln.split()
    if p and p[0] in ('"G3364"','"G336411T3"','"G3364T9"') and len(p) >= 3:
        for m, v in enumerate(p[2:14], 1):
            rows.append((p[0].strip('"'), int(p[1]), m, float(v)))
f = pd.DataFrame(rows, columns=['seri','yil','ay','deger'])
f['tarih'] = pd.to_datetime(dict(year=f.yil, month=f.ay, day=1))
f[['tarih','seri','deger']].sort_values(['seri','tarih']).to_csv(f'{OUT}/fed_ip_havacilik.csv', index=False)

# 4) Eurostat C30.3
rows = []
for geo in ['FR','DE','EU27_2020','IT','ES']:
    u = f'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_inpr_m?format=JSON&geo={geo}&nace_r2=C303&s_adj=SCA&unit=I21'
    try:
        j = json.loads(get(u)); idx = j['dimension']['time']['category']['index']; inv = {v:k for k,v in idx.items()}
        for k, v in j['value'].items(): rows.append((inv[int(k)], geo, v))
        print('Eurostat OK', geo)
    except Exception as e:
        print('Eurostat FAIL', geo, e)
pd.DataFrame(rows, columns=['donem','geo','endeks_2021_100']).sort_values(['geo','donem']).to_csv(f'{OUT}/eurostat_c303.csv', index=False)

# 5) Airbus/Boeing yillik (Wikipedia)
html = get('https://en.wikipedia.org/wiki/Competition_between_Airbus_and_Boeing')
t = pd.read_html(io.StringIO(html))
x = [d for d in t if d.shape[1] == 22][0]
x.columns = ['|'.join(map(str, c)) for c in x.columns]
def col(s): return [c for c in x.columns if c.startswith(s)][0]
res = pd.DataFrame({'yil': x[col('Year')], 'airbus_teslimat': x[col('Airbus[50][25]|Deli')], 'boeing_teslimat': x[col('Boeing[49]|Deli\xadveries|')],
                    'airbus_net_siparis': x[col('Airbus[50][25]|Orders')], 'boeing_net_siparis': x[col('Boeing[49]|Orders')]})
res['yil'] = pd.to_numeric(res['yil'].astype(str).str.extract(r'(\d{4})')[0], errors='coerce')
res = res.dropna(subset=['yil']).astype({'yil': int})
for c in res.columns[1:]: res[c] = pd.to_numeric(res[c].astype(str).str.replace(r'[^\d\-]', '', regex=True), errors='coerce')
res.sort_values('yil').to_csv(f'{OUT}/airbus_boeing_yillik.csv', index=False)
print(res.sort_values('yil').tail(10).to_string())
