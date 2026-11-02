"""v_tv denetim: f_*.csv tv_ticker <-> tv_map.csv karşılaştırması + tv_final.csv üretimi.
Çalıştırma: nice -n 10 python3 audit.py [--fetchlist]   (önce fetch.py ile doğrulama önbelleği doldurulur)"""
import sys, re, json
import pandas as pd
from common import *
from drivers import atoms, YMAP, BYC, CAT, KNOWN
from special import special
sys.path.insert(0, CODE)
from fetch import load_cache

FC = load_cache()          # bağımsız sayfa doğrulama önbelleği (curl)
S40 = pd.read_csv(f'{CODE}/sample40_webfetch.csv', dtype=str)
WF = set(S40.loc[S40.sonuc == 'TEYIT', 'tv_best'])   # WebFetch ile teyit edilen 40 kod

ALLBEST = {d['best'] for d in YMAP.values() if d['best']} | set(BYC)
ALLALT = {a for d in YMAP.values() for a in d['alts']}
VERIFIED = {d['best'] for d in YMAP.values() if d['status'] == 'VERIFIED_PAGE'} | \
           {c for c, L in BYC.items() if any(x['status'] == 'VERIFIED_PAGE' for x in L)}


REDIR_TGT = set()
for _r in FC.values():
    _m = re.match(r'^https://www.tradingview.com/symbols/([A-Z0-9_]+)-([^/?]+)/$', _r.get('eff') or '')
    if _r.get('http') == '200' and _m:
        REDIR_TGT.add(f'{_m.group(1)}:{_m.group(2)}')


def page_ok(code):
    """Bağımsız doğrulama: 200 + pro_symbol/resolved == kod (ya da kanonik yönlendirme)."""
    r = FC.get(code)
    if not r:
        return None
    if r.get('http') != '200':
        return False
    ps = (r.get('pro_symbol') or r.get('resolved') or '')
    return True if ps else None


def page_desc(code):
    r = FC.get(code) or {}
    return r.get('short_desc') or r.get('desc') or ''


def page_resolved(code):
    r = FC.get(code) or {}
    return r.get('pro_symbol') or r.get('resolved') or ''


# ---------- Çin alternatifleri ----------
CIN = pd.read_csv(f'{OUT}/cin_alternatifler.csv', dtype={'orijinal': str})
CIN['alt_clean'] = CIN.alternatif_tv.str.replace('?', '', regex=False).str.replace(r'\s*\(.*\)', '', regex=True).str.strip()
CIN_KEY = {'000001.SS': 'SIDX:sh000001', '000016.SS': 'SIDX:sh000016', '000300.SS': 'SIDX:sh000300',
           '399001.SZ': 'SIDX:sz399001', '399006.SZ': 'SIDX:sz399006'}


def cin_alts(key):
    """(en iyi açılabilir alternatif, ikinciler, HKEX alternatifi, not)"""
    d = CIN[CIN.orijinal == key]
    if d.empty:
        return None
    d = d.sort_values('corr_weekly', ascending=False)
    ok = d[~d.alt_clean.str.contains('HKEX|HSI:|Çin borsası', regex=True)]
    hk = d[d.alt_clean.str.contains('HKEX', regex=False)]
    best = ok.iloc[0] if len(ok) else None
    sec = list(ok.alt_clean.iloc[1:3]) if len(ok) > 1 else []
    note = ''
    if best is not None:
        note = f"cin_alternatifler: {best.alternatif_yahoo} haftalık r={best.corr_weekly:.2f} (3y {best.corr_weekly_3y:.2f}), güven {best.guven}"
    hkc = None
    if len(hk):
        h = hk.iloc[0]
        hkc = h.alt_clean
        note += f"; HK karşılığı {hkc} r={h.corr_weekly:.2f} (HKEX açılmayabilir)"
    od = str(d.orijinal_desc.iloc[0])
    return (best.alt_clean if best is not None else '', sec, hkc, note,
            (f"{od} (Çin) -> alternatif: {best.alternatif_desc}" if best is not None else od))


def is_china(code):
    return code.split(':')[0] in CHINA_PREFIX


