# Araştırma verimliliği: geçmiş oturumların analizi ve yeni protokol (10.11.2026)

## Kısa yanıt

- 28 Ekim – 9 Kasım arasındaki 23 oturum, liste fiyatıyla yaklaşık **3.760 $** değerinde kullanım yaptı. Şu anki planında haftalık kotanın tamamı yaklaşık **2.200 $**'a denk geliyor.
- Harcamanın **%92'si alt ajanlarda**, **%89'u Opus'ta**. 156 iş akışının 155'inde alt ajana model yazılmamış; hepsi oturumun en pahalı modelini devralmış.
- İsraf, kaliteyi getiren şeylerde değil şunlarda: mekanik işi de pahalı modelle yapan çok sayıda ajan, ajan başına uzun araç döngüsü, her üreticiye bir ya da birkaç doğrulayıcı, okunmayan hacim.
- Çözüm iki parça: depo kökündeki `CLAUDE.md` (protokol, yani istediğin prompt) ve aşağıdaki 5 adım.
- Beklenen etki: benzer işler için kabaca 5–10 kat daha az kota. Bu bir tahmin; protokolle henüz gerçek bir araştırma çalıştırılmadı.

## Ne yapmalıyım

1. **Ultracode'u kapat.** Oturumun başında `/effort ultracode off` yaz. Bu oturumda açıktı; 9 Kasım'daki Arthur Morgan oturumunda da asistan açık olduğunu söylemişti. Açıkken ajana “her esaslı işte çok ajanlı iş akışı kur” deniyor. Protokol bununla çelişmemesi için yazıldı, ama güvenilir çözüm ayarı kapatmak. Mobil uygulamada bu ayarın nerede durduğu ve oturumlar arasında kalıcı olup olmadığı belgelenmemiş; yeni oturumda “ultracode açık mı?” diye sorarak kontrol edebilirsin.
2. **Protokolü varsayılan dala al.** `CLAUDE.md` şu an `claude/research-efficiency-tokens-5vrjbl` dalında. Yeni oturumlar deponun varsayılan dalını klonluyor; dosya oraya girince her oturuma ve her alt ajana kendiliğinden yüklenir. İstersen bunun için bir PR açarım.
3. **İsteğe bağlı emniyet:** bulut ortamının ayarlarına `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` değişkenini ekle. Model yazılmamış alt ajanlar o zaman Opus yerine Sonnet'e düşer. Belgelere göre iş akışı ajanlarına da uygulanıyor; bulut oturumunda çalıştığını ben sınamadım.
4. **Bir araştırma, bir oturum.** Bir saatten uzun aradan sonra ya da konu değişince yeni oturum aç. Bağlamı 300 bin token'ı geçmiş oturumlara yazılan 18 takip mesajı, hiçbir ajan çalıştırmadan toplam 80 $ tutmuş: mesaj başına ortalama 4,4 $. Küçük bağlamlı oturumda aynı tür mesaj 1,4 $. Örnek: “21.05'te değil 17.55'te ver” 6,3 $.
5. **Ana model Opus yeter.** Fable'ı araştırma oturumunun ana modeli yapma; Diş lisans oturumunda alt ajanlar Fable'ı devraldı ve o oturumun 316 $'ının 273 $'ı Fable'dan geldi. Basit sorularda `/model sonnet` de yeter.

İstek yazarken yalnızca sorunu yaz. İstersen sonuna `Seviye: S`, `M` ya da `L` ekle. “Maksimum ajan”, “gazı ver” yazmana gerek yok; “kotam az” yazman da kaliteyi düşürmez, protokol bu sözleri sürecin alt ucuna çevirir.

## Gerekçe ve kanıt

### Oturum başına harcama

Kota payı, şu anki planın haftalık ~2.200 $'ına göre hesaplandı (2 Kasım'dan önceki plan daha küçüktü).

| Oturum | Maliyet | Haftalık kota payı | Alt ajan |
|---|---|---|---|
| VİOP lead-lag | 654 $ | %30 | 86 |
| BIST + ABD kazanç stratejileri | 483 $ | %22 | 59 |
| XAUUSD | 358 $ | %16 | 62 |
| Takipçi artırma (yıllık takvim) | 330 $ | %15 | en az 33 |
| 1876 Balkan haritaları | 325 $ | %15 | 66 |
| Diş hekimliği lisansı ABD/Kanada | 316 $ | %14 | 188 |
| Jung'un bütün kitapları | 214 $ | %10 | 243 |
| Osmanlı Balkanı şahsiyetleri | 189 $ | %9 | 40 |
| ETF stratejileri | 187 $ | %8 | 24 |
| Psikoloji kitap özetleri | 133 $ | %6 | 21 |
| Diş hekimliğinde iş yeri | 131 $ | %6 | 39 |
| DUS / INBDE stratejisi | 119 $ | %5 | 26 |
| Arthur Morgan | 74 $ | %3 | 10 |
| Fotoğraf arşivleri | 70 $ | %3 | 29 |
| Rumeli Instagram (isim, logo) | 55 $ | %2,5 | 26 |
| Instagram telif | 44 $ | %2 | 12 |
| BIST 5 ajanlı komite | 41 $ | %2 | 5 |
| Arkadaşlıkta “nazar” etkisi | 16 $ | %0,7 | 8 |
| Havacılık endeksleri ve DXY | 6 $ | %0,3 | 0 |
| Mu kıtası | 6 $ | %0,3 | 5 |
| Kendini beğendirme | 5 $ | %0,2 | 5 |

