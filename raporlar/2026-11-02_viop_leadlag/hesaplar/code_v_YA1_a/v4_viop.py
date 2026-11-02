"""v_YA1_a — VİOP pay vadelisi bülten verisiyle (data/viop_panel.parquet, SSF) dolum gerçekçiliği.
Sözleşme seçimi: olay günü t'de vadesi t'den SONRA olan en yakın vade (b,c için); d için vadesi t+8 takvim gününden sonra olan en yakın.
Aynı sözleşme kodu t+1 (ve t+5) günlerinde izlenir. qty==0 -> işlem yok (open/close=0) -> dolum yok.
Vadeli limit: prev_settle*(1±0,10) (bülten 'en yüksek/prev_settle' maks ~1,100). Kilit: close>=lim_up-0,01 (tavan) / close<=lim_dn+0,01 (taban).
Testler:
 A) Spot tavan (TC) günü t: vadeli de kilitli mi? Kilitli değilse vadeliyi t kapanışında AL -> t+1 açılış / t+1 kapanış (spot gap'inin vadeliyle alınabilirliği)
 B) Spot TC -> t+1 vadeli açılışta SAT, vadeli kapanışta (ve uzlaşmada) KAPAT; spot gün-içi ile karşılaştırma; t+1 vadeli işlem görmüş mü?
 C) Spot TU -> aynı (sıkı dokunma tanımı)
 D) Spot taban (BC) günü t: vadeli kilitli mi? değilse t kapanışında SAT -> t+1 açılış/kapanış ; t+1 (dolum-uygun) vadeli kapanışta SAT -> t+5 kapanış
Maliyet: 15 bps + 1 tik (0,01 TL / vadeli fiyatı).
"""
import numpy as np, pandas as pd, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v0_panel import SCR, index_ret
from v2_bt import nw_t
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 200)

def st(x, dates, cost_bps=0, tik=None):
    x = pd.Series(np.asarray(x, float)); d = pd.Series(np.asarray(dates))
    if tik is not None: x = x - np.asarray(tik, float)
    x = x - cost_bps / 1e4
    ok = x.notna().values; x = x[ok]; d = d[ok]
    if len(x) < 8: return dict(n=len(x))
    gm = x.groupby(d.values).mean()
    return dict(n=len(x), trade=round(1e4 * x.mean(), 1), t_cl=round(gm.mean() / (gm.std() / np.sqrt(len(gm))), 2) if len(gm) > 2 else np.nan,
                day=round(1e4 * gm.mean(), 1), t_nw=round(nw_t(gm), 2), hit=round((x > 0).mean(), 3))

V = pd.read_parquet(SCR + '/data/viop_panel.parquet')
V = V[(V.segment == 'SSF')].copy()
for c in ['open', 'high', 'low', 'close', 'vwap']:
    V.loc[V.qty.fillna(0) <= 0, c] = np.nan
V = V[['date', 'code', 'root', 'expiry', 'settle', 'prev_settle', 'open', 'high', 'low', 'close', 'vwap', 'qty', 'trades', 'value_tl']]
Vk = V.set_index(['code', 'date']).sort_index()
E = pd.read_parquet(HERE + '/_ev.parquet'); E = E[(E.reg == 'P10') & E.viop & (E.date >= '2020-03-13')].copy()
E = E[E.TC | E.TU | E.BC].copy()
print('VİOP47 P10 olay: TC', E.TC.sum(), 'TU', E.TU.sum(), 'BC', E.BC.sum())
# sözleşme seçimi
Vs = V[['date', 'root', 'code', 'expiry']].copy()
def pick(ev, min_days):
    m = ev[['stock', 'date']].reset_index().merge(Vs, left_on=['stock', 'date'], right_on=['root', 'date'], how='left')
    m = m[m.expiry > m.date + pd.Timedelta(days=min_days)]
    m = m.sort_values('expiry').groupby('index').head(1).set_index('index')
    return m.code.reindex(ev.index)
E['code'] = pick(E, 0); E['code_d'] = pick(E, 8)
def look(code, dates, fields):
    idx = pd.MultiIndex.from_arrays([code.values, pd.to_datetime(dates).values])
    ok = code.notna().values & pd.notna(dates).values
    out = pd.DataFrame(index=code.index, columns=fields, dtype=float)
    sub = Vk.reindex(idx[ok])[fields]
    out.loc[ok, fields] = sub.values
    return out
