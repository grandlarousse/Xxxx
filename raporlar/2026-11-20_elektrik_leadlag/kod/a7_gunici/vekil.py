#!/usr/bin/env python3
"""vekil.py — 17:50 vekili: bir rules.py kuralını "kapanıştan önce görülen fiyatla" yeniden kurar (A7, YONTEM_EK E1).

Soru: kullanıcı kararı 17:50'de verir, ama kurallar t günü KAPANIŞ getirisiyle yazılmıştır.
Bu araç t günü kapanışına bağlı girdileri 17:50 fiyatıyla değiştirir, kuralı yeniden kurar ve
gerçek kapanışla kurulan sinyalle karşılaştırır.

Kullanım (komut satırı):
    python3 -I vekil.py <panel_klasoru> <.../kod/<ajan>/rules.py | ajan klasörü> \
        [--nokta p_1750] [--bas 2025-07-01] [--son 2026-11-20] [--mod tam|hizli] [--kor] [--cikti sonuc.csv]

Kullanım (Python):
    import sys; sys.path.insert(0, '<.../kod/a7_gunici>'); sys.path.insert(0, '<.../kod/ortak>')
    import elib, vekil
    P = elib.load('<panel>')
    build = vekil.kural_yukle('<.../kod/a4_olay/rules.py>')
    tablo, sinyaller = vekil.karsilastir(build, P, nokta='p_1750', bas='2025-07-01')
    print(tablo[['ad', 'n_gercek', 'n_vekil', 'kesinlik', 'yakalama', 'ort_kacan_bps', 'ort_yanlis_bps', 'fark_bps']])

Ne değiştirilir (yalnız t satırı; t−1 ve öncesi gerçek kapanışla kalır):
    ret_cc(t)   = p_nokta(t)/p_close(t−1) − 1  [= (1+r_cc)·p_nokta/p_close − 1; kurumsal işlem günlerinde de doğru]
    ret_oc(t)   = p_nokta(t)/p_open(t) − 1
    close_raw(t)= p_nokta(t)
    lim_up/lim_dn(t) = gün içinde sınıra değmiş VE nokta fiyatı günün ucunda (yarım adım içinde); fill_long/fill_short buna göre
    vol_tl(t)   = vol_tl · hacim_payi  (17:50'ye kadar oluşan hacim; ölçüm: ek/a7_kapanis_hacim.csv, varsayılan 0,92)
    idx_ret/idx(t): XELKT, XU030, XU100 kendi anlık değeriyle; anlık değeri olmayan endeksler XU100'ün oranıyla
    px (uzun tablo): c ve c_raw
Değiştirilmeyenler (uyarı sütunu `vekilsiz_girdi`): viop_daily/viop_front (uzlaşma 18:00–18:10'da oluşur; gün içi
vadeli verisi yok), lim_*_touch, snap. Bu girdileri kullanan kuralın (A6) vekil sonucu İYİMSERDİR.

mod='tam'  : her gün için yalnız o günün satırı değiştirilip build() yeniden çağrılır (doğru; gün sayısı × build süresi).
mod='hizli': bütün günler birden değiştirilir, tek build(). Yalnız t günü getirisini kullanan kurallarda aynı sonucu
             verir; çok günlük birikimli getiri ya da yürüyen std kullanan kurallarda yaklaşık olur.

Çıktı sütunları: kesinlik = ortak / vekil sinyali (17:50'de "var" dediğinin kaçı kapanışta da var);
yakalama = ortak / gerçek sinyal; ort_kacan_bps = 17:50'de görülmeyen gerçek sinyallerin ortalama fazla getirisi;
ort_yanlis_bps = 17:50'de görülüp kapanışta kaybolan sinyallerin sonucu (kullanıcı bunlara girmiş olur);
ort_gercek_bps / ort_vekil_bps = kâğıt üstü kural ile 17:50'de uygulanan kuralın dolabilir işlem ortalaması.
Getiriler giriş = t KAPANIŞI varsayımıyla ve gerçek kapanış kilidine göre "dolabilir" hesaplanır (elib).
--kor: getiri sütunlarını yazmaz (kör protokol: yalnız örtüşme).

Not: panel_dev'de hisselerin p_1750 sütunu saatlik veriden gelir ve gerçekte 17:30 fiyatıdır (20 dk bayat); gerçek
17:50 yalnız 5 dakikalık verinin olduğu son ~60 günde vardır (snap.bar_1750 = '17:45'). `--nokta p_son` (18:00 son
sürekli işlem fiyatı; yalnız yaz saati aylarında) üst sınırı verir.
"""
import argparse
import importlib.util
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ortak'))
import elib  # noqa: E402

