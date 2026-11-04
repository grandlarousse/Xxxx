#!/usr/bin/env python3
"""Koza göreli momentum — günlük sinyal betiği (strateji B: TRMET artığı, TRMET1! / TRALT1! çifti).

Yalnız pandas, numpy, requests kullanır. Veri: Yahoo Finance v8 "chart" uç noktası (günlük, temettü+bölünme düzeltmeli 'adjclose').

KURAL (araştırma c2_koza.py ile birebir aynı sinyal):
  r      = günlük log getiri (bayat gün: hacim<=0 ya da yüksek==düşük -> fiyat yok sayılır; getiri son geçerli fiyata göre;
           |r| > günlük limit (+%10,5 / −%10,5; 13.03.2020 öncesi %20,5) -> veri hatası, NaN)
  grp    = ort(r_TRALT, r_TRENJ)          (biri eksikse NaN)
  β_g    = 250g cov(r_TRMET, grp)/var(grp), en az 120 gözlem, BİR GÜN ÖNCESİNE kadar (shift 1), [0,2; 2,0] kırpılır
  u      = r_TRMET − β_g·grp
  z3     = (u_t + u_t−1 + u_t−2) / (std60(u)·√3)    (std60 en az 40 gözlem)
  β_TA   = 250g β(r_TRMET, r_TRALT), shift 1, [0,3; 2,0]
  z3 > +1,5 -> TRMET1! AL + β_TA oranında TRALT1! SAT ; z3 < −1,5 -> TRMET1! SAT + TRALT1! AL
PRATİK KURAL (REHBER_koza.md): ilk sinyal gününde gir (uzlaşma), 2 iş günü sonra uzlaşmada çık; çıkış gününde sinyal aynı yönde
  hâlâ aktifse 2 gün uzat (toplam en fazla 6 gün); ters sinyal varsa çevir; vadeli limitte kilitliyse o gün girme.
Takvim: dört BIST serisinin (TRMET, TRALT, TRENJ, XU030) Yahoo tarihlerinin birleşimi; BIST tatilleri doğal olarak yok;
  bir hissede bar yoksa o gün o hissenin getirisi NaN (araştırmayla aynı). Yabancı piyasa sembolü kullanılmaz -> ABD tatili hizalaması gerekmez.

Kullanım:
  python3 sinyal_koza.py                          # son tamamlanmış kapanışa göre
  python3 sinyal_koza.py --sermaye 1000000 --risk 0.0075
  python3 sinyal_koza.py --canli TRMET=101.5 TRALT=35.10 TRENJ=74.20   # 17:50–17:55'te aracı kurum ekranındaki CANLI fiyatlarla
  python3 sinyal_koza.py --ters                   # TERS kural (TRALT artığı; TRALT1! − β·TRMET1!) — yalnız bilgi
"""
import argparse, sys, time, datetime as dt
import numpy as np, pandas as pd, requests

SYMS = ['TRMET', 'TRALT', 'TRENJ', 'XU030']
REG = pd.Timestamp('2020-03-13')  # ±%10 limit rejimi başlangıcı
THR = 1.5
SIGMA_TRADE = 0.0205  # pratik kural (P0L) işlem başı brüt getiri std'si ≈ %2,05 (2019–2026 backtest)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
CUTOFF_MIN = 18 * 60 + 30  # bugünün Yahoo barı bu saatten (TSİ) önce tamamlanmamış sayılır


def trfloat(x):
    """'0,0075' ya da '1.000.000' gibi Türkçe yazımı da kabul eder (DENETİM: argparse float virgülü reddediyordu)."""
    x = str(x).strip()
    if ',' in x: x = x.replace('.', '').replace(',', '.')
    elif x.count('.') > 1: x = x.replace('.', '')
    return float(x)


def tsi_now():
    return pd.Timestamp.now(tz='Europe/Istanbul')


