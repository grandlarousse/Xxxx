"""Volatilite ailesi yardımcı modülü (kod/lib.py'yi değiştirmeden genişletir).

ZAMANLAMA: lib.py sözleşmesine uyar. Cboe endeksleri (VIX, VIX9D, VIX3M, VIX6M, VVIX) 16:15 ET'de kapanır;
ETF kapanışı 16:00 ET. Bu yüzden VIX tabanlı sinyallerde C0 hafif iyimserdir (15 dk ileri bakış);
O1 (t+1 açılış) ve C1 (t+1 kapanış) temizdir. Raporlarda O1/C1 esas alınır.

İçerik:
  FAM, GROUPS          : aile ETF'leri ve kopya grupları
  ctx(index)           : Cboe serileri ETF takvimine hizalı (VIX'in GTH tatil satırları düşer)
  proxy_vxx()          : VIX vade yapısından türetilmiş kısa vadeli VIX vadeli endeksi vekili (2009-09+),
                         YALNIZ 2017-07..2021 (IS) verisinde VIXY'ye uydurulur; sadece kapanış (C0/C1) içindir.
  synth(kind)          : -0.5x / -1x / +1.5x / +2x günlük sıfırlamalı sentetik seriler (vekil ya da VIXY'den)
  ev(df, sig, ...)     : lib.trades + lib.stats + 1.000/2.500/10.000 USD maliyet duyarlılığı + p
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import lib

FAM = ["VXX", "VIXY", "UVXY", "UVIX", "SVXY", "SVIX", "VIXM"]
GROUPS = {
    "kisa_vade_long_1x": ["VXX", "VIXY"],          # aynı endeks (S&P 500 VIX Short-Term Futures), kopya
    "kisa_vade_long_kaldirac": ["UVXY", "UVIX"],   # 1.5x ve 2x aynı endeks; bağımsız kanıt değil
    "kisa_vade_ters": ["SVXY", "SVIX"],            # -0.5x ve -1x aynı endeks; bağımsız kanıt değil
    "orta_vade_long": ["VIXM"],                    # farklı endeks (Mid-Term Futures, 4-7. ay)
}
LEV = {"VXX": 1.0, "VIXY": 1.0, "UVXY": 1.5, "UVIX": 2.0, "SVXY": -0.5, "SVIX": -1.0, "VIXM": 1.0}
OUT = os.path.join(lib.ROOT, "sonuclar", "aile_volatilite")
os.makedirs(OUT, exist_ok=True)

_vcache = {}

def vix(name):
    if name not in _vcache:
        _vcache[name] = lib.vol_index(name)
    return _vcache[name]

def ctx(index):
    """Cboe kapanışlarını verilen işlem günü takvimine hizalar (tatilde VIX satırı varsa düşer; eksik gün ffill YOK)."""
    x = pd.DataFrame({n: vix(n).reindex(index) for n in ["VIX", "VIX9D", "VIX3M", "VIX6M", "VVIX"]})
    x["R3M"] = x["VIX"] / x["VIX3M"]          # VIX/VIX3M: <1 kontango, >1 backwardation
    x["R9D"] = x["VIX9D"] / x["VIX"]          # VIX9D/VIX: kısa uç
    x["VIX_SMA10"] = x["VIX"].rolling(10).mean()
    x["VVIX_SMA10"] = x["VVIX"].rolling(10).mean()
    x["VIX_chg"] = x["VIX"].pct_change()
    x["VVIX_chg"] = x["VVIX"].pct_change()
    return x

def costs(df):
    sp = lib.spread_bp_tier(df)
    return {pos: 2 * lib.COMM_USD / pos * 1e4 + sp for pos in (1000.0, 2500.0, 10000.0)}

# ---------------- vekil endeks (uzun dönem testi için) ----------------
_proxy = {}

def proxy_vxx(fit_end="2021-12-31"):
    """Kısa vadeli VIX vadeli endeksinin günlük log getirisi vekili:
         r = a + b1*dlog(VIX) + b2*dlog(VIX3M) + b3*dlog(VIX6M) + b4*log(VIX/VIX3M)_{t-1}
       Katsayılar YALNIZ VIXY 2017-07..fit_end ile tahmin edilir. Dönüş: (DataFrame[c], bilgi dict).
       Takvim: SPY varsa SPY günleri, öncesi VIX günleri (2016 öncesi VIX satırları = NYSE günleri)."""
    if fit_end in _proxy: return _proxy[fit_end]
    v = {n: vix(n) for n in ["VIX", "VIX3M", "VIX6M"]}
    spy = lib.load("SPY").index
    pre = v["VIX3M"].index[v["VIX3M"].index < spy[0]]
    idx = pre.append(spy)
    V = {n: s.reindex(idx) for n, s in v.items()}
    X = pd.DataFrame({"dV": np.log(V["VIX"]).diff(), "d3": np.log(V["VIX3M"]).diff(),
                      "d6": np.log(V["VIX6M"]).diff(), "sl": np.log(V["VIX"] / V["VIX3M"]).shift(1)})
    y = np.log(lib.load("VIXY")["c"]).diff().reindex(idx)
    D = pd.concat([y.rename("y"), X], axis=1).dropna()
    fit = D[D.index <= pd.Timestamp(fit_end)]
    A = np.c_[np.ones(len(fit)), fit[["dV", "d3", "d6", "sl"]].values]
    b = np.linalg.lstsq(A, fit["y"].values, rcond=None)[0]
    Xa = X.dropna()
    p = pd.Series(np.c_[np.ones(len(Xa)), Xa.values] @ b, index=Xa.index)
    oos = D[D.index > pd.Timestamp(fit_end)]
    po = np.c_[np.ones(len(oos)), oos[["dV", "d3", "d6", "sl"]].values] @ b
    info = {"coef": b.tolist(), "fit_n": len(fit), "corr_fit": float(np.corrcoef(A @ b, fit["y"])[0, 1]),
            "corr_oos": float(np.corrcoef(po, oos["y"])[0, 1]), "mean_y_oos_bp": float(oos["y"].mean() * 1e4),
            "mean_p_oos_bp": float(po.mean() * 1e4), "start": str(p.index[0].date())}
    lvl = np.exp(p.cumsum())
    out = pd.DataFrame({"c": lvl}); out["o"] = out["c"]  # açılış yok: yalnız C0/C1 kullanılabilir
    out["h"] = out["c"]; out["l"] = out["c"]; out["raw_c"] = out["c"]; out["dv"] = 1e9; out["v"] = 1e9
    _proxy[fit_end] = (out, info)
    return out, info

def synth_from_returns(r, lev, start_level=100.0):
    """Günlük sıfırlamalı kaldıraçlı/ters seri (basit getiri r, kaldıraç lev). Ücret yok (yıllık ~%1 ihmal)."""
    rr = (lev * r).clip(lower=-0.99)
    c = start_level * (1 + rr.fillna(0)).cumprod()
    out = pd.DataFrame({"c": c}); out["o"] = out["c"]; out["h"] = c; out["l"] = c; out["raw_c"] = c
    out["dv"] = 1e9; out["v"] = 1e9
    return out

def synth_proxy(lev):
    p, _ = proxy_vxx()
    return synth_from_returns(p["c"].pct_change(), lev)

def stitched_svxy():
    """Gerçek SVXY (2018-09-18+) öncesine VIXY'den -0.5x sentetik (2017-07-17..2018-09-17) ekler; o/c ikisi de var.
    Not: Şubat 2018'de gerçek SVXY -1x idi; burada BUGÜNKÜ ürün yapısı (-0.5x) simüle edilir."""
    vx = lib.load("VIXY"); sv = lib.load("SVXY")
    pre = vx[vx.index < sv.index[0]].copy()
    rc = pre["c"].pct_change()
    c = (1 - 0.5 * rc.fillna(0)).cumprod()
    # açılış: önceki sentetik kapanış * (1 - 0.5*gece getirisi VIXY)
    ovn = pre["o"] / pre["c"].shift(1) - 1
    o = c.shift(1) * (1 - 0.5 * ovn)
    o.iloc[0] = c.iloc[0]
    # ölçek: sentetik son kapanış * (1 - 0.5 * VIXY'nin SVXY ilk günündeki getirisi) = SVXY ilk kapanışı
    r0 = sv["c"].iloc[0]
    scale = r0 / c.iloc[-1] / (1 - 0.5 * (vx["c"].reindex(sv.index).iloc[0] / vx["c"].reindex(pre.index).iloc[-1] - 1))
    syn = pd.DataFrame({"o": o * scale, "c": c * scale})
    syn["h"] = syn[["o", "c"]].max(axis=1); syn["l"] = syn[["o", "c"]].min(axis=1)
    syn["raw_c"] = syn["c"]; syn["v"] = np.nan; syn["dv"] = sv["dv"].median(); syn["div"] = 0.0
    out = pd.concat([syn, sv[syn.columns]])
    return out

