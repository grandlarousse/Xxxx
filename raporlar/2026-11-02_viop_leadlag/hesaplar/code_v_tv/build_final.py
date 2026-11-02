"""v_tv: tv_final.csv + uyuşmazlık listesi + f_* düzeltme eşlemesi üretir.
Çalıştırma: nice -n 10 python3 build_final.py"""
import re, sys, urllib.parse
import pandas as pd
from common import *
from drivers import atoms, YMAP, BYC, CAT
from special import special, SPECIAL
import audit
from audit import expected, evaluate, FC, WF, VERIFIED, is_china, cin_alts

# HKEX satırları için ABD/OTC alternatifi (sayfa okumasıyla doğrulananlar; HK_ALT_CHECK ile filtrelenir)
HK_ALT = {
    '0300.HK': ['AMEX:CHIQ', 'AMEX:FXI'], '0323.HK': ['OTC:MAANF', 'AMEX:SLX'], '0347.HK': ['OTC:ANGGF', 'AMEX:SLX'],
    '0358.HK': ['OTC:JIAXF', 'AMEX:COPX'], '0386.HK': ['OTC:SNPMF', 'AMEX:FXI'], '0700.HK': ['OTC:TCEHY', 'AMEX:KWEB'],
    '0857.HK': ['OTC:PCCYF', 'AMEX:FXI'], '0868.HK': ['OTC:XYIGF', 'AMEX:FXI'], '0914.HK': ['OTC:AHCHY', 'AMEX:FXI'],
    '0941.HK': ['AMEX:FXI', 'NASDAQ:MCHI'], '1070.HK': ['OTC:TCLHF', 'AMEX:CHIQ'], '1211.HK': ['OTC:BYDDY', 'OTC:BYDDF'],
    '1787.HK': ['AMEX:GDX', 'AMEX:GLD'], '1818.HK': ['OTC:ZHAOF', 'AMEX:GDX'], '1919.HK': ['OTC:CICOY', 'AMEX:BOAT'],
    '2899.HK': ['OTC:ZIJMF', 'OTC:ZIJMY'], '3606.HK': ['OTC:FYGGY', 'AMEX:FXI'], '3993.HK': ['OTC:CMCLF', 'AMEX:COPX'],
    '6690.HK': ['OTC:HSHCY', 'OTC:HRSHF'], '9863.HK': ['AMEX:KARS', 'AMEX:FXI'], '0001.HK': ['OTC:CKHUY'],
}
# sayfası var ama grafiği bayat/illikit olabilecek OTC gri piyasa kodları
OTC_GREY = {'OTC:JIAXF', 'OTC:XYIGF', 'OTC:ZHAOF', 'OTC:FYGGY', 'OTC:CMCLF', 'OTC:ZIJMF', 'OTC:PCCYF', 'OTC:SNPMF', 'OTC:BYDDF', 'OTC:MAANF', 'OTC:ANGGF', 'OTC:TCLHF', 'OTC:HRSHF'}

# sayfası 404 çıkan kodlar için doğrulanmış vekil
FALLBACK = {'COMEX:BUS1!': ['LME:SC1!', 'COMEX:HRC1!'], 'BIST:XAGTRY1!': ['BIST:XAGUSD1!'],
            'TVC:TR5YCDS': ['TVC:TR10Y', 'TVC:TR02Y']}

VIOP_IDX = [('XU030', 'BIST:XU030D1!', 'VİOP BIST 30 endeks vadelisi (sürekli ön ay; akşam seansı VAR)'),
            ('XLBNK', 'BIST:XLBNKD1!', 'VİOP BIST Likit Banka endeks vadelisi (akşam seansı VAR)'),
            ('X10XB', 'BIST:X10XBD1!', 'VİOP BIST Banka Dışı Likit 10 endeks vadelisi (akşam seansı VAR)'),
            ('XSD25', 'BIST:XSD25D1!', 'VİOP BIST Sürdürülebilirlik 25 endeks vadelisi (akşam seansı VAR)')]
