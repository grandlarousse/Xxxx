// Kullanım:  node render.js onizleme <cikti.jpg> t1,t2,...   |   node render.js tam <kare_klasoru> [isci_sayisi]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = __dirname;
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.woff2': 'font/woff2', '.woff': 'font/woff' };
(async () => {
  const srv = http.createServer((req, res) => {
    const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
  });
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const url = `http://127.0.0.1:${srv.address().port}/index.html`;
  const browser = await chromium.launch();
  const open = async () => {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('[sayfa]', m.text()); });
    page.on('pageerror', e => console.log('[sayfa hatası]', e.message));
    await page.goto(url);
    await page.waitForFunction(() => window.READY || window.FAILED, null, { timeout: 120000 });
    const failed = await page.evaluate(() => window.FAILED); if (failed) throw new Error(failed);
    return page;
  };
  const [mode, out, arg] = process.argv.slice(2);
  if (mode === 'onizleme') {
    const page = await open();
    const times = arg.split(',').map(Number);
    if (process.env.HARITA) await page.evaluate(() => { window.DEBUG = true; });
    const cols = Math.min(4, times.length), cw = 360, ch = 640;
    const b64 = await page.evaluate(({ times, cols, cw, ch }) => {
      const rows = Math.ceil(times.length / cols);
      const s = document.createElement('canvas'); s.width = cols * cw; s.height = rows * ch;
      const sx = s.getContext('2d'); sx.imageSmoothingQuality = 'high';
      const c = document.getElementById('c');
      times.forEach((t, i) => {
        window.renderAt(t);
        const x = (i % cols) * cw, y = Math.floor(i / cols) * ch;
        sx.drawImage(c, x, y, cw, ch);
        sx.fillStyle = '#ff0'; sx.font = '20px monospace'; sx.fillText(t.toFixed(2) + 's', x + 8, y + 24);
      });
      return (times.length === 1 ? c : s).toDataURL('image/jpeg', 0.9).slice(23);
    }, { times, cols, cw, ch });
    fs.writeFileSync(out, Buffer.from(b64, 'base64'));
    console.log('yazıldı', out);
  } else {
    fs.mkdirSync(out, { recursive: true });
    const nW = Number(arg || 4);
    const info = await (await open()).evaluate(() => window.FILM);
    const total = Math.round(info.DUR * info.FPS);
    let next = 0; const t0 = Date.now();
    await Promise.all(Array.from({ length: nW }, async () => {
      const page = await open();
      for (;;) {
        const i = next++; if (i >= total) break;
        const b64 = await page.evaluate(t => { window.renderAt(t); return document.getElementById('c').toDataURL('image/jpeg', 0.96).slice(23); }, i / info.FPS);
        fs.writeFileSync(path.join(out, String(i).padStart(5, '0') + '.jpg'), Buffer.from(b64, 'base64'));
        if (i % 150 === 0) console.log('kare', i, '/', total, ((Date.now() - t0) / 1000).toFixed(0) + 's');
      }
    }));
    console.log('bitti', total, 'kare', ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  await browser.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
