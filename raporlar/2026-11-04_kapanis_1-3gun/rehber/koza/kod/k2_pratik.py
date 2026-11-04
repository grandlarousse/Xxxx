"""(2) PRATİK, ÖRTÜŞMESİZ kuralın backtest'i — VİOP uzlaşma fiyatlarıyla (ortak panel + 02–03.11.2026 bültenleri).
Kural (P0, ana): t günü kapanış verisiyle z3 hesaplanır. Pozisyon yokken |z3|>1,5 -> yön(z3) ile
  TRMET1! AL + β_TA·TRALT1! SAT (z3>0) ya da tersi; giriş t uzlaşması. Planlanan çıkış t+2 uzlaşması.
  Çıkış gününde sinyal AYNI yönde hâlâ aktifse 2 gün uzat (toplam en fazla 6 gün). Aksi halde çık.
  Çıkış gününde TERS yönde sinyal varsa aynı uzlaşmada ters pozisyon açılır. 6 gün dolup sinyal hâlâ aynı yöndeyse çıkılır
  ve aynı yöne yeniden giriş için sinyalin önce bant içine dönmesi beklenir. Pozisyondayken ara günlerdeki sinyaller yok sayılır.
  Vade: giriş/uzatma anında vadesi planlanan çıkıştan SONRA olan en yakın vade (curlib.choose); uzatmada vade değişirse devir (ek maliyet).
Varyantlar: P1 sabit h2 (uzatmasız); P0L limit kilidi günü giriş yok; P2 gecikmeli (dünkü kapanışın sinyali, bugün uzlaşmada giriş);
  TERS (TRALT artığı, TRALT1! − β·TRMET1!)."""
import numpy as np, pandas as pd, json
import kl
from kl import C
cal = kl.use_ext_panel()
R = pd.DataFrame({s: kl.spot_ret_fresh(s) for s in ['TRMET', 'TRALT', 'TRENJ', 'XU030']})
SIG = kl.koza_signal(R, 'TRMET'); SIGA = kl.koza_signal(R, 'TRALT')
# --- araştırma z3 ile uyum ---
Z0 = pd.read_parquet(kl.DL + '/z3_arastirma.parquet')
cm = Z0.z3.dropna().index.intersection(SIG.z3.dropna().index)
dz = (Z0.z3.reindex(cm) - SIG.z3.reindex(cm)).abs()
print(f'Taze Yahoo z3 ile araştırma z3 farkı: ortak gün {len(cm)}, maks |fark| {dz.max():.2e}, sinyal uyumu '
      f'{((Z0.z3.reindex(cm).abs() > 1.5) == (SIG.z3.reindex(cm).abs() > 1.5)).mean():.4f}')
print('VİOP takvimi', cal.min().date(), '→', cal.max().date(), '| spot son', R.dropna(how="all").index.max().date())
lockM = kl.lock_series('TRMET', cal); lockA = kl.lock_series('TRALT', cal); LOCK = (lockM | lockA).values
FM, FA = C.fut('TRMET'), C.fut('TRALT')
n = len(cal)


def simulate(sig, legs=('TRMET', 'TRALT'), thr=1.5, h=2, maxh=6, extend=True, lag=0, lock=False):
    z = sig.z3.reindex(cal).values; bH = sig.bH.reindex(cal).fillna(1.0).values
    if lag:
        z = np.r_[np.full(lag, np.nan), z[:-lag]]; bH = np.r_[np.full(lag, 1.0), bH[:-lag]]
    F1, F2 = C.fut(legs[0]), C.fut(legs[1])
    act = np.where(np.isfinite(z) & (np.abs(z) > thr), np.sign(z), 0.0)
    trades = []; pos = None; block = 0.0
    for i in range(n):
        if pos is not None and i == pos['exit']:
            held = pos['exit'] - pos['i0']
            if extend and act[i] == pos['s'] and held + h <= maxh and i + h < n:
                pos['segs'].append(i); pos['exit'] = i + h; continue
            pos['capped'] = bool(act[i] == pos['s']); trades.append(pos); block = pos['s'] if pos['capped'] else 0.0; pos = None
        if pos is None:
            if block and act[i] != block: block = 0.0
            if act[i] != 0 and act[i] != block and i + h < n and not (lock and LOCK[i]):
                pos = dict(i0=i, s=act[i], b=bH[i], segs=[i], exit=i + h, z=z[i])
    if pos is not None: pos['open'] = True; trades.append(pos)
    rows = []
    for p in trades:
        if p.get('open'): continue
        segs = np.array(p['segs']); d = cal[segs]
        r1 = F1.fwd(d, h, 'E0'); r2 = F2.fwd(d, h, 'E0')
        j1 = F1.choose(segs, h); j2 = F2.choose(segs, h)
        rolls = int((np.diff(j1) != 0).sum() + (np.diff(j2) != 0).sum() > 0) if len(segs) > 1 else 0
        nroll = int(max((np.diff(j1) != 0).sum(), (np.diff(j2) != 0).sum())) if len(segs) > 1 else 0
        b = p['b']; x = p['s'] * (np.sum(r1) - b * np.sum(r2)) / (1 + b)
        P1 = F1.ST.values[p['i0'], j1[0]] if j1[0] >= 0 else np.nan; P2 = F2.ST.values[p['i0'], j2[0]] if j2[0] >= 0 else np.nan
        tick = 2 * (1 / (1 + b) * 0.01 / P1 + b / (1 + b) * 0.01 / P2) * 1e4  # 1 tik/bacak/yön, brüt sermaye başına bps
        rows.append(dict(entry=cal[p['i0']], exit=cal[p['exit']], days=p['exit'] - p['i0'], side=p['s'], beta=b, z=p['z'],
                         gross=x * 1e4, nroll=nroll, tick=tick * (1 + nroll), capped=p.get('capped', False),
                         lock_entry=bool(LOCK[p['i0']]), P1=P1, P2=P2))
    T = pd.DataFrame(rows)
    T['cost8'] = 8 * (1 + T.nroll); T['cost15'] = 15 * (1 + T.nroll)
    T['net8'] = T.gross - T.cost8; T['net15'] = T.gross - T.cost15
    T['net8t'] = T.net8 - T.tick; T['net15t'] = T.net15 - T.tick
    return T


