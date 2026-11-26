// MyVia 414 (Park Myvia 414, Bornova/Izmir) kafe verisi - Google Haritalar (Playwright)
// Kullanim:
//   node gmaps_scrape.js                 -> kesif + ayrinti + yorumlar, ../veri/ altina yazar
//   node gmaps_scrape.js --reuse         -> kesif dosyasi varsa tekrar aramaz
//   node gmaps_scrape.js --place <url>   -> tek yerin ayrinti + hakkinda + yorumlari, stdout'a JSON
// Loglar stderr'e gider; stdout yalnizca --place modunda JSON'dur.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const VERI = path.resolve(__dirname, '../veri');
const CENTER = { lat: 38.4508, lon: 27.2010 };
const BOX = { latMin: 38.4501, latMax: 38.4515, lonMin: 27.2004, lonMax: 27.2016 };
const QUERIES = ['kafe', 'kahve', 'coffee', 'cafe', 'pastane', 'tatlı', 'çay', 'bistro', 'Myvia 414', 'Park Myvia'];
const ZOOMS = [18, 19];
const MAX_REVIEWS = 80;
const DETAIL_MAX_M = 300;       // merkezden bu mesafeden uzaktaki yerler icin ayrinti acilmaz
const KEYWORDS = ['laptop', 'bilgisayar', 'ders', 'çalış', 'priz', 'şarj', 'wifi', 'wi-fi', 'internet', 'sessiz', 'sakin', 'gürültü', 'müzik', 'kalabalık', 'kitap', 'oku', 'fiyat', 'pahalı', 'uygun', 'ucuz', '₺', 'tl', 'lira', 'latte', 'filtre', 'v60', 'chemex', 'espresso', 'çekirdek', 'nesil', 'servis', 'garson', 'personel', 'masa', 'koltuk', 'sigara', 'süre', 'kalk'];
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

const log = (...a) => console.error(new Date().toISOString().slice(11, 19), ...a);
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const pause = () => sleep(1500 + Math.random() * 1500);
const norm = (s) => s.toLocaleLowerCase('tr').replace(/ı/g, 'i');
const NKW = KEYWORDS.map(norm);

// ---------- geometri ----------
function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371000, t = x => x * Math.PI / 180;
  const a = Math.sin(t(lat2 - lat1) / 2) ** 2 + Math.cos(t(lat1)) * Math.cos(t(lat2)) * Math.sin(t(lon2 - lon1) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}
function boxDist(lat, lon) {
  const la = Math.min(Math.max(lat, BOX.latMin), BOX.latMax);
  const lo = Math.min(Math.max(lon, BOX.lonMin), BOX.lonMax);
  return haversine(lat, lon, la, lo);
}
function coordsFromUrl(u) {
  const m = u.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/);
  if (m) return { lat: +m[1], lon: +m[2] };
  const m2 = u.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
  return m2 ? { lat: +m2[1], lon: +m2[2] } : null;
}
function idFromUrl(u) {
  const m = u.match(/!1s(0x[0-9a-f]+:0x[0-9a-f]+)/i);
  return m ? m[1] : null;
}
function classify(p) {
  const text = [p.adres, p.ad, p.konumda].filter(Boolean).join(' ');
  let neden = null;
  if (p.lat != null && p.lat >= BOX.latMin && p.lat <= BOX.latMax && p.lon >= BOX.lonMin && p.lon <= BOX.lonMax) neden = 'koordinat kutu içinde';
  else if (/myvia|park myvia|\b414\b/i.test(text)) neden = 'ad/adres/konum metninde Myvia/414';
  if (neden) return { konum: 'içinde', neden };
  if (p.kutu_mesafe_m != null && p.kutu_mesafe_m <= 120) return { konum: 'bitişik', neden: `kutuya ${Math.round(p.kutu_mesafe_m)} m` };
  return { konum: 'dışında', neden: p.kutu_mesafe_m != null ? `kutuya ${Math.round(p.kutu_mesafe_m)} m` : 'koordinat yok' };
}
function kafeMi(kategori, ad) {
  const re = /kafe|cafe|kahve|coffee|pastane|tatlı|çay|fırın|bistro|kahvaltı|dondurma|börek|kruvasan|croissant|boyoz|çikolata/i;
  if (kategori && !/kapalı/i.test(kategori)) return re.test(kategori);
  return /coffee|kahve|cafe|kafe|pastane/i.test(ad || '');
}