### Para nereye gitti

- **Model.** Opus 3.347 $, Fable 273 $, Sonnet 68 $, Haiku 70 $. Kayıtlardaki birim fiyatlara göre Sonnet, Opus'un yarısı; Haiku kırkta biri.
- **Alt ajanlar.** 13 günde 987 alt ajan. Ana ajanın kendi döngüsü harcamanın yalnızca %8'i.
- **Doğrulama katmanı.** Ajanların %46'sı doğrulayıcı, hakem, çürütücü ya da düzeltici. Çoğu işte üretici başına bir, bazılarında iki-üç.
- **Araç döngüsü.** Ajan başına araç çağrısı medyanı 36, üst çeyrek 73; iş akışlarının onda birinde 100'ün üstünde. Bir iş akışında ajanlara “15–25 arama” denmiş, ortalama 95 çağrı yapmışlar. Ajan başına maliyet 0,9 $ ile 10 $ arasında değişiyor ve çağrı sayısıyla birlikte artıyor.
- **Bağlam.** Harcamanın üçte biri yazılan metin, üçte ikisi bağlam: araç sonuçlarının yazılması ve her çağrıda yeniden okunması.
- **Belirsiz ekonomi sözleri işe yaramadı.** “Rasyonel ol, f/p” denen Jung 214 $, “idareli kullan” denen psikoloji özetleri 133 $ tuttu. “Eko yap, kotam az” denen havacılık işi 6 $ tuttu ve sunulamaz çıktı.

### Ajan sayısı nereye kadar verimli

- **8 ajana kadar:** 5–16 $. En iyi fiyat/kalite örneği burada: 4 araştırmacı ve 4 doğrulayıcı, 16 $, 14 mekanizma, 110 atıf kontrolü. Bu işte ana ajan her araştırmacıya kendi hipotezlerini ve aday kaynakları önceden vermişti.
- **10–40 ajan:** 44–189 $.
- **60 ajan ve üstü:** 214–654 $. Bu oturumların ardından gelen mesajların: “neye göre trade yapmam gerektiğini anlamadım”, “o kadar karmaşık ki basitleştir”, “raporum nerede”. VİOP işinde kendi değerlendirmen: onca listeden 3–4 sinyal işe yaradı.
- Anthropic'in çok ajanlı araştırma sistemi yazısındaki ölçek: basit olgu sorusu 1 ajan ve 3–10 araç çağrısı; karşılaştırma 2–4 alt ajan, ajan başına 10–15 çağrı; karmaşık araştırma 10'dan fazla alt ajan. Senin büyük oturumların 24–243 ajan kullandı; basit bir soru olan Mu kıtası bile 5 ajan.
- Aynı yazı token kullanımının performans farkının %80'ini açıkladığını da söylüyor. Yani token kaliteyi gerçekten artırabiliyor; mesele hangi token. Protokol bağımsız kaynak taramasını ve sonucun dayandığı iddiaların doğrulanmasını koruyor. Kestiği şeyler: mekanik işte pahalı model, tekrarlanan arama, uzun döngü, her satıra çoklu doğrulama, okunmayan hacim.

### Protokolün seviyeleri ve tahmini maliyet

| Seviye | Alt ajan | Tahmini maliyet | Haftalık kota payı |
|---|---|---|---|
| S | 0–2 | 1–3 $ | ~%0,1 |
| M | 4–9 | 10–20 $ | ~%0,5–1 |
| L | en çok 24 | 35–60 $ | ~%2–3 |

Tahmin, kayıtlardaki ajan başı maliyetten türetildi: 20 çağrı civarında kalan bir Opus ajanı 1,2–2 $ tutmuş, Sonnet bunun yarısı; üstüne ana ajanın 3–20 $'lık kendi döngüsü.

### Kuru çalıştırma

Taslak, geçmişteki 6 gerçek isteğin üzerinde yalnızca plan çıkartılarak sınandı. Hiçbiri çalıştırılmadı.

| İstek | Geçmişte | Protokolle plan |
|---|---|---|
| Mu kıtası | 5 ajan, 6 $ | S, 0 ajan |
| Arkadaşlıkta “nazar” etkisi | 8 ajan, 16 $ | S, 1 ajan |
| DUS / INBDE stratejisi | 26 ajan, 119 $ | M, 8 ajan |
| XAUUSD | 62 ajan, 358 $ | L, 11 ajan |
| Jung'un bütün kitapları | 243 ajan, 214 $ | L, 19 ajan |
| Havacılık endeksleri ve DXY | 0 ajan, 6 $, sunulamaz | 2 ajan, sunulabilir rapor |

