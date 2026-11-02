"""Bağımsız TradingView sayfa doğrulayıcı (v_tv).
Yalnızca HALKA AÇIK https://www.tradingview.com/symbols/<BORSA>-<SEMBOL>/ sayfası düz GET ile okunur:
curl varsayılan User-Agent, Origin/Referer/çerez taklidi YOK, iç API / websocket YOK. ~1 istek/sn, tek işçi.
Sayfa HTML'i dl/tvpages/ altına (güvenilmeyen veri dizini) yazılır; ayrıştırma bu betikte yapılır.
Kullanım: python3 -I fetch.py codes.txt  -> code_v_tv/fetch_cache.jsonl'a ekler (önbellekte varsa atlar)."""
import json, os, re, subprocess, sys, time, urllib.parse

ROOT = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
DL = f'{ROOT}/dl/tvpages'
CACHE = f'{ROOT}/out/code_v_tv/fetch_cache.jsonl'
os.makedirs(DL, exist_ok=True)


def first(pat, s):
    m = re.search(pat, s)
    if not m:
        return None
    try:
        return json.loads('"' + m.group(1) + '"')
    except Exception:
        return m.group(1)


def fetch(code, timeout=30):
    exch, sym = code.split(':', 1)
    path = urllib.parse.quote(f'{exch}-{sym}', safe='-._~!')
    url = f'https://www.tradingview.com/symbols/{path}/'
    fn = os.path.join(DL, re.sub(r'[^A-Za-z0-9_.!-]', '_', f'{exch}-{sym}') + '.html')
    p = subprocess.run(['curl', '-sS', '-L', '--max-redirs', '3', '--compressed', '-m', str(timeout),
                        '-o', fn, '-w', '%{http_code} %{url_effective}', url], capture_output=True)
    w = p.stdout.decode('utf8', 'replace').strip().split(' ', 1)
    http, eff = (w + [''])[:2]
    body = ''
    try:
        with open(fn, 'r', encoding='utf8', errors='replace') as f:
            body = f.read()
    except Exception:
        pass
    title = first(r'<title>([^<]*)</title>', body)
    rec = dict(code=code, url=url, http=http, eff=eff, title=title,
               pro_symbol=first(r'"pro_symbol":"((?:[^"\\]|\\.)*)"', body),
               resolved=first(r'"resolved_symbol":"((?:[^"\\]|\\.)*)"', body),
               short_desc=first(r'"short_description":"((?:[^"\\]|\\.)*)"', body),
               desc=first(r'"description":"((?:[^"\\]|\\.)*)"', body),
               isin=first(r'"isin_displayed":"((?:[^"\\]|\\.)*)"', body),
               typ=first(r'"type":"((?:[^"\\]|\\.)*)"', body),
               exchange=first(r'"exchange":"((?:[^"\\]|\\.)*)"', body),
               ts=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    return rec


def load_cache():
    d = {}
    if os.path.exists(CACHE):
        for line in open(CACHE, encoding='utf8'):
            try:
                r = json.loads(line)
                d[r['code']] = r
            except Exception:
                pass
    return d


if __name__ == '__main__':
    codes = [c.strip() for c in open(sys.argv[1], encoding='utf8') if c.strip() and ':' in c]
    done = load_cache()
    todo = [c for c in dict.fromkeys(codes) if c not in done]
    print(f'{len(codes)} kod, {len(todo)} yeni', flush=True)
    with open(CACHE, 'a', encoding='utf8') as out:
        for i, c in enumerate(todo):
            try:
                r = fetch(c)
            except Exception as e:
                r = dict(code=c, http='ERR', err=str(e))
            out.write(json.dumps(r, ensure_ascii=False) + '\n'); out.flush()
            print(i, c, r.get('http'), r.get('pro_symbol'), (r.get('short_desc') or r.get('desc') or '')[:60], flush=True)
            time.sleep(1.1)
