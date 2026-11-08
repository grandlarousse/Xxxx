# Görev P: takvim 2026-11-09 → 2027-07-06 (sinyal_altin.py takvim fonksiyonları + birincil kaynaklarla doğrulanmış olay saatleri)
# DENETİM (2026-11-08): bitiş 30.06 → 06.07.2027 (QEND çıkışı 02.07 ile Bağımsızlık Günü 05.07'nin E1-C2 giriş/çıkışı ve 02.07 NFP kapsansın);
#   NYSE yarım günü metni/saati, TR yarım günü metni, vade sonu LBMA saatleri ve kanıt, idari izin notu düzeltildi. Tarihler birincil kaynaklarla
#   denetlendi: nyse.com (2026–27 tatil/erken kapanış), federalreserve.gov (FOMC 2026–27), bls.gov (CPI/NFP 2026–27), ICE LBMA 2026/2027 PDF, Diyanet 2027.
import sys, datetime as dt
import pandas as pd

S_ = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S_}/out/sentez")
import sinyal_altin as SA
from zoneinfo import ZoneInfo

D = dt.date
BAS, BIT = D(2026, 11, 9), D(2027, 7, 6)
NY, IST = ZoneInfo("America/New_York"), ZoneInfo("Europe/Istanbul")
GUN = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
def g(d): return f"{d:%d.%m.%Y} {GUN[d.weekday()]}"
def tsi_et(d, hh, mm=0):
    return dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=NY).astimezone(IST).strftime("%H:%M")
def etf_emir(d):
    if SA.nyse_yarim(d): return f"12:50–12:58 ET ({tsi_et(d, 12, 50)}–{tsi_et(d, 12, 58)} TSİ; yarım gün, kapanış 13:00 ET)"
    return f"15:50–15:58 ET ({tsi_et(d, 15, 50)}–{tsi_et(d, 15, 58)} TSİ)"

rows = []
def add(d, cephe, olay, ne, saat="", kaynak=""):
    rows.append(dict(tarih=str(d), gun=GUN[d.weekday()], cephe=cephe, olay=olay, ne_yapilir=ne, saat_tsi=saat, kaynak=kaynak))

KAY_NYSE = "nyse.com/markets/hours-calendars (2026–2027 tatil ve erken kapanış tablosu); sinyal_altin.nyse_tatilleri ile aynı"
KAY_TR = "Diyanet vakithesaplama 2027 dini günler (8 Mart arife, 9–11 Mart Ramazan B., 15 Mayıs arife Cmt, 16–19 Mayıs Kurban B.); sinyal_altin.TR_TATIL/TR_YARIM ile aynı"

# ---------------- E1-C2 tatil öncesi GDX
hol = sorted([(h, ad) for y in (2026, 2027) for h, ad in SA.nyse_tatilleri(y).items() if BAS <= h <= D(2027, 7, 31)])
for h, ad in hol:
    son = SA.onceki(h, SA.nyse_is_gunu)          # tatil öncesi son işlem günü (çıkış)
    gir = SA.onceki(son, SA.nyse_is_gunu)        # bir önceki işlem günü (giriş)
    if gir > BIT: continue
    add(h, "NYSE", f"NYSE tatili: {ad}", "ABD ETF işlemi yok. Ertesi VİOP gününde A4-C1 için yeni ABD kapanışı yoksa yeni dilim 0.", "", KAY_NYSE)
    add(gir, "ETF", f"E1-C2 GİRİŞ ({ad} {h:%d.%m} öncesi)", f"GDX'i bugün kapanışa yakın al: {etf_emir(gir)}. Çıkış {g(son)} kapanışında.", tsi_et(gir, 15, 50), KAY_NYSE)
    yarim = SA.nyse_yarim(son)
    add(son, "ETF", f"E1-C2 ÇIKIŞ ({ad} öncesi son gün" + (", ABD yarım günü" if yarim else "") + ")",
        f"Dün alınan GDX'i bugün sat: {etf_emir(son)}." + (" Yarım gün: E3-1 yeni pozisyon açmaz; dünkü E3-1 GDXJ'si de bu pencerede satılır." if yarim else ""),
        tsi_et(son, 12, 50) if yarim else tsi_et(son, 15, 50), KAY_NYSE)
# yarım günler (E1-C2 çıkışı olmayanlar dahil)
for d in pd.date_range(BAS, BIT).date:
    if SA.nyse_is_gunu(d) and SA.nyse_yarim(d):
        add(d, "NYSE", "NYSE yarım günü (13:00 ET kapanış)",
            f"Kapanış 13:00 ET ({tsi_et(d, 13, 0)} TSİ), karar 12:00 ET ({tsi_et(d, 12, 0)} TSİ). E3-1 devre dışı: yeni GDXJ yok; önceki seansın ({g(SA.onceki(d, SA.nyse_is_gunu))}) E3-1 GDXJ pozisyonu varsa {etf_emir(d)} penceresinde satılır. E2 kademeli dilimler ve bütün emirler 12:50–12:58 ET'de.",
            tsi_et(d, 12, 50), KAY_NYSE)

