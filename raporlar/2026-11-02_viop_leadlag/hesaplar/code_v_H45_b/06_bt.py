"""06: işlenebilirlik — spot (iddia kurgusu) vs gerçek VİOP ENKAI / KCHOL / XU030 vadelisi fiyatlarıyla backtest.
(b) pos = -sign(z(TUR_{t-1})) |z|>thr ; (c) pos = sign(z(USD_{t-1})) |z|>thr.  Sinyaller 06:30 UTC'den önce bilinir.
Vadeli hedefleri: VWAP->uzlaşma (gün boyu VWAP algoritmasıyla giriş, uzlaşma fiyatından çıkış), ve Fo->Fc (yalnız 2024-11-19+; öncesinde
pay vadelisi akşam seansı olasılığı nedeniyle Fo, TUR kapanışından önce olabilir).
"""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *
import importlib.util
def _imp(n, f):
    s = importlib.util.spec_from_file_location(n, OUT + '/' + f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
f02 = _imp('f02', '02_futaudit.py'); r01 = _imp('r01', '01_repro.py')

E = bist('ENKAI'); X30 = bist('XU030'); K = bist('KCHOL')
tur, _, _ = us_lag('TUR'); usd, _ = fx_lag('TRY=X')
FE = f02.front('ENKAI'); FX = f02.front('XU030'); FK = f02.front('KCHOL')
for F in (FE, FX, FK):
    F['vw_s'] = np.log(F.Fs / F.Fvw); F['o_c'] = np.log(F.Fc / F.Fo); F['o_s'] = np.log(F.Fs / F.Fo)
avail = pd.Series(E.index.isin(FE.index), E.index)

def line(lab, pos, tgt, cost, start=T0, mask=None):
    p = pos if mask is None else pos.where(mask, 0)
    r, pnl = bt(p, tgt, cost, start)
    s = ' | '.join(f"{k} n {r[k][0]} {r[k][1]:+.1f} t {r[k][2]:+.2f}" for k in ('IS', 'OOS', 'ALL'))
    print(f'  {lab:52s} {cost:2d}bps: {s}')
    return r, pnl

out = []
for nm, raw, sgn in [('(b) -TUR', tur, -1), ('(c) USD', usd, +1)]:
    z = zsig(raw)
    for thr in (1.0, 2.0):
        pos = (sgn * np.sign(z)).where(z.abs() > thr, 0).fillna(0)
        print(f'\n=== {nm} z>{thr} ===')
        r, pnl = line('spot müzayede->kapanış (tüm)', pos, E['intra'], 8)
        yr = r['yr']; print('    yıllar:', yr)
        # long / short bacak
        for leg, m in [('LONG', pos > 0), ('SHORT', pos < 0)]:
            line(f'spot, yalnız {leg} bacak', pos, E['intra'], 8, mask=m)
        line('spot, vadeli MEVCUT günler', pos, E['intra'], 8, mask=avail)
        line('spot, vadeli YOK günler (2021-06..2023-04)', pos, E['intra'], 8, mask=~avail)
        line('ENKAI vadeli VWAP->uzlaşma (mevcut günler)', pos, FE['vw_s'].reindex(E.index), 8)
        line('ENKAI vadeli VWAP->uzlaşma', pos, FE['vw_s'].reindex(E.index), 0)
        line('ENKAI vadeli Fo->Fc (2024-11-19+)', pos, FE['o_c'].reindex(E.index), 8, start=pd.Timestamp('2024-11-19'))
        line('spot aynı günler (2024-11-19+)', pos, E['intra'], 8, start=pd.Timestamp('2024-11-19'))
        line('XU030 vadeli VWAP->uzlaşma (3bps)', pos, FX['vw_s'].reindex(E.index), 3)
        # ENKAI - XU030 hedge'li (vadeli, VWAP), maliyet 8+3
        hed = FE['vw_s'].reindex(E.index) - FX['vw_s'].reindex(E.index)
        line('ENKAI-XU030 vadeli VWAP hedge (11bps)', pos, hed, 11)
        # en büyük 10 gün payı (spot, OOS)
        p = pnl[pnl.index >= SPLIT]
        if len(p) > 20:
            top = p.sort_values(ascending=False).head(10).sum() / p.sum() if p.sum() > 0 else np.nan
            print(f'    spot OOS: en iyi 10 günün toplam kâra oranı {top:.2f}; en iyi 10 gün: {[d.date().isoformat() for d in p.sort_values(ascending=False).head(5).index]}')

# (a) vadeli-tabanlı türev sinyal (sigF = NAVgap - vadeli ilk işlem gap'i) -> vadeli VWAP->uzlaşma. VWAP 06:30-07:00 sinyal-öncesi işlemleri
# içerdiği için iyimser yanlı.
print('\n=== (a) türev: sigF = NAVgap - KCHOL vadeli Fo gap -> KCHOL vadeli VWAP->uzlaşma (iyimser yanlı) ===')
nav = r01.basket_gap(r01.W)
sigF = (nav - np.log(FK.Fo / FK.Fps).reindex(K.index))
roll = (FK["code"] != FK["code"].shift(1)).reindex(K.index).fillna(True).astype(bool)
sigF = sigF.where(~roll)
z = zsig(sigF); pos = np.sign(z).where(z.abs() > 0.5, 0).fillna(0)
for c in (0, 8):
    line('sigF z>0.5 -> KCHOL vadeli VWAP->uzlaşma 2020+', pos, FK['vw_s'].reindex(K.index), c, start=pd.Timestamp('2020-01-01'))
sig = nav - K['gap']; z = zsig(sig); pos = np.sign(z).where(z.abs() > 0.5, 0).fillna(0)
line('iddia sig z>0.5 -> KCHOL vadeli VWAP->uzlaşma 2020+', pos, FK['vw_s'].reindex(K.index), 8, start=pd.Timestamp('2020-01-01'))
line('iddia sig z>0.5 -> spot müzayede->kapanış 2014+', pos, K['intra'], 8)
line('iddia sig z>0.5 -> spot müzayede->kapanış 2014+', pos, K['intra'], 15)
