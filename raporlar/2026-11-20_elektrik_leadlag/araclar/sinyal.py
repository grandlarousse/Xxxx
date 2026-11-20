#!/usr/bin/env python3
"""sinyal.py — BIST elektrik (XELKT) günlük sinyal betiği. Bağımlılık: pandas, numpy, requests.

Araştırmadaki dondurulmuş kuralların günlük uygulaması (raporlar/2026-11-20_elektrik_leadlag):
  S1  XELKT kapanışı son 20 günün (bugün dâhil) en yüksek kapanışı       -> dolabilir sektör sepeti AL, 3 gün
  S2  XELKT günlük getirisi / önceki 60 günün std'si (1 gün gecikmeli) >= 1 -> aynı sepet AL, 3 gün
  S3  XU030 z >= 1 ve XELKT z < 0,5 (sektör geride)                      -> AKSEN, ENJSA, ODAS spot AL, 3 gün
  T2  sakin ve güçlü: dolabilir, tavana/tabana değmemiş, 20 günlük oynaklığı sektörün alt yarısında,
      günlük getirisi sektörün en üst üçte birliğinde                    -> 1 gün (sektöre göre; maliyetle ~0)
  K1  günün sektöre göre en kötü beşte birliği                           -> ertesi gün sektörün altında (ALMA)
  K2  sektörden >= 5 puan geride kapanan                                 -> ALMA
Giriş sinyal günü kapanışında (kapanış seansı 18:01–18:10), çıkış h işlem günü sonra kapanışta.

Veri: İş Yatırım'ın herkese açık uç noktaları (HisseTekil, IndexHistoricalAll). Takvim = XU100 günleri.

Kullanım:
  python3 sinyal.py                                   # son işlem günü
  python3 sinyal.py --tarih 2026-11-05                # geçmiş bir günü yeniden üretir
  python3 sinyal.py --gunici XELKT=552,4 XU030=13950  # 17:50'de elle girilen endeks değerleriyle
  python3 sinyal.py --csv hisse.csv --gecmis 20       # hisse tablosu CSV + son 20 günün sinyal dökümü
  python3 sinyal.py --kaydet ham/                     # indirilen ham yanıtları saklar
  python3 sinyal.py --ham ham/ --tarih 2026-11-05     # indirmeden, saklanan ham dosyalardan
"""
import argparse
import datetime as dt
import json
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import requests

XELKT = ('A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES '
         'ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ '
         'NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN').split()
VIOP3 = ['AKSEN', 'ENJSA', 'ODAS']
ENDEKSLER = ['XELKT', 'XU030', 'XU100']
ISY = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/'
UA = {'User-Agent': 'Mozilla/5.0'}
MARJ_TARIH = pd.Timestamp('2020-03-13')     # bu tarihten itibaren günlük marj ±%10, öncesi ±%20
ADIM_TARIH = pd.Timestamp('2023-11-06')     # yeni fiyat adımı tablosu
ZWIN, ZMIN, HIWIN = 60, 40, 20              # z: 60 günlük std (en az 40), 1 gün gecikmeli; zirve: 20 gün
Z_ESIK, Z_GERI = 1.0, 0.5
IPO_GUN, MIN_SEPET = 20, 5
GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']


# ------------------------------------------------------------------------------------------------ veri
def _say(tur, txt):
    try:
        j = json.loads(txt)
        return len(j['value']) if tur == 'isy_hisse' else len(j['data'])
    except Exception:
        return 0


