#!/usr/bin/env python3
"""Defter satırlarını toplu doğrular: her PMID için PubMed kaydını çeker,
alıntının özet/başlıkta birebir geçip geçmediğine bakar. Çıktı: betik_dogrulama.tsv"""
import re, sys, glob, os, urllib.request, urllib.parse, xml.etree.ElementTree as ET, html, unicodedata
D = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(D, 'u*.md'))):
    for ln in open(f, encoding='utf-8'):
        m = re.search(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)', ln)
        if not m or ln.count('|') < 3: continue
        p = [x.strip() for x in ln.split('|')]
        rows.append(dict(src=os.path.basename(f)[:2], pmid=m.group(1), claim=p[0], quote=html.unescape(p[2])))
pmids = sorted({r['pmid'] for r in rows})
def norm(s):
    s = unicodedata.normalize('NFKC', html.unescape(s)).lower()
    s = s.replace('−', '-').replace('–', '-').replace('—', '-').replace('’', "'")
    return re.sub(r'[^a-z0-9%.<>=±-]+', ' ', s).strip()
meta = {}
for i in range(0, len(pmids), 80):
    data = urllib.parse.urlencode({'db': 'pubmed', 'id': ','.join(pmids[i:i+80]), 'retmode': 'xml'}).encode()
    xml = urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', data, timeout=60).read()
    for a in ET.fromstring(xml).iter('PubmedArticle'):
        pm = a.findtext('.//PMID')
        title = ''.join(a.find('.//ArticleTitle').itertext()) if a.find('.//ArticleTitle') is not None else ''
        ab = ' '.join(''.join(x.itertext()) for x in a.iter('AbstractText'))
        au = a.findtext('.//AuthorList/Author/LastName') or '?'
        nau = len(a.findall('.//AuthorList/Author'))
        yr = a.findtext('.//JournalIssue/PubDate/Year') or (a.findtext('.//JournalIssue/PubDate/MedlineDate') or '?')[:4]
        j = a.findtext('.//Journal/ISOAbbreviation') or ''
        pt = ';'.join(x.text for x in a.iter('PublicationType') if x.text and 'Research Support' not in x.text)
        meta[pm] = dict(title=title, ab=ab, au=au + (' ve ark.' if nau > 1 else ''), yr=yr, j=j, pt=pt)
out = ['kaynak\tPMID\tyazar\tyıl\tdergi\ttür\talıntı_eşleşme\tiddia\tbaşlık']
bad = []
for r in rows:
    m = meta.get(r['pmid'])
    if not m:
        out.append(f"{r['src']}\t{r['pmid']}\tKAYIT YOK\t\t\t\tYOK\t{r['claim']}\t"); bad.append(r); continue
    hay = norm(m['title'] + ' ' + m['ab'])
    segs = re.findall(r'"([^"]+)"', r['quote'])
    frags = [norm(x) for s in segs for x in re.split(r'\.\.\.|…|\[[^\]]*\]', s)]
    frags = [x.strip(' .') for x in frags if len(x.strip(' .')) >= 8]
    if not frags: st = 'alıntı yok'
    else:
        ok = sum(1 for x in frags if x in hay)
        st = 'TAM' if ok == len(frags) else (f'KISMİ {ok}/{len(frags)}' if ok else 'EŞLEŞMEDİ')
    if st not in ('TAM',): bad.append(dict(r, st=st, noab=not m['ab']))
    out.append('\t'.join([r['src'], r['pmid'], m['au'], m['yr'], m['j'], m['pt'][:40], st, r['claim'][:90], m['title'][:110]]))
open(os.path.join(D, 'betik_dogrulama.tsv'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'satır={len(rows)} benzersiz PMID={len(pmids)} kayıt bulunan={len(meta)}')
from collections import Counter
print(Counter(l.split('\t')[6] for l in out[1:]))
print('--- TAM olmayanlar')
for b in bad: print(b['src'], b['pmid'], b.get('st'), 'ÖZET YOK' if b.get('noab') else '', '|', b['claim'][:70], '|', b['quote'][:110])
print('--- PMID künyeleri')
for pm in pmids:
    m = meta.get(pm)
    if m: print(pm, '|', m['au'], m['yr'], m['j'], '|', m['title'][:95])
