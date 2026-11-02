"""cache.jsonl + candidates.json -> out/tv_map.csv"""
import csv, json, os, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__))
OUTCSV = os.path.join(D, '..', 'tv_map.csv')
rows = json.load(open(os.path.join(D, 'candidates.json'), encoding='utf8'))
cache = {}
for cf in ('cache.jsonl', 'cache_b.jsonl', 'cache_manual.jsonl'):
    p = os.path.join(D, cf)
    if not os.path.exists(p):
        continue
    for l in open(p, encoding='utf8'):
        try:
            r = json.loads(l)
            if r['tv'] in cache and cache[r['tv']].get('http') == '200' and r.get('http') != '200':
                continue
            cache[r['tv']] = r
        except Exception:
            pass

DELAY = {  # kaynak: https://www.tradingview.com/data-coverage/ (01.11.2026 okundu; fiyatlar değişebilir)
 'BIST': 'BIST: ücretsiz 15 dk gecikmeli; gerçek zamanlı ücretli BIST paketi',
 'CME_MINI': 'CME grubu: ücretsiz 10 dk gecikmeli; gerçek zamanlı ücretli', 'CME': 'CME grubu: 10 dk gecikmeli; gerçek zamanlı ücretli',
 'CBOT': 'CME grubu: 10 dk gecikmeli; gerçek zamanlı ücretli', 'CBOT_MINI': 'CME grubu: 10 dk gecikmeli; gerçek zamanlı ücretli',
 'COMEX': 'CME grubu: 10 dk gecikmeli; gerçek zamanlı ücretli', 'NYMEX': 'CME grubu: 10 dk gecikmeli; gerçek zamanlı ücretli',
 'ICEUS': 'ICE US: 10 dk gecikmeli; gerçek zamanlı pahalı paket', 'ICEEUR': 'ICE Europe: 10 dk gecikmeli; gerçek zamanlı pahalı paket',
 'ICEENDEX': 'ICE Endex: 10 dk gecikmeli; gerçek zamanlı pahalı paket',
 'NYSE': 'ABD: ücretsiz Cboe One üzerinden sınırlı gerçek zamanlı', 'NASDAQ': 'ABD: ücretsiz Cboe One üzerinden sınırlı gerçek zamanlı',
 'AMEX': 'ABD: ücretsiz Cboe One üzerinden sınırlı gerçek zamanlı', 'CBOE': 'Cboe: hisse/ETF ücretsiz gerçek zamanlı; Cboe endeksleri (VIX vb.) 15 dk gecikmeli',
 'OTC': 'OTC: 15 dk gecikmeli', 'XETR': '15 dk gecikmeli', 'EURONEXT': '15 dk gecikmeli', 'LSE': '15 dk gecikmeli; fiyat GBX (peni)',
 'SIX': '15 dk gecikmeli', 'MIL': '15 dk gecikmeli', 'BME': '15 dk gecikmeli', 'OMXSTO': '15 dk gecikmeli', 'OMXHEX': '15 dk gecikmeli',
 'OMXCOP': '15 dk gecikmeli', 'OSL': '15 dk gecikmeli', 'VIE': '15 dk gecikmeli', 'GPW': '15 dk gecikmeli', 'BET': '15 dk gecikmeli',
 'ATHEX': '15 dk gecikmeli', 'PSECZ': 'gecikmeli', 'TSE': '20 dk gecikmeli', 'KRX': '20 dk gecikmeli', 'TWSE': '15 dk gecikmeli',
 'NSE': '15 dk gecikmeli', 'BSE': 'gecikmeli', 'SET': '15 dk gecikmeli', 'ASX': '20 dk gecikmeli', 'TADAWUL': '15 dk gecikmeli',
 'BMV': '20 dk gecikmeli', 'BMFBOVESPA': '15 dk gecikmeli', 'JSE': '15 dk gecikmeli', 'TASE': '15 dk gecikmeli', 'TSX': '15 dk gecikmeli',
 'IDX': '10 dk gecikmeli', 'HKEX': '15 dk gecikmeli', 'SGX': '10 dk gecikmeli (SGX vadeli gerçek zamanlı pahalı)',
 'SP': 'S&P endeksleri 10 dk gecikmeli', 'DJ': 'Dow Jones endeksleri 10 dk gecikmeli', 'TVC': 'TVC = TradingView kendi türetilmiş/CFD akışı (ücretsiz)',
 'FX': 'FXCM akışı (ücretsiz)', 'FX_IDC': 'ICE Data FX akışı (ücretsiz)', 'OANDA': 'OANDA (ücretsiz)', 'SAXO': 'Saxo (ücretsiz)',
 'EUREX': '15 dk gecikmeli', 'LME': 'gün sonu (gerçek zamanlı ücretli)', 'BITSTAMP': 'kripto, ücretsiz gerçek zamanlı',
 'COINBASE': 'kripto, ücretsiz gerçek zamanlı', 'KRAKEN': 'kripto, ücretsiz', 'RUS': 'Rusya borsası verisi — yaptırımlar nedeniyle bayat/sınırlı olabilir',
}
STOP = set('''inc corp corporation co company ltd limited sa s a ag plc group holding holdings the nv n v se spa s p a oyj publ ab asa as a s
class b tbk pt public de of and bank banco sab cv c v kgaa aktiengesellschaft societe anonyme anonim sirketi sanayi ve ticaret tas t a s
international industries industry etf fund trust shares ishares msci index spdr state street select sector vanguard'''.split())
def toks(s):
    s = (s or '').replace('Ø', 'O').replace('ø', 'o')
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return {t for t in s.split() if len(t) > 1 and t not in STOP}

