"""Mıknatıs (magnet) etkisi: fiyat limite yaklaşınca limite doğru hızlanma var mı? Saatlik (h1, 2023-11+) BIST hisseleri.
Başlangıç: bir saatlik bar kapanışında önceki güne göre getiri L0 aralığında (yakın: +%7..+%8; plasebo: +%3..+%4, ayna: -%7..-%8 / -%3..-%4).
Sonuç: aynı gün kalan barlarda önce hangi bariyer görülür: üst (+%9,8 ~ limit / plasebo +%6,8) mi alt (L0 - %3) mı? Aynı barda ikisi birden -> belirsiz (hariç).
Martingal altında P(üst önce) ~ %50 (simetrik mesafe). Mıknatıs -> yakın grupta P(üst) plasebodan belirgin yüksek."""
import numpy as np, pandas as pd, glob, os, alib
from alib import ll
files = [f for f in glob.glob(alib.SCR + '/data/h1/*.IS.parquet') if not os.path.basename(f).startswith('X')]
prev_close = {}
res = []
for f in files:
    sym = os.path.basename(f)[:-8]
    h = pd.read_parquet(f); h = h[h.index >= '2023-11-01']
    if len(h) < 500: continue
    k = sym.replace('.IS', '')
    try:
        d = ll.raw(sym).copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
    except Exception: continue
    pc = d['c'].shift(1)
    h = h.copy(); h['day'] = h.index.tz_convert(None).normalize(); h['pc'] = pc.reindex(h.day).values
    h = h.dropna(subset=['pc'])
    for day, g in h.groupby('day'):
        if len(g) < 4: continue
        rc = (g.c / g.pc - 1).values; rh = (g.h / g.pc - 1).values; rl = (g.l / g.pc - 1).values
        for side in [1, -1]:
            for lab, lo, hi_, up_b in [('near', 0.07, 0.08, 0.098), ('placebo', 0.03, 0.04, 0.068)]:
                idx = np.where((side * rc[:-1] >= lo) & (side * rc[:-1] < hi_))[0]
                if not len(idx): continue
                i = idx[0]; start = side * rc[i]; dn_b = start - 0.03
                if lab == 'placebo': up_b = start + 0.03
                else: up_b = 0.098  # limit; mesafe start'a göre 1,8..2,8 puan (alt bariyer 3 puan) -> martingal P(üst) > %50 beklenir
                out = 'none'
                for j in range(i + 1, len(g)):
                    hu = (side * rh[j] >= up_b) if side == 1 else (side * rl[j] >= up_b)
                    hd = (side * rl[j] <= dn_b) if side == 1 else (side * rh[j] <= dn_b)
                    if hu and hd: out = 'both'; break
                    if hu: out = 'up'; break
                    if hd: out = 'down'; break
                res.append(dict(sym=k, day=day, side=side, grp=lab, start=start, up_dist=up_b - start, out=out, viop=k in alib.VIOP))
R = pd.DataFrame(res); R.to_csv('res_magnet.csv', index=False)
for side in [1, -1]:
    for lab in ['near', 'placebo']:
        s = R[(R.side == side) & (R.grp == lab)]; s2 = s[s.out.isin(['up', 'down'])]
        pu = (s2.out == 'up').mean() if len(s2) else np.nan
        # martingal (Brownian, sürüklenmesiz) altında P(üst önce) = alt_mesafe/(alt+üst)
        pm = (0.03 / (0.03 + s2.up_dist)).mean() if len(s2) else np.nan
        print('yön', side, lab, 'n', len(s), 'kesin', len(s2), 'P(üst önce)=%.3f  martingal beklenen=%.3f  hiçbiri=%.2f ikisi=%.2f' % (pu, pm, (s.out == 'none').mean(), (s.out == 'both').mean()))