def _getir(tur, kod, bas, son, ham=None, kaydet=None):
    """Bir serinin ham JSON metni. ham verilirse yalnız klasörden okur (ağ yok)."""
    if ham:
        p = os.path.join(ham, tur, kod + '.json')
        if not os.path.exists(p):
            return None
        with open(p, encoding='utf-8') as f:
            return f.read()
    if tur == 'isy_endeks':
        url = ISY + 'ChartData.aspx/IndexHistoricalAll'
        par = {'period': 1440, 'from': bas.strftime('%Y%m%d') + '000000', 'to': son.strftime('%Y%m%d') + '235959',
               'endeks': kod}
    else:
        url = ISY + 'Data.aspx/HisseTekil'
        par = {'hisse': kod, 'startdate': bas.strftime('%d-%m-%Y'), 'enddate': son.strftime('%d-%m-%Y')}
    txt = None
    for a in range(4):
        try:
            r = requests.get(url, params=par, headers=UA, timeout=60)
            if r.status_code == 200 and _say(tur, r.text) > 0:
                txt = r.text
                break
        except Exception:
            pass
        time.sleep(0.5 * 2 ** a + random.random())
    if txt and kaydet:
        os.makedirs(os.path.join(kaydet, tur), exist_ok=True)
        with open(os.path.join(kaydet, tur, kod + '.json'), 'w', encoding='utf-8') as f:
            f.write(txt)
    return txt


def _endeks_seri(txt):
    d = json.loads(txt)['data']
    ix = (pd.to_datetime([x[0] for x in d], unit='ms') + pd.Timedelta(hours=3)).normalize()
    s = pd.Series([x[1] for x in d], index=ix, dtype=float)
    return s[~s.index.duplicated(keep='last')].sort_index()


def _hisse_tablo(txt):
    d = pd.DataFrame(json.loads(txt)['value'])
    out = pd.DataFrame({'c_raw': d['HG_KAPANIS'], 'h_raw': d['HG_MAX'], 'l_raw': d['HG_MIN'],
                        'c_adj': d['HGDG_KAPANIS'], 'vol_tl': d['HG_HACIM']}).astype(float)
    out.index = pd.to_datetime(d['HGDG_TARIH'], format='%d-%m-%Y').values
    return out[~out.index.duplicated(keep='last')].sort_index()


def veri_yukle(bas, son, ham=None, kaydet=None, hisseler=None, sessiz=False):
    """Ham veriyi indirir (ya da ham klasöründen okur). Dönen: (endeks sözlüğü, hisse sözlüğü, eksik listesi)."""
    hisseler = list(hisseler or XELKT)
    isler = [('isy_endeks', k) for k in ENDEKSLER] + [('isy_hisse', k) for k in hisseler]
    with ThreadPoolExecutor(4) as ex:
        metin = list(ex.map(lambda t: _getir(t[0], t[1], bas, son, ham, kaydet), isler))
    endeks, hisse, eksik = {}, {}, []
    for (tur, kod), txt in zip(isler, metin):
        if not txt or _say(tur, txt) == 0:
            eksik.append(kod)
            continue
        if tur == 'isy_endeks':
            endeks[kod] = _endeks_seri(txt)
        else:
            hisse[kod] = _hisse_tablo(txt)
    for k in ENDEKSLER:
        if k not in endeks:
            raise SystemExit(f'HATA: {k} endeks verisi alınamadı (İş Yatırım erişilemedi ya da ham dosya yok).')
    if eksik and not sessiz:
        print('UYARI: verisi alınamayan hisseler (sepet dışı sayıldı): ' + ', '.join(eksik), file=sys.stderr)
    return endeks, hisse, eksik


# ------------------------------------------------------------------------------------------------ panel
def fiyat_adimi(p, tarihler=None):
    """BIST Pay Piyasası fiyat adımı (TL)."""
    p = np.asarray(p, dtype=float)
    yeni = np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500],
                     [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)
    if tarihler is None:
        return yeni
    eski = np.select([p < 20, p < 50, p < 100], [0.01, 0.02, 0.05], 0.10)
    return np.where(np.asarray(pd.DatetimeIndex(tarihler) >= ADIM_TARIH), yeni, eski)