Planlayıcılar ve iki eleştirmen 16 sorun buldu; hepsi son sürüme işlendi. En önemlileri: “kotam az” sözünün kaliteyi düşürmemesi, alıntı ve sayı çıkarmanın Haiku'ya verilmemesi, backtest sonuçlarının ayrıca doğrulanması, karar tablosunun ana raporda kalması, alt ajanların dosyanın yalnızca ilk paragrafını uygulaması.

## Emin olunmayanlar ve doğrulama kapsamı

- Dolar tutarları, oturum kayıtlarındaki kullanım verisinin liste fiyatı karşılığıdır; abonelikte bu para ödenmiyor. Kotanın modelleri nasıl ağırlıklandırdığı belgelenmemiş. “Haftalık kota ≈ 2.200 $” iki haftalık pencerede kota yüzdesi ile maliyetin karşılaştırılmasından çıktı (2.155 $ ve 2.277 $).
- 5–10 kat tasarruf ölçülmedi, tahmin. İlk iki-üç araştırmada rapor sonundaki maliyet satırını bu tabloyla karşılaştır.
- Kalite riski: Sonnet üreticiler Opus'un yakalayacağı bir şeyi kaçırabilir. Karşılığında örneklemli doğrulama, hata oranı yüksekse tam kontrol ve üst modele çıkma kuralı var. İlk işlerde kalite düşerse seviyeyi yükselt (`Seviye: L`); protokolü kaldırma.
- Araç bütçesi sert biçimde uygulanamıyor; ajan bütçeyi aşabilir. Protokol aşımı görünür kılıyor (`araç: kullanılan/bütçe`) ve sonraki dalgayı daraltıyor.
- Ultracode'un geçmiş oturumların hepsinde açık olduğu kayıtlardan görülemiyor; iki oturumda kesin.
- Takipçi artırma oturumunun ilk bölümü okunamadı (ilk mesaj ve 6 iş akışı betiği eksik); maliyet toplamı tam.
- Kapsam: 23 oturumun tamamı, 887 sayfa olay kaydı okundu. Fiyat katsayıları kayıtlardaki maliyet alanıyla sınandı (Sonnet ve Haiku'da birebir, Opus'ta R² 0,9995).

## Kaynaklar

- 23 oturumun olay kayıtları (kullanım, kota ve iş akışı olayları).
- Claude Code belgeleri: [maliyet](https://code.claude.com/docs/en/costs.md), [iş akışları](https://code.claude.com/docs/en/workflows.md), [alt ajanlar](https://code.claude.com/docs/en/sub-agents.md), [model ve efor](https://code.claude.com/docs/en/model-config.md), [önbellek](https://code.claude.com/docs/en/prompt-caching.md), [bulut oturumları](https://code.claude.com/docs/en/claude-code-on-the-web.md).
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), 13.06.2025.

## Ek: protokolün yüklenmediği yerde kullanılacak kısa sürüm

`CLAUDE.md` varsayılan dala girene kadar ya da başka bir depoda, isteğinin sonuna bunu yapıştır:

```
Araştırma kuralları: Kalite düşmeyecek, token israfı olmayacak.
1) Önce seviye seç ve tek satırla bildir: S = alt ajansız, sen en çok 20 araç çağrısı.
   M = 3–6 üretici + 1–3 doğrulayıcı. L = en çok 18 üretici + 6 doğrulayıcı, öğeleri 3–5'li grupla.
2) Her alt ajana model yaz: veri indirme ve biçim işi haiku; araştırma, yazım, kod ve
   kaynak kontrolü sonnet; yöntem denetimi ve eleştirmen opus. Sentezi sen yap.
3) Her alt ajana dar soru, kendi hipotezlerin ve aday kaynaklar, en fazla 20 araç çağrısı.
   Dönüş: 400 kelime özet + iddia defteri (iddia | URL | kısa alıntı ya da sayı | güven).
4) Doğrulama: sonucun dayandığı ve şaşırtıcı iddialar tam, kalanı örneklemle.
   Rapordaki her sayı, tarih ve alıntı bir defter satırına dayansın. Tartışma = tek eleştirmen turu.
5) Teslim: tek rapor, önce 6 satırlık kısa yanıt, sonra somut adımlar. Dosyayı sohbette gönder.
   Sonuna ajan sayısını modele göre yaz.
```

## Devam notu

- Bulgular: 23 oturum, ~3.760 $ liste karşılığı, %92 alt ajan, %89 Opus; haftalık kota ≈ 2.200 $.
- Çıktılar: `CLAUDE.md` (protokol, depo kökü) ve bu rapor. Dal: `claude/research-efficiency-tokens-5vrjbl`.
- Açık işler: protokolün varsayılan dala alınması; ultracode'un kapatılması; ilk gerçek araştırmada maliyetin ölçülmesi.
- Ham veri bu oturumun geçici klasöründeydi, depoya eklenmedi.
- Yatırım tavsiyesi içermez; yalnızca kullanım analizi.

Maliyet özeti: Seviye L · 10 tarama ajanı (haiku) + 2 belge ve web ajanı (haiku) + 6 plan ajanı ve 2 eleştirmen (opus) · 2 dalga · bu oturum yaklaşık 25–30 $, haftalık kotanın ~%1,3'ü.