# ---------- atomik sembol için beklenen kod ----------
def expected(y):
    """dict(kodu, alt[list], durum, not, aciklama)"""
    name = ''
    if y in YMAP:
        name = YMAP[y]['name'] or ''
    elif y in CAT.index:
        name = CAT.loc[y, 'name'] if isinstance(CAT.loc[y, 'name'], str) else ''
    if y == 'SIDX:USDCNH':
        return dict(kodu='FX:USDCNH', alt=['FX_IDC:USDCNH', 'FX_IDC:USDCNY'], durum='DOGRULANDI_V', aciklama='USD/CNH offshore yuan',
                    nt='Çin borsası değil; Sina USDCNH = FX:USDCNH (sayfa v_tv ile okundu)')
    if y.startswith(('FUT:', 'SIDX:')) or (y in YMAP and YMAP[y]['status'] == 'CHINA_BLOCKED') or y.endswith(('.SS', '.SZ')):
        key = CIN_KEY.get(y, y)
        ca = cin_alts(key)
        if ca and ca[0]:
            alts = ca[1] + ([ca[2]] if ca[2] else [])
            return dict(kodu=ca[0], alt=alts, durum='CIN_ENGELLI_ALT', aciklama=(name + ' -> alternatif') if name else ca[4],
                        nt='Çin borsası kodu VERİLMEZ (kullanıcıda açılmıyor); ' + ca[3])
        d = YMAP.get(y)
        alts = d['alts'] if d else ['AMEX:ASHR', 'CBOE:CNYA', 'AMEX:FXI']
        if y == '518880.SS':
            return dict(kodu='AMEX:GLD', alt=['COMEX:GC1!'], durum='CIN_ENGELLI_ALT', aciklama=name,
                        nt='Çin altın ETF; kod verilmez; altın vekili (test edilmedi, mekanik vekil)')
        return dict(kodu=alts[0], alt=alts[1:], durum='CIN_ENGELLI_ALT', aciklama=name,
                    nt='Çin borsası kodu VERİLMEZ; genel A-pay ETF vekili (şirkete özgü alternatif test edilmedi)')
    if y in YMAP:
        d = YMAP[y]
        st = d['status']
        kod = d['best']
        alts = list(d['alts'])
        nt = ''
        if kod.startswith('HKEX:'):
            key = y
            ca = cin_alts(key)
            extra = [ca[0]] if ca and ca[0] else []
            alts = [a for a in alts + extra if a]
            alts = list(dict.fromkeys(alts))
            return dict(kodu=kod, alt=alts, durum='HKEX_BELIRSIZ', aciklama=name,
                        nt='HKEX kullanıcıda açılmayabilir -> ABD/OTC alternatifi kullan' + ('; ' + ca[3] if ca else ''))
        if y.endswith('.IS') and y[:-3] in ('XU030', 'XLBNK', 'X10XB', 'XSD25'):
            alts = alts + [f'BIST:{y[:-3]}D1!']
        if st == 'VERIFIED_PAGE':
            du = 'DOGRULANDI'
            if kod in WF:
                du = 'DOGRULANDI_2KEZ'
                nt = 'WebFetch ile bağımsız teyit (v_tv örneklemi)'
            elif page_ok(kod) or kod in REDIR_TGT:
                du = 'DOGRULANDI_2KEZ'
                nt = 'sayfa bağımsız tekrar okundu (v_tv)'
            elif page_ok(kod) is False:
                du = 'CELISKI'
                nt = f"tv_map VERIFIED ama v_tv okumasında HTTP {FC[kod].get('http')}"
            return dict(kodu=kod, alt=alts, durum=du, aciklama=name, nt=nt)
        # UNCERTAIN
        po = page_ok(kod)
        return dict(kodu=kod, alt=alts, durum='BELIRSIZ' if not po else 'DOGRULANDI_V', aciklama=name,
                    nt=(d['notes'] or '')[:160] + ('' if po is None else f" | v_tv: HTTP {FC.get(kod, {}).get('http')}"))
    # katalogda olup tv_map'te olmayan (çoğu 2. tur BIST sembolleri)
    if y.endswith('.IS'):
        kod = 'BIST:' + y[:-3]
    else:
        kod = ''
    po = page_ok(kod) if kod else None
    du = 'DOGRULANDI_V' if po else ('YOK_404' if po is False else 'KURAL')
    nt = 'tv_map\'te yok; ' + ('v_tv sayfa okuması: ' + page_desc(kod) if po else ('v_tv: sayfa 404' if po is False else 'yalnız kural (BIST:<KOD>)'))
    return dict(kodu=kod, alt=[], durum=du, aciklama=name or (page_desc(kod) if kod else ''), nt=nt)


