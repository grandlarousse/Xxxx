"""Adim 2: (a) 1787.HK / 2899.HK / 600547.SS -> TRALT zamanlama denetimi.
HK seansi 01:30-04:00 + 05:00-08:00 UTC (+08:00-08:10 kapanis muzayedesi). Sanghay 01:30-03:30 + 05:00-07:00 UTC.
BIST surekli islem 07:00 UTC'de baslar (acilis muzayedesi ~06:40-07:00). TRALT gun-ici = acilis->kapanis (07:00->15:10 UTC).
Sinyal varyantlari (BIST gunu t, onceki BIST gunu t'):
  CLOSE : log C_t / C_t'                     (orijinal; HK icin 07:00-08:10 UTC BIST ile ORTUSUR -> ileriye bakma)
  OPEN  : log O_t / C_t'                     (gunluk veri; 01:30 UTC'de bilinir; tum donem)
  P0400 : log P(04:00 UTC, ogle arasi) / C_t' (h1; HK 2024-08+ guvenilir)
  P0630 : log P(06:30 UTC) / C_t'            (h1; BIST acilisindan 30 dk once)
  OVL   : log C_t / P(06:30)                 (BIST ile kismen ortusen kisim, 06:30-08:10)
Hedefler: TRALT acilis->kapanis (gunluk); TRALT 07:30->kapanis ve 08:30->kapanis (h1, yalniz 2025-11-24+).
HK h1 verisi 2024-Q3 oncesi gunluk kapanisla tutarsiz (sd 100+ bps) -> h1 sinyalleri 2024-09-01'den itibaren."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a/"
C = V.cal()
TR = V.bist_daily("TRALT.IS"); XU = V.bist_daily("XU100.IS")

def hk_snaps(sym):
    d = V.rawd(sym); d = d.copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    f = (d["adj"] / d["c"])  # temettu faktoru
    h = V.rawd(sym, "h1").copy(); h["end"] = h.index + pd.Timedelta(minutes=60)
    h["day"] = pd.DatetimeIndex(h["ldate"].values)
    def snap(cut):  # cut: UTC saat 'HH:MM' -> o ana kadar BITMIS son barin kapanisi (yarim gun barlari 04:06 dahil)
        hh, mm = map(int, cut.split(":"))
        lim = h["day"].dt.tz_localize("UTC") + pd.Timedelta(hours=hh, minutes=mm)
        ok = h["end"] <= lim
        # 04:06 yarim gun barini 04:00 kesitine dahil et (bitis 04:10)
        if cut == "04:00": ok = ok | (h.index.strftime("%H:%M") == "04:06")
        return h[ok].groupby("day")["c"].last()
    out = pd.DataFrame({"C": d["c"], "O": d["o"], "f": f})
    for cut in ["04:00", "06:30", "07:30"]:
        out["P" + cut.replace(":", "")] = snap(cut)
    out.loc[out["O"] <= 0, "O"] = np.nan
    return out

def signals(sym):
    x = hk_snaps(sym)
    Cc = C[C >= x.index[0]]
    # t' referansi: onceki BIST gunu itibariyla son HK kapanisi (temettu faktoru ile t bazina)
    prevC = x["C"].reindex(x.index.union(Cc)).ffill().reindex(Cc).shift(1)
    prevf = x["f"].reindex(x.index.union(Cc)).ffill().reindex(Cc).shift(1)
    X = x.reindex(Cc)  # t gunu HK gozlemi (yoksa NaN = taze bilgi yok)
    ref = prevC * prevf / X["f"]
    S = pd.DataFrame(index=Cc)
    S["CLOSE"] = np.log(X["C"] / ref)
    S["OPEN"] = np.log(X["O"] / ref)
    S["P0400"] = np.log(X["P0400"] / ref); S["P0630"] = np.log(X["P0630"] / ref); S["P0730"] = np.log(X["P0730"] / ref)
    S["OVL"] = np.log(X["C"] / X["P0630"])
    S["OVL0730"] = np.log(X["C"] / X["P0730"])
    S["AFT"] = np.log(X["P0630"] / X["P0400"])
    # gecersiz h1 donemi
    S.loc[S.index < "2024-09-01", ["P0400", "P0630", "P0730", "OVL", "OVL0730", "AFT"]] = np.nan
    # 12 sigma temizlik CLOSE/OPEN
    for c in S:
        sd = S[c].rolling(250, min_periods=60).std().shift(1); S.loc[(S[c].abs() > 12 * sd) & sd.notna(), c] = np.nan
    return S

def tralt_h1_targets():
    h = V.rawd("TRALT.IS", "h1").copy(); h["day"] = pd.DatetimeIndex(h["ldate"].values); h["hm"] = h.index.strftime("%H:%M")
    p0730 = h[h.hm == "06:30"].groupby("day")["c"].last()   # 06:30-07:30 barinin kapanisi = 07:30 UTC fiyati
    p0830 = h[h.hm == "07:30"].groupby("day")["c"].last()
    o_h1 = h[h.hm == "06:30"].groupby("day")["o"].last()
    T = pd.DataFrame({"p0730": p0730, "p0830": p0830, "o_h1": o_h1}).reindex(TR.index)
    out = pd.DataFrame(index=TR.index)
    out["oc"] = TR["intra"]
    out["e0730"] = np.log(TR["c"] / T["p0730"]); out["e0830"] = np.log(TR["c"] / T["p0830"])
    out["first30"] = np.log(T["p0730"] / TR["o"])
    out["o_chk_bps"] = 1e4 * np.log(T["o_h1"] / TR["o"])
    return out

rows = []
def run(sname, S, tgt, tname, sigcol, start=None, end=None, cost=10):
    df = pd.concat([S[sigcol].rename("s"), tgt.rename("y")], axis=1).dropna()
    if start: df = df[df.index >= start]
    if end: df = df[df.index <= end]
    if len(df) < 40: return
    c, t, n = V.zt(df.y, df.s)
    r, _ = V.bt(df.s, df.y, cost); r0, _ = V.bt(df.s, df.y, 0)
    rows.append({"driver": sname, "signal": sigcol, "target": tname, "start": str(df.index[0].date()), "n": n, "corr": c, "t": t,
                 "gross_bps_all": r0["ALL"].get("mean_bps"), "net10_bps_all": r["ALL"].get("mean_bps"), "sh_all": r["ALL"].get("sharpe"),
                 "sh_IS": r["IS"].get("sharpe"), "sh_OOS": r["OOS"].get("sharpe"), "net10_OOS": r["OOS"].get("mean_bps")})

if __name__ == "__main__":
    TT = tralt_h1_targets()
    print("TRALT acilis kontrolu (h1 ilk bar acilisi vs gunluk acilis, bps):", TT["o_chk_bps"].describe().round(1).to_dict())
    for sym, st0 in [("1787.HK", "2018-10-01"), ("2899.HK", "2014-01-01"), ("600547.SS", "2014-01-01")]:
        S = signals(sym)
        # tum donem (gunluk) : CLOSE vs OPEN
        for sc in ["CLOSE", "OPEN"]:
            run(sym, S, TR["intra"], "TRALT_oc", sc, st0)
            run(sym, S, TR["intra"], "TRALT_oc", sc, st0, "2020-12-31")
            run(sym, S, TR["intra"], "TRALT_oc", sc, "2021-01-01")
        # h1 donemi (2024-09+): tum varyantlar ayni orneklemde
        common = S[["CLOSE", "OPEN", "P0400", "P0630", "OVL"]].dropna().index
        Sc = S.loc[common]
        for sc in ["CLOSE", "OPEN", "P0400", "P0630", "P0730", "OVL", "AFT"]:
            run(sym, S.loc[common], TR["intra"], "TRALT_oc[h1 ornek]", sc)
        # BIST h1 hedefleri (2025-11-24+)
        for sc in ["CLOSE", "P0630", "OVL"]:
            run(sym, S, TT["oc"], "TRALT_oc[2025-11+]", sc, "2025-11-24")
            run(sym, S, TT["e0730"], "TRALT_0730->kap", sc, "2025-11-24")
            run(sym, S, TT["e0830"], "TRALT_0830->kap", sc, "2025-11-24")
            run(sym, S, TT["first30"], "TRALT_acilis->0730", sc, "2025-11-24")
    R = pd.DataFrame(rows)
    R.round(4).to_csv(OUT + "s02_hk_timing.csv", index=False)
    print(R.round(3).to_string())
