"""A1 — Senkron iddialar: corr, pc|XU100 (tam 2010+/IS 2014-20/OOS 2021-26/son 250g), yıl işareti, haftalık pc,
ortak faktör testi (XU100+USDTRY+EEM_t+EEM_{t-1} [+STOXX] [+sektör]), 250g kayan pc özeti. Çıktı: res/a1_sync.csv"""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim')
from vk import *
os.makedirs(f'{OUT}/res', exist_ok=True)
M = ret('XU100'); U = ret('TRY=X'); E = ret('EEM'); STX = ret('^STOXX'); SPX = ret('^GSPC')
CF3 = [M, U, E, E.shift(1)]
EU_DEF = ['RHM.DE', 'BA.L', 'LDO.MI', 'HO.PA', 'SAAB-B.ST', 'KOG.OL', 'HAG.DE', 'R3NK.DE']
DRV = {'EU_DEF': basket(EU_DEF, 3)}
def R(x): return DRV[x] if x in DRV else ret(x)

def roll_pc(a, b, m, w=250):
    df = pd.concat([a.rename('a'), b.rename('b'), m.rename('m')], axis=1).dropna()
    r = df.rolling(w, min_periods=int(w * 0.8))
    rab = r.corr().unstack()
    cab, cam, cbm = rab[('a', 'b')], rab[('a', 'm')], rab[('b', 'm')]
    return ((cab - cam * cbm) / np.sqrt((1 - cam ** 2) * (1 - cbm ** 2))).dropna()

def row(claim, a_sym, b_sym, sector=None, eu=False, start=FULL0, note=''):
    a = R(a_sym); b = R(b_sym)
    o = dict(claim=claim, a=a_sym, b=b_sym)
    s1y = last_n(pd.concat([a, b, M], axis=1).dropna().iloc[:, 0], 250)
    per = {'full': (start, None), 'IS': IS_, 'OOS': OOS_, '1y': (s1y, None)}
    for k, (s, e) in per.items():
        df = pd.concat([a, b], axis=1).dropna(); df = df[df.index >= pd.Timestamp(s)]
        if e: df = df[df.index <= pd.Timestamp(e)]
        o[f'corr_{k}'] = df.iloc[:, 0].corr(df.iloc[:, 1]) if len(df) > 60 else np.nan
        pc, t, n = pcorr(a, b, [M], s, e); o[f'pc_{k}'] = pc; o[f't_{k}'] = t; o[f'n_{k}'] = n
    same, tot, _ = years_sign(a, b, [M], y0=int(start[:4]), ref=o['pc_full'])
    o['yrs_same'] = f'{same}/{tot}'; o['yrs_frac'] = same / tot if tot else np.nan
    ctrl = CF3 + ([STX] if eu else [])
    for k in ['full', 'OOS', '1y']:
        s, e = per[k]; pc, t, n = pcorr(a, b, ctrl, s, e); o[f'pcCF_{k}'] = pc; o[f'tCF_{k}'] = t
    if sector:
        for sec in sector.split('+'):
            pc, t, n = pcorr(a, b, ctrl + [R(sec)], start, None); o[f'pcSEC_{sec}'] = pc; o[f'tSEC_{sec}'] = t
    # haftalık
    wa, wb, wm = weekly(a), weekly(b), weekly(M)
    pc, t, n = pcorr(wa, wb, [wm], start, None); o['pcW_full'] = pc; o['tW_full'] = t
    pc, t, n = pcorr(wa, wb, [wm], OOS_[0], None); o['pcW_OOS'] = pc
    # kayan
    rp = roll_pc(a[a.index >= pd.Timestamp(start)], b, M)
    if len(rp):
        o.update(roll_min=rp.min(), roll_med=rp.median(), roll_last=rp.iloc[-1], roll_pos=(rp > 0).mean())
    # lag1 senkron kontrol (sürücü t-1 -> hisse t, pc|XU100_t, XU100_{t-1})
    pc, t, n = pcorr(a, b.shift(1), [M, M.shift(1), a.shift(1)], start, None); o['pc_lag1'] = pc; o['t_lag1'] = t
    o['note'] = note
    return o