# ---------------- değerlendirme ----------------
def ev(df, sig, h=1, mode="C0", exit_sig=None, cost_df=None, label="", extra=None):
    """lib.trades/stats ile değerlendirme + maliyet duyarlılığı. cost_df: maliyetin hesaplanacağı gerçek ETF df'si."""
    cdf = df if cost_df is None else cost_df
    cs = costs(cdf)
    c25 = cs[2500.0]
    tr = lib.trades(df, sig, h, mode, exit_sig, c25)
    s = lib.stats(tr, df, h, mode, label)
    s["cost_bp"] = c25; s["h"] = h; s["mode"] = mode
    if len(tr):
        s["net_1000_bp"] = float((tr["gross"].mean() * 1e4) - cs[1000.0])
        s["net_10000_bp"] = float((tr["gross"].mean() * 1e4) - cs[10000.0])
        s["p"] = lib.t_to_p(s.get("t", np.nan), s["n"])
        s["first"] = str(tr["sig_date"].min().date()); s["last"] = str(tr["sig_date"].max().date())
    if extra: s.update(extra)
    return s, tr

TAIL = {"Subat_2018": ("2018-01-29", "2018-02-16"), "Mart_2020": ("2020-02-20", "2020-03-31"),
        "Agu_2024": ("2024-07-29", "2024-08-09"), "Nis_2025": ("2025-03-31", "2025-04-17"),
        "Kas_2026": ("2026-11-02", "2026-11-06")}

def tail_report(tr):
    """İşlemlerin kuyruk dönemlerindeki toplam net getirisi (bp) ve işlem sayısı."""
    out = {}
    for k, (a, b) in TAIL.items():
        m = (tr["entry_date"] <= pd.Timestamp(b)) & (tr["exit_date"] >= pd.Timestamp(a)) if len(tr) else []
        if len(tr) and m.any():
            x = tr[m]
            out[k] = f"{len(x)} islem, toplam net {(np.prod(1 + x['net']) - 1) * 1e4:.0f} bp, en kotu {x['net'].min() * 1e4:.0f} bp"
        else:
            out[k] = "pozisyon yok"
    return out

def worst_hday(df, h):
    """ETF'nin kendi en kötü h günlük kapanış-kapanış getirisi (bp) ve tarihi."""
    r = df["c"].pct_change(h)
    d = r.idxmin()
    return float(r.min() * 1e4), str(d.date())
