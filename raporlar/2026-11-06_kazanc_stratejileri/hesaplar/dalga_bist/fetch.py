"""İş Yatırım ChartData günlük (period=1440) indirici. VARSAYILAN başlıklar (UA taklidi yok). Tek tek istek, 0.7 sn bekleme.
Boş pencere: 'from' geri çekilerek tekrar, olmazsa ikiye bölme. Önbellek: scratchpad/data/dalga_bist/d/<KOD>.csv (ldate,px).
ldate = (UTC ts + 3 sa).normalize()  (TSİ işlem günü). Kullanım: python3 -I fetch.py [KOD ...] [FORCE=1]"""
import os, sys, time, requests, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kumeler import tum_kodlar
BASE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist/d"
U = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
S = requests.Session()
def _req(code, f, t):
    try:
        r = S.get(U, params={"period": 1440, "from": f, "to": t, "endeks": code}, timeout=90)
        if r.status_code == 200 and r.text.strip():
            d = r.json().get("data") or []
            return pd.Series([x[1] for x in d], index=pd.to_datetime([x[0] for x in d], unit="ms"), dtype=float)
        if r.status_code == 429: time.sleep(10)
    except Exception:
        pass
    return pd.Series(dtype=float)
def _get(code, a, b, depth=0):
    for k in range(3):
        x = _req(code, (a - pd.Timedelta(days=k)).strftime("%Y%m%d%H%M%S"), b.strftime("%Y%m%d%H%M%S"))
        time.sleep(0.7)
        if len(x): return x[x.index >= a - pd.Timedelta(hours=3)]
    if (b - a) <= pd.Timedelta(days=20) or depth >= 6: return pd.Series(dtype=float)
    mid = (a + (b - a) / 2).normalize()
    l = _get(code, a, mid - pd.Timedelta(seconds=1), depth + 1); r = _get(code, mid, b, depth + 1)
    p = [z for z in (l, r) if len(z)]
    return pd.concat(p) if p else pd.Series(dtype=float)
def fetch(code, start="2009-06-01", end="2026-11-06 23:59:59", force=False):
    p = os.path.join(BASE, code + ".csv")
    if os.path.exists(p) and not force: return "cached"
    s = _get(code, pd.Timestamp(start), pd.Timestamp(end))
    if len(s) == 0: return "empty"
    s = s.sort_index(); s = s[~s.index.duplicated(keep="last")]
    df = pd.DataFrame({"ldate": (s.index + pd.Timedelta(hours=3)).normalize(), "px": s.values})
    df = df.drop_duplicates("ldate", keep="last")
    df.to_csv(p, index=False)
    return f"ok n={len(df)} {df.ldate.iloc[0].date()}..{df.ldate.iloc[-1].date()}"
if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    args = [a for a in sys.argv[1:] if "=" not in a]; force = "FORCE=1" in sys.argv
    for c in (args or tum_kodlar()):
        print(c, fetch(c, force=force), flush=True)