def _carpan(a):
    """Düzeltme çarpanı F (ham/düzeltilmiş), kurumsal işlemler arasında sabit; son gün F = 1."""
    f = a.c_raw / a.c_adj
    fz = f.ffill()
    adim = (fz / fz.shift(1) - 1).abs()
    cadj = a.c_adj.ffill()
    gurultu = 2.2 * 0.00005 / np.minimum(cadj, cadj.shift(1))
    aday = sorted(d for d in adim[adim > np.maximum(0.0005, gurultu)].index if d > a.index[0])
    sinir = [a.index[0]] + aday
    seg = pd.Series(np.searchsorted(pd.DatetimeIndex(sinir), a.index, side='right') - 1, index=a.index)
    med = f.groupby(seg).median()
    tut = [0]
    for k in range(1, len(med)):
        if abs(med.iloc[k] / med.iloc[tut[-1]] - 1) > 0.0003:
            tut.append(k)
    sinir = [sinir[k] for k in tut]
    seg = pd.Series(np.searchsorted(pd.DatetimeIndex(sinir), a.index, side='right') - 1, index=a.index)
    F = f.groupby(seg).transform('median')
    F = F.ffill().bfill()
    return F / F.iloc[-1]


def panel_kur(endeks, hisse, tarih=None):
    """Araştırma panelinin (kod/d1_veri/02_panel.py + elib.load) İş Yatırım'la sınırlı karşılığı.
    Dönen sözlük: cal, idx, R (günlük getiri), vol, fiyat, lu/ld (tavanda/tabanda kapandı), tu/td (değdi),
    tr (işlem görebilir: veri var, hacim > 0, halka arzdan beri > 20 gün, ilk tavansız kapanış görülmüş),
    dol (dolabilir = tr ve tavanda kapanmamış), adv (t−1'e kadarki 60 günlük medyan TL hacim)."""
    if tarih is not None:
        tarih = pd.Timestamp(tarih)
        endeks = {k: v.loc[:tarih] for k, v in endeks.items()}
        hisse = {k: v.loc[:tarih] for k, v in hisse.items()}
    hisse = {k: v for k, v in hisse.items() if len(v)}
    if not hisse:
        raise SystemExit('HATA: hiç hisse verisi yok.')
    herhangi = pd.Index(sorted(set().union(*[set(v.index) for v in hisse.values()])))
    x100 = endeks['XU100'].dropna()
    cal = x100.index[(x100.index.dayofweek < 5) & x100.index.isin(herhangi)]
    if len(cal) < ZWIN + 5:
        raise SystemExit(f'HATA: yalnız {len(cal)} işlem günü var; en az {ZWIN + 5} gerekir (--gun değerini büyütün).')
    pos = pd.Series(np.arange(len(cal)), index=cal)
    W, ipo0 = {}, {}
    for s in [k for k in XELKT if k in hisse] + [k for k in hisse if k not in XELKT]:
        a = hisse[s]
        a = a[a.index.isin(cal)]
        if len(a) == 0:
            continue
        ilk = a.index[0]
        a = a.reindex(cal[cal >= ilk]).copy()
        F = _carpan(a)
        islemsiz = ~(a.vol_tl > 0) & a.c_raw.notna()
        a.loc[islemsiz, 'h_raw'] = a.c_raw[islemsiz]
        a.loc[islemsiz, 'l_raw'] = a.c_raw[islemsiz]
        c = a.c_raw / F
        pc = c.ffill().shift(1)
        baz = a.c_raw.ffill().shift(1) * F / F.shift(1)             # bugünün ham ölçeğinde baz fiyat
        m = pd.Series(np.where(a.index >= MARJ_TARIH, 0.10, 0.20), index=a.index)
        tk = fiyat_adimi(baz * (1 + m), a.index) / baz
        tol = np.maximum(0.006, tk + 1e-9)
        d = pd.DataFrame(index=a.index)
        d['c_raw'] = a.c_raw
        d['vol'] = a.vol_tl.fillna(0.0)
        d['ret'] = c / pc - 1
        d['tu'] = (a.h_raw / baz - 1 >= m - tol)
        d['td'] = (a.l_raw / baz - 1 <= -(m - tol))
        d['lu'] = d.tu & (a.c_raw / baz - 1 >= m - tol) & (a.c_raw >= a.h_raw - 1e-9)
        d['ld'] = d.td & (a.c_raw / baz - 1 <= -(m - tol)) & (a.c_raw <= a.l_raw + 1e-9)
        d = d[a.c_raw.notna()]
        W[s] = d
        # pencerenin ilk günlerinde zaten işlem gören hisse eski sayılır (halka arz süzgeci uygulanmaz)
        ipo0[s] = int(pos[d.index[0]]) - (100000 if pos[d.index[0]] <= 2 else 0)
    syms = list(W)

    def genis(col):
        return pd.DataFrame({s: W[s][col] for s in syms}).reindex(cal)

    def mantik(col):
        return genis(col).astype('boolean').fillna(False).astype(bool)

    R, fiyat, vol = genis('ret'), genis('c_raw'), genis('vol')
    listeli = pd.DataFrame({s: (cal >= W[s].index[0]) for s in syms}, index=cal)
    ipo_n = pd.DataFrame({s: (pos - ipo0[s] + 1).clip(lower=0) for s in syms}, index=cal)
    var = fiyat.notna()
    vol = vol.where(var | ~listeli, 0.0)
    lu, ld, tu, td = mantik('lu'), mantik('ld'), mantik('tu'), mantik('td')
    ilk_serbest = ((~lu) & R.notna()).cumsum() > 0
    tr = (ipo_n > IPO_GUN) & (vol > 0) & var & R.notna() & ilk_serbest
    idx = pd.DataFrame({k: endeks[k] for k in ENDEKSLER}).reindex(cal)
    return {'cal': cal, 'idx': idx, 'R': R, 'vol': vol, 'fiyat': fiyat, 'lu': lu, 'ld': ld, 'tu': tu, 'td': td,
            'tr': tr, 'dol': tr & ~lu, 'ipo_n': ipo_n, 'adv': vol.rolling(60, min_periods=20).median().shift(1),
            'syms': syms}


