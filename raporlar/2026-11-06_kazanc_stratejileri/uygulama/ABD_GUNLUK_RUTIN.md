# ABD günlük rutin (TSİ): tek sayfa

**Ne için:** `PLAN_ABD.md` kurallarının her gün uygulanışı. Kural metni orada; § numaraları onu gösterir. Saatler TSİ (ABD kış saati; TSİ = ET + 8; seans 17:30–00:00).
**Araçlar:** IBKR Pro **nakit hesap** (TWS ya da Client Portal), TradingView günlük grafikte `kod/abd_rejim_ve_sablon.pine` (`ABD_RJ`, **derlenmedi, test edilmedi**; ilk kullanımda §2.5 değerleriyle karşılaştır), finviz, işlem günlüğü (§8.2).
**Değişmez kural:** 17:30–00:00 arasında emir girilmez, değiştirilmez, iptal edilmez (kritik ihlal, §8.5 DUR-6a). Bu saatlerde yalnız dolum bildirimi gelir.

## 1. Kapanış bloğu: gece 00:30–01:00 **ya da** sabah 08:00–09:00 (birini seç, her gün aynısı; 20–30 dk)

Gece bloğu VIX kapanışından (00:15) sonra başlar. Emirler seans dışında girilir; stoplar yalnız normal seansta (RTH) tetiklendiği için bu sırada korumasız an oluşmaz.

