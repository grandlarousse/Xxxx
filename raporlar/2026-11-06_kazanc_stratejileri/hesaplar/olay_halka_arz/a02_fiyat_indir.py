"""Adım 2: İş Yatırım'dan fiyat indirme (tek istek, ~0.8 sn arayla, VARSAYILAN başlıklar).
(a) ChartData IndexHistoricalAll (günlük DÜZELTİLMİŞ kapanış) -> px/cd_<KOD>.parquet  [birincil seri]
(b) Data.aspx/HisseTekil (aynı sitenin 'Hisse Tekil' tarihsel veri sayfasının kaynağı): günlük
    HGDG_* = düzeltilmiş kapanış/min/max/AOF, HG_* = DÜZELTİLMEMİŞ kapanış/min/max/AOF, hacim, sermaye.
    -> px/ht_<KOD>.parquet. Tavan kilidi (min=max=kapanış) ve halka arz fiyatına göre ilk gün getirisi
    için düzeltilmemiş seri şart. KONTR 19.07.2024 bedelsizinde HG -%67, HGDG sürekli (doğrulandı).
Kullanım: python3 -I a02_fiyat_indir.py"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import PX, RAW_WEB, polite_get

CD = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
HT = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"
END = pd.Timestamp("2026-11-06")


def cd_req(code, a, b):
    r = polite_get(CD, params={"period": 1440, "from": a.strftime("%Y%m%d%H%M%S"), "to": b.strftime("%Y%m%d%H%M%S"), "endeks": code}, sleep=0.8)
    try:
        if r is not None and r.status_code == 200 and r.text.strip():
            d = r.json().get("data") or []
            return pd.Series([x[1] for x in d], index=pd.to_datetime([x[0] for x in d], unit="ms"), dtype=float)
    except Exception:
        pass
    return pd.Series(dtype=float)


def cd_try(code, a, b):
    for k in range(2):
        x = cd_req(code, a - pd.Timedelta(days=k), b)
        if len(x):
            return x[x.index >= a - pd.Timedelta(hours=4)]
    return pd.Series(dtype=float)


def cd_get(code, a, b):
    """Boş pencere sorunu: önce tüm pencere (2 deneme); boşsa son 90 günü yokla (boşsa hisse işlem görmüyor
    -> vazgeç, gereksiz istek yok); doluysa yıllık, gerekirse çeyreklik pencerelerle topla."""
    x = cd_try(code, a, b)
    if len(x):
        return x
    if not len(cd_try(code, b - pd.Timedelta(days=90), b)):
        return pd.Series(dtype=float)
    parts = []
    y = a
    while y <= b:
        ye = min(y + pd.DateOffset(years=1) - pd.Timedelta(seconds=1), b)
        z = cd_try(code, y, ye)
        if not len(z):
            q = y
            while q <= ye:
                qe = min(q + pd.DateOffset(months=3) - pd.Timedelta(seconds=1), ye)
                zz = cd_try(code, q, qe)
                if len(zz):
                    parts.append(zz)
                q = q + pd.DateOffset(months=3)
        else:
            parts.append(z)
        y = y + pd.DateOffset(years=1)
    return pd.concat(parts) if parts else pd.Series(dtype=float)


def fetch_cd(code, start):
    p = os.path.join(PX, f"cd_{code}.parquet")
    if os.path.exists(p):
        return "cached"
    s = cd_get(code, pd.Timestamp(start), END + pd.Timedelta(hours=23))
    if len(s) == 0:
        return "empty"
    s = s.sort_index(); s = s[~s.index.duplicated(keep="last")]
    df = s.rename("px").to_frame()
    df["ldate"] = (df.index + pd.Timedelta(hours=3)).normalize()  # TSİ işlem günü
    df = df.drop_duplicates("ldate", keep="last").set_index("ldate")
    df.to_parquet(p)
    return f"ok n={len(df)} {df.index[0].date()}..{df.index[-1].date()}"


def fetch_ht(code, start):
    p = os.path.join(PX, f"ht_{code}.parquet")
    if os.path.exists(p):
        return "cached"
    r = polite_get(HT, params={"hisse": code, "startdate": pd.Timestamp(start).strftime("%d-%m-%Y"), "enddate": END.strftime("%d-%m-%Y")}, sleep=0.8, timeout=150)
    try:
        v = r.json().get("value") or []
    except Exception:
        v = []
    if not v:  # bir kez daha, kısa pencereyle
        st2 = max(pd.Timestamp(start) + pd.DateOffset(years=1), pd.Timestamp("2020-01-01"))
        r = polite_get(HT, params={"hisse": code, "startdate": st2.strftime("%d-%m-%Y"), "enddate": END.strftime("%d-%m-%Y")}, sleep=3, timeout=150)
        try:
            v = r.json().get("value") or []
        except Exception:
            v = []
    if not v:
        return "empty"
    df = pd.DataFrame(v)
    df["date"] = pd.to_datetime(df["HGDG_TARIH"], format="%d-%m-%Y")
    keep = ["date", "HGDG_KAPANIS", "HGDG_AOF", "HGDG_MIN", "HGDG_MAX", "HGDG_HACIM", "HG_KAPANIS", "HG_AOF", "HG_MIN", "HG_MAX", "HG_HACIM", "SERMAYE", "END_DEGER", "PD"]
    df = df[[c for c in keep if c in df.columns]].sort_values("date").drop_duplicates("date").set_index("date")
    df.to_parquet(p)
    return f"ok n={len(df)} {df.index[0].date()}..{df.index[-1].date()}"


def main():
    rows = [l.strip().split("|") for l in open(os.path.join(RAW_WEB, "liste_yillar.txt"), encoding="utf-8") if l.strip()]
    # endeksler
    for code in ("XU100", "XHARZ", "XUTUM"):
        print(code, "cd", fetch_cd(code, "2019-01-01"), flush=True)
    for y, kod, slug in rows:
        st = f"{int(y)-1}-01-01"
        print(kod, "ht", fetch_ht(kod, st), "| cd", fetch_cd(kod, st), flush=True)


if __name__ == "__main__":
    main()
