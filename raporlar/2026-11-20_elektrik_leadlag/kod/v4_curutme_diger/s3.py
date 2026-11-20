"""V4 — S3 (A5_gecikme1_viop3_h3) çürütme. Kullanım: python3 -I s3.py <panel_full>"""
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import elib, pm, tt, hac, indep_pos, add, save, PER  # noqa: E402

D = sys.argv[1]
P = elib.load(D)
idx = P['ret_cc'].index
TRIO = ['AKSEN', 'ENJSA', 'ODAS']
H = 3
r = P['idx_ret'][['XELKT', 'XU030']].reindex(idx)
den = r.rolling(60, min_periods=40).std().shift(1)
z = r / den
sigC = ((z['XU030'] >= 1) & (z['XELKT'] < 0.5)).fillna(False)          # özgün (c)
sigU = (z['XU030'] >= 1).fillna(False)                                 # koşulsuz (a)
sigB = ((z['XU030'] >= 1) & (z['XELKT'] >= 0.5)).fillna(False)         # sektör de güçlü (b)

f, fl, _ = elib.fwd_exec(P, H, 'long', TRIO)
fl = fl.reindex_like(f).fillna(False)
# bağımsız kısa kod: düzeyden düz 3 günlük getiri
Rt = P['ret_cc'][TRIO]
Lv = (1 + Rt.fillna(0)).cumprod()
f_own = (Lv.shift(-H) / Lv - 1).where(Rt.notna())
LX = P['idx']['XU030'].reindex(idx)
fX = LX.shift(-H) / LX - 1


def demean(F, U, parts):
    out = pd.DataFrame(np.nan, index=F.index, columns=F.columns)
    for per in parts:
        m = pm(F.index, per)
        mu = F[m].where(U[m]).mean()
        out.loc[m] = (F[m] - mu).values
    return out


def ds(E, s, U=fl):
    S = pd.DataFrame(np.repeat(s.values[:, None], E.shape[1], axis=1), index=E.index, columns=E.columns) & U
    return E.where(S).mean(axis=1)


E_uc = demean(f, fl, ['IS', 'OOS1', 'KASA'])
E_hv = demean(f, fl, ['IS', 'HAVUZ'])
E_own_hv = demean(f_own, fl, ['IS', 'HAVUZ'])

print('== 0. Yineleme (elib fwd_exec + per)')
for per, E in [('IS', E_uc), ('OOS1', E_uc), ('KASA', E_uc), ('HAVUZ', E_hv)]:
    p = ds(E, sigC)[pm(idx, per)]
    mu, t, n = hac(p, H)
    add('S3', 'yineleme: per, elib dolum', per, n, mu, t, f'bagimsiz={len(indep_pos(p, H))}')
p = ds(E_own_hv, sigC)[pm(idx, 'HAVUZ')]
mu, t, n = hac(p, H)
add('S3', 'yineleme: kendi kisa kod (duz f3, per)', 'HAVUZ', n, mu, t, '')

print('== 1. Olaylar (2023+) ve en iyiler cikinca')
pH = ds(E_hv, sigC)[pm(idx, 'HAVUZ')]
praw = ds(f, sigC)[pm(idx, 'HAVUZ')]
ev = pd.DataFrame({'per': pH, 'ham': praw}).dropna()
ev['xu030'] = r['XU030'].reindex(ev.index)
ev['xelkt'] = r['XELKT'].reindex(ev.index)
ev['zX'] = z['XU030'].reindex(ev.index)
ev['zE'] = z['XELKT'].reindex(ev.index)
ev['xu030_f3'] = fX.reindex(ev.index)
for c in TRIO:
    ev[c] = E_hv[c].where(fl[c]).reindex(ev.index)
ind = indep_pos(pH, H)
ev['bagimsiz'] = ev.index.isin(ind)
pd.set_option('display.width', 250)
print((ev.assign(**{k: (1e4 * ev[k]).round(0) for k in ['per', 'ham', 'xu030_f3'] + TRIO},
                 xu030=(100 * ev.xu030).round(2), xelkt=(100 * ev.xelkt).round(2)).round(2)).to_string())
