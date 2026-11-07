"""Son dönem yaması: verilen semboller için 2026-10-01..2026-11-06 dakika mumları (günlük dosyalar)."""
import os, sys, time, requests, datetime as dt
S = sys.argv[1]; syms = sys.argv[2].split(",")
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
d0, d1 = dt.date(2026, 10, 1), dt.date(2026, 11, 6)
for sym in syms:
    D = f"{S}/data/duka_m/{sym}"; os.makedirs(D, exist_ok=True)
    d = d0
    while d <= d1:
        if d.weekday() < 5 or d.weekday() == 6:
            fn = f"{D}/{d:%Y%m%d}.bi5"
            if not os.path.exists(fn):
                url = f"https://datafeed.dukascopy.com/datafeed/{sym}/{d.year}/{d.month-1:02d}/{d.day:02d}/BID_candles_min_1.bi5"
                for att in range(5):
                    try:
                        r = s.get(url, timeout=45)
                        if r.status_code in (200, 404):
                            open(fn, "wb").write(r.content if r.status_code == 200 else b""); break
                    except Exception:
                        s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
                    time.sleep(2 * 2 ** att)
        d += dt.timedelta(days=1)
    print("done", sym, flush=True)
