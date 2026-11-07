#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_veri.py - leadlag_uygulama (BIST) ham veri indirme. Ham veri depoya KONMAZ.

Kaynaklar (yalniz izinli olanlar, varsayilan istek basliklari, istekler arasi bekleme, 429'da geri cekilme):
  * Is Yatirim ChartData IndexHistoricalAll (hisse ve endeks duzeltilmis gunluk kapanis; UTC ms -> TSI gun)
  * FRED fredgraph.csv (DHHNGSP, DCOILBRENTEU, SP500, VIXCLS, DTWEXBGS)
  * CBOE VIX_History.csv
  * Ken French 49 sanayi portfoyu gunluk (zip)
  * Borsa Istanbul VIOP gunluk bulteni (son 3 is gunu; guncel deger hesaplari icin)
Yahoo/Stooq KULLANILMAZ.

Kullanim: python3 01_veri.py --veri /tmp/.../scratchpad/data/leadlag2
"""
import argparse, os, time, io, zipfile
from datetime import datetime, timedelta
import pandas as pd, requests

ISY_URL = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
CBOE_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{}_History.csv"
FRENCH_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_daily_CSV.zip"
VIOP_URL = "https://www.borsaistanbul.com/data/vadeli/viop_{:%Y%m%d}.csv"

HISSE = ["ENERY", "AHGAZ", "RYSAS", "RYGYO", "ENJSA", "AKSEN", "AYGAZ", "TUPRS", "KCHOL", "SAHOL", "AKBNK",
         "BRSAN", "BRYAT", "TRMET", "TRALT", "TRENJ"]
ENDEKS = ["XU100", "XU030", "XUTUM", "XELKT", "XGMYO", "XULAS", "USDTRY"]
FRED = ["DHHNGSP", "DCOILBRENTEU", "SP500", "VIXCLS", "DTWEXBGS"]

S = requests.Session()  # varsayilan basliklar; User-Agent degistirilmez


def isy(kod, bas, son, deneme=4):
    out = []
    # 3 yillik pencerelerle (uzun pencerelerde bos donen yanitlara karsi)
    a = bas
    while a < son:
        b = min(a + timedelta(days=3 * 365), son)
        p = {"period": 1440, "from": a.strftime("%Y%m%d000000"), "to": b.strftime("%Y%m%d235959"), "endeks": kod}
        for k in range(deneme):
            try:
                r = S.get(ISY_URL, params=p, timeout=60)
                if r.status_code == 429:
                    time.sleep(10 * (k + 1)); continue
                if r.status_code == 200 and r.text.strip():
                    d = r.json().get("data") or []
                    if d:
                        ts = pd.to_datetime([x[0] for x in d], unit="ms") + pd.Timedelta(hours=3)
                        out.append(pd.Series([float(x[1]) for x in d], index=ts.normalize()))
                    break
            except (requests.RequestException, ValueError):
                pass
            time.sleep(3 * (k + 1))
        time.sleep(0.8)
        a = b + timedelta(days=1)
    if not out:
        return pd.Series(dtype=float)
    s = pd.concat(out)
    return s[~s.index.duplicated(keep="last")].sort_index()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--veri", required=True)
    ap.add_argument("--bas", default="2009-01-01")
    ap.add_argument("--isy", action="store_true", help="Is Yatirim indir (07.11 gecesi baglanti kopuyordu; o zaman 01b_onbellek.py)")
    a = ap.parse_args()
    V = a.veri
    for d in ("isy", "fred", "cboe", "french", "viop"):
        os.makedirs(os.path.join(V, d), exist_ok=True)
    bas = datetime.strptime(a.bas, "%Y-%m-%d"); son = datetime.now()
    log = []
    for kod in (HISSE + ENDEKS if a.isy else []):
        f = os.path.join(V, "isy", kod + ".csv")
        if os.path.exists(f) and os.path.getsize(f) > 1000:
            log.append(f"{kod}: onbellek"); continue
        s = isy(kod, bas, son)
        if len(s):
            s.rename("px").to_frame().to_csv(f)
        log.append(f"{kod}: {len(s)} gun {s.index.min() if len(s) else '-'} -> {s.index.max() if len(s) else '-'}")
        print(log[-1], flush=True)
    for sid in FRED:
        try:
            r = S.get(FRED_URL.format(sid), timeout=60); time.sleep(0.8)
            if r.status_code == 200 and "," in r.text[:200]:
                open(os.path.join(V, "fred", sid + ".csv"), "w").write(r.text)
                log.append(f"FRED {sid}: {len(r.text.splitlines())} satir")
            else:
                log.append(f"FRED {sid}: HTTP {r.status_code}")
        except requests.RequestException as e:
            log.append(f"FRED {sid}: hata {e}")
        print(log[-1], flush=True)
    try:
        r = S.get(CBOE_URL.format("VIX"), timeout=60); time.sleep(0.8)
        if r.status_code == 200:
            open(os.path.join(V, "cboe", "VIX.csv"), "w").write(r.text); log.append("CBOE VIX ok")
    except requests.RequestException as e:
        log.append(f"CBOE hata {e}")
    try:
        r = S.get(FRENCH_URL, timeout=120); time.sleep(0.8)
        if r.status_code == 200:
            open(os.path.join(V, "french", "49_daily.zip"), "wb").write(r.content); log.append("French 49 daily ok")
    except requests.RequestException as e:
        log.append(f"French hata {e}")
    g = pd.Timestamp(son).normalize(); n = 0
    while n < 4:
        if g.weekday() < 5:
            f = os.path.join(V, "viop", f"viop_{g:%Y%m%d}.csv")
            if not os.path.exists(f):
                try:
                    r = S.get(VIOP_URL.format(g), timeout=60); time.sleep(0.8)
                    if r.status_code == 200 and r.text.lstrip().startswith("TARIH;"):
                        open(f, "w", encoding="utf-8").write(r.text); n += 1; log.append(f"VIOP {g:%Y%m%d} ok")
                except requests.RequestException:
                    pass
            else:
                n += 1
        g -= pd.Timedelta(days=1)
        if (pd.Timestamp(son) - g).days > 12:
            break
    print("\n".join(log))
    open(os.path.join(V, "indirme_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