// ---------- tarayici ----------
async function launch() {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const ctx = await browser.newContext({ locale: 'tr-TR', userAgent: UA, viewport: { width: 1400, height: 900 } });
  const page = await ctx.newPage();
  return { browser, page };
}
async function handleConsent(page) {
  try {
    if (/consent\./.test(page.url())) {
      const b = page.locator('button:has-text("Tümünü kabul et"), button:has-text("Accept all")').first();
      await b.click({ timeout: 5000 });
      await page.waitForLoadState('domcontentloaded');
      await sleep(2000);
    }
  } catch (e) { /* onay ekrani yok */ }
}
async function goto(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await handleConsent(page);
}

// ---------- kesif ----------
async function discover(page) {
  const found = new Map();
  for (const q of QUERIES) {
    for (const z of ZOOMS) {
      const url = `https://www.google.com/maps/search/${encodeURIComponent(q)}/@${CENTER.lat},${CENTER.lon},${z}z?hl=tr`;
      try {
        await goto(page, url);
        await sleep(5000);
        let n = 0;
        if (/\/maps\/place\//.test(page.url()) && !(await page.$('div[role=feed]'))) {
          const href = page.url(); const c = coordsFromUrl(href);
          const ad = await page.$eval('h1', e => e.innerText).catch(() => null);
          const id = idFromUrl(href) || `${ad}@${c && c.lat}`;
          if (!found.has(id)) found.set(id, { id, ad, href, ...c, sorgular: [] });
          found.get(id).sorgular.push(`${q}@${z}`);
          log(`kesif ${q} ${z}z -> tek yer: ${ad}`);
          continue;
        }
        let stable = 0, last = 0;
        for (let i = 0; i < 30 && stable < 3; i++) {
          n = await page.$$eval('div[role=feed] a[aria-label]', a => a.length).catch(() => 0);
          const end = await page.$eval('div[role=feed]', f => /sonuna|end of the list/i.test(f.innerText.slice(-200))).catch(() => false);
          if (end) break;
          stable = n === last ? stable + 1 : 0; last = n;
          await page.$eval('div[role=feed]', f => { f.scrollTop = f.scrollHeight; }).catch(() => { });
          await sleep(1500);
        }
        const items = await page.$$eval('div[role=feed] a[aria-label]', as => as.map(a => ({ ad: a.getAttribute('aria-label'), href: a.href })));
        for (const it of items) {
          const c = coordsFromUrl(it.href) || {};
          const id = idFromUrl(it.href) || `${it.ad}@${c.lat}`;
          if (!found.has(id)) found.set(id, { id, ad: it.ad, href: it.href, ...c, sorgular: [] });
          found.get(id).sorgular.push(`${q}@${z}`);
        }
        log(`kesif ${q} ${z}z -> ${items.length} sonuc, toplam ${found.size}`);
      } catch (e) { log(`kesif HATA ${q} ${z}z: ${e.message.split('\n')[0]}`); }
      await pause();
    }
  }
  return [...found.values()];
}

// ---------- yer sayfasi ----------
async function openPlace(page, url) {
  for (let t = 0; t < 4; t++) {
    await goto(page, t === 0 ? url : page.url());
    if (t > 0) await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForSelector('h1', { timeout: 15000 }).catch(() => { });
    await sleep(4000);
    const tabs = await page.$$eval('button[role=tab]', e => e.map(x => x.innerText)).catch(() => []);
    if (tabs.length >= 2 && tabs.some(x => /Yorumlar/.test(x))) return { tabs, limited: tabs.length < 3 };
    log('  sinirli gorunum/sekme yok, yeniden deneniyor', t + 1);
  }
  const tabs = await page.$$eval('button[role=tab]', e => e.map(x => x.innerText)).catch(() => []);
  return { tabs, limited: true };
}