for d, rw in ev.iterrows():
    add('S3', 'olay', d.strftime('%Y-%m-%d'), int(rw.bagimsiz), 1e4 * rw.per, None,
        f'XU030 {100 * rw.xu030:+.2f}%; XELKT {100 * rw.xelkt:+.2f}%; zX {rw.zX:.2f}; zE {rw.zE:.2f}; uclu ham3g {1e4 * rw.ham:+.0f}; XU030 3g {1e4 * rw.xu030_f3:+.0f}')
srt = ev['per'].sort_values(ascending=False)
for k in [0, 1, 2, 3, 5, 10]:
    keep = ev['per'].drop(srt.index[:k])
    pk = pH.copy()
    pk.loc[srt.index[:k]] = np.nan
    mu, t, n = hac(pk, H)
    mu2, t2, n2 = tt(keep)
    add('S3', f'en iyi {k} gun haric (per)', 'HAVUZ', n, mu, t, f'basit t={t2:.2f}; cikanlar: {",".join(x.strftime("%y-%m-%d") for x in srt.index[:k])}')
# yalnız bağımsız olaylar
ei = ev[ev.bagimsiz]['per']
mu, t, n = tt(ei)
add('S3', 'yalniz bagimsiz olaylar (basit t)', 'HAVUZ', n, mu, t, f'medyan={1e4 * ei.median():.0f}; isabet={(ei > 0).mean():.2f}; sd={1e4 * ei.std():.0f}')
si = ei.sort_values(ascending=False)
for k in [3, 5]:
    mu, t, n = tt(si.iloc[k:])
    add('S3', f'bagimsiz olaylar, en iyi {k} haric (basit t)', 'HAVUZ', n, mu, t, '')
add('S3', 'gun duzeyi medyan / isabet (per)', 'HAVUZ', len(ev), 1e4 * ev['per'].median(), None, f'isabet per>0: {(ev.per > 0).mean():.2f}; ham>0: {(ev.ham > 0).mean():.2f}')
for y, g in ev.groupby(ev.index.year):
    add('S3', 'yil (per, gun ort.)', str(y), len(g), 1e4 * g['per'].mean(), None, f'bagimsiz={int(g.bagimsiz.sum())}; ham={1e4 * g.ham.mean():.0f}')

print('== 2. Gecikme mi momentum mu')
fXd = fX.copy()
Xdm = {}
for parts in (['IS', 'HAVUZ'],):
    out = pd.Series(np.nan, index=idx)
    for per in parts:
        m = pm(idx, per)
        out[m] = fX[m] - fX[m].mean()
    Xdm = out
beta = pd.DataFrame({c: Rt[c].rolling(250, min_periods=60).cov(r['XU030']) / r['XU030'].rolling(250, min_periods=60).var() for c in TRIO}).shift(1).fillna(1.0)
hed = f - beta.mul(fX, axis=0)
E_hed = demean(hed, fl, ['IS', 'HAVUZ'])
E_hed_uc = demean(hed, fl, ['IS', 'OOS1', 'KASA'])


def EP(per, hedged=False):
    """Döneme uygun dönem-nötr kıyas: IS/OOS1/KASA kendi dönem ortalaması, HAVUZ 2023+ ortalaması."""
    if hedged:
        return E_hed if per == 'HAVUZ' else E_hed_uc
    return E_hv if per == 'HAVUZ' else E_uc

