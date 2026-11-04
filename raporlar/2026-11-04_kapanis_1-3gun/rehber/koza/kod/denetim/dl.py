"""Denetim: bağımsız Yahoo günlük indirici (ham JSON da saklanır)."""
import json, time, sys, requests, pandas as pd, os
OUT = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/veri'
def get(sym):
    url = f'https://query2.finance.yahoo.com/v8/finance/chart/{sym}'
    p = {'period1': 946684800, 'period2': int(time.time()) + 86400, 'interval': '1d', 'events': 'div,splits', 'includePrePost': 'false'}
    for a in range(6):
        try:
            r = requests.get(url, params=p, headers={'User-Agent': 'Mozilla/5.0'}, timeout=40)
            if r.status_code == 200: break
        except Exception as e: print(e)
        time.sleep(2 ** a)
    j = r.json(); json.dump(j, open(f'{OUT}/{sym}.json', 'w'))
    res = j['chart']['result'][0]; q = res['indicators']['quote'][0]
    adj = res['indicators']['adjclose'][0]['adjclose']
    ts = pd.to_datetime(res['timestamp'], unit='s', utc=True)
    df = pd.DataFrame({'o': q['open'], 'h': q['high'], 'l': q['low'], 'c': q['close'], 'adj': adj, 'v': q['volume'], 'ts': ts})
    df['d'] = ts.tz_convert('Europe/Istanbul').tz_localize(None).normalize()
    df.to_parquet(f'{OUT}/{sym}.parquet'); print(sym, len(df), df.d.iloc[-1], res['meta'].get('regularMarketTime'))
for s in sys.argv[1:]: get(s); time.sleep(0.5)