# ---------- f_* satır değerlendirmesi ----------
def evaluate():
    a = load_findings()
    recs = []
    for (drv, tv), g in a.groupby([a.driver_yahoo.fillna(''), a.tv_ticker.fillna('')], sort=False):
        toks = tv_tokens(tv)
        codes = [c for c, _ in toks]
        qmark = [c for c, q in toks if q]
        at, kind = atoms(drv)
        sp = special(drv) if kind in ('none', 'composite') else None
        stocks = set(g.stock.dropna())
        stk = {t for s in stocks for t in re.findall(r'[A-Z][A-Z0-9]{3,5}', str(s))}
        tgt = {f'BIST:{s}' for s in stk} | {f'BIST:{s}1!' for s in stk} | {f'BIST:{s}D1!' for s in stk}
        tgt_only = bool(codes) and all(c in tgt for c in codes) and not any(f'BIST:{x[:-3]}' in tgt for x in at if x.endswith('.IS'))
        issues, exp_codes = [], []
        china_tok = [c for c in codes if is_china(c)]
        pseudo = [c for c in codes if c.split(':')[0] in PSEUDO_PREFIX]
        if china_tok:
            issues.append('CIN_KODU:' + ','.join(china_tok))
        if pseudo:
            issues.append('SAHTE_ONEK:' + ','.join(pseudo))
        if at and not sp:
            for y in at:
                e = expected(y)
                exp_codes.append(e['kodu'])
                ok_set = {e['kodu']} | set(e['alt'])
                if y in YMAP and YMAP[y]['best']:
                    ok_set.add(YMAP[y]['best'])
                hit = [c for c in codes if c in ok_set]
                if e['durum'] == 'CIN_ENGELLI_ALT':
                    if not codes:
                        issues.append(f'EKSIK_CIN_ALT:{y}->{e["kodu"]}')
                    elif not hit:
                        given = [c for c in codes if not is_china(c)]
                        issues.append(f'CIN_ALT_FARKLI:{y}:{"/".join(given) or "-"}->{e["kodu"]}')
                    continue
                if e['durum'] == 'HKEX_BELIRSIZ':
                    if not any(c in e['alt'] or (c.split(':')[0] in ('OTC', 'NYSE', 'NASDAQ', 'AMEX', 'CBOE')) for c in codes):
                        issues.append(f'HKEX_ALT_YOK:{y}->{"/".join(e["alt"][:2])}')
                    continue
                if not codes:
                    issues.append(f'EKSIK:{y}->{e["kodu"]}')
                elif e['kodu'] and e['kodu'] in codes:
                    pass
                elif hit:
                    issues.append(f'ALT_KULLANILMIS:{y}:{"/".join(hit)}(tercih {e["kodu"]})')
                elif tgt_only:
                    issues.append(f'HEDEF_KODU:{y}:{"/".join(codes)}->{e["kodu"]}')
                elif len(at) > 1:
                    issues.append(f'EKSIK_BILESEN:{y}->{e["kodu"]}')
                else:
                    issues.append(f'UYUSMAZ:{y}:{"/".join(codes)}->{e["kodu"]}')
        elif sp:
            du, kod, alt, nt = sp
            kod_codes = [c for c, _ in tv_tokens(kod or '')]
            if kod_codes and du not in ('KENDI', 'TAKVIM', 'OLAY') and not any(c in codes for c in kod_codes):
                issues.append(f'OZEL_DUZELTME:{drv}:{"/".join(codes) or tv or "-"}->{kod}')
        unk = [c for c in codes if c not in ALLBEST and c not in ALLALT and not c.endswith('<KOD>') and not c.endswith('<KOD>1!')]
        q_ok = [c for c in qmark if c in VERIFIED]
        if q_ok:
            issues.append('GEREKSIZ_SORU:' + ','.join(q_ok))
        recs.append(dict(driver_yahoo=drv, tv_ticker_f=tv, n=len(g), src=','.join(sorted(set(g.src))), kind=kind,
                         atoms='|'.join(at), tv_codes='|'.join(codes), expected='|'.join(exp_codes),
                         unknown_codes='|'.join(unk), issues=' ; '.join(issues), target_only=tgt_only,
                         desc=str(g.driver_desc.iloc[0])[:120]))
    return pd.DataFrame(recs)


if __name__ == '__main__':
    ev = evaluate()
    ev.to_csv(f'{CODE}/eval_pairs.csv', index=False)
    print(len(ev), 'benzersiz (sürücü, tv_ticker) çifti')
    if '--fetchlist' in sys.argv:
        need = set()
        for s in ev.unknown_codes.dropna():
            need |= {c for c in s.split('|') if c}
        allat = set()
        for s in ev.atoms.dropna():
            allat |= {x for x in s.split('|') if x}
        for y in allat:
            e = expected(y)
            for c in [e['kodu']] + e['alt']:
                if c and c not in VERIFIED:
                    need.add(c)
        from special import SPECIAL
        for v in SPECIAL.values():
            for c, _ in tv_tokens(v[1] + ' ' + v[2]):
                if c not in VERIFIED:
                    need.add(c)
        need = {c for c in need if not is_china(c) and c.split(':')[0] not in PSEUDO_PREFIX and '<KOD>' not in c}
        need -= set(FC)
        open(f'{CODE}/codes_batch2.txt', 'w').write('\n'.join(sorted(need)) + '\n')
        print('doğrulanacak yeni kod:', len(need))
