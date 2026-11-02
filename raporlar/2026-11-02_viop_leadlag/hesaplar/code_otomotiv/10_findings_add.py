"""05_findings.py çıktısını (../f_otomotiv.csv) 03/06/07/08/09 sonuçlarıyla günceller (05'ten SONRA çalıştır)."""
import pandas as pd, numpy as np, os
F = pd.read_csv('../f_otomotiv.csv')
def upd(st, dr, rel, **kw):
    i = (F.stock == st) & (F.driver_yahoo == dr) & (F.relation == rel)
    for k, v in kw.items(): F.loc[i, k] = v
upd('ASTOR', 'SU.PA', 'regime', confidence='ORTA', notes='07_regime: corr 2023-24 -0,04 -> 2025-26 0,25 (Fisher z=4,4); pc -0,13 -> +0,13 (z=4,0); sepet (SU,ABBN,ETN,SIE,HD Hyundai,Hyosung) corr -0,01 -> 0,26 (z=4,2); 250g kayan corr son değer 0,32 = tarihi max; kısa post örneklem (~450g)')
upd('ASTOR', 'EUPWR.IS', 'sync', notes='pc|XU100 0,37; 2023-24 pc 0,45 -> 2025-26 0,29 (z=-2,8): yerel tema zayıflıyor, küresel tema güçleniyor; 250g kayan corr min 0,39')
upd('ARCLK', 'KRDMB.IS', 'lead_intra', confidence='ÇOK DÜŞÜK', notes='09/08: ARCLK_{t-1}, XU100_{t-1}, KRDMD_{t-1} kontrolünde t=-2,4, OOS -1,2 -> BIST içi tersine dönüş/likidite artefaktı')
upd('DOAS', 'XHB', 'lead_intra', confidence='DÜŞÜK', mechanism='ABD tüketici döngüsel risk iştahı (faiz kanalı DEĞİL)',
    notes='SPX1/IWM1/EEM1/TNX1 kontrollerinde t=3,4 (IS 2,7/OOS 2,2); ITB t=3,3, XLY t=3,1 aynı işaret; TNX/TLT/ZN ≈ 0 -> faiz kanalı yok; XU100 gün-içi etkisi yok (t=-0,3) -> DOAS’a özgü; FDR (lead_intra_pc, 7.044 test) geçti')
