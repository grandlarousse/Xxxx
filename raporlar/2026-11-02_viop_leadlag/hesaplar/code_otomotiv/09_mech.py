"""Sürpriz mekanizma testi: ON->FROTO (otomotiv yarı iletken kanalı?) ve XHB/ITB->DOAS (faiz/kredi kanalı?). Kardeş sürücüler aynı işareti veriyor mu?
Çıktı: res/mech.csv"""
from common import *
S = pd.read_csv(os.path.join(RES, 'scan_all.csv'))
q = S[(S.family == 'lead_intra_pc') & (((S.stock == 'FROTO') & S.driver.isin(['ON', 'NXPI', 'IFX.DE', 'STM', 'SMH', '^SOX', 'NVDA', 'TSLA', 'F', 'GM', 'APTV', 'ALV', 'BWA']))
      | ((S.stock == 'DOAS') & S.driver.isin(['XHB', 'ITB', '^TNX', 'TLT', 'ZN=F', 'IEF', 'KBE', 'KRE', 'IWM', 'VNQ', 'XRT', 'XLY'])))]
print(q[['stock', 'driver', 'r', 'n', 't_iid', 'p_bh']].round(3).to_string(index=False))
xg = D('XU100')['gap']; dD = D('DOAS'); dF = D('FROTO'); spx1 = R('^GSPC').shift(1)
rows = []
for nm, y, x, c in [('XHB1->DOAS | +TNX1', dD['intra'], R('XHB').shift(1), [xg, dD['gap'], spx1, R('^TNX').shift(1)]),
                    ('TNX1->DOAS', dD['intra'], R('^TNX').shift(1), [xg, dD['gap'], spx1]),
                    ('XHB1->FROTO', dF['intra'], R('XHB').shift(1), [xg, dF['gap'], spx1]),
                    ('XHB1->TOASO', D('TOASO')['intra'], R('XHB').shift(1), [xg, D('TOASO')['gap'], spx1]),
                    ('ON1->FROTO | +NXPI1,IFX1', dF['intra'], R('ON').shift(1), [xg, dF['gap'], spx1, R('NXPI').shift(1), R('IFX.DE').shift(1)]),
                    ('ON1->TOASO', D('TOASO')['intra'], R('ON').shift(1), [xg, D('TOASO')['gap'], spx1])]:
    pc, t, n = pcorr(y, x, c); rows.append({'test': nm, 'pc': pc, 't': t, 'n': n})
M_ = pd.DataFrame(rows); M_.to_csv(os.path.join(RES, 'mech.csv'), index=False); print(M_.round(3).to_string(index=False))