def ok(r):
    return r is not None and r.get('http') == '200' and bool(r.get('info'))
def code_of(c, r):
    """Kullanıcının yazması gereken kod: yönlendirme varsa talep edilen kod (sembol mevcut), yoksa sayfanın çözdüğü kod."""
    res = r['info'].get('resolved_symbol') or c
    redirected = (r.get('eff', '').split(' ')[-1] not in ('', '0'))
    if redirected:
        return c, (res if res != c else None), True
    return res, (c if res != c else None), False

def prefix(code):
    return code.split(':')[0] if ':' in code else ''

out = []
for d in rows:
    y, nm, g = d['yahoo'], d['name'], d['group']
    notes = []
    best = alt = ''; status = ''; ev = ''
    verified = []  # (code, url, info, note)
    for c in d['cands'] + d['alt_cands']:
        r = cache.get(c)
        if ok(r):
            code, other, redir = code_of(c, r)
            nt = ''
            if redir and other:
                nt = f'{c} sayfası kanonik sayfaya yönleniyor (orada {other} gösteriliyor) — {c} mevcut'
            elif other:
                nt = f'{other} yazılınca TradingView {code} olarak çözüyor'
            if code not in [v[0] for v in verified]:
                verified.append((code, r['url'], r['info'], nt, c in d['cands']))
    if d['china']:
        status = 'CHINA_BLOCKED'
        alt = ' | '.join(v[0] for v in verified) or d.get('china_alt', '') or 'AMEX:ASHR | CBOE:CNYA | AMEX:FXI (genel A-hisse vekili; şirkete özgü ADR/ETF için cin ajanı)'
        notes.append('Çin borsası (SSE/SZSE) kullanıcıda açılmıyor — kod verilmedi; ABD ETF alternatifi (cin ajanı veriyle test ediyor)')
        ev = verified[0][1] if verified else ''
    else:
        prim = [v for v in verified if v[4]]
        if prim:
            b = prim[0]; best, ev = b[0], b[1]; status = 'VERIFIED_PAGE'
            if b[3]: notes.append(b[3])
            # isim kontrolü (hisse/ETF)
            if d['type'] in ('EQUITY', 'ETF', 'MUTUALFUND'):
                ti = b[2]
                tvn = ' '.join(str(ti.get(k) or '') for k in ('description', 'local_description', 'short_description'))
                a_, b_ = toks(nm), toks(tvn)
                if not a_ or not b_:
                    a_ = set(re.sub(r'[^a-z0-9 ]', ' ', nm.lower()).split()); b_ = set(re.sub(r'[^a-z0-9 ]', ' ', tvn.lower()).split())
                if not (a_ & b_):
                    status = 'UNCERTAIN'; notes.append(f'İSİM UYUŞMAZLIĞI? TV açıklaması: "{ti.get("description")}" — elle kontrol et')
                else:
                    notes.append(f'TV: {ti.get("description")}' + (f' ({ti.get("isin_displayed")})' if ti.get('isin_displayed') else ''))
            else:
                notes.append(f'TV: {b[2].get("description")}')
            alts = [v[0] for v in verified if v[0] != best]
            alt = ' | '.join(alts)
        else:
            tried = [c for c in d['cands'] if c in cache]
            best = d['cands'][0] if d['cands'] else ''
            if tried:
                status = 'UNCERTAIN'; notes.append('aday sayfa(lar) 404: ' + ', '.join(tried))
                alts = [v[0] for v in verified]
                alt = ' | '.join(alts)
                if alts:
                    best, alt = alts[0], ' | '.join(alts[1:]); status = 'VERIFIED_PAGE'
                    ev = verified[0][1]; notes.append('birincil aday yok; doğrulanmış alternatif kullanıldı')
            else:
                status = 'CONVENTION'; notes.append('mekanik kural; sayfa okunmadı')
        if d['hk']:
            notes.append('HKEX: kullanıcıda açılmayabilir (belirsiz) — alternatif: ' + (alt or 'yok'))
    p = prefix(best)
    if '1!' in best or re.search(r'[FGHJKMNQUVXZ]20\d\d$', best):
        notes.append('sürekli kontrat 1! = ön ay; vade dönüşünde (roll) fiyat sıçraması olur')
    if p in DELAY: notes.append(DELAY[p])
    if p == 'BIST' and best.endswith('1!'):
        notes.append('VİOP vadelisi: 15 dk gecikmeli; gerçek zamanlı BIST vadeli paketi ücretli')
    out.append({'yahoo': y, 'name': nm, 'tv_best': best, 'tv_alt': alt, 'status': status, 'evidence_url': ev, 'notes': '; '.join(notes)})

with open(OUTCSV, 'w', newline='', encoding='utf8') as f:
    w = csv.DictWriter(f, fieldnames=['yahoo', 'name', 'tv_best', 'tv_alt', 'status', 'evidence_url', 'notes'])
    w.writeheader(); w.writerows(out)
import collections
print(collections.Counter(o['status'] for o in out))
