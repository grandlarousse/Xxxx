"""A6 — küçük ek kontroller: T2 2014+ replikasyonu (XU100+STOXX+SPX), K-a IS/OOS t'leri, FDR sayımı, SISE–XBANK son 250g ortak faktör."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim')
from vk import *
M = ret('XU100'); STX = ret('^STOXX'); SPX = ret('^GSPC')
print('T2 AEFES – bira, pc|XU100+STOXX+SPX:')
for b in ['CARL-B.CO', 'HEIA.AS', 'ABI.BR', 'CCH.L', 'BUD']:
    r = [f'{s[:4]}-{(e or "2026")[:4]} {pcorr(ret("AEFES"), ret(b), [M, STX, SPX], s, e)[0]:.3f}' for s, e in [('2010-01-01', None), ('2014-01-01', None), IS_, OOS_]]
    print(' ', b, ' | '.join(r))
A1 = pd.read_csv(f'{OUT}/res/a1_sync.csv')
print('\nK-a IS/OOS t:'); print(A1[A1.claim == 'K-a'][['a', 'b', 'pc_IS', 't_IS', 'pc_OOS', 't_OOS', 'pc_1y', 't_1y']].round(2).to_string(index=False))
main = A1[~A1.claim.str.contains('placebo')]
print(f'\nFDR: {len(A1)} senkron test (plasebo dahil); q<0,05 geçen {int((A1.q_bh < 0.05).sum())}; plasebo hariç {len(main)} testte {int((main.q_bh < 0.05).sum())}; plasebo {int((A1[A1.claim.str.contains("placebo")].q_bh < 0.05).sum())}/20')
print(A1[(A1.q_bh < 0.05) & A1.claim.isin(['K-e', 'T2', 'S3', 'O2', 'T3'])][['claim', 'a', 'b', 'pc_full', 't_full', 'q_bh']].round(3).to_string(index=False))
# SISE–XBANK son 250g işaret dönüşü: genel mi?
print('\nSon 250g pc|XU100 ~ XBANK (sanayi/defansif hisseler):')
for s in ['SISE', 'BIMAS', 'ASELS', 'TUPRS', 'EREGL', 'FROTO', 'TCELL', 'AEFES', 'CIMSA', 'KCHOL']:
    st = last_n(pd.concat([ret(s), ret('XBANK'), M], axis=1).dropna().iloc[:, 0], 250)
    p = pcorr(ret(s), ret('XBANK'), [M], st, None); pf = pcorr(ret(s), ret('XBANK'), [M], FULL0, None)
    print(f'  {s}: tam {pf[0]:+.3f} | son 250g {p[0]:+.3f} (t {p[1]:.1f})')