for per in ['IS', 'OOS1', 'KASA', 'HAVUZ']:
    m = pm(idx, per)
    pa = (fX - fX[m].mean()).where(sigC)[m]
    mu, t, n = hac(pa, H)
    add('S3', 'ayni gunlerde XU030 kendi 3g (donem ort. cikarilmis)', per, n, mu, t, '')
    mu, t, n = hac(ds(EP(per, True), sigC)[m], H)
    add('S3', 'XU030 beta korumali uclu (per)', per, n, mu, t, f'ort beta={beta[m].where(sigC[m]).mean().mean():.2f}')
    mu, t, n = hac(ds(EP(per), sigU)[m], H)
    add('S3', '(a) kosulsuz XU030 z>=1 -> uclu (per)', per, n, mu, t, '')
    pb = ds(EP(per), sigB)[m]
    mub, tb, nb = hac(pb, H)
    add('S3', '(b) XU030 z>=1 ve XELKT z>=0,5 -> uclu (per)', per, nb, mub, tb, '')
    pc = ds(EP(per), sigC)[m]
    a, b = pc.dropna(), pb.dropna()
    dif = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    add('S3', '(c)-(b): gecikme kosulunun katkisi (Welch)', per, len(a), 1e4 * dif, dif / se, '')
    mu, t, n = hac(ds(EP(per, True), sigB)[m], H)
    add('S3', '(b) beta korumali', per, n, mu, t, '')
    mu, t, n = hac(ds(EP(per, True), sigU)[m], H)
    add('S3', '(a) beta korumali', per, n, mu, t, '')

print('== 3. Kiyas duyarliligi')
bc = f.where(fl).rolling(121, center=True, min_periods=60).mean()
E_c60 = f - bc
ym = pd.Series(idx.year * 100 + idx.month, index=idx)
nos = f.where(fl).where(np.repeat(~sigC.values[:, None], f.shape[1], axis=1))
E_ay = f - nos.groupby(ym).transform('mean')
E_ownb = f - elib.bench_own(f, H)
for per in ['IS', 'OOS1', 'KASA', 'HAVUZ']:
    m = pm(idx, per)
    for nm, E in [('ham', f), ('own (gecikmeli 250g)', E_ownb), ('merkezli +-60 gun ort.', E_c60), ('ayni ayin diger gunleri', E_ay)]:
        mu, t, n = hac(ds(E, sigC)[m], H)
        add('S3', 'kiyas: ' + nm, per, n, mu, t, '')

print('== 4. Karar ani')


def rd(kind, sym):
    d = pd.read_parquet(os.path.join(D, kind, sym + '.parquet'))
    ts = pd.to_datetime(d['ts_tr'])
    return d.assign(date=ts.dt.normalize(), hm=ts.dt.hour * 100 + ts.dt.minute)


def bar(d, hm):
    return d[d.hm == hm].groupby('date').c.last()


V = {}
for s in ['XU030', 'XELKT']:
    h1, m5 = rd('h1_isy', s), rd('m5_isy', s)
    V[(s, '17:00')] = bar(h1, 1600)
    V[(s, '18:00')] = bar(h1, 1700)
    V[(s, '17:30')] = bar(m5, 1725)
    V[(s, '17:50')] = bar(m5, 1745)
    V[(s, '17:55')] = bar(m5, 1750)