# ---------------- QEND
for (y, m) in ((2026, 12), (2027, 3), (2027, 6)):
    ay = SA.viop_gunleri(D(y, m, 1), (D(y, m + 1, 1) if m < 12 else D(y + 1, 1, 1)) - dt.timedelta(days=1))
    gir = ay[-2]; cik = SA.sonraki(gir, SA.tr_is_gunu, 3)
    kontrat = {12: "F_XAUUSD0227 (Aralık vadesi 31.12'de biter)", 3: "F_XAUUSD0427", 6: "F_XAUUSD0827 (Haziran vadesi 30.06'da biter)"}[m]
    add(gir, "VİOP", f"QEND GİRİŞ ({m}. ay sondan 2. VİOP günü)", f"Uzlaşma penceresinde (18:00–18:10 TSİ) 1 birim UZUN, kontrat {kontrat}. Çıkış {g(cik)} uzlaşması.", "18:00–18:10", "sinyal_altin.viop_gunleri + TR takvimi")
    add(cik, "VİOP", "QEND ÇIKIŞ (girişten 3 VİOP günü sonra)", "QEND uzun pozisyonunu uzlaşma penceresinde (18:00–18:10 TSİ) kapat.", "18:00–18:10", "sinyal_altin.sonraki(tr_is_gunu, 3)")

# ---------------- VİOP vadeleri ve roll
ROLL = {"F_XAUUSD1226": ("24.12–29.12.2026", "Vade sonu fiyatı LBMA PM'dir ama 31.12.2026'da PM ihalesi YOK (ICE takvimi) → sabah (AM, 10:30 Londra = 13:30 TSİ) fiyatı kullanılır; uzlaşma anından 4,5 saat önceki fiyat (31.12.2025'te de PM yoktu: F_XAUUSD1225 son uzlaşması 4.308,0, 11:00 UTC spot 4.306,3, 15:00 UTC spot 4.345,5 → AM'ye uydu). Açık pozisyonu en geç 29.12 uzlaşmasında 0227'ye taşı. 24.12'den itibaren yeni dilimleri (A8-3 5 gün, A4 3 gün) doğrudan 0227'de aç; 30.12 QEND girişi 0227'de. 2023–2025 Aralık roll'larında açık pozisyon 24–30.12'de geçti."),
        "F_XAUUSD0227": ("22.02–24.02.2027", "Son işlem günü 26.02.2027 Cum; vade sonu fiyatı LBMA PM = 15:00 Londra (GMT) = 18:00 TSİ. 19.02'den itibaren yeni A8-3 dilimlerini, 22.02'den itibaren bütün yeni dilimleri 0427'de aç; açık pozisyonu 22–24.02'de taşı."),
        "F_XAUUSD0427": ("26.04–28.04.2027", "Son işlem günü 30.04.2027 Cum (23.04 Cuma tatil); vade sonu fiyatı LBMA PM = 15:00 Londra (BST, 28.03'ten beri) = 17:00 TSİ, uzlaşma penceresinden 1 saat önce. 22.04'ten itibaren yeni A8-3 dilimlerini, 26.04'ten itibaren bütün yeni dilimleri 0627'de aç; açık pozisyonu 26–28.04'te taşı."),
        "F_XAUUSD0627": ("23.06–25.06.2027", "Son işlem günü 30.06.2027 Çar; vade sonu fiyatı LBMA PM = 15:00 Londra (BST) = 17:00 TSİ. 23.06'dan itibaren yeni dilimleri 0827'de aç; açık pozisyonu 23–25.06'da taşı; 29.06 QEND girişi 0827'de (Haziran vadesi tutuş bitmeden kapanır).")}
for code, (pencere, ne) in ROLL.items():
    vs = SA.viop_vade_son_gunu(code)
    add(vs, "VİOP", f"{code} vade sonu (son işlem günü)", ne, "", "borsaistanbul.com kıymetli maden sözleşmeleri: son işlem günü vade ayının son iş günü; vade sonu fiyatı LBMA Gold Price PM")
    a, b = pencere.split("–")
    da = dt.datetime.strptime(a + "." + b.split(".")[-1], "%d.%m.%Y").date()
    add(da, "VİOP", f"{code} → sonraki vade ROLL penceresi başlıyor ({pencere})", f"Açık pozisyonları {pencere} arasında uzlaşma penceresinde (18:00–18:10 TSİ) sonraki vadeye taşı (eski vadeyi kapat, yenisini aç; iki bacak aynı pencerede).", "18:00–18:10", "panel v_code değişimleri 2022–2026 (açık pozisyon vadeye 1–4 VİOP günü kala geçti)")