VEKILSIZ = {'viop_daily', 'viop_front', 'lim_up_touch', 'lim_dn_touch', 'snap'}


# ---------------------------------------------------------------- anlık fiyat yardımcıları
GUNICI_KOLON = ('p_1630', 'p_1700', 'p_1730', 'p_1750', 'p_son')
_ARTIK = {}


def yahoo_artik(P, pencere=11):
    """Yahoo gün içi hisse fiyatlarındaki ARTIK düzeltme çarpanı (gün × hisse; çoğu gün 1).
    snap fiyatları `bar / yahoo_carpan` ile ham ölçeğe çevrilmiş, ama Yahoo geçmiş barları nakit temettü için de
    küçültüyor (ör. 0,9991); bu pay snap'te duruyor ve tavan fiyatındaki işlemi "tavanın altında" gösteriyor.
    Kestirim: saatlik barların günlük en yükseği/en düşüğü ile günlük ham en yüksek/en düşük oranının yürüyen medyanı."""
    key = dict.get(P, 'dir')
    if key in _ARTIK:
        return _ARTIK[key]
    R = dict.__getitem__(P, 'ret_cc')
    px = dict.__getitem__(P, 'px')[['date', 'sym', 'h_raw', 'l_raw']].copy()
    px['date'] = pd.to_datetime(px['date'])
    hi = px.pivot(index='date', columns='sym', values='h_raw')
    lo = px.pivot(index='date', columns='sym', values='l_raw')
    sn = dict.__getitem__(P, 'snap')
    car = None
    if 'yahoo_carpan' in sn.columns:
        car = sn.assign(date=pd.to_datetime(sn['date'])).pivot(index='date', columns='sym', values='yahoo_carpan')
    out = {}
    d1 = os.path.join(str(key), 'h1')
    if os.path.isdir(d1):
        for f in sorted(os.listdir(d1)):
            sym = f.replace('.parquet', '')
            if sym not in hi.columns:
                continue
            h = pd.read_parquet(os.path.join(d1, f), columns=['ts_tr', 'h', 'l'])
            g = h.groupby(h['ts_tr'].dt.normalize()).agg(h=('h', 'max'), l=('l', 'min'))
            c = car[sym].reindex(g.index).fillna(1.0) if (car is not None and sym in car.columns) else 1.0
            gh = (g['h'] / c) / hi[sym].reindex(g.index)
            gl = (g['l'] / c) / lo[sym].reindex(g.index)
            gh = gh.where((gh > 0.97) & (gh < 1.03)).rolling(pencere, center=True, min_periods=3).median()
            gl = gl.where((gl > 0.97) & (gl < 1.03)).rolling(pencere, center=True, min_periods=3).median()
            a = pd.concat([gh, gl], axis=1).mean(axis=1)
            out[sym] = a.where((a - 1).abs() >= 1e-4, 1.0)
    A = pd.DataFrame(out).reindex(R.index).fillna(1.0) if out else pd.DataFrame(index=R.index)
    _ARTIK[key] = A
    return A


def snap_fiyat(P, kolon, duzelt=True):
    """snap (uzun) → tarih × sembol matrisi. duzelt: hisselerin gün içi fiyatı Yahoo artık çarpanına bölünür."""
    s = dict.__getitem__(P, 'snap')[['date', 'sym', kolon]].copy()
    s['date'] = pd.to_datetime(s['date'])
    M = s.pivot(index='date', columns='sym', values=kolon)
    if duzelt and kolon in GUNICI_KOLON:
        A = yahoo_artik(P)
        ortak = [c for c in M.columns if c in A.columns]
        if ortak:
            M[ortak] = M[ortak] / A[ortak].reindex(M.index).fillna(1.0)
    return M


def snap_oran(P, nokta='p_1750'):
    """oran[t, sym] = p_nokta / p_close (aynı gün, ham fiyat). ±%15 dışı (veri hatası) boş."""
    q = snap_fiyat(P, nokta) / snap_fiyat(P, 'p_close')
    q = q.where((q > 0.85) & (q < 1.15))
    return q.reindex(P['ret_cc'].index)


