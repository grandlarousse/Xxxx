#!/usr/bin/env python3
"""Ajan ciktilarini okura gidecek dosyalara derler:
  ek/01_karanlik_psikoloji_rehberi.md, ek/02..11_*.md (124 kitap), ek/12_envanter.md, ek/parcalar/rapor_liste.md, RAPOR.md
Kullanim: python3 derle.py"""
import glob, json, os, re, unicodedata
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOK = os.path.dirname(K)
def oku(p): return open(p, encoding="utf-8").read().strip()
def kelime(s): return len(s.split())
def f(s):
    s = (s or "").replace("ı", "i").replace("İ", "I")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

# ---------- 01: rehber ----------
R = [oku(K + f"/parcalar/rehber_R{i}.md") for i in range(1, 5)]
basliklar = [r.split("\n")[0].lstrip("# ").strip() for r in R]
rehber = "# Karanlık psikoloji: alan rehberi\n\n" + \
 "Bu rehber, kitaplara geçmeden önce alanın kavramlarını, bilimini ve tuzaklarını anlatır. Dört bölümdür:\n\n" + \
 "\n".join(f"{i+1}. {b}" for i, b in enumerate(basliklar)) + "\n\n" + \
 "Okurken bilinmesi gerekenler:\n- Kanıt etiketleri: [araştırma] deneysel ya da sistematik araştırması olan; [klinik] klinisyen gözlemine ve vaka yazınına dayanan; [popüler] sosyal medya ve öz yardım dilinden gelen, araştırması zayıf ya da olmayan.\n- \"(doğrulanmadı)\" işareti, o ayrıntının bu oturumda kaynaktan görülemediğini gösterir.\n- \"(önceki raporda ayrıntılı)\" işaretli kitaplar `raporlar/2026-11-20_iktidar_kitaplari/` raporunda anlatıldı.\n- Bu rehber tanı koymak için değildir. Bir yakınınızda bu özellikleri görüyorsanız etiket koymak yerine davranışa bakın ve gerekirse bir uzmana danışın.\n\n" + \
 "\n\n---\n\n".join(R) + "\n"
open(K + "/01_karanlik_psikoloji_rehberi.md", "w", encoding="utf-8").write(rehber)

# ---------- 02-11: kitaplar ----------
BOLUM = [
 ("02_karanlik_kisiligin_bilimi", "Karanlık kişiliğin bilimi", "K001 K002 K003 K004 K041 K042 K043 K044 K045 K046"),
 ("03_kotulugun_psikolojisi", "Kötülüğün psikolojisi", "K005 K006 K007 K008 K077 K078 K079 K080 K081 K082"),
 ("04_psikopati_klasikler_ve_bilim", "Psikopati: klasikler ve bilim", "K009 K010 K011 K012 K013 K014 K015 K059 K060 K061 K062 K063 K064"),
 ("05_psikopati_anilar_ve_korunma", "Psikopati: anılar, iş yeri ve korunma", "K016 K065 K066 K067 K068 K069 K070 K071 K072 K073 K074 K075 K076"),
 ("06_narsisizm", "Narsisizm", "K017 K018 K019 K020 K021 K022 K023 K024 K047 K048 K049 K050 K051 K052 K053 K054"),
 ("07_istismar_ve_zorlayici_denetim", "Psikolojik istismar ve zorlayıcı denetim", "K025 K026 K027 K028 K083 K084 K085 K086 K087 K088 K089 K090 K091"),
 ("08_gaslighting_santaj_ve_korunma", "Gaslighting, şantaj, hazırlama ve korunma", "K029 K030 K031 K032 K055 K056 K057 K058 K092 K093 K094"),
 ("09_tarikat_beyin_yikama_sorgu", "Tarikat, beyin yıkama, sorgu ve dezenformasyon", "K033 K034 K035 K036 K095 K096 K097 K098 K099 K100 K101 K102 K103 K104 K105 K106"),
 ("10_aldatma_ve_dolandiricilik", "Aldatma, yalan ve dolandırıcılık", "K037 K038 K107 K108 K109 K110 K111 K112 K113 K114 K115"),
 ("11_populer_karanlik_psikoloji_ve_turkiye", "Popüler karanlık psikoloji, gizli ikna ve Türkiye", "K039 K040 K116 K117 K118 K119 K120 K121 K122 K123 K124"),
]
liste = {b["dosya"][:4]: b for b in json.load(open(K + "/parcalar/kitap_listesi.json"))}
dosya = {os.path.basename(p)[:4]: p for p in glob.glob(K + "/kitaplar/K*.md")}
kullanilan = [k for _, _, ks in BOLUM for k in ks.split()]
assert len(kullanilan) == len(set(kullanilan)) == 124, (len(kullanilan), len(set(kullanilan)))
eksik = [k for k in kullanilan if k not in dosya]
def tr_var(t):
    """True: Türkçe baskı künyede ad ve kaynakla var; None: var olduğu söyleniyor ama doğrulanmadı; False: görünmüyor."""
    m = re.search(r"\*\*Künye\.?\*\*(.*?)\n\*\*", t, re.S)
    cumle = [f(c) for c in re.split(r"(?<=[.;])\s+", m.group(1) if m else "") if "turk" in f(c)]
    ku = " ".join(cumle)
    if "buyuk olasilik" in ku: return None
    if re.search(r"turkce baski(si)?:|turkce yazilmis ozgun|turkce, ozgun|turkcede .*adiyla (cevrilmistir|cikti)|turkce baskisi var", ku): return True
    if re.search(r"cevirisi olabilecek|cevrildigi biliniyor|adiyla cevrilmis|turkcesi .*bellekten|buyuk olasilikla .*cevirisidir", ku): return None
    return False
