#!/usr/bin/env python3
"""RAPOR.md -> RAPOR.html -> PDF (Chromium/Playwright ile).

Kullanım: python3 hesap/03_pdf_uret.py
Girdi : ../RAPOR.md (ve grafik/ klasöründeki PNG'ler)
Çıktı : ../Havacilik_Savunma_DXY_Raporu.pdf
"""
import pathlib
import re
import subprocess
import sys

import markdown

KOK = pathlib.Path(__file__).resolve().parent.parent
MD = KOK / "RAPOR.md"
HTML = KOK / "hesap" / "_rapor.html"
PDF = KOK / "Havacilik_Savunma_DXY_Raporu.pdf"

CSS = r"""
@page { size: A4; margin: 17mm 15mm 18mm 15mm; }
* { box-sizing: border-box; }
html { font-family: 'Inter', 'DejaVu Sans', sans-serif; font-size: 10.4pt; line-height: 1.5; color: #1b2430;
       font-feature-settings: 'calt' 0, 'case' 0, 'tnum' 0, 'ss01' 0; font-variant-ligatures: none; }
body { margin: 0; }
h1 { font-size: 21pt; line-height: 1.2; margin: 0 0 4pt; color: #0f2a47; letter-spacing: -0.2pt; }
h2 { font-size: 14pt; margin: 20pt 0 6pt; padding-bottom: 3pt; border-bottom: 1.2pt solid #0f2a47; color: #0f2a47; break-after: avoid; }
h3 { font-size: 11.4pt; margin: 14pt 0 4pt; color: #17406b; break-after: avoid; }
h4 { font-size: 10.4pt; margin: 10pt 0 3pt; color: #17406b; break-after: avoid; }
p { margin: 0 0 7pt; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 7pt; padding-left: 16pt; }
li { margin-bottom: 2.5pt; }
strong { color: #0f2a47; }
a { color: #1a5a96; text-decoration: none; word-break: break-word; }
blockquote { margin: 8pt 0; padding: 7pt 11pt; background: #eef3f8; border-left: 3pt solid #1a5a96; border-radius: 2pt; break-inside: avoid; }
blockquote p:last-child { margin-bottom: 0; }
code { font-family: 'JetBrains Mono', 'DejaVu Sans Mono', monospace; font-size: 8.8pt; background: #f1f3f5; padding: 0 2pt; border-radius: 2pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 8.6pt; line-height: 1.35; }
thead { display: table-header-group; }
table { break-inside: avoid; }
tr { break-inside: avoid; }
li { break-inside: avoid; }
th { background: #0f2a47; color: #fff; font-weight: 600; text-align: left; padding: 4pt 5pt; vertical-align: bottom; }
td { padding: 3.5pt 5pt; border-bottom: 0.5pt solid #d5dbe2; vertical-align: top; }
tbody tr:nth-child(even) td { background: #f6f8fa; }
td[align=right], th[align=right] { text-align: right; }
td[align=center], th[align=center] { text-align: center; }
img { max-width: 100%; display: block; margin: 6pt auto 2pt; }
p:has(> img) { break-inside: avoid; margin-bottom: 2pt; }
p:has(> img) + p > em:only-child, .altyazi { display: block; font-size: 8.4pt; color: #5a6675; text-align: center; margin-bottom: 9pt; }
hr { border: 0; border-top: 0.6pt solid #c7ced6; margin: 12pt 0; }
.kapak { border-bottom: 2.2pt solid #0f2a47; padding-bottom: 9pt; margin-bottom: 12pt; }
.kapak .ust { font-size: 8.6pt; letter-spacing: 1.1pt; text-transform: uppercase; color: #5a6675; margin-bottom: 5pt; }
.kapak .alt { font-size: 9.4pt; color: #5a6675; margin-top: 4pt; }
.kutu { background: #f3f7fb; border: 0.6pt solid #c4d3e3; border-radius: 3pt; padding: 8pt 11pt; margin: 8pt 0 10pt; break-inside: avoid; }
.kutu p:last-child, .kutu ul:last-child { margin-bottom: 0; }
.uyari { background: #fdf6e7; border: 0.6pt solid #e6cf9a; border-radius: 3pt; padding: 8pt 11pt; margin: 8pt 0 10pt; break-inside: avoid; }
.uyari p:last-child { margin-bottom: 0; }
.kucuk, .kucuk td, .kucuk th { font-size: 7.8pt; }
.kaynak { font-size: 8.2pt; line-height: 1.4; }
.kaynak li { margin-bottom: 1.5pt; }
.sayfa-kir { break-before: page; }
"""

SABLON = """<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<title>{baslik}</title>
<style>{css}</style></head>
<body>{govde}</body></html>
"""

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [html, pdf] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.pdf({
    path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%;font-family:Inter,'DejaVu Sans',sans-serif;font-size:7.5pt;color:#7a8594;padding:0 15mm;display:flex;justify-content:space-between;"><span>Havacılık-Savunma Endeksleri ve Dolar · 19 Kasım 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
"""


def main():
    metin = MD.read_text(encoding="utf-8")
    govde = markdown.markdown(
        metin,
        extensions=["tables", "attr_list", "md_in_html", "sane_lists", "footnotes"],
        output_format="html5",
    )
    # grafik yolları: RAPOR.md'ye göre göreli -> mutlak file://
    govde = re.sub(r'src="(?!https?:|file:|data:)([^"]+)"', lambda m: f'src="file://{(KOK / m.group(1)).resolve()}"', govde)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", govde, re.S)
    baslik = re.sub(r"<[^>]+>", "", m.group(1)) if m else "Rapor"
    HTML.write_text(SABLON.format(baslik=baslik, css=CSS, govde=govde), encoding="utf-8")
    js = KOK / "hesap" / "_pdf.js"
    js.write_text(JS, encoding="utf-8")
    r = subprocess.run(["node", str(js), str(HTML), str(PDF)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    print("PDF:", PDF, f"{PDF.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
