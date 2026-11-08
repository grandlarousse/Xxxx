"""3) Aileye özel hipotezler (hipotezler.csv KR01-KR06 + yönlendirme). Çalıştır: python3 -I kod/ajan_kripto/03_hipotezler.py
Her test önce dayanakta (BTC_D 2016-11..2026-11 IS/OOS; BTC_ET 2023-06+ birebir 16:00 ET), sonra ETF'de.
Maliyet: 2.500$ pozisyon, IBIT/ETHA/ilgili ETF makası. Çıktı: sonuclar/aile_kripto/hipotez_testleri.csv (+ yardımcı tablolar)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import kr, lib
import strategies as S

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 400)
ROWS = []
SP = {s: kr.spread_bp(s) for s in kr.FAM}
SP["BTC_D"] = SP["BTC_ET"] = SP["IBIT"]; SP["ETH_D"] = SP["ETH_ET"] = SP["ETHA"]

BTC_D = kr.crypto_daily_proxy("BTC-USD"); ETH_D = kr.crypto_daily_proxy("ETH-USD")
BTC_ET = kr.crypto_et_proxy("BTC-USD"); ETH_ET = kr.crypto_et_proxy("ETH-USD")
SER = {"BTC_D": BTC_D, "ETH_D": ETH_D, "BTC_ET": BTC_ET, "ETH_ET": ETH_ET}
def series(nm):
    return SER[nm] if nm in SER else lib.load(nm)

def edge_parts(df, tr, h, mode):
    u = lib.uncond(df, h, mode).dropna()
    out = {}
    for nm, m_tr, m_u in (("is", tr.sig_date <= lib.IS_END, u.index <= lib.IS_END), ("oos", tr.sig_date > lib.IS_END, u.index > lib.IS_END)):
        if m_tr.sum() > 1:
            uu = u[m_u]; uu = uu[uu.index >= tr.sig_date[m_tr].min()]
            out[f"{nm}_edge_bp"] = (tr.gross[m_tr].mean() - uu.mean()) * 1e4
    return out

def add(hyp, nm, sig, h, mode, note="", exit_sig=None):
    df = series(nm)
    s, tr = kr.full_eval(df, sig.reindex(df.index).fillna(False), h, mode, SP[nm], exit_sig=exit_sig, label=hyp)
    if s.get("n", 0) == 0: return s, tr
    s.update(edge_parts(df, tr, h, mode))
    s.update({"hipotez": hyp, "seri": nm, "not": note})
    ROWS.append(s)
    return s, tr

def add_tr(hyp, nm, tr, spread, note=""):
    s = kr.summarize(tr, hyp, spread=spread)
    if s.get("n", 0) == 0: return s
    s.update({"hipotez": hyp, "seri": nm, "not": note, "mode": "C->O", "h": 0, "cost_bp": kr.cost_at(spread, 2500)})
    ROWS.append(s)
    return s

def show(hyp):
    d = pd.DataFrame([r for r in ROWS if r["hipotez"] == hyp])
    cols = [c for c in ["seri", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "uncond_bp", "edge_bp", "t", "t_edge", "is_net_bp", "oos_net_bp",
                        "is_edge_bp", "oos_edge_bp", "years_pos_frac", "win", "pf", "net_1000", "net_10000", "not"] if c in d]
    print(f"\n=== {hyp} ===")
    print(d[cols].round(2).to_string(index=False))

# -------------------------------------------------------------------------------------------------
# KR01 gece / gün içi ve KR05 kış-yaz
on_rows = []
for nm in ["BTC_ET", "ETH_ET", "IBIT", "FBTC", "BITB", "ARKB", "GBTC", "ETHA", "ETHE", "BITX", "BITU", "ETHU", "MSTU", "CONL", "BLOK"]:
    df = series(nm)
    on = df["o"].shift(-1) / df["c"] - 1           # t kapanış -> t+1 açılış
    idr = df["c"].shift(-1) / df["o"].shift(-1) - 1  # t+1 gün içi
    d = pd.DataFrame({"on": on, "id": idr}).dropna()
    dst = kr.is_dst(d.index)
    rec = {"seri": nm, "n": len(d), "gece_bp": d.on.mean() * 1e4, "gece_t": kr.tstat(d.on), "gunici_bp": d.id.mean() * 1e4,
           "gunici_t": kr.tstat(d.id), "gece_kis_bp": d.on[~dst].mean() * 1e4, "gece_kis_t": kr.tstat(d.on[~dst]),
           "gece_yaz_bp": d.on[dst].mean() * 1e4, "gece_yaz_t": kr.tstat(d.on[dst]),
           "gece_kumulatif_pct": (np.prod(1 + d.on) - 1) * 100, "gunici_kumulatif_pct": (np.prod(1 + d.id) - 1) * 100}
    on_rows.append(rec)
    sp = SP.get(nm, SP["IBIT"])
    allsig = pd.Series(True, index=df.index)
    tr = kr.overnight_trades(df, allsig, kr.cost_at(sp, 2500))
    add_tr("KR01_gece_her_gun", nm, tr, sp, "t kapanışında al, t+1 açılışında sat; her gün")
    if nm in ("BTC_ET", "IBIT"):
        win = pd.Series(~kr.is_dst(df.index), index=df.index)
        add_tr("KR05_gece_kis", nm, kr.overnight_trades(df, win, kr.cost_at(sp, 2500)), sp, "yalnız ABD kış saati (kapanış 21:00 UTC)")
        add_tr("KR05_gece_yaz", nm, kr.overnight_trades(df, ~win, kr.cost_at(sp, 2500)), sp, "yalnız ABD yaz saati (kapanış 20:00 UTC)")
ON = pd.DataFrame(on_rows)
ON.to_csv(os.path.join(kr.OUT, "gece_gunici.csv"), index=False)
print("=== KR01/KR05 gece (C->O) ve gün içi (O->C) ortalamaları, bp ===")
print(ON.round(2).to_string(index=False))
show("KR01_gece_her_gun"); show("KR05_gece_kis"); show("KR05_gece_yaz")

# KR05 saatlik: 21-23 UTC penceresi
h1 = pd.read_parquet(os.path.join(kr.ROOT, "data", "crypto", "BTC-USD_h1.parquet"))
r1 = np.log(h1["c"] / h1["o"])
w = r1[r1.index.hour.isin([21, 22])]
wd = w.groupby(w.index.normalize()).sum()
print("\nKR05 BTC 21:00-23:00 UTC toplam getirisi (2023-05+): ort %.1f bp, t=%.2f, n=%d" % (wd.mean() * 1e4, kr.tstat(wd), len(wd)))
print((wd.groupby(wd.index.year).agg(["mean", "count"]) * [1e4, 1]).round(1).to_string())

# Seans ayrıştırması (ET saatleriyle)
hh = h1.copy(); hh.index = h1.index.tz_convert("America/New_York")
lr = np.log(hh["c"] / hh["o"]); hr = hh.index.hour
sess = np.select([(hr >= 9) & (hr < 16), (hr >= 16) & (hr < 20), (hr >= 20) | (hr < 3)], ["ABD_seans_09_16ET", "ABD_aksam_16_20ET", "Asya_20_03ET"], "Avrupa_03_09ET")
SS = pd.DataFrame({"r": lr.values, "sess": sess, "gun": hh.index.tz_localize(None).normalize(), "dow": hh.index.dayofweek}, index=hh.index)
SS["hafta_sonu"] = SS.dow >= 5
agg = SS.groupby(["gun", "sess", "hafta_sonu"]).r.sum().reset_index()
agg["yil"] = agg.gun.dt.year
sess_rows = []
for (sname, we), g in agg.groupby(["sess", "hafta_sonu"]):
    rec = {"seans": sname, "hafta_sonu": we, "n_gun": len(g), "ort_bp": g.r.mean() * 1e4, "t": kr.tstat(g.r), "yillik_toplam_pct": g.r.mean() * (104 if we else 261) * 100}
    for y, gy in g.groupby("yil"):
        rec[f"y{y}_bp"] = gy.r.mean() * 1e4
    sess_rows.append(rec)
SE = pd.DataFrame(sess_rows)
SE.to_csv(os.path.join(kr.OUT, "seans_getirileri.csv"), index=False)
print("\n=== BTC seans getirileri (saatlik, 2023-05..2026-11; günlük toplam log getiri, bp) ===")
print(SE.round(2).to_string(index=False))

# -------------------------------------------------------------------------------------------------
# KR02 hafta sonu: Cuma kapanışı -> Pazartesi kapanışı (C0 h=1 Cuma sinyali); kontrol: diğer günler
for nm in ["BTC_D", "ETH_D", "BTC_ET", "IBIT", "ETHA", "BITX", "BLOK", "MSTU", "CONL"]:
    df = series(nm)
    fri = pd.Series(df.index.dayofweek == 4, index=df.index)
    add("KR02_cuma_C0_h1", nm, fri, 1, "C0", "Cuma kapanışında al, sonraki işlem günü (Pzt) kapanışında sat")
    add("KR02_diger_gunler_C0_h1", nm, ~fri, 1, "C0", "kontrol: Cuma dışı günlerde 1 gün")
    if nm in ("BTC_ET", "IBIT", "ETHA", "BITX"):
        add_tr("KR02_cuma_gece_C->O", nm, kr.overnight_trades(df, fri, kr.cost_at(SP[nm], 2500)), SP[nm], "Cuma kapanış -> Pzt açılış")
show("KR02_cuma_C0_h1"); show("KR02_diger_gunler_C0_h1"); show("KR02_cuma_gece_C->O")

# Hafta sonu BTC hareketi -> Pazartesi açılış boşluğu (gerçek zamanlı) ve Pazartesi gün içi
I = lib.load("IBIT"); E = BTC_ET
x = pd.DataFrame({"ibit_gap": np.log(I["o"] / I["c"].shift(1)), "btc_gece": np.log(E["o"] / E["c"].shift(1)).reindex(I.index),
                  "ibit_id": np.log(I["c"] / I["o"])}).dropna()
x["pzt"] = x.index.dayofweek == 0
gap_rows = []
for nm, g in (("tum_gunler", x), ("pazartesi", x[x.pzt]), ("diger", x[~x.pzt])):
    b, t = kr.nw_t(g.ibit_gap.values, np.column_stack([np.ones(len(g)), g.btc_gece.values]), 1)
    b2, t2 = kr.nw_t(g.ibit_id.values, np.column_stack([np.ones(len(g)), g.btc_gece.values]), 1)
    gap_rows.append({"ornek": nm, "n": len(g), "corr_gap_btcgece": g.ibit_gap.corr(g.btc_gece), "R2": g.ibit_gap.corr(g.btc_gece) ** 2,
                     "egim": b[1], "egim_t": t[1], "gunici_on_btcgece_egim": b2[1], "gunici_t": t2[1],
                     "corr_gunici_btcgece": g.ibit_id.corr(g.btc_gece)})
GP = pd.DataFrame(gap_rows)
GP.to_csv(os.path.join(kr.OUT, "ibit_bosluk_btc_gece.csv"), index=False)
print("\n=== IBIT açılış boşluğu ~ BTC 16:00->09:30 ET (gerçek zamanlı) ve IBIT gün içi ~ BTC gece ===")
print(GP.round(3).to_string(index=False))

# -------------------------------------------------------------------------------------------------
# KR04 haftalık momentum: g7 = 7 takvim günü getirisi, son 52 haftanın üst %20'si -> C0 h=3
def g7_signal(nm, top=True):
    if nm in ("BTC_D", "ETH_D"):
        raw = pd.read_parquet(os.path.join(kr.ROOT, "data", "crypto", ("BTC-USD" if nm == "BTC_D" else "ETH-USD") + ".parquet"))["c"]
        raw.index = pd.to_datetime(raw.index)
    else:
        raw = lib.btc_at_us_close("ETH-USD" if nm.startswith("ETH") else "BTC-USD")
    g = raw.pct_change(7)
    q = g.rolling(364, min_periods=300).quantile(0.8 if top else 0.2)
    s = (g >= q) if top else (g <= q)
    df = series(nm)
    return s.reindex(df.index).fillna(False)
for nm in ["BTC_D", "ETH_D", "BTC_ET", "ETH_ET"]:
    for mode in (("C0", "C1") if nm.endswith("_D") else ("C0", "O1", "C1")):
        add("KR04_hafta_mom_ust20_h3", nm, g7_signal(nm, True), 3, mode, "g7 >= son 52 hafta %80 dilimi")
        add("KR04_hafta_mom_alt20_h3", nm, g7_signal(nm, False), 3, mode, "kontrol: g7 <= %20 dilimi")
for etf, base in (("IBIT", "BTC_ET"), ("BITX", "BTC_ET"), ("ETHA", "ETH_ET")):
    sig = g7_signal(base, True).reindex(lib.load(etf).index).fillna(False)
    for mode in ("C0", "O1", "C1"):
        add("KR04_hafta_mom_ust20_h3", etf, sig, 3, mode, f"sinyal {base} 16:00 ET")
show("KR04_hafta_mom_ust20_h3"); show("KR04_hafta_mom_alt20_h3")

# -------------------------------------------------------------------------------------------------
# BTC fiyat desenleri (yönlendirme): 1 günlük z, 3 gün düşüş, 20 gün zirve kırılımı — dayanakta, sonra ETF'ye aktarım
c_ = lambda d: d["c"]
PAT = {
    "BTC_z1_lt_m2": lambda d: lib.zret(c_(d), 1) < -2,
    "BTC_z1_gt_p2": lambda d: lib.zret(c_(d), 1) > 2,
    "BTC_3gun_dusus": lambda d: (c_(d).diff() < 0) & (c_(d).diff().shift(1) < 0) & (c_(d).diff().shift(2) < 0),
    "BTC_20g_zirve": lambda d: c_(d) >= c_(d).rolling(20).max(),
    "BTC_20g_dip": lambda d: c_(d) <= c_(d).rolling(20).min(),
}
for pn, fn in PAT.items():
    for nm in ["BTC_D", "ETH_D", "BTC_ET", "ETH_ET"]:
        df = series(nm); sig = fn(df).fillna(False); sig.iloc[:60] = False
        for h in (1, 3):
            for mode in (("C0", "C1") if nm.endswith("_D") else ("C0", "O1", "C1")):
                add(pn, nm, sig, h, mode)
    # ETF'ye aktarım: sinyal BTC_ET (16:00 ET) -> IBIT/BITX ; ETH_ET -> ETHA
    for etf, base in (("IBIT", "BTC_ET"), ("BITX", "BTC_ET"), ("ETHA", "ETH_ET"), ("MSTU", "BTC_ET"), ("CONL", "BTC_ET"), ("BLOK", "BTC_ET")):
        bdf = series(base); sig = fn(bdf).fillna(False); sig.iloc[:60] = False
        sig = sig.reindex(lib.load(etf).index).fillna(False)
        for h in (1, 3):
            for mode in ("C0", "O1", "C1"):
                add(pn, etf, sig, h, mode, f"sinyal {base}")
    show(pn)

# -------------------------------------------------------------------------------------------------
# KR06 kaldıraçlı BTC/ETH kaybı: e_h = r_lev(t,t+h) - L*r_1x(t,t+h)
k6 = []
for lev, base, L in (("BITX", "IBIT", 2), ("BITU", "IBIT", 2), ("SBIT", "IBIT", -2), ("BITI", "IBIT", -1), ("ETHU", "ETHA", 2)):
    a = lib.load(lev)["c"]; b = lib.load(base)["c"]
    d = pd.DataFrame({"a": a, "b": b}).dropna()
    rb1 = d.b.pct_change()
    sig20 = rb1.rolling(20).std()
    for h in (1, 3):
        ra = d.a.shift(-h) / d.a - 1; rb = d.b.shift(-h) / d.b - 1
        e = (ra - L * rb).dropna()
        hi = sig20.reindex(e.index) >= 0.04
        k6.append({"lev": lev, "base": base, "L": L, "h": h, "n": len(e), "e_ort_bp": e.mean() * 1e4, "e_t": kr.tstat(e),
                   "e_ort_sigma20_ge4_bp": e[hi].mean() * 1e4, "n_sigma_ge4": int(hi.sum()),
                   "e_ort_sigma20_lt4_bp": e[~hi].mean() * 1e4, "medyan_bp": e.median() * 1e4})
K6 = pd.DataFrame(k6)
K6.to_csv(os.path.join(kr.OUT, "kaldirac_kaybi.csv"), index=False)
print("\n=== KR06 kaldıraç/ters ürün takip kaybı e_h = r_lev - L*r_1x (bp) ===")
print(K6.round(2).to_string(index=False))

# -------------------------------------------------------------------------------------------------
# Perşembe gün içi (genel kütüphanede FDR geçen tek 'negatif' takvim satırı) — dönem kontrolü
th = []
for nm in ["BTC_ET", "ETH_ET", "IBIT", "ETHA", "BITO", "BLOK", "SPY", "QQQ"]:
    df = series(nm); idr = df["c"] / df["o"] - 1
    for per, a, b in (("2016-2021", "2016-01-01", "2021-12-31"), ("2022-01..2023-05", "2022-01-01", "2023-05-31"), ("2023-06..2026-11", "2023-06-01", "2026-12-31")):
        z = idr[a:b]
        if len(z) < 50: continue
        zt = z[z.index.dayofweek == 3]; zo = z[z.index.dayofweek != 3]
        th.append({"seri": nm, "donem": per, "n_per": len(zt), "persembe_gunici_bp": zt.mean() * 1e4, "t": kr.tstat(zt), "diger_gunler_bp": zo.mean() * 1e4})
TH = pd.DataFrame(th); TH.to_csv(os.path.join(kr.OUT, "persembe_gunici.csv"), index=False)
print("\n=== Perşembe gün içi (O->C) dönem kontrolü ===")
print(TH.round(2).to_string(index=False))
for nm in ["SBIT", "BITI"]:
    df = lib.load(nm); wed = pd.Series(df.index.dayofweek == 2, index=df.index)
    add("PER_gunici_ters", nm, wed, 1, "O1", "Çarşamba sinyali -> Perşembe açılışta al, Perşembe kapanışta sat")
show("PER_gunici_ters")

# -------------------------------------------------------------------------------------------------
R = pd.DataFrame(ROWS)
R.to_csv(os.path.join(kr.OUT, "hipotez_testleri.csv"), index=False)
print("\nToplam hipotez satırı:", len(R))
