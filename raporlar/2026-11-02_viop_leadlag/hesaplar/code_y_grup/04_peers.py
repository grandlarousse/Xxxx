"""Sektör emsali (grup bağı YOK) yüksek korelasyonlu çiftler: grup çiftlerindeki 'açılış ayrışması -> gün içi yakalama' (g2i) etkisinin
grup bağına mı yoksa sadece yüksek korelasyon + likidite farkına mı bağlı olduğunu ayırmak için kontrol kümesi."""
from gx import *
import importlib.util
spec = importlib.util.spec_from_file_location('p2', HERE + '/02_pairs.py'); p2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p2)
PEERS = [('GARAN','AKBNK'),('GARAN','YKBNK'),('AKBNK','YKBNK'),('GARAN','ISCTR'),('AKBNK','ISCTR'),('YKBNK','ISCTR'),('GARAN','TSKB'),('AKBNK','ALBRK'),('GARAN','SKBNK'),
 ('EREGL','KRDMD'),('ISDMR','KRDMD'),('CIMSA','OYAKC'),('AKCNS','OYAKC'),('OYAKC','NUHCM'),('CIMSA','NUHCM'),('BIMAS','MGROS'),('MGROS','SOKM'),('BIMAS','SOKM'),
 ('THYAO','PGSUS'),('TCELL','TTKOM'),('FROTO','DOAS'),('TOASO','DOAS'),('ASTOR','EUPWR'),('AKSEN','ODAS'),('ZOREN','AKSEN'),('ENJSA','AKSEN'),('PETKM','SASA'),
 ('TUPRS','PETKM'),('ALARK','ENKAI'),('TKFEN','ENKAI'),('HEKTS','GUBRF'),('ARCLK','VESTL'),('ARCLK','VESBE'),('ANSGR','AKGRT'),('ANHYT','AGESA'),('TURSG','AKGRT'),
 ('EKGYO','ISGYO'),('ISMEN','GLBMD'),('KCHOL','SAHOL'),('KCHOL','DOHOL'),('SAHOL','AGHOL'),('KCHOL','AGHOL'),('GUBRF','BAGFS'),('TRALT','PETKM'),('AEFES','ULKER'),('CCOLA','ULKER'),
 ('TAVHL','PGSUS'),('ISCTR','HALKB'),('ISCTR','VAKBN'),('GARAN','VAKBN'),('BRSAN','EREGL'),('BRSAN','KRDMD'),('KORDS','BRISA'),('OTKAR','ASELS'),('TTRAK','FROTO')]
rows = []
for x, y in PEERS:
    for (a, b) in [(x, y), (y, x)]:
        try:
            o = p2.lead_stats(a, b, ''); A, B = R(a), R(b); df = pd.concat([A, B, R('XU100')], axis=1).dropna(); df = df[df.index >= '2010-01-01']
            o['pc'] = ll.partial_corr(df.iloc[:, 0], df.iloc[:, 1], [df.iloc[:, 2]])[0]
            o.update(dict(x=a, y=b, liq_x=liq(a, '2021-01-01')[0], liq_y=liq(b, '2021-01-01')[0])); rows.append(o)
        except Exception as e: print('ERR', a, b, e)
P = pd.DataFrame(rows); P.to_csv(HERE + '/res_peers.csv', index=False)
print(P[['x','y','pc','g2i_t','g2i_t_IS','g2i_t_OOS','l1_intra_t']].round(2).to_string())
