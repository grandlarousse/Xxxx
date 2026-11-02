"""b4: olay bazında faktör ayrıştırma, sadece-Cuma alt kümesi, kendi VİOP ayrıştırmam (uzlaşma ve 09:30 açılış seansı), saatlik ilk bar girişi."""
import sys, os, csv; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vb import *
cal = bist_cal(); N = len(cal)
X = load('XU100.IS'); O = np.log(X.o.reindex(cal).values); C = np.log(X.c.reindex(cal).values)
ev = ev_load(('rating',)); post = ev[ev.period == 'post'].copy()
post['i0'] = [react_idx(cal, a, f) for a, f in zip(post.ann, post.after_close)]
post = post.drop_duplicates('i0').reset_index(drop=True)
post['fri'] = post.ann.dt.dayofweek == 4
i0, dr = post.i0.values, post.dir.values
COST = 15e-4
def us(sym):
    d = load(sym); return np.log(d.o * d.adj / d.c), np.log(d.adj), d.index
def us_w(sym, h=2):
    o, c, idx = us(sym); out = []
    for i in i0:
        j = idx.searchsorted(cal[i]); out.append(c.iloc[j + h] - o.iloc[j] if j + h < len(idx) else np.nan)
    return np.array(out)
eem, tur = us_w('EEM'), us_w('TUR')
# Dimson beta of XU100 (TL) on EEM: r_t = a + b0 EEM_t + b1 EEM_{t-1}
e_c = np.log(load('EEM').adj); e_c = e_c.reindex(e_c.index.union(cal)).ffill().reindex(cal).values
rE = np.diff(e_c, prepend=np.nan); rX = np.diff(C, prepend=np.nan)
def dbeta(i):
    y = rX[i - 260:i - 5]; Z = np.column_stack([np.ones(len(y)), rE[i - 260:i - 5], rE[i - 261:i - 6]]); m = np.isfinite(y) & np.isfinite(Z).all(1)
    b = np.linalg.lstsq(Z[m], y[m], rcond=None)[0]; return b[1] + b[2]
bX = np.array([dbeta(i) for i in i0])
def tbeta(i):
    a = np.log(load('TUR').adj).diff(); f = np.log(load('EEM').adj).diff(); df = pd.concat([a, f], axis=1, keys=['a', 'f'], sort=True).dropna()
    w_ = df[(df.index < cal[i]) & (df.index >= cal[i] - pd.Timedelta(days=365))]; return np.cov(w_.a, w_.f)[0, 1] / w_.f.var()
bT = np.array([tbeta(i) for i in i0])
xu = C[i0 + 2] - O[i0]
T = pd.DataFrame({'react': cal[i0].date, 'ag': post.agency, 'dir': dr, 'fri': post.fri,
                  'XU100': 1e4 * (-dr * xu), 'EEM': 1e4 * (-dr * eem), 'bX': bX.round(2), 'XU100_ab': 1e4 * (-dr * (xu - bX * eem)),
                  'TUR': 1e4 * (-dr * tur), 'TUR_ab': 1e4 * (-dr * (tur - bT * eem))})
print(T.round(0).to_string(index=False))
T.to_csv(HERE + '/res_b4_event_factor.csv', index=False)
for lab, m in [('TÜMÜ', np.ones(len(T), bool)), ('SADECE CUMA (n=17)', T.fri.values), ('IS 2014-20', pd.to_datetime(T.react).dt.year.values <= 2020), ('OOS 2021-26', pd.to_datetime(T.react).dt.year.values >= 2021)]:
    print(f'-- {lab}')
    for c in ['XU100', 'XU100_ab', 'TUR', 'TUR_ab', 'EEM']:
        v = T.loc[m, c] / 1e4 - (COST if c != 'EEM' else 0); print('   ' + fmt(v, c + (' (net 15bps)' if c != 'EEM' else ' (brüt)')))
print('ortalama Dimson beta XU100/EEM', bX.mean().round(2), ' TUR/EEM', bT.mean().round(2))

