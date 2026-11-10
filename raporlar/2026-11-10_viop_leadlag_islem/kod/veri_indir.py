"""VIOP bulten indirici (yeniden baslatilabilir). python3 veri_indir.py <raw_dir> <baslangic> <bitis>
Var olan dosya atlanir; 404 -> '.404' isaret dosyasi (tatil/yok). 3 deneme, artan bekleme."""
import os, sys, time, datetime as dt, requests
from concurrent.futures import ThreadPoolExecutor
raw, d0, d1 = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(raw, exist_ok=True)
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
days = [d for d in (dt.date.fromisoformat(d0) + dt.timedelta(i) for i in range((dt.date.fromisoformat(d1) - dt.date.fromisoformat(d0)).days + 1)) if d.weekday() < 5]
def get(d):
    f = f"{raw}/viop_{d:%Y%m%d}.csv"
    if os.path.exists(f) or os.path.exists(f + ".404"): return "skip"
    for a in range(3):
        try:
            r = S.get(f"https://www.borsaistanbul.com/data/vadeli/viop_{d:%Y%m%d}.csv", timeout=60)
            if r.status_code == 200 and r.content[:5] == b"TARIH":
                open(f, "wb").write(r.content); return "ok"
            if r.status_code in (404, 200):  # 200 ama html = yok
                open(f + ".404", "w").write(str(r.status_code)); return "404"
            time.sleep(3 * (a + 1))
        except Exception:
            time.sleep(3 * (a + 1))
    return "fail"
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(get, days))
from collections import Counter
print(Counter(res))