async function extractDetail(page) {
  const d = await page.evaluate(() => {
    const main = document.querySelector('div[role=main]');
    const txt = main ? main.innerText : '';
    const out = { txt: txt.slice(0, 3000) };
    out.ad = (document.querySelector('h1') || {}).innerText || null;
    const attr = (sel, a) => { const e = document.querySelector(sel); return e ? e.getAttribute(a) : null; };
    const adr = attr('[data-item-id="address"]', 'aria-label');
    out.adres = adr ? adr.replace(/^Adres:\s*/, '').trim() : null;
    const ph = attr('[data-item-id^="phone"]', 'aria-label');
    out.telefon = ph ? ph.replace(/^Telefon:\s*/, '').trim() : null;
    const web = document.querySelector('a[data-item-id="authority"]');
    out.web = web ? web.href : null;
    const loc = attr('[data-item-id="locatedin"]', 'aria-label');
    out.konumda = loc ? loc.replace(/^Konum:\s*/, '').trim() : null;
    const cat = document.querySelector('button[jsaction*="category"]');
    out.kategori = cat ? cat.innerText.trim() : null;
    const rs = document.querySelector('div.F7nice');
    if (rs) {
      const r = rs.querySelector('span[aria-hidden=true]'); out.puan = r ? r.innerText.trim() : null;
      const c = rs.querySelector('span[aria-label*="yorum"]'); out.yorum_sayisi = c ? (c.getAttribute('aria-label') || c.innerText).replace(/[^\d.]/g, '') : null;
    }
    const days = [];
    document.querySelectorAll('table tr').forEach(tr => {
      const t = tr.innerText.replace(/\s+/g, ' ').trim();
      const m = t.match(/^(Pazartesi|Salı|Çarşamba|Perşembe|Cumartesi|Cuma|Pazar)\s*(.*)$/);
      if (m) days.push([m[1], m[2].replace(/[\ue000-\uf8ff]/g, '').trim()]);
    });
    out.saatler = days;
    return out;
  });
  const t = d.txt;
  if (!d.puan) { const m = t.match(/\n(\d[,.]\d)\n/); if (m) d.puan = m[1]; }
  if (!d.yorum_sayisi) { const m = t.match(/\((\d[\d.]*)\)/) || t.match(/(\d[\d.]*) yorum/); if (m) d.yorum_sayisi = m[1].replace(/\./g, ''); }
  if (!d.kategori) { const m = t.match(/\n([^\n]{3,40})·?\n(?:Genel Bakış|Yol tarifi)/); if (m) d.kategori = m[1].replace(/·/, '').trim(); }
  // durum
  let durum = 'bilinmiyor';
  if (/Kalıcı olarak kapandı/i.test(t)) durum = 'Kalıcı olarak kapandı';
  else if (/Geçici olarak kapalı/i.test(t)) durum = 'Geçici olarak kapalı';
  else {
    const m = t.match(/^(Açık|Kapalı|Kapanış|Açılış|Yakında kapanıyor|Yakında açılıyor)[^\n]*/m);
    durum = m ? `açık (kalıcı kapanma yok); anlık: ${m[0].trim()}` : 'açık (kalıcı kapanma işareti yok)';
  }
  // fiyat
  let fiyat = null;
  let m = t.match(/(?:kişi başı|kişi başına)[^\n₺]{0,40}(₺\s?[\d.,]+(?:\s?[–-]\s?[\d.,]+|\+)?)/i)
    || t.match(/(₺\s?[\d.,]+(?:\s?[–-]\s?[\d.,]+|\+))/) || t.match(/^\s*(₺{1,4})\s*$/m);
  if (m) fiyat = m[1].trim();
  const fm = await page.$$eval('[aria-label*="Fiyat" i], [aria-label*="kişi başı" i]', e => e.map(x => x.getAttribute('aria-label')).slice(0, 3)).catch(() => []);
  if (!fiyat && fm.length) fiyat = fm[0];
  d.kisi_basi = fiyat; d.durum = durum;
  delete d.txt;
  return d;
}

async function extractAbout(page) {
  try {
    const tab = page.locator('button[role=tab]:has-text("Hakkında")').first();
    if (!(await tab.count())) return null;
    await tab.click({ timeout: 5000 });
    await sleep(2500);
    return await page.evaluate(() => {
      const main = document.querySelector('div[role=main]');
      const res = []; let sec = '';
      main.querySelectorAll('h2, li').forEach(e => {
        if (e.tagName === 'H2') { sec = e.innerText.trim(); return; }
        const lab = e.querySelector('[aria-label]');
        const label = lab ? lab.getAttribute('aria-label').trim() : '';
        const ad = e.innerText.split('\n').map(s => s.trim()).filter(Boolean).pop() || label;
        let var_ = null;
        if (/\svar$/i.test(label)) var_ = true; else if (/\syok$|değil$|olmayan/i.test(label)) var_ = false;
        res.push({ bolum: sec, ad, var: var_, aria: label });
      });
      return res;
    });
  } catch (e) { log('  hakkinda HATA', e.message.split('\n')[0]); return null; }
}

