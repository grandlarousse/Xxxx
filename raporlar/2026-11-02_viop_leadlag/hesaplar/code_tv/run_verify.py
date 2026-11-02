"""candidates.json'daki adayların halka açık TradingView sembol sayfalarını sırayla (nazikçe, ~1 sn arayla) okur.
Sonuçlar cache.jsonl'e eklenir (yeniden başlatılabilir). Başlık sahteciliği / iç API YOK."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tvpage
D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(D, 'cache_b.jsonl' if '--nonpriority' in sys.argv else 'cache.jsonl')
CACHES = [os.path.join(D, 'cache.jsonl'), os.path.join(D, 'cache_b.jsonl')]

def load_cache():
    c = {}
    for cf in CACHES:
      if os.path.exists(cf):
        for l in open(cf, encoding='utf8'):
            try:
                r = json.loads(l)
                if r.get('http') in ('200', '404'):
                    c[r['tv']] = r
            except Exception:
                pass
    return c

def ok(r):
    return r is not None and r.get('http') == '200' and bool(r.get('info'))

def get(tv, cache, f):
    if tv in cache:
        return cache[tv]
    for attempt in range(3):
        r = tvpage.fetch(tv)
        r['ts'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        time.sleep(1.0)
        if r['http'] in ('200', '404'):
            break
        if r['http'] == '429':
            time.sleep(30)
        else:
            time.sleep(3)
    f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
    cache[tv] = r
    return r

def main():
    rows = json.load(open(os.path.join(D, 'candidates.json'), encoding='utf8'))
    only_priority = '--priority' in sys.argv
    cache = load_cache()
    n = 0
    with open(CACHE, 'a', encoding='utf8') as f:
        order = sorted(rows, key=lambda d: not d['priority'])  # önce öncelikli
        if '--nonpriority' in sys.argv: order = order[::-1]
        for d in order:
            if only_priority and not d['priority']:
                continue
            if '--nonpriority' in sys.argv and d['priority']:
                continue
            found = False
            for i, c in enumerate(d['cands']):
                if found and not d['priority']:
                    break
                if d['priority'] and i >= 4:
                    break
                r = get(c, cache, f); n += 1
                found = found or ok(r)
            for c in d['alt_cands'][:4]:
                get(c, cache, f); n += 1
    print('done', n, 'cache', len(cache))

if __name__ == '__main__':
    main()
