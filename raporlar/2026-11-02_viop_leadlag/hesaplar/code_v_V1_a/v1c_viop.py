"""VİOP F_XU030 (ve varsa F_XLBNK / F_XBANK) gerçek vadeli fiyatlarıyla V1 testi.
Eksik bülten günlerini indirir (≥0,4 sn ara, dosya varsa atlar) -> data/viop/.
Giriş: t0 kapanış/uzlaşma (açılış fiyatı akşam seansı nedeniyle olay öncesi olabilir -> KULLANILMAZ, sadece t0 09:30 öncesi dönemde bilgi amaçlı)."""
import sys, os, time, subprocess, csv
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_V1_a')
from v1 import *
VD = SC + '/data/viop'
rat = EV[EV.kind == 'rating'].copy()
rat = rat[rat.react >= '2017-04-05']
need = set()
for i in rat.react_i:
    for k in [-1, 0, 1, 2]: need.add(CAL[int(i) + k])
miss = [d for d in sorted(need) if not os.path.exists(f'{VD}/viop_{d:%Y%m%d}.csv')]
print('gerekli gün', len(need), 'eksik', len(miss), [f'{d:%Y-%m-%d}' for d in miss])
for d in miss:
    url = f'https://www.borsaistanbul.com/data/vadeli/viop_{d:%Y%m%d}.csv'
    f = f'{VD}/viop_{d:%Y%m%d}.csv'
    r = subprocess.run(['curl', '-sS', '-f', '-m', '60', '-o', f + '.part', url], capture_output=True, text=True)
    if r.returncode == 0 and os.path.getsize(f + '.part') > 1000: os.replace(f + '.part', f); print('indirildi', d.date())
    else:
        print('İNDİRİLEMEDİ', d.date(), r.stderr[:120])
        if os.path.exists(f + '.part'): os.remove(f + '.part')
    time.sleep(0.4)

def parse(d):
    f = f'{VD}/viop_{d:%Y%m%d}.csv'
    if not os.path.exists(f): return None
    rows = []
    with open(f, encoding='windows-1254', errors='replace') as fh:
        rd = csv.reader(fh, delimiter=';'); hdr = [h.strip() for h in next(rd)]; next(rd)
        for r in rd:
            if len(r) < 20: continue
            rows.append(dict(zip(hdr, r)))
    df = pd.DataFrame(rows)
    def fl(x):
        try: return float(x)
        except Exception: return np.nan
    for c in ['UZLASMA FIYATI', 'ACILIS FIYATI', 'KAPANIS FIYATI', 'ISLEM MIKTARI', 'ONCEKI UZLASMA FIYATI']:
        df[c] = df[c].map(fl)
    return df

def fut(root, d0, d2):
    a, b = parse(d0), parse(d2)
    if a is None or b is None: return None
    pref = f'F_{root}'
    A = a[a['SOZLESME KODU'].str.match(rf'^{pref}\d{{4}}$')]
    if A.empty: return None
    A = A.sort_values('ISLEM MIKTARI', ascending=False).iloc[0]
    code = A['SOZLESME KODU']
    B = b[b['SOZLESME KODU'] == code]
    if B.empty: return None
    B = B.iloc[0]
    return dict(code=code, s0=A['UZLASMA FIYATI'], c0=A['KAPANIS FIYATI'], o0=A['ACILIS FIYATI'], prev_s=A['ONCEKI UZLASMA FIYATI'],
                s2=B['UZLASMA FIYATI'], c2=B['KAPANIS FIYATI'], qty0=A['ISLEM MIKTARI'])

rows = []
for _, e in rat.iterrows():
    i = int(e.react_i)
    for root in ['XU030', 'XLBNK', 'XBANK']:
        r = fut(root, CAL[i], CAL[i + 2])
        if r is None: continue
        sp = 'XU030.IS' if root == 'XU030' else 'XBANK.IS'
        rows.append(dict(react=e.react, dir=e.dir, root=root, **r,
                         fut_settle_t0_t2=-e.dir * np.log(r['s2'] / r['s0']),
                         fut_close_t0_t2=-e.dir * np.log(r['c2'] / r['c0']),
                         fut_prevsettle_t2=-e.dir * np.log(r['s2'] / r['prev_s']),
                         spot_close0_t2=-e.dir * trade(sp, i, 'close0', 2),
                         spot_open_t2=-e.dir * trade(sp, i, 'open', 2)))
F = pd.DataFrame(rows); F.to_csv(OUT + '/res_viop_futures.csv', index=False)
show = F.copy()
for c in [c for c in F.columns if c.startswith(('fut_', 'spot_'))]: show[c] = (1e4 * show[c]).round(0)
print(show.drop(columns=['s0', 'c0', 'o0', 'prev_s', 's2', 'c2']).to_string(index=False))
for root in F.root.unique():
    X = F[F.root == root]
    for col in ['fut_settle_t0_t2', 'fut_close_t0_t2', 'spot_close0_t2', 'spot_open_t2', 'fut_prevsettle_t2']:
        print(root, col, summarize(X[col], 4 if root == 'XU030' else 8))