print('\n=== Kendi VİOP ayrıştırmam: F_XU030 en aktif kontrat, t0 uzlaşma -> t+2 uzlaşma (4 bps) ===')
VD = S + '/data/viop'
def vparse(d):
    f = f'{VD}/viop_{d:%Y%m%d}.csv'
    if not os.path.exists(f): return None
    with open(f, encoding='windows-1254', errors='replace') as fh:
        rd = csv.reader(fh, delimiter=';'); hdr = [h.strip() for h in next(rd)]; next(rd)
        rows = [dict(zip(hdr, r)) for r in rd if len(r) >= 20 and r[1].startswith('F_XU030')]
    df = pd.DataFrame(rows)
    for c in ['UZLASMA FIYATI', 'ONCEKI UZLASMA FIYATI', 'ACILIS FIYATI', 'KAPANIS FIYATI', 'ISLEM MIKTARI', 'ACILIS SEANSI FIYATI']:
        df[c] = pd.to_numeric(df.get(c, pd.Series(np.nan, index=df.index)), errors='coerce')
    return df.set_index('SOZLESME KODU')
rows = []
for i, d_, fri in zip(i0, dr, post.fri):
    a, b = vparse(cal[i]), vparse(cal[i + 2]); pv = vparse(cal[i - 1])
    if a is None or b is None or a.empty: rows.append(dict(react=cal[i].date())); continue
    k = a['ISLEM MIKTARI'].idxmax()
    if k not in b.index: rows.append(dict(react=cal[i].date())); continue
    s0, s2 = a.at[k, 'UZLASMA FIYATI'], b.at[k, 'UZLASMA FIYATI']; os_ = a.at[k, 'ACILIS SEANSI FIYATI']
    rows.append(dict(react=cal[i].date(), fri=fri, code=k, qty=a.at[k, 'ISLEM MIKTARI'], settle=1e4 * (-d_ * np.log(s2 / s0)),
                     open_session=1e4 * (-d_ * np.log(s2 / os_)) if np.isfinite(os_) and os_ > 0 else np.nan,
                     spot_close=1e4 * (-d_ * (np.log(load('XU030.IS').c.reindex(cal).values[i + 2] / load('XU030.IS').c.reindex(cal).values[i])))))
V = pd.DataFrame(rows); print(V.round(0).to_string(index=False)); V.to_csv(HERE + '/res_b4_viop.csv', index=False)
print(fmt(V.settle.dropna() / 1e4 - 4e-4, 'F_XU030 uzlaşma t0->t+2 (4 bps)'))
print(fmt(V[V.fri == True].settle.dropna() / 1e4 - 4e-4, '  sadece Cuma'))
print(fmt(V.open_session.dropna() / 1e4 - 4e-4, 'F_XU030 09:30 açılış seansı -> t+2 uzlaşma'))
print(fmt(V.spot_close.dropna() / 1e4 - 15e-4, 'XU030 spot kapanış t0->t+2 (aynı olaylar)'))

print('\n=== Saatlik: ilk bar kapanışı (~10:30 TSİ) girişi, 2023-11+ olaylar ===')
h = pd.read_parquet(S + '/data/h1/XU100.IS.parquet'); h.index = pd.to_datetime(h.index, utc=True)
for i, d_ in zip(i0, dr):
    day = cal[i]
    if day < pd.Timestamp('2023-11-15'): continue
    b = h[h.index.normalize().tz_localize(None) == day].sort_index()
    if b.empty: print(day.date(), 'h1 yok'); continue
    c2 = C[i + 2]; o_d = O[i]
    r_open = -d_ * (c2 - o_d); r_b1 = -d_ * (c2 - np.log(b.c.iloc[0])); r_b2 = -d_ * (c2 - np.log(b.c.iloc[1]))
    print(f'{day.date()} dir {d_:+d} | bar0 {b.index[0].strftime("%H:%M")} o {b.o.iloc[0]:.1f} c {b.c.iloc[0]:.1f}; günlük o {np.exp(o_d):.1f} | açılış {1e4*r_open:+.0f}  1.bar {1e4*r_b1:+.0f}  2.bar {1e4*r_b2:+.0f} bps')
