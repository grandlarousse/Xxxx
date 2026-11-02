"""tv_final.csv biçim denetimi (v_tv): borsa kuralları + Çin öneki + doğrulama kapsamı."""
import json, re
import pandas as pd
from common import OUT, CODE, tv_tokens, CHINA_PREFIX, VIOP47

f = pd.read_csv(f'{OUT}/tv_final.csv', dtype=str).fillna('')
fc = {}
for l in open(f'{CODE}/fetch_cache.jsonl', encoding='utf8'):
    r = json.loads(l); fc[r['code']] = r
s40 = set(pd.read_csv(f'{CODE}/sample40_webfetch.csv', dtype=str).tv_best)

probs = []
allc = []
for _, r in f.iterrows():
    for col in ('tv_kodu', 'tv_alternatif'):
        for c, _ in tv_tokens(r[col]):
            allc.append((r.yahoo, col, c))
            ex, sy = c.split(':', 1)
            if ex in CHINA_PREFIX or ex in ('SIDX', 'FUT', 'SINA'):
                probs.append((r.yahoo, c, 'ÇİN/sahte önek'))
            if ex == 'KRX' and not re.fullmatch(r'\d{6}|KOSPI|KOSPI200', sy):
                probs.append((r.yahoo, c, 'KRX 6 hane değil'))
            if ex == 'TSE' and not re.fullmatch(r'\d{4}[A-Z]?', sy):
                probs.append((r.yahoo, c, 'TSE 4 hane değil'))
            if re.search(r'\.(KS|T|HK|SS|SZ|IS|L|PA|DE|MX)$', sy) and ex != 'LSE':
                probs.append((r.yahoo, c, 'Yahoo soneki kalmış'))
            if ex in ('NYSEARCA', 'ARCA', 'BATS'):
                probs.append((r.yahoo, c, 'ETF öneki TV biçiminde değil'))
            if r.yahoo.endswith('.MX') and ex == 'BMV' and re.search(r'[A-Z]{4,}[AB]$', sy) and '/' not in sy:
                probs.append((r.yahoo, c, "BMV seri harfi '/' ile yazılmalı"))
            if c in ('NYSE:GOLD',) and 'Barrick' in r.aciklama:
                probs.append((r.yahoo, c, 'Barrick = NYSE:B'))
            if c == 'NYSE:IAG' and 'Airlines' in r.aciklama:
                probs.append((r.yahoo, c, 'IAG havayolu = LSE:IAG'))
            if c == 'NYSE:HEI' and 'Heidelberg' in r.aciklama:
                probs.append((r.yahoo, c, 'Heidelberg = XETR:HEI'))
            if '<KOD>' not in c and not any(ch in c for ch in '*()'):
                fr = fc.get(c)
                if fr is not None and fr.get('http') != '200':
                    probs.append((r.yahoo, c, f"sayfa HTTP {fr.get('http')}"))

codes = {c for _, _, c in allc if '<KOD>' not in c}
read = {c for c in codes if c in fc and fc[c].get('http') == '200'}
notread = sorted(codes - set(fc))
print('tv_final satır:', len(f), '| benzersiz kod:', len(codes), '| v_tv sayfa okuması 200:', len(read),
      '| okunmamış:', len(notread), '| WebFetch örneklemi:', len(s40))
print('okunmamış kodlar:', notread[:40])
need = [f'BIST:{k}' for k in VIOP47] + [f'BIST:{k}1!' for k in VIOP47]
miss = [c for c in need if c not in set(f.tv_kodu) | {x for s in f.tv_alternatif for x in s.split(' | ')}]
print('47 hisse + 47 pay vadelisi eksik:', miss)
pr = pd.DataFrame(probs, columns=['yahoo', 'kod', 'sorun']).drop_duplicates()
print('biçim sorunları:', len(pr)); print(pr.to_string())
pr.to_csv(f'{CODE}/lint_sorunlar.csv', index=False)
