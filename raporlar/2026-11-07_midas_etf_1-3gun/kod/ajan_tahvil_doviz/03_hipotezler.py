"""3) Aileye özel hipotez testleri (notlar/hipotezler.csv TD01-TD09 + görev yönlendirmesi).
Çalıştır: python3 -I kod/ajan_tahvil_doviz/03_hipotezler.py
Tüm sinyaller t kapanışında bilinen bilgiyle; olay takvimleri önceden bilinir. Veri: td.load (dağıtım düzeltmeli).
Her satır = (hipotez, varyant, işlem ETF'i, mod, h) = 1 test. 'birincil'=True: literatürdeki/hipotez dosyasındaki ana kural.
Parametre taraması yok; yalnız literatür eşikleri ve birkaç komşu (açıkça 'komsu' etiketli).
Çıktılar: hipotez_testleri.csv (tüm satırlar + BH-FDR), hipotez_ozet.csv (birincil satırlar), fx_gun_saati.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib, strategies as S

pd.set_option("display.width", 260); pd.set_option("display.max_rows", 400); pd.set_option("display.max_columns", 40)
SPY = lib.load("SPY")
IDX = SPY.index
LASTFULL = pd.Timestamp("2026-10-31")   # Kasım 2026 eksik ay: ay sonu sinyalleri bu tarihten sonra üretilmez
ROWS = []

def ev(hyp, var, sym, sig, hs=(1, 2, 3), modes=("C0", "O1", "C1"), primary=None, beklenen="+", sinyal_kaynak=""):
    df = td.load(sym)
    sg = sig.reindex(df.index).fillna(False).astype(bool)
    for h in hs:
        for m in modes:
            s, tr = td.full_eval(df, sg, h, m, label=f"{hyp}|{var}", sym=sym, warm=60)
            r = td.row(s, {"hyp": hyp, "var": var, "beklenen": beklenen, "sinyal": sinyal_kaynak,
                           "birincil": bool(primary is not None and (h, m) == primary)})
            ROWS.append(r)

def me_k(idx, k):
    s = S.month_nth_from_end(idx, k)
    return s & (idx <= LASTFULL)

# ---------------- TD01: TLT ay sonu ----------------
TL = td.load("TLT")
me4 = me_k(TL.index, 4); me3 = me_k(TL.index, 3)
for sym in ["TLT", "EDV", "ZROZ", "TLH", "IEF", "GOVT", "AGG", "LQD", "TIP", "MUB", "EMB", "HYG", "SHY", "TMF", "UBT", "TMV", "TBT"]:
    bek = "-" if sym in ("TMV", "TBT") else "+"
    # Hartley & Schwarz: sondan 4. gün kapanışında gir, son 3 gün tut (çıkış ay son günü kapanışı)
    ev("TD01_ay_sonu", "k4_h3_son_gun", sym, me4, hs=(3,), primary=(3, "C0"), beklenen=bek, sinyal_kaynak="takvim")
    # görev yönlendirmesi: sondan 3. gün kapanışında gir -> ay son günü (h=2) / yeni ayın ilk günü (h=3)
    ev("TD01_ay_sonu", "k3", sym, me3, hs=(2, 3), beklenen=bek, sinyal_kaynak="takvim")
# ay başı (ilk 3 gün) tersine dönüş: ayın son günü kapanışında TBT/TMV
mlast = me_k(TL.index, 1)
for sym in ["TLT", "TMV", "TBT"]:
    ev("TD01b_ay_basi_donus", "son_gun_h3", sym, mlast, hs=(1, 3), modes=("C0",), beklenen="-" if sym == "TLT" else "+", sinyal_kaynak="takvim")

# ---------------- TD02: Hazine ihale döngüsü ----------------
a10 = td.events("hazine_ihale_10y30y", ["UST10Y_ihale"]); a30 = td.events("hazine_ihale_10y30y", ["UST30Y_ihale"])
A10 = td.ev_on_idx(a10, IDX); A30 = td.ev_on_idx(a30, IDX)
pre10 = td.ev_on_idx(a10, IDX, -3)      # C_{A-3} -> C_{A-1}: ihale öncesi zayıflık (h=2)
for sym in ["TLT", "TLH", "IEF", "EDV", "TMF"]:
    ev("TD02_ihale_sonrasi", "A30_h2", sym, A30, hs=(1, 2), primary=(2, "C0"), sinyal_kaynak="takvim")
    ev("TD02_ihale_sonrasi", "A10_h2", sym, A10, hs=(1, 2), sinyal_kaynak="takvim")
for sym in ["TLT", "IEF", "TBT", "TMV"]:
    ev("TD02_ihale_oncesi", "A10-3_h2", sym, pre10, hs=(2,), primary=(2, "C0"), beklenen="-" if sym in ("TLT", "IEF") else "+",
       sinyal_kaynak="takvim")

# ---------------- TD03: FOMC çevresi ----------------
fomc = td.events("fomc", ["FOMC_karar"])
Dm2 = td.ev_on_idx(fomc, IDX, -2); Dm1 = td.ev_on_idx(fomc, IDX, -1)
for sym in ["TLT", "IEF", "EDV", "AGG", "TMF", "TMV"]:
    bek = "-" if sym == "TMV" else "+"
    ev("TD03_FOMC", "D-2_h3", sym, Dm2, hs=(3,), primary=(3, "C0"), beklenen=bek, sinyal_kaynak="takvim")
    ev("TD03_FOMC", "D-1_h1", sym, Dm1, hs=(1,), beklenen=bek, sinyal_kaynak="takvim")

# ---------------- TD04: CPI / NFP günleri ----------------
cpi = td.events("cpi", ["CPI"]); nfp = td.events("nfp", ["NFP"])
pre_cpi = td.ev_on_idx(cpi, IDX, -1); pre_nfp = td.ev_on_idx(nfp, IDX, -1)
pre_both = pre_cpi | pre_nfp
for sym in ["TLT", "IEF", "TMF", "TMV"]:
    bek = "-" if sym == "TMV" else "+"
    ev("TD04_CPI_NFP", "CPI_veya_NFP", sym, pre_both, hs=(1,), primary=(1, "C0"), beklenen=bek, sinyal_kaynak="takvim")
    ev("TD04_CPI_NFP", "yalniz_CPI", sym, pre_cpi, hs=(1,), beklenen=bek, sinyal_kaynak="takvim")
    ev("TD04_CPI_NFP", "yalniz_NFP", sym, pre_nfp, hs=(1,), beklenen=bek, sinyal_kaynak="takvim")

# ---------------- TD10: TLT IBS / RSI2 iki yönlü dönüş (sinyal TLT verisinden) ----------------
rs = lib.rsi(TL["c"], 2); ib = lib.ibs(TL)
lo_rsi = rs < 10; hi_rsi = rs > 90; lo_ibs = ib < 0.2; hi_ibs = ib > 0.8
for sym in ["TLT", "TMF", "UBT", "EDV"]:
    ev("TD10_TLT_donus", "RSI2<10_long", sym, lo_rsi, primary=(3, "C0") if sym == "TLT" else None, sinyal_kaynak="NASDAQ:TLT RSI2")
    ev("TD10_TLT_donus", "IBS<0.2_long", sym, lo_ibs, primary=(1, "C0") if sym == "TLT" else None, sinyal_kaynak="NASDAQ:TLT IBS")
for sym in ["TMV", "TBT"]:
    ev("TD10_TLT_donus", "RSI2>90_ters", sym, hi_rsi, primary=(3, "C0") if sym == "TMV" else None, sinyal_kaynak="NASDAQ:TLT RSI2")
    ev("TD10_TLT_donus", "IBS>0.8_ters", sym, hi_ibs, primary=(1, "C0") if sym == "TMV" else None, sinyal_kaynak="NASDAQ:TLT IBS")

# ---------------- TD11: 10 yıllık getiri değişimi z-skoru ----------------
y10 = td.yld("DGS10").ffill(); dy = y10.diff(); z1 = dy / dy.rolling(60).std()
dy3 = y10.diff(3); z3 = dy3 / (dy.rolling(60).std() * math.sqrt(3))
for sym in ["TLT", "IEF", "TMF"]:
    ev("TD11_faiz_z", "dDGS10_z>=2_TLTal(donus)", sym, z1 >= 2, primary=(1, "C0") if sym == "TLT" else None, sinyal_kaynak="TVC:US10Y")
    ev("TD11_faiz_z", "dDGS10_z<=-2_TLTal(momentum)", sym, z1 <= -2, beklenen="?", sinyal_kaynak="TVC:US10Y")
    ev("TD11_faiz_z", "dDGS10_3g_z>=2_TLTal", sym, z3 >= 2, hs=(3,), sinyal_kaynak="TVC:US10Y")
for sym in ["TMV", "TBT"]:
    ev("TD11_faiz_z", "dDGS10_z<=-2_TERSal(donus)", sym, z1 <= -2, primary=(1, "C0") if sym == "TMV" else None, sinyal_kaynak="TVC:US10Y")
    ev("TD11_faiz_z", "dDGS10_3g_z<=-2_TERSal", sym, z3 <= -2, hs=(3,), sinyal_kaynak="TVC:US10Y")

# ---------------- TD05: FOMC günü döviz ----------------
for sym in ["FXA", "UDN", "FXE", "FXB", "FXC", "UUP"]:
    ev("TD05_FOMC_doviz", "D-1_h1", sym, Dm1, hs=(1,), primary=(1, "C0"), beklenen="-" if sym == "UUP" else "+", sinyal_kaynak="takvim")

# ---------------- TD06: ay sonu USD hedge dengelemesi ----------------
spc = SPY["c"]
ml = S.month_last_day(IDX)
prev_ml = spc.where(ml).ffill().shift(1)            # önceki ayın son kapanışı (t'de bilinir)
# shift(1) ayın son günündeki değeri o güne değil sonraki güne taşır; ay içinde değişmez
prev_ml = spc.where(ml).shift(1).ffill()
mtd = spc / prev_ml - 1
k3 = me_k(IDX, 3)
up = k3 & (mtd >= 0.03); dn = k3 & (mtd <= -0.03)
for sym in ["FXE", "UDN", "FXB", "FXA"]:
    ev("TD06_ay_sonu_USD", "SPY_ay_ici>=+3%", sym, up, hs=(2,), primary=(2, "C0"), sinyal_kaynak="AMEX:SPY ay içi getiri")
ev("TD06_ay_sonu_USD", "SPY_ay_ici<=-3%", "UUP", dn, hs=(2,), primary=(2, "C0"), sinyal_kaynak="AMEX:SPY ay içi getiri")
ev("TD06_ay_sonu_USD", "SPY_ay_ici>=+3%_UUP", "UUP", up, hs=(2,), beklenen="-", sinyal_kaynak="AMEX:SPY ay içi getiri")

# ---------------- TD07: FXY güvenli liman ----------------
vix = lib.vol_index("VIX").reindex(IDX)
rspy = spc.pct_change()
shock = (rspy <= -0.02) | (vix / vix.shift(1) - 1 >= 0.20)
for sym in ["FXY", "FXF", "YCL"]:
    ev("TD07_FXY_guvenli_liman", "SPY<=-2%_veya_VIX+20%", sym, shock, hs=(1, 2), primary=(2, "C0") if sym == "FXY" else None,
       sinyal_kaynak="AMEX:SPY, CBOE:VIX")

# ---------------- TD12: USDJPY <- DGS2 değişimi ----------------
y2 = td.yld("DGS2").ffill(); d2 = y2.diff(); z2 = d2 / d2.rolling(60).std()
ev("TD12_JPY_DGS2", "dDGS2_z>=1.5_YCS", "YCS", z2 >= 1.5, primary=(1, "C0"), sinyal_kaynak="TVC:US02Y")
ev("TD12_JPY_DGS2", "dDGS2_z>=1.5_FXY", "FXY", z2 >= 1.5, beklenen="-", sinyal_kaynak="TVC:US02Y")
ev("TD12_JPY_DGS2", "dDGS2_z<=-1.5_FXY", "FXY", z2 <= -1.5, primary=(1, "C0"), sinyal_kaynak="TVC:US02Y")
ev("TD12_JPY_DGS2", "dDGS2_z<=-1.5_YCL", "YCL", z2 <= -1.5, sinyal_kaynak="TVC:US02Y")

# ---------------- TD09: bakır/altın -> faiz ----------------
cp = lib.load("CPER")["c"].reindex(IDX); gl = lib.load("GLD")["c"].reindex(IDX)
ratio = cp / gl; xr = ratio / ratio.shift(5) - 1
for sym in ["TBT", "TMV", "TLT"]:
    ev("TD09_bakir_altin", "CPER/GLD_5g>=+3%", sym, xr >= 0.03, hs=(3,), primary=(3, "C0") if sym == "TBT" else None,
       beklenen="-" if sym == "TLT" else "+", sinyal_kaynak="AMEX:CPER/AMEX:GLD (vadeli: COMEX:HG1!/COMEX:GC1!)")

# ---------------- TD13: HYG/JNK <- SPY (sert SPY düşüşü sonrası HY) ----------------
zs = lib.zret(spc, 1)
for sym in ["HYG", "JNK", "USHY"]:
    ev("TD13_HY_SPY", "SPY_z1<=-1.5", sym, zs <= -1.5, primary=(1, "C0") if sym == "HYG" else None, sinyal_kaynak="AMEX:SPY")
    ev("TD13_HY_SPY", "SPY_z1>=+1.5", sym, zs >= 1.5, beklenen="-", sinyal_kaynak="AMEX:SPY")

# ---------------- TD14: döviz kısa vadeli momentum/dönüş (5 günlük) ----------------
for sym in ["UUP", "FXE", "FXY", "FXB", "FXA", "FXC", "FXF"]:
    d = td.load(sym); z5 = lib.zret(d["c"], 5)
    ev("TD14_doviz_5g", "z5>=1.5_momentum", sym, z5 >= 1.5, hs=(3,), beklenen="?", sinyal_kaynak="kendi")
    ev("TD14_doviz_5g", "z5<=-1.5_donus", sym, z5 <= -1.5, hs=(3,), beklenen="?", sinyal_kaynak="kendi")

res = pd.DataFrame(ROWS)
res["fdr10"] = lib.bh_fdr(res["p"].values, 0.10)
# yön-uyumlu (tek yönlü) p: beklenen '+' ise net>0 hipotezi
res["p1"] = np.where(res["t"] > 0, res["p"] / 2, 1 - res["p"] / 2)
res["fdr10_tek"] = lib.bh_fdr(res["p1"].values, 0.10)
res["kabul"] = [td.passes(r) for _, r in res.iterrows()]
res.to_csv(os.path.join(td.OUT, "hipotez_testleri.csv"), index=False)
N = len(res)
print("Toplam hipotez testi:", N, " iki yönlü FDR geçen:", int(res.fdr10.sum()), " (pozitif net:", int((res.fdr10 & (res.mean_net_bp > 0)).sum()),
      ") tek yönlü FDR geçen:", int(res.fdr10_tek.sum()), " eşik geçen (n/net/t/IS/OOS/yıl):", int(res.kabul.sum()))
cols = ["hyp", "var", "sym", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_bp_1000", "net_bp_10000", "win", "pf", "t", "is_net_bp",
        "oos_net_bp", "years_pos_frac", "maxdd", "worst_bp", "fdr10", "kabul"]
pr = res[res.birincil]
pr.to_csv(os.path.join(td.OUT, "hipotez_ozet.csv"), index=False)
print("\nBİRİNCİL kurallar:")
print(pr[cols].round(2).to_string(index=False))
print("\nEşiği geçen tüm satırlar:")
print(res[res.kabul][cols].round(2).to_string(index=False))
print("\nEn yüksek t (net) ilk 30:")
print(res.sort_values("t", ascending=False)[cols].head(30).round(2).to_string(index=False))

# ---------------- TD08: döviz gün saati (gece vs gün içi) ----------------
fx = []
for sym in ["UUP", "FXE", "FXY", "FXF", "FXB"]:
    d = td.load(sym)
    on = np.log(d["o"] / d["c"].shift(1)).dropna(); idy = np.log(d["c"] / d["o"]).dropna()
    for nm, r in (("gece_C->O", on), ("gun_ici_O->C", idy)):
        for per, m in (("tum", r.index > r.index[0]), ("IS", r.index <= lib.IS_END), ("OOS", r.index > lib.IS_END)):
            x = r[m]
            fx.append({"sym": sym, "parca": nm, "donem": per, "n": len(x), "ort_bp": x.mean() * 1e4, "t": td._t(x.values),
                       "maliyet_bp": td.cost_at(d)})
fx = pd.DataFrame(fx)
fx.to_csv(os.path.join(td.OUT, "fx_gun_saati.csv"), index=False)
print("\nTD08 döviz gün saati (her gün; maliyet gidiş-dönüş):")
print(fx.round(2).to_string(index=False))
