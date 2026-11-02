# v_YG2_b — 2. aşama çürütme: Kapanış müzayedesi dönüşü (YG2)
Tarih: 02.11.2026 · Kod: `out/code_v_YG2_b/` (ll.py ve 1. aşama kodu import edilmedi; ham parquet'ten kendi panelim)
Çalıştırma: `nice -n 10 python3 w1_panel.py`, sonra w2 … w12 (sıra `vlib.py` başında).

## Karar: DÜZELT. İlişki çürütülemedi (ORTA, istatistik olarak YÜKSEK'e yakın); VİOP'ta uygulanamaz; spotta net kâr DÜŞÜK

## 1. Replikasyon (yaz günleri, 47 hisse, 19.408 gözlem, 422 gün; gün kümelenmiş SE)
| y | CA | 2 yönlü FE (hisse+gün) |
|---|---|---|
| gap_{t+1} | −0,151 (t −3,5) | −0,156 (−6,3) |
| O→07:30_{t+1} | −0,197 (−4,0) | −0,211 (−6,9) |
| C→07:30_{t+1} | **−0,359 (−6,5)** | −0,370 (−10,6) |
| 07:30→C_{t+1} | +0,03 (0,4) | −0,01 |
| P15:00→07:30_{t+1} | +0,635 (11,5): müzayede hareketinin ~%64'ü kalıcı | |

- Portföy (|CA|>25, C→07:30): ham 14,2 bps (t 4,8), 5.870 işlem. Kesitsel arındırılmış: 13,9 (t 8,4).
- Yıllık eğim: 2024 −0,28 (FE t −6,2), 2025 −0,41 (−6,1), 2026 −0,35 (−6,0).

## 2. Çürütme denemeleri
**Veri hatası mı?** Hayır.
- Yahoo günlük C, vade sonu kesin uzlaşmasıyla (= spot kapanış seansı fiyatı) h1 döneminde %93,5 oranında birebir aynı.
- Kalan %6,5'in hepsi tam bölünme oranı (AEFES 10, BIMAS 2, FROTO 10, SASA 8 …).
- h1 ile günlük arasında ölçek kayması yok: ay-hisse medyan CA −34 ile +42 bps arasında.
- 06:30 barı bozuk değil: P07:30 = O yalnız günlerin %3–5'inde.

**Veri madenciliği:** Etki ızgarada düzgün ve sahte-OOS'tan geçiyor.
- Izgara: 6 eşik × 6 çıkış × ham/arındırılmış = 72 hücrenin hepsi pozitif.
- Sahte-OOS (parametre yalnız 2024 yazında, arındırılmış getiriyle seçildi): en iyi hücre |CA|>25 / 07:30. IS 13,3 (t 6,1) → 2025–26 OOS 14,2 (t 6,4). 36/36 hücrede OOS > 0, 32/36'sında t > 2.
- Uyarı: ham getiriyle seçim yapılsaydı 2024 verisi 14:30 çıkışını seçecekti; bunun OOS sonucu 4–10 bps (t 0,7–1,2).

**Plasebolar:**
- *Sahte müzayede:* son 30 dk sürekli işlem L30 → P15:00..07:30 için b +0,004 (t 0,1). L60 için +0,12 (t 2,4), yani devam. Yalnız müzayede hareketi dönüyor.
- *Permütasyon (500'er):*
  - Hisse içinde tarih karıştırma: null %99'u 6,5 (ham) / 4,9 (arındırılmış).
  - Aynı gün rastgele hisse (rastgele çift): null %99'u 3,6 / 3,4.
  - Gözlenen 14,2 / 13,9; p < 0,002.
- *Bayat sinyal CA_{t−1}:* 7,5 bps (t 2,6) çıktı, yani SIFIR DEĞİL. Ama bu bir artefakt değil, dönüşün ikinci gece de sürmesi.
  - CA otokorelasyonu 0,02.
  - Gece+sabah parçaları: t+1 −0,36, t+2 −0,10 (FE t −3,2), t+3 ≈0, t+4 −0,08 (t −2,7).
  - Gündüz parçaları hep ≈0.
  - C_t→C_{t+3}: −0,53 (t −2,9). Dönüş "%35, 10:30'da bitiyor" denenden büyük ve yavaş.

**Ortak faktör:** Yok.
- P&L ~ XU030 C→07:30: alfa 13,7 (t 3,6), beta 0,03.
- Ham uzun ayak (27,8) koşulsuz gece kaymasıyla şişmiş. Arındırılmış: uzun 10,0, kısa 22,5.

**Asimetri (yeni):** Asıl etki CA>0 tarafında, yani müzayede fiyatı yukarı ittiğinde.
- Eğim: CA>0 −0,45 (FE t −9,2), CA<0 −0,25 (t −4,0).
- |CA|>50: kısa ayak 40,6 bps (t 9,0), uzun 7,7 (t 1,0).
- |CA|>100: kısa 77, uzun −8.
- "Kapanışı yukarı işaretleme / fon NAV" literatürüyle uyumlu.

**Alt dönem:**
- 2014–17, 2018–20 ve 2021–23 dönemleri doğrudan TEST EDİLEMEZ (P15:00 yalnız 2023-11'den beri var).
- Yaz blokları (3 yıl × 3 parça): arındırılmış portföy 9/9 pozitif (8,3–18,9). Ama eğim Tem–Ağu 2024'te −0,01, Eyl–Eki 2026'da +0,09.
- Aylar: arındırılmış değer Mayıs dışında hepsinde t > 2.

**SSF baz vekili (2017–2026) mekanizmaya özgü DEĞİL** (1. aşamanın yorumu abartılı).
- Alt dönem katsayıları: 2017 +0,01 (t 0,9), 2018–20 +0,18 (11,8), 2021–23 +0,11 (4,7), 2024–26 +0,12 (9,3).
- h1 döneminde CA, vekil varyansının yalnız %12'sini açıklıyor.
- Vekilin CA'ya dik parçası da ertesi gap'i tahmin ediyor (+0,056, t 4,2); öngörü gücünün ~%60'ı CA dışından.
- Vekil 2021–26'da ertesi gün-içini de tahmin ediyor (+0,09, t 4,3). CA etmiyor (07:30→C +0,03).
- Sonuç: vekil, SSF'nin 18:05–18:15 fiyat keşfini ölçüyor; CA dönüşünün uzun dönem kanıtı sayılamaz.

**Kış (1. aşama uyarısını düzeltiyorum):** Ham getiriyle kışta etki 0,2 bps çıkıyor, ama bu piyasa gürültüsünden kaynaklanıyor.
- Hisseye özgü LH_id = LH − LH_XU030 (LH = log(C/P14:30)) → arındırılmış getiri:

| | Eğim (FE) | Portföy |LH_id|>25 |
|---|---|---|
| Yaz | −0,153 (t −5,8) | 10,8 (t 7,5) |
| Kış | −0,119 (t −2,7) | 7,5 (t 4,4) |

- 3 kış sezonu: 8,8 / 4,5 / 5,2. Etki büyük olasılıkla yıl boyu var.

**Uç değer:**
- En iyi 10 / 20 / 40 gün hariç: ham 10,0 / 7,6 / 3,4 (t 1,4); arındırılmış 11,6 / 10,1 / 7,5 (t 4,7).
- Medyan gün 16,7 bps, isabet %64. Blok bootstrap %95 güven aralığı [8,2; 19,0].
- En çok katkı veren 5 hisse (TOASO, ENJSA, TKFEN, HEKTS, ODAS) hariç 10,1 (t 3,0); 10 hisse hariç 7,6 (t 2,3). Hisselerin %85'i pozitif.
- Vade sonu hariç 14,3; toplu müzayede günleri hariç 12,6.

**Likidite (ex-ante, geçmiş 60 gün TL hacim tercilleri):**
- Alt 19,4 (t 4,8), orta 14,6 (3,9), **üst 1,5 (0,3)**.
- SSF'si likit olan büyüklerde etki yok. İddiadaki "likitlerde 7,7" ifadesi yanıltıcı.

**Tik:** |CA| ≥ 3 tik olan işlemlerde 13,4 (t 4,5), yani tik artefaktı değil.

## 3. İşlenebilirlik
**VİOP (pay vadelisi): UYGULANAMAZ.**
- SSF uzlaşma→uzlaşma ~ CA: **+0,26 (t 2,6)**, yani SSF ertesi gün CA YÖNÜNDE gidiyor. Dönüş stratejisi −11,8 bps (t −2,1).
- Ters işlem (SSF'de CA yönünde, 18:05–18:15 VWAP girişi): brüt +11,8 (t 2,1). 2024'te 4,9 (t 0,7). 8–15 bps maliyetle ≈0. Yalnız hipotez.

**Spot:** Giriş C'den, KFİ penceresinde (18:08–18:10); çıkış ertesi gün 10:30'da piyasa emriyle.
- Maliyet varsayımı: 4 bps komisyon + çıkışta 0,5–1 tik + kısa ayakta 2 bps ödünç.

| Eşik ve evren | Net (0,5 / 1 tik) | İşlem/gün |
|---|---|---|
| |CA|>25, tümü | +4,7 (t 1,6) / +0,2 | 14 |
| |CA|>25, likiditede alt 2/3 | +6,9 / +2,3 | |
| |CA|>25, likiditede üst 1/3 | −8 / −12 | |
| |CA|>50, likiditede alt 2/3 | +15,7 (t 2,8) / +11,1 (t 2,0) | ~3 |

- Açığa satış olmadan (yalnız uzun + XU030 hedge'i): |CA|>25 −2,4; |CA|>50 −6,9. **Kâr, kapanışta spot açığa satışa bağlı.** Kriz dönemlerinde SPK yasakları ve ödünç bulunabilirliği belirsiz.
- **Kapasite:** Müzayede + KFİ hacmi (üst sınır) günlük hacmin ~%3'ü. Etkinin yaşadığı hisselerde 2,6–7,4 mn TL/gün. Gerçekçi işlem büyüklüğü ≤0,5–1 mn TL; günlük beklenen kâr birkaç bin TL.

## 4. Düzeltilmiş iddia
- **Etki:** Spot kapanış müzayedesi hareketinin %35'i ertesi sabah 10:30'a kadar dönüyor (C→07:30 −0,36, t −6,5; FE t −10,6). İkinci gece ek ~%10–15 dönüyor.
- **Yön asimetrisi:** Dönüş esas olarak yukarı itilen kapanışlarda (−0,45). Aşağı itilenlerde −0,25.
- **Kapsam:** Etki hisseye özgü ve likiditede alt 2/3'te; en likit üçte birde yok. Arındırılmış kış vekili yıl boyu sürdüğünü gösteriyor.
- **Sağlamlık:** Plasebo, permütasyon, sahte-OOS ve uç değer testlerinden geçiyor.
- **IS/OOS:** İddiadaki "IS/OOS" h1'in iki yarısı. 2014–2023 için doğrudan test yok; SSF vekili bu boşluğu dolduramıyor.
- **İşlem:** VİOP pay vadelisiyle uygulanamaz (SSF CA yönünde ilerliyor). Spotta KFİ'de C'den giriş ve açığa satışla, |CA|>50 olan illikit hisselerde net ~+10–15 bps. Kapasite çok küçük.
