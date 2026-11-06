"""Ortak yardimcilar: veri yukleme, temizlik, TL/USD risksiz getiri, donem-bazli portfoy motoru, istatistikler.
Kurallar: sinyal t kapanisinda, islem t+1 kapanisinda (EXEC_LAG=1). Maliyet = tek yon oran x turnover.
Veri: Is Yatirim HisseTekil (hisse, temettu+bedelsiz duzeltmeli) ve ChartData (endeks, FIYAT endeksi, temettu haric)."""
import os, glob, json
import numpy as np, pandas as pd
SP = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad"
DD = SP + "/data/bist_test"
OUTD = "/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/bist_test/cikti"
os.makedirs(OUTD, exist_ok=True)
SON = pd.Timestamp("2026-11-05")      # son TAM kapanis (06.11 gun ici olabilir -> kesildi)
BAS = pd.Timestamp("2009-01-01")

# ---------------- TL risksiz: TCMB 1 hafta repo (resmi tablo) + efektif fonlama duzeltmeleri ----------------
# Kaynak: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo
REPO = """01.01.2009 15.00
15.01.2009 13.00
19.02.2009 11.50
19.03.2009 10.50
16.04.2009 9.75
14.05.2009 9.25
16.06.2009 8.75
16.07.2009 8.25
18.08.2009 7.75
15.10.2009 7.25
19.11.2009 6.50
20.05.2010 7.00
17.12.2010 6.50
21.01.2011 6.25
05.08.2011 5.75
19.12.2012 5.50
17.04.2013 5.00
17.05.2013 4.50
29.01.2014 10.00
23.05.2014 9.50
25.06.2014 8.75
18.07.2014 8.25
21.01.2015 7.75
25.02.2015 7.50
25.11.2016 8.00
01.06.2018 16.50
08.06.2018 17.75
14.09.2018 24.00
26.07.2019 19.75
13.09.2019 16.50
25.10.2019 14.00
13.12.2019 12.00
17.01.2020 11.25
20.02.2020 10.75
18.03.2020 9.75
23.04.2020 8.75
22.05.2020 8.25
25.09.2020 10.25
20.11.2020 15.00
25.12.2020 17.00
19.03.2021 19.00
24.09.2021 18.00
22.10.2021 16.00
19.11.2021 15.00
17.12.2021 14.00
19.08.2022 13.00
23.09.2022 12.00
21.10.2022 10.50
25.11.2022 9.00
24.02.2023 8.50
23.06.2023 15.00
21.07.2023 17.50
25.08.2023 25.00
22.09.2023 30.00
27.10.2023 35.00
24.11.2023 40.00
22.12.2023 42.50
26.01.2024 45.00
22.03.2024 50.00
27.12.2024 47.50
24.01.2025 45.00
07.03.2025 42.50
18.04.2025 46.00
25.07.2025 43.00
12.09.2025 40.50
24.10.2025 39.50
12.12.2025 38.00
23.01.2026 37.00
23.10.2026 36.00"""
# 2009 degerleri: o donem politika faizi TCMB O/N borc alma idi (1 hafta repo politika faizi 20.05.2010'da basladi); yaklasik.
# Efektif fonlama (AOFM) politika faizinin belirgin ustunde oldugu donemler icin MUHAFAZAKAR (engeli yukselten) duzeltme:
OVR = [("2011-10-21", "2012-06-30", 9.5), ("2012-07-01", "2012-12-31", 7.0), ("2013-07-01", "2014-01-28", 6.75),
       ("2015-01-01", "2016-11-24", 8.75), ("2016-11-25", "2017-01-23", 8.3), ("2017-01-24", "2018-04-25", 12.0),
       ("2018-04-26", "2018-05-31", 14.5), ("2025-03-20", "2025-04-17", 46.0)]
def rf_tl_annual(idx, extra_pp=0.0):
    rows = [l.split() for l in REPO.strip().splitlines()]
    s = pd.Series([float(r[1]) for r in rows], index=pd.to_datetime([r[0] for r in rows], format="%d.%m.%Y"))
    s = s.reindex(idx.union(s.index)).ffill().reindex(idx)
    for a, b, v in OVR:
        m = (s.index >= a) & (s.index <= b); s[m] = np.maximum(s[m], v)
    return (s + extra_pp) / 100.0
