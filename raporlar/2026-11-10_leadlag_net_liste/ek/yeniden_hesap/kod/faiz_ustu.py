"""Elestirmen itirazi 1: vadeli tasima (TL faizi) dusulunce ne kaliyor?
faiz_ustu = islem getirisi - yillik_faiz(yil) * takvim_gunu/365  (uzun);  kisa: -getiri + faiz*gun/365
Faiz serisi YAKLASIK yillik ortalama politika faizidir (elle girildi); 2026 = F_XU030 Aralik priminden ~%27-30.
Kullanim: python3 -I faiz_ustu.py <veri_klasoru>"""
import json, sys, os, math
import numpy as np, pandas as pd
D = sys.argv[1]
RATE = {2011:6.0,2012:5.8,2013:5.0,2014:9.0,2015:8.0,2016:8.0,2017:11.5,2018:17.5,2019:20.5,2020:10.5,2021:17.5,2022:12.5,2023:21.0,2024:49.0,2025:43.0,2026:30.0}
def load(s):
    j = json.load(open(os.path.join(D, s + '.json')))['chart']['result'][0]
    q = j['indicators']['quote'][0]
    w = pd.to_datetime(pd.Series(j['timestamp']), unit='s', utc=True) + pd.Timedelta(seconds=j['meta'].get('gmtoffset', 0))
    df = pd.DataFrame({'c': q['close'], 'v': q['volume'], 'a': j['indicators']['adjclose'][0]['adjclose']})
    df.index = pd.to_datetime(w.dt.date.values)
    df = df.dropna(subset=['a'])
    df = df[~df.index.duplicated(keep='last')]
    if s.endswith('.IS') and not s.startswith('XU'):
        df = df[df.v.fillna(0) > 0]
    r = np.log(df.a).diff()
    if s.endswith('.IS'): r[r.abs() > 0.25] = np.nan
    return df, r
def z60(r): return r / r.rolling(60).std().shift(1)
def trades(tgt_df, sig, h, side=1):
    idx = tgt_df.index; p = np.log(tgt_df.a.values); out = []; i = 260; n = len(idx)
    s = sig.reindex(idx).fillna(False).values
    while i < n - h:
        if s[i]:
            g = (p[i + h] - p[i]) * 1e4
            cal = (idx[i + h] - idx[i]).days
            carry = RATE[idx[i].year] / 100 * cal / 365 * 1e4
            out.append((idx[i], side * g, side * (g - carry), cal)); i += h
        else: i += 1
    return pd.DataFrame(out, columns=['d', 'brut', 'fu', 'cal']).set_index('d')
def st(x):
    x = x.dropna(); n = len(x)
    return (n, round(x.mean(), 1), round(x.mean() / (x.std(ddof=1) / math.sqrt(n)), 2)) if n > 2 else (n, np.nan, np.nan)
def rep(name, tr, cost):
    a = st(tr.brut); b = st(tr.fu); o = st(tr.fu[tr.index >= '2022-01-01']); s = st(tr.fu[tr.index >= '2024-01-01']); i = st(tr.fu[tr.index < '2022-01-01'])
    print(f"{name:44s} n={a[0]:4d} brut={a[1]:6.1f} | faiz_ustu={b[1]:6.1f} (t {b[2]:5.2f}) | -maliyet{cost}: {b[1]-cost:6.1f} | IS {i[1]:6.1f} (t {i[2]:5.2f}) | 2022+ {o[1]:6.1f} (t {o[2]:5.2f}) | 2024+ n={s[0]} {s[1]:6.1f} (t {s[2]:5.2f}) | ort.takvim gun {tr.cal.mean():.2f}")
xu, rxu = load('XU030.IS'); zxu = z60(rxu)
for h in (2, 3): rep(f"XU030 z>=1 -> XU030 uzun h{h}", trades(xu, zxu >= 1, h), 5)
# ABD -> BIST esleme
def map_us(sig_us, bist_idx):
    pos = np.searchsorted(bist_idx.values, sig_us.index.values, side='right')
    ok = pos < len(bist_idx)
    return pd.Series(sig_us.values[ok], index=bist_idx[pos[ok]]).groupby(level=0).max()
kbe, rk = load('KBE'); zk = z60(rk)
ak, rak = load('AKBNK.IS')
sig = map_us((zk >= 1.5), ak.index)
rep("KBE z>=1.5 -> AKBNK uzun h2", trades(ak, sig, 2), 10)
sig1 = map_us((zk >= 1.0), ak.index); rep("KBE z>=1.0 -> AKBNK uzun h2", trades(ak, sig1, 2), 10)
# TUPRS
gs = [f for f in os.listdir(D) if 'GSPC' in f][0][:-5]
ref = pd.concat([load(x)[1] for x in ['VLO', 'MPC', 'PSX', 'PBF']], axis=1).mean(axis=1); spx = load(gs)[1]
x = pd.concat([ref, spx], axis=1).dropna(); x.columns = ['b', 'm']
beta = (x.b.rolling(250).cov(x.m) / x.m.rolling(250).var()).shift(1)
P = x.b - beta * x.m; z = P / P.rolling(250).std().shift(1)
tu, rtu = load('TUPRS.IS')
def map_sum(v, bist_idx):
    pos = np.searchsorted(bist_idx.values, v.index.values, side='right'); ok = pos < len(bist_idx)
    return pd.Series(v.values[ok], index=bist_idx[pos[ok]])
# z'yi BIST gunune tasirken cok gun duserse P'leri topla -> basit: son gunun z'si yerine toplam P / sd
Pm = map_sum(P.dropna(), tu.index).groupby(level=0).sum(); sdm = map_sum((P.rolling(250).std().shift(1)).dropna(), tu.index).groupby(level=0).last()
zb = (Pm / sdm)
for h in (2, 3):
    rep(f"TUPRS rafineri z>1 uzun h{h}", trades(tu, zb > 1, h), 10)
    rep(f"   ... ve TUPRS o gun artida h{h}", trades(tu, (zb > 1) & (rtu.reindex(zb.index) > 0), h), 10)
    rep(f"   ... ve TUPRS o gun ekside/yatay h{h}", trades(tu, (zb > 1) & (rtu.reindex(zb.index) <= 0), h), 10)
    rep(f"TUPRS rafineri z<-1 KISA h{h}", trades(tu, zb < -1, h, side=-1), 10)
ry, rry = load('RYGYO.IS'); rs, rrs = load('RYSAS.IS')
rep("RYGYO z>1 -> RYSAS uzun h1", trades(rs, z60(rry) > 1, 1), 10)
# yil yil XU030 h3
t = trades(xu, zxu >= 1, 3); print("XU030 h3 yil yil (n, brut, faiz_ustu):", {int(y): (len(g), round(g.brut.mean()), round(g.fu.mean())) for y, g in t.groupby(t.index.year)})
t = trades(ak, sig, 2); print("KBE>AKBNK h2 yil yil:", {int(y): (len(g), round(g.brut.mean()), round(g.fu.mean())) for y, g in t.groupby(t.index.year)})