def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return (x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def mdd(x):
    c = np.cumsum(np.nan_to_num(x)); return float((c - np.maximum.accumulate(np.r_[0, c])[1:]).min())


def report(name, T, extra=''):
    T = T.dropna(subset=['gross']).copy()
    yrs = (T.entry.max() - T.entry.min()).days / 365.25
    o = dict(name=name, n=len(T), per_yr=len(T) / yrs, days=T.days.mean(), gross=T.gross.mean(), t=tstat(T.gross), hit=(T.gross > 0).mean(),
             net8=T.net8.mean(), net15=T.net15.mean(), net8t=T.net8t.mean(), net15t=T.net15t.mean(), tick=T.tick.mean(), rolls=int(T.nroll.sum()),
             sd=T.gross.std(), worst=T.gross.min(), worst_d=str(T.loc[T.gross.idxmin(), 'entry'].date()), best=T.gross.max(),
             mdd15t=mdd(T.net15t.values), mdd8=mdd(T.net8.values), ext=(T.days > 2).mean(), capped=int(T.capped.sum()),
             time_in=T.days.sum() / len(cal[(cal >= T.entry.min()) & (cal <= T.exit.max())]))
    for lab, a, b in [('IS', '2017-01-01', '2021-12-31'), ('OOS', '2022-01-01', '2026-12-31'), ('y2426', '2024-01-01', '2026-12-31'),
                      ('y1719', '2017-01-01', '2019-12-31'), ('y2021', '2020-01-01', '2021-12-31'), ('y2223', '2022-01-01', '2023-12-31')]:
        m = (T.entry >= a) & (T.entry <= b); o[lab] = T.gross[m].mean(); o[lab + '_t'] = tstat(T.gross[m]); o[lab + '_n'] = int(m.sum())
        o[lab + '_net15t'] = T.net15t[m].mean()
    k = T.gross.sort_values(ascending=False).index[10:]; o['ex10'] = T.gross[k].mean(); o['ex10_t'] = tstat(T.gross[k])
    yy = T.groupby(T.entry.dt.year).agg(m=('gross', 'mean'), k=('gross', 'size'), n15=('net15t', 'mean'))
    o['by_year'] = ' '.join(f'{y % 100:02d}:{r.m:+.0f}(n{r.k})' for y, r in yy.iterrows())
    o['yrs_pos'] = f'{(yy.m > 0).sum()}/{len(yy)}'
    print(f"\n== {name} {extra}\n n={o['n']} ({o['per_yr']:.1f}/yıl), ort. tutma {o['days']:.2f} gün, uzatılan %{100 * o['ext']:.0f}, 6g sınırı {o['capped']}, "
          f"piyasada zaman %{100 * o['time_in']:.0f}, vade devri {o['rolls']}\n brüt {o['gross']:+.1f} bps (t {o['t']:.2f}), isabet {o['hit']:.2f}, σ {o['sd']:.0f} | "
          f"net8 {o['net8']:+.1f}, net15 {o['net15']:+.1f}, tik ort {o['tick']:.1f} -> net8+tik {o['net8t']:+.1f}, net15+tik {o['net15t']:+.1f}\n"
          f" IS(17–21) {o['IS']:+.1f} (t {o['IS_t']:.2f}, n {o['IS_n']}) | OOS(22–26) {o['OOS']:+.1f} (t {o['OOS_t']:.2f}, n {o['OOS_n']}) | "
          f"2024–26 {o['y2426']:+.1f} (t {o['y2426_t']:.2f}, n {o['y2426_n']}; net15+tik {o['y2426_net15t']:+.1f})\n"
          f" 17–19 {o['y1719']:+.1f} (t {o['y1719_t']:.2f}) | 20–21 {o['y2021']:+.1f} (t {o['y2021_t']:.2f}) | 22–23 {o['y2223']:+.1f} (t {o['y2223_t']:.2f})\n"
          f" en iyi 10 hariç {o['ex10']:+.1f} (t {o['ex10_t']:.2f}) | en kötü {o['worst']:+.0f} ({o['worst_d']}), en iyi {o['best']:+.0f} | "
          f"maks düşüş (işlem toplamı) net8 {o['mdd8']:.0f} bps, net15+tik {o['mdd15t']:.0f} bps\n yıllar: {o['by_year']} (pozitif {o['yrs_pos']})")
    return o


RES = []
T0 = simulate(SIG); RES.append(report('P0 ANA: ilk sinyal, h2, aynı yönde uzat (≤6g), E0 uzlaşma', T0))
T0L = simulate(SIG, lock=True); RES.append(report('P0L: P0 + kilitli günde giriş yok', T0L))
T1 = simulate(SIG, extend=False); RES.append(report('P1: örtüşmesiz sabit h2 (uzatmasız)', T1))
T1b = simulate(SIG, h=3, extend=False); RES.append(report('P1b: örtüşmesiz sabit h3 (bilgi)', T1b))
T2 = simulate(SIG, lag=1); RES.append(report('P2 GECİKMELİ: dünkü kapanış sinyali, bugün uzlaşmada giriş (uzatmalı)', T2))
T2b = simulate(SIG, lag=1, extend=False); RES.append(report('P2b: gecikmeli, sabit h2', T2b))
TA = simulate(SIGA, legs=('TRALT', 'TRMET')); RES.append(report('TERS P0: TRALT artığı, TRALT1! − β·TRMET1! (uzatmalı)', TA))
TAb = simulate(SIGA, legs=('TRALT', 'TRMET'), extend=False); RES.append(report('TERS P1: sabit h2', TAb))
TA2 = simulate(SIGA, legs=('TRALT', 'TRMET'), lag=1); RES.append(report('TERS P2: gecikmeli', TA2))
# eşik duyarlılığı (yalnız bilgi, seçim için değil)
for thr in [1.25, 1.75, 2.0]:
    RES.append(report(f'P0 eşik {thr} (bilgi)', simulate(SIG, thr=thr)))
pd.DataFrame(RES).to_csv(kl.OUT + '/kod/res_pratik.csv', index=False)
for nm, T in [('P0', T0), ('P0L', T0L), ('P1', T1), ('P2', T2), ('TERS', TA)]:
    T.to_csv(kl.OUT + f'/kod/islemler_{nm}.csv', index=False)
# güncel fiyatlarla 1 çift: 1 TRMET + round(β·P_M/P_A) TRALT
last = SIG.dropna(subset=['bH']).iloc[-1]
PM = FM.front_series('settle', 2)[0].dropna().iloc[-1]; PA = FA.front_series('settle', 2)[0].dropna().iloc[-1]
nA = int(round(last.bH * PM / PA)); G = 100 * PM + nA * 100 * PA
print(f'\nGüncel: β_TA {last.bH:.3f}, TRMET1! {PM:.2f}, TRALT1! {PA:.2f} -> 1 çift = 1 TRMET + {nA} TRALT, brüt nominal {G:,.0f} TL '
      f'(gerçek oran {nA * PA / PM:.2f})')
for o in RES[:3] + [RES[4], RES[6]]:
    print(f"  {o['name'][:40]:40s}: işlem başı brüt {o['gross'] * G / 1e4:+.0f} TL, net15+tik {o['net15t'] * G / 1e4:+.0f} TL / çift; "
          f"yılda {o['per_yr']:.1f} işlem -> yıllık ≈ {o['net15t'] * o['per_yr'] * G / 1e4:+.0f} TL / çift")
json.dump(dict(G=G, nA=nA, PM=PM, PA=PA, bTA=float(last.bH)), open(kl.OUT + '/kod/cift.json', 'w'))
# P0 işlem listesi: en kötü 5 / en iyi 5 / son 8
pd.set_option('display.width', 200)
c = ['entry', 'exit', 'days', 'side', 'beta', 'z', 'gross', 'net15t', 'nroll']
print('\nP0 en kötü 5:\n', T0.nsmallest(5, 'gross')[c].round(2).to_string(index=False))
print('P0 en iyi 5:\n', T0.nlargest(5, 'gross')[c].round(2).to_string(index=False))
print('P0 son 8:\n', T0.tail(8)[c].round(2).to_string(index=False))
# P0 ile araştırma (örtüşen) arasındaki ilişki: P0 işlemlerinin giriş günleri, araştırmanın sinyal günlerinin ne kadarı
sd_days = cal[(SIG.z3.reindex(cal).abs() > 1.5).fillna(False).values]
print(f'\nSinyal günü {len(sd_days)}; P0 işlem {len(T0)}; P0 giriş günleri {T0.entry.isin(sd_days).mean():.2f} sinyal günü')
