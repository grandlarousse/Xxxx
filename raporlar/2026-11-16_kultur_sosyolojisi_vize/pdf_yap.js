// kitapcik.html dosyasını A5 PDF'e çevirir.  Kullanım: node pdf_yap.js
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'kitapcik.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(dir, 'SOS337_Kultur_Sosyolojisi_Vize_Tekrar.pdf'),
    width: '148mm',
    height: '210mm',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate:
      '<div style="width:100%;font-family:Inter,sans-serif;font-size:7pt;color:#7a8794;' +
      'padding:0 11mm;display:flex;justify-content:space-between;">' +
      '<span>SOS 337 Kültür Sosyolojisi · Vize Tekrar</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '13mm', bottom: '15mm', left: '11mm', right: '11mm' },
  });
  await browser.close();
})();
