# d2: dış/makro kuralların bağımsız yeniden üretimi (10.11.2026)

Kod: kod/d2_dis.py (python3 -I, 4 sn). Tüm satırlar: ek/d2_tum_sonuclar.csv (anahtar x dönem). Diğer: d2_A_dilim.csv, d2_B_ham_kur.csv, d2_bugun.csv, d2_bugun_abd.json, d2_islemler_*.csv.

## Yöntem notu
- Bağımsız kod, b1–b4 betikleri açılmadı. Plan 3–5. bölüm tanımları uygulandı; maliyet bireysel (hedge'liyse +6 bps).
- E2'de örtüşmeme: ilk denemede (çıkış gününe kadar yeni işlem yok) B/C/D E2 sayıları tutmadı. Giriş günü bazlı kurala (bir sonraki işlemin girişi önceki çıkıştan önce olmasın) geçince A, B, C, D E2 sayıları birebir tuttu. Yani verilen E2 sayıları "giriş bazlı" örtüşmeme ile; E0'da çıkış bazlı. Bu bir tutarlılık notu, iyi sonuç aramak değil.
- Ham zaman dilimi ayrışımı S_KUL'da yanıltıcı: hedefin t günü getirisi koşulda kullanıldığı için açılış→kapanış dilimi yapay negatif çıkar (−70 bps). Yalnız S_ONCU ve basit kural yorumlanır.

## Yeniden üretim (özet; tam tablo yanıt metninde)
A S_ONCU E0: n 458/457, brüt 50,8, t 3,29: birebir. OOS 61,6, SON2Y 36,9: birebir. E2 41,5/41,8 (giriş bazlı). S_KUL 239/240, 30,8 (28,1). S_IKISI 255/259, 61,5 (65,4).
B (E2 giriş bazlı): FROTO S_ONCU 175/77,8/2,64 birebir; ENKAI S_ONCU 121/79,3/2,85 ve OOS 99,1 birebir; VESTL S_ONCU 151/76,7/2,06 birebir; FROTO S_KUL 106/124,8 (verilen 132,3, −%6); TOASO S_KUL 107/98,9 (89,2).
C: h3 394/56,1 t 2,7 (391/54,8); OOS 34,2/1,14 birebir; SON2Y 102,6/2,34 birebir; h2 463/42,2 (460/40,3); E2 h2 13,2 (12,4); hedge'li h3 394/51,3 t 3,3 (385/56,4 t 3,8); OOS 30,4 (34,0).
D hedge'li h2 394/47,8 t 2,96 (388/44,0 t 2,8); OOS 46,1 (47,1); SON2Y 94,3 (95); E2 26,6 birebir; tek bacak E2 26,3 t 1,2 (24,5 t 1,3). KATI GC=F sürümü bu görevde yapılmadı.

## Bulgular
1. A hâlâ ayakta ama zayıflıyor: SON2Y brüt 36,9 (t 1,17), net bireysel 12,7, en iyi 10 çıkınca −17,8. Yıllık brüt (E0 h2): 2024 82, 2025 27, 2026 41 (n≈53/yıl). h=1 maliyetten sonra ~0. Plan z_L'deki β 250 günde ABD rafinerileri için NEGATİF (−0,2…−0,5; korelasyon −0,1); yani plan "artığı" S&P'yi geri ekliyor; β=1 sade kural farklı günleri seçiyor ve benzer sonuç veriyor (h2 TAM 43,0 t 2,7; SON2Y 51,9 t 1,8 net 27,4; ex10 0,7). Yalnız SAT SON2Y −1,2 ve 2026 −84: kazanç AL tarafında.
2. Zaman dilimi (S_ONCU, TAM): önceki kapanış→açılış 6,5 (t 1,5); açılış→kapanış 29,4 (t 3,4); kapanış t→t+1 24,8; t+1→t+2 24,7. Kazanç t günü içinde ama kapanıştan sonrası da var (E0 ile yakalanan ≈50). SON2Y: açılışa kadar 27,2 (t 3,0), gün içi 18,7, kapanıştan sonra 22,9 + 4,8 (t 1,3 ve 0,2): son 2 yılda ağırlık kapanıştan önceye kaydı; hipotez SON2Y için büyük ölçüde doğru, TAM için değil.
3. B çürütme: FROTO S_KUL E2 tüm yıllarda pozitif (8/8), kriz çıkarılınca 134 (t 3,4), ex-temettü çıkarılınca 119 (t 3,0), hedge'li 80,8 (t 2,7): dayanıyor. Ama E0 45,6 (t 1,25) ve E3 (bir gün geç) 85,1; 2024–26'da E3 −6: kazanç t+2..t+3 günlerinde, bir öncü-gecikmeli mekanizma için tuhaf profil. |ham değişim|≥50 bps ile 2024–26 n=16, −24: 2024–26 kazancı küçük kur günlerinde. Sinyal günü USDTRY medyan |ham| 2017–23'te 122 bps, 2024–26'da 41, 2026'da 21 bps (günlerin %50'si <20 bps): hipotez kısmen doğru. Plasebo (XU030, BIMAS, TCELL, TTKOM, EKGYO) TAM'da 5–62 bps, t≤2,2; 2024–26'da ise hepsi 35–110 bps (TCELL t 2,3): etki FROTO'ya özgü TAM'da, son dönemde kısmen piyasa geneli.
4. C: E2'de çöküyor (h2 13, h3 5; net −13/−22) ve OOS h3 t 1,14; hipotez doğru. SON2Y ve 2026 çok güçlü (h3 hedge'li 116, t 3,2) ama 2023 −106/−128.
5. D: hedge'siz TAM 31 (t 1,6), hedge'li 48 (t 3,0): hedge yardımcı. Yıllık hedge'li: 2021 −39, 2023 −42, 2026 +148; altın yıllığı 2020 +20, 2025 +45 iken 2026 −13: "yalnız rallide" hipotezi net doğrulanmadı. E2 net −4.

## Doğrulama kapsamı
Verilen iddialar yeniden üretim tablosundaki kalemlerle karşılaştırıldı; ölçüt dışı kalanlar: ENKAI/VESTL/FROTO S_ONCU E0 (E2 tanımıyla çözüldü), FROTO E0 n 114 vs 106 (kıyas dışı), C hedge'li h3 t 3,3 vs 3,8. Çoklu test düzeltmesi yapılmadı; ayrıntı satırları d2_tum_sonuclar.csv.
