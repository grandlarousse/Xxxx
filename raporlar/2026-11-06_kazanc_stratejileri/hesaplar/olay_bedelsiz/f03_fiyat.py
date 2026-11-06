"""Is Yatirim fiyat verisi (varsayilan basliklar, tek tek, ~0.8 sn bekleme).
(a) HisseTekil  : gunluk DUZELTILMIS kapanis (HGDG_KAPANIS) + DUZELTILMEMIS kapanis/min/max/AOF (HG_*), SERMAYE, piyasa degeri (PD), hacim.
    GET /_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse=KOD&startdate=dd-mm-yyyy&enddate=dd-mm-yyyy
(b) ChartData   : IndexHistoricalAll (gorevde belirtilen duzeltilmis kapanis kaynagi) -> endeksler + capraz kontrol.
Kullanim: python3 f03_fiyat.py tekil KOD1 KOD2 ... | python3 f03_fiyat.py chart KOD1 ... | python3 f03_fiyat.py tekil @liste.txt
Cikti: <CACHE>/px_tekil/<KOD>.parquet , <CACHE>/px_chart/<KOD>.parquet"""
import os, sys, time, requests, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz"
UT = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"
UC = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
S = requests.Session()
COLS = {"HGDG_TARIH": "tarih", "HGDG_KAPANIS": "adj", "HG_KAPANIS": "c", "HG_MIN": "lo", "HG_MAX": "hi", "HG_AOF": "vwap",
        "HG_HACIM": "hacim_tl", "SERMAYE": "sermaye", "PD": "pd", "END_DEGER": "xu100", "HGDG_MIN": "adj_lo", "HGDG_MAX": "adj_hi"}
def _tekil(kod, a, b, tries=3):
    for k in range(tries):
        try:
            r = S.get(UT, params={"hisse": kod, "startdate": a.strftime("%d-%m-%Y"), "enddate": b.strftime("%d-%m-%Y")}, timeout=75)
            if r.status_code == 200:
                j = r.json()
                if j.get("ok"): return pd.DataFrame(j.get("value") or [])
        except Exception as e: print("err", kod, str(e)[:80], flush=True)
        time.sleep(3 * (k + 1))
    return None
def tekil(kod, bas="2013-01-01", son="2026-11-06"):
    p = f"{CACHE}/px_tekil/{kod}.parquet"
    if os.path.exists(p): return "cached"
    a, b = pd.Timestamp(bas), pd.Timestamp(son)
    df = _tekil(kod, a, b); time.sleep(0.8)
    if df is None:  # 3 parcaya bol (her parca 1 deneme; zaman asiminda uzun beklemeyi onler)
        parts = []; edges = pd.date_range(a, b, periods=4)
        for x0, x1 in zip(edges[:-1], edges[1:]):
            x = _tekil(kod, x0, x1, tries=1); time.sleep(0.8)
            if x is not None and len(x): parts.append(x)
        df = pd.concat(parts) if parts else pd.DataFrame()
    if len(df) == 0:
        pd.DataFrame(columns=list(COLS.values())).to_parquet(p); return "empty"
    df = df[[c for c in COLS if c in df.columns]].rename(columns=COLS)
    df["tarih"] = pd.to_datetime(df.tarih, format="%d-%m-%Y")
    df = df.drop_duplicates("tarih").sort_values("tarih").set_index("tarih")
    df.to_parquet(p); return f"ok n={len(df)} {df.index[0].date()}..{df.index[-1].date()}"
def _chart(kod, a, b):
    try:
        r = S.get(UC, params={"period": 1440, "from": a.strftime("%Y%m%d%H%M%S"), "to": b.strftime("%Y%m%d%H%M%S"), "endeks": kod}, timeout=90)
        if r.status_code == 200 and r.text.strip():
            d = r.json().get("data") or []
            return pd.Series([x[1] for x in d], index=pd.to_datetime([x[0] for x in d], unit="ms"), dtype=float)
    except Exception: pass
    return pd.Series(dtype=float)
def _chart_rec(kod, a, b, depth=0):
    for k in range(2):
        x = _chart(kod, a - pd.Timedelta(days=k), b); time.sleep(0.8)
        if len(x): return x[x.index >= a - pd.Timedelta(days=1)]
    if (b - a) <= pd.Timedelta(days=5) or depth >= 7: return pd.Series(dtype=float)
    m = (a + (b - a) / 2).normalize()
    l = _chart_rec(kod, a, m - pd.Timedelta(seconds=1), depth + 1); r = _chart_rec(kod, m, b, depth + 1)
    z = [s for s in (l, r) if len(s)]
    return pd.concat(z) if z else pd.Series(dtype=float)
def chart(kod, bas="2013-01-01", son="2026-11-06"):
    p = f"{CACHE}/px_chart/{kod}.parquet"
    if os.path.exists(p): return "cached"
    s = _chart_rec(kod, pd.Timestamp(bas), pd.Timestamp(son) + pd.Timedelta(hours=23))
    if len(s) == 0: pd.DataFrame(columns=["px"]).to_parquet(p); return "empty"
    s = s.sort_index(); s = s[~s.index.duplicated(keep="last")]
    df = s.rename("px").to_frame(); df.index = (df.index + pd.Timedelta(hours=3)).normalize(); df = df[~df.index.duplicated(keep="last")]
    df.index.name = "tarih"; df.to_parquet(p); return f"ok n={len(df)} {df.index[0].date()}..{df.index[-1].date()}"
if __name__ == "__main__":
    kind = sys.argv[1]; kods = []
    for a in sys.argv[2:]:
        kods += open(a[1:]).read().split() if a.startswith("@") else [a]
    os.makedirs(f"{CACHE}/px_tekil", exist_ok=True); os.makedirs(f"{CACHE}/px_chart", exist_ok=True)
    for i, k in enumerate(kods):   # 'KOD' ya da 'KOD:bas:son' (olay pencereleri icin daraltilmis aralik; sunucu yukunu yariya indirir)
        kk = k.split(":"); f = tekil if kind == "tekil" else chart
        print(i, k, f(kk[0], kk[1], kk[2]) if len(kk) == 3 else f(kk[0]), flush=True)
