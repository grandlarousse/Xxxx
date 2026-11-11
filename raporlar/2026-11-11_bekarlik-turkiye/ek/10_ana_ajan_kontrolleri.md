# Ana ajan kontrolleri (betikle, birincil kaynaktan)

Doğrulayıcıların bütçesi 58 satırın 32'sine yetmedi. Kalan kritik satırlar ajan açmadan, betikle birincil kaynaktan kontrol edildi. Bu dosya o kontrollerin kaydıdır.

## 1. Yaşa ve cinsiyete göre hiç evlenmemişlerin payı (%)

Kaynak: Eurostat `demo_pjanmarsta` (Population on 1 January by age, sex and legal marital status), `geo=TR`, `marsta=SIN` ve `TOTAL`, tek yaşlar 20-54; veri güncellemesi 25.09.2026. Oran = hiç evlenmemiş / toplam, beşer yaşlık gruplarda toplanarak hesaplandı. Türkiye için veri olan yıllar: 2014-2018 ve 2022-2025.

API çağrısı: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjanmarsta?format=JSON&lang=EN&geo=TR&marsta=SIN&marsta=TOTAL&sex=M&sex=F&age=Y20...&age=Y54`

| Yaş | E 2014 | E 2018 | E 2022 | E 2025 | K 2014 | K 2018 | K 2022 | K 2025 |
|---|---|---|---|---|---|---|---|---|
| 20-24 | 88,4 | | | 93,3 | 59,2 | | | 77,6 |
| 25-29 | 49,4 | 52,9 | 58,1 | 63,7 | 24,1 | 27,0 | 32,7 | 38,9 |
| 30-34 | 20,6 | 23,8 | 28,1 | 33,2 | 11,7 | 11,4 | 13,2 | 16,5 |
| 35-39 | 10,0 | 12,3 | 15,3 | 18,6 | 8,4 | 8,1 | 8,0 | 9,4 |
| 40-44 | 5,6 | 7,3 | 9,4 | 11,7 | 6,7 | 6,8 | 6,7 | 7,3 |
| 45-49 | 3,7 | | | 7,8 | 5,5 | | | 6,6 |
| 50-54 | 2,7 | | | 5,1 | 4,3 | | | 5,8 |

Boş hücreler hesaplanmadı (veri var). Sınır: resmî medeni durum; yalnızca dinî nikâhı olanlar "hiç evlenmemiş" sayılır. Anket temelli TNSA 2018'de (ek/06) kadınlarda oranlar daha düşük (30-34: %8,4), çünkü anket fiilî birlikteliği sayar.

Kuşak hesabı: 1 Ocak 2014'te 30-34 yaşındaki erkeklerde %20,6; aynı kuşak 1 Ocak 2025'te 41-45 yaşında, 40-44 grubunda %11,7. Oran 0,57. Göç ve ölüm hesaba katılmadı; kaba bir göstergedir.

## 2. TÜİK Türkiye Aile Yapısı Araştırması 2021 (rapor PDF'i, pdftotext ile okundu)

Kaynak: https://www.tuik.gov.tr/media/announcements/turkiye_aile_yapisi_ara%C5%9Ftirmasi_2021.pdf

**Tablo 4.4, evlilik kararı (evlilik deneyimi olanlar, %)**

| Yaş | Görücü, görüşü sorulmadan | Görücü, kendi rızasıyla | Görücü toplam | Kendi kararı, aile rızasıyla | Kendi kararı, rıza dışında | Kaçma |
|---|---|---|---|---|---|---|
| Türkiye | 10,7 | 46,1 | 56,8 | 34,9 | 2,7 | 5,3 |
| 15-24 | 4,4 | 36,1 | 40,5 | 44,4 | 5,9 | 8,9 |
| 25-34 | 3,8 | 31,7 | 35,5 | 55,9 | 3,4 | 5,1 |
| 35-44 | 6,1 | 41,2 | 47,3 | 45,1 | 2,7 | 4,8 |
| 45-54 | 9,7 | 51,5 | 61,2 | 31,1 | 2,4 | 5,0 |
| 55-64 | 15,4 | 54,6 | 70,0 | 22,1 | 2,7 | 4,7 |
| 65+ | 21,2 | 53,4 | 74,6 | 16,5 | 2,1 | 6,4 |
| Üniversite mezunu | 2,2 | 22,1 | 24,3 | 71,7 | 3,2 | 0,8 |

**Tablo 4.7-4.10, önümüzdeki 3 yılda evlenmeyi düşünmeyen ya da kararsız, evli olmayan bireylerin gerekçeleri (%, çoklu yanıt)**

| Grup | Düşünmeyen/kararsız payı | Maddi kazanç yetersiz | İş garantisi yok | Eğitime öncelik | Kariyere öncelik | Yaşım küçük | Uygun biriyle karşılaşmadım | Sağlıklı evlilik yürüteceğimi düşünmüyorum |
|---|---|---|---|---|---|---|---|---|
| Türkiye | 80,1 | 11,9 | 6,6 | 29,5 | 6,0 | 6,7 | 10,2 | 7,1 |
| Erkek | 73,2 | 22,5 | 11,2 | 29,8 | 5,2 | 7,7 | 9,1 | 3,4 |
| Kadın | 87,0 | 2,9 | 2,6 | 29,3 | 6,7 | 5,8 | 11,1 | 10,2 |
| Hiç evlenmedi | 76,6 | 14,2 | 8,9 | 41,5 | 8,0 | 9,4 | 9,5 | 1,5 |
| 25-34 | 56,2 | 27,1 | 14,7 | 6,5 | 12,2 | 2,8 | 19,8 | 2,7 |
| 35-44 | 64,0 | 19,1 | 6,4 | 0,6 | 5,8 | 0,1 | 31,4 | 5,8 |
| Kadın, hiç evlenmedi (4.9) | | 3,5 | 4,2 | 50,0 | 10,7 | 9,9 | 11,5 | 1,5 |
| Kadın, 25-34 (4.9) | | 7,6 | 10,4 | 8,9 | 17,7 | 3,2 | 26,5 | 2,1 |
| Erkek, hiç evlenmedi (4.10) | | 22,7 | 12,6 | 34,7 | 5,9 | 8,9 | 7,9 | 1,4 |
| Erkek, 25-34 (4.10) | | 38,8 | 17,2 | 5,1 | 9,0 | 2,6 | 15,9 | 3,0 |

Not: Kadınlarda "sağlıklı evlilik yürüteceğimi düşünmüyorum" payının yüksekliği (%10,2) dul ve yaşlı kadınlardan geliyor (eşi ölmüşlerde %25,7); hiç evlenmemişlerde %1,5. Rapora genç kadınlara özgü bir bulgu olarak alınmadı.

**Tablo 4.13 ve 4.14, eşte aranan özellikler (%, 15-24 yaş; parantez içinde Türkiye geneli)**

| Özellik | Kadınların erkekte aradığı | Erkeklerin kadında aradığı |
|---|---|---|
| Gelir getirici bir işinin olması | 91,8 (92,1) | 39,7 (38,6) |
| Üniversite mezunu olması | 56,3 (46,0) | 35,5 (30,4) |
| Yüksek gelirli ya da varlıklı olması | 41,7 (39,7) | 20,3 (18,0) |
| Eşine âşık olması | 89,2 (80,9) | 86,6 (80,0) |
| Ev işleri ve çocuk bakımını paylaşması | 86,3 (82,3) | 85,1 (86,4) |
| Ev işlerinde becerikli olması | 70,2 (70,4) | 77,0 (81,7) |
| Benzer hayat tarzı | 80,3 (82,7) | 76,4 (80,3) |
| İlk kez evlenecek olması | 80,9 (75,3) | 80,3 (75,5) |
| Dindar olması | 69,0 (74,9) | 62,0 (68,2) |
| Aynı etnik kökenden olması | 54,0 (64,4) | 46,6 (54,1) |
| Aynı mezhepten olması | 51,4 (61,0) | 41,9 (50,7) |
| Benzer siyasi görüş | 38,6 (44,2) | 30,8 (35,8) |
| Güzel / yakışıklı olması | 47,7 (40,2) | 57,7 (51,7) |

## 3. Makale özetleri (Europe PMC arama servisi) ve sayfa metinleri

| İddia | Sonuç |
|---|---|
| Mayo-Wilson 2014: bireysel BDT SMD -1,19 (bekleme listesine göre), -0,56 (psikolojik plaseboya göre); 101 çalışma, 13.164 katılımcı | Özette aynen görüldü |
| Joel 2020: 43 veri seti, 29 laboratuvar; en güçlü yordayıcılar algılanan partner bağlılığı, takdir, cinsel doyum, algılanan partner doyumu, çatışma | Özette görüldü |
| Stinson, Cameron & Hoplock: yedi örneklem, 1.897 kişi (üniversite öğrencileri ve çevrimiçi yetişkinler), üçte ikisi arkadaşlıktan başlamış | Özette görüldü (basım yılı 2022, çevrimiçi 2021) |
| Spielmann 2013: daha az duyarlı ve daha az çekici adaylara ilgi; 3. çalışma boylamsal; 7. çalışma hızlı tanışma etkinliği | Özette görüldü |
| Apostolou 2023: 14 ülke (Türkiye dahil), N=7.181, yaklaşık %13 istemsiz bekâr | Özette görüldü |
| Başkent açık erişim: 453 Türkçe konuşan katılımcı (taahhüt korkusu); 990 Yunan ve Türk katılımcı (korku ve çaba) | Sayfada görüldü |
| Pepping & MacDonald: üç alt grup (kaygılı, kaçınan, güvenli); derleme makalesi | Özette görüldü |
| Eastwick & Finkel 2008: hızlı tanışma ve izleme çalışması | Özette görüldü |
| Cacioppo 2013: evliliklerin üçte birinden fazlası çevrimiçi başlıyor | Özette görüldü (rapora alınmadı) |
| Pew 2020: bekârların yarısı ilişki ya da flört aramıyor | Sayfada görüldü |
| TAYA 2021 bülten metni: %80,1; %29,5; %11,9; %10,2; %22,5; %56,8; %46,1; %34,9 | Sayfada görüldü |
| Gençlik 2025: 15-24 yaşta erkeklerin %96,8'i, kadınların %88,9'u hiç evlenmemiş | Sayfada görüldü (rapora alınmadı; Eurostat tablosu kullanıldı) |
| Bilgi Üniversitesi 2020: %74,9 | Sayfada görüldü |
| AB 2024 binde 3,9; İtalya 2,9; Güney Kore 2024 4,4 | Sayfalarda görüldü |
| Üniversitelerde kadın öğrenci oranı %53,2 | Başlıkta görüldü |
| Evli kadınların %38,3'ünün eşi daha eğitimli, %17,0'ının eşi daha az eğitimli, %43,3 eşit | Sayfada görüldü |
| 2010 ilk evlenme yaşı erkek 26,5, kadın 23,2 | Sayfada görüldü |
| 2001 ilk evlenme yaşı (26,0 / 22,7) | Sayfada bulunamadı; rapora alınmadı |
| KONDA 2008-2018 sayıları (bianet) | Sayfa metni çekilemedi; rapora alınmadı |
| Twenge (ABD, yüz yüze görüşme), Ramirez 2015, Pronk & Denissen özeti | Europe PMC'de bulunamadı ya da zaman aşımı; ilk ikisi "doğrulanamadı" etiketiyle kullanıldı, Pronk doğrulayıcı tarafından özetten doğrulandı |
| Japonya IPSS sayıları | Sayfada bulunamadı; rapora alınmadı |

## 4. Link kontrolü

Tek betikle iki tur: birinci dalga defterlerindeki 87 linkin 73'ü 200 döndü (6'sı 403, 3'ü 404, 2'si zaman aşımı, 3'ü 203). Rapora giren kaynakların durumu RAPOR.md "Kaynaklar" bölümünde.
