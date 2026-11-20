#!/usr/bin/env python3
"""Ajan ciktilarini okura gidecek ek dosyalara derler.
  ek/01_iktidar_48_yasa.md, ek/02..10_*.md (125 kitap), ek/11_envanter.md, ek/parcalar/rapor_liste.md
Kullanim: python3 derle.py"""
import glob, json, os, re

K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARIH = "20.11.2026"

YASALAR = """Ustanı asla gölgede bırakma|Dostlarına fazla güvenme, düşmanlarını kullanmayı öğren|Niyetlerini gizle|Her zaman gerekenden az konuş|Çok şey itibara bağlıdır: onu canın gibi koru|Ne pahasına olursa olsun dikkat çek|İşi başkalarına yaptır, ama övgüyü hep sen al|Başkalarını ayağına getir; gerekirse yem kullan|Tartışarak değil, eylemlerinle kazan|Bulaşma: mutsuzlardan ve şanssızlardan uzak dur|İnsanları kendine bağımlı kılmayı öğren|Kurbanını seçici dürüstlük ve cömertlikle silahsızlandır|Yardım isterken insanların çıkarına seslen; merhametine ya da minnetine asla|Dost gibi görün, casus gibi çalış|Düşmanını tümüyle ez|Saygınlığını artırmak için yokluğunu kullan|Başkalarını tedirgin tut: ne yapacağın kestirilemesin|Kendini korumak için kale kurma: yalnızlık tehlikelidir|Kiminle uğraştığını bil: yanlış kişiyi gücendirme|Kimseye bağlanma|Enayiyi avlamak için enayi rolü yap: hedefinden daha aptal görün|Teslimiyet taktiğini kullan: zayıflığı güce çevir|Güçlerini yoğunlaştır|Kusursuz saray adamını oyna|Kendini yeniden yarat|Ellerini temiz tut|İnsanların inanma ihtiyacını kullan, tarikat benzeri bir mürit kitlesi yarat|İşe cesaretle gir|Sonuna kadar planla|Başarılarını zahmetsizmiş gibi göster|Seçenekleri sen belirle: başkalarını senin dağıttığın kartlarla oynat|İnsanların hayallerine oyna|Herkesin zayıf noktasını bul|Kendi tarzında soylu ol: kral gibi davran ki kral gibi davranılsın|Zamanlama sanatında ustalaş|Sahip olamadığın şeyi küçümse: görmezden gelmek en iyi intikamdır|Etkileyici gösteriler yarat|İstediğin gibi düşün, herkes gibi davran|Balık tutmak için suyu bulandır|Bedava yemeği küçümse|Büyük bir adamın yerine geçmekten kaçın|Çobanı vur, sürü dağılsın|Başkalarının kalbine ve aklına hitap et|Ayna etkisiyle silahsızlandır ve çileden çıkar|Değişimin gerekliliğini vaaz et, ama bir anda fazla reform yapma|Asla fazla mükemmel görünme|Hedeflediğin noktayı aşma; zaferde durmayı bil|Biçimsiz ol""".split("|")
assert len(YASALAR) == 48

BOLUMLER = [
 ("02_greene_ve_cevresi", "Greene'in diğer kitapları ve doğrudan kaynakları", "A01 A02 A03 A04 B01 B02 B03 B04 B05 B06"),
 ("03_bati_klasikleri", "Batı klasikleri: Antik Çağ, Machiavelli ve devlet aklı", "B19 B20 B21 B22 B23 B24 A05 A06 A07 A08 B07 B08 B09 B10 B11 B12"),
 ("04_saray_ve_entrika", "Saray, salon ve entrika kitapları", "A09 A10 A11 A12 B13 B14 B15 B16 B17 B18"),
 ("05_cin_klasikleri_ve_strateji", "Çin klasikleri ve strateji", "A13 A14 A15 A16 B31 B32 B33 B34 B35 B36"),
 ("06_hint_islam_turk_siyasetnameleri", "Hint, İslam ve Türk siyasetnameleri", "A17 A18 B37 A19 A20 B38 B39 B40 B41 B42 B43 A33 B44 B45 B46 B47 B48"),
 ("07_is_dunyasinda_guc", "İş dünyasında güç", "A21 A22 B50 A23 A24 B49 B51 B52 B53 B54"),
 ("08_siyasette_guc", "Siyasette güç: taktik, darbe, direniş", "A25 A26 A27 A28 B55 B56 B57 B58 B59 B60 B61 B62 B63 B64 B65"),
 ("09_etkileme_manipulasyon_propaganda", "Etkileme, manipülasyon ve propaganda", "A29 B72 A30 A31 A32 B73 B74 B75 B76 B77 B78 B79 B80 B81 B82 B83"),
 ("10_iktidar_kurami_ve_bilimi", "İktidar kuramı ve iktidarın bilimi", "A34 A35 A36 B25 B26 B27 B28 B29 B30 B84 B85 B86 B87 B88 B89 B66 B67 B68 B69 B70 B71"),
]