yh = rd('h1', 'XU030')
y1730 = bar(yh, 1630)
chk = pd.concat([V[('XU030', '17:30')], y1730], axis=1, sort=True).dropna()
print('XU030 17:30: isy_m5 ile yahoo_h1 ortak gun', len(chk), 'ort |fark| bps', 1e4 * (chk.iloc[:, 0] / chk.iloc[:, 1] - 1).abs().mean() if len(chk) else None)
V[('XU030', '17:30')] = V[('XU030', '17:30')].combine_first(y1730)
prev = P['idx'][['XELKT', 'XU030']].reindex(idx).shift(1)
SUB = {'2017-2022': (idx >= '2017-01-01') & (idx <= '2022-12-30'), '2023+': pm(idx, 'HAVUZ')}
for tau in ['17:00', '17:30', '17:50', '17:55', '18:00']:
    zx = (V[('XU030', tau)].reindex(idx) / prev['XU030'] - 1) / den['XU030']
    ze = (V[('XELKT', tau)].reindex(idx) / prev['XELKT'] - 1) / den['XELKT']
    av = zx.notna() & ze.notna()
    st = ((zx >= 1) & (ze < 0.5)).fillna(False) & av
    for nm, m in SUB.items():
        sc_ = sigC & av & m
        nC, nT = int(sc_.sum()), int((st & m).sum())
        both = int((sc_ & st).sum())
        fa = st & ~sigC & m
        mi = sc_ & ~st
        E = E_hv
        mu, t, n = hac(ds(E, st & m), H)
        mum, tm_, nm_ = tt(ds(E, mi).dropna())
        muf, tf_, nf_ = tt(ds(E, fa).dropna())
        muc, tc_, nc_ = hac(ds(E, sc_), H)
        xok = float(((zx >= 1) & sc_).sum() / max(nC, 1))
        eok = float(((ze < 0.5) & sc_).sum() / max(nC, 1))
        add('S3', f'karar ani {tau}: sinyal {tau} degeriyle, giris kapanis (per)', nm, nT, mu, t,
            f'veri gunu={int((av & m).sum())}; kapanis sinyali={nC}; yakalanan={both} ({both / max(nC, 1):.0%}); yanlis={int(fa.sum())} ({int(fa.sum()) / max(nT, 1):.0%}); '
            f'kapanis sinyali ayni gunler per={muc:.0f} (t {tc_:.1f}); kacan per={mum:.0f} (n {nm_}); yanlis per={muf:.0f} (n {nf_}); XU030 kosulu hazir={xok:.0%}; XELKT kosulu hazir={eok:.0%}')
# 17:30 → kapanış: üçlü fiyatı (snap, ham baz) — kazancın ne kadarı kapanıştan önce gidiyor?
sn = P['snap'].copy()
sn['date'] = pd.to_datetime(sn['date'])
for col in ['p_1700', 'p_1730', 'p_son']:
    pv = sn[sn.sym.isin(TRIO)].pivot(index='date', columns='sym', values=col)
    pcl = sn[sn.sym.isin(TRIO)].pivot(index='date', columns='sym', values='p_close')
    g = (pcl / pv - 1).reindex(idx)
    m = pm(idx, 'HAVUZ')
    a = g[m].where(np.repeat(sigC[m].values[:, None], g.shape[1], axis=1)).mean(axis=1).dropna()
    b = g[m].where(np.repeat(~sigC[m].values[:, None], g.shape[1], axis=1)).mean(axis=1).dropna()
    mu, t, n = tt(a)
    add('S3', f'uclu: {col} -> resmi kapanis getirisi, sinyal gunleri', 'HAVUZ', n, mu, t, f'diger gunler ort={1e4 * b.mean():.1f} (n {len(b)})')

print('== 5. Vadeli ve maliyet')
vf = P['viop_front'].copy()
vf['date'] = pd.to_datetime(vf['date'])
m = pm(idx, 'HAVUZ')
tot_s, tot_f = [], []
for u in TRIO:
    s = vf[vf.und == u].drop_duplicates('date').set_index('date')
    f3f = s['ret_settle_f3'].reindex(idx)
    okk = sigC & m & f3f.notna() & fl[u] & f_own[u].notna()
    a, b = f_own[u][okk], f3f[okk]
    carry = (s['ret_settle'].reindex(idx) - Rt[u])[m]
    px = P['close_raw'][u]
    tick_s = pd.Series(elib.tick_of(px.values), index=idx)
    tick_f = pd.Series(elib.tick_of(px.values, elib.TICK_TABLE_FUT), index=idx)
    add('S3', f'vadeli {u}: uzlasma f3 - spot f3 (ayni olaylar)', 'HAVUZ', int(okk.sum()), 1e4 * (b - a).mean(), tt(b - a)[1],
        f'spot ham={1e4 * a.mean():.0f}; vadeli ham={1e4 * b.mean():.0f}; gunluk tasima (vadeli-spot getirisi, tum gunler)={1e4 * carry.mean():.1f} bps/gun; '
        f'son fiyat {px.dropna().iloc[-1]:.2f} TL; 1 adim spot={1e4 * (tick_s / px).dropna().iloc[-1]:.0f} bps, vadeli={1e4 * (tick_f / px).dropna().iloc[-1]:.0f} bps; '
        f'olay gunlerinde ort. adim spot={1e4 * (tick_s / px)[okk].mean():.0f}, vadeli={1e4 * (tick_f / px)[okk].mean():.0f} bps')
    tot_s.append(a)
    tot_f.append(b)
