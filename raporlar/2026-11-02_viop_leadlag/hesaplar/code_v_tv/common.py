"""v_tv: TradingView kod denetimi — ortak yardımcılar (bağımsız; ll.py / code_tv import EDİLMEZ)."""
import re, glob, os
import pandas as pd

ROOT = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
OUT = f'{ROOT}/out'
CODE = f'{OUT}/code_v_tv'

CHINA_PREFIX = ('SSE', 'SZSE', 'SHFE', 'DCE', 'ZCE', 'CFFEX', 'INE', 'GFEX')
# Çin borsası öneki: TV önekleri büyük harf + ':'; 'SIDX'/'FUT'/'SINA' iç (veri kaynağı) etiketleri de TV kodu değildir
PSEUDO_PREFIX = ('SIDX', 'FUT', 'SINA')

VIOP47 = ("AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN "
          "GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN "
          "TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK").split()

# TV kodu ayıklayıcı: ÖNEK:SEMBOL ; sembolde . ! / _ & - olabilir (LSE:BA., BMV:ALPEK/A, BIST:XU030D1!)
TOK = re.compile(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9_]{1,15}):([A-Za-z0-9_.!/&<>]+)')


def tv_tokens(s):
    """Serbest metinden TV kodlarını çıkar. Dönüş: [(kod, soru_isareti_var_mi)]"""
    if not isinstance(s, str):
        return []
    out = []
    for m in TOK.finditer(s):
        pre, sym = m.group(1), m.group(2)
        end = m.end()
        q = end < len(s) and s[end:end + 2].strip().startswith('?')
        # sondaki noktalama: LSE iki harfli kodlarda '.' meşru (LSE:BA.) -> yalnızca LSE dışında sondaki '.'/',' sil
        sym = sym.rstrip(',;')
        if pre != 'LSE':
            sym = sym.rstrip('.')
        if sym.endswith('/'):
            sym = sym.rstrip('/')
        # formül parçası: NYMEX:HO1!*42 -> TOK '*'da durur; '/' formül bölmesi: 'NYMEX:HO1!/ICEEUR' gibi
        if '/' in sym and pre != 'BMV':
            sym = sym.split('/')[0]
        out.append((f'{pre}:{sym}', q))
    return out


def load_tvmap():
    t = pd.read_csv(f'{OUT}/tv_map.csv', dtype=str)
    ymap, byc = {}, {}
    for _, r in t.iterrows():
        alts = [c for c, _ in tv_tokens(r.tv_alt)] if isinstance(r.tv_alt, str) else []
        d = dict(yahoo=r.yahoo, name=r['name'], best=r.tv_best if isinstance(r.tv_best, str) else '',
                 alts=alts, status=r.status, notes=r.notes if isinstance(r.notes, str) else '',
                 url=r.evidence_url if isinstance(r.evidence_url, str) else '')
        if isinstance(r.yahoo, str):
            ymap[r.yahoo] = d
        if d['best']:
            byc.setdefault(d['best'], []).append(d)
    return t, ymap, byc


def load_catalog():
    c = pd.read_csv(f'{ROOT}/data/catalog.csv', dtype=str)
    return c.set_index('sym')


def load_findings():
    rows = []
    for f in sorted(glob.glob(f'{OUT}/f_*.csv')):
        d = pd.read_csv(f, dtype=str)
        d['src'] = os.path.basename(f)[2:-4]
        rows.append(d)
    return pd.concat(rows, ignore_index=True)