def oku(p):
    return open(p, encoding="utf-8").read().strip()

def kelime(s):
    return len(s.split())

# ---------- 01: 48 yasa ----------
cerceve = oku(K + "/parcalar/iktidar_cerceve.md")
cerceve = re.sub(r"(?m)^# .*\n", "", cerceve)            # varsa ust baslik
cerceve = re.sub(r"(?m)^## ", "### ", cerceve)
yasalar = []
for ad in ["yasa_1-12", "yasa_13-24", "yasa_25-36", "yasa_37-48"]:
    t = oku(K + f"/parcalar/{ad}.md")
    t = re.sub(r"(?m)^Not: Yasa adlarını biz çevirdik\.?\s*\n", "", t)
    yasalar.append(t.strip())
govde = "\n\n".join(yasalar)
def bas(m):
    n = int(m.group(1))
    return f"### Yasa {n} — {YASALAR[n-1]}"
govde, adet = re.subn(r"(?m)^### Yasa (\d+) — .*$", bas, govde)
assert adet == 48, adet
icindekiler = "\n".join(f"{i+1}. {a}" for i, a in enumerate(YASALAR))
y01 = f"""# İktidar: Güç Sahibi Olmanın 48 Yasası (The 48 Laws of Power, 1998)

Robert Greene'in kitabının ayrıntılı anlatımı. İki kısımdır: önce kitabın çerçevesi (yazar, doğuşu, yapısı, etkisi, eleştiriler), sonra 48 yasa tek tek. Her yasada beş başlık var: özü, kitaptaki örnekler, mantığı, tersi ve bir not.

Okurken bilinmesi gerekenler:
- Yasa adlarını biz çevirdik. Altın Kitaplar baskısındaki resmî Türkçe başlıklar bu oturumda bulunamadı; sizdeki baskıda adlar farklı olabilir.
- "Not" başlıkları bizim eklememizdir: Greene'in tarih anlatımının kaynaklarla çeliştiği yerleri ve yasanın eleştirisini içerir.
- "(doğrulanmadı)" işareti, o ayrıntının bu oturumda kaynaktan görülemediğini gösterir.

## 48 yasanın listesi

{icindekiler}

## Birinci kısım: Kitabın çerçevesi

{cerceve}

## İkinci kısım: 48 yasa, tek tek

{govde}
"""
open(K + "/01_iktidar_48_yasa.md", "w", encoding="utf-8").write(y01)

# ---------- 02-10: kitaplar ----------
kat = {}
kp = K + "/dogrulama/turkce_baski_katalog.json"
if os.path.exists(kp):
    kat = json.load(open(kp, encoding="utf-8"))
dosya = {os.path.basename(p)[:3]: p for p in glob.glob(K + "/kitaplar/*.md")}
assert len(dosya) == 125, len(dosya)

def katalog_satiri(anahtar):
    v = [x for x in (kat.get(anahtar) or []) if x.get("yayinevi")]
    v2 = [x for x in (kat.get(anahtar) or []) if not x.get("yayinevi")]
    if not v and not v2:
        return f"*Satıştaki Türkçe baskı (D&R ve Kitapseç katalogları, {TARIH}): bu iki katalogda görünmüyor.*", False
    gor, parca = set(), []
    for x in v + v2:
        y = x.get("yayinevi") or ""
        an = y or x["ad"]
        if an in gor: continue
        gor.add(an)
        parca.append(f"{x['ad']} ({y})" if y else x["ad"])
        if len(parca) >= 5: break
    return f"*Satıştaki Türkçe baskılar (D&R ve Kitapseç katalogları, {TARIH}): " + "; ".join(parca) + ".*", True

ozet = []   # rapor listesi icin
toplam = {}
for ad, baslik, kodlar in BOLUMLER:
    kodlar = kodlar.split()
    parcalar, icerik = [], []
    for k in kodlar:
        t = oku(dosya[k])
        satirlar = t.split("\n")
        assert satirlar[0].startswith("## "), dosya[k]
        h = satirlar[0][3:].strip()
        anahtar = os.path.basename(dosya[k])[:-3]
        ks, var = katalog_satiri(anahtar)
        m = re.search(r"\*\*Bir cümleyle\.?\*\*\.?\s*(.+)", t)
        bc = m.group(1).strip() if m else ""
        kisa = h.split(" (")[0]
        ozet.append((ad, baslik, k, kisa, bc, var))
        icerik.append(kisa)
        parcalar.append(satirlar[0] + "\n\n" + ks + "\n" + "\n".join(satirlar[1:]))
    ic = "\n".join(f"{i+1}. {x}" for i, x in enumerate(icerik))
    metin = f"# {baslik}\n\nBu dosyada {len(kodlar)} kitap var. Her kitap aynı sırayla anlatılır: künye, bir cümleyle, bağlam, yapısı, ana fikirler, İktidar'la ilişkisi, eleştiri, kimler okumalı. Başlığın hemen altındaki italik satır, kitapçı kataloglarının betikle taranmasından gelir; künye paragrafındaki bilgiyle çelişirse katalog satırı daha günceldir. \"(doğrulanmadı)\" işareti, o ayrıntının bu oturumda kaynaktan görülemediğini gösterir.\n\n## Bu dosyadaki kitaplar\n\n{ic}\n\n" + "\n\n---\n\n".join(parcalar) + "\n"
    open(K + f"/{ad}.md", "w", encoding="utf-8").write(metin)
    toplam[ad] = (len(kodlar), kelime(metin))

