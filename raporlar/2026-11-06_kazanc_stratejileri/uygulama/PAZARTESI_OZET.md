# Pazartesi 9 Kasım 2026: tek sayfa özet (BIST/VİOP + ABD)

_Ayrıntı ve gerekçeler: `PLAN_BIST.md`, `PLAN_ABD.md`. Rakamlar 05.11 kapanışına göre; Cuma 06.11 kapanışıyla `tarama/` altında yenilenir. Yatırım tavsiyesi değildir._

## Bugünkü durum

| | BIST/VİOP | ABD |
|---|---|---|
| Cuma 06.11 | — | S&P 7.376,86 (+%0,31), 200 GHO'nun %0,7 üstünde, 10 < 20. Nasdaq +%1,1, NDX ~+%2. NFP +165 bin, işsizlik %4,1. Ralli denemesinin 1. günü 06.11, FTD en erken 11.11. Hâlâ KIRMIZI: 05.11'deki VIX/VIX3M 1,10 son iki kapanış içinde. Ayrıntı: `tarama/abd_rejim_20261106.md` |
| Rejim | **KAPALI** (7 göstergenin 0'ı açık; Cuma 06.11 kapanışıyla da değişmedi). XU100 11.483, 5 günde +%6,7 ama 200 günlüğün %15,4, 50 günlüğün %9,1 altında. XBANK 16.398, 200 günlüğün (16.948) %3,2 altında; bankalar 126 günlük göreli güç zirvesinde. Net rezerv bir haftada −6,5 mlr $. | **KIRMIZI.** VIX/VIX3M 1,10. S&P ve Nasdaq'ta 10 günlük ortalama 20 günlüğün altında, dip teyit günü (FTD) yok. |
| Pazartesi canlı işlem | **Yok** (çekirdek dışında) | **Yok** |
| En erken ilk risk | Sinyal gelirse K1 (SAHOL↔AKBNK) ve K4 sondası. Rejim GEÇİŞ'e en erken 26.11'de dönebilir. | İlk pilot en erken **16.11, 16:45–17:15 TSİ**, tek pozisyon, %0,25 risk |

## Pazartesi yapılacaklar

**BIST hesabı (09:00–12:00):**
1. Hesabın %15'i doğrudan bankada 32 günlük mevduata (1. dilim). %85'i banka iştiraki PPF'ye; tasfiyedeki 7 portföy şirketinin fonları asla. Kalıcı hedef %60 mevduat / %40 PPF; dilimler 16, 23 ve 30.11'de.
2. Aracı kuruma 12 yazılı soru gönder (Kural 0): VİOP teminatı faiz kazanıyor mu? Kurum teminat oranları? Sunucu taraflı stop var mı? Cevap gelmeden VİOP kolu yok.
3. Kapanış bazlı alarmlar (Cuma 06.11 kapanışıyla güncel; kaynak `tarama/bist_sinyal_20261106.md`):

   | Alarm | Tetik | 06.11 kapanışı | Gereken | Not |
   |---|---|---|---|---|
   | ENERY | > 14,60 | 14,05 | +%3,9 | AHGAZ ile tek isim sayılır. Bilanço 9.11 akşamı, karar en erken 10.11. |
   | AHGAZ | > 48,70 | 46,82 | +%4,0 | ENERY ile tek isim sayılır. Bilanço 9.11 akşamı, karar en erken 10.11. |
   | ENJSA | > 127,00 | 122,00 | +%4,1 | — |
   | KCHOL | > 225,50 | 206,10 | +%9,4 | — |
   | RYSAS | > 30,28 | 27,34 | +%10,8 | Spot, ×0,75 boy |
   | XU100 | 12.630 (SMA50) / 13.566 (SMA200) | 11.483 | — | — |
   | XBANK | 16.948 (SMA200) | 16.398 | — | — |
   | K1 SAHOL↔AKBNK, z=+2 | SAHOL ≥ 93,06 ya da AKBNK ≤ 64,40 | Bugün z −0,54 | — | Öbür bacak sabitken |
   | K1 SAHOL↔AKBNK, z=−2 | SAHOL ≤ 84,09 ya da AKBNK ≥ 71,27 | — | — | Öbür bacak sabitken |

   - Aynı kümede oldukları için ENERY, AHGAZ ve ENJSA'dan en çok bir pozisyon açılır.
   - KAPALI rejimde K4'te en çok 2 sonda açılır, %0,25 riskle.
   - 06.11 VİOP bülteni (resmi uzlaşma):
     - F_XU0301226 14.878, XU030 spot 14.290. İma basit faiz %27,3 (bileşik %30,7), 05.11'de %29,3 idi.
     - Nakit-taşıma eşiği %35,6 olduğu için bu kol kapalı.
     - Vadeli spota göre 55 günde ~%1,3 ucuz. Rejim açılırsa endeks long'unu vadeliyle kurmak spottan biraz ucuz.
   - F_USDTRY1126 ima faizi %29,9 (KRİZ eşiği %41).
   - K6 carry kapısı kapalı.
4. Dışlama listesini emir ekranında "yasak" yap: fon tasfiyesi baskısındaki hisseler ve SPK'nın suç duyurusunda bulunduğu 13 hisse (`PLAN_BIST.md` §4.2).

**ABD hesabı:**
1. Strateji sermayesini yaz. Para TL'deyse E = likit servetin %10'u (en çok %15'i). Bunun %40'ı bu sabah SWIFT'le IBKR nakit hesabına gider; önce küçük bir tutarla kur makasını ölç. %10'u PPF'ye, %50'si 32 günlük mevduata.
2. Hesap fonlanınca 1 adetlik emir testleri: BUY STOP-LIMIT + ekli GTC stop, MOO/MOC, OCA grubu. Midas yalnız ≤500 $ ile test; ekli stop yoksa kullanılmaz.
3. İzleme listesi ve işlem günlüğü. Opsiyon, margin ve kaldıraçlı ETF yok.

**Servet düzeyinde (yazılı karar):** Ölçü birimin TL engeli mi, USD mi? Döviz anahtarı servetin tamamına uygulanır; tetikleri `PLAN_ABD.md` §1.5'te. BIST planındaki "kur koruması yok" kararı yalnız BIST işlem hesabı içindir.

## Haftanın takvimi (TSİ)

| Gün | Olay | Ne yapılır |
|---|---|---|
| Pzt 9.11 | 3Ç konsolide bilançoların son günü | 18:00'den önce bilançosu çıkmamış hisseye kapanışta giriş yok |
| Sal 10.11 | 16:30 ABD TÜFE | ABD'de 16:45'ten önce emir yok |
| Çar 11.11 | ABD tahvil piyasası kapalı | BIST'te hiçbir kolda yeni giriş yok. ABD'de FTD var mı, bak. |
| Per 12.11 | 01:00 MSCI duyurusu. 14:30 TCMB rezervleri. Akşam SPK bülteni. | MSCI'ın çıkardığı hisseler 30.11'e kadar alınmaz. Rezerv bir hafta daha ≤−5 mlr $ gelirse BIST KRİZ kesicisi tetiklenir: 5 gün yeni giriş yok. Döviz anahtarına da bak. |
| Cum 13.11 | Kredili işlem esnekliği bitiyor | Uzatılmazsa kırılım girişleri 23.11'e, VİOP-47 dışında long 30.11'e kadar yok |
| Pzt 16.11 | — | Mevduat 2. dilim. ABD'de ilk pilot için en erken gün. |
| 30.11 | VİOP Kasım vadesi, MSCI değişikliklerinin yürürlüğü | Pay vadelisini fiziki teslimata taşıma |
| 10.12 | PPK (anket: %35) | Sürprizsiz indirim olursa bankalarda ~15.03.2027'ye kadar yarım boy |

## Kollar ve sınırlar (özet)

**BIST:**

| Kol | Kural | Not |
|---|---|---|
| K1 | SAHOL↔AKBNK, 60 günlük z ≥2, VİOP, ertesi kapanışta giriş, 20 gün tut | Rejimden bağımsız |
| K3 | Temettü öncesi 5 gün, spot | Rejimden bağımsız |
| K3b | Yüksek verimli temettü (≥%5) | Pilot 01.02.2027 |
| K4 | Kırılım: 52 haftalık zirve + trend şablonu + %15 iz-stop | Risk KAPALI %0,25 (en çok 2), GEÇİŞ %0,5, AÇIK %0,75 |
| K6 | Carry | Kapalı |
| K8 | Halka arz katılımı | Seri bozulduğu gün kapanışta sat |

- Toplam açık risk KAPALI'da ≤%2,5. Uydu aylık −%2,5'te durur.

**ABD:**
- Kurulumlar: S1 baz kırılımı ve S2 10/20 günlük ortalamaya geri çekilme. Girişler 16:45–17:15'te bekleyen emirle, çıkışlar gece 00:30–01:00'de ya da sabah. 17:30–00:00 arasında ekran yok.
- Risk: işlem başı %0,25, küme ≤%0,75, toplam açık risk sarıda %1,25.
- Aylık devre kesici %3. Strateji sermayesi −%8'e inerse plan durur.

**İkisinde de asla:**
- kredili işlem
- piyasa emri
- stopu aşağı çekmek
- zarara ekleme
- plan dışı işlem (BIST'te yalnız K9 kanalı, %0,25 risk)
- dışlama listesindeki hisse
- tavan serisi bittikten sonra halka arz alımı

## Neden bu kadar temkinli?

İki piyasada da rejim şu an yüksek getirili swing stratejilerine karşı.
- **BIST:** Bu rejimde kanıtın tavanı çıta + birkaç puan. Merkez beklenti +1…+2 puan, %80 aralık −2…+5,5 puan.
- **ABD:** İlk faz bir ispat dönemi. Yüksek getiri, kenar 100 işlem ve 12 ayda kanıtlanıp risk %0,75–1'e çıktığında gelir.

Rejim döndüğünde kurallar boyutu kendiliğinden büyütüyor. Kârın çoğu o zaman birkaç büyük işlemden gelir. Planın amacı o ana hazır ve ölçülmüş girmek.