def kilit_vekil(P, nokta='p_1750'):
    """Nokta anında tavan/taban kilidi: gün içinde sınıra değmiş ve nokta fiyatı günün ucunda (yarım adım içinde).
    Dönen: (tavan, taban, fiyat_var) bool matrisleri."""
    R = P['ret_cc']
    px = P['px'][['date', 'sym', 'h_raw', 'l_raw']].copy()
    px['date'] = pd.to_datetime(px['date'])
    hi = px.pivot(index='date', columns='sym', values='h_raw').reindex(index=R.index, columns=R.columns)
    lo = px.pivot(index='date', columns='sym', values='l_raw').reindex(index=R.index, columns=R.columns)
    p = snap_fiyat(P, nokta).reindex(index=R.index, columns=R.columns)
    tick = pd.DataFrame(elib.tick_of(hi.values), index=R.index, columns=R.columns)
    tu = P['lim_up_touch'] if 'lim_up_touch' in P else P['lim_up']
    td = P['lim_dn_touch'] if 'lim_dn_touch' in P else P['lim_dn']
    up = (tu | P['lim_up']) & (p >= hi - 0.5 * tick)
    dn = (td | P['lim_dn']) & (p <= lo + 0.5 * tick)
    return up.fillna(False).astype(bool), dn.fillna(False).astype(bool), p.notna()


def vekil_panel(P, nokta='p_1750', hacim_payi=0.92):
    """Bütün günleri vekille değiştirilmiş matrisler (sözlük). Vekili olmayan hücre gerçek değerinde kalır."""
    R = P['ret_cc']
    q = snap_oran(P, nokta)
    qs = q.reindex(columns=R.columns)
    has = qs.notna()
    N = {'ret_cc': ((1 + R) * qs - 1).where(has, R)}
    if 'ret_oc' in P:
        A = P['ret_oc']
        qa = qs.reindex(index=A.index, columns=A.columns)
        N['ret_oc'] = ((1 + A) * qa - 1).where(qa.notna(), A)
    if 'close_raw' in P:
        A = P['close_raw']
        qa = qs.reindex(index=A.index, columns=A.columns)
        N['close_raw'] = (A * qa).where(qa.notna(), A)
    if 'vol_tl' in P:
        A = P['vol_tl']
        qa = qs.reindex(index=A.index, columns=A.columns)
        N['vol_tl'] = (A * hacim_payi).where(qa.notna(), A)
    if 'px' in P:
        up, dn, _ = kilit_vekil(P, nokta)
        N['lim_up'] = up.where(has, P['lim_up']).astype(bool)
        N['lim_dn'] = dn.where(has, P['lim_dn']).astype(bool)
        N['fill_long'] = P['tradable'] & ~N['lim_up']
        N['fill_short'] = P['tradable'] & ~N['lim_dn']
    if 'idx_ret' in P:
        I = P['idx_ret']
        qi = q.reindex(index=I.index, columns=I.columns)
        for ref in ('XU100', 'XU030'):            # anlık değeri olmayan endeks: geniş endeksin oranı
            if ref in q.columns:
                qi = qi.apply(lambda col: col.fillna(q[ref].reindex(I.index)))
        N['idx_ret'] = ((1 + I) * qi - 1).where(qi.notna(), I)
        if 'idx' in P:
            L = P['idx']
            ql = qi.reindex(index=L.index, columns=L.columns)
            N['idx'] = (L * ql).where(ql.notna(), L)
    return N, q


