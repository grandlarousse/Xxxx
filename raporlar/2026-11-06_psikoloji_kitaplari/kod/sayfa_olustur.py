"""Kitap özetlerini (kitaplar/*.md) ve okuma haritasını (00_okuma_haritasi.md)
tek bir HTML okuma sayfasına çevirir: ../yaranma_ve_ret_kitapligi.html

Kullanım: python3 kod/sayfa_olustur.py   (klasörün kökünden)
Gerekli: pip install markdown
"""
import html
import json
import pathlib
import re

import markdown

KOK = pathlib.Path(__file__).resolve().parent.parent
KITAPLAR = sorted((KOK / "kitaplar").glob("[0-9][0-9]_*.md"))
HARITA = KOK / "00_okuma_haritasi.md"
CIKTI = KOK / "yaranma_ve_ret_kitapligi.html"

MD_EXT = ["tables", "sane_lists", "attr_list"]


def md2html(text: str) -> str:
    out = markdown.markdown(text, extensions=MD_EXT, output_format="html")
    # tabloları yatay kaydırılabilir kaba al
    out = out.replace("<table>", '<div class="tablo"><table>').replace("</table>", "</table></div>")
    # dış bağlantılar yeni sekmede
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)
    return out


def kelime(text: str) -> int:
    return len(re.findall(r"\w+", text))


def kitap_oku(p: pathlib.Path):
    raw = p.read_text(encoding="utf-8")
    lines = raw.splitlines()
    baslik = next((l[2:].strip() for l in lines if l.startswith("# ")), p.stem)
    govde = "\n".join(l for l in lines if not l.startswith("# ") or l[2:].strip() != baslik)
    # künye: başlıktan sonraki ilk dolu satır(lar), ilk ## başlığına kadar
    kunye = []
    after = False
    for l in lines:
        if l.startswith("# "):
            after = True
            continue
        if after:
            if l.startswith("## "):
                break
            if l.strip():
                kunye.append(l.strip().lstrip("-* ").strip())
    # H2 başlıkları -> içindekiler
    h2 = [l[3:].strip() for l in lines if l.startswith("## ")]
    # hakem hükmü
    hakem = ""
    m = re.search(r"## Hakem notu\s*\n(.+?)(\n## |\Z)", raw, re.S)
    if m:
        hakem = m.group(1).strip()
    # "Tek paragrafta" bölümünün ilk paragrafı -> kart özeti
    tez = ""
    m = re.search(r"## Tek paragrafta[^\n]*\n+(.+?)(\n\n|\n## )", raw, re.S)
    if m:
        tez = re.sub(r"[*_`]", "", m.group(1).strip())
        if len(tez) > 330:
            tez = tez[:330].rsplit(" ", 1)[0] + "…"
    no = p.name[:2]
    return {
        "no": no,
        "id": f"kitap-{no}",
        "baslik": baslik,
        "kunye": " ".join(kunye)[:400],
        "tez": tez,
        "kelime": kelime(raw),
        "dakika": round(kelime(raw) / 200),
        "h2": h2,
        "html": md2html(govde),
        "hakem": bool(hakem),
    }