async function extractReviews(page, maxReviews) {
  const out = { cipler: [], yorumlar: [], not: [] };
  try {
    await page.locator('button[role=tab]:has-text("Yorumlar")').first().click({ timeout: 5000 });
    await sleep(2500);
  } catch (e) { out.not.push('yorumlar sekmesi açılamadı'); return out; }
  // cipler
  out.cipler = await page.evaluate(() => {
    const res = [], seen = new Set();
    document.querySelectorAll('div[role=main] button.e2moi, div[role=main] [role=radiogroup] button').forEach(b => {
      const parts = b.innerText.split('\n').map(s => s.trim()).filter(Boolean);
      if (!parts.length) return;
      const last = parts[parts.length - 1];
      let ad, sayi = null;
      if (/^\d+$/.test(last) && parts.length > 1) { sayi = +last; ad = parts.slice(0, -1).join(' '); } else ad = parts.join(' ');
      if (!seen.has(ad)) { seen.add(ad); res.push({ ad, sayi }); }
    });
    return res;
  }).catch(() => []);
  // Not: oturumsuz Google Haritalar yorum listesini ~5 yorumla sinirlar (oturum acma istemi).
  // Cozum: farkli siralamalar + yorum ici anahtar kelime aramasi, her biri en cok 5 yorum doner; birlestirilir.
  const all = new Map();
  const readNow = async (tag) => {
    await page.evaluate(() => document.querySelectorAll('div.jftiEf[data-review-id] button.w8nwRe').forEach(b => { try { b.click(); } catch (e) { } })).catch(() => { });
    await sleep(500);
    const rs = await page.evaluate(() => {
      const res = [];
      document.querySelectorAll('div.jftiEf[data-review-id]').forEach(r => {
        const st = r.querySelector('.kvMYJc'); const stl = st ? st.getAttribute('aria-label') : '';
        const dt = r.querySelector('.rsqaWe');
        let metin = '';
        r.querySelectorAll('.wiI7pd').forEach(e => { if (!metin && !e.closest('.CDe7pd')) metin = e.textContent.trim(); });
        res.push({ id: r.getAttribute('data-review-id'), yildiz: stl ? +(stl.match(/\d/) || [null])[0] : null, tarih: dt ? dt.innerText.trim() : null, metin });
      });
      return res;
    }).catch(() => []);
    let nw = 0;
    for (const r of rs) if (!all.has(r.id)) { all.set(r.id, { yildiz: r.yildiz, tarih: r.tarih, metin: r.metin, kaynak: tag }); nw++; }
    return rs;
  };
  const dismiss = async () => { try { await page.locator('button:has-text("Kapat")').first().click({ timeout: 800 }); } catch (e) { } };
  const setSort = async (name) => {
    const sb = page.locator('button').filter({ hasText: /(En alakalı|En yeni|En yüksek puanlı|En düşük puanlı)/ }).first();
    await sb.click({ timeout: 5000 }); await sleep(1000);
    await page.locator(`[role=menuitemradio]:has-text("${name}")`).first().click({ timeout: 5000 });
    await sleep(2800);
  };
  let newest = [];
  try { await setSort('En yeni'); newest = await readNow('en yeni'); }
  catch (e) { out.not.push('"En yeni" sıralaması seçilemedi: ' + e.message.split('\n')[0]); newest = await readNow('varsayılan'); }
  const newestIds = newest.map(r => r.id);
  for (const so of ['En yüksek puanlı', 'En düşük puanlı']) {
    if (all.size >= maxReviews) break;
    try { await setSort(so); await readNow(so.toLowerCase()); } catch (e) { out.not.push(so + ' sıralaması alınamadı'); }
  }
  const terms = ['laptop', 'priz', 'wifi', 'sessiz', 'çalış', 'ders', 'fiyat', 'kalabalık', 'masa', 'müzik', 'kitap', 'sigara'];
  const inp = page.locator('div[role=main] input').first();
  if (await inp.count()) {
    for (const t of terms) {
      if (all.size >= maxReviews) break;
      try { await dismiss(); await inp.fill(t); await inp.press('Enter'); await sleep(2500); await readNow('arama:' + t); }
      catch (e) { out.not.push('yorum araması başarısız: ' + t); }
    }
  } else out.not.push('yorum arama kutusu yok');
  const list = [...all.entries()].map(([id, r]) => ({ id, ...r }));
  // en yeni 5 basta, sonra digerleri
  const rank = (r) => { const i = newestIds.indexOf(r.id); return i < 0 ? 999 : i; };
  list.sort((x, y) => rank(x) - rank(y));
  out.yorumlar = list.map(({ id, ...r }) => r);
  out.not.push(`oturumsuz görünüm: sıralama başına ≤5 yorum; toplam ${list.length} benzersiz yorum (en yeni sıralamadan ${newestIds.length})`);
  return out;
}

