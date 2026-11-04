"""Render merged calendar (+ optional editor actions) to Markdown, CSV and XLSX.

Usage: python3 -I render.py MERGED_JSON ACTIONS_JSON_OR_- OUT_DIR
"""
import sys, json, csv, datetime, os, re

merged = json.load(open(sys.argv[1]))
actions = [] if sys.argv[2] == '-' else json.load(open(sys.argv[2]))
out_dir = sys.argv[3]
os.makedirs(out_dir, exist_ok=True)

order, days = merged['order'], merged['days']
SCOPE_RANK = {'core': 0, 'kisi': 1, 'post_1912': 2, 'pre_1352': 3, 'kultur': 4}
CONF_RANK = {'high': 0, 'medium': 1, 'low': 2}
SCOPE_LABEL = {'core': '', 'kisi': 'Kişi', 'post_1912': '1912 sonrası', 'pre_1352': '1352 öncesi', 'kultur': 'Gelenek'}
SCOPE_CSV = {'core': '1352–1912', 'kisi': 'Kişi', 'post_1912': '1912 sonrası', 'pre_1352': '1352 öncesi', 'kultur': 'Gelenek'}
AY = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
GUN = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
VERDICT_TR = {'confirmed': 'doğrulandı', 'corrected': 'düzeltilerek doğrulandı', 'unverifiable': 'kontrol edilemedi',
              'not_checked': 'ikinci kontrol yapılmadı', 'replacement_by_verifier': 'kontrolcü ekledi'}

# ---- apply editor actions ----
applied = []
idx = {e['id']: (k, e) for k, t in days.items() for e in t['events']}
for a in actions:
    k_e = idx.get(a.get('id'))
    if not k_e:
        applied.append(('SKIP-unknown-id', a)); continue
    k, e = k_e
    t = days[k]
    if a['type'] == 'drop':
        t['events'] = [x for x in t['events'] if x['id'] != e['id']]
        if t['primaryId'] == e['id']:
            t['primaryId'] = None
    elif a['type'] == 'set_primary':
        t['primaryId'] = e['id']
    elif a['type'] == 'edit_title' and a.get('value'):
        e['title_tr'] = a['value']
    elif a['type'] == 'flag':
        e['editor_flag'] = a.get('value') or a.get('reason', '')
    applied.append((a['type'], a.get('id')))
for k in order:
    t = days[k]
    if not t['primaryId'] and t['events']:
        t['primaryId'] = sorted(t['events'], key=lambda e: (SCOPE_RANK.get(e.get('scope'), 5), CONF_RANK.get(e.get('date_confidence'), 3)))[0]['id']


def real_date(k):
    m, d = map(int, k.split('-'))
    y = 2026 if (m == 11 and d >= 4) or m == 12 else 2027
    return datetime.date(y, m, d)


def year_key(e):
    m = re.search(r'\d{3,4}', str(e.get('year', '')))
    return int(m.group()) if m else 9999


def sorted_events(t):
    prim = [e for e in t['events'] if e['id'] == t['primaryId']]
    rest = sorted([e for e in t['events'] if e['id'] != t['primaryId']],
                  key=lambda e: (SCOPE_RANK.get(e.get('scope'), 5), year_key(e)))
    return prim + rest


def good_sources(e):
    src = [s for s in (e.get('sources') or []) + (e.get('verify_sources') or []) if isinstance(s, str) and s.startswith('http')]
    seen, out = set(), []
    for s in src:
        s = s.split(' ')[0].strip().rstrip('.,;')
        if s.endswith(')') and s.count('(') < s.count(')'):
            s = s[:-1]
        if s not in seen:
            seen.add(s); out.append(s)
    # prefer non day-page sources first
    day_page = re.compile(r'wikipedia\.org/wiki/(\d{1,2}_[A-Za-zÇŞĞÜÖİçşğüöı]+|[A-Z][a-z]+_\d{1,2})$')
    return sorted(out, key=lambda s: 1 if day_page.search(s) else 0)


def needs_warning(e):
    return e.get('date_confidence') in ('medium', 'low')


def md_url(u):
    return u.replace('(', '%28').replace(')', '%29').replace(' ', '%20')


def clean(s):
    return re.sub(r'\s+', ' ', (s or '').strip())


