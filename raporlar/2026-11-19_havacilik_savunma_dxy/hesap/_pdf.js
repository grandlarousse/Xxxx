
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
