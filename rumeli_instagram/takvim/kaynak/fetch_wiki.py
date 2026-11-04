import sys, time, urllib.request, urllib.parse, os, json, datetime
OUT = sys.argv[1]
TR = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
EN = ['January','February','March','April','May','June','July','August','September','October','November','December']
UA = 'RumeliHistoryCalendar/1.0 (personal research script; python-urllib)'
def get(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode('utf-8')
        except Exception as e:
            time.sleep(3 * (attempt + 1))
    return None
start = datetime.date(2026, 11, 4)
for i in range(365):
    d = start + datetime.timedelta(days=i)
    for lang, names, sub in (('tr', TR, 'wiki_tr'), ('en', EN, 'wiki_en')):
        title = f"{d.day} {names[d.month-1]}" if lang == 'tr' else f"{names[d.month-1]} {d.day}"
        fn = os.path.join(OUT, sub, f"{d.month:02d}-{d.day:02d}.txt")
        if os.path.exists(fn) and os.path.getsize(fn) > 500:
            continue
        url = f"https://{lang}.wikipedia.org/w/index.php?title={urllib.parse.quote(title.replace(' ', '_'))}&action=raw"
        txt = get(url)
        if txt:
            open(fn, 'w').write(txt)
        else:
            print('FAIL', lang, title, flush=True)
        time.sleep(0.6)
print('DONE', flush=True)
