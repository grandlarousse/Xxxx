"""TEST 3 (+6): 52-hafta / 6-ay zirve kirilimi ve 'trend sablonu' (Minervini tarzi). Olay bazli + 10 slotlu portfoy.
Evren: gunluk en likit 150 (60g medyan TL hacim), guncel-listeli hisseler (survivorship!).
TT: P>SMA50>SMA150>SMA200, SMA200 21 gun once kendisinden dusuk, P>=1.25*52h-dip, P>=0.75*52h-zirve, RS (0.4*R3a+0.2*R6a+0.2*R9a+0.2*R12a) evren-ici yuzdelik >= 80.
Tetikler: B52 = kapanis onceki 252 gunun en yuksek kapanisinin ustunde; B126 = onceki 126 gun.
Sinyaller: S1 B52 | S2 B52+TT | S3 B126+TT | S4 TT ilk gun | S5 B52+TT+rejim(XU100>SMA200).
Cikis: sabit 10/20/40 gun; iz-suren stop %15 (zirve kapanistan, en fazla 120 gun); kapanis<SMA50 (en fazla 120 gun). Cikis sinyali kapanista -> ertesi kapanis.
Giris: sinyal t kapanisi -> t+1 kapanisi. Maliyet 25 bp gidis-donus. Ayni hissede acik islem varken yeni giris yok.
Kiyas (placebo): ayni giris/cikis tarihlerinde evrendeki TUM likit hisselerin ortalama getirisi (eslesmis rastgele)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
B = base(); cal = B.index
px = pd.read_parquet(f"{DD}/panel_px.parquet"); rank = pd.read_parquet(f"{DD}/panel_liqrank.parquet")
P = px.ffill(); cols = P.columns
UNIV = os.environ.get("UNIV", "top150")
if UNIV == "top75": liq = (rank <= 75).fillna(False)
elif UNIV == "kohort2009":   # 31.12.2009'da zaten fiyati olan hisseler (IPO secim etkisini azaltir; survivorship kalir)
    coh = px.loc[:"2009-12-31"].notna().any(); liq = ((rank <= 150) & coh.values[None, :]).fillna(False)
else: liq = (rank <= 150).fillna(False)
GERCEKCI = os.environ.get("GERCEKCI", "0") == "1"   # tavan kapanista alim yok, taban kapanista satis bir gun ertelenir
SUF = ("" if UNIV == "top150" else "_" + UNIV) + ("_gercekci" if GERCEKCI else "")
xu = load_index("XU100").reindex(cal).ffill()
COST = 0.0025
S50, S150, S200 = P.rolling(50).mean(), P.rolling(150).mean(), P.rolling(200).mean()
hi252 = P.shift(1).rolling(252, min_periods=240).max(); lo252 = P.rolling(252, min_periods=240).min()
hi126 = P.shift(1).rolling(126, min_periods=120).max()
rs = 0.4 * (P / P.shift(63) - 1) + 0.2 * (P / P.shift(126) - 1) + 0.2 * (P / P.shift(189) - 1) + 0.2 * (P / P.shift(252) - 1)
rsp = rs.where(liq).rank(axis=1, pct=True)
TT = (P > S50) & (S50 > S150) & (S150 > S200) & (S200 > S200.shift(21)) & (P >= 1.25 * lo252) & (P >= 0.75 * hi252) & (rsp >= 0.8)
B52 = P > hi252; B126 = P > hi126
reg = (xu > xu.rolling(200).mean())
SIG = {"S1_B52": B52 & liq, "S2_B52+TT": B52 & TT & liq, "S3_B126+TT": B126 & TT & liq,
       "S4_TT_ilkgun": TT & ~TT.shift(1, fill_value=False) & liq, "S5_B52+TT+rejim": B52 & TT & liq & reg.values[:, None]}
START = np.flatnonzero(cal >= pd.Timestamp("2010-01-01"))[0]
Pv = P.values; S50v = S50.values; T = len(cal)
rfc = (1 + B.rf_d).cumprod().values; xuv = xu.values; liqv = liq.values; rspv = rsp.values

def make_trades(sig, exit_rule):
    sv = sig.values; out = []
    for j in range(sv.shape[1]):
        idx = np.flatnonzero(sv[:, j]); busy = -1
        for t in idx:
            if t < START or t <= busy: continue
            e = t + 1
            if e >= T or np.isnan(Pv[e, j]): continue
            if GERCEKCI and Pv[e, j] / Pv[t, j] - 1 >= 0.095: continue
            if exit_rule[0] == "fix":
                x = e + exit_rule[1]
                if x >= T: continue
            else:
                x = None; peak = Pv[e, j]
                for d in range(e + 1, min(e + 121, T)):
                    p = Pv[d, j]
                    if np.isnan(p): continue
                    peak = max(peak, p)
                    hit = (p <= peak * (1 - exit_rule[1])) if exit_rule[0] == "trail" else (p < S50v[d, j])
                    if hit: x = d + 1; break
                if x is None: x = min(e + 120, T - 1)
                if x >= T: continue
            if GERCEKCI:
                while x < T - 1 and Pv[x, j] / Pv[x - 1, j] - 1 <= -0.095: x += 1
            out.append((j, t, e, x)); busy = x
    return out

def trade_table(tr):
    if not tr: return pd.DataFrame()
    j, t, e, x = map(np.array, zip(*tr))
    g = Pv[x, j] / Pv[e, j] - 1
    rfw = rfc[x] / rfc[e] - 1; xw = xuv[x] / xuv[e] - 1
    base = np.array([np.nanmean(Pv[xx, liqv[ee]] / Pv[ee, liqv[ee]] - 1) for ee, xx in zip(e, x)])
    return pd.DataFrame({"hisse": cols[j], "sinyal": cal[t], "giris": cal[e], "cikis": cal[x], "gun": x - e, "brut": g, "net": g - COST,
                         "rf": rfw, "xu100": xw, "evren_ort": base, "rs": rspv[t, j]})

def summarize(df):
    if df.empty: return {}
    n = df.net; w = n[n > 0]; l = n[n <= 0]
    yrs = (cal[-1] - cal[START]).days / 365.25
    return {"N": len(df), "islem_yil": len(df) / yrs, "ort_gun": df.gun.mean(), "ort_net": n.mean(), "medyan_net": n.median(),
            "isabet": (n > 0).mean(), "isabet_rf_ustu": (n > df.rf).mean(), "kazanc_ort": w.mean(), "kayip_ort": l.mean(),
            "payoff": w.mean() / -l.mean() if len(l) else np.nan, "carpiklik": n.skew(), "p05": n.quantile(0.05), "p95": n.quantile(0.95),
            "ort_rf_ustu": (n - df.rf).mean(), "ort_xu100_ustu": (n - df.xu100).mean(), "ort_evren_ustu(placebo)": (df.brut - df.evren_ort).mean(),
            "t_evren_ustu(ay-kume)": tstat_cluster(df.brut - df.evren_ort, df.giris.dt.to_period("M")),
            "ort_net_2024_26": n[df.giris >= "2024-01-01"].mean(), "evren_ustu_2024_26": (df.brut - df.evren_ort)[df.giris >= "2024-01-01"].mean(),
            "N_2024_26": int((df.giris >= "2024-01-01").sum())}

def tstat_cluster(v, g):
    m = v.groupby(g.values).mean()
    return m.mean() / m.std() * np.sqrt(len(m)) if len(m) > 2 else np.nan

def portfolio(df, K=10):
    """K slotlu portfoy: her giriste ozkaynak/K; slot doluysa yeni sinyal atlanir (yuksek RS oncelikli). Nakit TL rf kazanir."""
    df = df.sort_values(["giris", "rs"], ascending=[True, False])
    ent = {}; [ent.setdefault(int(cal.get_loc(r.giris)), []).append(r) for r in df.itertuples()]
    rfd = B.rf_d.values; cash = 1.0; pos = []; eq = np.ones(T); ntr = 0
    jmap = {c: i for i, c in enumerate(cols)}
    for d in range(START, T):
        cash *= (1 + rfd[d])
        val = 0.0; keep = []
        for p in pos:
            v = p["sh"] * Pv[d, p["j"]] if not np.isnan(Pv[d, p["j"]]) else p["last"]
            p["last"] = v
            if d >= p["x"]: cash += v * (1 - COST / 2)
            else: keep.append(p); val += v
        pos = keep
        for r in ent.get(d, []):
            if len(pos) >= K: break
            e = cash + val; a = min(e / K, cash)
            if a <= 0: break
            j = jmap[r.hisse]; cash -= a; a_net = a * (1 - COST / 2)
            pos.append({"j": j, "sh": a_net / Pv[d, j], "x": int(cal.get_loc(r.cikis)), "last": a_net}); val += a_net; ntr += 1
        eq[d] = cash + val
    e = pd.Series(eq[START:], index=cal[START:]); return e.pct_change().fillna(0), ntr

if __name__ == "__main__":
    EXITS = {"sabit10": ("fix", 10), "sabit20": ("fix", 20), "sabit40": ("fix", 40), "iz%15": ("trail", 0.15), "SMA50alti": ("sma", 0)}
    rows = []; pf_rows = []; yt = {}
    for sn, sig in SIG.items():
        for en, er in EXITS.items():
            df = trade_table(make_trades(sig, er))
            st = summarize(df); rows.append(dict(sinyal=sn, cikis=en, **st))
            if sn in ("S2_B52+TT", "S1_B52", "S5_B52+TT+rejim") and en in ("sabit20", "iz%15", "SMA50alti"):
                r, ntr = portfolio(df)
                m = r.index
                for cur in ("TL", "USD"):
                    rr = r if cur == "TL" else to_usd(r, B.fx_r.reindex(m))
                    rf = B.rf_d.reindex(m) if cur == "TL" else B.tb_d.reindex(m)
                    a = stats(rr, rf, ppy=252); k = m >= "2024-01-01"; b = stats(rr[k], rf[k], ppy=252)
                    pf_rows.append(dict(sinyal=sn, cikis=en, para=cur, islem=ntr, **a, CAGR_24_26=b.get("CAGR"), Fazla_24_26=b.get("Fazla"), MaxDD_24_26=b.get("MaxDD")))
                    if cur == "TL": yt[f"{sn} {en}"] = yearly(rr.values, m)
                # PORTFOY PLACEBO: ayni giris/cikis tarihleri, hisse yerine ayni gun likit evrenden rastgele hisse (NPL cekilis)
                if en in ("iz%15", "sabit20") and sn in ("S1_B52", "S2_B52+TT"):
                    rng = np.random.default_rng(11); cg = []; shp = []
                    NPL = int(os.environ.get("NPL", "40"))
                    gi = df.giris.map(cal.get_loc).values; ci = df.cikis.map(cal.get_loc).values
                    for _ in range(NPL):
                        hs = []
                        for ee, xx in zip(gi, ci):
                            pool = np.flatnonzero(liqv[ee - 1] & ~np.isnan(Pv[ee]) & ~np.isnan(Pv[xx]))
                            hs.append(cols[rng.choice(pool)])
                        rp, _ = portfolio(df.assign(hisse=hs, rs=rng.random(len(df))))
                        exr = rp - B.rf_d.reindex(rp.index)
                        cg.append((1 + rp).prod() ** (252 / len(rp)) - 1); shp.append(exr.mean() / exr.std() * np.sqrt(252))
                    a0 = stats(r, B.rf_d.reindex(r.index), ppy=252)
                    pf_rows.append(dict(sinyal=sn, cikis=en, para="PLACEBO-TL", islem=ntr, CAGR=float(np.median(cg)), Sharpe=float(np.median(shp)),
                                        placebo_p95_CAGR=float(np.percentile(cg, 95)), placebo_p95_Sharpe=float(np.percentile(shp, 95)),
                                        yuzdelik_Sharpe=float(np.mean(np.array(shp) < a0["Sharpe"]))))
                if sn == "S2_B52+TT" and en == "iz%15":
                    df.to_csv(f"{OUTD}/t03_islemler_S2_iz15{SUF}.csv", index=False)
                    by = df.assign(y=df.giris.dt.year).groupby("y").agg(N=("net", "size"), ort_net=("net", "mean"), isabet=("net", lambda v: (v > 0).mean()),
                                                                           evren_ustu=("brut", "mean"))
                    by["evren_ustu"] = df.assign(y=df.giris.dt.year, z=df.brut - df.evren_ort).groupby("y").z.mean()
                    by.to_csv(f"{OUTD}/t03_yillik_islem_S2_iz15{SUF}.csv")
    # stres: 50 bp maliyet (islem bazinda)
    for r_ in rows: r_["ort_net_50bp"] = r_.get("ort_net", np.nan) - 0.0025 if r_ else np.nan
    D = pd.DataFrame(rows); D.to_csv(f"{OUTD}/t03_islem_ozet{SUF}.csv", index=False)
    F = pd.DataFrame(pf_rows); F.to_csv(f"{OUTD}/t03_portfoy{SUF}.csv", index=False)
    pd.DataFrame(yt).to_csv(f"{OUTD}/t03_portfoy_yillik_TL{SUF}.csv")
    pd.set_option("display.width", 280); pd.set_option("display.max_columns", 40)
    print(D.round(3).to_string()); print(F.round(3).to_string())