VIOP_OTHER = [('USDTRY', 'BIST:USDTRY1!', 'VİOP USD/TRY vadelisi (akşam seansı YOK)'),
              ('EURTRY', 'BIST:EURTRY1!', 'VİOP EUR/TRY vadelisi'),
              ('XAUTRY', 'BIST:XAUTRY1!', 'VİOP gram altın TL vadelisi'),
              ('XAUUSD', 'BIST:XAUUSD1!', 'VİOP ons altın USD vadelisi (akşam seansı VAR)'),
              ('XAGUSD', 'BIST:XAGUSD1!', 'VİOP ons gümüş USD vadelisi (akşam seansı VAR)'),
              ('XPTUSD', 'BIST:XPTUSD1!', 'VİOP ons platin USD vadelisi (akşam seansı VAR)'),
              ('XPDUSD', 'BIST:XPDUSD1!', 'VİOP ons paladyum USD vadelisi (akşam seansı VAR)'),
              ('XCUUSD', 'BIST:XCUUSD1!', 'VİOP bakır USD/ton vadelisi (akşam seansı VAR)'),
              ('XAGTRY', 'BIST:XAGTRY1!', 'VİOP gram gümüş TL vadelisi')]


def fc(code):
    return FC.get(code)


def resolve(code):
    """(nihai_kod, bayrak, açıklama). bayrak: OK, YONLENDI, 404, YOK(okunmadı)"""
    r = fc(code)
    if not r:
        return code, 'YOK', ''
    if r.get('http') != '200':
        return code, '404', ''
    d = r.get('short_desc') or r.get('desc') or ''
    eff = (r.get('eff') or '').replace('https://www.tradingview.com', '')
    m = re.match(r'^/symbols/([^/?]+)/', eff)
    seg = m.group(1) if m else ''
    if '?contract=' in eff or '-' not in seg:
        # vade sözleşmesi sayfası ya da sağlayıcısız kanonik sayfa (FX/kripto/CFD): kod geçerli, olduğu gibi kalır
        return code, ('KANONIK' if '-' not in seg else 'OK'), d
    ex, sy = seg.split('-', 1)
    tgt = f"{ex}:{urllib.parse.unquote(sy)}"
    return (tgt, 'YONLENDI', d) if tgt != code else (code, 'OK', d)


def clean_codes(codes):
    """Kod listesini doğrula/çöz; 404 olanları ayıkla. Dönüş (iyi, 404'ler, notlar)"""
    good, bad, notes = [], [], []
    for c in codes:
        if not c:
            continue
        if is_china(c):
            bad.append(c); notes.append(f'{c} Çin borsası -> çıkarıldı'); continue
        if '<KOD>' in c or any(ch in c for ch in '*()+') or re.search(r'!-|-[A-Z]+:', c):
            good.append(c); continue
        k, fl, d = resolve(c)
        if fl == '404':
            bad.append(c); notes.append(f'{c} sayfası 404')
        elif fl == 'YONLENDI':
            good.append(k); notes.append(f'{c} -> {k} (TV yönlendiriyor)')
        else:
            good.append(k)
    return list(dict.fromkeys(good)), bad, notes


def atom_row(y, ev_f=None):
    e = expected(y)
    kod, alts, du, nt = e['kodu'], list(e['alt']), e['durum'], e['nt']
    notes = [nt] if nt else []
    if du == 'HKEX_BELIRSIZ':
        cand = HK_ALT.get(y, []) + alts
        g, b, n = clean_codes(cand)
        # OTC açıklaması şirketle uyumlu mu? (sayfa açıklaması kayda geçer)
        alts = g
        for c in g:
            if c in OTC_GREY:
                notes.append(f'{c}: OTC gri piyasa, grafik bayat/boşluklu olabilir')
        if b:
            notes.append('doğrulanamayan aday çıkarıldı: ' + ','.join(b))
    else:
        g, b, n = clean_codes([kod])
        if g:
            if g[0] != kod:
                notes.append(f'{kod} yazılınca {g[0]} açılıyor -> {g[0]} kullan')
            kod = g[0]
        elif b and du not in ('CIN_ENGELLI_ALT',):
            fb, _, _ = clean_codes(FALLBACK.get(kod, []))
            notes.append(f'{kod} TradingView sayfası YOK (404, v_tv)' + (f' -> vekil {fb[0]}' if fb else ''))
            alts = fb[1:] + alts
            kod = fb[0] if fb else ''
            du = 'BELIRSIZ'
        ga, ba, na = clean_codes(alts)
        alts = [a for a in ga if a != kod]
        if ba:
            notes.append('404 alternatif çıkarıldı: ' + ','.join(ba))
    if y.endswith('.IS') and y[:-3] in VIOP47:
        alts = [f'BIST:{y[:-3]}1!'] + [a for a in alts if a != f'BIST:{y[:-3]}1!']
    for xi, fut, _ in VIOP_IDX:
        if y == f'{xi}.IS':
            alts = [fut] + [a for a in alts if a != fut]
    return dict(yahoo=y, aciklama=e['aciklama'], tv_kodu=kod, tv_alternatif=' | '.join(alts), durum=du,
                not_='; '.join(x for x in notes if x))


