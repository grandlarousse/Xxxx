#!/usr/bin/env python3
"""SAHOL/AKBNK oran ortalamaya dönüş — günlük kapanış sinyali (bağımlılık: pandas, numpy, requests).

Kural (araştırmadaki ile birebir):
  r = log(adj kapanış) farkı; BIST takvimi (XU100 günleri); kurumsal işlem/veri hatası: |basit getiri| > %20,5 (13.03.2020 öncesi) / %10,5 (sonrası) -> NaN
  β = 250 günlük (en az 125) kayan cov(rSAHOL, rAKBNK)/var(rAKBNK), BİR GÜN GECİKMELİ (bugünün β'sı dünkü veriyle)
  S = kümülatif( rSAHOL − β·rAKBNK ), z = (S − ort60(S)) / std60(S)
  GİRİŞ: |z| > 1,5 olan yeni bir bölümün ilk günü -> z > +1,5: SHORT spread (SAHOL SAT, AKBNK AL) ; z < −1,5: LONG spread (SAHOL AL, AKBNK SAT)
  ÇIKIŞ: Kural A (varsayılan, 1–5 gün): z bant içine döner (|z| <= 1,5)   | Kural C: |z| 1,0'a döner | Kural B: |z| 0,5'e döner
  Uygulama: aynı akşam VİOP ön vade (vadeye 1 iş gününden fazla kalan en yakın vade) uzlaşma penceresinde (seansın son 10 dk'sı).
  Kontrat oranı: N_AKBNK = yuvarla( N_SAHOL · β · F_SAHOL / F_AKBNK )   (β-ağırlıklı TL nominal)

Kullanım:
  python3 sinyal.py                               # Yahoo'dan çek, Kural A
  python3 sinyal.py --kural B --fa 84.38 --fb 63.64 --sermaye 1000000
  python3 sinyal.py --csv-sahol sahol.csv --csv-akbnk akbnk.csv   # CSV: tarih + (adj)kapanış sütunu
  python3 sinyal.py --pozisyon long               # elinizdeki pozisyon için çıkış kontrolü
  python3 sinyal.py --canli                       # seans içinde (ör. 17:55) anlık fiyatla tahmini z
"""
import argparse, sys, time, datetime as dt
import numpy as np, pandas as pd, requests

REGIME = pd.Timestamp('2020-03-13')
RULES = {'A': 1.5, 'C': 1.0, 'B': 0.5}
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

# ------------------------------------------------------------------ veri
def yahoo(sym, canli=False):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}'
    p = {'period1': int(pd.Timestamp('2008-01-01').timestamp()), 'period2': int(time.time()) + 86400, 'interval': '1d', 'events': 'div,splits', 'includePrePost': 'false'}
    for a in range(4):
        try:
            r = requests.get(url, params=p, headers=UA, timeout=40)
            if r.status_code == 200: break
        except Exception:
            pass
        time.sleep(2 * (a + 1))
    else:
        raise SystemExit(f'{sym}: Yahoo erişilemedi')
    j = r.json()['chart']['result'][0]; q = j['indicators']['quote'][0]; m = j['meta']
    adj = (j['indicators'].get('adjclose') or [{}])[0].get('adjclose') or q['close']
    idx = pd.to_datetime(j['timestamp'], unit='s', utc=True).tz_convert('Europe/Istanbul').tz_localize(None).normalize()
    d = pd.DataFrame({'o': q['open'], 'h': q['high'], 'l': q['low'], 'c': q['close'], 'adj': adj, 'v': q['volume']}, index=idx)
    d = d[~d.index.duplicated(keep='last')]
    # son barın kapanışı henüz boşsa: regularMarketPrice (18:05 sonrası kapanış seansı fiyatı; --canli ile seans içi anlık)
    rmt = pd.Timestamp(m.get('regularMarketTime', 0), unit='s', tz='UTC').tz_convert('Europe/Istanbul')
    last = d.index[-1]; note = ''
    if pd.isna(d['c'].iloc[-1]) and rmt.tz_localize(None).normalize() == last:
        if canli or (rmt.hour * 60 + rmt.minute >= 18 * 60 + 5):
            px = float(m['regularMarketPrice']); d.loc[last, ['c', 'adj']] = px
            d.loc[last, 'v'] = d['v'].iloc[-1] if pd.notna(d['v'].iloc[-1]) and d['v'].iloc[-1] > 0 else 1
            for k in ['o', 'h', 'l']:
                if pd.isna(d.loc[last, k]): d.loc[last, k] = px
            note = f' (son gün {last.date()} kapanışı = regularMarketPrice {px} @ {rmt.strftime("%H:%M")})'
    if canli and rmt.tz_localize(None).normalize() == last and pd.notna(m.get('regularMarketPrice')):
        px = float(m['regularMarketPrice']); f = d['adj'].iloc[-1] / d['c'].iloc[-1] if pd.notna(d['c'].iloc[-1]) and d['c'].iloc[-1] > 0 else 1.0
        d.loc[last, 'c'] = px; d.loc[last, 'adj'] = px * f; note = f' (CANLI: {last.date()} {rmt.strftime("%H:%M")} fiyatı {px})'
    d = d.dropna(subset=['c']); d = d[d['c'] > 0]
    return d, note

