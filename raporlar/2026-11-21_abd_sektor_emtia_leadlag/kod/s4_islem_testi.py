import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, ortak
H = ortak.hizali_getiri
def z(x): return ortak.zskor(x, 60, 40)
vix = np.log(ortak.oku('^VIX')['close']).diff().reindex(ortak.takvim())
testler = {
 'ZL z>1 al ADM': ((z(H('ZL=F')) > 1).astype(float), 'ADM'),
 'ZL z>1 al BG': ((z(H('ZL=F')) > 1).astype(float), 'BG'),
 'ZL z<-1 sat BG': (-(z(H('ZL=F')) < -1).astype(float), 'BG'),
 'ZL |z|>1 yon BG': (np.sign(z(H('ZL=F'))).where(z(H('ZL=F')).abs() > 1, 0), 'BG'),
 'ZL |z|>1 yon ADM': (np.sign(z(H('ZL=F'))).where(z(H('ZL=F')).abs() > 1, 0), 'ADM'),
 'ZS |z|>1 yon BG': (np.sign(z(H('ZS=F'))).where(z(H('ZS=F')).abs() > 1, 0), 'BG'),
 'VIX z>1.5 al XBI': ((z(vix) > 1.5).astype(float), 'XBI'),
 'VIX z>1.5 al XLV': ((z(vix) > 1.5).astype(float), 'XLV'),
 'XLV z<-1.5 al XLV': ((z(H('XLV')) < -1.5).astype(float), 'XLV'),
 'XLP z<-1.5 al XLP': ((z(H('XLP')) < -1.5).astype(float), 'XLP'),
 'XBI z<-1.5 al XBI': ((z(H('XBI')) < -1.5).astype(float), 'XBI'),
 'XLP z<-1.5 al XLV': ((z(H('XLP')) < -1.5).astype(float), 'XLV'),
 'IWM z<-1.5 al XBI': ((z(H('IWM')) < -1.5).astype(float), 'XBI'),
 'UUP z>1.5 sat XLP': (-(z(H('UUP')) > 1.5).astype(float), 'XLP'),
 'UNH z<-2 al HUM': ((z(H('UNH')) < -2).astype(float), 'HUM'),
 'HE z>1 al TSN': ((z(H('HE=F')) > 1).astype(float), 'TSN'),
 'CC z>1.5 sat HSY': (-(z(H('CC=F')) > 1.5).astype(float), 'HSY'),
}
kol = ['is_n','is_net_bps','is_t_anormal','oos_n','oos_net_bps','oos_t_anormal','son_n','son_net_bps','son_t_anormal']
sat = []
for ad, (s, hdf) in testler.items():
    for h in (1, 3):
        r = ortak.donemli_test(s, hdf, h=h, maliyet_bps=5)
        pl = ortak.plasebo(s, hdf, h) if h == 1 else {}
        sat.append(dict(test=ad, h=h, **{k: r.get(k) for k in kol}, plasebo=list(pl.values())))
d = pd.DataFrame(sat); pd.set_option('display.width', 250)
d.to_csv(os.path.join(ortak.KOK, 'ek', 'hipotez', 's4_islem_testi.csv'), index=False)
print(d.to_string(index=False))
print(ortak.yillik_tablo(np.sign(z(H('ZL=F'))).where(z(H('ZL=F')).abs() > 1, 0), 'BG', 1).tail(10))