# ---- stats ----
n_days = len(order)
n_core_primary = sum(1 for k in order if days[k]['events'] and next(e for e in days[k]['events'] if e['id'] == days[k]['primaryId']).get('scope') == 'core')
n_empty = sum(1 for k in order if not days[k]['events'])
n_events = sum(len(days[k]['events']) for k in order)
n_unver_primary = sum(1 for k in order if days[k]['events'] and next(e for e in days[k]['events'] if e['id'] == days[k]['primaryId']).get('verdict') in ('unverifiable', 'not_checked'))

# ---- markdown ----
md_intro = []
md_intro.append("# Rumeli'de Tarihte Bugün")
md_intro.append("")
md_intro.append("**560 Yıl Rumeli · 4 Kasım 2026 – 3 Kasım 2027 · Yılın her günü**")
md_intro.append("")
md_intro.append("Bu takvim yılın her günü için Osmanlı Rumelisi'nden ve Rumeli Türklerinin tarihinden olaylar veriyor. "
          "Her günün ★ ile işaretli ilk satırı **günün ana olayı**. Altındakiler aynı güne ait yedek olaylar: ana olayı geçen yıl paylaştıysan ya da başka bir açı istersen onları kullan.")
md_intro.append("")
md_intro.append(f"**Özet:** {n_days} gün, {n_events} olay. Ana olayı 1352–1912 çerçevesinden olan gün sayısı: {n_core_primary}. "
          f"Doğrulanmış olay bulunamayan gün: {n_empty}. Ana olayı ikinci kontrolde bağımsız kaynakla teyit edilemeyen gün: {n_unver_primary}.")
md_intro.append("")
md_intro.append("## Nasıl okunur")
md_intro.append("")
md_intro.append("- **Etiketsiz satırlar** sayfanın ana çerçevesinden, yani 1352–1912 arası Osmanlı Rumelisi'nden.")
md_intro.append("- **[Kişi]** Rumeli'de doğmuş ya da Rumeli'yle özdeşleşmiş birinin doğum veya ölüm günü.")
md_intro.append("- **[1912 sonrası]** Balkan Savaşları'ndan sonra Rumeli Türklerinin yaşadıkları: göçler, mübadele, Batı Trakya, Bulgaristan, Makedonya, Kosova Türkleri. Çerçevenin dışında ama kitlenin duygusal takvimi.")
md_intro.append("- **[1352 öncesi]** ve **[Gelenek]** Balkanlardaki erken Türk varlığı ve sabit günlü gelenekler.")
md_intro.append("- **⚠** Gün kaynaklara göre değişiyor ya da kesin değil. Notu oku; paylaşırken \"bazı kaynaklara göre\" demek iyi olur.")
md_intro.append("- **Not:** Takvim çevirisi, kuşatmanın hangi günü gibi açıklamalar.")
md_intro.append("- **(kontrol edilemedi)** İkinci kontrolde bağımsız bir kaynakla teyit edilemedi. Paylaşmadan önce kaynağa kendin bak.")
md_intro.append("")
md_intro.append("## Tarih kuralı")
md_intro.append("")
md_intro.append("- 1582'den önceki olaylarda tarih yazımında yerleşik tarih kullanıldı (Jülyen takvimi; ör. Kosova 15 Haziran 1389). Çevrilmedi.")
md_intro.append("- 1582'den sonraki olaylar Miladi (Gregoryen) tarihle verildi. Bulgar, Sırp, Rus ve Yunan kaynaklarındaki eski takvim tarihleri Gregoryen'e çevrildi (1800'lerde +12, 1900–1923'te +13 gün).")
md_intro.append("- Osmanlı belgelerindeki Rumi ve Hicri tarihler için güvenilir kaynaktaki Miladi karşılığı alındı.")
md_intro.append("")
md_intro.append("## Kullanmadan önce")
md_intro.append("")
md_intro.append("- Her olayın yanında kaynağı var. Gönderiyi hazırlarken kaynağı bir kez aç: hem doğruluğu görürsün hem de açıklamaya kaynak yazabilirsin.")
md_intro.append("- Takvim yılın bütün günlerini kapsıyor. 4 Kasım 2027'den sonra aynı günler yeniden geçerli; ertesi yıl yedek olayları kullanabilirsin.")
md_intro.append("- Hassas günlerde (savaş, katliam, göç) ortak hafıza dilini koru; büyüme rehberindeki \"Yapma listesi\" bölümüne bak.")
md_intro.append("")

