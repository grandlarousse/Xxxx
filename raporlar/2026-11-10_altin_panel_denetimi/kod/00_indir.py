"""Veri indirici (ana ajan tarafından yazıldı).
1) Borsa İstanbul VİOP günlük bültenleri (kamuya açık CSV) -> yalnız ilgili dayanaklar.
2) Yahoo Finance chart API (kamuya açık) -> günlük, saatlik ve 5 dk seriler.
Çıktı: <S>/veri/viop_filtre.csv, <S>/veri/yahoo_<tür>/<sembol>.csv
Kullanım: python3 00_indir.py <S> viop|yahoo
"""
import sys, os, time, datetime as dt, concurrent.futures as cf
import requests, pandas as pd

S = sys.argv[1]
MODE = sys.argv[2]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
KEEP = ("F_XAUUSD", "F_XAUTRY", "F_TRALT", "F_KOZAL", "F_TRMET", "F_KOZAA", "F_XU030", "F_USDTRY")


def norm(h):
    return h.upper().replace("Ö", "O").replace("Ş", "S").replace("İ", "I").replace("Ü", "U").replace("Ç", "C").replace("Ğ", "G").strip()


def one(d):
    url = f"https://www.borsaistanbul.com/data/vadeli/viop_{d:%Y%m%d}.csv"
    st = None
    r = None
    for a in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=60)
            st = r.status_code
            if st == 404:
                return d, "404", []
            if st == 200:
                break
        except Exception as e:  # ağ hatası: yeniden dene
            st = type(e).__name__
        time.sleep(1.5 * 2 ** a)
    else:
        return d, f"fail:{st}", []
    txt = r.content.decode("cp1254", errors="replace")
    lines = txt.splitlines()
    if not lines or "TARIH" not in norm(lines[0]):
        return d, "nohdr", []
    hdr = [norm(c) for c in lines[0].split(";")]
    ci = hdr.index("SOZLESME KODU") if "SOZLESME KODU" in hdr else 1
    out = []
    for l in lines[1:]:
        p = l.split(";")
        if len(p) > ci and p[ci].strip().startswith(KEEP):
            rec = dict(zip(hdr, [x.strip() for x in p]))
            rec["DOSYA_TARIHI"] = d.isoformat()
            out.append(rec)
    return d, "ok", out


if MODE == "viop":
    d0, d1 = dt.date(2018, 11, 1), dt.date(2026, 11, 10)
    days = [d0 + dt.timedelta(i) for i in range((d1 - d0).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    rows, stat = [], {}
    with cf.ThreadPoolExecutor(10) as ex:
        for i, (d, s, o) in enumerate(ex.map(one, days)):
            stat[s] = stat.get(s, 0) + 1
            rows += o
            if s.startswith("fail") or s == "nohdr":
                print("SORUN", d, s, flush=True)
            if i % 200 == 0:
                print("ilerleme", i, len(days), stat, flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(f"{S}/veri/viop_filtre.csv", index=False)
    print("gun durumlari:", stat, "satir:", len(df), "sutun:", list(df.columns), flush=True)
    print("VIOP_BITTI", flush=True)
else:
    P = {"daily": {"period1": 1104537600, "interval": "1d"}, "h1": {"range": "730d", "interval": "60m"},
         "m5": {"range": "60d", "interval": "5m"}}

    def fetch(sym, kind):
        pr = dict(P[kind])
        pr.update(includePrePost="false")
        if kind == "daily":
            pr["period2"] = int(time.time()) + 86400
        r = None
        for a in range(5):
            try:
                r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}", params=pr, headers=UA, timeout=40)
                if r.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(2 * 2 ** a)
        res = r.json()["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
        idx = pd.to_datetime(res["timestamp"], unit="s", utc=True)
        df = pd.DataFrame({"o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "v": q["volume"],
                           "adj": adj if adj else q["close"]}, index=idx)
        tz = res["meta"].get("exchangeTimezoneName")
        df["ldate"] = idx.tz_convert(tz).tz_localize(None).normalize()
        df = df.dropna(subset=["c"])
        df = df[~df["ldate"].duplicated(keep="last")] if kind == "daily" else df[~df.index.duplicated(keep="last")]
        os.makedirs(f"{S}/veri/yahoo_{kind}", exist_ok=True)
        fn = sym.replace("=", "_").replace("^", "_")
        df.to_csv(f"{S}/veri/yahoo_{kind}/{fn}.csv", index_label="utc")
        return len(df), str(df.index[0])[:10], str(df.index[-1])[:16], tz

    D = ["TRALT.IS", "TRMET.IS", "TRENJ.IS", "XU030.IS", "XU100.IS", "GC=F", "SI=F", "GLD", "IAU", "PHYS", "GDX", "GDXJ",
         "SLV", "NEM", "USDTRY=X", "DX-Y.NYB", "UUP", "^TNX", "TIP", "^VIX", "SPY", "TUR"]
    H = ["GC=F", "GLD", "GDX", "GDXJ", "PHYS", "TRALT.IS", "TRMET.IS", "XU030.IS", "USDTRY=X", "SI=F"]
    M = ["GC=F", "GLD", "GDX", "TRALT.IS"]
    for kind, L in (("daily", D), ("h1", H), ("m5", M)):
        for s in L:
            try:
                print(kind, s, fetch(s, kind), flush=True)
            except Exception as e:
                print("SORUN", kind, s, repr(e)[:120], flush=True)
            time.sleep(0.4)
    print("YAHOO_BITTI", flush=True)