# ---------------- TR tatilleri ve yarım günler
for d in sorted(SA.TR_TATIL):
    if BAS <= d <= BIT:
        add(d, "VİOP", "Türkiye resmi tatili — VİOP kapalı", "VİOP işlem yok; kademeli dilim sayımı VİOP günleriyle ilerler (tatil sayılmaz). Midas/ABD ETF normal. Hükümetin ek idari izin günleri VİOP'u kapatmaz (ör. 08.04.2024 tam gün açıktı); BIST yıllık tatil duyurusunu kontrol et.", "", KAY_TR)
for d in sorted(SA.TR_YARIM):
    if BAS <= d <= BIT:
        add(d, "VİOP", "TR yarım günü (Ramazan Bayramı arifesi): VİOP öğleden sonra kapalı, akşam seansı yok",
            "Uzlaşma penceresi 12:30–12:40 TSİ. LOWMOM ve A8-3 yeni dilim açmaz (DEVRE DIŞI); A4-C1 ve QEND normal, emirler 12:30–12:40'ta. Açık dilimler sürer.", "12:30–12:40", KAY_TR)
add(D(2026, 12, 31), "VİOP", "31 Aralık: normal seans, akşam seansı yok (1 Ocak tatil)", "Emirler normal uzlaşma penceresinde (18:00–18:10 TSİ). F_XAUUSD1226'nın son işlem günü.", "18:00–18:10", "KULLANIM.md §5")

# ---------------- Spotun kapalı olduğu VİOP günleri (A8-3 nötr)
for d in pd.date_range(BAS, BIT).date:
    if SA.tr_is_gunu(d) and SA.spot_kapali(d):
        add(d, "VİOP", "Spot altın kapalı (VİOP açık)", "A8-3 yeni dilimi 0 (NÖTR); LOWMOM bir önceki spot gününün değerini kullanır. Açık dilimler sürer.", "", "sinyal_altin.spot_kapali")

# ---------------- A4-C1: yeni ABD kapanışı olmayan VİOP günleri / çok günlü getiri
vg = SA.viop_gunleri(D(2026, 11, 2), BIT)
def son_abd(d):  # gün d 15:00 UTC'den önce kapanmış son ABD seansı (yarım günde 09:30 UTC)
    x = d
    while True:
        x -= dt.timedelta(days=1)
        if SA.nyse_is_gunu(x): return x
for i in range(1, len(vg)):
    d, p = vg[i], vg[i - 1]
    if d < BAS: continue
    a, b = son_abd(d), son_abd(p)
    if a == b:
        add(d, "VİOP", "A4-C1: yeni ABD kapanışı yok", f"GDXJ/GLD getirisi 0 → e=0 → yeni dilim 0 (son ABD kapanışı {g(a)} önceki VİOP gününde de kullanıldı).", "", "sinyal_altin A4 tanımı (VİOP satırlarında fark)")
    else:
        n = len([x for x in SA.nyse_gunleri(b + dt.timedelta(days=1), a)])
        if n > 1:
            add(d, "VİOP", f"A4-C1: getiri {n} ABD seansını kapsar", f"GDXJ ve GLD değişimini {g(b)} kapanışından {g(a)} kapanışına al (tek günlük değil).", "", "sinyal_altin A4 tanımı")

# ---------------- ABD makro olayları (birincil kaynak: federalreserve.gov, bls.gov)
FOMC = [D(2026, 12, 9), D(2027, 1, 27), D(2027, 3, 17), D(2027, 4, 28), D(2027, 6, 9)]
CPI = [D(2026, 11, 10), D(2026, 12, 10), D(2027, 1, 13), D(2027, 2, 11), D(2027, 3, 10), D(2027, 4, 13), D(2027, 5, 12), D(2027, 6, 10)]
NFP = [D(2026, 12, 4), D(2027, 1, 8), D(2027, 2, 5), D(2027, 3, 5), D(2027, 4, 2), D(2027, 5, 7), D(2027, 6, 4), D(2027, 7, 2)]
for d in FOMC:
    t = tsi_et(d, 14); tb = tsi_et(d, 14, 30)
    add(d, "ABD/risk", "FOMC faiz kararı" + (" (SEP)" if d.month in (12, 3, 6) else ""),
        f"Karar 14:00 ET = {t} TSİ, basın toplantısı {tb} TSİ. VİOP uzlaşmasından SONRA (akşam seansında oynaklık). ETF karar anından (15:00 ET = {tsi_et(d, 15)} TSİ) ÖNCE: E3-1 m değeri FOMC tepkisini içerir; emir penceresinde spread geniş olabilir, pozisyon boyutunu küçültmeyi düşün.",
        t, "federalreserve.gov/monetarypolicy/fomccalendars.htm" + (" (2027 tarihleri 'tentative')" if d.year == 2027 else ""))