ozet, toplam = [], {}
for ad, baslik, kodlar in BOLUM:
    kodlar = kodlar.split(); parcalar, ic = [], []
    for k in kodlar:
        if k not in dosya: continue
        t = oku(dosya[k]); s = t.split("\n"); assert s[0].startswith("## "), dosya[k]
        h = s[0][3:].strip(); kisa = h
        if h.endswith(")"):
            d = 0
            for i in range(len(h) - 1, -1, -1):
                d += {")": 1, "(": -1}.get(h[i], 0)
                if d == 0: kisa = h[:i].strip(); break
        m = re.search(r"\*\*Bir cümleyle\.?\*\*\.?\s*(.+)", t); bc = m.group(1).strip() if m else ""
        m2 = re.search(r"\[(araştırma|klinik|popüler)\]", t[t.find("**Bilimsel dayanağı"):] if "**Bilimsel dayanağı" in t else t)
        etiket = m2.group(1) if m2 else ""
        ozet.append((ad, baslik, k, kisa, bc, tr_var(t), liste[k]["katman"], etiket)); ic.append(kisa); parcalar.append(t)
    metin = f"# {baslik}\n\nBu dosyada {len(parcalar)} kitap var. Her kitap aynı sırayla anlatılır: künye, bir cümleyle, bağlam, yapısı, ana fikirler, bilimsel dayanağı, karanlık psikoloji haritasındaki yeri, eleştiri, kimler okumalı. \"(doğrulanmadı)\" işareti, o ayrıntının bu oturumda kaynaktan görülemediğini gösterir. Kanıt etiketleri ve kavramlar için `01_karanlik_psikoloji_rehberi.md` dosyasına bakın.\n\n## Bu dosyadaki kitaplar\n\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(ic)) + "\n\n" + "\n\n---\n\n".join(parcalar) + "\n"
    open(K + f"/{ad}.md", "w", encoding="utf-8").write(metin); toplam[ad] = (len(parcalar), kelime(metin))

L, son = [], None
for ad, baslik, k, kisa, bc, var, kat, et in ozet:
    if ad != son: L.append(f"\n**{baslik}** (`ek/{ad}.md`)\n"); son = ad
    trs = " *(TR)*" if var is True else (" *(TR?)*" if var is None else "")
    L.append(f"- {'★ ' if kat == 'A' else ''}**{kisa}**{trs}{f' [{et}]' if et else ''}: {bc}")
