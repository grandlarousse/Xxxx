araç: 31/35
Dosyalar: hesap/02_analiz.py (tek komut, yeniden üretir), hesap/sonuclar.md, hesap/sonuclar.json, grafik/G1..G9.png (hepsi Read ile gözle kontrol edildi, düzeltildi). Ek veri: Fed G.17 GMF (imalat), Eurostat imalat C, BIS ABD geniş EER (indi).

M0: Birikim kimliği Airbus'ta 2019-25 gerçekle tutuyor (fark 0-2); Boeing'de tutmuyor (2020: -2.271, 2023: +262; ASC 606). Geriye kurulan toplam birikim 1987 öncesi <=0; birikim/teslimat oranı 1987-2025 (Y4, Y5 n=38).

M1 (yıllık, DXY +%10 etkisi, varyant ii, HAC=3; GA %95; Wald p): Y1 toplam teslimat -8,2% [-14,6; -1,2] p=0,022; Y2 Airbus -11,7% [-20,7; -1,7] p=0,023; Y3 Boeing -8,2% [-16,9; +1,5] p=0,096; Y4 birikim/teslimat -17,1% [-25,2; -8,1] p<0,001; Y5 sipariş yoğunluğu -28,4 puan [-46,9; -9,9] p=0,003. Varyant i/iii benzer (Y1: -7,3% p=0,042; -8,9% p=0,013). 15 modelden ham p<0,05: 12; BH sonrası: 11. Ortak F p Y1(ii)=0,042, Y3 anlamsız. n=51 (Y1-Y3), 38 (Y4-Y5).
Kararlılık (Y1, ii): 1978-1999 -11,3% p=0,034; 2000-2025 -5,2% p=0,327 (b GA [-1,67; +0,56]); Y4/Y5 1978-99 yalnız n=12. 20 yıllık kayan pencere Y1: medyan -5,8%, aralık -21,4..+0,9; 29 pencerenin 3'ünde p<0,05 (Y2: 8, Y3: 1); Y1'de yalnız 1 pencere pozitif.
BIS EER sağlamlığı (1995-2025, n=28): Y1 +1,0% p=0,87; Y2 +2,3% p=0,70; Y3 -1,6% p=0,85; aynı örneklemde DXY de p>0,75.
Korelasyon: 60 test (5 Y x k=0..5 x Pearson/Spearman); ham p<0,05: 7; BH sonrası: 1 (Y5, k=2, Pearson r=-0,62). Eşzamanlı Y1 r=-0,16 (G5). Güç: n=51'de %80 güçle saptanabilir en küçük |r|=0,38; n=38'de 0,44.

M2 (çeyreklik, HAC=12): ABD G336411T3 tam dönem -3,5% [-6,8; -0,1] p=0,044 (n=214); 1973-99 -4,2% [-8,4; +0,2] p=0,063; 2000-26 -0,5% [-5,6; +4,9] p=0,85; 2019Ç1-2021Ç4 hariç -3,2% p=0,046; G3364 -2,2% [-5,2; +1,0] p=0,18. Eurostat C30.3: FR -3,8% p=0,023; DE +1,5% p=0,40; EU27 -1,1% p=0,55. 11 modelden ham 3, BH sonrası 0. Granger (VAR gecikme 2): DXY->üretim p=0,54; üretim->DXY p=0,40. G.17 kaynak türü (fiziksel/işçi saati) G336411T3 için bulunamadı (genel metodoloji: fiziksel veri varsa o, yoksa işçi saati).

M3: ±%10 eşiğini aşan 36 bölüm; izleyen yıl teslimat değişimi bölümler arasında işaret karışık (örn. -24..+61%); tüm dönem ort. +5,8%, medyan +7,1%; G336411T3 +12 ay ort. +2,4%.
M4: Toplam teslimat 2018 1.606; 2025 1.393 (yıllık açık 213, kümülatif açık 2019-25: 3.414); birikim/teslimat 8,4 (2018) -> 15,8 (2020) -> 10,7 (2025); DXY yıllık ort. 2022 104,05 (+%12,5), 2025 100,78.
M5 (39 test; ham p<0,05: 8; BH sonrası: 6), b_d tüm dönem: ABD varlıkları hepsi anlamsız (ITA +0,08 p=0,54; LMT +0,22 p=0,12); Avrupa: AIR.PA +0,73 (BH p=0,019), RHM.DE -0,73 (BH p=0,058), MSCI Europe A&D Capped -0,06 p=0,72. 2022-26: ITA -0,59, PPA -0,52, LMT -1,33, BA.L -0,98 (BH p 0,019-0,037); 2015-21: RHM.DE -1,15 (BH p=0,004). 36 aylık kısmi korelasyon: ITA -0,41..+0,38 (son -0,28); Europe A&D -0,22..+0,43 (son -0,14).
Kur etkisi (MSCI Europe A&D Capped NETR): 2025 USD +77,7% / EUR +56,7%; 2026 YTD (30 Eki) USD -2,9% / EUR +2,2%.
M6: ETF 2026 YTD (30 Eki -> 18 Kas): ITA -2,1 -> -2,8; XAR -5,6 -> -9,1; PPA +1,7 -> -1,5; EUAD -6,2 -> -8,5; S&P 500 +10,7 -> +7,0. 2026 zirve ITA/XAR/URTH 14 Ağu (EUAD 13 Oca, PPA 2 Mar); ITA zirve->dip -20,0% (23 Eki), EUAD -22,0% (15 May).

Şaşırtıcı/uyarılar: BIS EER ve 2000 sonrası altörnekte etki sıfıra yakın/anlamsız; negatif işaret 1978-99'da güçlü. Y4/Y5 "bekleme" göstergeleri sipariş patlamasında da yükselir, birikim Boeing için ASC 606 yüzünden gürültülü. HAC küçük örneklemde p'leri iyimser tutar. Olay kuklalı varyantta R2 0,50-0,66. MSCI World A&D ve standart Europe A&D yok (Capped proxy); MSCI günlük veri yok. M5 MSCI son verisi 2026-10'a kesildi. Boeing 2026 teslimat 524 (csv) vs 523 (hedef dosyası). Yapılamayan: G336411T3 kaynak türü.
