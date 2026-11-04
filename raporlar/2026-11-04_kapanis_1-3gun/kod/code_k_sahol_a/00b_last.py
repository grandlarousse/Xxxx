"""Yahoo günlük barında son günün kapanışı (c) henüz NaN ise: meta.regularMarketPrice (18:05 sonrası = kapanış seansı fiyatı) ile tamamla.
Çıktı: dl_k_sahol_a/daily_last.parquet (sym, o,h,l,c,adj,v,ldate). Ortak veriye dokunmaz."""
import requests, pandas as pd, numpy as np, datetime as dt, time
NEW = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_k_sahol_a'
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64)'
rows = []
for sym in ['SAHOL.IS', 'AKBNK.IS', 'XU100.IS', 'XU030.IS', 'XBANK.IS']:
    j = S.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}', params={'range': '5d', 'interval': '1d'}, timeout=30).json()['chart']['result'][0]
    q = j['indicators']['quote'][0]; m = j['meta']
    idx = pd.to_datetime(j['timestamp'], unit='s', utc=True)
    df = pd.DataFrame({'o': q['open'], 'h': q['high'], 'l': q['low'], 'c': q['close'], 'v': q['volume']}, index=idx)
    df['ldate'] = idx.tz_convert('Europe/Istanbul').tz_localize(None).normalize()
    old = pd.read_parquet(f'{NEW}/daily/{sym}.parquet'); lastd = old['ldate'].max()
    rmt = pd.Timestamp(m['regularMarketTime'], unit='s', tz='UTC').tz_convert('Europe/Istanbul')
    for t, r in df[df.ldate > lastd].iterrows():
        c = r.c
        if (pd.isna(c)) and rmt.tz_localize(None).normalize() == r.ldate and rmt.hour * 60 + rmt.minute >= 18 * 60 + 5:
            c = m['regularMarketPrice']
        if pd.isna(c): continue
        rows.append(dict(sym=sym, o=r.o if pd.notna(r.o) else c, h=max(r.h, c) if pd.notna(r.h) else c, l=min(r.l, c) if pd.notna(r.l) else c, c=float(c), adj=float(c), v=r.v, ldate=r.ldate, _ts=t))
        print(sym, r.ldate.date(), 'c=', c, 'kaynak=', 'regularMarketPrice' if pd.isna(r.c) else 'bar', 'rmt=', rmt)
    time.sleep(0.3)
E = pd.DataFrame(rows).set_index('_ts'); E.index.name = None
E.to_parquet(f'{NEW}/daily_last.parquet'); print(E)
