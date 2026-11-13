'use strict';
/* 560 Yıl Rumeli — Sırp-Bulgar Savaşı (1885) Reel'i.
   Her kare yalnızca t'nin (saniye) fonksiyonudur: renderAt(t) aynı t için hep aynı kareyi çizer. */
(async function () {
  const W = 1080, H = 1920, DUR = 30, FPS = 30;
  const cv = document.getElementById('c');
  const ctx = cv.getContext('2d');
  const TAU = Math.PI * 2;

  /* ---------- yardımcılar ---------- */
  const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
  const lerp = (a, b, t) => a + (b - a) * t;
  const prog = (t, a, b) => clamp((t - a) / (b - a));
  const eOut3 = x => 1 - Math.pow(1 - x, 3);
  const eIO = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  const eOutExpo = x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
  const eIn2 = x => x * x;
  function rng(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const mix = (a, b, t, al = 1) => {
    const A = hex(a), B = hex(b); t = clamp(t);
    return `rgba(${Math.round(lerp(A[0], B[0], t))},${Math.round(lerp(A[1], B[1], t))},${Math.round(lerp(A[2], B[2], t))},${al})`;
  };
  const rgba = (h, al) => mix(h, h, 0, al);

  const C = {
    land: '#27303a', coast: '#8fa3b8',
    otto: '#801616', ottoHi: '#bb261d', ottoDim: '#4f1414',
    bg: '#1d4b34', bgHi: '#37a568',
    rs: '#1f2f47', rsHi: '#3d72bd',
    gold: '#dcb55c', white: '#f4efe4', red: '#ea3a2b', blue: '#9fc5ff', green: '#93e2ab',
  };
  const FAM = { disp: 'Anton', sans: 'Oswald', serif: '"Playfair Display"' };

  /* ---------- yazı tipleri ---------- */
  const sample = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ abcçdefgğhıijklmnoöprsştuüvyz 0123456789 .,–·’';
  await Promise.all([
    document.fonts.load('400 100px Anton', sample),
    document.fonts.load('500 100px Oswald', sample),
    document.fonts.load('600 100px Oswald', sample),
    document.fonts.load('italic 500 100px "Playfair Display"', sample),
    document.fonts.load('italic 700 100px "Playfair Display"', sample),
  ]);
  await document.fonts.ready;

  /* ---------- harita verisi ---------- */
  const world = await (await fetch('node_modules/world-atlas/countries-10m.json')).json();
  const proj = d3.geoMercator().scale(100 * 180 / Math.PI).center([24, 42]).translate([0, 0]);
  proj.clipExtent([proj([6, 53]), proj([46, 29])]);
  const gp = geo => { const p = new Path2D(); d3.geoPath(proj, p)(geo); return p; };
  const geoms = world.objects.countries.geometries;
  const merged = (...names) => {
    const gs = geoms.filter(g => names.includes(g.properties.name));
    if (gs.length !== names.length) console.error('eksik ülke', names, gs.map(g => g.properties.name));
    return gp(topojson.merge(world, gs));
  };
  const P = {
    land: gp(topojson.feature(world, world.objects.land)),
    BG: merged('Bulgaria'), RS: merged('Serbia'), GR: merged('Greece'), ME: merged('Montenegro'),
    OTB: merged('Albania', 'Kosovo', 'Macedonia', 'Turkey'),
  };
  const poly = pts => {
    const p = new Path2D();
    pts.forEach(([lo, la], i) => { const [x, y] = proj([lo, la]); if (i) p.lineTo(x, y); else p.moveTo(x, y); });
    p.closePath(); return p;
  };
  const BIG = [-6000, -6000, 12000, 12000];
  const comp = (...paths) => { const p = new Path2D(); p.rect(...BIG); paths.forEach(q => p.addPath(q)); return p; };

  /* 1885 sınırları: bugünkü ülke şekilleri + elle çizilmiş (şematik) bölme çizgileri */
  const rumSouth = [[23.75, 42.02], [24.0, 41.9], [24.35, 41.85], [24.65, 41.72], [24.95, 41.62], [25.3, 41.6], [25.6, 41.6], [25.9, 41.7], [26.1, 41.83], [26.3, 41.93], [26.55, 41.97], [26.95, 42.05], [27.3, 42.12], [27.6, 42.2], [27.85, 42.22], [28.6, 42.25]];
  const rumNorth = [[23.75, 42.02], [23.72, 42.25], [23.72, 42.48], [23.95, 42.6], [24.25, 42.7], [24.35, 42.77], [24.6, 42.77], [24.95, 42.72], [25.32, 42.75], [25.9, 42.78], [26.3, 42.85], [26.6, 42.9], [26.9, 42.9], [27.3, 42.85], [27.6, 42.78], [27.9, 42.72], [28.6, 42.7]];
  const Z = {
    RUM: poly([...rumNorth, ...rumSouth.slice(1).reverse()]),
    BGO: poly([[22.3, 42.2], [22.52, 42.16], [22.8, 42.12], [23.07, 42.07], [23.4, 42.03], ...rumSouth, [28.6, 41.0], [22.3, 41.0]]),
    GR: poly([[19.5, 40.6], [19.9, 39.95], [19.97, 39.78], [20.05, 39.65], [20.12, 39.52], [20.18, 39.39], [20.3, 39.22], [20.45, 39.1], [20.6, 38.97], [20.745, 38.945], [20.8, 38.97], [20.95, 38.985], [21.03, 39.02], [20.95, 39.15], [21.02, 39.35], [21.15, 39.6], [21.3, 39.8], [21.8, 39.87], [22.2, 39.9], [22.45, 39.97], [22.72, 39.97], [23.6, 39.62], [24.3, 39.65], [24.9, 39.15], [25.2, 38.2], [25.75, 37.7], [26.2, 37.1], [26.15, 36.7], [26.05, 36.45], [25.9, 36.0], [24.8, 36.0], [23.55, 35.9], [23.45, 35.75], [23.2, 35.4], [23.2, 34.5], [30, 34.5], [30, 42.5], [19.5, 42.5]]),
    AH: poly([[18.9, 44.88], [19.37, 44.9], [19.6, 44.97], [19.72, 44.77], [19.95, 44.7], [20.2, 44.67], [20.44, 44.82], [20.62, 44.82], [20.8, 44.72], [20.93, 44.68], [21.15, 44.73], [21.33, 44.81], [21.36, 44.815], [21.6, 44.8], [22.5, 45.2], [22.5, 46.6], [18.6, 46.6]]),
    SAN: poly([[19.0, 43.62], [19.45, 43.72], [19.55, 43.68], [19.75, 43.6], [20.0, 43.5], [20.3, 43.42], [20.6, 43.3], [20.8, 43.27], [20.95, 43.1], [20.6, 42.75], [19.0, 42.75]]),
    PRE: poly([[21.3, 42.52], [21.7, 42.5], [21.95, 42.44], [22.25, 42.42], [22.25, 42.1], [21.3, 42.1]]),
    TSA: poly([[22.66, 43.19], [22.74, 43.02], [22.68, 42.9], [22.75, 42.84], [23.1, 42.84], [23.1, 43.2]]),
    BOS: poly([[22.3, 42.3], [22.28, 42.5], [22.36, 42.62], [22.75, 42.62], [22.75, 42.3]]),
    ME: poly([[18.7, 43.5], [18.84, 43.35], [19.1, 43.2], [19.35, 43.05], [19.58, 42.96], [19.72, 42.85], [19.86, 42.7], [19.8, 42.52], [19.9, 42.4], [20.6, 42.4], [20.6, 43.7], [18.7, 43.7]]),
  };
  const REG = {
    serbia: { base: P.RS, exc: comp(Z.AH, Z.SAN, Z.PRE, Z.TSA, Z.BOS), edges: [Z.AH, Z.SAN, Z.PRE, Z.TSA, Z.BOS] },
    bulg: { base: P.BG, exc: comp(Z.BGO), edges: [Z.BGO] },
    outl: [{ base: P.RS, inc: Z.TSA }, { base: P.RS, inc: Z.BOS }],
    rum: { base: P.BG, inc: Z.RUM },
    otto: [{ base: P.OTB }, { base: P.GR, inc: Z.GR }, { base: P.BG, inc: Z.BGO }, { base: P.RS, inc: Z.SAN }, { base: P.RS, inc: Z.PRE }, { base: P.ME, inc: Z.ME }],
  };
  const GRAT = new Path2D();
  for (let lo = 8; lo <= 44; lo += 2) { const a = proj([lo, 30]), b = proj([lo, 52]); GRAT.moveTo(a[0], a[1]); GRAT.lineTo(b[0], b[1]); }
  for (let la = 30; la <= 52; la += 2) { const a = proj([8, la]), b = proj([44, la]); GRAT.moveTo(a[0], a[1]); GRAT.lineTo(b[0], b[1]); }

  function clipReg(r) { ctx.clip(r.base); if (r.inc) ctx.clip(r.inc); if (r.exc) ctx.clip(r.exc, 'evenodd'); }
  function fillReg(r, style) { ctx.save(); clipReg(r); ctx.fillStyle = style; ctx.fillRect(...BIG); ctx.restore(); }
  function fillBleed(r, style, z) {
    ctx.save(); if (r.inc) ctx.clip(r.inc);
    ctx.fillStyle = style; ctx.fill(r.base);
    ctx.strokeStyle = style; ctx.lineWidth = 1.6 / z; ctx.lineJoin = 'round'; ctx.stroke(r.base);
    ctx.restore();
  }
  function strokeReg(r, style, w, z, glow) {
    ctx.save(); clipReg(r);
    ctx.strokeStyle = style; ctx.lineWidth = 2 * w / z; ctx.lineJoin = 'round';
    if (glow) { ctx.shadowColor = glow; ctx.shadowBlur = 20; }
    ctx.stroke(r.base); if (r.inc) ctx.stroke(r.inc); (r.edges || []).forEach(e => ctx.stroke(e));
    ctx.restore();
  }

  /* ---------- doku ve gren ---------- */
  const GRAIN = [];
  for (let k = 0; k < 8; k++) {
    const g = document.createElement('canvas'); g.width = 540; g.height = 960;
    const gx = g.getContext('2d'); const id = gx.createImageData(540, 960); const r = rng(1000 + k);
    for (let i = 0; i < id.data.length; i += 4) { const v = (r() * 255) | 0; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; }
    gx.putImageData(id, 0, 0); GRAIN.push(g);
  }
  const DUST = [];
  { const r = rng(77); for (let i = 0; i < 54; i++) DUST.push({ x: r() * W, y: r() * H, vx: -14 + r() * 28, vy: -34 + r() * 22, r: 0.8 + r() * 2.2, a: 0.05 + r() * 0.16, f: 0.6 + r() * 1.8, p: r() * TAU }); }
  const MOTTLE = document.createElement('canvas'); MOTTLE.width = 540; MOTTLE.height = 960;
  {
    const mx = MOTTLE.getContext('2d'); mx.fillStyle = '#808080'; mx.fillRect(0, 0, 540, 960);
    [[9, 16, 0.55, 11], [27, 48, 0.4, 12], [90, 160, 0.28, 13]].forEach(([w, h, a, seed]) => {
      const s = document.createElement('canvas'); s.width = w; s.height = h;
      const sx = s.getContext('2d'); const id = sx.createImageData(w, h); const r = rng(seed);
      for (let i = 0; i < id.data.length; i += 4) { const v = (r() * 255) | 0; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; }
      sx.putImageData(id, 0, 0);
      mx.globalAlpha = a; mx.imageSmoothingEnabled = true; mx.imageSmoothingQuality = 'high'; mx.drawImage(s, 0, 0, 540, 960);
    });
  }

  /* ---------- kamera ---------- */
  // [t, boylam, enlem, yakınlık, geçiş]
  const KEYS = [
    [0.0, 24.4, 42.0, 0.86, 'lin'],
    [3.2, 24.4, 42.0, 0.94, 'lin'],
    [4.6, 24.6, 42.1, 1.02, 'io'],
    [6.3, 25.75, 42.3, 1.8, 'io'],
    [9.3, 25.8, 42.3, 1.95, 'lin'],
    [10.5, 27.0, 41.72, 1.68, 'io'],
    [13.2, 27.1, 41.7, 1.8, 'lin'],
    [13.21, 22.7, 43.25, 2.15, 'lin'],
    [14.5, 22.7, 43.25, 2.2, 'lin'],
    [19.2, 22.72, 43.22, 2.5, 'lin'],
    [20.1, 22.95, 42.98, 3.5, 'io'],
    [23.7, 22.93, 42.98, 3.75, 'lin'],
    [25.0, 24.4, 42.1, 1.0, 'io'],
    [30.01, 24.4, 42.1, 1.1, 'lin'],
  ].map(k => { const [x, y] = proj([k[1], k[2]]); return { t: k[0], x, y, lz: Math.log(k[3]), e: k[4] }; });
  function cam(t) {
    let i = 1; while (i < KEYS.length - 1 && KEYS[i].t < t) i++;
    const a = KEYS[i - 1], b = KEYS[i];
    let u = prog(t, a.t, b.t); if (b.e === 'io') u = eIO(u);
    return { x: lerp(a.x, b.x, u), y: lerp(a.y, b.y, u), z: Math.exp(lerp(a.lz, b.lz, u)) };
  }
  const HITS = [[0.3, 10], [1.55, 12], [7.0, 7], [9.9, 5], [13.2, 20], [13.55, 14], [14.5, 8], [17.5, 8], [19.6, 9], [19.9, 12], [20.5, 10], [20.8, 10], [22.0, 13], [24.9, 9], [25.3, 14]];
  function shake(t) {
    let dx = 0, dy = 0;
    HITS.forEach(([t0, amp], i) => {
      const d = t - t0; if (d < 0 || d > 0.7) return;
      const e = amp * Math.exp(-d * 8);
      dx += e * Math.sin(d * 71 + i * 1.7); dy += e * Math.cos(d * 63 + i * 2.3);
    });
    return [dx, dy];
  }
  let CAM = { x: 0, y: 0, z: 1, sx: 0, sy: 0 };
  const S = (lon, lat) => { const [px, py] = proj([lon, lat]); return [W / 2 + CAM.sx + (px - CAM.x) * CAM.z, H / 2 + CAM.sy + (py - CAM.y) * CAM.z]; };

  /* ---------- yazı ---------- */
  function fontOf(o, size) { return `${o.it ? 'italic ' : ''}${o.w || 400} ${size}px ${FAM[o.f || 'disp']}`; }
  function fit(s, o, maxW) {
    ctx.save(); ctx.font = fontOf(o, 100); ctx.letterSpacing = ((o.ls || 0) * 100) + 'px';
    const w = ctx.measureText(s).width; ctx.restore();
    return Math.min(o.size, 100 * maxW / w);
  }
  function txt(s, x, y, o) {
    const a = o.a === undefined ? 1 : o.a; if (a <= 0.004) return;
    ctx.save();
    ctx.globalAlpha = a; ctx.translate(x, y);
    const sc = o.sc || 1; if (sc !== 1) ctx.scale(sc, sc);
    ctx.font = fontOf(o, o.size);
    const ls = (o.ls || 0) * o.size; ctx.letterSpacing = ls + 'px';
    ctx.textAlign = o.align || 'center'; ctx.textBaseline = 'alphabetic';
    if (o.blur > 0.4) ctx.filter = `blur(${o.blur.toFixed(1)}px)`;
    if (o.sh !== 0) { ctx.shadowColor = `rgba(0,0,0,${o.sh === undefined ? 0.85 : o.sh})`; ctx.shadowBlur = o.shb || 26; ctx.shadowOffsetY = 3; }
    ctx.fillStyle = o.color || C.white;
    ctx.fillText(s, ctx.textAlign === 'center' ? ls / 2 : 0, 0);
    ctx.restore();
  }
  // kind: slam | rise | fade | track
  function line(t, s, x, y, o, tin, tout, kind, maxW) {
    if (t < tin || t > tout) return;
    const size = maxW ? fit(s, o, maxW) : o.size;
    let a = 1, sc = 1, dy = 0, blur = 0, ls = o.ls || 0;
    if (kind === 'slam') { const p = prog(t, tin, tin + 0.28), e = eOutExpo(p); sc = lerp(1.75, 1, e); a = clamp(p * 4); blur = (1 - e) * 14; }
    else if (kind === 'rise') { const p = eOut3(prog(t, tin, tin + 0.55)); dy = (1 - p) * 34; a = p; }
    else if (kind === 'track') { const p = eOut3(prog(t, tin, tin + 0.8)); a = p; ls += (1 - p) * 0.3; }
    else { a = eOut3(prog(t, tin, tin + 0.6)); }
    const q = prog(t, tout - 0.3, tout); a *= 1 - q; sc *= 1 + 0.05 * eIn2(q);
    sc *= 1 + 0.012 * prog(t, tin, tout);          // hafif süzülme
    txt(s, x, y + dy, { ...o, size, a: a * (o.a === undefined ? 1 : o.a), sc, blur, ls });
  }

  /* ---------- harita üstü öğeler ---------- */
  const bez = (A, Cc, B, u) => { const a = (1 - u) * (1 - u), b = 2 * (1 - u) * u, d = u * u; return [a * A[0] + b * Cc[0] + d * B[0], a * A[1] + b * Cc[1] + d * B[1]]; };
  function arrow(ll, p, w, color, alpha, glow) {
    if (p <= 0.03 || alpha <= 0.01) return;
    const A = S(...ll[0]), Cc = S(...ll[1]), B = S(...ll[2]);
    let L = 0, prev = A;
    for (let i = 1; i <= 24; i++) { const q = bez(A, Cc, B, p * i / 24); L += Math.hypot(q[0] - prev[0], q[1] - prev[1]); prev = q; }
    const hl = Math.min(w * 3.0, L * 0.6), pb = p * (1 - hl / Math.max(L, 1));
    const N = 30, Lp = [], Rp = [];
    for (let i = 0; i <= N; i++) {
      const u = pb * i / N, q = bez(A, Cc, B, u), q2 = bez(A, Cc, B, Math.min(1, u + 0.01));
      let dx = q2[0] - q[0], dy = q2[1] - q[1]; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
      const hw = w * (0.12 + 0.88 * Math.pow(i / N, 0.8)) * 0.5;
      Lp.push([q[0] - dy * hw, q[1] + dx * hw]); Rp.push([q[0] + dy * hw, q[1] - dx * hw]);
    }
    const neck = bez(A, Cc, B, pb), tip = bez(A, Cc, B, p);
    let dx = tip[0] - neck[0], dy = tip[1] - neck[1]; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    const hw = w * 1.25;
    ctx.save(); ctx.globalAlpha = alpha;
    const g = ctx.createLinearGradient(A[0], A[1], tip[0], tip[1]);
    g.addColorStop(0, rgba(color, 0.1)); g.addColorStop(0.55, rgba(color, 0.9)); g.addColorStop(1, rgba(color, 1));
    ctx.fillStyle = g; if (glow) { ctx.shadowColor = glow; ctx.shadowBlur = 26; }
    ctx.beginPath(); ctx.moveTo(Lp[0][0], Lp[0][1]);
    for (const q of Lp) ctx.lineTo(q[0], q[1]);
    ctx.lineTo(neck[0] - dy * hw, neck[1] + dx * hw); ctx.lineTo(tip[0], tip[1]); ctx.lineTo(neck[0] + dy * hw, neck[1] - dx * hw);
    for (let i = N; i >= 0; i--) ctx.lineTo(Rp[i][0], Rp[i][1]);
    ctx.closePath(); ctx.fill(); ctx.restore();
  }
  function city(lon, lat, name, a, o = {}) {
    if (a <= 0.01) return;
    const [x, y] = S(lon, lat);
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = o.color || C.white;
    ctx.shadowColor = 'rgba(0,0,0,.9)'; ctx.shadowBlur = 8;
    ctx.beginPath(); ctx.arc(x, y, o.r || 6, 0, TAU); ctx.fill();
    ctx.shadowBlur = 0; ctx.strokeStyle = 'rgba(0,0,0,.65)'; ctx.lineWidth = 2; ctx.stroke(); ctx.restore();
    const side = o.side || 1;
    txt(name, x + side * 15, y + (o.dy === undefined ? 10 : o.dy), { f: 'sans', w: 500, size: o.size || 28, ls: 0.05, color: o.color || C.white, align: side > 0 ? 'left' : 'right', a, sh: 0.95, shb: 10 });
  }
  function mlabel(lon, lat, s, o) {
    const [x, y] = S(lon, lat);
    txt(s, x, y, { f: 'sans', w: 500, size: 26, ls: 0.32, color: C.white, sh: 0.9, shb: 12, ...o });
  }
  function burst(lon, lat, t, t0, seed, k = 1) {
    const e = prog(t, t0, t0 + 0.75); if (e <= 0 || e >= 1) return;
    const [x, y] = S(lon, lat); const r = rng(seed); const a = 1 - e;
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    const R = 150 * k * (0.35 + 0.65 * eOut3(e));
    const g = ctx.createRadialGradient(x, y, 0, x, y, R);
    g.addColorStop(0, `rgba(255,236,190,${a})`); g.addColorStop(0.35, `rgba(255,120,40,${a * 0.55})`); g.addColorStop(1, 'rgba(255,60,20,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, R, 0, TAU); ctx.fill();
    ctx.strokeStyle = `rgba(255,214,150,${a * 0.9})`; ctx.lineWidth = 1 + 6 * a;
    ctx.beginPath(); ctx.arc(x, y, (16 + 125 * eOut3(e)) * k, 0, TAU); ctx.stroke();
    ctx.lineCap = 'round';
    for (let i = 0; i < 16; i++) {
      const ang = r() * TAU, d0 = (14 + r() * 26) * k, d1 = d0 + (50 + r() * 120) * k * eOut3(e);
      ctx.strokeStyle = `rgba(255,${180 + (r() * 60 | 0)},110,${a * 0.9})`; ctx.lineWidth = 1.5 + r() * 2.5;
      ctx.beginPath(); ctx.moveTo(x + Math.cos(ang) * lerp(d0, d1, 0.55), y + Math.sin(ang) * lerp(d0, d1, 0.55));
      ctx.lineTo(x + Math.cos(ang) * d1, y + Math.sin(ang) * d1); ctx.stroke();
    }
    ctx.restore();
  }
  function swords(x, y, a, s = 1) {
    if (a <= 0.01) return;
    ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s); ctx.lineCap = 'round';
    ctx.shadowColor = 'rgba(0,0,0,.95)'; ctx.shadowBlur = 12;
    for (const sg of [-1, 1]) {
      ctx.save(); ctx.rotate(sg * Math.PI / 4);
      ctx.strokeStyle = C.white; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, 22); ctx.lineTo(0, -28); ctx.stroke();
      ctx.strokeStyle = C.gold; ctx.lineWidth = 4.5; ctx.beginPath(); ctx.moveTo(-9, 13); ctx.lineTo(9, 13); ctx.stroke();
      ctx.restore();
    }
    ctx.restore();
  }

  const A_MAIN = [[22.0, 43.31], [22.55, 43.24], [22.95, 42.89]];
  const A_NORTH = [[22.28, 43.86], [22.5, 44.06], [22.82, 43.98]];
  const A_SOUTH = [[22.25, 42.98], [22.55, 42.76], [22.88, 42.76]];
  const A_BACK = [[22.99, 42.88], [22.9, 43.1], [22.62, 43.13]];

  /* ---------- harita ---------- */
  function drawMap(t) {
    const z = CAM.z;
    const g = ctx.createRadialGradient(W / 2, H / 2, 60, W / 2, H / 2, 1250);
    g.addColorStop(0, '#0b1219'); g.addColorStop(1, '#04070a');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);

    ctx.save();
    ctx.translate(W / 2 + CAM.sx, H / 2 + CAM.sy); ctx.scale(z, z); ctx.translate(-CAM.x, -CAM.y);
    ctx.strokeStyle = 'rgba(160,190,220,0.055)'; ctx.lineWidth = 1 / z; ctx.stroke(GRAT);
    ctx.fillStyle = C.land; ctx.fill(P.land);

    // Sırbistan
    const kS = 0.8 * prog(t, 14.5, 15.0) * (1 - 0.7 * prog(t, 21.7, 22.6)) + 0.12 * (t >= 14.5 && t < 21.7 ? Math.sin((t - 14.5) * 3.2) : 0);
    fillReg(REG.serbia, mix(C.rs, C.rsHi, kS));
    // Bulgaristan Prensliği
    const kB = 0.22 * prog(t, 19.3, 20.0) + 0.4 * Math.exp(-Math.max(0, t - 22.0) * 2.2) * (t >= 22.0 ? 1 : 0);
    const colB = mix(C.bg, C.bgHi, kB);
    fillReg(REG.bulg, colB); REG.outl.forEach(r => fillReg(r, colB));

    // Doğu Rumeli
    const w = eIO(prog(t, 6.8, 8.0));
    const hi = prog(t, 4.2, 5.0);
    if (w < 1) {
      const pulse = 0.5 + 0.5 * Math.sin((t - 4.2) * 4.4);
      fillReg(REG.rum, mix(C.otto, C.ottoHi, 0.25 + hi * (0.5 + 0.25 * pulse)));
      ctx.save(); clipReg(REG.rum); ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.strokeStyle = rgba(C.gold, 0.1 + 0.2 * hi); ctx.lineWidth = 2; ctx.beginPath();
      for (let k = -H; k < W + H; k += 18) { ctx.moveTo(k, 0); ctx.lineTo(k + H * 0.6, H); }
      ctx.stroke(); ctx.restore();
    }
    if (w > 0) {
      const f = lerp(23.0, 28.9, w);
      const wl = (ff) => poly([[10, 40], [ff - 1.15, 40], [ff + 1.35, 45], [10, 45]]);
      const settle = prog(t, 8.0, 9.6), uni = prog(t, 24.2, 25.4);
      const colR = uni > 0 ? mix(C.bgHi, C.bg, lerp(0.62, 1, uni)) : mix(C.bgHi, C.bg, 0.62 * settle);
      ctx.save(); ctx.clip(wl(f)); fillReg(REG.rum, uni >= 1 ? colB : colR); ctx.restore();
      if (w < 1) {
        const band = new Path2D(); band.addPath(wl(f + 0.03));
        ctx.save(); ctx.clip(band); ctx.clip(comp(wl(f - 0.09)), 'evenodd');
        ctx.globalCompositeOperation = 'lighter'; fillReg(REG.rum, 'rgba(255,232,180,0.6)'); ctx.restore();
      }
    }

    // Osmanlı
    const dimO = 0.55 * prog(t, 9.4, 10.6) * (1 - 0.5 * prog(t, 23.8, 24.6));
    const revO = 0.45 * (1 - prog(t, 3.2, 4.6));
    const colO = revO > 0 ? mix(C.otto, C.ottoHi, revO) : mix(C.otto, C.ottoDim, dimO);
    REG.otto.forEach(r => fillBleed(r, colO, z));

    // kıyı ve sınırlar
    ctx.strokeStyle = rgba(C.coast, 0.24); ctx.lineWidth = 1.1 / z; ctx.lineJoin = 'round'; ctx.stroke(P.land);
    strokeReg(REG.serbia, rgba(C.blue, 0.22 + 0.55 * clamp(kS)), 1.3, z);
    strokeReg(REG.bulg, rgba(C.green, 0.3 + 0.3 * kB), 1.2, z); REG.outl.forEach(r => strokeReg(r, rgba(C.green, 0.3), 1.2, z));
    const uniA = 1 - prog(t, 24.2, 25.4);
    if (uniA > 0.01) {
      if (w < 0.5) strokeReg(REG.rum, rgba(C.gold, 0.35 + 0.65 * hi), 1.2 + 1.3 * hi, z, hi > 0.2 ? rgba(C.gold, 0.9) : null);
      else strokeReg(REG.rum, mix(C.gold, C.green, prog(t, 7.6, 9.4), (0.95 - 0.5 * prog(t, 8.2, 9.6)) * uniA), 2.0, z, t < 9.2 ? rgba(C.green, 0.8) : null);
    }
    ctx.restore();

    // doku
    ctx.save(); ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = 0.55;
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(MOTTLE, 0, 0, W, H); ctx.restore();

    /* --- etiketler, oklar --- */
    const win = (a, b, fi = 0.5, fo = 0.4) => prog(t, a, a + fi) * (1 - prog(t, b - fo, b));
    // genel görünüm etiketleri
    const ov = win(3.5, 6.0);
    mlabel(23.7, 41.02, 'OSMANLI DEVLETİ', { size: 30, a: 0.92 * ov, color: '#f1d9cf' });
    mlabel(25.3, 43.32, 'BULGARİSTAN PRENSLİĞİ', { size: 22, a: 0.8 * ov, color: C.green });
    mlabel(21.05, 43.95, 'SIRBİSTAN', { size: 22, a: 0.8 * ov, color: C.blue });
    mlabel(26.5, 44.3, 'ROMANYA', { size: 19, a: 0.4 * ov });
    // Doğu Rumeli
    const ra = win(4.5, 13.1);
    mlabel(25.95, 42.52, 'DOĞU RUMELİ', { size: lerp(22, 34, prog(t, 4.6, 6.3)), a: ra * (t < 8 ? 1 : 0.75), color: t < 7.4 ? C.gold : C.white });
    city(24.75, 42.14, 'Filibe', win(5.0, 13.1), { side: 1 });
    city(23.32, 42.70, 'Sofya', win(5.4, 9.2) * 0.8, { side: -1, size: 24, r: 5 });
    // İstanbul sahnesi
    const ia = win(9.9, 13.15);
    if (ia > 0) {
      const [ix, iy] = S(28.98, 41.01);
      const ph = ((t - 9.9) % 1.6) / 1.6;
      ctx.save(); ctx.strokeStyle = rgba(C.gold, 0.7 * (1 - ph) * ia); ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(ix, iy, 10 + 46 * ph, 0, TAU); ctx.stroke(); ctx.restore();
      city(28.98, 41.01, 'İSTANBUL', ia, { side: -1, size: 32, r: 8, color: C.gold });
      city(26.56, 41.68, 'Edirne', ia * 0.9, { side: 1, size: 25, r: 5, dy: 34 });
      // hiç başlamayan harekât: kesik çizgi sınırda durur ve söner
      const A = S(26.56, 41.68), B = S(24.9, 42.1), Cc = S(25.9, 42.05);
      const go = eOut3(prog(t, 10.5, 11.5)) * 0.3, fade = 1 - prog(t, 12.3, 13.0);
      ctx.save(); ctx.lineCap = 'round';
      ctx.setLineDash([3, 13]); ctx.strokeStyle = `rgba(244,239,228,${0.34 * ia})`; ctx.lineWidth = 3;
      ctx.beginPath(); for (let i = 0; i <= 40; i++) { const q = bez(A, Cc, B, i / 40); if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); } ctx.stroke();
      if (go > 0.01 && fade > 0) {
        ctx.setLineDash([16, 12]); ctx.strokeStyle = `rgba(244,239,228,${0.95 * fade})`; ctx.lineWidth = 6;
        ctx.shadowColor = 'rgba(255,255,255,.6)'; ctx.shadowBlur = 12;
        ctx.beginPath(); for (let i = 0; i <= 30; i++) { const q = bez(A, Cc, B, go * i / 30); if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); } ctx.stroke();
        const q = bez(A, Cc, B, go); const xa = prog(t, 11.45, 11.7) * fade;
        ctx.setLineDash([]); ctx.strokeStyle = rgba(C.red, xa); ctx.lineWidth = 7; ctx.shadowColor = 'rgba(0,0,0,.9)';
        ctx.beginPath(); ctx.moveTo(q[0] - 18, q[1] - 18); ctx.lineTo(q[0] + 18, q[1] + 18); ctx.moveTo(q[0] + 18, q[1] - 18); ctx.lineTo(q[0] - 18, q[1] + 18); ctx.stroke();
      }
      ctx.restore();
    }
    // savaş sahneleri
    if (t >= 14.5 && t < 24.6) {
      const wa = win(14.6, 24.4, 0.4, 0.5);
      mlabel(21.45, 43.72, 'SIRBİSTAN', { size: 30, a: 0.85 * wa * (1 - prog(t, 19.3, 20.0)), color: C.blue });
      mlabel(24.05, 43.32, 'BULGARİSTAN', { size: 30, a: 0.85 * wa * (1 - prog(t, 19.3, 20.0)), color: C.green });
      // Bulgar savunma hattı
      const dl = eOut3(prog(t, 19.5, 20.0));
      if (dl > 0) {
        const A = S(23.09, 43.0), Cc = S(22.98, 42.87), B = S(23.08, 42.74);
        ctx.save(); ctx.strokeStyle = rgba(C.green, 0.95 * wa); ctx.lineWidth = 9; ctx.lineCap = 'round';
        ctx.shadowColor = rgba(C.green, 0.9); ctx.shadowBlur = 22;
        ctx.beginPath(); for (let i = 0; i <= 24; i++) { const q = bez(A, Cc, B, dl * i / 24); if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); } ctx.stroke(); ctx.restore();
      }
      // Sırp ilerleyişi
      const ret = prog(t, 21.0, 21.9);
      const sa = wa * (1 - 0.85 * ret), sp = 1 - 0.3 * eIO(ret);
      arrow(A_NORTH, eOut3(prog(t, 15.55, 17.1)) * sp, 22, C.blue, sa, 'rgba(120,170,255,.8)');
      arrow(A_SOUTH, eOut3(prog(t, 15.7, 17.3)) * sp, 22, C.blue, sa, 'rgba(120,170,255,.8)');
      arrow(A_MAIN, eOut3(prog(t, 15.3, 17.0)) * sp, 34, C.blue, sa, 'rgba(120,170,255,.9)');
      // Bulgar karşı taarruzu
      arrow(A_BACK, eOut3(prog(t, 21.2, 22.3)), 34, C.green, wa, 'rgba(120,255,170,.9)');
      city(21.90, 43.32, 'Niş', wa, { side: -1 });
      city(22.59, 43.15, 'Pirot', wa, { side: -1, dy: 46 });
      city(23.32, 42.70, 'Sofya', wa, { side: 1, color: C.green });
      city(22.87, 43.99, 'Vidin', wa * (1 - prog(t, 19.3, 20.0)), { side: 1 });
      // Slivnitsa
      const sl = win(19.5, 24.4, 0.3, 0.5);
      const [sx, sy] = S(23.03, 42.85);
      swords(sx, sy, sl, lerp(2.2, 1.15, eOutExpo(prog(t, 19.5, 19.9))));
      txt('Slivnitsa', sx + 46, sy - 20, { f: 'sans', w: 600, size: 34, ls: 0.05, color: C.gold, align: 'left', a: sl, sh: 0.95, shb: 10 });
      burst(22.96, 42.88, t, 19.9, 71, 1.15); burst(22.9, 42.95, t, 20.5, 72, 0.95); burst(22.98, 42.79, t, 20.8, 73, 1.05); burst(22.93, 42.9, t, 21.4, 74, 0.8);
    }
    // son görünüm
  }

  /* ---------- katmanlar ---------- */
  function scrims(top, bot) {
    if (top > 0) {
      const g = ctx.createLinearGradient(0, 0, 0, 860);
      g.addColorStop(0, `rgba(3,5,8,${0.95 * top})`); g.addColorStop(0.5, `rgba(3,5,8,${0.7 * top})`); g.addColorStop(1, 'rgba(3,5,8,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, 860);
    }
    if (bot > 0) {
      const g = ctx.createLinearGradient(0, 1060, 0, H);
      g.addColorStop(0, 'rgba(3,5,8,0)'); g.addColorStop(0.42, `rgba(3,5,8,${0.72 * bot})`); g.addColorStop(1, `rgba(3,5,8,${0.97 * bot})`);
      ctx.fillStyle = g; ctx.fillRect(0, 1060, W, H - 1060);
    }
  }
  function glow(x, y, r, color, a) {
    if (a <= 0.004) return;
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, rgba(color, a)); g.addColorStop(1, rgba(color, 0));
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g; ctx.fillRect(x - r, y - r, 2 * r, 2 * r); ctx.restore();
  }
  const hit = (t, t0, k = 6) => (t >= t0 ? Math.exp(-(t - t0) * k) : 0);

  function texts(t) {
    const cx = W / 2;
    const small = { f: 'sans', w: 500, size: 40, ls: 0.3, color: C.gold };
    const it = { f: 'serif', w: 500, it: 1, size: 54, color: C.white };

    /* 0 — kanca */
    if (t < 3.3) {
      glow(cx, 900, 900, '#8a1010', 0.1 + 0.22 * hit(t, 0.3, 2.5) + 0.38 * hit(t, 1.55, 1.6));
      const d = { f: 'disp', size: 215, color: C.white };
      line(t, 'TOPRAK', cx, 640, d, 0.30, 3.25, 'slam', 900);
      line(t, 'BİZİMDİ.', cx, 868, d, 0.52, 3.25, 'slam', 900);
      const r = { ...d, color: C.red };
      line(t, 'SAVAŞAN', cx, 1128, r, 1.55, 3.25, 'slam', 900);
      line(t, 'BİZ DEĞİLDİK.', cx, 1318, r, 1.80, 3.25, 'slam', 900);
    }
    /* 1a — Doğu Rumeli */
    line(t, 'EYLÜL 1885', cx, 318, small, 3.5, 6.3, 'track');
    line(t, 'DOĞU RUMELİ', cx, 494, { f: 'disp', size: 132 }, 3.8, 6.3, 'slam', 920);
    line(t, 'Osmanlı’ya bağlı özerk vilayet', cx, 578, it, 4.3, 6.3, 'rise', 900);
    /* 1b — ilhak */
    line(t, '18 EYLÜL 1885 · FİLİBE', cx, 318, small, 6.4, 9.3, 'track');
    line(t, 'BULGARİSTAN', cx, 1262, { f: 'disp', size: 124, color: C.green }, 7.0, 9.3, 'slam', 840);
    line(t, 'İLHAK ETTİ.', cx, 1390, { f: 'disp', size: 124 }, 7.2, 9.3, 'slam', 840);
    line(t, 'Tek kurşun atılmadan.', cx, 1470, it, 7.9, 9.3, 'rise', 840);
    /* 2 — İstanbul */
    line(t, 'İSTANBUL SUSTU.', cx, 480, { f: 'disp', size: 150 }, 9.9, 13.1, 'slam', 920);
    line(t, 'Tek asker sınırı geçmedi.', cx, 1400, { ...it, size: 60 }, 11.3, 13.1, 'rise', 840);
    /* 3 — tarih kartı */
    if (t >= 13.2 && t < 14.5) {
      const out = 1 - prog(t, 14.38, 14.5);
      ctx.save(); ctx.globalAlpha = out; ctx.fillStyle = '#030406'; ctx.fillRect(0, 0, W, H); ctx.restore();
      glow(cx, 1000, 950, '#a01212', (0.16 + 0.5 * hit(t, 13.2, 3) + 0.4 * hit(t, 13.55, 3)) * out);
      line(t, 'SIRP–BULGAR SAVAŞI', cx, 690, { ...small, size: 38 }, 13.25, 14.5, 'track');
      line(t, '13 KASIM', cx, 960, { f: 'disp', size: 270 }, 13.2, 14.5, 'slam', 900);
      line(t, '1885', cx, 1250, { f: 'disp', size: 320, color: C.red }, 13.55, 14.5, 'slam', 900);
    }
    /* 3 — Sırbistan */
    line(t, '13 KASIM 1885', cx, 318, small, 14.6, 19.2, 'track');
    line(t, 'SIRBİSTAN', cx, 488, { f: 'disp', size: 128, color: C.blue }, 14.8, 19.2, 'slam', 920);
    line(t, 'SAVAŞ İLAN ETTİ.', cx, 612, { f: 'disp', size: 112 }, 15.1, 19.2, 'slam', 920);
    line(t, 'Bizim toprağımız yüzünden', cx, 1345, it, 16.9, 19.2, 'rise', 840);
    line(t, 'BİZ DEĞİL, ONLAR SAVAŞTI.', cx, 1455, { f: 'disp', size: 96 }, 17.5, 19.2, 'slam', 840);
    /* 4 — Slivnitsa */
    line(t, '17–19 KASIM 1885', cx, 318, small, 19.6, 23.7, 'track');
    line(t, 'SLİVNİTSA', cx, 504, { f: 'disp', size: 150 }, 19.6, 23.7, 'slam', 920);
    line(t, 'SIRBİSTAN İKİ HAFTADA', cx, 1290, { f: 'sans', w: 600, size: 62, ls: 0.07 }, 21.6, 23.7, 'rise', 840);
    line(t, 'YENİLDİ.', cx, 1468, { f: 'disp', size: 185, color: C.red }, 22.0, 23.7, 'slam', 840);
    /* 5 — hüküm */
    line(t, 'OSMANLI İSE', cx, 800, { f: 'disp', size: 124 }, 24.3, 26.9, 'slam', 920);
    line(t, 'SAVAŞMADAN', cx, 1010, { f: 'disp', size: 200, color: C.red }, 24.9, 26.9, 'slam', 920);
    line(t, 'KAYBETTİ.', cx, 1218, { f: 'disp', size: 200, color: C.red }, 25.3, 26.9, 'slam', 920);
    /* 6 — kapanış */
    if (t >= 27.0) {
      glow(cx, 960, 800, '#7a5a16', 0.2 * prog(t, 27.1, 28.2));
      const p = prog(t, 27.2, 28.0), e = eOutExpo(p);
      const g = ctx.createLinearGradient(0, 700, 0, 1020); g.addColorStop(0, '#f6dc94'); g.addColorStop(1, '#b98a30');
      txt('560', cx, 1010, { f: 'disp', size: 400, color: g, a: clamp(p * 3), sc: lerp(1.3, 1, e) * (1 + 0.02 * prog(t, 27.2, 30)), blur: (1 - e) * 16 });
      const lw = 460 * eOut3(prog(t, 27.7, 28.5));
      ctx.fillStyle = rgba(C.gold, 0.9); ctx.fillRect(cx - lw / 2, 1068, lw, 3);
      line(t, 'YIL RUMELİ', cx, 1168, { f: 'sans', w: 500, size: 66, ls: 0.4 }, 27.75, 31, 'track');
      line(t, '1885 · SIRP–BULGAR SAVAŞI', cx, 1262, { f: 'sans', w: 500, size: 30, ls: 0.28, color: C.gold, a: 0.75 }, 28.3, 31, 'fade');
    }
    /* marka */
    const ba = prog(t, 3.5, 4.2) * (1 - prog(t, 26.6, 27.0)) * 0.72;
    if (ba > 0.01) {
      txt('560 YIL RUMELİ', cx, 252, { f: 'sans', w: 500, size: 24, ls: 0.46, color: C.gold, a: ba, shb: 8 });
      ctx.fillStyle = rgba(C.gold, ba * 0.7); ctx.fillRect(cx - 250, 243, 60, 2); ctx.fillRect(cx + 190, 243, 60, 2);
    }
  }

  function post(t) {
    // parlamalar
    const fl = 0.34 * hit(t, 0.3, 11) + 0.34 * hit(t, 1.55, 11) + 0.22 * hit(t, 7.0, 10) + 0.55 * hit(t, 13.2, 9) + 0.4 * hit(t, 13.55, 10)
      + 0.5 * hit(t, 14.5, 9) + 0.22 * hit(t, 17.5, 11) + 0.3 * hit(t, 19.6, 10) + 0.3 * hit(t, 22.0, 10) + 0.3 * hit(t, 24.9, 11) + 0.42 * hit(t, 25.3, 9);
    if (fl > 0.004) { ctx.fillStyle = `rgba(255,236,224,${Math.min(0.75, fl)})`; ctx.fillRect(0, 0, W, H); }
    // toz zerreleri
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (const d of DUST) {
      const x = ((d.x + d.vx * t) % (W + 80) + (W + 80)) % (W + 80) - 40;
      const y = ((d.y + d.vy * t) % (H + 80) + (H + 80)) % (H + 80) - 40;
      const a = d.a * (0.55 + 0.45 * Math.sin(t * d.f + d.p));
      ctx.fillStyle = `rgba(255,226,190,${a.toFixed(3)})`;
      ctx.beginPath(); ctx.arc(x, y, d.r, 0, TAU); ctx.fill();
    }
    ctx.restore();
    // vinyet
    const g = ctx.createRadialGradient(W / 2, H / 2, 520, W / 2, H / 2, 1220);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.78)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    // gren
    ctx.save(); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = 0.085;
    ctx.imageSmoothingEnabled = true; ctx.drawImage(GRAIN[Math.round(t * FPS) % GRAIN.length], 0, 0, W, H); ctx.restore();
    // açılış / kapanış
    const edge = 1 - prog(t, 0, 0.25) + prog(t, 29.6, 30);
    if (edge > 0.004) { ctx.fillStyle = `rgba(0,0,0,${clamp(edge)})`; ctx.fillRect(0, 0, W, H); }
  }

  function renderAt(t) {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.shadowBlur = 0; ctx.shadowColor = 'transparent'; ctx.setLineDash([]);
    ctx.fillStyle = '#030406'; ctx.fillRect(0, 0, W, H);

    const c = cam(t), sh = shake(t);
    CAM = { x: c.x, y: c.y, z: c.z, sx: sh[0], sy: sh[1] };
    if (window.DEBUG) { drawMap(t); return; }
    // harita görünürlüğü: kancada silik, sonra tam; kapanışta söner
    const mv = t < 2.9 ? 0.3 * prog(t, 1.7, 2.9) : lerp(0.3, 1, prog(t, 2.9, 3.6)) * (1 - prog(t, 26.7, 27.05));
    if (mv > 0.004 && !(t >= 13.26 && t < 14.38)) {
      drawMap(t);
      const top = prog(t, 3.2, 3.8) * (1 - prog(t, 23.8, 24.3)), bot = 0.9 * top;
      scrims(top, bot);
      const dim = Math.max(1 - mv, 0.6 * prog(t, 24.0, 24.6) * (t < 27.05 ? 1 : 0));
      if (dim > 0.004) { ctx.fillStyle = `rgba(3,4,6,${dim})`; ctx.fillRect(0, 0, W, H); }
    }
    texts(t);
    post(t);
  }

  window.renderAt = renderAt;
  window.FILM = { W, H, DUR, FPS };
  window.READY = true;
})().catch(e => { console.error('FILM HATASI', e && e.stack || e); window.FAILED = String(e && e.stack || e); });