function snippets(yorumlar) {
  const res = [];
  for (const y of yorumlar) {
    if (!y.metin) continue;
    const n = norm(y.metin);
    let idx = -1; const hit = [];
    NKW.forEach((k, i) => { const j = n.indexOf(k); if (j >= 0) { hit.push(KEYWORDS[i]); if (idx < 0 || j < idx) idx = j; } });
    if (idx < 0) continue;
    const s = Math.max(0, idx - 150), e = Math.min(y.metin.length, s + 300);
    res.push({ yildiz: y.yildiz, tarih: y.tarih, anahtar: hit, snippet: y.metin.slice(s, e) });
    if (res.length >= 40) break;
  }
  return res;
}

async function scrapePlace(page, url, withReviews = true) {
  const missing = [];
  const { tabs, limited } = await openPlace(page, url);
  const detail = await extractDetail(page);
  const cur = page.url();
  const c = coordsFromUrl(cur) || coordsFromUrl(url) || {};
  const p = {
    ad: detail.ad, url: cur, place_id: idFromUrl(cur) || idFromUrl(url), kategori: detail.kategori, puan: detail.puan || null,
    yorum_sayisi: detail.yorum_sayisi || null, adres: detail.adres, lat: c.lat ?? null, lon: c.lon ?? null,
    durum: detail.durum, saatler: Object.fromEntries(detail.saatler || []), web: detail.web, telefon: detail.telefon,
    kisi_basi: detail.kisi_basi, konumda: detail.konumda, sekmeler: tabs, sinirli_gorunum: limited,
  };
  if (p.lat != null) { p.mesafe_m = Math.round(haversine(CENTER.lat, CENTER.lon, p.lat, p.lon)); p.kutu_mesafe_m = Math.round(boxDist(p.lat, p.lon)); }
  Object.assign(p, classify(p));
  p.kafe_mi = kafeMi(p.kategori, p.ad);
  for (const k of ['kategori', 'puan', 'yorum_sayisi', 'adres', 'web', 'telefon', 'kisi_basi']) if (!p[k]) missing.push(k);
  if (!Object.keys(p.saatler).length) missing.push('saatler');
  p.ozellikler = await extractAbout(page);
  if (p.ozellikler == null) { p.ozellikler = []; missing.push('hakkında_sekmesi'); }
  if (withReviews) {
    await pause();
    const r = await extractReviews(page, MAX_REVIEWS);
    p.yorum_cipleri = r.cipler; if (!r.cipler.length) missing.push('yorum_cipleri');
    p.yorum_cekilen = r.yorumlar.length;
    p.yorum_snippet = snippets(r.yorumlar);
    p.en_yeni_10 = r.yorumlar.filter(y => y.kaynak === 'en yeni' || y.kaynak === 'varsayılan').slice(0, 10);
    if (r.not.length) missing.push(...r.not);
    if (!r.yorumlar.length) missing.push('yorumlar');
  }
  p.eksik_alanlar = missing;
  return p;
}

