"""Dukascopy BID saatlik mum indirici, tek enstrüman, tek bağlantı (keep-alive). Ay indeksi 0 tabanlı. Kayıt: (saniye_ofset, open, close, low, high, volume) big-endian >iiiiif."""
import os, sys, time, requests
S, sym, y0, m0 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
D = f"{S}/data/duka_h/{sym}"; os.makedirs(D, exist_ok=True)
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
jobs = [(y, m) for y in range(y0, 2027) for m in range(12) if (y, m) >= (y0, m0) and (y, m) <= (2026, 9)]
jobs = jobs[::-1]  # en yeniden eskiye
fails = []
for i, (y, m) in enumerate(jobs):
    fn = f"{D}/{y}_{m:02d}.bi5"
    if os.path.exists(fn): continue
    url = f"https://datafeed.dukascopy.com/datafeed/{sym}/{y}/{m:02d}/BID_candles_hour_1.bi5"
    done = False
    for att in range(6):
        try:
            r = s.get(url, timeout=45)
            if r.status_code == 200:
                open(fn + ".part", "wb").write(r.content); os.replace(fn + ".part", fn); done = True; break
            if r.status_code == 404:
                open(fn, "wb").write(b""); done = True; break
        except Exception:
            s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
        time.sleep(2 * 2 ** att)
    if not done: fails.append((y, m))
    if i % 20 == 0: print(sym, i, len(jobs), y, m, flush=True)
print("DONE", sym, "fails", fails, flush=True)