def fetch(sym, retries=5):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}.IS'
    params = {'period1': 946684800, 'period2': int(time.time()) + 86400, 'interval': '1d', 'includePrePost': 'false', 'events': 'div,splits'}
    last = None
    for a in range(retries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=40)
            if r.status_code == 200:
                res = r.json()['chart']['result'][0]; break
            last = f'HTTP {r.status_code}'
        except Exception as e:  # ağ hatası
            last = str(e)
        time.sleep(2 ** a)
    else:
        raise SystemExit(f'{sym}: Yahoo verisi alınamadı ({last})')
    q = res['indicators']['quote'][0]; adj = res['indicators'].get('adjclose', [{}])[0].get('adjclose') or q['close']
    idx = pd.to_datetime(res['timestamp'], unit='s', utc=True)
    df = pd.DataFrame({'o': q['open'], 'h': q['high'], 'l': q['low'], 'c': q['close'], 'adj': adj, 'v': q['volume']}, index=idx)
    df['ldate'] = idx.tz_convert('Europe/Istanbul').tz_localize(None).normalize()
    m = res['meta']
    # bugünün barı: Yahoo BIST verisi ~15 dk GECİKMELİ (denetim: 12:41'de regularMarketTime 12:25). Kapanış seansı ~18:05'te
    # biter; 18:30 TSİ öncesi bugünün barı tamamlanmamış sayılır -> atılır (DENETİM DÜZELTMESİ: eski sınır 18:15 idi, 18:15–18:20
    # arasında Yahoo barı kapanış öncesi fiyatı gösterebiliyordu). Sonrasında kapanış NaN ise regularMarketPrice ile tamamla.
    now = tsi_now(); today = pd.Timestamp(now.date())
    rmt = pd.Timestamp(m.get('regularMarketTime', 0), unit='s', tz='UTC').tz_convert('Europe/Istanbul')
    if now.hour * 60 + now.minute < CUTOFF_MIN:
        df = df[df.ldate < today]
    else:
        k = df.ldate == today
        if k.any() and pd.isna(df.loc[k, 'c']).all() and rmt.normalize().tz_localize(None) == today:
            df.loc[k, ['c', 'adj']] = m.get('regularMarketPrice')
        if k.any() and rmt.normalize().tz_localize(None) == today and rmt.hour * 60 + rmt.minute < 18 * 60 + 5:
            print(f'  UYARI {sym}: Yahoo son fiyat zamanı {rmt:%H:%M} (< 18:05) -> bugünün barı kapanış seansını içermeyebilir; '
                  f'birkaç dakika sonra yeniden çalıştırın.', file=sys.stderr)
    df = df.dropna(subset=['c'])
    df = df[~df.ldate.duplicated(keep='last')].set_index('ldate')
    return df, m


def spot_ret(df, sym):
    d = df.copy()
    if not sym.startswith('XU'):
        st = (d.v <= 0) | (d.h == d.l)
        d.loc[st, ['c', 'adj']] = np.nan
    a = d['adj']
    r = np.log(a / a.ffill().shift(1)).where(a.notna())
    pre = r.index < REG
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    if not sym.startswith('XU'):
        r = r.mask((r > up) | (r < dn))
    return r


def beta(y, x, w=250, mp=120):
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)


def signal(R, target='TRMET'):
    R = R[SYMS].dropna(how='all')
    y, hedge = (R.TRMET, R.TRALT) if target == 'TRMET' else (R.TRALT, R.TRMET)
    grp = pd.concat([hedge, R.TRENJ], axis=1).mean(axis=1, skipna=False)
    b_g = beta(y, grp).clip(0.2, 2.0)
    u = y - b_g * grp
    sd60 = u.rolling(60, min_periods=40).std()
    z3 = u.rolling(3, min_periods=3).sum() / (sd60 * np.sqrt(3))
    bH = beta(y, hedge).clip(0.3, 2.0)
    return pd.DataFrame({'r_y': y, 'r_h': hedge, 'r_e': R.TRENJ, 'grp': grp, 'b_g': b_g, 'u': u, 'sd60': sd60, 'z3': z3, 'bH': bH})


def replay(S, R, ndays=400):
    """Pratik kuralı son ndays günde oynatır (VİOP kilidi yerine spot ±%9,5 vekili). Döner: işlem listesi ve açık pozisyon."""
    S = S.iloc[-ndays:]
    z = S.z3.values; act = np.where(np.isfinite(z) & (np.abs(z) > THR), np.sign(z), 0.0)
    rr = R.reindex(S.index)
    lock = ((rr.TRMET.abs() > np.log(1.095)) | (rr.TRALT.abs() > np.log(1.095))).values
    trades, pos, block = [], None, 0.0
    for i in range(len(S)):
        if pos is not None and i == pos['exit']:
            if act[i] == pos['s'] and pos['exit'] - pos['i0'] + 2 <= 6:
                pos['exit'] += 2; pos['ext'] += 1
                continue
            pos['out'] = i; trades.append(pos); block = pos['s'] if act[i] == pos['s'] else 0.0; pos = None
        if pos is None:
            if block and act[i] != block: block = 0.0
            if act[i] != 0 and act[i] != block and not lock[i]:
                pos = dict(i0=i, s=act[i], exit=i + 2, ext=0, b=S.bH.values[i], z=z[i])
    return S.index, trades, pos