def from_csv(path):
    x = pd.read_csv(path, sep=None, engine='python')
    cols = {c.lower().strip(): c for c in x.columns}
    dc = next((cols[k] for k in ['date', 'tarih', 'time', 'datetime'] if k in cols), x.columns[0])
    pc = next((cols[k] for k in ['adj close', 'adj_close', 'adjclose', 'adj', 'düzeltilmiş', 'close', 'kapanış', 'kapanis', 'c'] if k in cols), x.columns[-1])
    s = x[pc]
    if s.dtype == object:
        s = s.astype(str).str.strip()
        s = (s.str.replace('.', '', regex=False).str.replace(',', '.', regex=False) if s.str.contains(',').any() else s).astype(float)  # 1.234,56 (TR) veya 1234.56
    ds = x[dc].astype(str).str.strip()
    iso = ds.str.match(r'^\d{4}-\d{2}-\d{2}').mean() > 0.9
    idx = pd.to_datetime(ds.str[:10] if iso else ds, format='%Y-%m-%d' if iso else None, dayfirst=not iso, errors='coerce')
    idx = pd.DatetimeIndex(idx).tz_localize(None).normalize() if getattr(idx, 'tz', None) is None else pd.DatetimeIndex(idx).tz_convert(None).normalize()
    d = pd.DataFrame({'c': s.values, 'adj': s.values, 'v': 1.0, 'h': np.nan, 'l': np.nan}, index=idx).dropna(subset=['c'])
    d = d[~d.index.duplicated(keep='last')].sort_index()
    return d, f' (CSV: {path}, sütun {pc})'

def clean_ret(d, cal):
    if d['v'].fillna(0).gt(0).mean() > 0.5:
        stale = (d['v'].fillna(0) <= 0) & (d['h'] == d['l']); d = d[~stale]
    s = d['adj'].astype(float); s = s[s > 0]
    cal = cal[cal >= s.index[0]]
    s = s.reindex(s.index.union(cal)).ffill().reindex(cal)
    r = np.log(s).diff()
    lim = pd.Series(np.where(r.index < REGIME, 0.205, 0.105), index=r.index)
    r[(np.expm1(r).abs() > lim)] = np.nan
    return r

