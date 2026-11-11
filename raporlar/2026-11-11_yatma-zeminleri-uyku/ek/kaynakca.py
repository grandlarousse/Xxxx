#!/usr/bin/env python3
"""RAPOR.md içindeki <!--KAYNAKLAR--> yer tutucusunu PubMed künyeleriyle doldurur."""
import os, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, '..', 'RAPOR.md')
G = [('Evrim ve antropoloji', '27470330 22555951 26662946 32792402 22158814 26480842 28063234 28701566 36945298 39999887 11124203'),
     ('Fizyoloji, ısı, pozisyon', '10938176 24136970 26245965 38409133 33647762 39191505 29138608'),
     ('Yatak sertliği ve sert zemin', '14630439 18379395 29073401 34878594 42432412 11059462 21294014 40365263 38803581 17597575 37020853 41052041 26851461 16076735'),
     ('Kamp, sallanma, ilk gece, topraklanma, uzay', '23910656 28162893 37749123 30686735 42268039 32061115 32855111 34998093 27112296 2711096 15650465 22291721 35327058 25127232'),
     ('Koltuk ve kanepe', '29889574 36231565 37496454 18691289 27540486'),
     ('Özel gruplar', '25311597 19826174 35726558 31193832 20398112 40569873 34398473 27049597 33895703 32229033 33468060 36233488')]
ids = [p for _, s in G for p in s.split()]
xml = urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', urllib.parse.urlencode({'db': 'pubmed', 'id': ','.join(ids), 'retmode': 'xml'}).encode(), timeout=90).read()
M = {}
for a in ET.fromstring(xml).iter('PubmedArticle'):
    au = a.findtext('.//AuthorList/Author/LastName') or '?'
    n = len(a.findall('.//AuthorList/Author'))
    yr = a.findtext('.//JournalIssue/PubDate/Year') or (a.findtext('.//JournalIssue/PubDate/MedlineDate') or '?')[:4]
    t = ''.join(a.find('.//ArticleTitle').itertext()).rstrip('.')
    M[a.findtext('.//PMID')] = f"{au}{' ve ark.' if n > 1 else ''} {yr}. {t}. *{a.findtext('.//Journal/ISOAbbreviation')}*."
out = []
for h, s in G:
    out.append(f'**{h}**\n')
    out += [f"- {M[p]} https://pubmed.ncbi.nlm.nih.gov/{p}/" for p in s.split() if p in M]
    out.append('')
eksik = [p for p in ids if p not in M]
txt = open(R, encoding='utf-8').read()
assert '<!--KAYNAKLAR-->' in txt
open(R, 'w', encoding='utf-8').write(txt.replace('<!--KAYNAKLAR-->', '\n'.join(out).rstrip()))
print('kaynak sayısı', len(ids) - len(eksik), 'eksik', eksik)