# ------------------------------------------------------------------------------------------------ sinyaller
def endeks_sinyal(idx, sepet_n=None):
    """Tarih düzeyi sinyaller (kod/a5_rotasyon/rules.py ve kod/a2_endeks/rules.py ile aynı tanım).
    idx: XELKT ve XU030 düzey sütunları (takvim sıralı). sepet_n: günlük dolabilir hisse sayısı (S2 için >= 5)."""
    L = idx[['XELKT', 'XU030']]
    r = L.pct_change(fill_method=None)
    sd = r.rolling(ZWIN, min_periods=ZMIN).std()
    z = r / sd.shift(1)
    E = pd.DataFrame(index=idx.index)
    E['XELKT'], E['XU030'] = L['XELKT'], L['XU030']
    E['rE'], E['rX'] = r['XELKT'], r['XU030']
    E['sdE'], E['sdX'] = sd['XELKT'].shift(1), sd['XU030'].shift(1)          # bugünün z'sinde kullanılan std
    E['zE'], E['zX'] = z['XELKT'], z['XU030']
    E['esikS1'] = L['XELKT'].shift(1).rolling(HIWIN - 1, min_periods=HIWIN - 1).max()   # bugün aşılması gereken
    E['S1'] = L['XELKT'] >= L['XELKT'].rolling(HIWIN, min_periods=HIWIN).max()
    s2 = z['XELKT'] >= Z_ESIK
    if sepet_n is not None:
        s2 = s2 & (sepet_n.reindex(idx.index).ffill() >= MIN_SEPET)
    E['S2'] = s2
    E['S3'] = (z['XU030'] >= Z_ESIK) & (z['XELKT'] < Z_GERI)
    # yarın kapanış için tetik düzeyleri (bugünün verisiyle bilinir)
    E['yS1'] = L['XELKT'].rolling(HIWIN - 1, min_periods=HIWIN - 1).max()
    E['ysdE'], E['ysdX'] = sd['XELKT'], sd['XU030']
    return E


def _dilim_maske(X, oran, yon, min_n):
    """Gün içi sıralamada en alt/üst 'oran'lık dilim: floor(n·oran) hisse (en az 1), n >= min_n; eşitlikte sütun sırası."""
    n = X.notna().sum(axis=1)
    kq = np.floor(n * oran).clip(lower=1)
    r = X.rank(axis=1, method='first', ascending=(yon == 'alt'))
    m = r.le(kq, axis=0) & X.notna()
    return m & np.repeat((n >= min_n).values[:, None], X.shape[1], axis=1)