print('COST', elib.COST)
Sg = pd.DataFrame(np.repeat(sigC.values[:, None], 3, axis=1), index=idx, columns=TRIO) & fl
for per in ['OOS1', 'KASA', 'HAVUZ']:
    mm = pm(idx, per)
    Sm = Sg.copy()
    Sm[~mm] = False
    X = EP(per).where(Sm)
    vals = X.values[np.isfinite(X.values)]
    cs = {s: elib.cost_bps(P, Sm, s) for s in elib.COST}
    add('S3', 'spot maliyet sonrasi net (islem basina per)', per, len(vals), 1e4 * vals.mean(), None,
        '; '.join(f'{s}: maliyet {c:.0f} -> net {1e4 * vals.mean() - c:.0f}' for s, c in cs.items()))
cnt = sigC.groupby(idx.year).sum()
ind_all = indep_pos(ds(f, sigC), H)
ci = pd.Series(1, index=ind_all).groupby(ind_all.year).sum()
add('S3', 'yilda olay sayisi (sinyal gunu / bagimsiz)', '2010-2026', int(sigC.sum()), None, None,
    '; '.join(f'{y}:{int(cnt.get(y, 0))}/{int(ci.get(y, 0))}' for y in range(2017, 2027)) + f'; 2023+ yillik ort. bagimsiz={ci[ci.index >= 2023].sum() / 3.88:.1f}')

print('== 6. Tek hisse ve en kotu olaylar')
for per in ['IS', 'OOS1', 'KASA', 'HAVUZ']:
    mm = pm(idx, per)
    for u in TRIO:
        p = EP(per)[u].where(sigC & fl[u])[mm]
        mu, t, n = hac(p, H)
        add('S3', f'tek hisse {u} (per)', per, n, mu, t, '')
    for drop in TRIO:
        keep = [c for c in TRIO if c != drop]
        mu, t, n = hac(ds(EP(per)[keep], sigC, fl[keep])[mm], H)
        add('S3', f'{drop} haric ikili (per)', per, n, mu, t, '')
w = ev.sort_values('ham').head(6)
add('S3', 'en kotu 6 olay (uclu ham 3g)', 'HAVUZ', len(ev), 1e4 * w.ham.mean(), None, '; '.join(f'{d.strftime("%Y-%m-%d")}:{1e4 * v:+.0f}' for d, v in w.ham.items()))
st_ = f.where(Sg)[pm(idx, 'HAVUZ')].stack().dropna().sort_values()
add('S3', 'en kotu 5 tek hisse islemi (ham 3g)', 'HAVUZ', len(st_), 1e4 * st_.head(5).mean(), None, '; '.join(f'{d.strftime("%Y-%m-%d")} {c}:{1e4 * v:+.0f}' for (d, c), v in st_.head(5).items()))
add('S3', 'ham 3g dagilimi (islem)', 'HAVUZ', len(st_), 1e4 * st_.mean(), None, f'%5={1e4 * st_.quantile(.05):.0f}; %25={1e4 * st_.quantile(.25):.0f}; medyan={1e4 * st_.median():.0f}; %75={1e4 * st_.quantile(.75):.0f}; kazanan={(st_ > 0).mean():.2f}; sd={1e4 * st_.std():.0f}')
# t+1 girişi
s1 = sigC.shift(1, fill_value=False)
for per in ['OOS1', 'KASA', 'HAVUZ']:
    mu, t, n = hac(ds(EP(per), s1)[pm(idx, per)], H)
    add('S3', 't+1 kapanisindan giris (per)', per, n, mu, t, '')
save('s3.csv')