ASCII = {'Ocak': 'ocak', 'Şubat': 'subat', 'Mart': 'mart', 'Nisan': 'nisan', 'Mayıs': 'mayis', 'Haziran': 'haziran',
         'Temmuz': 'temmuz', 'Ağustos': 'agustos', 'Eylül': 'eylul', 'Ekim': 'ekim', 'Kasım': 'kasim', 'Aralık': 'aralik'}
months = []  # (title, filename, lines)
cur_month = None
for k in order:
    dt = real_date(k)
    mkey = (dt.year, dt.month)
    if mkey != cur_month:
        cur_month = mkey
        title = f"{AY[dt.month-1]} {dt.year}"
        fname = f"{len(months)+1:02d}_{ASCII[AY[dt.month-1]]}_{dt.year}.md"
        lines = [f"# {title} · Rumeli'de Tarihte Bugün", "",
                 "★ günün ana olayı · ⚠ gün tartışmalı · [Kişi] doğum/ölüm · [1912 sonrası] Balkan Türkleri · _(kontrol edilemedi)_ paylaşmadan önce kaynağa bak. "
                 "Okuma rehberi ve tarih kuralı: [README](../README.md).", ""]
        months.append((title, fname, lines))
    md = months[-1][2]
    t = days[k]
    md.append(f"### {dt.day} {AY[dt.month-1]} {dt.year} · {GUN[dt.weekday()]}")
    md.append("")
    if not t['events']:
        note = clean(t.get('gap_note')) or 'Seri içeriklerinden birini (Eski Adıyla, Rumeli Sözlüğü, Dedemin Bavulu) kullan.'
        md.append(f"- Bu gün için doğrulanmış bir olay bulunamadı. Öneri: {note}")
        md.append("")
        continue
    for e in sorted_events(t):
        is_p = e['id'] == t['primaryId']
        label = SCOPE_LABEL.get(e.get('scope'), '')
        bits = []
        head = f"{clean(str(e.get('year')))} · {clean(e.get('title_tr')).rstrip('.')}."
        line = ("★ **" + head + "**") if is_p else head
        line += " " + clean(e.get('detail_tr'))
        if label:
            line += f" **[{label}]**"
        cn = clean(e.get('calendar_note'))
        if needs_warning(e):
            line += f" ⚠ _{cn}_" if cn else " ⚠ _Gün kaynaklara göre değişebilir._"
        elif cn:
            line += f" _Not: {cn}_"
        if e.get('verdict') in ('unverifiable', 'not_checked'):
            line += " _(kontrol edilemedi)_"
        if clean(e.get('editor_flag')):
            line += f" _Editör notu: {clean(e.get('editor_flag'))}_"
        srcs = good_sources(e)[:2]
        if srcs:
            line += " · " + ", ".join(f"[kaynak{'' if i == 0 else ' ' + str(i+1)}]({md_url(s)})" for i, s in enumerate(srcs))
        md.append("- " + line)
        if is_p and clean(e.get('content_idea')):
            md.append(f"  - _İçerik fikri:_ {clean(e.get('content_idea'))}")
    md.append("")

os.makedirs(os.path.join(out_dir, 'aylar'), exist_ok=True)
for title, fname, lines in months:
    open(os.path.join(out_dir, 'aylar', fname), 'w').write('\n'.join(lines) + '\n')
md_intro.append("## Aylar")
md_intro.append("")
for title, fname, lines in months:
    md_intro.append(f"- [{title}](aylar/{fname})")
md_intro.append("")
md_intro.append("## Diğer dosyalar")
md_intro.append("")
md_intro.append("- [Kısa takvim](rumeli_tarihte_bugun_kisa.md): her gün için tek satır, sadece ana olay.")
md_intro.append("- `rumeli_tarihte_bugun.xlsx`: bütün olaylar tek tabloda; tarih, kapsam ya da ana olay sütununa göre süzebilirsin.")
md_intro.append("- `rumeli_tarihte_bugun.csv`: aynı tablo, noktalı virgülle ayrılmış, UTF-8. Türkçe Excel'de doğrudan açılır.")
md_intro.append("- `kaynak/`: takvimi üreten betikler (Vikipedi gün sayfalarını indirme, birleştirme, dosyaları oluşturma).")
md_intro.append("")
open(os.path.join(out_dir, 'README.md'), 'w').write('\n'.join(md_intro))