open(K + "/parcalar/rapor_liste.md", "w", encoding="utf-8").write("\n".join(L).strip() + "\n")

# ---------- 12: envanter ----------
ONCEKI = ["cialdini", "carnegie", "schopenhauer", "bernays", "joule", "simon|in sheep", "hadnagy", "maurer", "konnikova", "le bon", "hoffer", "ellul", "herman.*chomsky|manufacturing consent", "lifton.*thought reform|thought reform", "milgram", "christie", "babiak", "keltner", "klaas", "greene", "francesco", "holiday", "haley", "machiavelli", "mazarin", "arendt.*on violence", "canetti"]
secili = [(f(b["soyad"]), f(b["ozgun_ad"])[:18]) for b in liste.values()]
def secildi(b):
    y, a = f(b["yazar"]), f(b["ozgun_ad"])
    return any(s in y and (t[:10] in a or a[:10] in t) for s, t in secili)
def onceki(b):
    y, a = f(b["yazar"]), f(b["ozgun_ad"])
    return any(re.search(p, y + " | " + a) for p in ONCEKI) and not re.search(r"lifton.*(nazi|losing)|arendt.*(eichmann|origins)", y + " | " + a)
kesif = []
for p in sorted(glob.glob(K + "/parcalar/kesif_D*.json")):
    for b in json.load(open(p))["kitaplar"]:
        b = dict(b); b["dilim"] = os.path.basename(p)[6:8]; kesif.append(b)
ekk = json.load(open(K + "/parcalar/envanter_ek.json")) if os.path.exists(K + "/parcalar/envanter_ek.json") else []
ETIKET = [("kişilik-bilimi", "Karanlık kişiliğin bilimi"), ("psikopati", "Psikopati"), ("narsisizm", "Narsisizm"), ("istismar", "İstismar, gaslighting, zorlayıcı denetim"),
          ("korunma-iyileşme", "Korunma ve iyileşme"), ("zihin-denetimi", "Tarikat, beyin yıkama, sorgu"), ("dolandırıcılık", "Aldatma ve dolandırıcılık"),
          ("kötülük", "Kötülük ve zulüm"), ("popüler-karanlık", "Popüler karanlık psikoloji ve gizli ikna"), ("baştan-çıkarma", "Baştan çıkarma ve pickup"), ("anı", "Anılar"), ("kurgu", "Kurgu")]
E = {e: [] for e, _ in ETIKET}; gor = set(); onc = []
for b in kesif + ekk:
    an = (f(b["yazar"])[:14], re.sub(r"[^a-z]", "", f(b["ozgun_ad"]))[:16])
    if an in gor: continue
    gor.add(an)
    if secildi(b): continue
    if onceki(b): onc.append(b); continue
    tur = (b.get("tur") or "kişilik-bilimi").split("|")[0].strip()
    if tur not in E: tur = "kişilik-bilimi"
    tr = f"; Türkçesi: {b['turkce_ad']}" if b.get("turkce_ad") else ""
    E[tur].append((-(b.get("yakinlik") or 2), b["yazar"], f"- **{b['yazar']} — {b['ozgun_ad']}** ({b['yil']}{tr}): {b['gerekce'].strip()}"))
say = sum(len(v) for v in E.values())
m = [f"# Envanter: ayrıntılı anlatılmayan {say} kitap", "", "Keşif ajanlarının ve eleştirmenin bulduğu, ama ayrıntılı anlatılan 124 kitabın dışında kalan kitaplar; her biri tek satırla.", "",
     "Okurken bilinmesi gerekenler:", "- Künyelerin çoğu ajanların belleğinden ya da tek bir katalog kaydından gelir ve tek tek doğrulanmadı; Türkçe adlar da öyle. Satın almadan önce kontrol edin.",
     "- Sıralama her başlık altında alana yakınlığa göredir.", ""]