P = []
# K-a çimento
for x in ['CIMSA', 'OYAKC']:
    for y in ['OYAKC', 'AKCNS', 'NUHCM', 'AFYON', 'BUCIM', 'KONYA']:
        if x == y or (x == 'OYAKC' and y == 'CIMSA'): continue
        P.append(('K-a', x, y, 'XUSIN+XTAST', False))
# K-b
for y in ['BAGFS', 'HEKTS', 'EGGUB']: P.append(('K-b', 'GUBRF', y, 'XKMYA', False))
P.append(('K-c', 'TKFEN', 'ENKAI', 'XINSA+XHOLD', False))
P.append(('K-d', 'SISE', 'XBANK', 'XUSIN', False))
for x in ['BIMAS', 'ASELS']: P.append(('K-d_ref', x, 'XBANK', 'XUSIN', False))
# K-e küresel emsaller
for y in ['CF', 'NTR', 'MOS', 'YAR.OL', 'ICL', 'IPI']: P.append(('K-e', 'GUBRF', y, None, True))
for y in ['CTVA', 'FMC', 'BAYN.DE', 'UPL.NS']: P.append(('K-e', 'HEKTS', y, None, True))
for y in ['SGO.PA', 'OI', '5201.T', 'VID.MC']: P.append(('K-e', 'SISE', y, None, True))
for y in ['HEI.DE', 'HOLN.SW', 'CX', 'VMC']: P.append(('K-e', 'CIMSA', y, None, True))
for y in ['HEI.DE', 'HOLN.SW']: P.append(('K-e', 'OYAKC', y, None, True))
# O1, O2
P.append(('O1', 'ASTOR', 'EUPWR', 'XUSIN', False)); P.append(('O1', 'ASTOR', 'GESAN', 'XUSIN', False))
P.append(('O1_ref', 'EUPWR', 'GESAN', 'XUSIN', False))
for y in ['EXV5.DE', 'RNO.PA', 'STLAM.MI']: P.append(('O2', 'TOASO', y, 'XUSIN', True))
P.append(('O2_ref', 'FROTO', 'EXV5.DE', 'XUSIN', True))
# S1, S3
P.append(('S1', 'TCELL', 'TKC', 'XILTM', False)); P.append(('S1_ref', 'TTKOM', 'TKC', 'XILTM', False))
P.append(('S3', 'ASELS', 'EU_DEF', None, True))
# T1, T2, T3
P.append(('T1', 'AEFES', 'CCOLA', 'XGIDA', False))
for y in ['CARL-B.CO', 'HEIA.AS', 'ABI.BR', 'CCH.L', 'BUD']: P.append(('T2', 'AEFES', y, 'XGIDA', True))
for x in ['BIMAS', 'MGROS', 'SOKM', 'ULKER']:
    for y in ['CARL-B.CO', 'HEIA.AS', 'ABI.BR', 'CCH.L', 'BUD']: P.append(('T2_placebo', x, y, None, True))
P.append(('T3', 'ULKER', 'CC=F', 'XGIDA', False))

rows = []
for cl, a, b, sec, eu in P:
    try:
        rows.append(row(cl, a, b, sec, eu))
    except Exception as ex:
        print('HATA', cl, a, b, ex)
R1 = pd.DataFrame(rows)
R1['p_full'] = R1['t_full'].apply(p_from_t); R1['q_bh'] = bh(R1['p_full'].values)
R1.to_csv(f'{OUT}/res/a1_sync.csv', index=False)
pd.set_option('display.width', 260); pd.set_option('display.max_columns', 60)
cols = ['claim', 'a', 'b', 'corr_full', 'pc_full', 't_full', 'n_full', 'pc_IS', 'pc_OOS', 't_OOS', 'pc_1y', 'n_1y', 'yrs_same', 'pcCF_full', 'pcCF_OOS', 'pcCF_1y', 'pcW_full', 'pcW_OOS', 'roll_min', 'roll_med', 'roll_last', 'roll_pos', 'pc_lag1', 't_lag1', 'q_bh']
print(R1[cols].round(3).to_string(index=False))
sc = [c for c in R1.columns if c.startswith('pcSEC') or c.startswith('tSEC')]
print(R1[['claim', 'a', 'b'] + sc].round(3).dropna(how='all', subset=sc).to_string(index=False))