# ---- rows for csv / xlsx ----
header = ['Tarih', 'Gün', 'Ana olay', 'Yıl', 'Başlık', 'Ayrıntı', 'Kapsam', 'Takvim notu', 'Gün güveni',
          'İkinci kontrol', 'Editör notu', 'İçerik fikri', 'Kaynak 1', 'Kaynak 2']
CONF_TR = {'high': 'yüksek', 'medium': 'orta', 'low': 'düşük'}
rows = []
for k in order:
    dt = real_date(k)
    t = days[k]
    if not t['events']:
        rows.append([dt.isoformat(), GUN[dt.weekday()], 'boş gün', '', '', clean(t.get('gap_note')), '', '', '', '', '', '', '', ''])
        continue
    for e in sorted_events(t):
        s = good_sources(e)
        rows.append([dt.isoformat(), GUN[dt.weekday()], 'evet' if e['id'] == t['primaryId'] else '',
                     clean(str(e.get('year'))), clean(e.get('title_tr')), clean(e.get('detail_tr')),
                     SCOPE_CSV.get(e.get('scope'), ''), clean(e.get('calendar_note')),
                     CONF_TR.get(e.get('date_confidence'), ''), VERDICT_TR.get(e.get('verdict'), e.get('verdict', '')),
                     clean(e.get('editor_flag')), clean(e.get('content_idea')) if e['id'] == t['primaryId'] else '',
                     s[0] if s else '', s[1] if len(s) > 1 else ''])

with open(os.path.join(out_dir, 'rumeli_tarihte_bugun.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(header)
    w.writerows(rows)

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = 'Takvim'
    ws.append(header)
    for r in rows:
        ws.append(r)
    widths = [12, 11, 9, 14, 40, 70, 14, 40, 10, 22, 40, 50, 40, 40]
    for i, wd in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wd
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill('solid', fgColor='DDD5C4')
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
        if row[2].value == 'evet':
            for c in row:
                c.font = Font(bold=True)
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions
    wb.save(os.path.join(out_dir, 'rumeli_tarihte_bugun.xlsx'))
except Exception as ex:
    print('xlsx skipped:', ex)

print(json.dumps(dict(days=n_days, events=n_events, core_primary=n_core_primary, empty=n_empty,
                      unverified_primary=n_unver_primary, actions_applied=len([a for a in applied if not a[0].startswith('SKIP')]),
                      actions_skipped=len([a for a in applied if a[0].startswith('SKIP')])), ensure_ascii=False))

# ---- short version: one line per day ----
short = ["# Rumeli'de Tarihte Bugün: kısa takvim", "",
         "**4 Kasım 2026 – 3 Kasım 2027 · her gün için ana olay**", "",
         "Her günün yalnızca ana olayı. Ayrıntı, kaynak, yedek olaylar ve içerik fikirleri için [aylık dosyalara](README.md#aylar) bak. "
         "⚠ = gün tartışmalı, notuna bak. Etiketler: [Kişi], [1912 sonrası], [1352 öncesi], [Gelenek].", ""]
cur = None
for k in order:
    dt = real_date(k)
    if (dt.year, dt.month) != cur:
        cur = (dt.year, dt.month)
        short += ["", f"## {AY[dt.month-1]} {dt.year}", "", "| Tarih | Gün | Yıl | Ana olay |", "|---|---|---|---|"]
    t = days[k]
    if not t['events']:
        short.append(f"| {dt.day} {AY[dt.month-1]} | {GUN[dt.weekday()]} | | _Doğrulanmış olay yok_ |")
        continue
    e = next(x for x in t['events'] if x['id'] == t['primaryId'])
    lab = SCOPE_LABEL.get(e.get('scope'), '')
    txt = clean(e.get('title_tr')).rstrip('.').replace('|', '/')
    if lab:
        txt += f" [{lab}]"
    if needs_warning(e):
        txt += " ⚠"
    short.append(f"| {dt.day} {AY[dt.month-1]} | {GUN[dt.weekday()]} | {clean(str(e.get('year'))).replace('|','/')} | {txt} |")
open(os.path.join(out_dir, 'rumeli_tarihte_bugun_kisa.md'), 'w').write('\n'.join(short) + '\n')
