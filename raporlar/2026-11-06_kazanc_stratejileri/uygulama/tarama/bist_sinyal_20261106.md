# BIST günlük sinyal — 2026-11-06 kapanışı (üretim 2026-11-06 18:32 TSİ)

**Özet 2026-11-06:** Rejim **KAPALI** (0/7 açık) | KRİZ: **yok** | K4 nitelikli: **0** | K1 z **−0,54**, K2 z **1,56** | XU030 F_XU0301226 ima basit **%29,3** / bileşik %33,1 (eşik %35,6) → **kapalı** | bülten 2026-11-05 (BAYAT: spot kesimi 2026-11-06)

Kaynak: İş Yatırım ChartData/HisseTekil (varsayılan başlık), Borsa İstanbul VİOP bülteni, KAP endeks listesi (KAP). Makro: VARSAYILAN (PLAN_BIST.md 05.11.2026 degerleri) - guncelleyin. Bulunamayan kod: —. Bilgi amaçlıdır.

## 1. Rejim (PLAN §2)
| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.483 vs 13.566 (−%15,4) | 0 |
| T2 | XU100 12 ay > nakit 12 ay (max TLREF, PPF %45,5) | +%4,7 vs TLREF bileşik +%47,3 / PPF +%45,5; bugünkü eşik ~16.159 (plan 30.11 eşiği 15.860) | 0 |
| T3 | XU100 son 5 kapanış > SMA50 | SMA50 12.630 (−%9,1) | 0 |
| M1 | Swap hariç net rezerv 3 hafta artış (elle) | 30,8 → 24,3 mlr $ | 0 |
| M2 | Aylık TÜFE < %2, 2 ay üst üste (elle) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli, elle) | 248 (teyitli: H) | 0 |
| M5 | XBANK > SMA200 | 16.398 vs 16.948 | 0 |

**Durum: KAPALI** → K4 r₀ = %0,25; ertesi işlem gününden geçerli.

**KRİZ kesicisi (herhangi biri):**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%6,7 | — |
| b USDTRY 10g yıllık > %35 | +%26,4 | — |
| c CDS > 300 (teyitli) | 248 | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 mlr $ (haftalık değişim) | — |
| e F_USDTRY ön ay ima > politika + 5 | +%32,3 | — |
| f MSCI danışma | hayır | — |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf değişim ≥ −2 ve seviye ≥ 20: ✗; 2 yabancı DİBS haftalık ≥ −500 mn $: ✗; 3 F_USDTRY ön ay ima ≤ politika + 5 (CDS yerine): ✓; 4 USDTRY 10g yıllık ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✗; 6 Kural 0: ✗

## 2. K4 kırılım (PLAN §3 K4; evren ilk 75 likit, dışlama hariç)
Likidite sırası 100 hissede hesaplandı (60g medyan TL hacim). RS = 0,4·R3a+0,2·R6a+0,2·R9a+0,2·R12a, ilk 150 likit içinde yüzdelik. Tetik = yarın aşılması gereken kapanış (bugün dahil 252 gün zirvesi).

**Nitelikli: yok.**

