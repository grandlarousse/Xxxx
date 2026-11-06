"""Endeks gunluk kapanislari: Is Yatirim ChartData IndexHistoricalAll (period=1440), VARSAYILAN basliklar, 0.6 sn bekleme.
Bos pencere donerse 'from' geri cekilir / pencere ikiye bolunur. Not: BIST fiyat endeksleri (temettu HARIC).
Cikti: scratchpad/data/bist_test/endeks/<KOD>.csv (ldate, px); ldate = (UTC ts + 3 sa).normalize()"""
import os, sys, time, requests, pandas as pd
OUT = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bist_test/endeks"
U = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
S = requests.Session()
def req(code, a, b):
    try:
        r = S.get(U, params={"period": 1440, "from": a.strftime("%Y%m%d%H%M%S"), "to": b.strftime("%Y%m%d%H%M%S"), "endeks": code}, timeout=90)
        if r.status_code == 200 and r.text.strip():
            d = r.json().get("data") or []
            return pd.Series([x[1] for x in d], index=pd.to_datetime([x[0] for x in d], unit="ms"), dtype=float)
    except Exception: pass
    return pd.Series(dtype=float)
def get(code, a, b, depth=0):
    for k in range(3):
        x = req(code, a - pd.Timedelta(days=k), b); time.sleep(0.6)
        if len(x): return x[x.index >= a - pd.Timedelta(hours=3)]
    if (b - a) <= pd.Timedelta(days=30) or depth >= 5: return pd.Series(dtype=float)
    m = (a + (b - a) / 2).normalize()
    p = [z for z in (get(code, a, m - pd.Timedelta(seconds=1), depth + 1), get(code, m, b, depth + 1)) if len(z)]
    return pd.concat(p) if p else pd.Series(dtype=float)
KOD = "XU100 XU030 XU050 XUTUM XYUZO XBANK XUSIN XHOLD XELKT XGMYO XKMYA XMANA XULAS XTCRT XGIDA XILTM XUTEK XTAST XMADN XUMAL XUHIZ XSGRT XFINK XKAGT XTEKS XINSA XSPOR XTRZM XMESY XBLSM XAKUR XUSRD XKOBI USDTRY".split()
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for c in (sys.argv[1:] or KOD):
        p = f"{OUT}/{c}.csv"
        if os.path.exists(p): print(c, "cached"); continue
        s = get(c, pd.Timestamp("2005-01-01"), pd.Timestamp("2026-11-06 23:59:59"))
        if not len(s): print(c, "empty", flush=True); continue
        s = s.sort_index(); s = s[~s.index.duplicated(keep="last")]
        df = pd.DataFrame({"ldate": (s.index + pd.Timedelta(hours=3)).normalize(), "px": s.values}).drop_duplicates("ldate", keep="last")
        df.to_csv(p, index=False); print(c, len(df), df.ldate.iloc[0].date(), df.ldate.iloc[-1].date(), flush=True)