def slugify(s: str) -> str:
    s = s.lower()
    for a, b in zip("çğıöşüâî", "cgiosuai"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def h2_idleri(html_text: str, kid: str) -> str:
    def rep(m):
        t = re.sub("<[^>]+>", "", m.group(1))
        return f'<h2 id="{kid}--{slugify(t)}">{m.group(1)}</h2>'
    return re.sub(r"<h2>(.+?)</h2>", rep, html_text)


kitaplar = [kitap_oku(p) for p in KITAPLAR]
for k in kitaplar:
    k["html"] = h2_idleri(k["html"], k["id"])

harita_html = md2html(HARITA.read_text(encoding="utf-8")) if HARITA.exists() else ""
toplam = sum(k["kelime"] for k in kitaplar)

kartlar = []
for k in kitaplar:
    kartlar.append(f"""
      <li class="kart">
        <a href="#{k['id']}" class="kart-link">
          <span class="kart-no">{k['no']}</span>
          <span class="kart-govde">
            <span class="kart-baslik">{html.escape(k['baslik'])}</span>
            <span class="kart-tez">{html.escape(k['tez'])}</span>
            <span class="kart-meta">{f"{k['kelime']:,}".replace(",", ".")} kelime · yaklaşık {k['dakika']} dk okuma</span>
          </span>
        </a>
      </li>""")

makaleler = []
for i, k in enumerate(kitaplar):
    onceki = kitaplar[i - 1] if i > 0 else None
    sonraki = kitaplar[i + 1] if i < len(kitaplar) - 1 else None
    icindekiler = "".join(
        f'<li><a href="#{k["id"]}" data-hedef="{k["id"]}--{slugify(t)}">{html.escape(t)}</a></li>' for t in k["h2"]
    )
    nav = '<nav class="kitap-nav" aria-label="Kitaplar arası geçiş">'
    nav += f'<a href="#{onceki["id"]}">← {onceki["no"]}</a>' if onceki else '<span></span>'
    nav += '<a href="#">Kitaplık</a>'
    nav += f'<a href="#{sonraki["id"]}">{sonraki["no"]} →</a>' if sonraki else '<span></span>'
    nav += "</nav>"
    makaleler.append(f"""
    <article id="{k['id']}" class="kitap" hidden>
      <header class="kitap-bas">
        <p class="ust-etiket">Kitap {k['no']} / {len(kitaplar):02d} · yaklaşık {k['dakika']} dk</p>
        <h1>{html.escape(k['baslik'])}</h1>
        <details class="icindekiler"><summary>Bu özetin bölümleri</summary><ol>{icindekiler}</ol></details>
      </header>
      <div class="metin">{k['html']}</div>
      {nav}
    </article>""")

SAYFA = """<title>Yaranma ve Ret Kitaplığı</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:wght@500;700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=IBM+Plex+Sans+Condensed:wght@400;500&display=swap">
<style>
/* Düzen: tek sütun okuma odası; ana sayfa = harita + raf (kartlar), kitap = tek makale; hash ile geçiş */
:root {
  --zemin: #f3f5f4;
  --kagit: #fbfcfb;
  --murekkep: #1d2422;
  --soluk: #5b6662;
  --cizgi: #d5dcd9;
  --vurgu: #1f5d55;
  --vurgu-zemin: #e3eeeb;
  --font-baslik: "Alegreya", "Iowan Old Style", Georgia, serif;
  --font-metin: "Literata", "Iowan Old Style", Georgia, serif;
  --font-arac: "IBM Plex Sans Condensed", "Arial Narrow", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --zemin: #121615; --kagit: #171c1b; --murekkep: #dfe6e3; --soluk: #9aa7a2;
    --cizgi: #2c3533; --vurgu: #7cc2b6; --vurgu-zemin: #1d2b28; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --zemin: #121615; --kagit: #171c1b; --murekkep: #dfe6e3; --soluk: #9aa7a2;
  --cizgi: #2c3533; --vurgu: #7cc2b6; --vurgu-zemin: #1d2b28; color-scheme: dark;
}
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body {
  background: var(--zemin); color: var(--murekkep);
  font-family: var(--font-metin); font-size: 1.0625rem; line-height: 1.7;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 0 4rem;
}
.sayfa { max-width: 44rem; margin: 0 auto; }
a { color: var(--vurgu); text-underline-offset: 0.18em; }
a:focus-visible, summary:focus-visible { outline: 2px solid var(--vurgu); outline-offset: 3px; border-radius: 2px; }
.ust-cubuk {
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5;
  background: var(--zemin); border-bottom: 1px solid var(--cizgi);
  display: flex; gap: 1rem; align-items: baseline; justify-content: space-between;
  padding-block: 0.6rem; font-family: var(--font-arac); font-size: 0.9rem;
}
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--zemin); }
.ust-cubuk a { text-decoration: none; font-weight: 500; }
.ust-cubuk .yer { color: var(--soluk); min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
h1, h2, h3 { font-family: var(--font-baslik); line-height: 1.2; text-wrap: balance; }
.giris h1 { font-size: clamp(2rem, 6vw, 2.8rem); margin: 2.2rem 0 0.4rem; letter-spacing: -0.01em; }
.giris .alt { color: var(--soluk); font-family: var(--font-arac); font-size: 0.95rem; margin: 0; }
.harita { margin-top: 1.6rem; }
.harita h2 { font-size: 1.5rem; margin-top: 2rem; }
.raf-baslik { font-family: var(--font-arac); text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.8rem; color: var(--soluk); margin: 2.4rem 0 0.6rem; }
.raf { list-style: none; padding: 0; margin: 0; display: grid; gap: 0; border-top: 1px solid var(--cizgi); }
.kart { border-bottom: 1px solid var(--cizgi); }
.kart-link { display: grid; grid-template-columns: 2.4rem 1fr; gap: 0.8rem; padding-block: 1rem; text-decoration: none; color: inherit; }
.kart-link:hover .kart-baslik { color: var(--vurgu); }
.kart-no { font-family: var(--font-baslik); font-size: 1.6rem; color: var(--vurgu); line-height: 1.1; font-variant-numeric: tabular-nums; }
.kart-govde { display: grid; gap: 0.3rem; min-width: 0; }
.kart-baslik { font-family: var(--font-baslik); font-weight: 700; font-size: 1.15rem; line-height: 1.3; }
.kart-tez { font-size: 0.95rem; color: var(--soluk); line-height: 1.55; }
.kart-meta { font-family: var(--font-arac); font-size: 0.8rem; color: var(--soluk); letter-spacing: 0.02em; }
.kitap { scroll-margin-top: 5rem; }
.kitap-bas { padding-top: 2rem; border-bottom: 1px solid var(--cizgi); padding-bottom: 1.2rem; }
.ust-etiket { font-family: var(--font-arac); text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.78rem; color: var(--vurgu); margin: 0; }
.kitap-bas h1 { font-size: clamp(1.7rem, 5vw, 2.3rem); margin: 0.4rem 0 0.6rem; }
.kunye { font-family: var(--font-arac); color: var(--soluk); font-size: 0.92rem; line-height: 1.5; margin: 0 0 1rem; }
.icindekiler { background: var(--kagit); border: 1px solid var(--cizgi); border-radius: 6px; padding: 0.6rem 0.9rem; font-family: var(--font-arac); font-size: 0.95rem; }
.icindekiler summary { cursor: pointer; font-weight: 500; }
.icindekiler ol { margin: 0.6rem 0 0.2rem; padding-left: 1.3rem; display: grid; gap: 0.25rem; }
.metin h2 { font-size: 1.55rem; margin: 2.6rem 0 0.8rem; padding-top: 0.6rem; border-top: 1px solid var(--cizgi); scroll-margin-top: 4rem; }
.metin h3 { font-size: 1.22rem; margin: 2rem 0 0.5rem; }
.metin h4 { font-family: var(--font-arac); font-size: 1rem; margin: 1.4rem 0 0.4rem; }
.metin p, .metin li { hyphens: auto; }
.metin blockquote { margin: 1.2rem 0; padding: 0.2rem 1rem; border-left: 3px solid var(--vurgu); background: var(--vurgu-zemin); }
.metin code { font-family: var(--font-arac); font-size: 0.92em; }
.tablo { overflow-x: auto; margin: 1.2rem 0; border: 1px solid var(--cizgi); border-radius: 6px; background: var(--kagit); }
.tablo table { border-collapse: collapse; width: 100%; font-family: var(--font-arac); font-size: 0.93rem; line-height: 1.45; }
.tablo th, .tablo td { text-align: left; vertical-align: top; padding: 0.55rem 0.7rem; border-bottom: 1px solid var(--cizgi); min-width: 8rem; }
.tablo th { background: var(--vurgu-zemin); font-weight: 500; }
.tablo tr:last-child td { border-bottom: 0; }
hr { border: 0; border-top: 1px solid var(--cizgi); margin: 2rem 0; }
.kitap-nav { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--cizgi); font-family: var(--font-arac); }
.kitap-nav a { text-decoration: none; font-weight: 500; }
.dipnot { margin-top: 3rem; color: var(--soluk); font-family: var(--font-arac); font-size: 0.85rem; }
</style>

<div class="sayfa">
  <div class="ust-cubuk"><a href="#">Kitaplık</a><span class="yer" id="yer">10 kitap · __TOPLAM__ kelime</span></div>

  <section id="ana" class="giris">
    <h1>Yaranma ve Ret Kitaplığı</h1>
    <p class="alt">Sohbetlerindeki sorgulara göre seçilmiş on psikoloji kitabı, kitabın yerini tutacak ayrıntıda.</p>
    <div class="harita metin">__HARITA__</div>
    <p class="raf-baslik">Raf</p>
    <ol class="raf">__KARTLAR__</ol>
    <p class="dipnot">Her özet önce bir yazar ajan tarafından kaynaklarla yazıldı, sonra ayrı bir hakem ajan tarafından denetlenip düzeltildi. Hakemin notu her özetin sonunda. Özetler kitabın haritasıdır; bir terapistin değerlendirmesinin yerini tutmaz.</p>
  </section>

  __MAKALELER__
</div>

<script>
(function () {
  var ana = document.getElementById('ana');
  var yer = document.getElementById('yer');
  var kitaplar = Array.prototype.slice.call(document.querySelectorAll('article.kitap'));
  var varsayilan = yer.textContent;
  function goster() {
    var h = (location.hash || '').slice(1);
    var hedef = null, alt = null;
    if (h) {
      var parca = h.split('--');
      hedef = document.getElementById(parca[0]);
      if (parca.length > 1) alt = document.getElementById(h);
    }
    if (!hedef || !hedef.classList.contains('kitap')) {
      ana.hidden = false;
      kitaplar.forEach(function (a) { a.hidden = true; });
      yer.textContent = varsayilan;
      return;
    }
    ana.hidden = true;
    kitaplar.forEach(function (a) { a.hidden = (a !== hedef); });
    yer.textContent = hedef.querySelector('h1').textContent;
    if (alt) { alt.scrollIntoView(); } else { window.scrollTo({ top: 0, behavior: 'instant' }); }
  }
  // içindekiler bağlantıları: kitabı aç ve ilgili başlığa kaydır
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-hedef]');
    if (!a) return;
    e.preventDefault();
    var el = document.getElementById(a.getAttribute('data-hedef'));
    if (el) el.scrollIntoView();
  });
  window.addEventListener('hashchange', goster);
  goster();
})();
</script>
"""

sayfa = (
    SAYFA.replace("__HARITA__", harita_html)
    .replace("__KARTLAR__", "".join(kartlar))
    .replace("__MAKALELER__", "".join(makaleler))
    .replace("__TOPLAM__", f"{toplam:,}".replace(",", "."))
)
CIKTI.write_text(sayfa, encoding="utf-8")
print(f"{len(kitaplar)} kitap, {toplam} kelime -> {CIKTI} ({CIKTI.stat().st_size // 1024} KB)")
