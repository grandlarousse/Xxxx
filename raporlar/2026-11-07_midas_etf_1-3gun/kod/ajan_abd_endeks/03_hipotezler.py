"""3) Aileye özel hipotez testleri (hipotezler.csv AE01-AE15 + yönlendirme). Çalıştır:
   python3 -I kod/ajan_abd_endeks/03_hipotezler.py
Çıktı: sonuclar/aile_abd_endeks/hipotez_testleri.csv (her satır bir test: hipotez x varyant x sinyal ETF x işlem ETF x mod x h),
       sonuclar/aile_abd_endeks/hipotez_ozet.csv (hipotez x varyant x mod x h: aile içi tutarlılık),
       sonuclar/aile_abd_endeks/gece_gunici.csv (AE14 ölçümü).
Tüm testler kendi BH-FDR (q=0.10) kümesine girer. Parametreler hipotez dosyasındaki/literatürdeki varsayılanlar; TARAMA YOK."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ae, lib
from lib import rsi, ibs, sma, zret

U = ae.CORE                       # SPY QQQ IWM DIA RSP MDY
D = {s: lib.load(s) for s in set(ae.FAM)}
X = ae.ctx()
VIX = X["VIX"]; VIX3M = X["VIX3M"]
SPY = D["SPY"]
ROWS = []

def run(hyp, var, sig_sym, sig, trade_sym=None, hs=(1, 2, 3), modes=("C0", "O1", "C1"), exit_fn=None, note=""):
    trade_sym = trade_sym or sig_sym
    df = D[trade_sym]
    s_al = sig.reindex(df.index).fillna(False).astype(bool)
    ex = None if exit_fn is None else exit_fn.reindex(df.index).fillna(False).astype(bool)
    for h in hs:
        for m in modes:
            s, tr = ae.full_eval(df, s_al, h, m, exit_sig=ex, label=f"{hyp}|{var}", sym=trade_sym)
            r = ae.row(s, {"hyp": hyp, "var": var, "sig_sym": sig_sym, "trade_sym": trade_sym, "exit": "kural" if ex is not None else "sabit",
                           "note": note})
            ROWS.append(r)

def c(s): return D[s]["c"]
def ret(s): return c(s).pct_change()

# ---------- AE01 IBS<0.2, 1 gün ----------
for s in U:
    run("AE01_IBS_dusuk", "ibs<0.2", s, ibs(D[s]) < 0.2, hs=(1,))
# ---------- AE02 IBS>0.8 (long beklenen negatif) + ters ETF ile uygulama ----------
for s in U:
    run("AE02_IBS_yuksek", "ibs>0.8 long (beklenen<0)", s, ibs(D[s]) > 0.8, hs=(1,))
for base, invs in ae.INV.items():
    for inv, L in invs:
        run("AE02_IBS_yuksek", f"ibs>0.8 ters ETF {L}x", base, ibs(D[base]) > 0.8, trade_sym=inv, hs=(1,))
# ---------- AE03 RSI2<10 & >SMA200, çıkış C>SMA5 (en çok 3 gün) ----------
for s in U:
    cc = c(s)
    run("AE03_RSI2", "rsi2<10 & c>sma200, cikis c>sma5 max3", s, (rsi(cc, 2) < 10) & (cc > sma(cc, 200)), hs=(3,),
        exit_fn=cc > sma(cc, 5))
# ---------- AE04 RSI4<25 & >SMA200, çıkış RSI4>55 (en çok 3) ----------
for s in U:
    cc = c(s)
    run("AE04_RSI4_25", "rsi4<25 & c>sma200, cikis rsi4>55 max3", s, (rsi(cc, 4) < 25) & (cc > sma(cc, 200)), hs=(3,),
        exit_fn=rsi(cc, 4) > 55)
# ---------- AE05 3 ardışık düşüş & >SMA200, çıkış ilk yükseliş (en çok 3) ----------
for s in U:
    cc = c(s); d1 = cc.diff()
    run("AE05_3gun_dusus", "3 dusus & c>sma200, cikis ilk yukselis max3", s,
        (d1 < 0) & (d1.shift(1) < 0) & (d1.shift(2) < 0) & (cc > sma(cc, 200)), hs=(3,), exit_fn=d1 > 0)
# ---------- AE06 Turnaround Tuesday ----------
for s in U:
    idx = D[s].index
    run("AE06_Turnaround_Tuesday", "pzt r<=-1.5%", s, pd.Series(idx.dayofweek == 0, index=idx) & (ret(s) <= -0.015), hs=(1,))
# ---------- AE07 Ay dönümü ----------
import strategies as S
for s in U:
    idx = D[s].index
    run("AE07_ay_donumu", "t=sondan 2. gun, 3 gun tut", s, S.month_nth_from_end(idx, 2), hs=(3,))
    run("AE07_ay_donumu", "t=son gun, yeni ayin ilk 3 gunu", s, S.month_nth_from_end(idx, 1), hs=(3,))
# ---------- AE08 pre-FOMC ----------
fomc = ae.events("fomc", ["FOMC_karar"])
for s in U:
    idx = D[s].index
    dset = idx[idx.isin(fomc)]
    pos = idx.get_indexer(dset)
    pre = pd.Series(False, index=idx); pre.iloc[pos[pos > 0] - 1] = True
    run("AE08_pre_FOMC", "t=FOMC-1 (C0: D-1 kapanis->D kapanis)", s, pre, hs=(1,))
# ---------- AE09 Makro duyuru günü (t+1 = CPI / NFP / FOMC) ----------
cpi = ae.events("cpi", ["CPI"]); nfp = ae.events("nfp", ["NFP"])
for s in U:
    idx = D[s].index
    nxt = pd.Series(idx, index=idx).shift(-1)
    for nm, ev in (("CPI", cpi), ("NFP", nfp), ("CPI|NFP|FOMC", cpi.union(nfp).union(fomc))):
        sig = nxt.isin(ev)
        run("AE09_makro_duyuru_gunu", f"t+1={nm}", s, sig, hs=(1,))
# ---------- AE10 OPEX haftası ----------
opex = ae.events("opex")
for s in U:
    idx = D[s].index
    # OPEX haftasının Pazartesi'sinden önceki son işlem günü
    mondays = pd.DatetimeIndex([d - pd.Timedelta(days=d.dayofweek) for d in opex])
    sig = pd.Series(False, index=idx)
    for mo in mondays:
        prev = idx[idx < mo]
        if len(prev): sig.loc[prev[-1]] = True
    run("AE10_opex_haftasi", "t=OPEX haftasi oncesi son gun, 3 gun tut", s, sig, hs=(3,))
# ---------- AE11 Tatil öncesi ----------
for s in U:
    idx = D[s].index
    ph = S.pre_holiday(idx)
    sig = ph.shift(-1).fillna(False).astype(bool)   # t+1 tatil öncesi son işlem günü (takvim önceden bilinir)
    run("AE11_tatil_oncesi", "t+1=tatil oncesi gun, C0 h1", s, sig, hs=(1,))
# ---------- AE12 VIX sıçraması ----------
spy200 = (SPY["c"] > sma(SPY["c"], 200))
vix_sp = (VIX >= 1.2 * VIX.rolling(10).mean())
for s in U:
    run("AE12_VIX_sicrama", "vix>=1.2*sma10 & SPY>sma200", s, vix_sp.reindex(D[s].index) & spy200.reindex(D[s].index), hs=(3,))
    run("AE12_VIX_sicrama", "vix>=1.2*sma10 (filtresiz)", s, vix_sp.reindex(D[s].index), hs=(3,))
# ---------- AE13 SPY->IWM öncülük ----------
gap = ret("SPY") - ret("IWM")
for tr_sym in ("IWM", "TNA"):
    run("AE13_SPY_IWM_onculuk", "r_SPY-r_IWM>=+1pt -> IWM long", "IWM", gap >= 0.01, trade_sym=tr_sym, hs=(1, 3))
run("AE13_SPY_IWM_onculuk", "r_SPY-r_IWM<=-1pt -> IWM long (ters yon kontrol)", "IWM", gap <= -0.01, hs=(1, 3))
# ---------- AE15 Büyük gün dönüşü ----------
for s in U:
    r = ret(s); sd20 = r.rolling(20).std()
    run("AE15_buyuk_gun_donusu", "r<=-2*sd20 -> long h2", s, r <= -2 * sd20, hs=(2,))
    run("AE15_buyuk_gun_donusu", "r>=+2*sd20 -> long h2 (beklenen<=0)", s, r >= 2 * sd20, hs=(2,))

# ---------- X1: IBS<0.1 & düşüş günü + filtreler (yönlendirme: 200g ort., VIX rejimi) ----------
vr = (VIX / VIX3M)
for s in U:
    cc = c(s); base = (ibs(D[s]) < 0.1) & (cc < cc.shift(1))
    idx = D[s].index
    filt = {
        "filtresiz": pd.Series(True, index=idx),
        "c>sma200": cc > sma(cc, 200),
        "c<sma200": cc <= sma(cc, 200),
        "VIX<20": (VIX < 20).reindex(idx).fillna(False),
        "VIX>=20": (VIX >= 20).reindex(idx).fillna(False),
        "VIX/VIX3M<1": (vr < 1).reindex(idx).fillna(False),
        "VIX/VIX3M>=1": (vr >= 1).reindex(idx).fillna(False),
    }
    for fn, f in filt.items():
        run("X1_ibs01_dusus_filtre", fn, s, base & f, hs=(1, 2, 3))
# ---------- X2: VIX backwardation -> kontango dönüşü ----------
bd = (vr < 1) & (vr.shift(1) >= 1)
for s in U:
    run("X2_backw_kontango_donus", "VIX/VIX3M 1 ustunden alta", s, bd.reindex(D[s].index), hs=(1, 2, 3))
# ---------- X3: faktör çiftleri arası göreli dönüş (long kaybeden) ----------
for a, b in (("SPHB", "SPLV"), ("IWF", "IWD"), ("QQQ", "IWM"), ("IWO", "IWN")):
    ratio = (c(a) / c(b)).dropna()
    z = zret(ratio, 1)
    run("X3_faktor_goreli_donus", f"z1({a}/{b})<-2 -> {a} long", a, z < -2, hs=(1, 3))
    run("X3_faktor_goreli_donus", f"z1({a}/{b})>+2 -> {b} long", b, z > 2, hs=(1, 3))
    z3 = zret(ratio, 3)
    run("X3_faktor_goreli_donus", f"z3({a}/{b})<-2 -> {a} long", a, z3 < -2, hs=(3,))
    run("X3_faktor_goreli_donus", f"z3({a}/{b})>+2 -> {b} long", b, z3 > 2, hs=(3,))
# ---------- X4: aşırı alım sonrası ters ETF (kısa yön) ----------
for base, invs in ae.INV.items():
    cc = c(base); d1 = cc.diff()
    sigs = {"rsi2>90": rsi(cc, 2) > 90,
            "3 gun yukselis": (d1 > 0) & (d1.shift(1) > 0) & (d1.shift(2) > 0),
            "rsi2>90 & c<sma200": (rsi(cc, 2) > 90) & (cc < sma(cc, 200))}
    for nm, sg in sigs.items():
        for inv, L in invs:
            run("X4_asiri_alim_ters_ETF", f"{base} {nm} -> {inv} ({L}x)", base, sg, trade_sym=inv, hs=(1, 3))
# ---------- X5: gece tutma (kapanışta al, açılışta sat) maliyetli ----------
# lib.trades açılışta çıkış desteklemediği için doğrudan hesaplanır
GN = []
for s in ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY", "TQQQ", "UPRO", "TNA"]:
    d = D[s]
    on = d["o"] / d["c"].shift(1) - 1; da = d["c"] / d["o"] - 1; cc = d["c"].pct_change()
    for nm, part in (("tum", slice(None)), ("IS", slice(None, lib.IS_END)), ("OOS", slice(lib.IS_END + pd.Timedelta(days=1), None))):
        o_ = on.loc[part].dropna(); i_ = da.loc[part].dropna(); c_ = cc.loc[part].dropna()
        GN.append({"sym": s, "donem": nm, "n": len(o_), "gece_ort_bp": o_.mean() * 1e4, "gece_t": ae._t(o_.values),
                   "gunici_ort_bp": i_.mean() * 1e4, "gunici_t": ae._t(i_.values), "kapanis_kapanis_bp": c_.mean() * 1e4,
                   "gece_pay": o_.sum() / c_.sum() if c_.sum() != 0 else np.nan,
                   "gece_tut_net_bp_2500": o_.mean() * 1e4 - ae.cost_at(d, 2500), "gece_tut_net_bp_10000": o_.mean() * 1e4 - ae.cost_at(d, 10000)})
gn = pd.DataFrame(GN); gn.to_csv(os.path.join(ae.OUT, "gece_gunici.csv"), index=False)

res = pd.DataFrame(ROWS)
res["fdr10_kendi"] = lib.bh_fdr(res["p"].values, 0.10)
res.to_csv(os.path.join(ae.OUT, "hipotez_testleri.csv"), index=False)

# Özet: hipotez x varyant x mod x h -> sinyal ETF'leri arasında tutarlılık
def summ(d):
    return pd.Series({"n_etf": len(d), "pos_net": int((d.mean_net_bp > 0).sum()), "isoos_pos": int(((d.is_net_bp > 0) & (d.oos_net_bp > 0)).sum()),
                      "t_ge2": int((d.t >= 2).sum()), "fdr": int((d.fdr10_kendi & (d.mean_net_bp > 0)).sum()),
                      "med_n": d.n.median(), "med_gross": d.mean_gross_bp.median(), "med_net": d.mean_net_bp.median(),
                      "med_t": d.t.median(), "med_yp": d.years_pos_frac.median(),
                      "etf": " ".join(f"{a}:{b:.0f}/{t:.1f}" for a, b, t in zip(d.trade_sym, d.mean_net_bp, d.t))})
sm = res.groupby(["hyp", "var", "mode", "h"]).apply(summ).reset_index()
sm.to_csv(os.path.join(ae.OUT, "hipotez_ozet.csv"), index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_rows", 500); pd.set_option("display.max_colwidth", 120)
print("Toplam test:", len(res), " FDR(q=0.10) geçen:", int(res.fdr10_kendi.sum()), " pozitif geçen:", int((res.fdr10_kendi & (res.mean_net_bp > 0)).sum()))
print(sm.round(2).to_string(index=False))
print(gn.round(2).to_string(index=False))
