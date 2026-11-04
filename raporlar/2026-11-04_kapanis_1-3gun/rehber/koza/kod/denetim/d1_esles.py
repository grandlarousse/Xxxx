"""(1) Bağımsız z3 vs betik vs araştırma — son 300 BIST günü."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/kod')
import bag
B, D = bag.signal(upto='2026-11-03')
B.to_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/bag_sig.parquet')
# betik: kendi fetch'i ile (ayrı süreçte üretilen dosya)
S = pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/betik_sig.parquet')
Z0 = pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_rehber_koza/z3_arastirma.parquet')
last300 = B.index[-300:]
print('Son 300 BIST günü:', last300[0].date(), '→', last300[-1].date())
for nm, Z in [('betik', S.z3), ('araştırma (c2/curlib, veri 30.10)', Z0.z3)]:
    c = last300.intersection(Z.index)
    a = B.z3.reindex(c); b = Z.reindex(c)
    both = a.notna() & b.notna()
    sa = np.where(a.abs() > 1.5, np.sign(a), 0); sb = np.where(b.abs() > 1.5, np.sign(b), 0)
    print(f'  {nm}: ortak gün {len(c)}, ikisi de z3 geçerli {both.sum()}, NaN uyumu {(a.isna() == b.isna()).mean():.4f}, '
          f'maks|Δz3| {(a - b).abs().max():.2e}, sinyal uyumu {(sa == sb).mean():.4f}, sinyal günleri bağımsız {int((sa != 0).sum())} / {nm} {int((sb != 0).sum())}')
    for col in ['b_g', 'bH']:
        cc = {'b_g': 'b_g', 'bH': 'bH' if nm == 'betik' else 'bTA'}[col]
        src = S if nm == 'betik' else Z0
        print(f'     {col}: maks|Δ| {(B[col].reindex(c) - src[cc].reindex(c)).abs().max():.2e}')
# tam geçmiş uyum
c = B.index.intersection(Z0.index); a = B.z3.reindex(c); b = Z0.z3.reindex(c)
print('Tam geçmiş araştırma ile: gün', len(c), 'maks|Δz3|', f'{(a-b).abs().max():.2e}', 'NaN uyumu', f'{(a.isna()==b.isna()).mean():.4f}',
      'sinyal uyumu', f"{((a.abs()>1.5)==(b.abs()>1.5)).mean():.4f}")
c = B.index.intersection(S.index); a = B.z3.reindex(c); b = S.z3.reindex(c)
print('Tam geçmiş betik ile: gün', len(c), 'maks|Δz3|', f'{(a-b).abs().max():.2e}', 'NaN uyumu', f'{(a.isna()==b.isna()).mean():.4f}')
# NaN z3 günleri son 300
nanz = last300[B.z3.reindex(last300).isna().values]
print('Son 300 günde z3 NaN günler:', [d.date() for d in nanz])
print('Son 300 günde sinyal günleri:', ' '.join(f"{d.date()}{'+' if s>0 else '-'}" for d, s in B.sig.reindex(last300).items() if s != 0))
print(B.tail(6)[['u','sd60','z3','b_g','bH']].round(4))