1. **Rejim (§2.2–2.4).** Yaz: durum; S&P / 200 GHO (< 1,02 ise yakın bölge); VIX/VIX3M dün ve bugün (biri ≥ 1,00 ise KIRMIZI); S&P ve NDX'te 10 > 20; S5FI / S5TH; ralli denemesinin gün sayısı; FTD (4. gün ve sonrası, S&P ya da NDX ≥ +%1,5, hacim artışı); SARI sayacı (3 kapanış gerekir); pilot freni.
2. **Risk panosu (§5; E ve NLV birlikte).** Açık gap-ayarlı ısı / tavan; küme ısıları; brüt maruziyet; en kötü hafta toplamı; ayın net gerçekleşen zararı + açık risk (Faz 1'de ≥ %3 E ise ay sonuna kadar giriş yok); merdiven kademesi (−%3 / −%5 / −%6,5 / dur −%8 E); kritik ihlal sayacı.
3. **Her açık pozisyon için çıkış kontrolü (§3.5–3.6), bu sırayla:**
   - İlk 3 seansta kapanış < pivot − 0,5 ATR (S2'de < sinyal günü dibi) → tamamen çık (MOO).
   - Kapanış ≥ dolum + 2R, ya da 4. seans kapanışı ≥ dolum + 1R → lot A MOO; lot B'nin stopu dolum fiyatına.
   - Kapanış ≥ +1,5R → stop dolum fiyatına.
   - Kapanış < 10 GHO (hızlı hisse) ya da < 20 GHO (diğerleri) → tamamen çık (MOO).
   - 10. seans: kâr < +1R **ve** son 5 seansta girişten beri en yüksek kapanış yok → tamamen çık (MOO).
   - Girişten +%100 → en az 1/2 MOO; kalan için kapanış ≤ en yüksek kapanış × 0,90 ya da < 10 GHO → çık.
   - Bilanço ya da ikili olay: son seans bugünse SELL MOC (stopla aynı OCA); MOC+OCA testi geçmediyse son seansın açılışında MOO.
4. **Emirleri gir (seans dışı).** Her satış emri, satılan lotun stopuyla **aynı OCA grubunda** ("Cancel all remaining orders with block"). Dünkü dolumlarda stopu böl: stop adedi lot B'ye iner, lot A için aynı fiyattan yeni GTC STP (OCA adı `TICKER-A`). Stop yükseltmeleri burada yapılır; **stop asla aşağı çekilmez**.
5. **Stop mutabakatı.** Her pozisyon için: canlı GTC SELL STP var mı, adetler toplamı pozisyona eşit mi, "yalnız RTH" açık mı? Eksik varsa hemen gir.
6. **Günlük (§8.2).** Dolum, kayma (bps ve R), komisyon, gerçekleşen R, MAE/MFE, TCMB kuru, TL maliyet/bedel, ihlal (kritik / diğer). Gölge kayıtlar (G1, G2) ayrı sekmede.
7. **G1 gölge taraması (yalnız kayıt):** `https://finviz.com/screener.ashx?v=152&f=cap_midover,earningsdate_prevdays5,sh_price_o20,sh_relvol_o3,ta_gap_u8&o=-gap` (gap ve RVOL son seansa bakar; kombinasyon bu oturumda çalıştırılmadı, kodlar HAZ §5b'de).

## 2. Akşam emir bloğu: 16:30–17:15 (10–15 dk; yalnız giriş)

1. **Veri günü mü** (CPI, PPI, NFP 16:30)? Öyleyse 16:45'ten önce emir yok. 16:45'te S&P vadelisi önceki kapanışa göre ±%1,5'ten fazla oynadıysa bugün yeni giriş yok.
2. **Takvim (§7).** Bugün "yeni giriş yok" günü mü (17.11, 25.11, 27.11, 9.12)? 22:00 TSİ olayı var mı (18.11 FOMC tutanakları)? Varsa giriş emirleri GTD, 21:55 TSİ'de düşer.
3. **Kaç emir?** N = min(günlük kalan giriş hakkı; boş pozisyon yeri; ⌊kalan ısı / (1,25 × 1R)⌋). Bekleyen emirler dolmuş sayılır. Σ(adet × limit) ≤ min(kalan brüt tavan; yerleşmiş USD nakit − NLV'nin %5'i). SARI'da günde ≤ 2, YEŞİL'de ≤ 3; yakın bölgede toplam 1 pozisyon.
4. **Aday kontrolü** (Cumartesi listesinden): 10 seans içinde bilanço ya da ikili olay varsa çıkar; pre-market haber; stop 1,0–2,0 ATR ve ≤ %8; adet limite göre; pozisyon ≤ %7,5 E; küme izni ve tetik (K9 dışı kümelerde FTD ya da S&P 10 > 20).
5. **Emir.** BUY STP LMT (DAY, "outside RTH" kapalı) + ekli GTC SELL STP (piyasa, yalnız RTH). N'yi aşan adaylar OCA gruplarına; aynı kümenin adayları aynı grupta. Emir değeri ön ayarı (%7,5 E) uyarı verirse emir hatalıdır, düzelt.
6. **Kayıt.** Emir ekranının görüntüsü ve günlüğe "plan" satırı. Bitti; 17:30'dan sonra ekran yok.

## 3. Haftalık ve aylık

| Ne zaman | İş |
|---|---|
| Perşembe | TCMB haftalık rezerv verisi → döviz anahtarı (§1.5) |
| Cumartesi (60–90 dk) | Finviz sıkı ve geniş trend şablonu URL'leri (HAZ §5a) ve TradingView ücretsiz standart tarayıcı. Kısa listeyi `ABD_RJ` ile grafikte kontrol et (TT, RS/52H, 52H uzaklığı, ADR, ATR, uzamış). Finviz endüstri grupları (3 ay). İzleme listesi tablosu: kurulum, pivot, tetik, limit, stop, stop/ATR, adet (50k / 250k / 1m), bilanço ve ikili olay tarihi. Cuma kapanışına göre acil stop: son 10 seansın dibi − %0,5 (yalnız yukarı). Haftalık uyum satırı: ihlaller, "dışarıda kalma" günleri, G2. Her 10 canlı işlemde istatistik (§8.3) |
| Ayın son hafta sonu | Küme izni (HAZ §5c skoru, §4.3) ve 60 günlük korelasyonlar. E'nin yeniden hesabı. Aylık rapor: USD, % E, % NLV; "TL mevduata göre" sütunu yalnız bilgi, karar için kullanılmaz (§8.6). Faz kapısı |
| 1–4.12 | Vergi kontrol noktası; kazanç hasadı yalnız müşavir onayıyla (§6.5) |
| 8.12 kapanışı | FOMC, CPI ve bütçe süresi için makro gap-ayarlı ısı (§5.3) |

## 4. Asla

AI çip, güç ya da veri merkezinde dip alımı · bilanço ya da ikili olay öncesi giriş · zarardaki pozisyona ekleme · stopu aşağı çekmek ya da iptal edip yeniden girmemek · KIRMIZI/TURUNCU'da canlı giriş · girişte risk > 1,25 × 1R · opsiyon, kaldıraçlı ETF, margin, açığa satış · seans içinde emir değiştirmek. **İlk kritik ihlal: 10 seans yeni işlem yok + yazılı inceleme. İkincisi (12 ay içinde): plan durur.**