def daily_from_annual(r_ann):
    dt = r_ann.index.to_series().diff().dt.days.fillna(1).clip(lower=1)
    return (1 + r_ann.shift(1).fillna(r_ann.iloc[0])) ** (dt / 365.0) - 1   # dunku orandan bugune birikim (basit, gun sayisi)

def load_index(code):
    d = pd.read_csv(f"{DD}/endeks/{code}.csv", parse_dates=["ldate"]).set_index("ldate")["px"]
    # Veri hatasi: bazi endekslerde (XBANK, XFINK, XILTM, XSPOR, XUMAL) 02.07.2010-31.12.2010 arasi degerler /100 -> geri olcekle
    q = d / d.shift(1); f = pd.Series(1.0, index=d.index)
    f[q < 0.02] = 100.0; f[q > 50] = 0.01
    d = d * f.cumprod()
    return d[(d.index >= BAS) & (d.index <= SON)]

_cal = None
def calendar():
    global _cal
    if _cal is None: _cal = load_index("XU100").index
    return _cal

def base():
    """Gunluk takvim; USDTRY, TL rf, USD rf (FRED DTB3, gerceklesen T-bill getirisi ~ oran/360)."""
    cal = calendar()
    fx = load_index("USDTRY").reindex(cal).ffill()
    rf = rf_tl_annual(cal)
    tb = pd.read_csv(f"{DD}/DTB3.csv", na_values=".", parse_dates=["observation_date"]).set_index("observation_date")["DTB3"]
    tb = tb.reindex(cal.union(tb.index)).ffill().reindex(cal) / 100.0
    dt = cal.to_series().diff().dt.days.fillna(1).clip(lower=1)
    df = pd.DataFrame({"fx": fx, "rf_ann": rf, "tb_ann": tb})
    df["rf_d"] = daily_from_annual(rf)
    df["tb_d"] = tb.shift(1).fillna(tb.iloc[0]) * dt / 360.0
    df["fx_r"] = fx.pct_change().fillna(0)
    return df

# ---------------- hisse paneli ----------------
def load_stocks(min_days=120):
    cal = calendar()
    fr = {k: {} for k in ("adj", "raw", "vol_tl", "mcap")}
    for p in sorted(glob.glob(f"{DD}/hisse/*.parquet")):
        c = os.path.basename(p)[:-8]
        x = pd.read_parquet(p)
        x = x[(x.index >= BAS) & (x.index <= SON)]
        if len(x) < min_days: continue
        for k in fr:
            if k in x: fr[k][c] = x[k]
    P = {k: pd.DataFrame(v).reindex(cal) for k, v in fr.items()}
    return P

def clean_returns(P, log=None):
    """Gunluk duzeltmeli getiri. Supheli sicrama: |r_adj|>%25. Ham fiyat ayni hareketi gosteriyorsa (gercek: aski donusu vb.) tut;
    gostermiyorsa (duzeltme hatasi) ham getiriyi kullan; ham da >%25 ise (bolunme + duzeltme hatasi) 0 yap."""
    adj, raw = P["adj"], P["raw"]
    ra = adj / adj.ffill().shift(1) - 1
    rr = raw / raw.ffill().shift(1) - 1
    sus = ra.abs() > 0.25
    keep = sus & ((ra - rr).abs() < 0.02)
    fix_raw = sus & ~keep & (rr.abs() <= 0.25)
    zero = sus & ~keep & ~fix_raw
    r = ra.where(~fix_raw, rr).where(~zero, 0.0)
    info = {"supheli": int(sus.sum().sum()), "gercek_tutulan": int(keep.sum().sum()), "ham_ile_duzeltilen": int(fix_raw.sum().sum()), "sifirlanan": int(zero.sum().sum())}
    traded = adj.notna() & (P["vol_tl"].fillna(0) > 0)
    return r, traded, info

# ---------------- rebalans tarihleri ----------------
def rebal_dates(freq, cal=None, start="2010-01-01"):
    """freq: 'W' (haftanin son islem gunu), 'M' (ayin son islem gunu), 'W2','W4' (her 2/4 haftada bir)."""
    cal = calendar() if cal is None else cal
    s = pd.Series(cal, index=cal)
    if freq.startswith("W"):
        g = s.groupby([cal.isocalendar().year.values, cal.isocalendar().week.values]).last().sort_values().values
        k = int(freq[1:]) if len(freq) > 1 else 1
        g = g[::k]
    else:
        g = s.groupby([cal.year, cal.month]).last().values
    g = pd.DatetimeIndex(g)
    return g[g >= pd.Timestamp(start)]

