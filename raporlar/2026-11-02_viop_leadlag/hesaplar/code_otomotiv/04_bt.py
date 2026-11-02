"""Backtestler (look-ahead yok): sinyal BIST açılışından ÖNCE bilinir, pozisyon açılış->kapanış (intra_t) kazanır.
Maliyet 8 ve 15 bps gidiş-dönüş. IS 2014-2020 / OOS 2021+ (ASTOR: örneklem ortası).
Çıktı: res/bt.csv"""
from common import *

def avg(syms, L):
    return pd.concat([R(s).shift(L) for s in syms], axis=1).mean(axis=1, skipna=False)

def intra_basket(stocks):
    return pd.concat([D(s)['intra'] for s in stocks], axis=1).mean(axis=1)

EXP = ['FROTO', 'TOASO', 'ARCLK', 'VESTL']
grid_kr = ['267260.KS', '298040.KS', '010120.KS']
tests = [
  ('BT1a F_{t-1} -> FROTO intra_t', R('F').shift(1), D('FROTO')['intra'], SPLIT),
  ('BT1b mean(F,STLA)_{t-1} -> TOASO intra_t', avg(['F', 'STLA'], 1), D('TOASO')['intra'], SPLIT),
  ('BT1c EXV5.DE(Avrupa oto)_{t-1} -> TOASO intra_t', R('EXV5.DE').shift(1), D('TOASO')['intra'], SPLIT),
  ('BT1d EXV5.DE_{t-1} -> FROTO intra_t', R('EXV5.DE').shift(1), D('FROTO')['intra'], SPLIT),
  ('BT2a Kore şebeke sepeti_t (lag0) -> ASTOR intra_t', avg(grid_kr, 0), D('ASTOR')['intra'], None),
  ('BT2b Kore şebeke sepeti_t (lag0) -> ASTOR gap_t [işlenemez, referans]', avg(grid_kr, 0), D('ASTOR')['gap'], None),
  ('BT2c GEV/ETN/VRT ort._{t-1} -> ASTOR intra_t', avg(['ETN', 'VRT', 'HUBB'], 1), D('ASTOR')['intra'], None),
  ('BT3a EURUSD_{t-1} -> ihracatçı sepeti intra_t', R('EURUSD=X').shift(1), intra_basket(EXP), SPLIT),
  ('BT3b USDTRY_{t-1} -> ihracatçı sepeti intra_t', R('TRY=X').shift(1), intra_basket(EXP), SPLIT),
  ('BT3c EURTRY_{t-1} -> FROTO intra_t', R('EURTRY=X').shift(1), D('FROTO')['intra'], SPLIT),
  ('BT4a KOSPI_t (lag0) -> TOASO intra_t', R('^KS11').shift(0), D('TOASO')['intra'], SPLIT),
  ('BT4b Samsung_t (lag0) -> VESTL intra_t', R('005930.KS').shift(0), D('VESTL')['intra'], SPLIT),
  ('BT4c LG Elec_t (lag0) -> ARCLK intra_t', R('066570.KS').shift(0), D('ARCLK')['intra'], SPLIT),
  ('BT4d LG Display_t (lag0) -> VESTL intra_t', R('034220.KS').shift(0), D('VESTL')['intra'], SPLIT),
]
rows = []
for name, sig, tgt, sp in tests:
    if sp is None:
        sp_, _ = split_for(tgt, sig); sp = str(sp_.date())
    res = bt(sig, tgt, costs=(0, 8, 15), split=sp)
    for c in (0, 8, 15):
        r = bt_row(name, res, c); r['split'] = sp; rows.append(r)
B = pd.DataFrame(rows); B.to_csv(os.path.join(RES, 'bt.csv'), index=False)
c = ['test', 'cost_bps', 'IS_n', 'IS_mean_bps', 'IS_t', 'IS_sharpe', 'OOS_n', 'OOS_mean_bps', 'OOS_t', 'OOS_sharpe', 'OOS_hit']
print(B[B.cost_bps.isin([0, 8])][c].round(2).to_string(index=False))