for d in CPI:
    t = tsi_et(d, 8, 30)
    add(d, "ABD/risk", "ABD TÜFE (CPI)", f"08:30 ET = {t} TSİ. VİOP karar anından (18:00 TSİ) ve A8-3 son saat penceresinden (17:00–18:00 TSİ) ÖNCE; ETF kararından önce. Gün içi sert hareket olabilir.", t, "bls.gov/schedule/news_release/cpi.htm")
for d in NFP:
    t = tsi_et(d, 8, 30)
    add(d, "ABD/risk", "ABD tarım dışı istihdam (NFP)", f"08:30 ET = {t} TSİ. VİOP karar anından ve son saat penceresinden ÖNCE; ETF kararından önce. Gün içi sert hareket olabilir.", t, "bls.gov/schedule/news_release/empsit.htm")
add(D(2027, 3, 14), "ABD/saat", "ABD yaz saatine geçiş (Türkiye UTC+3 sabit)",
    "15 Mart'tan itibaren ETF saatleri 1 saat ERKEN: karar 15:00 ET = 22:00 TSİ, emir 22:50–22:58 TSİ, kapanış 23:00 TSİ; E3-1 için önceki gün 16:00 ET = 23:00 TSİ. ABD veri saatleri 15:30 TSİ, FOMC 21:00 TSİ. VİOP saatleri değişmez.", "", "ABD DST: Mart'ın 2. Pazarı")

# ---------------- LBMA ihaleleri (ICE Benchmark Administration takvimi)
LBMA = [(D(2026, 12, 24), "yalnız AM ihalesi (PM yok)"), (D(2026, 12, 25), "ihale yok"), (D(2026, 12, 28), "ihale yok (Boxing Day)"),
        (D(2026, 12, 31), "yalnız AM ihalesi (PM yok) — F_XAUUSD1226 vade sonu fiyatı AM olur"), (D(2027, 1, 1), "ihale yok"), (D(2027, 3, 26), "ihale yok (Kutsal Cuma)"),
        (D(2027, 3, 29), "ihale yok (Paskalya Pazartesi)"), (D(2027, 5, 3), "ihale yok"), (D(2027, 5, 31), "ihale yok")]
for d, s in LBMA:
    add(d, "LBMA", f"LBMA Gold Price: {s}", "Londra likiditesi düşük; VİOP açıksa uzlaşma fiyatı yine 18:00–18:10 VWAP'tır (vade sonu dışında etkisi yok).", "", "ice.com/publicdocs/Gold_Holiday_Calendar_2026.pdf ve _2027.pdf")

# ---------------- Temettü (TradingView varsayılanı temettüsüz kapanış) — TAHMİNİ
EXD = [(D(2026, 12, 18), "SPY", "≈%0,25–0,3"), (D(2026, 12, 21), "GDX ve GDXJ", "GDX ≈%0,7–1,7, GDXJ ≈%0,5–2,6 (2024–25: %2,3–2,6)"),
       (D(2027, 3, 19), "SPY", "≈%0,25–0,3"), (D(2027, 6, 17), "SPY", "≈%0,25–0,3 (18 Haziran Juneteenth tatili)")]
for d, t, b in EXD:
    add(d, "ETF", f"TAHMİNİ temettü (ex-date) {t}: {b}",
        f"Bu günün yüzde değişimini TradingView'da temettü düzeltmeli oku (ADJ açık) ya da temettü yüzdesini değişime ekle; aksi halde ertesi günün E2/A4 artığı yanlış çıkar. Tarihi ihraççı sitesinden (vaneck.com, ssga.com) kontrol et.",
        "", "Yahoo adjclose/close oranı: GDX/GDXJ ex-date 19.12.2022, 18.12.2023, 23.12.2024, 22.12.2025 (Pzt); SPY Mart/Haz/Eyl/Ara 3. Cuma")

T = pd.DataFrame(rows).drop_duplicates(subset=["tarih", "cephe", "olay"]).sort_values(["tarih", "cephe", "olay"]).reset_index(drop=True)
T.to_csv(f"{S_}/out/rehber/takvim.csv", index=False, encoding="utf-8")
print(T.to_string(max_colwidth=70))
print(len(T))