// ---------- cikti ----------
function csvCell(v) { const s = v == null ? '' : String(v); return /[",\n;]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
function writeOutputs(places) {
  fs.mkdirSync(VERI, { recursive: true });
  fs.writeFileSync(path.join(VERI, 'gmaps_kafeler.json'), JSON.stringify({ uretim: new Date().toISOString(), merkez: CENTER, kutu: BOX, yerler: places }, null, 1));
  const cols = ['ad', 'kategori', 'kafe_mi', 'konum', 'mesafe_m', 'kutu_mesafe_m', 'puan', 'yorum_sayisi', 'durum', 'adres', 'konumda', 'kisi_basi', 'web', 'telefon', 'ozellik_sayisi', 'cip_sayisi', 'yorum_cekilen', 'snippet_sayisi', 'eksik_alanlar', 'url'];
  const rows = places.map(p => ({ ...p, ozellik_sayisi: (p.ozellikler || []).length, cip_sayisi: (p.yorum_cipleri || []).length, snippet_sayisi: (p.yorum_snippet || []).length, eksik_alanlar: (p.eksik_alanlar || []).join('|') }));
  fs.writeFileSync(path.join(VERI, 'gmaps_ozet.csv'), [cols.join(','), ...rows.map(r => cols.map(c => csvCell(r[c])).join(','))].join('\n'));
}

async function main() {
  const argv = process.argv.slice(2);
  const pi = argv.indexOf('--place');
  const { browser, page } = await launch();
  try {
    if (pi >= 0) {
      const p = await scrapePlace(page, argv[pi + 1]);
      process.stdout.write(JSON.stringify(p, null, 1) + '\n');
      return;
    }
    fs.mkdirSync(VERI, { recursive: true });
    const kf = path.join(VERI, 'gmaps_kesif.json');
    let cands;
    if (argv.includes('--reuse') && fs.existsSync(kf)) cands = JSON.parse(fs.readFileSync(kf, 'utf8'));
    else { cands = await discover(page); fs.writeFileSync(kf, JSON.stringify(cands, null, 1)); }
    log('aday yer:', cands.length);
    const places = [];
    for (const c of cands) {
      if (c.lat == null) { log('koordinat yok:', c.ad); }
      const dist = c.lat != null ? haversine(CENTER.lat, CENTER.lon, c.lat, c.lon) : 0;
      if (dist > DETAIL_MAX_M) {
        places.push({ ad: c.ad, url: c.href, place_id: c.id, lat: c.lat, lon: c.lon, mesafe_m: Math.round(dist), kutu_mesafe_m: Math.round(boxDist(c.lat, c.lon)), konum: 'dışında', kafe_mi: null, kategori: null, eksik_alanlar: ['ayrıntı açılmadı (300 m dışı)'] });
        continue;
      }
      const pre = classify({ ad: c.ad, lat: c.lat, lon: c.lon, kutu_mesafe_m: boxDist(c.lat, c.lon) });
      let p = null;
      for (let t = 0; t < 2 && !p; t++) {
        try {
          log(`yer: ${c.ad} (${Math.round(dist)} m, ön ${pre.konum})`);
          // once ayrinti (yorumsuz), sonra karara gore yorum
          p = await scrapePlace(page, c.href, false);
          const wantReviews = p.konum !== 'dışında' || (p.mesafe_m <= 250 && p.kafe_mi);
          if (wantReviews) {
            await pause();
            const r = await extractReviews(page, MAX_REVIEWS);
            p.yorum_cipleri = r.cipler; if (!r.cipler.length) p.eksik_alanlar.push('yorum_cipleri');
            p.yorum_cekilen = r.yorumlar.length; p.yorum_snippet = snippets(r.yorumlar); p.en_yeni_10 = r.yorumlar.filter(y => y.kaynak === 'en yeni' || y.kaynak === 'varsayılan').slice(0, 10);
            if (r.not.length) p.eksik_alanlar.push(...r.not);
            if (!r.yorumlar.length) p.eksik_alanlar.push('yorumlar');
          } else p.eksik_alanlar.push('yorumlar çekilmedi (kapsam dışı)');
        } catch (e) { log('  HATA', e.message.split('\n')[0]); p = null; await pause(); }
      }
      if (!p) p = { ad: c.ad, url: c.href, place_id: c.id, lat: c.lat, lon: c.lon, konum: pre.konum, eksik_alanlar: ['ayrıntı çekilemedi'] };
      p.sorgular = c.sorgular;
      places.push(p);
      writeOutputs(places);
      await pause();
    }
    writeOutputs(places);
    log('bitti. yer:', places.length);
  } finally { await browser.close(); }
}
main().catch(e => { console.error('ERR', e); process.exit(1); });
