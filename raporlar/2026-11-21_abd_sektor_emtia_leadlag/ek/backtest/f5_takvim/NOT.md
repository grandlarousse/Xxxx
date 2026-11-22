# F5 Takvim etkileri: not

**Kısa yanıt:** Takvim kurallarının hiçbiri 1-3 günlük kapanış alımında bugün tek başına sinyal değil. Sonuç: 0 SAĞLAM, 0 KOŞULLU, 3 İZLE. Ay dönümü, FOMC öncesi yükseliş ve haftanın günü etkileri 2005-2018'de (IS) vardı, 2019 sonrasında (OOS) kayboldu.

**Testler:** 53 kural x 33 hedef = 1.749 test. Haftanın günü iki yönde sayıldı. BH, F5 ailesi içinde uygulandı. Beklenen yanlış pozitif: 0,07 SAĞLAM, 0,24 KOŞULLU. Ayrıca her kural için 25 hisse ETF'inin eşit ağırlıklı havuz testi var (`kural_ozet.csv`); betimleyicidir, sınıflanmaz.

**Eleme:**
- IS t ≥ 2,5 veren 6 test var; hiçbiri OOS t ≥ 2,0 vermedi.
- Ön elemeden 8 test geçti; hepsi B koşulunda kaldı.
- İZLE olan üç test:
  - `tom_b|TLT` (T-3 → T): IS t 2,83, OOS t 1,53; 2024 sonrası -14 bps.
  - `fomc_once|HYG`: IS t 2,10, OOS t 1,54; 2024 sonrası net -6 bps; en büyük işlemler 2008-09'dan.
  - `opex_sonra_hafta_aylik|OIH`: h = 5, profil dışı; işlem başına 121 bps ama tek işlem ±%10-13 oynuyor.
- OOS t ≥ 2,5 veren 5 testin IS t'si sıfır ya da ters (XLU tatil öncesi, XLF/XLRE T-1, OIH vade haftası). Seçim yalnız IS'te yapıldığı için sayılmaz.

**Havuz (maliyetli, IS t / OOS t):**
- Ay dönümü T-4 → T-1: 2,02 / -0,14.
- T+1 takastan sonra (28.05.2024 sonrası, 30 ay) T-4 → T-1 ve T-3 → T pencerelerinde hedef medyanı -16 / -24 bps. Takasın etkiyi bir gün kaydırdığı hipotezi desteklenmiyor.
- FOMC öncesi gün: 2,05 / -0,26. VIX > 20 iken: 52 bps, 2,01 / 0,55.
- Tatil öncesi: 0,39 / 2,00. Etki yalnız son dönemde var.
- Vade haftası SAT: -0,26 / 1,55. 1. dalgadaki -16 bps bulgusu IS'te yok.
- TÜFE ve istihdam günleri: sıfıra yakın.
- Haftanın günü: maliyetten sonra hepsi negatif. DBA, CPER ve HYG'de iki yönün de t ≤ -3 olması günlük 10-20 bps maliyetten geliyor, sinyal değil.

**Filtre mi?** Maliyetsiz havuzda IS ve OOS'ta aynı işaretle |t| ≥ 1,5 veren kural yok. 1 ile 1,5 arasında kalan zayıf adaylar:
- AL'dan kaçın: çeyrek dışı ay sonu son gün (-19 bps; OOS t -2,2); FOMC karar günü alıp 2 gün tutma (-30 bps).
- Hafif ekle: tatil öncesi gün (+15 bps).

Bunlar ancak başka bir sinyalin zamanlamasında ikincil filtre olabilir.

**Hipotezle çelişenler:**
- Ay sonu son gün (T) "+" diye yazılmıştı; çeyrek dışında negatif çıktı. 14 hedefte OOS t ≤ -2, KRE'de IS t -2,0 / OOS t -3,4. Ters yön sınıflanmaz; ileride keşif olarak sınanmalı.
- UNG perşembe SAT (14 bps, t 0,9 / 1,1) tutmadı.
- USO perşembe AL tutmadı: tüm dönemde 4 bps; 2024 sonrası 52 bps, t 2,0.

**Bugünkü rejim (dünkü VIX > 20; bilgi amaçlı, sınıflanmadı):**
- Ay dönümü T-4 → T-1 havuzu: 96 bps, 2,00 / 1,23 (n = 78).
- FOMC sonrası 1-2 gün: -65 / -69 bps.

**20.11.2026 kapanışı:** Vade günüydü. `opex_sonra_h1..h3` ve `al_cum` açık ama ayakta değil. İZLE girişleri: TLT 24.11 ve 28.12, HYG 8.12. OIH kuralı açılmıyor çünkü 27.11 haftasında tatil var. Gün gün liste: `takvim_6hafta.csv`.

**Veri:**
- FOMC: 2021-2026 fomccalendars.htm'den, 7 yıl fomchistorical sayfalarından (toplam 8 sayfa), 9 yıl bellekten. Sayfası çekilen 7 yılda bellek listesi sayfayla birebir tuttu. 1.8.2018 toplantısı sayfada bulunamadı, bellekten eklendi. 2020 Mart toplantısı iptal edildi. 175 karar günü (9.12.2026 dahil): `fomc_tarihleri.csv`.
- TÜFE ve istihdam: bls.gov arşivi. Kutsal Cuma'ya düşen 9 rapor atlandı. Aralık tarihleri BLS takviminden.
- Tatiller NYSE takvim boşluklarından çıkarıldı; Sandy (2012) çıkarıldı. Yarım günler kurala göre belirlendi: Şükran sonrası cuma, 24 Aralık, 3 Temmuz.
- Vade haftası kuralları yalnız 5 günlük tam haftalarda uygulandı. CPER'de ertesi açılış girişi kullanıldı.
- SAT bacağında "ham net ≥ 0" şartı kütüphane dışında eklendi.
- H koşulu: dairesel plasebo p ≤ 0,025 ve etki, 1-4 gün kaydırılmış sinyallerin ortalamasından büyük olmalı.
