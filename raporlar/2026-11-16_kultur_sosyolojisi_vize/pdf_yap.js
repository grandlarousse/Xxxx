// kitapcik.html dosyasını iki boyutta PDF'e çevirir.  Kullanım: node pdf_yap.js
//  - telefon sürümü (dar sayfa, büyük yazı): SOS337_Kultur_Sosyolojisi_Vize_Tekrar.pdf
//  - yazdırma sürümü (A5):                   SOS337_Kultur_Sosyolojisi_Vize_Tekrar_A5_yazdirma.pdf
const path = require('path');
const { chromium } = require('playwright');

const SURUMLER = [
  { dosya: 'SOS337_Kultur_Sosyolojisi_Vize_Tekrar.pdf', w: '118mm', h: '200mm', m: { top: '11mm', bottom: '13mm', left: '9mm', right: '9mm' } },
  { dosya: 'SOS337_Kultur_Sosyolojisi_Vize_Tekrar_A5_yazdirma.pdf', w: '148mm', h: '210mm', m: { top: '13mm', bottom: '15mm', left: '11mm', right: '11mm' } },
];

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'kitapcik.html'));
  await page.evaluate(() => document.fonts.ready);
  for (const s of SURUMLER) {
    await page.pdf({
      path: path.join(dir, s.dosya),
      width: s.w,
      height: s.h,
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate:
        '<div style="width:100%;font-family:Inter,sans-serif;font-size:7pt;color:#7a8794;' +
        'padding:0 ' + s.m.left + ';display:flex;justify-content:space-between;">' +
        '<span>SOS 337 Kültür Sosyolojisi · Vize Tekrar</span>' +
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
      margin: s.m,
    });
  }
  await browser.close();
})();