f = ['open', 'high', 'low', 'close', 'settle', 'prev_settle', 'qty', 'trades', 'vwap']
F0 = look(E.code, E.date, f).add_prefix('f0_'); F1 = look(E.code, E.date_1, f).add_prefix('f1_')
E = pd.concat([E, F0, F1], axis=1)
Fd1 = look(E.code_d, E.date_1, ['close', 'settle', 'prev_settle', 'qty']).add_prefix('d1_')
Fd5 = look(E.code_d, E.date_5, ['close', 'settle', 'qty']).add_prefix('d5_')
Fd0 = look(E.code_d, E.date, ['close', 'settle', 'prev_settle', 'qty']).add_prefix('d0_')
E = pd.concat([E, Fd0, Fd1, Fd5], axis=1)
print('vadeli eşleşme oranı t:', E.f0_settle.notna().mean().round(3), ' t+1:', E.f1_settle.notna().mean().round(3))
E['f0_up'] = np.floor(E.f0_prev_settle * 1.10 * 100 + 1e-6) / 100; E['f0_dn'] = np.ceil(E.f0_prev_settle * 0.90 * 100 - 1e-6) / 100
E['f1_up'] = np.floor(E.f1_prev_settle * 1.10 * 100 + 1e-6) / 100; E['f1_dn'] = np.ceil(E.f1_prev_settle * 0.90 * 100 - 1e-6) / 100
E['f0_lockup'] = E.f0_close >= E.f0_up - 0.011; E['f0_lockdn'] = E.f0_close <= E.f0_dn + 0.011
E['f0_closeup'] = E.f0_close >= E.f0_up * 0.995  # limitin %0,5 yakınında
E['f1_traded'] = E.f1_qty.fillna(0) > 0; E['f0_traded'] = E.f0_qty.fillna(0) > 0
E['f1_openup'] = E.f1_open >= E.f1_up - 0.011
E['tikF1'] = 0.01 / E.f1_open; E['tikF0'] = 0.01 / E.f0_close
E['fint1'] = np.log(E.f1_close / E.f1_open); E['fint1s'] = np.log(E.f1_settle / E.f1_open)
E['fon1'] = np.log(E.f1_open / E.f0_close); E['fcc1'] = np.log(E.f1_close / E.f0_close); E['fcc1s'] = np.log(E.f1_settle / E.f0_settle)
E['fon1s'] = np.log(E.f1_open / E.f0_settle)
E['prem0'] = np.log(E.f0_close / E.c_unadj)  # vadeli kapanış / spot kapanış (Yahoo c bölünme-düzeltilmiş olabilir -> yalnız oran için)
for nm, m in [('TC', E.TC), ('TU', E.TU), ('BC', E.BC)]:
    s = E[m]
    print(f'\n##### {nm} (n={len(s)}) vadeli t verisi var: {s.f0_settle.notna().mean():.3f} | t işlem gördü: {s.f0_traded.mean():.3f} | t+1 işlem gördü: {s.f1_traded.mean():.3f}')
    if nm == 'TC':
        print(' t kapanışında vadeli tavanda kilitli (close>=lim-1tik):', round(s.f0_lockup.mean(), 3), '| limitin %0,5 yakınında:', round(s.f0_closeup.mean(), 3))
        print(' t+1 vadeli açılış tavanda:', round(s.f1_openup.mean(), 3))
        nl = s[(~s.f0_lockup) & s.f0_traded]
        print(' A) vadeli kilitli DEĞİL -> t kapanışında AL: n', len(nl))
        print('    t kapanış->t+1 açılış (brüt):', st(nl.fon1, nl.date), ' spot gap aynı olaylar:', st(nl.gap_1, nl.date))
        print('    t kapanış->t+1 kapanış (brüt):', st(nl.fcc1, nl.date), ' | 15bps+tik:', st(nl.fcc1, nl.date, 15, nl.tikF0))
        print('    uzlaşma->uzlaşma (brüt):', st(nl.fcc1s, nl.date))
        lk = s[s.f0_lockup]
        print('    (kilitli olanlar: t uzlaşma->t+1 açılış brüt, alınamaz):', st(lk.fon1s, lk.date))
    if nm in ('TC', 'TU'):
        ok = s[s.f1_traded]
        print(' B) t+1 vadeli açılışta SAT -> kapanış: brüt', st(-ok.fint1, ok.date), '\n    15bps:', st(-ok.fint1, ok.date, 15), '\n    15bps+tik:', st(-ok.fint1, ok.date, 15, ok.tikF1),
              '\n    30bps+tik:', st(-ok.fint1, ok.date, 30, ok.tikF1), '\n    uzlaşmada kapat 15+tik:', st(-ok.fint1s, ok.date, 15, ok.tikF1))
        print('    spot gün-içi (aynı olaylar) brüt:', st(-ok.intra_1, ok.date), ' | tüm olaylar spot brüt:', st(-s.intra_1, s.date))
        print('    vadeli açılış vs spot açılış farkı log(Fo/F0close) - spot gap, medyan bps:', round(1e4 * (ok.fon1 - ok.gap_1).median(), 1),
              ' | corr(vadeli gün-içi, spot gün-içi)=', round(ok[['fint1', 'intra_1']].corr().iloc[0, 1], 3))
        for a, b in [('2020-03-13', '2020-12-31'), ('2021-01-01', '2026-12-31'), ('2020-03-13', '2022-12-31'), ('2023-01-01', '2026-12-31')]:
            q = ok[(ok.date >= a) & (ok.date <= b)]
            print(f'    {a[:4]}-{b[:4]} vadeli 15+tik:', st(-q.fint1, q.date, 15, q.tikF1))
        yy = {int(y): st(-g.fint1, g.date, 15, g.tikF1).get('trade') for y, g in ok.groupby('yr')}
        print('    yıllar (vadeli, 15+tik, işlem başı):', yy)
        # likidite: t+1 vadeli işlem tutarı
        q = ok.f1_value_tl if 'f1_value_tl' in ok else None
    if nm == 'BC':
        print(' t kapanışında vadeli tabanda kilitli:', round(s.f0_lockdn.mean(), 3))
        nl = s[(~s.f0_lockdn) & s.f0_traded]
        print(' D1) vadeli kilitli DEĞİL -> t kapanışında SAT: n', len(nl), ' t->t+1 açılış brüt:', st(-nl.fon1, nl.date), ' t->t+1 kapanış brüt:', st(-nl.fcc1, nl.date),
              ' 15+tik:', st(-nl.fcc1, nl.date, 15, nl.tikF0))
        lk = s[s.f0_lockdn]
        print('    (kilitli olanlar uzlaşma->t+1 açılış, dolmaz):', st(-lk.fon1s, lk.date))
        fill = s[(s.BC_1 == False)]
        d1lock = fill.d1_close <= np.ceil(fill.d1_prev_settle * 0.90 * 100 - 1e-6) / 100 + 0.011
        print(' D2) t+1 spot taban değil (dolum-uygun) n', len(fill), '| t+1 vadeli (d sözleşmesi) işlem gördü:', round((fill.d1_qty.fillna(0) > 0).mean(), 3), '| t+1 vadeli tabanda kilitli:', round(d1lock.mean(), 3))
        ff = fill[(fill.d1_qty.fillna(0) > 0) & (fill.d5_qty.fillna(0) > 0) & ~d1lock]
        X = index_ret('XU100')
        xr = (X.lc.reindex(ff.date_5).values - X.lc.reindex(ff.date_1).values)
        fr = np.log(ff.d5_close / ff.d1_close)
        print('    vadeli t+1 kapanış SAT -> t+5 kapanış, XU100 hedge, 19bps+tik:', st(-(fr - xr), ff.date, 19, 0.01 / ff.d1_close), ' ham(hedgesiz) 15+tik:', st(-fr, ff.date, 15, 0.01 / ff.d1_close))
        print('    spot karşılığı (aynı olaylar) 19bps:', st(-ff.dr2_5, ff.date, 19))
E.to_parquet(HERE + '/_ev_viop.parquet')