class Izleyen(dict):
    """Hangi panel anahtarlarının okunduğunu kaydeden sözlük (vekillenmeyen girdi uyarısı için)."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.okunan = set()

    def __getitem__(self, k):
        self.okunan.add(k)
        return super().__getitem__(k)

    def get(self, k, d=None):
        self.okunan.add(k)
        return super().get(k, d)


def kur_vekilli(build, P, gunler, nokta='p_1750', hacim_payi=0.92, mod='tam', ilerleme=False):
    """Kuralı vekil girdilerle kurar. Dönen: ({kural adı: bool DataFrame (gunler × hisse)}, okunan anahtarlar)."""
    N, q = vekil_panel(P, nokta, hacim_payi)
    Q = Izleyen({k: v for k, v in P.items() if k != '_cache'})
    dict.__setitem__(Q, '_cache', {})
    gunler = pd.DatetimeIndex(gunler)
    if mod == 'hizli':
        for n, v in N.items():
            dict.__setitem__(Q, n, v)
        if 'px' in P:
            dict.__setitem__(Q, 'px', _px_tum(P, q))
        rules = build(Q)
        out = {r['ad']: r['sig'].reindex(gunler).fillna(False).astype(bool) for r in rules}
        return out, set(Q.okunan)
    for n in N:
        dict.__setitem__(Q, n, P[n].copy())
    px_grp = None
    if 'px' in P:
        Qpx = P['px'].copy()
        dict.__setitem__(Q, 'px', Qpx)
        px_grp = Qpx.groupby(pd.to_datetime(Qpx['date'])).indices
        jc = [Qpx.columns.get_loc(c) for c in ('c', 'c_raw')]
    rows = {}
    for k, t in enumerate(gunler):
        saved = {}
        for n in N:
            if t not in Q[n].index:
                continue
            i = Q[n].index.get_loc(t)
            saved[n] = (i, P[n].iloc[i].values.copy())
            dict.__getitem__(Q, n).iloc[i] = N[n].iloc[i].values
        if px_grp is not None and t in px_grp:
            pos = px_grp[t]
            old = Qpx.iloc[pos, jc].values.copy()
            r = q.loc[t].reindex(Qpx['sym'].values[pos]).values
            new = np.where(np.isfinite(r)[:, None], old * np.nan_to_num(r, nan=1.0)[:, None], old)
            Qpx.iloc[pos, jc] = new
        dict.__setitem__(Q, '_cache', {})
        for r_ in build(Q):
            s = r_['sig']
            rows.setdefault(r_['ad'], {})[t] = s.loc[t] if t in s.index else pd.Series(dtype=bool)
        for n, (i, v) in saved.items():
            dict.__getitem__(Q, n).iloc[i] = v
        if px_grp is not None and t in px_grp:
            Qpx.iloc[pos, jc] = old
        if ilerleme and (k + 1) % 50 == 0:
            print(f'  vekil: {k + 1}/{len(gunler)} gün', file=sys.stderr, flush=True)
    out = {ad: pd.DataFrame(d).T.reindex(gunler).fillna(False).astype(bool) for ad, d in rows.items()}
    return out, set(Q.okunan)


def _px_tum(P, q):
    px = P['px'].copy()
    d = pd.to_datetime(px['date'])
    qq = q.stack().rename('q')
    r = pd.MultiIndex.from_arrays([d, px['sym']]).map(qq.to_dict())
    r = pd.Series(np.asarray(r, dtype=float), index=px.index).fillna(1.0)
    for c in ('c', 'c_raw'):
        px[c] = px[c] * r
    return px


def _ozet(mask, X, F, h):
    p, n, _ = elib.day_series(mask, X, F)
    d = (n > 0).values.astype(float)
    if d.sum() == 0:
        return np.nan, np.nan, 0
    x = p.fillna(0).values
    mu, t = elib._hac_mean(x, d, max(h - 1, 0))
    if not np.isfinite(mu):
        mu = x.sum() / d.sum()
    return float(mu), (float(t) if np.isfinite(t) else np.nan), int(n.sum())


def karsilastir(build, P, nokta='p_1750', bas=None, son=None, mod='tam', hacim_payi=0.92, kor=False,
                min_kapsam=5, ilerleme=False):
    """Gerçek kapanışla ve vekille kurulan sinyalleri karşılaştırır.
    Dönen: (tablo DataFrame, {ad: (gercek, vekil)} sinyal matrisleri — değerlendirme günleriyle sınırlı)."""
    cols = list(P['ret_cc'].columns)
    q = snap_oran(P, nokta)
    kapsam = q.reindex(columns=cols).notna().sum(axis=1)
    gunler = kapsam.index[kapsam >= min_kapsam]
    if bas is not None:
        gunler = gunler[gunler >= pd.Timestamp(bas)]
    if son is not None:
        gunler = gunler[gunler <= pd.Timestamp(son)]
    if len(gunler) == 0:
        raise SystemExit('Vekil fiyatı olan gün yok (snap kapsamını ve --nokta sütununu kontrol et).')
    gercek = build(P)
    vek, okunan = kur_vekilli(build, P, gunler, nokta, hacim_payi, mod, ilerleme)
    uyar = ','.join(sorted(okunan & VEKILSIZ))
    bar = ''
    if 'bar_1750' in P['snap'].columns and nokta == 'p_1750':
        s = P['snap']
        s = s[pd.to_datetime(s['date']).isin(gunler) & s['sym'].isin(cols)]
        bar = ';'.join(f'{k}:{v}' for k, v in s['bar_1750'].value_counts().head(3).items())
    rows, sigs = [], {}
    for r in gercek:
        cr = [c for c in r['sig'].columns if c in cols]
        A = r['sig'].reindex(index=gunler, columns=cr).fillna(False).astype(bool)
        B = vek[r['ad']].reindex(index=gunler, columns=cr).fillna(False).astype(bool)
        sigs[r['ad']] = (A, B)
        h, side, olcu = int(r['h']), r.get('yon', 'long'), r.get('olcu', 'own')
        tp, fn, fp = A & B, A & ~B, B & ~A
        nA, nB, nT = int(A.values.sum()), int(B.values.sum()), int(tp.values.sum())
        gA, gB = A.any(axis=1), B.any(axis=1)
        row = {'ad': r['ad'], 'h': h, 'yon': side, 'olcu': olcu, 'arac': r.get('arac', 'spot'), 'nokta': nokta,
               'mod': mod, 'bas': str(gunler[0].date()), 'son': str(gunler[-1].date()), 'n_gun': len(gunler),
               'n_gercek': nA, 'n_vekil': nB, 'n_ortak': nT,
               'kesinlik': nT / nB if nB else np.nan, 'yakalama': nT / nA if nA else np.nan,
               'gun_gercek': int(gA.sum()), 'gun_vekil': int(gB.sum()), 'gun_ortak': int((gA & gB).sum())}
        M, fillable = elib.excess_measures(P, h, side, cr)
        F = fillable.reindex(gunler)
        row['n_vekil_dolmaz'] = int((B & ~F.fillna(False)).values.sum())   # 17:50'de sinyal var, kapanış kilitli
        row['n_gercek_dolmaz'] = int((A & ~F.fillna(False)).values.sum())
        if not kor:
            X = M[olcu].reindex(gunler) * 1e4
            for ad, m in (('ortak', tp), ('kacan', fn), ('yanlis', fp)):
                mu, _, n = _ozet(m, X, F, h)
                row[f'ort_{ad}_bps'], row[f'n_{ad}_dolabilir'] = mu, n
            mg, tg, _ = _ozet(A, X, F, h)
            mv, tv, _ = _ozet(B, X, F, h)
            row.update({'ort_gercek_bps': mg, 't_gercek': tg, 'ort_vekil_bps': mv, 't_vekil': tv,
                        'fark_bps': mv - mg if np.isfinite(mv) and np.isfinite(mg) else np.nan})
        row['vekilsiz_girdi'] = uyar
        row['bar_1750'] = bar
        rows.append(row)
    return pd.DataFrame(rows), sigs


def kural_yukle(yol):
    """rules.py dosyasından (ya da onu içeren klasörden) build fonksiyonunu yükler."""
    if os.path.isdir(yol):
        yol = os.path.join(yol, 'rules.py')
    spec = importlib.util.spec_from_file_location('rules_' + os.path.basename(os.path.dirname(os.path.abspath(yol))), yol)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.abspath(yol)))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod.build


def main():
    ap = argparse.ArgumentParser(description='17:50 vekiliyle kural yeniden kurma ve örtüşme raporu')
    ap.add_argument('panel')
    ap.add_argument('rules')
    ap.add_argument('--nokta', default='p_1750', help='snap sütunu: p_1750 | p_1730 | p_son | p_1700')
    ap.add_argument('--bas')
    ap.add_argument('--son')
    ap.add_argument('--mod', default='tam', choices=['tam', 'hizli'])
    ap.add_argument('--hacim-payi', type=float, default=0.92)
    ap.add_argument('--kor', action='store_true', help='getiri sütunlarını yazma (yalnız örtüşme)')
    ap.add_argument('--cikti')
    a = ap.parse_args()
    P = elib.load(a.panel)
    tablo, _ = karsilastir(kural_yukle(a.rules), P, a.nokta, a.bas, a.son, a.mod, a.hacim_payi, a.kor, ilerleme=True)
    pd.set_option('display.width', 250, 'display.max_columns', 40)
    goster = [c for c in ['ad', 'h', 'n_gun', 'n_gercek', 'n_vekil', 'n_ortak', 'kesinlik', 'yakalama', 'n_vekil_dolmaz',
                          'ort_ortak_bps', 'ort_kacan_bps', 'ort_yanlis_bps', 'ort_gercek_bps', 'ort_vekil_bps',
                          'fark_bps', 'vekilsiz_girdi'] if c in tablo.columns]
    print(tablo[goster].round(3).to_string(index=False))
    if a.cikti:
        tablo.to_csv(a.cikti, index=False)


if __name__ == '__main__':
    main()
