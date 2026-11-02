"""v_YA1_a — aynı olaylarda vadeli (bülten) ve spot (h1) giriş karşılaştırması: TC/TU VİOP47, 2023-11-30+.
Vadeli açılış (~09:30 ilk işlem) spot açılış seansından (09:55) önce; spot 10:30 fiyatı vadeli 10:30'un vekili (gün-içi corr ~0,9).
"""
import numpy as np, pandas as pd, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v5_h1 import st
EV = pd.read_parquet(HERE + '/_ev_viop.parquet')
H = pd.read_parquet(HERE + '/_ev_h1.parquet')[['stock', 'date', 'p1030', 'o1', 'cl1', 'open_match', 'f1030', 'o_to_1030']]
for c in ['TC', 'TU']: pass
M = EV.merge(H, on=['stock', 'date'], how='inner')
M = M[M.open_match & M.p1030.notna() & (M.f1_qty.fillna(0) > 0)]
# vadeli bazı: t+1 vadeli açılış / t vadeli kapanış vs spot gap
M['basis_open'] = np.log(M.f1_open / M.o1) - np.log(M.f0_close / (M.o1 / np.exp(M.gap_1)))  # (F_open/S_open) - (F_close_t/S_base_t) ~ açılışta baz değişimi
M['basis_close'] = np.log(M.f1_close / M.cl1) - np.log(M.f0_close / (M.o1 / np.exp(M.gap_1)))
for nm in ['TC', 'TU']:
    s = M[M[nm]]
    print(f'\n{nm} VİOP47, vadeli+h1 ortak olay n={len(s)} ({s.date.min().date()}..{s.date.max().date()})  [SAT pozisyonu brüt bps]')
    print('  vadeli açılış->vadeli kapanış :', st(-s.fint1, s.date))
    print('  spot açılış  ->spot kapanış   :', st(-s.intra_1, s.date))
    print('  spot 10:30   ->spot kapanış   :', st(-s.f1030, s.date))
    print('  spot açılış  ->spot 10:30     :', st(-s.o_to_1030, s.date))
    print('  baz değişimi (vadeli/spot) açılış anında, medyan bps:', round(1e4 * s.basis_open.median(), 1), ' kapanışta:', round(1e4 * s.basis_close.median(), 1))
    print('  vadeli t+1 açılış seansı/ilk işlem ~ spot açılışa göre (log Fo/So - log Fc/Sc) medyan bps:', round(1e4 * (s.basis_open - s.basis_close).median(), 1), ' ort:', round(1e4 * (s.basis_open - s.basis_close).mean(), 1))
    print('  vadeli 10:30 vekili -> kapanış @15+tik:', st(-s.f1030 - 0.01 / s.f1_close, s.date, 15), ' | @30+tik:', st(-s.f1030 - 0.01 / s.f1_close, s.date, 30), '| @8+tik', st(-s.f1030 - 0.01 / s.f1_close, s.date, 8))
    print('  t+1 vadeli işlem tutarı (TL) medyan:', round(s.f1_qty.median() * 100 * s.f1_close.median() / 1e6, 1), 'mn TL (yaklaşık, çarpan 100)')
