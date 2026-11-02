"""Elle aday dene: python3 -I manual.py EXCH:SYM ... -> cache_manual.jsonl'e ekler ve özet basar"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tvpage
D = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(D, 'cache_manual.jsonl'), 'a', encoding='utf8') as f:
    for s in sys.argv[1:]:
        r = tvpage.fetch(s); r['ts'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
        i = r['info']
        print(s, r['http'], r['eff'].split(' ')[-1], '|', i.get('resolved_symbol'), '|', i.get('description'), '|', i.get('type'), i.get('currency'), i.get('source'))
        time.sleep(1.0)