def _kova(skor, evren, nb, min_n):
    """Gün içi sıraya göre 0..nb−1 dilim (0 = en düşük); n < min_n ise NaN."""
    S = skor.where(evren)
    n = S.notna().sum(axis=1)
    rk = S.rank(axis=1, method='first')
    b = np.floor((rk - 1).mul(nb).div(n.where(n > 0), axis=0))
    b[(n < min_n).values] = np.nan
    return b


def hisse_sinyal(P):
    """Hisse düzeyi listeler (bool tarih×hisse). k5: kod/w3a_kacinma K4a5; kq: kod/a3_kesit rel1 en alt beşte birlik;
    t2: kod/w3b_damitma sade_sig; taban: tabana değdi (tabanda kapansın ya da kapanmasın)."""
    sc = [s for s in XELKT if s in P['R'].columns]
    R, tr, dol = P['R'][sc], P['tr'][sc], P['dol'][sc]
    lu, ld, tu, td = P['lu'][sc], P['ld'][sc], P['tu'][sc], P['td'][sc]
    rk = np.expm1(np.log1p(R)).where(tr)
    n = rk.notna().sum(axis=1)
    ew = rk.mean(axis=1).where(n >= 8)                       # işlem görebilir üyelerin eşit ağırlıklı getirisi
    rel = rk.sub(ew, axis=0)
    k5 = ((rel <= -0.05) & tr).fillna(False).astype(bool)
    kq = _dilim_maske(rel, 0.2, 'alt', 8)
    # T2 (sütunlar alfabetik: eşitlik kuralı araştırma koduyla aynı olsun)
    ss = sorted(sc)
    Rr = R[ss].round(4)
    gecerli = tr[ss] & Rr.notna()
    vol20 = Rr.rolling(20, min_periods=10).std().round(8).where(gecerli)
    bayrak = (tu[ss] & ~lu[ss]) | (td[ss] & ~ld[ss]) | ld[ss]
    sakin = _kova(vol20, dol[ss], 2, 6) == 0
    guclu = _kova(Rr.where(gecerli), dol[ss], 3, 6) == 2
    t2 = (dol[ss] & ~bayrak & sakin & guclu).astype(bool)[sc]
    return {'sc': sc, 'sepet': dol, 'rel': rel, 'ew': ew, 'n': n, 'k5': k5, 'kq': kq, 'taban': (td & tr),
            't2': t2, 'vol20': vol20[sc], 'sepet_n': dol.sum(axis=1)}


# ------------------------------------------------------------------------------------------------ çıktı
def tr_(x, nd=2, isaret=False):
    if x is None or pd.isna(x):
        return 'yok'
    s = f'{x:+,.{nd}f}' if isaret else f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def yz(x, nd=2):
    return '%' + tr_(100 * x, nd, True) if pd.notna(x) else 'yok'


def hisse_tablosu(P, H, t):
    """Son gün için hisse tablosu (likiditeye göre sıralı)."""
    sc = H['sc']
    T = pd.DataFrame({'kod': sc})
    T['tv_kodu'] = 'BIST:' + T['kod']
    T['son_fiyat'] = P['fiyat'].loc[t, sc].values
    T['adim_bps'] = np.round(fiyat_adimi(T['son_fiyat'].values) / T['son_fiyat'].values * 1e4, 1)
    T['medyan_hacim_60g_tl'] = P['adv'].loc[t, sc].values
    T['gunluk_getiri'] = P['R'].loc[t, sc].values
    T['sektore_gore_fark'] = H['rel'].loc[t, sc].values
    T['oynaklik20'] = H['vol20'].loc[t, sc].values
    for ad, M in [('dolabilir', H['sepet']), ('islem_gorebilir', P['tr'][sc]), ('tavanda_kapandi', P['lu'][sc]),
                  ('tabana_degdi', H['taban']), ('tabanda_kapandi', P['ld'][sc]), ('kacin_5puan', H['k5']),
                  ('kacin_en_kotu_beste_bir', H['kq']), ('t2_sakin_guclu', H['t2'])]:
        T[ad] = M.loc[t, sc].values.astype(bool)
    T['halka_arz_gun'] = P['ipo_n'].loc[t, sc].values
    T = T.sort_values('medyan_hacim_60g_tl', ascending=False, na_position='last').reset_index(drop=True)
    T.insert(0, 'tarih', str(t.date()))
    return T