upd('TOASO', 'STLAM.MI', 'regime', confidence='DÜŞÜK', notes='07: RK onayı 18.04.2025 öncesi/sonrası: STLAM corr 0,11 -> 0,22 (z=1,7, p=0,10), pc 0,02 -> 0,08 (p=0,39); USDTRY corr +0,12 -> -0,02 (p=0,03, ithalatçı yönüne kayış; pc farkı p=0,38); FROTO/DOAS bağı değişmedi')
upd('ASTOR', '267260.KS', 'lead_intra', notes='BT2a sign: 1.yarı -32 / 2.yarı +17,8 bps net; |z|>1 varyantı 2.yarı +47 bps net (t=1,3, n=130); işaret yarılar arasında değişiyor')
upd('FROTO', 'F', 'lead_intra', notes='sign: OOS net -6,5 bps; AMA |z|>2 (büyük Ford günleri): IS +41,9 / OOS +43,2 bps net (t 1,35 / 1,84; n 96/65) aynı işaret -> ayrı satır')
new = [
 dict(stock='FROTO', driver_yahoo='F', driver_desc='Ford büyük hareket günleri (|z|>2)', tv_ticker='NYSE:F', relation='lead_intra', lag=1, t_stat=1.84,
      is_oos='net 8bps: IS +41,9 bps (t 1,35, n 96) / OOS +43,2 bps (t 1,84, n 65)', bt_oos_mean_bps=43.16, bt_oos_sharpe=0.66, n=161, confidence='DÜŞÜK',
      mechanism='Büyük Ford/ABD oto şoklarına açılışta eksik tepki, gün içinde devam', notes='08_extra; IS ve OOS aynı işaret ama t<2; çok günlük (açılış t->kapanış t+4) IS +111 / OOS +63 bps (t 1,7/1,0)'),
 dict(stock='FROTO', driver_yahoo='ON', driver_desc='ABD otomotiv yarı iletken/döngüsel ailesi (ON, NXPI, STM, BWA, APTV, SOX)', tv_ticker='NASDAQ:ON', relation='lead_intra', lag=1,
      corr_full=0.089, t_stat=4.41, is_oos='IS t 2,5 / OOS t 2,3', n=2995, confidence='DÜŞÜK', mechanism='ABD seansı döngüsel bilgisi BIST açılışında eksik fiyatlanıyor (FROTO yabancı ağırlıklı)',
      notes='09_mech: ON, NXPI+IFX kontrollü t=4,4; aile 12/12 pozitif (t 1,9-3,5) -> ON’a özgü değil, genel ABD döngüsel->FROTO gün-içi; F sign BT maliyet sonrası negatif, büyüklük küçük (r≈0,05-0,09)'),
 dict(stock='FROTO', driver_yahoo='^TWII', driver_desc='Tayvan endeksi (lag0, BIST açılışından önce)', tv_ticker='TWSE:TAIEX?', relation='lead_intra', lag=0, corr_full=0.053,
      t_stat=3.61, is_oos='pc t IS 3,67 / OOS 2,14; |z|>1 BT net IS +23,6 (t 2,1) / OOS +14,5 bps (t 1,3)', bt_oos_mean_bps=14.47, bt_oos_sharpe=0.53, n=3000, confidence='DÜŞÜK',
      mechanism='Asya teknoloji/risk iştahı -> BIST gün-içi devam (BIST geneli: 47 hissenin 13’ünde t>2)', notes='03_asia FDR (174 test) geçti; EEM1/SOX1 kontrolünde t=2,6 (OOS 1,4) -> kısmen ABD bilgisinin tekrarı'),
 dict(stock='TOASO', driver_yahoo='STLA', driver_desc='Stellantis — saatlik kesin senkron (15:00 UTC hizalı)', tv_ticker='NYSE:STLA', relation='sync', lag=0, corr_full=0.236, pcorr_xu100=0.128,
      n=591, confidence='ORTA', mechanism='Ortaklık + Avrupa talebi; günlük lag0 korelasyonu eşzamansız kapanış nedeniyle düşük görünür',
      notes='06_hourly 2023-11+: günlük lag0 0,147 -> saatlik hizalı 0,236; pc 0,13 (günlük pc 0,06); F: 0,18->0,19 (pc 0,10)'),
 dict(stock='TOASO', driver_yahoo='STLAM.MI', driver_desc='Stellantis Milano — BIST kapanışı sonrası son 30-90 dk', tv_ticker='MIL:STLAM', relation='lead_intra', lag=1, intra_corr=0.164,
      t_stat=2.88, n=689, confidence='DÜŞÜK', mechanism='Avrupa kapanışına kadarki geç hareket TOASO açılışında fiyatlanmıyor (gap t=-0,4), gün içinde fiyatlanıyor',
      notes='06_hourly; 138 saatlik testten biri, FDR geçmez (9/138 |t|>2, şansla ~7 beklenir); DOAS aynı işaret t=2,4; 2023-11+ örneklem'),
 dict(stock='TOASO', driver_yahoo='TOASO.IS', driver_desc='Stellantis Türkiye devri KAP/RK kararları', tv_ticker='BIST:TOASO', relation='event', lag=0, n=4,
      confidence='ORTA', mechanism='Yurtiçi dağıtım işi + yeni üretim sözleşmeleri değerlemeye doğrudan etki',
      notes='Piyasa modeli AR: RK reddi sonrası 25.10.2024 -6,4% (z -3,5); onay 18.04.2025 +7,0% (z 3,3) ve 21.04.2025 +9,6% (z 4,5)'),
 dict(stock='ARCLK', driver_yahoo='WHR', driver_desc='Whirlpool Avrupa işi devri (Beko Europe)', tv_ticker='NYSE:WHR', relation='event', lag=0, n=2, confidence='DÜŞÜK',
      mechanism='Birleşme haberleri', notes='AR: duyuru 17.01.2023 +7,9% (z 3,8); kapanış 02.04.2024 +4,5% (z 2,5). Sonrasında WHR/ELUX bağı değişmedi (p>0,4); USDTRY pc +0,09 -> -0,06 (z -2,6) ama FROTO’da da benzer düşüş -> TL rejimi ile karışık'),
 dict(stock='ASTOR', driver_yahoo='GRID_BASKET', driver_desc='Küresel şebeke sepeti (SU, ABBN, ETN, SIE, 267260, 298040)', tv_ticker='EURONEXT:SU + SIX:ABBN + NYSE:ETN', relation='regime', lag=0,
      corr_1y=0.32, is_oos='2023-24 corr -0,01 / 2025-26 corr 0,26 (z=4,2); pc -0,06 -> 0,10 (z=2,4)', n=940, confidence='ORTA',
      mechanism='ABD trafo sözleşmeleri (Mart 2026 768,9 m$) ile küresel elektrifikasyon temasına entegrasyon', notes='07_regime; 250g kayan corr son değer 0,32 = tarihi max; işlenebilir öncülük yok (BT2c, 2025+ OOS +4 bps)'),
]
F = pd.concat([F, pd.DataFrame(new)], ignore_index=True)
F.to_csv('../f_otomotiv.csv', index=False)
print(len(F), 'satır;', F.confidence.value_counts().to_dict())
