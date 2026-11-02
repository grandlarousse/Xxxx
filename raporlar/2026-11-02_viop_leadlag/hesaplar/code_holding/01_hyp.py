"""Hipotez güdümlü çift testleri: 6 hisse x önceden belirlenmiş sürücüler (TL ve gerekirse USD bazlı).
Çıktı: code_holding/res_hyp.csv"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hc, pandas as pd, numpy as np

H = {
 'KCHOL': ['TUPRS', 'FROTO', 'YKBNK', 'ARCLK', 'TOASO', 'AYGAZ', 'OTKAR', 'TTRAK',
           'BZ=F', 'CRACK', 'HO=F', 'CRAK', 'VLO', 'F', 'STLAM.MI', 'STLA', 'VOW3.DE', 'RNO.PA', 'WHR', 'ELUX-B.ST',
           'EURUSD=X', 'EURTRY=X', 'TRY=X', '^STOXX50E', '^GDAXI', 'ES=F', 'EEM', 'TUR', 'EUFN', 'YKBNY', 'CARZ'],
 'SAHOL': ['AKBNK', 'ENJSA', 'CIMSA', 'AKSA', 'BRISA', 'KORDS', 'AKGRT',
           'EUFN', 'KBE', 'EEM', 'TUR', 'AKBTY', 'BBVA.MC', '^TNX', 'TRY=X', 'EURTRY=X', 'ES=F', '^STOXX50E',
           'NG=F', 'TTF=F', 'HEI.DE', 'PKO.WA', 'OTP.BD', 'SBK.JO', 'ITUB', 'EMB', 'BZ=F'],
 'DOHOL': ['GWIND', 'KAREL', 'GC=F', 'SI=F', 'HG=F', 'TRY=X', 'EURTRY=X', 'ES=F', 'EEM', 'TUR', 'BTC-USD', '^VIX',
           'TTF=F', 'ICLN', 'BZ=F', 'EUFN', '^STOXX50E', 'GDX'],
 'ALARK': ['ALCAR', 'BZ=F', 'MTF=F', 'TTF=F', 'NG=F', 'BTU', 'ARCH', 'WHC.AX', 'YAL.AX', 'KRBN',
           'ACS.MC', 'FER.MC', 'HOT.DE', 'SKA-B.ST', 'VIE.PA', 'STR.VI', 'BBY.L', 'PAVE',
           'TRY=X', 'EURTRY=X', 'ES=F', 'EEM', 'TUR', '^STOXX50E', 'TUI1.DE'],
 'ENKAI': ['TRY=X', 'EURTRY=X', 'RUB=X', 'IMOEX.ME', 'BZ=F', 'TTF=F', 'NG=F', '^TNX', '^IRX', 'ES=F', '^GSPC', 'EEM', 'TUR',
           'FLR', 'KBR', 'J', 'ACS.MC', 'HOT.DE', 'SKA-B.ST', 'GC=F', 'DX-Y.NYB', '^VIX', 'EURUSD=X', 'TLT', 'SHY', 'XLE'],
 'EKGYO': ['XHB', 'ITB', '^TNX', 'TLT', 'VNA.DE', 'LEG.DE', 'VNQ', 'EMB', 'TRY=X', 'EURTRY=X', 'EEM', 'TUR', 'ES=F',
           'XBANK', 'XGMYO', 'PSGYO', 'RYGYO', '^IRX', 'HYG', 'IFRA'],
}
USD_FOR = {'ENKAI': ['TRY=X', 'RUB=X', 'BZ=F', 'TTF=F', '^TNX', 'ES=F', '^GSPC', 'EEM', 'TUR', 'FLR', 'ACS.MC', 'HOT.DE', 'GC=F', 'DX-Y.NYB', 'EURUSD=X'],
           'KCHOL': ['BZ=F', 'ES=F', 'EEM', 'TUR', '^STOXX50E', 'EURUSD=X'],
           'SAHOL': ['EUFN', 'EEM', 'TUR', 'ES=F', '^TNX'],
           'ALARK': ['BZ=F', 'MTF=F', 'TTF=F', 'EEM', 'TUR', 'ACS.MC'],
           'DOHOL': ['GC=F', 'EEM', 'TUR', 'ES=F'],
           'EKGYO': ['XHB', 'ITB', '^TNX', 'VNA.DE', 'VNQ', 'EEM', 'TUR', 'EMB']}

def T(s):
    import ll
    if s in ('CRACK',) or s in hc.RATES: return s
    if s.isupper() and len(s) <= 6 and '.' not in s and '=' not in s and '-' not in s and not s.startswith('^'):
        p = os.path.join(hc.SCR, 'data/daily', s + '.IS.parquet')
        if os.path.exists(p): return s + '.IS'
    return s

rows = []
for st, ds in H.items():
    for d in ds:
        try:
            o = hc.pair(st, T(d))
            o['driver'] = T(d); rows.append(o)
        except Exception as e:
            print('ERR', st, d, e)
    for d in USD_FOR.get(st, []):
        try:
            o = hc.pair(st, T(d), usd=True); o['driver'] = T(d); rows.append(o)
        except Exception as e:
            print('ERR usd', st, d, e)
R = pd.DataFrame(rows)
R.to_csv(os.path.join(hc.CODE, 'res_hyp.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
cols = ['stock', 'driver', 'n', 'corr_full', 'corr_3y', 'corr_1y', 'pc', 'pc_t', 'pc_IS', 'pc_OOS', 'yr_same_sign', 'yr_same_sign_pc', 'beta',
        'c_lag1', 't_lag1', 'gap_c', 'gap_t', 'intra_c', 'intra_t', 'intra_IS_t', 'intra_OOS_t', 'intra_pc', 'intra_pc_t', 'drift_t', 'c_rev', 't_rev']
print(R[cols].round(3).to_string())