# ---------- rapor listesi ----------
L = []
son = None
for ad, baslik, k, kisa, bc, var in ozet:
    if ad != son:
        L.append(f"\n**{baslik}** (`ek/{ad}.md`)\n")
        son = ad
    isaret = ("★ " if k.startswith("A") else "") + ("" if var else "")
    tr = " *(TR)*" if var else ""
    L.append(f"- {isaret}**{kisa}**{tr}: {bc}")
open(K + "/parcalar/rapor_liste.md", "w", encoding="utf-8").write("\n".join(L).strip() + "\n")

# ---------- 11: envanter ----------
ham = json.load(open(K + "/parcalar/envanter_ham.json", encoding="utf-8"))
ekk = json.load(open(K + "/parcalar/envanter_ek.json", encoding="utf-8"))
ol = {}
if os.path.exists(K + "/parcalar/envanter_ol.json"):
    ol = json.load(open(K + "/parcalar/envanter_ol.json", encoding="utf-8"))
ETIKET = [("öğüt-kural", "Kural ve öğüt kitapları"), ("siyasetname", "Siyasetnameler ve hükümdara öğüt"), ("saray", "Saray ve saraylı"), ("özdeyiş", "Özdeyiş"),
          ("strateji", "Strateji"), ("etkileme", "Etkileme ve ikna"), ("manipülasyon", "Manipülasyon, dolandırıcılık, zihin denetimi"), ("propaganda", "Propaganda"),
          ("müzakere", "Müzakere"), ("kuram", "İktidar kuramı"), ("ampirik", "Ampirik araştırma"), ("biyografi", "Biyografi ve anı"), ("kurgu", "Kurgu")]
gor = set(); E = {e: [] for e, _ in ETIKET}
for b in ham + ekk:
    an = (b["yazar"][:18].lower(), re.sub(r"\(.*?\)", "", b["ozgun_ad"])[:20].lower())
    if an in gor: continue
    gor.add(an)
    tur = (b.get("tur") or "kuram").split("|")[0].strip()
    if tur not in E: tur = "kuram"
    d = ol.get(b["yazar"] + " | " + b["ozgun_ad"], {}).get("durum")
    yil = b["yil"] + (" ✓" if d == "uyuyor" else "")
    tr = f"; Türkçesi: {b['turkce_ad']}" if b.get("turkce_ad") else ""
    E[tur].append((-(b.get("yakinlik") or 2), b["yazar"], f"- **{b['yazar']} — {b['ozgun_ad']}** ({yil}{tr}): {b['gerekce'].strip()}"))
say = sum(len(v) for v in E.values())
m = [f"# Envanter: ayrıntılı anlatılmayan {say} kitap", "",
     "Keşif ajanlarının ve eleştirmenin bulduğu, ama ayrıntılı anlatılan 125 kitabın dışında kalan kitaplar. Her biri tek satırla tanıtılır.",
     "", "Okurken bilinmesi gerekenler:",
     "- Bu listedeki künyelerin çoğu ajanların belleğinden gelir ve tek tek doğrulanmadı. Yılın yanındaki ✓ işareti, yılın Open Library kaydıyla betikle karşılaştırılıp uyuştuğunu gösterir (yalnızca 1800 sonrası kitaplar denendi).",
     "- Türkçe adlar da bellekten; satın almadan önce kontrol edin.",
     "- Sıralama her başlık altında İktidar'a yakınlığa göredir.", ""]
for e, ad in ETIKET:
    if not E[e]: continue
    m.append(f"## {ad} ({len(E[e])})"); m.append("")
    m += [x[2] for x in sorted(E[e])]
    m.append("")
open(K + "/11_envanter.md", "w", encoding="utf-8").write("\n".join(m))

print("01:", kelime(y01), "kelime")
for ad, (n, w) in toplam.items(): print(ad, n, "kitap", w, "kelime")
print("envanter:", say, "kayit;", sum(1 for v in ol.values() if v.get("durum") == "uyuyor"), "yil OL ile uyusuyor")
print("TR katalogda bulunan:", sum(1 for x in ozet if x[5]), "/ 125")
