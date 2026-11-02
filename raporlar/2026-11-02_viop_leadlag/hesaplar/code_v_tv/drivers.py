"""Sürücü dizgesini (driver_yahoo) atomik Yahoo sembollerine ayır."""
import re
from common import *

_, YMAP, BYC = load_tvmap()
CAT = load_catalog()
KNOWN = set(YMAP) | set(CAT.index)
BIST_BARE = {s[:-3] for s in KNOWN if s.endswith('.IS')}

# 'SINA:CU(roll-düz...)' -> cin_alternatifler 'FUT:CU' ; 'SINA:sh000300' -> 'SIDX:sh000300'
SINA = re.compile(r'SINA:([A-Za-z0-9]+)')

TOKRE = re.compile(r'[A-Za-z0-9^=.&\-]+')
# çok parçalı dizgede yanlış pozitif üretebilecek kısa/genel kelimeler
STOP = {'AG', 'AU', 'B', 'F', 'T', 'O', 'J', 'ON', 'TM', 'CA', 'KR', 'HL', 'DG', 'OI', 'BA', 'CF', 'TS', 'TX', 'KO',
        'GIS', 'MSCI', 'FTSE', 'NAV', 'EVENT', 'BT', 'CPI', 'TCMB', 'PPK', 'SPK', 'EW', 'IS', 'OOS', 'GAP', 'SCAN',
        'CRACK', 'GLOBAL', 'ES', 'EU', 'US', 'EM', 'TL', 'TR', 'USD', 'X', 'D', 'C', 'A', 'E', 'H', 'K', 'L', 'M', 'P',
        'S', 'U', 'V', 'Y', 'Z', 'R', 'G', 'N', 'W', 'I', 'Q', 'VIOP', 'BIST', 'HC', 'RB', 'I', 'AL', 'CU', 'BAP', 'BSK', 'DİBS', 'TLREF'}


def atoms(drv):
    """Dönüş: (atomlar listesi, tür) ; tür ∈ {exact, bare_bist, composite, sina, none}"""
    if not isinstance(drv, str) or not drv.strip():
        return [], 'none'
    s = drv.strip()
    if s in KNOWN:
        return [s], 'exact'
    if s in BIST_BARE:
        return [s + '.IS'], 'bare_bist'
    if re.fullmatch(r'X[A-Z0-9]{3,5}\.IS', s):   # katalogda olmayan BIST endeksi (XK050.IS, XSRDK.IS ...)
        return [s], 'exact'
    m = SINA.search(s)
    if m:
        k = m.group(1)
        return [('SIDX:' + k) if (k.startswith(('sh', 'sz')) or k == 'USDCNH') else ('FUT:' + k)], 'sina'
    # saf liste: 'CF+MOS+NTR' / 'A|B|C' / 'A, B' -> STOP filtresi uygulanmaz (CF, OI, MT gibi kısa kodlar meşru)
    if re.fullmatch(r'[A-Za-z0-9^=.\-]+(\s*[+|,]\s*[A-Za-z0-9^=.\-]+)+', s):
        parts = [p.strip() for p in re.split(r'[+|,]', s)]
        res = []
        for p in parts:
            if p in KNOWN:
                res.append(p)
            elif p in BIST_BARE:
                res.append(p + '.IS')
        if res:
            return list(dict.fromkeys(res)), 'composite'
    out = []
    for tk in TOKRE.findall(s):
        tk = tk.strip('.-')
        cands = [tk]
        if tk not in KNOWN and '-' in tk:
            cands = tk.split('-')
        for c in cands:
            if c in STOP or len(c) < 2:
                continue
            if c in KNOWN and (len(c) >= 3 or any(ch in c for ch in '.=^-')):
                out.append(c)
            elif c in BIST_BARE and len(c) >= 4:
                out.append(c + '.IS')
    seen = []
    for o in out:
        if o not in seen:
            seen.append(o)
    return seen, ('composite' if seen else 'none')


if __name__ == '__main__':
    import pandas as pd
    a = load_findings()
    u = a[['driver_yahoo']].drop_duplicates()
    u['atoms'] = u.driver_yahoo.map(lambda x: atoms(x)[0])
    u['kind'] = u.driver_yahoo.map(lambda x: atoms(x)[1])
    print(u.kind.value_counts())
    pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 110); pd.set_option('display.max_rows', 500)
    print(u[u.kind.isin(['composite', 'none'])].to_string())
