"""Görev 3: Aileye özel hipotezler (hipotezler.csv TH01-TH06 + yönlendirme). Bilanço (TH04) ayrı: t5_bilanco.py.
Her kural önce dayanak hissede (sentetik kalibre 2x / ters, 2016-11..2026-11; IS<=2021, OOS 2022+) test edilir; ön-kayıtlı ana
varyant (hipotezler.csv'deki giriş/çıkış) 'on_kayitli' ile işaretlenir, diğer C0/O1/C1 x h varyantları sağlamlık içindir.
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t4_hipotez.py
Çıktılar: hipotez_testleri.csv (tüm satırlar), th01_oynaklik_kaybi.csv, th06_btc_regresyon.csv, smh_nvda_regresyon.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib, hrun
from hrun import S

pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)

def r1(sdf): return sdf["c"].pct_change()
def sig20(sdf): return r1(sdf).rolling(20).std().shift(1)   # t-1'e kadarki 20 günlük std (t'nin kendisi hariç)

# ---------------- TH01: oynaklık / yol kaybı ölçümü (gerçek ETF, kaldıraç geçişi sonrası) ----------------
SWITCH = {"NVDL": "2024-02-01", "NVDU": "2024-04-15", "TSLL": "2024-04-10", "CONL": "2024-02-01", "AAPU": "2024-04-10",
          "AMZU": "2024-04-15", "MSFU": "2024-04-10", "GGLL": "2024-04-10", "MSTU": "2024-09-19", "METU": "2024-06-06",
          "TSLQ": "2024-07-25", "NVDS": "2024-07-25"}
LNOW = {e: float(thk.tarama().loc[e, "lev"]) for e in thk.FAM}
LNOW["TSLQ"] = -2.0   # tarama.csv 'lev' -1 diyor; 2024-07 sonrası gerçekleşen beta -2.0 (t1: kaldirac_yillik.csv)
rows = []
for e in thk.FAM:
    d = lib.load(e); st = thk.UNDER[e]; s = S(st).reindex(d.index)
    L = LNOW[e]
    sg = s["c"].pct_change().rolling(20).std()
    for h in (1, 2, 3):
        Re = d["c"].shift(-h) / d["c"] - 1; Rs = s["c"].shift(-h) / s["c"] - 1
        z = pd.DataFrame({"Re": Re, "Rs": Rs, "sg": sg}).loc[SWITCH[e]:].dropna()
        z = z.iloc[::h]   # çakışmayan pencereler
        es = z.Re - L * z.Rs
        el = np.log1p(z.Re) - L * np.log1p(z.Rs)
        pred = -((L * L - L) / 2) * h * z.sg ** 2
        for b, zz in [("tum", z.index)] + [(f"sg_q{q}", z.index[pd.qcut(z.sg, 3, labels=False) == q]) for q in range(3)]:
            rows.append({"etf": e, "L": L, "h": h, "kova": b, "n": len(zz), "sg_ort_bp": z.sg.loc[zz].mean() * 1e4,
                         "basit_sapma_ort_bp": es.loc[zz].mean() * 1e4, "basit_sapma_t": es.loc[zz].mean() / (es.loc[zz].std() / math.sqrt(len(zz))) if len(zz) > 2 else np.nan,
                         "basit_sapma_std_bp": es.loc[zz].std() * 1e4,
                         "log_sapma_ort_bp": el.loc[zz].mean() * 1e4, "log_tahmin_bp": pred.loc[zz].mean() * 1e4,
                         "basit_sapma_p05_bp": es.loc[zz].quantile(0.05) * 1e4})
TH01 = pd.DataFrame(rows); TH01.to_csv(os.path.join(thk.OUT, "th01_oynaklik_kaybi.csv"), index=False)
print("TH01 (tum kova):"); print(TH01[TH01.kova == "tum"].round(1).to_string())
print(TH01[(TH01.h == 3)].pivot(index="etf", columns="kova", values="basit_sapma_ort_bp").round(1).to_string())

# ---------------- TH02: büyük hareket sonrası dönüş ----------------
big_dn = lambda st, sdf: r1(sdf) <= -2.5 * sig20(sdf)
big_up = lambda st, sdf: r1(sdf) >= 2.5 * sig20(sdf)
K4 = ["NVDA", "TSLA", "MSTR", "COIN"]; K5 = ["AAPL", "AMZN", "META", "MSFT", "GOOGL"]
hrun.run("TH02a_buyuk_dusus_long_4", big_dn, K4, primary=("C0", 2), note="hipotezler.csv: r<=-2.5σ20 -> 2x long C_t, çıkış C_t+2")
hrun.run("TH02a_buyuk_dusus_long_diger5", big_dn, K5, primary=("C0", 2), note="aile kontrolü (diğer 5 dayanak)")
hrun.run("TH02b_buyuk_yukselis_long_4", big_up, K4, primary=("C0", 2), note="beklenti: negatif (dönüş) -> mevcut long kapatılır")
hrun.run("TH02c_buyuk_yukselis_ters", big_up, ["TSLA"], L=-2.0, primary=("C0", 2), cost_etf={"TSLA": "TSLQ"}, note="TSLQ (-2x) sentetik")
hrun.run("TH02c_buyuk_yukselis_ters_nvda", big_up, ["NVDA"], L=-1.5, primary=("C0", 2), cost_etf={"NVDA": "NVDS"}, note="NVDS (-1.5x) sentetik")

# ---------------- TH03: hisse RSI(2)<10 & C>SMA200, çıkış hisse C>SMA5 (en fazla 3 gün) ----------------
rsi_tr = lambda st, sdf: (lib.rsi(sdf["c"], 2) < 10) & (sdf["c"] > lib.sma(sdf["c"], 200))
ex_sma5 = lambda st, sdf: sdf["c"] > lib.sma(sdf["c"], 5)
K7 = ["NVDA", "TSLA", "AAPL", "AMZN", "META", "MSFT", "GOOGL"]
hrun.run("TH03_rsi2_trend_sma5cikis", rsi_tr, K7, hs=(3,), exit_fn=ex_sma5, primary=("C0", 3), note="hipotezler.csv TH03")
hrun.run("TH03_rsi2_trend_sma5cikis_kripto", rsi_tr, ["MSTR", "COIN"], hs=(3,), exit_fn=ex_sma5, primary=("C0", 3), note="aile kontrolü")
# TH01 kuralı: tahmini 3 günlük log kaybı >%0.5 (σ20 > ~%4.1) ise tutuş 1 gün -> TH03 üzerinde
def ex_sma5_or_hv(st, sdf):
    sg = r1(sdf).rolling(20).std()
    hv = (3 * sg ** 2) > 0.005
    return ex_sma5(st, sdf) | hv.shift(1).fillna(False)   # yüksek oynaklıkta ilk kapanışta çık
hrun.run("TH01_kurali_TH03_uzerinde", rsi_tr, K7 + ["MSTR", "COIN"], hs=(3,), exit_fn=ex_sma5_or_hv, primary=("C0", 3), note="TH01 kuralı: σ yüksekse 1 gün")

# ---------------- TH05: opsiyon vadesi öncesi Cuma -> OE haftası Çarşamba ----------------
ox = pd.read_csv(os.path.join(thk.ROOT, "data", "events", "opex.csv"), parse_dates=["date"])
idx = S("NVDA").index
pos = pd.Series(np.arange(len(idx)), index=idx)
sig_d = pd.Series(False, index=idx); ex_d = pd.Series(False, index=idx)
for E in ox["date"]:
    if E < idx[0] or E > idx[-1]: continue
    fri = E - pd.Timedelta(days=7)
    a = idx[idx <= fri]
    wed = E - pd.Timedelta(days=(E.dayofweek - 2) % 7)
    b = idx[(idx <= wed) & (idx > fri)]
    if len(a) and len(b):
        sig_d[a[-1]] = True; ex_d[b[-1]] = True
opex_sig = lambda st, sdf: sig_d.reindex(sdf.index).fillna(False)
opex_ex = lambda st, sdf: ex_d.reindex(sdf.index).fillna(False)
hrun.run("TH05_opex_haftasi", opex_sig, ["NVDA", "TSLA", "AAPL"], hs=(5,), exit_fn=opex_ex, primary=("C0", 5), note="çıkış OE haftası Çarşamba kapanışı")
hrun.run("TH05_opex_haftasi_diger", opex_sig, ["MSTR", "COIN", "AMZN", "META", "MSFT", "GOOGL"], hs=(5,), exit_fn=opex_ex, primary=("C0", 5), note="aile kontrolü")

# ---------------- TH07 (ek, ters ETF): aşırı alım (RSI2>90) + hisse SMA200 altında -> ters ETF ----------------
ob_bear = lambda st, sdf: (lib.rsi(sdf["c"], 2) > 90) & (sdf["c"] < lib.sma(sdf["c"], 200))
hrun.run("TH07_ters_rsi2_gt90_ayi_tsla", ob_bear, ["TSLA"], L=-2.0, primary=("C0", 2), cost_etf={"TSLA": "TSLQ"}, note="ek hipotez (ters)")
hrun.run("TH07_ters_rsi2_gt90_ayi_nvda", ob_bear, ["NVDA"], L=-1.5, primary=("C0", 2), cost_etf={"NVDA": "NVDS"}, note="ek hipotez (ters)")

# ---------------- TH06: BTC@16:00 ET artığı -> MSTR / COIN ertesi gün ----------------
def nw(y, X, lags=5):
    X = np.column_stack([np.ones(len(y)), X]); n, k = X.shape
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b; u = X * e[:, None]; Sm = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; Sm += w * (G + G.T)
    V = xtx @ Sm @ xtx
    return b, b / np.sqrt(np.diag(V))

btc = lib.btc_at_us_close("BTC-USD")
regs = []
U = {}
for st in ["MSTR", "COIN"]:
    sdf = S(st)
    rb = np.log(btc.reindex(sdf.index)).diff()
    rs = np.log(sdf["c"]).diff()
    beta = rs.rolling(60).cov(rb) / rb.rolling(60).var()
    u = rb - beta * rs      # hipotez tanımı: u = r_BTC - β60 x r_hisse (β: hisse->BTC eğimi değil; aşağıda alternatif de var)
    bet2 = rb.rolling(60).cov(rs) / rb.rolling(60).var()
    gap = bet2 * rb - rs    # yetişme: hissenin BTC'ye göre geride kalışı
    fwd1 = rs.shift(-1); fwd3 = rs.shift(-1) + rs.shift(-2) + rs.shift(-3)
    fwdg = np.log(sdf["o"].shift(-1) / sdf["c"])  # ertesi açılış boşluğu
    for nm, x in [("u_TH06", u), ("r_btc", rb), ("yetisme_gap", gap)]:
        for hn, y in [("h1", fwd1), ("h3", fwd3), ("gap_t+1", fwdg)]:
            z = pd.DataFrame({"y": y, "x": x, "own": rs}).dropna()
            if len(z) < 100: continue
            b, t = nw(z.y.values, z[["x", "own"]].values, 5 if hn != "h3" else 8)
            sdx = z.x.std()
            regs.append({"hisse": st, "x": nm, "y": hn, "n": len(z), "basla": z.index[0].date(), "b_x": b[1], "t_x": t[1],
                         "b_own": b[2], "t_own": t[2], "bp_per_sd": b[1] * sdx * 1e4})
    U[st] = (u, gap, rb)
REGB = pd.DataFrame(regs); REGB.to_csv(os.path.join(thk.OUT, "th06_btc_regresyon.csv"), index=False)
print("\nTH06 BTC regresyonları (2023-06+, kendi gecikmesi kontrollü, NW):"); print(REGB.round(3).to_string())

def th06_sig(kind):
    def f(st, sdf):
        u, gap, rb = U[st]
        x = u if kind == "u" else gap
        sd = x.rolling(60).std().shift(1)
        return (x >= 2 * sd).reindex(sdf.index).fillna(False)
    return f
hrun.run("TH06_btc_artik_u_ge2sd", th06_sig("u"), ["MSTR", "COIN"], hs=(1, 2, 3), primary=("C0", 1), cost_etf={"MSTR": "MSTU", "COIN": "CONL"}, note="2023-06+ (BTC 16:00 ET verisi); IS yok")
hrun.run("TH06_btc_yetisme_ge2sd", th06_sig("gap"), ["MSTR", "COIN"], hs=(1, 2, 3), primary=("C0", 1), cost_etf={"MSTR": "MSTU", "COIN": "CONL"}, note="2023-06+; IS yok")

# BTC gece hareketi -> hisse açılış boşluğu (gerçek zamanlı izleme gücü)
h1 = pd.read_parquet(os.path.join(thk.ROOT, "data", "crypto", "BTC-USD_h1.parquet"))
hh = h1.copy(); hh.index = hh.index.tz_convert("America/New_York")
b09 = hh[hh.index.hour == 9]["o"]; b09.index = b09.index.tz_localize(None).normalize(); b09 = b09[~b09.index.duplicated(keep="last")]
night = []
for st in ["MSTR", "COIN"]:
    sdf = S(st)
    rb16 = btc.reindex(sdf.index)
    rn = np.log(b09.reindex(sdf.index) / rb16.shift(1))     # BTC: t-1 16:00 -> t 09:00 ET
    g = np.log(sdf["o"] / sdf["c"].shift(1))
    z = pd.DataFrame({"rn": rn, "g": g}).dropna()
    bb = np.cov(z.g, z.rn)[0, 1] / z.rn.var()
    night.append({"hisse": st, "n": len(z), "corr_btc_gece_vs_acilis_boslugu": z.g.corr(z.rn), "beta": bb, "r2": z.g.corr(z.rn) ** 2})
NIGHT = pd.DataFrame(night); NIGHT.to_csv(os.path.join(thk.OUT, "btc_gece_acilis.csv"), index=False)
print(NIGHT.round(3).to_string())

# ---------------- SMH -> NVDA (NVDL) öncülüğü / yetişme ----------------
smh = lib.load("SMH")["c"]
nv = S("NVDA")
rsm = np.log(smh.reindex(nv.index)).diff(); rn_ = np.log(nv["c"]).diff()
bet = rn_.rolling(60).cov(rsm) / rsm.rolling(60).var()
gapn = bet * rsm - rn_
sreg = []
for nm, x in [("r_smh", rsm), ("yetisme_gap", gapn)]:
    for hn, k in [("h1", 1), ("h3", 3)]:
        y = sum(rn_.shift(-i) for i in range(1, k + 1))
        for per, sl in [("tum", slice(None)), ("IS", slice(None, "2021-12-31")), ("OOS", slice("2022-01-01", None))]:
            z = pd.DataFrame({"y": y, "x": x, "own": rn_}).dropna().loc[sl]
            b, t = nw(z.y.values, z[["x", "own"]].values, 5 if k == 1 else 8)
            sreg.append({"x": nm, "y": hn, "donem": per, "n": len(z), "b_x": b[1], "t_x": t[1], "b_own": b[2], "t_own": t[2],
                         "bp_per_sd": b[1] * z.x.std() * 1e4})
SREG = pd.DataFrame(sreg); SREG.to_csv(os.path.join(thk.OUT, "smh_nvda_regresyon.csv"), index=False)
print("\nSMH -> NVDA (kendi gecikmesi kontrollü):"); print(SREG.round(3).to_string())
def smh_catch(st, sdf):
    sd = gapn.rolling(60).std().shift(1)
    return (gapn >= 2 * sd).reindex(sdf.index).fillna(False)
hrun.run("SMH_NVDA_yetisme_ge2sd", smh_catch, ["NVDA"], hs=(1, 2, 3), primary=("C0", 1), note="NVDL ← SMH (yönlendirme)")

# ---------------- kayıt + FDR ----------------
REG = pd.DataFrame(hrun.REG)
pool = REG[REG.duzey == "havuz"].copy()
pool["fdr_havuz"] = lib.bh_fdr(pool["p"].values, 0.10)
REG = REG.merge(pool[["hipotez", "varyant", "L", "fdr_havuz"]], on=["hipotez", "varyant", "L"], how="left")
REG["fdr_hisse"] = False
m = REG.duzey == "hisse"
REG.loc[m, "fdr_hisse"] = lib.bh_fdr(REG.loc[m, "p"].values, 0.10)
REG.to_csv(os.path.join(thk.OUT, "hipotez_testleri.csv"), index=False)
cols = ["hipotez", "stock", "mode", "h", "on_kayitli", "n", "n_tarih", "mean_gross_bp", "mean_net_bp", "t", "edge_bp", "t_edge",
        "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac", "win", "worst_bp", "hisse_pozitif", "hisse_k", "fdr_havuz"]
print("\nHavuz düzeyi hipotez testleri:", len(pool), " FDR geçen:", int(pool.fdr_havuz.sum()), "| hisse düzeyi:", int(m.sum()), " FDR geçen:", int(REG.loc[m, "fdr_hisse"].sum()))
print(REG[REG.duzey == "havuz"][cols].round(2).to_string())
