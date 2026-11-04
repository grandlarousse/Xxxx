"""Merge raw half-month research + verify outputs into one calendar.

Usage: python3 -I merge.py OUT_DIR task1.output task2.output ...
Writes OUT_DIR/merged.json and OUT_DIR/compact.txt
"""
import sys, json, datetime, os, re

out_dir = sys.argv[1]
files = sys.argv[2:]
SCOPE_RANK = {'core': 0, 'kisi': 1, 'post_1912': 2, 'pre_1352': 3, 'kultur': 4}
CONF_RANK = {'high': 0, 'medium': 1, 'low': 2}

start = datetime.date(2026, 11, 4)
order = []
for i in range(365):
    d = start + datetime.timedelta(days=i)
    order.append(f"{d.month:02d}-{d.day:02d}")
day_map = {k: {'date': k, 'events': [], 'primaryId': None, 'gap_note': ''} for k in order}

halves = []
for f in files:
    obj = json.load(open(f))
    res = obj.get('result', obj)
    halves += res.get('halves', [])
    if res.get('missing'):
        print('MISSING in', f, res['missing'])

stats = dict(halves=len(halves), events_in=0, refuted=0, corrected=0, moved=0, replacements=0,
             unverifiable=0, not_checked=0, confirmed=0)
moves = []
covered = set()
for h in halves:
    r = h.get('research')
    v = h.get('verify') or {}
    if not r:
        print('no research for', h.get('key'))
        continue
    by_id = {x['id']: x for x in v.get('verdicts', [])}
    for day in r.get('days', []):
        t = day_map.get(day['date'])
        if t is None:
            print('unknown date', day['date'])
            continue
        covered.add(day['date'])
        t['gap_note'] = day.get('gap_note', '') or ''
        evs = day.get('events', []) or []
        prim = evs[day['primary']]['id'] if isinstance(day.get('primary'), int) and 0 <= day['primary'] < len(evs) else None
        for e in evs:
            stats['events_in'] += 1
            vv = by_id.get(e.get('id'))
            e['verdict'] = vv['verdict'] if vv else 'not_checked'
            e['verify_note'] = vv.get('note', '') if vv else ''
            if vv and vv.get('sources'):
                e['verify_sources'] = vv['sources']
            stats[e['verdict']] = stats.get(e['verdict'], 0) + 1
            if e['verdict'] == 'refuted':
                continue
            if e['verdict'] == 'corrected':
                for src, dst in (('corrected_year', 'year'), ('corrected_title', 'title_tr'),
                                 ('corrected_detail', 'detail_tr'), ('corrected_calendar_note', 'calendar_note'),
                                 ('corrected_scope', 'scope')):
                    if vv.get(src):
                        e[dst] = vv[src]
                cd = vv.get('corrected_date') or ''
                if re.fullmatch(r'\d\d-\d\d', cd) and cd != day['date']:
                    e['moved_from'] = day['date']
                    moves.append((cd, e))
                    continue
            t['events'].append(e)
            if e.get('id') == prim:
                t['primaryId'] = e['id']
    for rp in v.get('replacements', []) or []:
        t = day_map.get(rp.get('date'))
        if t is None or not rp.get('event'):
            continue
        e = dict(rp['event'])
        e['id'] = f"{rp['date']}#r{len(t['events'])}"
        e['verdict'] = 'replacement_by_verifier'
        t['events'].append(e)
        stats['replacements'] += 1
        if not t['primaryId']:
            t['primaryId'] = e['id']

for to, e in moves:
    t = day_map.get(to)
    if t is None:
        print('cannot move', e.get('id'), 'to', to)
        continue
    e['id'] = f"{to}#m{len(t['events'])}"
    t['events'].append(e)
    stats['moved'] += 1

gaps = []
for k in order:
    t = day_map[k]
    if t['primaryId'] and not any(e['id'] == t['primaryId'] for e in t['events']):
        t['primaryId'] = None
    if not t['primaryId'] and t['events']:
        best = sorted(t['events'], key=lambda e: (SCOPE_RANK.get(e.get('scope'), 5), CONF_RANK.get(e.get('date_confidence'), 3)))[0]
        t['primaryId'] = best['id']
    if not t['events']:
        gaps.append(k)

stats['days_covered_by_research'] = len(covered)
stats['empty_days'] = len(gaps)
stats['empty_list'] = gaps
json.dump({'order': order, 'days': day_map, 'stats': stats}, open(os.path.join(out_dir, 'merged.json'), 'w'),
          ensure_ascii=False, indent=1)

lines = []
for k in order:
    t = day_map[k]
    if not t['events']:
        lines.append(f"{k} | BOŞ GÜN")
    for e in t['events']:
        note = (e.get('calendar_note') or '')[:110]
        lines.append(f"{e['id']} | {k} | {e.get('year')} | {e.get('scope')} | {e.get('date_confidence')} | "
                     f"{e.get('verdict')} | {'ANA' if e['id'] == t['primaryId'] else '-'} | {e.get('title_tr')}"
                     + (f" [not: {note}]" if note else ''))
open(os.path.join(out_dir, 'compact.txt'), 'w').write('\n'.join(lines))
print(json.dumps({k: v for k, v in stats.items() if k != 'empty_list'}, ensure_ascii=False))
print('empty days:', gaps)