# ------------------------------------------------------------------ sinyal ve kural
def compute(rA, rB, win=60, bwin=250):
    idx = rA.index.intersection(rB.index); rA, rB = rA.reindex(idx), rB.reindex(idx)
    braw = rA.rolling(bwin, min_periods=bwin // 2).cov(rB) / rB.rolling(bwin, min_periods=bwin // 2).var()
    beta = braw.shift(1)
    S = (rA - beta * rB).fillna(0).cumsum()
    z = (S - S.rolling(win, min_periods=win // 2).mean()) / S.rolling(win, min_periods=win // 2).std()
    return pd.DataFrame({'rA': rA, 'rB': rB, 'beta': beta, 'beta_next': braw, 'S': S, 'z': z})

def simulate(z, beta, thr=1.5, exit_z=1.5, maxN=None):
    """Araştırmadaki durum makinesi: her |z|>thr bölümüne en fazla bir giriş; çıkış side*z >= -exit_z veya maxN gün."""
    zz = z.values; bb = beta.values; n = len(zz)
    ep = np.where(np.abs(zz) > thr, np.sign(zz), 0.0); ep[np.isnan(zz)] = 0
    side = 0; last_ep = 0; k = 0; held = 0; T = []; act = 'BEKLE'
    for i in range(n):
        if ep[i] != 0 and (i == 0 or ep[i] != ep[i - 1]): k += 1
        eid = k if ep[i] != 0 else 0; act = 'BEKLE' if side == 0 else 'TUT'
        if side != 0:
            held += 1
            if (not np.isnan(zz[i]) and side * zz[i] >= -exit_z) or (maxN and held >= maxN):
                T[-1].update(exit=z.index[i], days=held); side = 0; act = 'KAPAT'
        if side == 0 and ep[i] != 0 and eid != last_ep and not np.isnan(bb[i]):
            side = int(-ep[i]); last_ep = eid; held = 0
            T.append(dict(entry=z.index[i], side=side, z_in=zz[i], beta=bb[i], exit=None, days=None))
            act = ('KAPAT + ' if act == 'KAPAT' else '') + ('AÇ LONG' if side > 0 else 'AÇ SHORT')
    return side, held, act, pd.DataFrame(T)

def trigger(S, target, win=60):
    S = S.values
    def zx(x):
        w = np.r_[S[-(win - 1):], S[-1] + x]; return (w[-1] - w.mean()) / w.std(ddof=1)
    lo, hi = (-0.6, 0.0) if target < 0 else (0.0, 0.6)
    if (zx(lo) - target) * (zx(hi) - target) > 0: return np.nan
    for _ in range(80):
        m = (lo + hi) / 2
        if (zx(m) - target) * (zx(lo) - target) <= 0: hi = m
        else: lo = m
    return (lo + hi) / 2

# ------------------------------------------------------------------ ana
def main():
    ap = argparse.ArgumentParser(description='SAHOL/AKBNK z-skoru ve VİOP spread sinyali')
    ap.add_argument('--kural', choices=['A', 'B', 'C'], default='A', help='A: |z|<=1,5 çıkış (1–5 gün) | C: 1,0 | B: 0,5 (2–3 hafta)')
    ap.add_argument('--esik', type=float, default=1.5); ap.add_argument('--pencere', type=int, default=60); ap.add_argument('--beta-pencere', type=int, default=250)
    ap.add_argument('--maxgun', type=int, default=0, help='0 = yok')
    ap.add_argument('--csv-sahol'); ap.add_argument('--csv-akbnk')
    ap.add_argument('--fa', type=float, help='F_SAHOL ön vade fiyatı (yoksa spot)'); ap.add_argument('--fb', type=float, help='F_AKBNK ön vade fiyatı (yoksa spot)')
    ap.add_argument('--sermaye', type=float, default=1_000_000); ap.add_argument('--risk', type=float, default=0.01, help='işlem başı risk (sermaye oranı)')
    ap.add_argument('--risk-birim', type=float, default=0.09, help='1 çiftin SAHOL nominaline göre varsayılan kötü durum kaybı (0,09 = tarihsel en kötü işlem; 0,03 = 5. yüzdelik)')
    ap.add_argument('--teminat-a', type=float, default=0.14); ap.add_argument('--teminat-b', type=float, default=0.15)
    ap.add_argument('--pozisyon', choices=['yok', 'long', 'short'], default=None, help='elinizdeki spread pozisyonu (çıkış kontrolü için)')
    ap.add_argument('--canli', action='store_true', help='seans içi anlık fiyatla tahmini z (karar için kapanışı bekleyin)')
    a = ap.parse_args()
    if a.csv_sahol and a.csv_akbnk:
        dA, nA = from_csv(a.csv_sahol); dB, nB = from_csv(a.csv_akbnk); cal = dA.index.union(dB.index)
    else:
        dA, nA = yahoo('SAHOL.IS', a.canli); dB, nB = yahoo('AKBNK.IS', a.canli)
        try:
            dX, _ = yahoo('XU100.IS', a.canli); cal = dX.index[dX['v'].fillna(0) > 0]
            if len(cal) < 0.9 * len(dA): cal = dX.index
            cal = cal.union(dA.index[-1:]).union(dB.index[-1:])
        except SystemExit:
            cal = dA.index.union(dB.index)
    rA, rB = clean_ret(dA, cal), clean_ret(dB, cal)
    K = compute(rA, rB, a.pencere, a.beta_pencere)
    t = K.index[-1]; z = K.z.iloc[-1]; b = K.beta.iloc[-1]; bn = K.beta_next.iloc[-1]
    pa, pb = dA['c'].reindex(K.index).ffill().iloc[-1], dB['c'].reindex(K.index).ffill().iloc[-1]
    fa, fb = (a.fa or pa), (a.fb or pb)
    exit_z = RULES[a.kural]
    side, held, act, T = simulate(K.z, K.beta, a.esik, exit_z, a.maxgun or None)
    print('=' * 78)
    print(f'SAHOL/AKBNK z-skoru  |  veri son günü: {t.date()}  |  Kural {a.kural} (giriş |z|>{a.esik}, çıkış |z|<={exit_z}{", max " + str(a.maxgun) + " gün" if a.maxgun else ""})')
    print(f'Kaynak: SAHOL{nA}; AKBNK{nB}')
    if t.normalize() < pd.Timestamp(dt.date.today()) - pd.Timedelta(days=4): print('UYARI: veri 4 günden eski görünüyor.')
    print('-' * 78)
    tab = pd.DataFrame({'SAHOL': dA['c'].reindex(K.index).ffill(), 'AKBNK': dB['c'].reindex(K.index).ffill(), 'β': K.beta, 'z': K.z}).tail(8)
    print(tab.round({'SAHOL': 2, 'AKBNK': 2, 'β': 3, 'z': 2}).to_string())
    print('-' * 78)
    print(f'BUGÜN z = {z:+.2f}   (giriş bandı ±{a.esik}, çıkış bandı ±{exit_z})')
    if z > a.esik: sig = 'z > +eşik  -> SHORT spread bölgesi: SAHOL SAT, AKBNK AL'
    elif z < -a.esik: sig = 'z < −eşik  -> LONG spread bölgesi: SAHOL AL, AKBNK SAT'
    else: sig = 'bant içinde -> yeni giriş yok'
    print('Sinyal bölgesi :', sig)
    print(f'Model durumu   : {"LONG" if side > 0 else "SHORT" if side < 0 else "POZİSYON YOK"}' + (f' ({held} gündür, giriş {T.iloc[-1].entry.date()} z={T.iloc[-1].z_in:+.2f}, β={T.iloc[-1].beta:.3f})' if side else ''))
    print(f'BUGÜNKÜ EYLEM  : {act}' + ('  (aynı akşam VİOP uzlaşma penceresinde)' if act not in ('BEKLE', 'TUT') else ''))
    if a.pozisyon in ('long', 'short'):
        sd = 1 if a.pozisyon == 'long' else -1
        print(f'Sizin pozisyon : {a.pozisyon.upper()} -> ' + ('ÇIKIŞ koşulu SAĞLANDI, kapatın' if sd * z >= -exit_z else f'tutun (çıkış: z {">=" if sd > 0 else "<="} {-sd * exit_z:+.1f})'))
    bh = T.iloc[-1].beta if side else b
    ratio = bh * fa / fb
    print('-' * 78)
    print(f'Hedge oranı β (bugün işlem açılırsa) = {b:.3f}   | yarın kullanılacak β = {bn:.3f}')
    print(f'Kontrat oranı N_AKBNK/N_SAHOL = β·F_SAHOL/F_AKBNK = {b:.3f}·{fa:.2f}/{fb:.2f} = {b * fa / fb:.3f}' + ('' if a.fa and a.fb else '  (spot fiyatla; vadeli fiyatını --fa/--fb ile verin)'))
    if np.isnan(b) or np.isnan(z): raise SystemExit('β veya z hesaplanamadı (veri yetersiz/hatalı tarih).')
    na_ = int(np.floor(a.sermaye * a.risk / (a.risk_birim * fa * 100))); nb_ = int(round(na_ * b * fa / fb))
    nomA, nomB = na_ * fa * 100, nb_ * fb * 100; mar = a.teminat_a * nomA + a.teminat_b * nomB
    print(f'Boyut (sermaye {a.sermaye:,.0f} TL, risk %{100 * a.risk:.1f}, kötü durum %{100 * a.risk_birim:.0f}): {na_} SAHOL + {nb_} AKBNK kontratı (1 kontrat = 100 pay)')
    print(f'   nominal {nomA:,.0f} + {nomB:,.0f} TL ; başlangıç teminatı ≈ {mar:,.0f} TL (SAHOL %{100 * a.teminat_a:.0f}, AKBNK %{100 * a.teminat_b:.0f}; aracı kurumla teyit edin)')
    print('-' * 78)
    print('Yarın kapanışta tetik seviyeleri (diğer hisse sabitken):')
    for tg in sorted({a.esik, -a.esik, exit_z, -exit_z}, reverse=True):
        x = trigger(K.S, tg, a.pencere)
        if np.isnan(x): continue
        print(f'   z = {tg:+.1f}: spread {100 * x:+.2f}%  -> SAHOL {pa * np.exp(x):.2f} TL (AKBNK {pb:.2f})  veya  AKBNK {pb * np.exp(-x / bn):.2f} TL (SAHOL {pa:.2f})')
    if len(T):
        L = T.tail(5).copy(); L['side'] = L.side.map({1: 'LONG', -1: 'SHORT'})
        print('Modelin son işlemleri:'); print(L[['entry', 'exit', 'side', 'z_in', 'days']].to_string(index=False))
    print('=' * 78)

if __name__ == '__main__':
    main()