**Bekleme listesi (tetiğe ≤ %15, şablonun 5 alt koşulundan ≥ 4'ü, ilk 100 likit):**
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon (diz/eğim/dip/zirve/RS) | RS | Lik. sıra | SMA50 | Küme | Bayrak |
|---|---|---|---|---|---|---|---|---|---|
| ENERY | 14,05 | 14,60 | +%3,9 | ✓✓✓✓✓ | 97 | 35 | 12,78 | ENERJİ_DAĞITIM | bilanço 9.11 akşamı → karar 10.11, aktif geri alım, AHGAZ+ENERY tek isim, spot ×0,75 |
| AHGAZ | 46,82 | 48,70 | +%4,0 | ✓✓✓✓✓ | 99 | 54 | 43,61 | ENERJİ_DAĞITIM | bilanço 9.11 akşamı → karar 10.11, aktif geri alım, AHGAZ+ENERY tek isim, spot ×0,75 |
| ENJSA | 122,00 | 127,00 | +%4,1 | ✓✓✓✓✓ | 94 | 43 | 112,43 | ENERJİ_DAĞITIM |  |
| KCHOL | 206,10 | 225,50 | +%9,4 | ✗✓✓✓✓ | 84 | 8 | 210,94 | HOLDİNG | bilanço 9.11 akşamı → karar 10.11 |
| RYSAS | 27,34 | 30,28 | +%10,8 | ✓✓✓✓✓ | 96 | 51 | 26,11 | — | bilanço 9.11 akşamı → karar 10.11, spot ×0,75 |
| TRGYO | 90,40 | 101,70 | +%12,5 | ✗✓✓✓✓ | 84 | 85 | 90,99 | GYO | spot ×0,75, K4 evreni dışı (likidite sırası > 75) |
| BRSAN | 682,00 | 769,50 | +%12,8 | ✗✓✓✓✓ | 90 | 26 | 669,44 | ÇELİK | stop %25 |
| GLYHO | 16,35 | 18,73 | +%14,6 | ✗✓✓✓✓ | 88 | 96 | 16,43 | HOLDİNG | spot ×0,75, K4 evreni dışı (likidite sırası > 75) |

Bugün 52 hafta kırılımı yapıp nitelik kazanmayanlar: —

Dışlananlar (ilk 100 likit içinde): ALTNY (60g'de 4 limit kapanış: 3↑/1↓), ASTOR (60g'de 11 limit kapanış: 3↑/8↓), BINHO (60g'de 10 limit kapanış: 2↑/8↓), BTCIM (60g'de 5 limit kapanış: 1↑/4↓), CVKMD (60g'de 3 limit kapanış: 1↑/2↓), CWENE (60g'de 4 limit kapanış: 1↑/3↓), ECZYT (60g'de 4 limit kapanış: 1↑/3↓), EGEEN (60g'de 6 limit kapanış: 4↑/2↓), GLRMK (fon payı/fiili dolaşım >%20), GUBRF (60g'de 5 limit kapanış: 2↑/3↓), HALKB (60g'de 6 limit kapanış: 6↑/0↓), KARSN (60g'de 9 limit kapanış: 5↑/4↓), KORDS (60g'de 4 limit kapanış: 2↑/2↓), PETKM (60g'de 3 limit kapanış: 3↑/0↓), SASA (60g'de 5 limit kapanış: 3↑/2↓), TCKRC (60g'de 6 limit kapanış: 2↑/4↓), TKFEN (60g'de 6 limit kapanış: 1↑/5↓), TUKAS (60g'de 3 limit kapanış: 2↑/1↓), TURSG (60g'de 4 limit kapanış: 0↑/4↓), VESTL (60g'de 4 limit kapanış: 4↑/0↓)

## 3. Küme 12 ay RS (dalga_bist §4; K7 filtresi ve K4 önceliği)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | R/MA50 | 126g RS zirvesinden gün | Genişlik 50 | Üye |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%24,0 | +%10,5 | −%8,1 | H | −%4,5 | 5 | %0,0 | 4 |
| 2 | HOLDİNG | Blok1 | +%22,0 | +%10,2 | −%8,4 | H | +%4,4 | 18 | %0,0 | 8 |
| 3 | KOZA_ALTIN | Ayrıştırıcı | +%21,6 | −%9,3 | −%24,6 | H | −%6,4 | 29 | %0,0 | 3 |
| 4 | PERAKENDE | Diğer | +%14,7 | +%1,4 | −%15,7 | H | −%3,9 | 16 | %0,0 | 5 |
| 5 | ÇELİK | Diğer | +%6,7 | −%3,3 | −%19,6 | H | −%1,5 | 50 | %14,3 | 7 |
| 6 | BANKA | Blok1 | +%3,9 | +%26,7 | +%5,4 | H | +%9,4 | **0 (KIRILIM)** | %44,4 | 9 |
| 7 | GYO | Blok1 | −%2,4 | +%10,8 | −%7,8 | H | +%4,1 | 21 | %14,3 | 7 |
| 8 | SAĞLIK | Blok3 | −%8,8 | −%7,5 | −%23,1 | H | −%6,3 | 40 | %20,0 | 5 |
| 9 | ELK_ÜRETİM | Blok2 | −%11,4 | −%3,6 | −%19,9 | H | −%1,9 | 108 | %16,7 | 6 |
| 10 | GIDA | Diğer | −%12,3 | +%3,4 | −%14,1 | H | +%2,7 | 122 | %0,0 | 7 |
| 11 | TELEKOM | Blok1 | −%12,6 | +%3,4 | −%14,0 | H | +%1,7 | 13 | %0,0 | 2 |
| 12 | TEKNOLOJİ | Blok2 | −%13,8 | −%11,7 | −%26,6 | H | −%4,3 | 111 | %12,5 | 8 |
| 13 | HAVACILIK | Blok1 | −%13,8 | +%15,9 | −%3,6 | H | +%12,3 | 1 | %75,0 | 4 |
| 14 | OTOMOTİV | Diğer | −%20,7 | +%3,7 | −%13,8 | H | +%1,8 | 108 | %0,0 | 6 |
| 15 | SAVUNMA | Ayrıştırıcı | −%25,2 | −%11,3 | −%26,3 | H | −%6,0 | 111 | %0,0 | 5 |
| 16 | ÇİMENTO | Blok3 | −%27,8 | −%20,7 | −%34,1 | H | −%3,7 | 113 | %22,2 | 9 |
| 17 | ELK_EKİPMAN | Blok2 | −%28,1 | −%33,8 | −%45,0 | H | −%8,0 | 110 | %20,0 | 5 |
| 18 | SİGORTA | Diğer | −%29,0 | −%10,8 | −%25,9 | H | −%5,1 | 104 | %0,0 | 6 |
| 19 | OTO_YAN | Blok3 | −%33,5 | −%3,4 | −%19,7 | H | −%2,0 | 113 | %0,0 | 5 |
| 20 | YENİLENEBİLİR | Blok2 | −%33,9 | −%31,1 | −%42,8 | H | −%8,6 | 111 | %0,0 | 6 |
| 21 | KİMYA | Blok3 | −%36,0 | −%18,2 | −%32,0 | H | −%6,5 | 123 | %0,0 | 5 |
| 22 | GÜBRE | Diğer | −%36,6 | −%17,6 | −%31,5 | H | −%13,8 | 122 | %0,0 | 3 |
| 23 | BEYAZ_EŞYA | Blok3 | −%56,6 | −%23,8 | −%36,6 | H | −%14,4 | 122 | %0,0 | 3 |
| 24 | CAM_SERAMİK | Blok3 | −%61,1 | −%29,1 | −%41,0 | H | −%13,3 | 112 | %0,0 | 5 |

Nakit 3 ay (TLREF): +%9,4. İlk 3: RAFİNERİ, HOLDİNG, KOZA_ALTIN. Filtre (3 ay TL > nakit) geçen ilk 3 içinden: yok → nakit.

## 4. Çift kolları (PLAN §3 K1, K2)
| Kol | z (60g, bugün dahil) | Son \|z\| ≥ 2 kesişimi | Karar |
|---|---|---|---|
| K1 SAHOL/AKBNK | −0,54 | 2026-10-22 | sinyal yok |
| K2 KCHOL/sepet | 1,56 | 2026-11-03 | sinyal yok |

K1 tam tetikler (diğer bacak sabit; SAHOL 87,30, AKBNK 68,65): z=+2 → SAHOL ≥ 93,06 ya da AKBNK ≤ 64,40; z=−2 → SAHOL ≤ 84,09 ya da AKBNK ≥ 71,27.

## 5. VİOP resmî bülten (uzlaşma fiyatı; bülten tarihi 2026-11-05 (BAYAT: spot kesimi 2026-11-06))
İma basit oran = (F_uzlaşma / S_kapanış − 1) × 365 / gün; spot, bültenin kendi tarihindeki kapanış. Eşik = 32 gün mevduat neti (%32,6) + 3 puan.

| Kontrat | Vade | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik | Nakit-taşıma | Hacim mn TL | Açık poz. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 2026-12-31 | 56 | 14.734 | 14.101 | %29,3 | %33,1 | %35,8 | %35,6 | kapalı | 51.179 | 446.504 |
| F_XU0300227 | 2027-02-26 | 113 | 15.405 | 14.101 | %29,9 | %33,1 | %35,8 | %35,6 | kapalı | 598 | 4.499 |
| F_XU0300427 | 2027-04-30 | 176 | 16.116 | 14.101 | %29,6 | %31,9 | %35,8 | %35,6 | kapalı | 14 | 431 |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 51,02, spot 50,05 (ChartData kapanışı; saat farkı ±1–2 puan), 25 gün, USD faizi %3,9 varsayımıyla ima TL basit **%32,3** (politika + 5 = %41).

Pay vadelileri (long için vadeli kuralı §1.5: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL, Kasım değil):
| Kontrat | Gün | Uzlaşma | Spot | İma basit | Mevduat neti − ima (puan) | Hacim mn TL | Açık poz. | Kural sağlanıyor |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 25 | 86,72 | 85,10 | %27,8 | +4,8 | 1.321 | 498.361 | H |
| F_SAHOL1226 | 56 | 89,29 | 85,10 | %32,1 | +0,5 | 22 | 10.750 | H |
| F_AKBNK1126 | 25 | 68,41 | 67,20 | %26,3 | +6,3 | 3.408 | 753.238 | H |
| F_AKBNK1226 | 56 | 70,35 | 67,20 | %30,6 | +2,1 | 118 | 16.098 | H |
| F_GARAN1126 | 25 | 144,45 | 142,00 | %25,2 | +7,4 | 1.836 | 160.641 | H |
| F_GARAN1226 | 56 | 147,85 | 142,00 | %26,9 | +5,8 | 51 | 3.431 | H |
| F_YKBNK1126 | 25 | 37,22 | 36,52 | %28,0 | +4,6 | 3.928 | 1.369.867 | H |
| F_YKBNK1226 | 56 | 38,24 | 36,52 | %30,7 | +1,9 | 59 | 31.925 | H |
| F_KCHOL1126 | 25 | 206,05 | 202,30 | %27,1 | +5,5 | 1.772 | 153.025 | H |
| F_KCHOL1226 | 56 | 211,60 | 202,30 | %30,0 | +2,6 | 30 | 6.776 | H |
| F_ENJSA1126 | 25 | 118,45 | 119,30 | −%10,4 | +43,0 | 132 | 14.463 | H |
| F_ENJSA1226 | 56 | 121,10 | 119,30 | %9,8 | +22,8 | 4 | 1.871 | H |
| F_TUPRS1126 | 25 | 338,55 | 331,75 | %29,9 | +2,7 | 2.178 | 95.648 | H |
| F_TUPRS1226 | 56 | 348,10 | 331,75 | %32,1 | +0,5 | 99 | 2.893 | H |
| F_THYAO1126 | 25 | 302,20 | 297,00 | %25,6 | +7,0 | 5.626 | 293.266 | H |
| F_THYAO1226 | 56 | 310,85 | 297,00 | %30,4 | +2,2 | 312 | 8.156 | H |
| F_BIMAS1126 | 25 | 376,55 | 369,25 | %28,9 | +3,7 | 709 | 43.446 | H |
| F_BIMAS1226 | 56 | 385,50 | 369,25 | %28,7 | +3,9 | 38 | 7.912 | H |

## 6. Ertesi gün emir özeti
- KRİZ yok.
- K4: emir yok.
- K1: sinyal yok. K2: sinyal yok.
- XU030 nakit-taşıma: kapalı; F_USDTRY ön ay ima %32,3 (KRİZ e eşiği %41); K6 kapısı KAPALI.
- Takvim kısıtları (PLAN §3.10 A1–A10), K3/K3b temettü takvimi ve bedelsiz pencereleri elle kontrol edilir; bu betik KAP'ı taramaz.
- Emir limitleri (PLAN §3, §6.2): alış min(plan limiti; P_son × 1,03); risk azaltan satış max(taban; P_son × 0,97); 18:01–18:05.