# ---------------- donem bazli EW portfoy motoru ----------------
def period_engine(sel, R, cost_side, rf_p, ls_bench=None):
    """sel: list of arrays (secilen sutun indeksleri) her donem icin; R: (n_per x n_stock) donem getirisi (exec->exec);
    esit agirlik, donem ici al-tut. Bos secim = nakit (rf). Maliyet: tek-yon oran x |w_yeni - w_kaymis| toplami.
    ls_bench: verilirse long - (bench - rf) (VIOP endeks kisa)."""
    n = len(sel); out = np.zeros(n); turn = np.zeros(n); prev_w = {}
    for t in range(n):
        s = sel[t]
        new_w = {int(i): 1.0 / len(s) for i in s} if len(s) else {}
        keys = set(new_w) | set(prev_w)
        to = sum(abs(new_w.get(k, 0) - prev_w.get(k, 0)) for k in keys) + (abs(1 - sum(new_w.values()) - (1 - sum(prev_w.values()))))
        turn[t] = to
        if len(s):
            rr = R[t, s]; rr = np.where(np.isnan(rr), 0.0, rr)
            gr = rr.mean()
            grow = {int(i): (1.0 / len(s)) * (1 + rr[j]) for j, i in enumerate(s)}
            tot = sum(grow.values()) or 1
            prev_w = {k: v / tot for k, v in grow.items()}
        else:
            gr = rf_p[t]; prev_w = {}
        out[t] = gr - cost_side * to
    if ls_bench is not None: out = out - (ls_bench - rf_p)
    return out, turn

def per_returns(px_exec):
    """exec tarihleri arasi getiriler: satir t = exec_t -> exec_{t+1}"""
    return (px_exec.shift(-1) / px_exec - 1)

def compound_between(daily, dates):
    """gunluk getiriyi exec tarihleri arasinda bilesikle: t -> t+1"""
    c = (1 + daily).cumprod()
    v = c.reindex(dates)
    return (v.shift(-1) / v - 1)

# ---------------- istatistik ----------------
def stats(r, rf, dates=None, ppy=None):
    r = pd.Series(r).astype(float); rf = pd.Series(rf).astype(float)
    m = r.notna() & rf.notna(); r, rf = r[m], rf[m]
    if len(r) < 8: return {}
    if ppy is None:
        if dates is not None:
            d = pd.DatetimeIndex(dates)[m.values] if len(dates) == len(m) else pd.DatetimeIndex(dates)
            yrs = max((d[-1] - d[0]).days / 365.25, 1e-9); ppy = len(r) / yrs
        else: ppy = 252
    yrs = len(r) / ppy
    eq = (1 + r).cumprod(); eqf = (1 + rf).cumprod()
    cagr = eq.iloc[-1] ** (1 / yrs) - 1; cagr_rf = eqf.iloc[-1] ** (1 / yrs) - 1
    ex = r - rf
    return {"CAGR": cagr, "rfCAGR": cagr_rf, "Fazla": (1 + cagr) / (1 + cagr_rf) - 1, "Vol": r.std() * np.sqrt(ppy),
            "Sharpe": ex.mean() / ex.std() * np.sqrt(ppy) if ex.std() > 0 else np.nan,
            "MaxDD": (eq / eq.cummax() - 1).min(), "Isabet": (ex > 0).mean(), "N": len(r)}

def to_usd(r_tl, fx_p):
    return (1 + r_tl) / (1 + fx_p) - 1

def yearly(r, dates):
    s = pd.Series(np.asarray(r, float), index=pd.DatetimeIndex(dates))
    return (1 + s).groupby(s.index.year).prod() - 1

def fmt_stats(d, keys=("CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "Isabet")):
    if not d: return " | ".join(["-"] * len(keys))
    o = []
    for k in keys:
        v = d.get(k, np.nan)
        o.append(f"{v:.2f}" if k == "Sharpe" else f"{100*v:.1f}%")
    return " | ".join(o)
