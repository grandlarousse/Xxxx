"""Hipotez güdümlü çift testleri: 6 hisse x önceden belirlenmiş sürücüler. Çıktı: res/hyp_pairs.csv
Çalıştır: python3 01_hyp.py"""
from common import *
import time

HYP = {
 'FROTO': ['F','GM','STLA','STLAM.MI','RNO.PA','VOW3.DE','MBG.DE','BMW.DE','DTG.DE','VOLV-B.ST','8TRA.DE','IVG.MI','PCAR','CMI',
           'CARZ','EXV5.DE','^STOXX','^GDAXI','EURUSD=X','EURTRY=X','TRY=X','7203.T','005380.KS','000270.KS','CON.DE','HG=F','ALI=F','MT',
           'TOASO.IS','DOAS.IS','KCHOL.IS','OTKAR.IS','TTRAK.IS','XUSIN.IS'],
 'TOASO': ['STLAM.MI','STLA','RNO.PA','VOW3.DE','F','EXV5.DE','^STOXX','FTSEMIB.MI','EURUSD=X','EURTRY=X','TRY=X','7203.T','005380.KS',
           'FROTO.IS','DOAS.IS','KCHOL.IS','XBANK.IS','XUSIN.IS'],
 'DOAS':  ['VOW3.DE','P911.DE','PAH3.DE','MBG.DE','BMW.DE','EXV5.DE','^GDAXI','^STOXX','EURTRY=X','EURUSD=X','TRY=X',
           'FROTO.IS','TOASO.IS','XBANK.IS','XUSIN.IS','XU030.IS'],
 'ARCLK': ['WHR','ELUX-B.ST','6752.T','066570.KS','6690.HK','0300.HK','HSHCY','000333.SZ','000651.SZ','600690.SS','KWEB','FXI','MCHI',
           'HRC=F','MT','SLX','HG=F','EURUSD=X','EURTRY=X','TRY=X','^STOXX','XHB','ITB','VESTL.IS','KCHOL.IS','FROTO.IS','XUSIN.IS'],
 'VESTL': ['034220.KS','LPL','066570.KS','005930.KS','6758.T','SONY','6752.T','2409.TW','3481.TW','000725.SZ','000100.SZ','1070.HK',
           '0921.HK','0751.HK','^SOX','SMH','GLW','WHR','ELUX-B.ST','EURUSD=X','EURTRY=X','TRY=X','^STOXX','ARCLK.IS','XUSIN.IS'],
 'ASTOR': ['ENR.DE','GEV','ETN','HUBB','VRT','POWL','NVT','AYI','267260.KS','298040.KS','010120.KS','103590.KS','006260.KS','SIE.DE',
           'ABBN.SW','SU.PA','PRY.MI','NKT.CO','6501.T','6503.T','6504.T','HPS-A.TO','POWERINDIA.NS','SWDY.CA','GRID','HG=F','ALI=F',
           'BTC-USD','ETH-USD','^SOX','NVDA','SMH','TRY=X','EURUSD=X','EUPWR.IS','GESAN.IS','CWENE.IS','SMRTG.IS','ALFAS.IS',
           'KONTR.IS','YEOTK.IS','XUSIN.IS'],
}

if __name__ == '__main__':
    rows = []; t0 = time.time()
    for st, drs in HYP.items():
        for dr in drs:
            try:
                o = pair_stats(st, dr, start='2010-01-01')
            except Exception as e:
                print('ERR', st, dr, e); continue
            rows.append(o)
        print(st, 'done', round(time.time() - t0, 1), 's', flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RES, 'hyp_pairs.csv'), index=False)
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
    cols = ['stock','driver','n','c_full','c_3y','c_1y','c_lag1','pc_xu100','pc_xu100_usd','c_usd','beta','c_IS','c_OOS','pc_IS','pc_OOS',
            'yr_same_sign','rev_t','lead_lag','gap_c','gap_t','intra_c','intra_t','intra_t_IS','intra_t_OOS','intra_pc_t','drift_t']
    print(df[cols].round(3).to_string())