def main():
    ev = evaluate()
    a = load_findings()
    # ---- atomlar ----
    allat = []
    for s in ev.atoms.dropna():
        allat += [x for x in s.split('|') if x]
    for k in VIOP47:
        allat.append(k + '.IS')
    for xi, _, _ in VIOP_IDX:
        allat.append(xi + '.IS')
    allat = list(dict.fromkeys(allat))
    rows = {y: atom_row(y) for y in allat}

    # ---- f_* uyuşmazlık / düzeltme ----
    mis, fix = [], []
    for _, r in ev.iterrows():
        drv, tvf = r.driver_yahoo, r.tv_ticker_f
        at = [x for x in str(r.atoms).split('|') if x and x != 'nan']
        sp = special(drv) if r.kind in ('none', 'composite') else None
        if sp:
            du, kod, alt, nt = sp
            if kod is None:   # akran sepeti: atomlardan üret
                kod = ' | '.join(rows[x]['tv_kodu'] for x in at if x in rows)
            dogru = kod
        elif at:
            dogru = ' | '.join(rows[x]['tv_kodu'] for x in at)
        else:
            dogru = ''
        fix.append(dict(driver_yahoo=drv, tv_ticker_f=tvf, tv_kodu_dogru=dogru, n=r.n, src=r.src, sorunlar=r.issues if isinstance(r.issues, str) else ''))
        for it in [x.strip() for x in str(r.issues).split(';') if x.strip() and x.strip() != 'nan']:
            typ = it.split(':')[0]
            mis.append(dict(tur=typ, src=r.src, driver_yahoo=drv, tv_ticker_f=tvf, dogru_kod=dogru, ayrinti=it, n_satir=r.n))
    mis = pd.DataFrame(mis)
    fixdf = pd.DataFrame(fix)

    # f_* içinde 404 dönen / yönlenen kodları ayrıca yakala (tv_map'te olmasa da)
    extra = []
    for _, r in ev.iterrows():
        for c in [x for x in str(r.tv_codes).split('|') if x and x != 'nan']:
            k, fl, d = resolve(c)
            if fl == '404':
                extra.append(dict(tur='KOD_404', src=r.src, driver_yahoo=r.driver_yahoo, tv_ticker_f=r.tv_ticker_f,
                                  dogru_kod=fixdf.loc[_, 'tv_kodu_dogru'], ayrinti=f'{c} sayfası yok (404)', n_satir=r.n))
            elif fl == 'YONLENDI':
                extra.append(dict(tur='KOD_YONLENDI', src=r.src, driver_yahoo=r.driver_yahoo, tv_ticker_f=r.tv_ticker_f,
                                  dogru_kod=k, ayrinti=f'{c} -> {k}', n_satir=r.n))
    if extra:
        mis = pd.concat([mis, pd.DataFrame(extra)], ignore_index=True)
    mis = mis.drop_duplicates(subset=['tur', 'src', 'driver_yahoo', 'tv_ticker_f', 'ayrinti'])
    # UYUSMAZ ama f_* kodunun sayfası var ve yönlenmiyor -> geçerli ama tercih edilmeyen kod
    def _retag(r):
        if r.tur != 'UYUSMAZ':
            return r.tur
        cs = [c for c, _ in tv_tokens(str(r.tv_ticker_f))]
        fl = [resolve(c)[1] for c in cs]
        if cs and all(x in ('OK', 'KANONIK') for x in fl):
            return 'GECERLI_FARKLI'
        if cs and all(x in ('OK', 'KANONIK', 'YONLENDI') for x in fl):
            return 'YONLENDI_CALISIR'
        return r.tur
    mis['tur'] = mis.apply(_retag, axis=1)

    # atom satırlarına f_* orijinal kod notu
    for y, row in rows.items():
        used = ev[ev.atoms.fillna('').str.split('|').map(lambda L: y in L)]
        fcodes = set()
        for s in used.tv_codes.dropna():
            fcodes |= {c for c in s.split('|') if c}
        wrong = sorted(c for c in fcodes if c not in {row['tv_kodu']} | set(row['tv_alternatif'].split(' | '))
                       and resolve(c)[1] == '404')
        if wrong:
            wu = used[used.tv_codes.fillna('').str.split('|').map(lambda L: any(w in L for w in wrong))]
            srcs = ','.join(sorted(set(','.join(wu.src).split(','))))
            row['not_'] = (row['not_'] + '; ' if row['not_'] else '') + f"DÜZELTME: f_[{srcs}] içindeki {', '.join(wrong)} TradingView'da YOK (404)"

    # ---- bileşik/özel sürücü satırları ----
    comp = []
    for drv, g in ev.groupby('driver_yahoo'):
        r0 = g.iloc[0]
        if r0.kind in ('exact', 'bare_bist') and not special(drv):
            if r0.kind == 'bare_bist':
                y = drv + '.IS'
                rr = dict(rows[y]); rr['yahoo'] = drv
                rr['not_'] = (rr['not_'] + '; ' if rr['not_'] else '') + f'Yahoo kodu {y}'
                comp.append(rr)
            continue
        if r0.kind == 'sina':
            y = r0.atoms
            rr = dict(rows[y]); rr['yahoo'] = drv
            if y == 'SIDX:USDCNH':
                rr.update(tv_kodu='FX:USDCNH', tv_alternatif='FX_IDC:USDCNH | FX_IDC:USDCNY', durum='DOGRULANDI_V',
                          not_='offshore yuan (Çin borsası değil); Sina verisinin TV karşılığı birebir FX:USDCNH')
            comp.append(rr)
            continue
        sp = special(drv)
        at = [x for x in str(r0.atoms).split('|') if x and x != 'nan']
        if sp:
            du, kod, alt, nt = sp
            if kod is None:
                kod = ' | '.join(rows[x]['tv_kodu'] for x in at if x in rows)
            kc = [c for c, _ in tv_tokens(kod)]
            isformula = du == 'FORMUL' or any(ch in kod for ch in '*()') or re.search(r'-[A-Z_]+:', kod)
            if not isformula and kc:
                g2, b2, n2 = clean_codes(kc)
                if b2:
                    nt = (nt + '; ' if nt else '') + 'doğrulanamadı: ' + ','.join(b2)
                kod = ' | '.join(g2)
            ac, ab = [], []
            for piece in [x.strip() for x in (alt or '').split('|') if x.strip()]:
                if '<KOD>' in piece or any(ch in piece for ch in '*()/') and not piece.startswith('BMV:'):
                    ac.append(piece); continue
                g3, b3, _ = clean_codes([c for c, _ in tv_tokens(piece)])
                ac += g3; ab += b3
            if ab:
                nt = (nt + '; ' if nt else '') + '404 alternatif çıkarıldı: ' + ','.join(ab)
            if not kod and du not in ('MODEL', 'OLAY', 'TV_YOK'):
                pass
            comp.append(dict(yahoo=drv, aciklama=str(r0.desc)[:120], tv_kodu=kod, tv_alternatif=' | '.join(ac), durum=du,
                             not_=nt))
        else:
            kod = ' | '.join(rows[x]['tv_kodu'] for x in at if x in rows)
            hk = [rows[x]['tv_alternatif'].split(' | ')[0] for x in at if x in rows and rows[x]['durum'] in ('HKEX_BELIRSIZ', 'CIN_ENGELLI_ALT')]
            du = 'SEPET' if len(at) > 1 else ('KOD' if at else 'MODEL')
            if len(at) == 1:
                rr = dict(rows[at[0]]); rr['yahoo'] = drv
                rr['not_'] = (rr['not_'] + '; ' if rr['not_'] else '') + f'sürücü = {at[0]} (zaman/pencere varyantı)'
                comp.append(rr); continue
            comp.append(dict(yahoo=drv, aciklama=str(r0.desc)[:120], tv_kodu=kod, tv_alternatif=' | '.join(hk),
                             durum=du, not_=f'bileşenler: {", ".join(at)}'))

    # ---- VİOP satırları ----
    viop = []
    for k in VIOP47:
        c = f'BIST:{k}1!'
        g, b, n = clean_codes([c])
        du = 'DOGRULANDI_2KEZ' if g and c in (VERIFIED | {x for d in YMAP.values() for x in d['alts']}) else ('DOGRULANDI_V' if g else 'BELIRSIZ')
        viop.append(dict(yahoo=f'VIOP:{k}1!', aciklama=f'{k} VİOP pay vadelisi (sürekli ön ay)', tv_kodu=c,
                         tv_alternatif=f'BIST:{k}', durum=du,
                         not_=("TV'de 15 dk gecikmeli; akşam seansı YOK; illikit -> bar boşlukları, vade dönüşünde baz sıçraması; "
                               f"vade kodu örn. BIST:{k}Z2026" if g else 'sayfa okunamadı')))
    for xi, c, d in VIOP_IDX + VIOP_OTHER:
        g, b, n = clean_codes([c])
        du = 'DOGRULANDI_2KEZ' if g and c in {x['best'] for x in YMAP.values()} | set(BYC) else ('DOGRULANDI_V' if g else 'BELIRSIZ')
        nt = 'TV\'de 15 dk gecikmeli; ' + ('vade kodu örn. BIST:XU030DZ2026 (Aralık 2026)' if xi == 'XU030' else '')
        if not g:
            nt = f'{c} sayfası 404 (TV kodu bulunamadı); USD gümüş için BIST:XAGUSD1!'
        viop.append(dict(yahoo=f'VIOP:{c.split(":")[1]}', aciklama=d, tv_kodu=c if g else '', tv_alternatif=('BIST:XAGUSD1!' if not g else (f'BIST:{xi}' if xi.startswith('X') and xi in ('XU030', 'XLBNK', 'X10XB', 'XSD25') else '')),
                         durum=du, not_=nt))

    fin = pd.DataFrame(list(rows.values()) + comp + viop)
    fin = fin.rename(columns={'not_': 'not'})
    fin.loc[fin.yahoo.fillna('').str.strip() == '', 'yahoo'] = '(boş driver_yahoo)'
    fin = fin.drop_duplicates(subset=['yahoo'], keep='first')
    # ÇİN öneki son kontrol
    for col in ['tv_kodu', 'tv_alternatif']:
        bad = fin[fin[col].fillna('').str.contains(r'(?<![A-Z_])(SSE|SZSE|SHFE|DCE|ZCE|CFFEX|INE|GFEX|SIDX|FUT|SINA):', regex=True)]
        assert bad.empty, bad[['yahoo', col]]
    order = {'DOGRULANDI_2KEZ': 0, 'DOGRULANDI': 1, 'DOGRULANDI_V': 2, 'HKEX_BELIRSIZ': 3, 'CIN_ENGELLI_ALT': 4, 'BELIRSIZ': 5}
    fin['_o'] = fin.yahoo.str.startswith('VIOP:').map({True: 0, False: 1})
    fin = fin.sort_values(['_o', 'yahoo']).drop(columns='_o')
    fin[['yahoo', 'aciklama', 'tv_kodu', 'tv_alternatif', 'durum', 'not']].to_csv(f'{OUT}/tv_final.csv', index=False)
    mis.to_csv(f'{CODE}/uyusmazliklar.csv', index=False)
    fixdf.to_csv(f'{CODE}/f_tv_duzeltme_esleme.csv', index=False)
    print('tv_final:', len(fin)); print(fin.durum.value_counts().to_string())
    print('uyuşmazlık kaydı:', len(mis)); print(mis.groupby('tur').n_satir.agg(['size', lambda s: s.astype(int).sum()]).to_string())


if __name__ == '__main__':
    main()