for e, ad in ETIKET:
    if not E[e]: continue
    m.append(f"## {ad} ({len(E[e])})"); m.append(""); m += [x[2] for x in sorted(E[e])]; m.append("")
m.append(f"## Önceki raporda ayrıntılı anlatılan ilgili kitaplar"); m.append("")
m.append("Bu kitaplar `raporlar/2026-11-20_iktidar_kitaplari/ek/` dosyalarında ayrıntılı anlatıldı: Cialdini (Influence; Pre-Suasion), Carnegie, Schopenhauer (Eristik Diyalektik), Bernays (Propaganda), Joule ve Beauvois, George K. Simon (In Sheep's Clothing), Hadnagy (Social Engineering), Maurer (The Big Con), Konnikova (The Confidence Game), Le Bon, Hoffer, Ellul, Herman ve Chomsky, Lifton (Thought Reform), Milgram, Christie ve Geis (Studies in Machiavellianism), Babiak ve Hare (Snakes in Suits), Keltner, Klaas, Greene (48 Laws of Power; The Art of Seduction; The Laws of Human Nature), de Francesco, Holiday, Haley, Machiavelli, Mazarin'e atfedilen Breviarium, Arendt (On Violence), Canetti.")
open(K + "/12_envanter.md", "w", encoding="utf-8").write("\n".join(m) + "\n")

# ---------- RAPOR.md ----------
ust_p, alt_p = K + "/parcalar/rapor_ust.md", K + "/parcalar/rapor_alt.md"
if os.path.exists(ust_p) and os.path.exists(alt_p):
    from collections import Counter
    alan = Counter()
    for p_ in glob.glob(K + "/defter/*.md"):
        for u in re.findall(r"https?://([^/ |)>]+)", open(p_, encoding="utf-8").read()): alan[u.lower().replace("www.", "")] += 1
    satir = [f"- `{a}`: {n} defter satırı" for a, n in alan.most_common(18)]
    deg = {"__KAYNAK_ALANLARI__": "\n".join(satir), "__TR_SAYI__": str(sum(1 for x in ozet if x[5] is True)), "__TRQ_SAYI__": str(sum(1 for x in ozet if x[5] is None)), "__ENV_SAYI__": str(say),
           "__ETIKET__": ", ".join(f"{sum(1 for x in ozet if x[7] == e)} [{e}]" for e in ["araştırma", "klinik", "popüler"]), "__DEFTER_SAYI__": str(len(glob.glob(K + "/defter/*.md"))),
           "__TAKTIK__": ", ".join(f"{n} [{e}]" for e, n in [(e, len(re.findall(r"(?m)^### \d+\..*\[" + e + r"\]", oku(K + "/parcalar/rehber_R3.md")))) for e in ["araştırma", "klinik", "popüler"]]),
           "__TRQ_SAYI__": str(sum(1 for x in ozet if x[5] is None))}
    alt = oku(alt_p); ust = oku(ust_p)
    for a_, b_ in deg.items(): alt = alt.replace(a_, b_); ust = ust.replace(a_, b_)
    rapor = ust + "\n\n" + oku(K + "/parcalar/rapor_liste.md") + "\n\n" + alt + "\n"
    open(KOK + "/RAPOR.md", "w", encoding="utf-8").write(rapor)
    print("RAPOR.md:", kelime(rapor), "kelime; govde yaklasik", kelime(ust) + kelime(alt))
print("01 rehber:", kelime(rehber), "kelime")
for ad, (n, w) in toplam.items(): print(ad, n, "kitap", w, "kelime")
print("envanter:", say, "kayit; onceki raporda:", len(onc), "; TR:", sum(1 for x in ozet if x[5] is True), "TR?:", sum(1 for x in ozet if x[5] is None), "/", len(ozet), "; eksik dosya:", eksik)
print("etiket:", {e: sum(1 for x in ozet if x[7] == e) for e in ["araştırma", "klinik", "popüler", ""]})
