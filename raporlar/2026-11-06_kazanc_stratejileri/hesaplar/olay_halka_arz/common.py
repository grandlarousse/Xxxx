"""Ortak yollar ve nazik HTTP yardımcıları (halka arz olay çalışması).
Ham veri repoya YAZILMAZ; tümü scratchpad altında: data/halka_arz/.
HTTP: varsayılan başlıklar (requests'in kendi User-Agent'ı), tek istek, istekler arası uyku."""
import os, time, requests

ROOT = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/halka_arz"
RAW_WEB = os.path.join(ROOT, "raw_web")
PX = os.path.join(ROOT, "px")
OUT = os.path.join(ROOT, "out")
for d in (RAW_WEB, PX, OUT, os.path.join(RAW_WEB, "pages"), os.path.join(RAW_WEB, "years")):
    os.makedirs(d, exist_ok=True)

S = requests.Session()  # varsayılan başlıklar; UA taklidi YOK
_last = [0.0]


def polite_get(url, params=None, sleep=0.8, timeout=90, tries=3):
    """Tek seferde tek istek; önceki istekten en az `sleep` sn sonra."""
    for k in range(tries):
        dt = time.time() - _last[0]
        if dt < sleep:
            time.sleep(sleep - dt)
        try:
            r = S.get(url, params=params, timeout=timeout)
            _last[0] = time.time()
            if r.status_code == 200:
                return r
            if r.status_code == 403:  # engel: zorlamıyoruz, vazgeç
                print("HTTP 403", url, "-> vazgeç", flush=True)
                return r
            if r.status_code == 429:  # hız limiti: uzun bekle, sonra tekrar (limite uyuyoruz)
                print("HTTP 429", url, "-> 60 sn bekle", flush=True)
                time.sleep(60)
                continue
        except Exception as e:
            _last[0] = time.time()
            print("ERR", url, e, flush=True)
        time.sleep(2 * (k + 1))
    return None
