import sys, os, re, json, datetime
BASE = sys.argv[1]
TRK = ['osmanlı','rumeli','balkan','edirne','selanik','bulgar','sırp','yunan','arnavut','bosna','hersek','makedon','kosova','macar','belgrad','budin','viyana','eflak','boğdan','mora','trakya','mübadele','mübadil','lozan','tuna','varna','niğbolu','mohaç','plevne','ayastefanos','bükreş','karlofça','pasarofça','sofya','filibe','üsküp','manastır','yanya','işkodra','saraybosna','dobruca','kırcaali','gümülcine','iskeçe','karadağ','romanya','habsburg','avusturya','eğri','zigetvar','kanije','uyvar','kamaniçe','lehistan','gelibolu','kırklareli','tekirdağ','çatalca','göçmen','muhacir','padişah','sultan','sadrazam','paşa','yeniçeri','sancak','beylerbeyi','rusçuk','şumnu','silistre','vidin','niş','prizren','mostar','travnik','kavala','drama','serez','dimetoka','gümülcine','lüleburgaz','kırkkilise','meriç','istanbul antlaşması','londra antlaşması','berlin','meşrutiyet','ittihat','girit','eğriboz','pomak','torbeş','gacal','yörük','akıncı','evlad-ı fatihan']
ENK = ['ottoman','rumelia','rumeli','balkan','adrianople','edirne','thessaloniki','salonica','salonika','bulgaria','serbia','serbian','greek','greece','albania','bosnia','herzegovina','macedonia','kosovo','hungar','belgrade','buda','vienna','wallachia','moldavia','morea','thrace','danube','varna','nicopolis','mohács','mohacs','plevna','pleven','san stefano','bucharest','karlowitz','passarowitz','sofia','plovdiv','philippopolis','skopje','bitola','monastir','ioannina','janina','shkodër','shkoder','scutari','sarajevo','dobruja','dobrudja','montenegr','romania','habsburg','szigetvár','szigetvar','kanizsa','eger','kamianets','kamieniec','gallipoli','turk','sultan','janissar','vizier','pasha','crete','cretan','negroponte','euboea','lepanto','mostar','nis,','niš','vidin','ruse','silistra','shumen','kardzhali','komotini','xanthi','kavala','serres','drama']
def lines_for(txt, lang):
    out = []; sec = ''
    for raw in txt.split('\n'):
        l = raw.strip()
        m = re.match(r'^==+\s*(.*?)\s*==+$', l)
        if m:
            sec = m.group(1); continue
        if not l.startswith('*'): continue
        ym = re.search(r'\[\[(\d{3,4})(?:\|[^\]]*)?\]\]|^\*+\s*(\d{3,4})\b|\{\{[^}]*?(\d{3,4})', l)
        year = None
        for g in (ym.groups() if ym else []):
            if g: year = int(g); break
        if year is None or year < 1300 or year > 2010: continue
        low = l.lower()
        keys = TRK if lang == 'tr' else ENK
        if any(k in low for k in keys):
            clean = re.sub(r'\[\[([^\]|]*\|)?([^\]]*)\]\]', r'\2', l)
            clean = re.sub(r'<ref[^>]*>.*?</ref>|<ref[^>]*/>', '', clean)
            clean = re.sub(r'\{\{[^{}]*\}\}', '', clean)
            clean = re.sub(r"'{2,}", '', clean).strip('* ').strip()
            out.append(f"[{lang}|{sec[:20]}] {clean[:300]}")
    return out
start = datetime.date(2026, 11, 4)
bymonth = {}
for i in range(365):
    d = start + datetime.timedelta(days=i)
    key = f"{d.month:02d}-{d.day:02d}"
    res = []
    for lang in ('tr', 'en'):
        fn = os.path.join(BASE, 'wiki_' + lang, key + '.txt')
        if os.path.exists(fn):
            res += lines_for(open(fn).read(), lang)
    bymonth.setdefault(f"{d.month:02d}", {})[key] = res
json.dump(bymonth, open(os.path.join(BASE, 'seed_by_month.json'), 'w'), ensure_ascii=False, indent=0)
for m, days in sorted(bymonth.items()):
    n = sum(len(v) for v in days.values()); chars = sum(len(x) for v in days.values() for x in v)
    print(m, len(days), 'days', n, 'lines', chars, 'chars', 'empty days:', sum(1 for v in days.values() if not v))