def yazdir(P, E, H, t, ts, gunici=None, eksik=(), gecmis=0):
    """t: endeks sinyal günü; ts: hisse verisinin son günü (gün içi modunda t'den önce olabilir)."""
    e = E.loc[t]
    cz = '=' * 74
    print(cz)
    print(f'ELEKTRİK SİNYALİ | {t.date()} {GUNLER[t.dayofweek]} | kaynak: İş Yatırım')
    if gunici:
        print('GÜN İÇİ MODU: endeks değerleri elle girildi (' + ', '.join(f'{k}={tr_(v)}' for k, v in gunici.items())
              + '). Kesin karar kapanışta.')
    print(cz)
    print('ENDEKSLER')
    print(f'  XELKT {tr_(e.XELKT):>10}  günlük {yz(e.rE):>7}  z {tr_(e.zE, 2, True):>6}  (60 g. std {yz(e.sdE)[1:]})')
    print(f'  XU030 {tr_(e.XU030):>10}  günlük {yz(e.rX):>7}  z {tr_(e.zX, 2, True):>6}  (60 g. std {yz(e.sdX)[1:]})')
    print('-' * 74)
    ev = lambda b: 'EVET' if bool(b) else 'HAYIR'
    print(f'S1  XELKT 20 günlük en yüksek kapanış: {ev(e.S1)}')
    print(f'      kapanış {tr_(e.XELKT)}; eşik {tr_(e.esikS1)} (uzaklık {yz(e.XELKT / e.esikS1 - 1)})')
    if e.S1:
        print('      -> dolabilir sepeti bugün kapanışta AL, 3 işlem günü sonra kapanışta SAT')
    print(f'S2  XELKT z >= 1: {ev(e.S2)}')
    print(f'      z {tr_(e.zE, 2, True)}; eşik getiri {yz(Z_ESIK * e.sdE)} = XELKT {tr_(e.XELKT / (1 + e.rE) * (1 + Z_ESIK * e.sdE))}')
    if e.S2:
        print('      -> dolabilir sepeti bugün kapanışta AL, 3 işlem günü sonra kapanışta SAT')
    print(f'S3  XU030 z >= 1 ve XELKT z < 0,5: {ev(e.S3)}')
    print(f'      XU030 z {tr_(e.zX, 2, True)} (eşik getiri {yz(Z_ESIK * e.sdX)}); XELKT z {tr_(e.zE, 2, True)} (üst sınır {yz(Z_GERI * e.sdE)})')
    if e.S3:
        print('      -> AKSEN, ENJSA, ODAS (spot) bugün kapanışta AL, 3 işlem günü sonra kapanışta SAT')
    if pd.isna(e.zX) or pd.isna(e.zE):
        print('      UYARI: z hesaplanamadı (endeks değeri eksik).')
    print('-' * 74)
    print('YARIN İÇİN TETİK DÜZEYLERİ (yarın kapanışta; bugünkü değerlere göre)')
    print(f'  S1: XELKT >= {tr_(e.yS1)}  ({yz(e.yS1 / e.XELKT - 1)})')
    print(f'  S2: XELKT >= {tr_(e.XELKT * (1 + Z_ESIK * e.ysdE))}  ({yz(Z_ESIK * e.ysdE)})')
    print(f'  S3: XU030 >= {tr_(e.XU030 * (1 + Z_ESIK * e.ysdX))}  ({yz(Z_ESIK * e.ysdX)})  ve  '
          f'XELKT < {tr_(e.XELKT * (1 + Z_GERI * e.ysdE))}  ({yz(Z_GERI * e.ysdE)})')
    print('-' * 74)
    T = hisse_tablosu(P, H, ts)
    if ts != t:
        print(f'HİSSE LİSTELERİ {ts.date()} kapanışına göredir (bugünün hisse verisi yok). Bugün tavanda')
        print('kapananı sepetten kendiniz çıkarın; kaçınma ve T2 listeleri bugün için geçerli değildir.')
    S = T[T.dolabilir]
    print(f'SEPET: dolabilir {len(S)} hisse (likiditeye göre sıralı) | eşit ağırlıklı sektör {yz(H["ew"].loc[ts])}'
          + ('' if len(S) >= MIN_SEPET else '  UYARI: 5\'ten az, S1/S2 uygulanmaz'))
    print('  #  TradingView    fiyat  adım  hacim   gün    fark  not')
    print('                      TL   bps  mn TL     %    puan')
    for i, r in S.iterrows():
        nt = [n for n, f in (('KAÇIN-5', r.kacin_5puan), ('en kötü 1/5', r.kacin_en_kotu_beste_bir),
                             ('taban', r.tabana_degdi), ('T2', r.t2_sakin_guclu), ('VİOP', r.kod in VIOP3)) if f]
        print(f'  {list(S.index).index(i) + 1:>2} {r.tv_kodu:<11} {tr_(r.son_fiyat):>8} {tr_(r.adim_bps, 0):>5} '
              f'{tr_(r.medyan_hacim_60g_tl / 1e6, 0):>6} {tr_(100 * r.gunluk_getiri, 1, True):>6} '
              f'{tr_(100 * r.sektore_gore_fark, 1, True):>6}  {", ".join(nt)}')
    D = T[~T.dolabilir]
    if len(D) or eksik:
        neden = lambda r: ('tavanda kapandı' if r.tavanda_kapandi else 'halka arz süzgeci' if r.halka_arz_gun <= IPO_GUN
                           else 'işlem yok' if pd.isna(r.gunluk_getiri) or pd.isna(r.son_fiyat) else 'süzgeç dışı')
        print('  Sepet dışı: ' + ', '.join([f'{r.kod} ({neden(r)})' for _, r in D.iterrows()]
                                          + [f'{k} (veri yok)' for k in eksik if k in XELKT]))
    print('-' * 74)
    print('KAÇINMA (bu hisseleri bugün kapanışta ALMA; 1 günlük)')
    K5, KQ, TB = T[T.kacin_5puan], T[T.kacin_en_kotu_beste_bir], T[T.tabana_degdi]
    f1 = lambda X: ', '.join(f'{r.kod} ({tr_(100 * r.sektore_gore_fark, 1, True)})' for _, r in
                             X.sort_values('sektore_gore_fark').iterrows()) or 'yok'
    print('  Sektörden >= 5 puan geride: ' + f1(K5))
    print('  Günün en kötü beşte birliği: ' + f1(KQ))
    print('  Tabana değen: ' + (', '.join(f'{r.kod} ({"tabanda kapandı" if r.tabanda_kapandi else "değdi"})'
                                          for _, r in TB.iterrows()) or 'yok'))
    print('-' * 74)
    T2 = T[T.t2_sakin_guclu]
    print('T2 SAKİN VE GÜÇLÜ (1 gün, sektöre göre; maliyet sonrası ~0: yalnız seçim yardımcısı)')
    print('  ' + (', '.join(f'{r.kod} (gün {tr_(100 * r.gunluk_getiri, 1, True)}, oynaklık {tr_(100 * r.oynaklik20, 1)})'
                            for _, r in T2.iterrows()) or 'yok'))
    if gecmis:
        print('-' * 74)
        print(f'SON {gecmis} GÜN')
        print('  tarih          XELKT   gün %    zE     zX   S1 S2 S3')
        for d, x in E.tail(gecmis).iterrows():
            print(f'  {d.date()} {tr_(x.XELKT):>10} {tr_(100 * x.rE, 2, True):>7} {tr_(x.zE, 2, True):>6} '
                  f'{tr_(x.zX, 2, True):>6}   {"X" if x.S1 else "."}  {"X" if x.S2 else "."}  {"X" if x.S3 else "."}')
    print(cz)
    print('Not: fark = hisse − eşit ağırlıklı sektör (puan). Dolabilir = işlem görüyor, halka arzdan beri')
    print('> 20 gün, tavanda kapanmamış. Yatırım tavsiyesi değildir; sonuçlar maliyet öncesi ölçülmüştür.')
    return T


