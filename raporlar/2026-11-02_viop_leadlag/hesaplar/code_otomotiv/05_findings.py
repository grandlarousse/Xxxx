"""res/*.csv -> ../f_otomotiv.csv (güven etiketleri BRIEF ölçeğine göre elle atanmış; gerekçe 'notes')."""
import pandas as pd, numpy as np, os
H = pd.read_csv('res/hyp_pairs.csv'); S = pd.read_csv('res/scan_fdr_hits.csv'); B = pd.read_csv('res/bt.csv')
B8 = B[B.cost_bps == 8].set_index('test')
F = [  # stock, driver, desc, tv, relation, lag, conf, mech, notes, bt
('FROTO','TOASO.IS','Tofaş (Koç oto kardeşi)','BIST:TOASO','sync',0,'YÜKSEK','Ortak Koç/oto sektör faktörü, yurtiçi talep/ÖTV','pc|XU100 0,31; tüm yıllar aynı işaret',None),
('FROTO','KCHOL.IS','Koç Holding','BIST:KCHOL','sync',0,'YÜKSEK','Holding NAV payı (FROTO KCHOL portföyünde büyük)','pc 0,15; IS/OOS aynı',None),
('FROTO','EXV5.DE','STOXX600 Otomobil ETF','XETR:EXV5','sync',0,'ORTA','Avrupa ticari araç/oto talebi (ihracatın ~%80i Avrupa)','ham 0,24 ama pc|XU100 sadece 0,06-0,07; çoğu küresel risk faktörü',None),
('FROTO','VOW3.DE','Volkswagen','XETR:VOW3','sync',0,'ORTA','Avrupa oto döngüsü (Ford-VW ticari araç işbirliği)','pc 0,07 (OOS 0,10 en istikrarlı Avrupa emsali)',None),
('FROTO','VOLV-B.ST','Volvo (kamyon)','OMXSTO:VOLV_B','sync',0,'DÜŞÜK','Ticari araç döngüsü','ham 0,20, pc 0,05',None),
('FROTO','IVG.MI','Iveco','MIL:IVG','sync',0,'DÜŞÜK','Avrupa hafif ticari (Transit rakibi)','pc 0,09 ama 2022+ örneklem; 1y corr ~0',None),
('FROTO','F','Ford Motor','NYSE:F','sync',0,'DÜŞÜK','%41 ortak (Ford), ama FROTO karı Avrupa hacmine bağlı','ham 0,14 (lag0) +0,09 (lag1 eşzamansız); pc|XU100 0,03',None),
('FROTO','F','Ford Motor','NYSE:F','lead_gap',1,'ORTA','Eşzamansız kapanış: ABD seansı BIST kapanışından sonra -> açılışta fiyatlanır','gap t=4,5; İŞLENEBİLİR DEĞİL',None),
('FROTO','F','Ford Motor','NYSE:F','lead_intra',1,'ÇOK DÜŞÜK','Gecikmeli tepki hipotezi','BT1a: OOS brüt 1,5 bps, 8 bps sonrası -6,5 bps; başarısız','BT1a F_{t-1} -> FROTO intra_t'),
('FROTO','EXV5.DE','STOXX600 Otomobil ETF','XETR:EXV5','lead_intra',1,'ÇOK DÜŞÜK','Avrupa kapanışı sonrası 30-90 dk bilgi','BT1d başarısız','BT1d EXV5.DE_{t-1} -> FROTO intra_t'),
('FROTO','TRY=X','USDTRY','FX:USDTRY','sync',0,'ORTA','TL değer kaybı -> ihracatçı TL fiyatı yükselir (XU100 kontrollü + işaret)','pc|XU100 +0,06 (ithalatçı DOAS -0,06); USD bazlı corr -0,40 = çeviri etkisi eksik geçiş',None),
('FROTO','EURTRY=X','EURTRY','FX:EURTRY','lead_intra',1,'DÜŞÜK','EUR gelir; kur şoku gecikmeli fiyatlama','FX düzeltmesi sonrası BT3c OOS net -6,3 bps; eski (hatalı etiketli) t~4 bulgusu kayboldu','BT3c EURTRY_{t-1} -> FROTO intra_t'),
('FROTO','EURUSD=X','EURUSD','FX:EURUSD','sync',0,'DÜŞÜK','EUR gelir/TL maliyet','ham 0,05, pc 0,00; USD bazlı 0,13 (risk-on dolar zayıflığı)',None),
('FROTO','000270.KS','Kia','KRX:000270','lead_intra',0,'DÜŞÜK','Asya oto emsali BIST açılışından önce kapanır','intra t=1,98, OOS 1,16; gap t=5,3 (açılışta fiyatlanıyor)',None),
('TOASO','FROTO.IS','Ford Otosan','BIST:FROTO','sync',0,'YÜKSEK','Ortak sektör/Koç faktörü','pc 0,31',None),
('TOASO','EXV5.DE','STOXX600 Otomobil ETF','XETR:EXV5','sync',0,'ORTA','Avrupa oto talebi (ihracat Stellantis Avrupa)','pc 0,10 (IS 0,15 / OOS 0,07); yılların %100ü pozitif; en güçlü yabancı emsal',None),
('TOASO','RNO.PA','Renault','EURONEXT:RNO','sync',0,'ORTA','Avrupa binek/hafif ticari','pc 0,08 (IS 0,14 / OOS 0,04 zayıflıyor)',None),
('TOASO','STLAM.MI','Stellantis (Milano)','MIL:STLAM','sync',0,'ORTA','%37,9 ortak; üretim sözleşmeleri (Doblo/K0, 2026 Q3 yeni platform)','pc 0,07 (IS 0,12 / OOS 0,06); yılların %100ü pozitif ama küçük',None),
('TOASO','STLA','Stellantis (NYSE)','NYSE:STLA','lead_intra',1,'ÇOK DÜŞÜK','ABD seansı gecikmeli tepki','BT1b (F+STLA ort.) OOS net -5 bps','BT1b mean(F,STLA)_{t-1} -> TOASO intra_t'),
('TOASO','^KS11','KOSPI','KRX:KOSPI?','lead_intra',0,'DÜŞÜK','Asya risk iştahı BIST açılışından önce biliniyor','FDR geçti (pc|XU100gap,kendi gap t=3,6; IS 3,7 / OOS 2,2) ama BT4a OOS brüt 4,9 bps -> net negatif','BT4a KOSPI_t (lag0) -> TOASO intra_t'),
('TOASO','005930.KS','Samsung Elektronik','KRX:005930','lead_intra',0,'DÜŞÜK','Mekanizma şüpheli (Asya risk proxy)','FDR geçti t=3,9 (IS 3,5/OOS 2,5); ekonomik büyüklük maliyet altında',None),
('TOASO','STLAM.MI','Stellantis','MIL:STLAM','regime',0,'ÇOK DÜŞÜK','2025 Stellantis Türkiye birleşmesi -> yurtiçi dağıtım payı artışı, Avrupa bağının zayıflaması beklenir','YAPILMADI (zaman yetmedi); 1y corr 0,24 ile 3y 0,18 arasında belirgin kırılma yok',None),
('DOAS','VOW3.DE','Volkswagen','XETR:VOW3','sync',0,'DÜŞÜK','VW Grubu distribütörü (ürün/marj), bilanço riski değil','ham 0,19 ama pc 0,06 (IS 0,05 / OOS 0,04)',None),
('DOAS','P911.DE','Porsche AG','XETR:P911','sync',0,'DÜŞÜK','Porsche distribütörlüğü','pc 0,06; 2022+ örneklem',None),
('DOAS','TRY=X','USDTRY','FX:USDTRY','sync',0,'ORTA','İTHALATÇI: TL değer kaybı maliyeti artırır -> ihracatçılara göre ters işaret','ham -0,15 (FROTO -0,06); pc|XU100 -0,06 vs ihracatçılar +0,04/+0,06; USD bazlı -0,44',None),
('DOAS','EURTRY=X','EURTRY','FX:EURTRY','sync',0,'DÜŞÜK','EUR bazlı ithal maliyet','ham -0,11, pc -0,05',None),
('DOAS','XHB','ABD konut inşaat ETF','AMEX:XHB','lead_intra',1,'ÇOK DÜŞÜK','Mekanizma yok (tarama sürprizi)','FDR geçti t=3,3, OOS 2,8; muhtemelen küresel döngüsel risk proxy',None),
('ARCLK','KCHOL.IS','Koç Holding','BIST:KCHOL','sync',0,'YÜKSEK','Holding NAV','pc 0,15',None),
('ARCLK','VESTL.IS','Vestel','BIST:VESTL','sync',0,'YÜKSEK','Beyaz eşya/yurtiçi talep ortak faktör','ham 0,40+; pc 0,09',None),
('ARCLK','WHR','Whirlpool (Beko Europe %25 ortağı)','NYSE:WHR','sync',0,'DÜŞÜK','Küresel beyaz eşya talebi/fiyat','ham 0,14 ama pc 0,04 (OOS 0,02)',None),
('ARCLK','WHR','Whirlpool','NYSE:WHR','lead_gap',1,'ORTA','Eşzamansız kapanış','gap t=4,6; işlenemez',None),
('ARCLK','ELUX-B.ST','Electrolux','OMXSTO:ELUX_B','sync',0,'DÜŞÜK','Avrupa beyaz eşya (Beko Europe rakibi)','pc 0,01',None),
('ARCLK','066570.KS','LG Electronics','KRX:066570','lead_intra',0,'ÇOK DÜŞÜK','Asya beyaz eşya emsali açılıştan önce','BT4c IS t=2,8 -> OOS 0,1; IS-only aşırı uyum','BT4c LG Elec_t (lag0) -> ARCLK intra_t'),
('ARCLK','6690.HK','Haier Smart Home (HK)','HKEX:6690 (açılmayabilir)','sync',0,'ÇOK DÜŞÜK','Çin beyaz eşya rekabeti','pc 0,01; HK seansı BIST ile çakışır',None),
('ARCLK','0300.HK','Midea (HK)','HKEX:300 (açılmayabilir)','sync',0,'ÇOK DÜŞÜK','Çin beyaz eşya','pc 0,00; n=489',None),
('ARCLK','FXI','Çin büyük şirketler ETF (Çin alternatifi)','AMEX:FXI','sync',0,'ÇOK DÜŞÜK','Çin talebi/rekabet','ham 0,13 ama pc -0,01: tamamen küresel risk; KWEB de aynı (pc -0,01)',None),
('ARCLK','MT','ArcelorMittal (çelik maliyeti)','NYSE:MT','sync',0,'ÇOK DÜŞÜK','Çelik maliyeti (ters beklenir)','ham +0,16 (risk-on), pc 0,00; maliyet kanalı görünmüyor',None),
('ARCLK','HRC=F','ABD HRC çelik vadelisi','COMEX:HRC1!','sync',0,'ÇOK DÜŞÜK','Çelik maliyeti','corr -0,04; seri %50 bayat',None),
('ARCLK','EURUSD=X','EURUSD','FX:EURUSD','sync',0,'DÜŞÜK','EUR gelir (Beko Europe)','pc 0,00; USD bazlı 0,14',None),
('ARCLK','KRDMB.IS','Kardemir B','BIST:KRDMB','lead_intra',1,'DÜŞÜK','BIST içi çapraz tersine dönüş (likidite)','FDR geçti t=-3,3, OOS -2,7; mekanizma zayıf',None),
('VESTL','ARCLK.IS','Arçelik','BIST:ARCLK','sync',0,'YÜKSEK','Ortak sektör','ham 0,42; pc 0,09 (OOS 0,16)',None),
('VESTL','034220.KS','LG Display (panel proxy)','KRX:034220','sync',0,'ÇOK DÜŞÜK','Panel fiyatı maliyet/talep','pc -0,02; LPL (NYSE) pc -0,02',None),
('VESTL','034220.KS','LG Display','KRX:034220','lead_intra',0,'ÇOK DÜŞÜK','Panel proxy açılıştan önce','BT4d OOS net -11,5 bps','BT4d LG Display_t (lag0) -> VESTL intra_t'),
('VESTL','005930.KS','Samsung Elektronik','KRX:005930','lead_intra',0,'ÇOK DÜŞÜK','TV rakibi','BT4b IS/OOS negatif','BT4b Samsung_t (lag0) -> VESTL intra_t'),
('VESTL','EURUSD=X','EURUSD','FX:EURUSD','sync',0,'ÇOK DÜŞÜK','Avrupa ihracatı','pc -0,05',None),
('VESTL','1070.HK','TCL Electronics (HK)','HKEX:1070 (açılmayabilir)','sync',0,'ÇOK DÜŞÜK','Çin TV rekabeti','corr 0,04',None),
('ASTOR','EUPWR.IS','Europower Enerji (trafo)','BIST:EUPWR','sync',0,'YÜKSEK','BIST trafo/şebeke teması; bireysel yatırımcı akışı','pc|XU100 0,37 (IS 0,45 / OOS 0,29)',None),
('ASTOR','GESAN.IS','Girişim Elektrik','BIST:GESAN','sync',0,'YÜKSEK','BIST enerji ekipmanı teması','pc 0,31',None),
('ASTOR','298040.KS','Hyosung Heavy (trafo)','KRX:298040','lead_gap',0,'ORTA','Kore kapanışı BIST açılışından önce -> açılışta fiyatlanır','gap t=4,6 (işlenemez); intra t=1,0',None),
('ASTOR','267260.KS','HD Hyundai Electric','KRX:267260','sync',0,'DÜŞÜK','Küresel trafo süper döngüsü','ham 0,07 -> son 1y 0,19 (artıyor); pc 0,03',None),
('ASTOR','267260.KS','Kore şebeke sepeti (267260+298040+010120)','KRX:267260','lead_intra',0,'DÜŞÜK','Asya şebeke haberi gün-içi yayılım','BT2a 1.yarı -24 bps / 2.yarı +25,8 bps (net 17,8, t=1,1); tutarsız','BT2a Kore şebeke sepeti_t (lag0) -> ASTOR intra_t'),
('ASTOR','SU.PA','Schneider Electric','EURONEXT:SU','regime',0,'DÜŞÜK','Küresel elektrifikasyon temasına entegrasyon','tam 0,12 -> son 1y 0,35; pc IS -0,12 / OOS +0,12 (rejim değişimi)',None),
('ASTOR','GRID','Akıllı şebeke ETF','NASDAQ:GRID','sync',0,'DÜŞÜK','Şebeke yatırım döngüsü','tam 0,09 -> 1y 0,26; pc ~0',None),
('ASTOR','ETN','Eaton','NYSE:ETN','lead_intra',1,'ÇOK DÜŞÜK','ABD şebeke/veri merkezi','BT2c (ETN/VRT/HUBB) OOS net 1,9 bps','BT2c GEV/ETN/VRT ort._{t-1} -> ASTOR intra_t'),
('ASTOR','HG=F','Bakır','COMEX:HG1!','sync',0,'ÇOK DÜŞÜK','Bakır girdi maliyeti / emtia teması','pc -0,05; yılların %25i aynı işaret',None),
('ASTOR','BTC-USD','Bitcoin (bireysel risk iştahı)','BITSTAMP:BTCUSD','sync',0,'ÇOK DÜŞÜK','Bireysel yatırımcı risk iştahı','corr 0,02; pc -0,01',None),
('FROTO','EURUSD=X','EURUSD','FX:EURUSD','lead_intra',1,'ÇOK DÜŞÜK','Ihracatçı sepeti EUR şoku','BT3a OOS net -17 bps (t=-3,1); ters işaret','BT3a EURUSD_{t-1} -> ihracatçı sepeti intra_t'),
('FROTO','TRY=X','USDTRY','FX:USDTRY','lead_intra',1,'ÇOK DÜŞÜK','Ihracatçı sepeti TL şoku','BT3b OOS net -17 bps; FX etiket düzeltmesinden sonra önceki t~4,7 bulgu sahteydi','BT3b USDTRY_{t-1} -> ihracatçı sepeti intra_t'),
('FROTO','KRW=X','USDKRW','FX:USDKRW','event',0,'ÇOK DÜŞÜK','ARTEFAKT: FX_FIX sonrası KRW=X lag0 BIST kapanışından SONRA biter -> look-ahead','taramada FDR geçti (t=-4,0) ama işlenemez; geçersiz',None),
('FROTO','GWLLY','Great Wall Motor OTC ADR','OTC:GWLLY?','lead_intra',1,'ÇOK DÜŞÜK','Bayat OTC fiyatı; mekanizma yok','FDR geçti t=3,6 (OOS 1,7)',None),
('TOASO','CSG.AS','CSG (savunma, Amsterdam)','EURONEXT:CSG?','sync',0,'ÇOK DÜŞÜK','Mekanizma yok; çok kısa örneklem','pc -0,24 taramada en yüksek; sahte olası',None),
]
rows = []
for st, dr, desc, tv, rel, lag, conf, mech, notes, btn in F:
    h = H[(H.stock == st) & (H.driver == dr)]
    o = dict(stock=st, driver_yahoo=dr, driver_desc=desc, tv_ticker=tv, relation=rel, lag=lag)
    if len(h):
        h = h.iloc[0]
        o.update(corr_full=h.c_full, corr_3y=h.c_3y, corr_1y=h.c_1y, pcorr_xu100=h.pc_xu100, beta=h.beta,
                 t_stat={'sync': h.t_full, 'regime': h.t_full, 'lead_gap': h.gap_t, 'lead_intra': h.intra_t}.get(rel, np.nan),
                 gap_corr=h.gap_c, intra_corr=h.intra_c, n=h.n,
                 is_oos=(f"pc IS {h.pc_IS:.3f} / OOS {h.pc_OOS:.3f}" if rel in ('sync', 'regime') else f"intra t IS {h.intra_t_IS:.2f} / OOS {h.intra_t_OOS:.2f}") + f" (split {h.split})")
    else:
        s = S[(S.stock == st) & (S.driver == dr)]
        if len(s):
            s = s.iloc[0]; o.update(corr_full=s.r, t_stat=s.t_nw, n=s.n, is_oos=f"IS t {s.t_IS:.2f} / OOS t {s.t_OOS:.2f} (tarama, {s.family})")
    if btn and btn in B8.index:
        b = B8.loc[btn]; o.update(bt_oos_sharpe=b.OOS_sharpe, bt_oos_mean_bps=b.OOS_mean_bps); notes += f" | BT8bps IS {b.IS_mean_bps:.1f}bps Sh {b.IS_sharpe:.2f}"
    o.update(confidence=conf, mechanism=mech, notes=notes); rows.append(o)
cols = 'stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes'.split(',')
out = pd.DataFrame(rows).reindex(columns=cols)
for c in ['corr_full','corr_3y','corr_1y','pcorr_xu100','beta','t_stat','gap_corr','intra_corr','bt_oos_sharpe','bt_oos_mean_bps']: out[c] = out[c].astype(float).round(3)
out.to_csv('../f_otomotiv.csv', index=False)
print(len(out), 'satır;', out.confidence.value_counts().to_dict())