def main():
    ap = argparse.ArgumentParser(description='Koza göreli momentum günlük sinyali')
    ap.add_argument('--sermaye', type=trfloat, default=1_000_000, help='Sermaye (TL), varsayılan 1.000.000')
    ap.add_argument('--risk', type=trfloat, default=0.0075, help='İşlem başı risk payı (0,005–0,01), varsayılan 0,0075')
    ap.add_argument('--kaldirac', type=trfloat, default=1.0, help='Brüt nominal / sermaye üst sınırı, varsayılan 1,0')
    ap.add_argument('--canli', nargs='*', default=None, help='Bugünün CANLI fiyatları: TRMET=.. TRALT=.. TRENJ=.. (17:50–17:55)')
    ap.add_argument('--ters', action='store_true', help='TERS kural (TRALT artığı) — yalnız bilgi')
    ap.add_argument('--vadeli', nargs='*', default=None, help='Boyut için vadeli fiyatları: TRMET=.. TRALT=.. (yoksa spot kapanış kullanılır)')
    ap.add_argument('--gecmis', type=int, default=8, help='Yazdırılacak son gün sayısı')
    a = ap.parse_args()
    now = tsi_now()
    D, META = {}, {}
    for s in SYMS:
        D[s], META[s] = fetch(s); time.sleep(0.3)
    print(f'Koza göreli momentum sinyali — çalıştırma {now:%Y-%m-%d %H:%M} TSİ')
    print('Kaynak: Yahoo Finance v8 chart (günlük, adjclose). Son tamamlanmış barlar:')
    for s in SYMS:
        print(f'  {s:6s} son tarih {D[s].index.max().date()}  kapanış {D[s].c.iloc[-1]:,.2f}  (Yahoo regularMarketPrice {META[s].get("regularMarketPrice")}, '
              f'zaman {pd.Timestamp(META[s].get("regularMarketTime", 0), unit="s", tz="UTC").tz_convert("Europe/Istanbul"):%Y-%m-%d %H:%M})')
    lastd = {s: D[s].index.max() for s in ['TRMET', 'TRALT', 'TRENJ']}
    if len(set(lastd.values())) > 1 and not a.canli:
        print(f'  UYARI: hisselerin son Yahoo tarihleri farklı {dict((k, str(v.date())) for k, v in lastd.items())} -> Yahoo bir seriyi geç '
              f'güncellemiş olabilir; son gün z3 NaN çıkar. 30 dk sonra yeniden çalıştırın ya da --canli ile fiyat girin.')
    live = {}
    if a.canli:
        for kv in a.canli:
            k, v = kv.split('='); live[k.upper()] = float(v.replace(',', '.'))
        miss = [s for s in ['TRMET', 'TRALT', 'TRENJ'] if s not in live]
        if miss: raise SystemExit(f'--canli eksik: {miss}')
        today = pd.Timestamp(now.date())
        for s in ['TRMET', 'TRALT', 'TRENJ']:
            df = D[s]
            if df.index.max() >= today: df = df[df.index < today]
            last = df.iloc[-1]; px = live[s]
            row = pd.DataFrame({'o': px, 'h': px * 1.0001, 'l': px, 'c': px, 'adj': last.adj * px / last.c, 'v': 1.0}, index=[today])
            D[s] = pd.concat([df, row])
        print(f'  CANLI fiyatlar bugüne ({today.date()}) eklendi: {live}  -> sinyal "17:50–17:55 fiyatıyla" yaklaşık; uzlaşmada kesinleşmez.')
    R = pd.DataFrame({s: spot_ret(D[s], s) for s in SYMS})
    tgt = 'TRALT' if a.ters else 'TRMET'; hed = 'TRMET' if a.ters else 'TRALT'
    S = signal(R, tgt).dropna(subset=['z3', 'bH'], how='all')
    L = S.iloc[-1]; t = S.index[-1]
    print(f'\nKural: {"TERS — TRALT artığı (bilgi amaçlı)" if a.ters else "ANA — TRMET artığı"}; sinyal tarihi {t.date()}')
    print(f'  u_t {L.u * 1e4:+.0f} bps | Σ3u {S.u.iloc[-3:].sum() * 1e4:+.0f} bps | σ60 {L.sd60 * 1e4:.0f} bps | z3 = {L.z3:+.2f} (eşik ±{THR})')
    print(f'  β_g {L.b_g:.2f} | β_{tgt}–{hed} (hedge) {L.bH:.2f}')
    if not np.isfinite(L.z3):
        print('  z3 hesaplanamadı (eksik/bayat veri ya da limit üstü getiri) -> SİNYAL YOK'); sig = 0
    else:
        sig = int(np.sign(L.z3)) if abs(L.z3) > THR else 0
    if sig > 0:
        yon = f'{tgt}1! AL + {hed}1! SAT (β={L.bH:.2f})'
    elif sig < 0:
        yon = f'{tgt}1! SAT + {hed}1! AL (β={L.bH:.2f})'
    else:
        yon = 'YOK'
    print(f'  SİNYAL: {yon}')
    # kontrat sayısı
    PM, PH = D[tgt].c.iloc[-1], D[hed].c.iloc[-1]
    PM_spot = PM  # DENETİM DÜZELTMESİ: tetik fiyatı her zaman SPOT kapanışa göre (eskiden --vadeli verilince vadeli fiyatı kullanılıyordu)
    fsrc = 'spot kapanış (vadeli fiyatını --vadeli ile verin)'
    if a.vadeli:
        vf = {k.upper(): float(v.replace(',', '.')) for k, v in (kv.split('=') for kv in a.vadeli)}
        PM, PH = vf.get(tgt, PM), vf.get(hed, PH); fsrc = 'vadeli fiyatları (--vadeli)'
    G = min(a.sermaye * a.risk / SIGMA_TRADE, a.sermaye * a.kaldirac)
    nM = max(int(round(G / (1 + L.bH) / (100 * PM))), 1); nH = int(round(L.bH * nM * PM / PH))
    notM, notH = nM * 100 * PM, nH * 100 * PH
    print(f'\nBoyut (sermaye {a.sermaye:,.0f} TL, risk %{a.risk * 100:.2f}, işlem σ≈%{SIGMA_TRADE * 100:.2f}): hedef brüt nominal {G:,.0f} TL')
    print(f'  {nM} x {tgt}1!  (~{notM:,.0f} TL)  ve  {nH} x {hed}1!  (~{notH:,.0f} TL)  -> oran 1 : {L.bH * PM / PH:.2f} ; '
          f'gerçekleşen nominal oranı {notH / notM:.2f}')
    print(f'  Teminat kaba tahmin (%15, iki bacak, netleştirme yok): {0.15 * (notM + notH):,.0f} TL. Fiyat kaynağı: {fsrc}.')
    # bir sonraki kapanış için tetik
    sd = L.sd60; s2 = S.u.iloc[-2:].sum()
    up = THR * sd * np.sqrt(3) - s2; dn = -THR * sd * np.sqrt(3) - s2
    print(f'\nBir sonraki kapanış için yaklaşık tetik (σ60 sabit varsayımı): yarının artığı u = r_{tgt} − {L.b_g:.2f}·ort(r_{hed}, r_TRENJ)')
    print(f'  z3 > +{THR} için u ≥ {up * 1e4:+.0f} bps ; z3 < −{THR} için u ≤ {dn * 1e4:+.0f} bps')
    print(f'  {hed} ve TRENJ yatay kalırsa {tgt} SPOT kapanışı: AL tetiği ≥ {PM_spot * np.exp(up):,.2f} ; SAT tetiği ≤ {PM_spot * np.exp(dn):,.2f} '
          f'(son spot fiyat {PM_spot:,.2f})')
    # kural geçmişi
    idx, trades, pos = replay(S, R)
    print('\nPratik kuralın son işlemleri (spot verisiyle yeniden oynatma; VİOP kilidi için spot ±%9,5 vekili):')
    for p in trades[-4:]:
        print(f'  giriş {idx[p["i0"]].date()} yön {"+" if p["s"] > 0 else "−"}{tgt[:3]} z {p["z"]:+.2f} β {p["b"]:.2f} -> çıkış {idx[p["out"]].date()} '
              f'({p["out"] - p["i0"]} gün, uzatma {p["ext"]})')
    if pos is not None:
        ex = pos['exit']; exd = idx[ex].date() if ex < len(idx) else f'{ex - len(idx) + 1}. sonraki iş günü'
        print(f'  AÇIK POZİSYON: giriş {idx[pos["i0"]].date()} yön {"TRMET AL / TRALT SAT" if pos["s"] > 0 else "TRMET SAT / TRALT AL"} '
              f'(β {pos["b"]:.2f}); planlanan çıkış uzlaşması: {exd}; çıkış günü sinyal aynı yöndeyse 2 gün uzat (≤6 gün)')
    else:
        print('  Açık pozisyon YOK (kurala göre).')
    print(f'\nSon {a.gecmis} gün:')
    T = S.iloc[-a.gecmis:][['r_y', 'r_h', 'r_e', 'u', 'z3', 'b_g', 'bH']].copy()
    T[['r_y', 'r_h', 'r_e', 'u']] *= 1e4
    T.columns = [f'r_{tgt}', f'r_{hed}', 'r_TRENJ', 'u(bps)', 'z3', 'β_g', 'β_hedge']
    print(T.round(2).to_string())
    print('\nUYARI: araştırma sinyali kapanış verisiyle; --canli ile 17:50–17:55 fiyatı kullanıldığında sinyal günlerinin %94–100\'ü aynı çıktı '
          '(2025-11 → 2026-11), tam geçmiş benzetimde işlem başı ≈ −4 bps fark. Yatırım tavsiyesi değildir.')


if __name__ == '__main__':
    main()