def _gunici_ayir(parcalar):
    out = {}
    for p in parcalar or []:
        if '=' not in p:
            raise SystemExit(f'--gunici biçimi: XELKT=552,4 XU030=13950 (hatalı: {p})')
        k, v = p.split('=', 1)
        k = k.strip().upper()
        if k not in ('XELKT', 'XU030'):
            raise SystemExit(f'--gunici yalnız XELKT ve XU030 kabul eder (hatalı: {k})')
        v = v.strip()
        if ',' in v:
            v = v.replace('.', '').replace(',', '.')
        out[k] = float(v)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='BIST elektrik (XELKT) günlük sinyali')
    ap.add_argument('--tarih', help='YYYY-AA-GG: geçmiş bir günü yeniden üretir')
    ap.add_argument('--gunici', nargs='+', metavar='KOD=DEĞER', help='ör. XELKT=552,4 XU030=13950 (17:50 değerleri)')
    ap.add_argument('--gun', type=int, default=450, help='çekilecek takvim günü (varsayılan 450 ≈ 300 işlem günü)')
    ap.add_argument('--csv', help='hisse tablosunu bu dosyaya yazar')
    ap.add_argument('--csv-gecmis', help='endeks sinyal geçmişini bu dosyaya yazar')
    ap.add_argument('--gecmis', type=int, default=0, help='son N günün sinyal dökümünü de yazdırır')
    ap.add_argument('--ham', help='indirmeden, bu klasördeki ham dosyaları kullanır (isy_endeks/, isy_hisse/)')
    ap.add_argument('--kaydet', help='indirilen ham yanıtları bu klasöre yazar')
    a = ap.parse_args(argv)
    bugun = dt.datetime.now(dt.timezone(dt.timedelta(hours=3)))
    son = pd.Timestamp(a.tarih) if a.tarih else pd.Timestamp(bugun.date())
    bas = son - pd.Timedelta(days=max(a.gun, 150))
    gunici = _gunici_ayir(a.gunici)
    endeks, hisse, eksik = veri_yukle(bas, son, a.ham, a.kaydet)
    P = panel_kur(endeks, hisse, son)
    H = hisse_sinyal(P)
    idx = P['idx'].copy()
    ts = idx.index[-1]
    if gunici:
        g = son.normalize()
        if g < ts:
            raise SystemExit('--gunici için tarih, verinin son gününden önce olamaz.')
        for k, v in gunici.items():
            idx.loc[g, k] = v
        idx = idx.sort_index()
    E = endeks_sinyal(idx, H['sepet_n'])
    t = E.index[-1]
    if not gunici and a.tarih and ts != son:
        print(f'UYARI: {son.date()} işlem günü değil ya da verisi yok; son veri günü {ts.date()} kullanıldı.')
    if not gunici and not a.tarih:
        if ts.date() == bugun.date() and (bugun.hour, bugun.minute) < (18, 10):
            print('UYARI: seans bitmeden alınan bugünkü veri kesin değildir; 18:10 sonrası yeniden çalıştırın.')
        if (pd.Timestamp(bugun.date()) - ts).days > 4:
            print('UYARI: veri 4 günden eski görünüyor.')
    T = yazdir(P, E, H, t, ts, gunici, eksik, a.gecmis)
    if a.csv:
        T.to_csv(a.csv, index=False)
        print('CSV yazıldı:', a.csv)
    if a.csv_gecmis:
        E.to_csv(a.csv_gecmis, index_label='tarih')
        print('CSV yazıldı:', a.csv_gecmis)


if __name__ == '__main__':
    main()
