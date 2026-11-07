import os, sys, time, requests, datetime as dt, random
S, sym = sys.argv[1], sys.argv[2]
D = f"{S}/data/duka_m/{sym}"; os.makedirs(D, exist_ok=True)
random.seed(7)
days = []
d = dt.date(2017, 3, 6)
while d <= dt.date(2026, 10, 30):
    if d.weekday() < 5: days.append(d)
    d += dt.timedelta(days=1)
# 2017-2026 her yıldan ~16 gün + son 60 iş günü tam
sample = sorted(set(random.sample(days[:-60], 150) + days[-60:]))
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
for i, d in enumerate(sample):
    fn = f"{D}/{d:%Y%m%d}.bi5"
    if os.path.exists(fn): continue
    url = f"https://datafeed.dukascopy.com/datafeed/{sym}/{d.year}/{d.month-1:02d}/{d.day:02d}/BID_candles_min_1.bi5"
    for att in range(5):
        try:
            r = s.get(url, timeout=45)
            if r.status_code in (200, 404):
                open(fn, "wb").write(r.content if r.status_code == 200 else b""); break
        except Exception:
            s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
        time.sleep(2 * 2 ** att)
    if i % 20 == 0: print(i, len(sample), d, flush=True)
print("DONE", flush=True)
