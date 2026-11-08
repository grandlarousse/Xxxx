"""5) Aday stratejilerin tekrar üretilebilir değerlendirmesi. Çalıştır:
   python3 -I kod/ajan_abd_endeks/05_adaylar.py
Basar: her aday için n, brüt/net bp (2.500 USD), 1.000/10.000 USD net, kazanma, PF, t, IS/OOS net ve t, yıl pozitif oranı,
maxDD, en kötü işlem; C0/O1/C1 mod sağlamlığı; aile içi diğer ETF'ler; sepet (aynı gün açılan işlemler ortalanmış) t;
komşu parametreler (IS ve OOS ayrı); kaldıraçlı araçla uygulama; yıllık döküm; VIX rejimi.
Çıktı: sonuclar/aile_abd_endeks/aday_*.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ae, lib
from lib import ibs, rsi, sma
import strategies as S

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)
OUT = ae.OUT
D = {s: lib.load(s) for s in ae.FAM}
VIX = ae.ctx()["VIX"]
COLS = ["sym", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_bp_1000", "net_bp_10000", "win", "pf", "t", "is_net_bp", "is_t",
        "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp"]

def sig_S1(d, thr=0.10, down=True):
    s = ibs(d) < thr
    if down: s = s & (d["c"] < d["c"].shift(1))
    return s

def sig_S2(d):
    c = d["c"]; d1 = c.diff()
    return (d1 < 0) & (d1.shift(1) < 0) & (d1.shift(2) < 0)

def exit_S2(d):
    return d["c"] > d["c"].shift(1)

def table(sigfn, syms, h, modes=("C0", "O1", "C1"), exitfn=None, sig_src=None, label=""):
    rows, trs = [], {}
    for s in syms:
        src = D[sig_src.get(s, s)] if sig_src else D[s]
        sg = sigfn(src)
        ex = exitfn(src) if exitfn else None
        for m in modes:
            st_, tr = ae.full_eval(D[s], sg, h, m, exit_sig=ex, label=label, sym=s)
            r = ae.row(st_); r["sig_src"] = sig_src.get(s, s) if sig_src else s
            rows.append(r); trs[(s, m)] = tr
    return pd.DataFrame(rows), trs

def yearly(tr):
    if not len(tr): return pd.Series(dtype=float)
    return (tr.groupby(tr["sig_date"].dt.year)["net"].apply(lambda x: (np.prod(1 + x) - 1) * 1e4)).round(0)

ALL = []
# ======================= S1: IBS<0.10 + düşüş günü, 3 gün =======================
print("=" * 30, "S1: IBS<0.10 ve kapanış<önceki kapanış -> 3 işlem günü tut", "=" * 30)
t1, tr1 = table(sig_S1, ae.CORE, 3, label="S1")
print("Çekirdek endeks ETF'leri (h=3):"); print(t1[COLS].round(2).to_string(index=False))
t1b, _ = table(sig_S1, ae.CORE, 2, label="S1_h2"); t1c, _ = table(sig_S1, ae.CORE, 1, label="S1_h1")
print("h=2 ve h=1 (komşu tutuş):")
print(pd.concat([t1b, t1c])[["sym", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
tf, _ = table(sig_S1, ae.FACTOR, 3, label="S1_faktor")
print("Faktör/temettü ETF'leri (h=3):"); print(tf[COLS].round(2).to_string(index=False))
ALL += [t1.assign(aday="S1"), t1b.assign(aday="S1_h2"), t1c.assign(aday="S1_h1"), tf.assign(aday="S1_faktor")]

# sepet: 6 çekirdek ETF, aynı giriş gününde açılan işlemler ortalanır
for m in ("C0", "O1", "C1"):
    bt, bn, bm = ae.basket_t([tr1[(s, m)] for s in ae.CORE])
    bt2, bn2, bm2 = ae.basket_t([tr1[(s, m)] for s in ["SPY", "QQQ", "IWM"]])
    print(f"Sepet t (6 çekirdek) {m} h3: t={bt:.2f} n_gün={bn} ort_net={bm:.1f}bp | (SPY,QQQ,IWM) t={bt2:.2f} n={bn2} ort={bm2:.1f}bp")

# yıllık döküm
for s in ("SPY", "QQQ"):
    for m in ("C0", "C1"):
        print(f"Yıllık bileşik net bp {s} {m}:", yearly(tr1[(s, m)]).to_dict())

# komşu parametreler (seçim için DEĞİL; IS/OOS kararlılığı)
NB = []
for s in ("SPY", "QQQ", "IWM", "DIA", "RSP", "MDY"):
    for thr in (0.05, 0.10, 0.15, 0.20, 0.30):
        for down in (True, False):
            for m in ("C0", "C1"):
                st_, _ = ae.full_eval(D[s], sig_S1(D[s], thr, down), 3, m, sym=s)
                NB.append({"sym": s, "ibs_esik": thr, "dusus_sarti": down, "mode": m, "n": st_["n"], "net_bp": st_["mean_net_bp"], "t": st_["t"],
                           "is_net_bp": st_["is_net_bp"], "is_t": st_["is_t"], "oos_net_bp": st_["oos_net_bp"], "oos_t": st_["oos_t"]})
nb = pd.DataFrame(NB); nb.to_csv(os.path.join(OUT, "aday_S1_komsu_parametre.csv"), index=False)
print("Komşu parametreler (C1, h=3) - IS ve OOS net bp:")
pv = nb[nb["mode"] == "C1"].pivot_table(index=["ibs_esik", "dusus_sarti"], columns="sym", values=["is_net_bp", "oos_net_bp"]).round(0)
print(pv.to_string())

# Genişlik: etki piyasa geneli zayıf kapanışlarda mı? (19 temsilci; aynı giriş günü kaç ETF sinyal verdi)
BR = []
for s in ae.REPS:
    st_, tr = ae.full_eval(D[s], sig_S1(D[s]), 3, "C1", sym=s); tr["sym"] = s; BR.append(tr)
br = pd.concat(BR).groupby("entry_date").agg(k=("sym", "count"), net=("net", "mean"))
br["genislik"] = pd.cut(br.k, [0, 1, 3, 6, 10, 19])
print("Genişlik (C1 h3, 19 temsilci; aynı gün sinyal veren ETF sayısına göre gün-ortalaması net bp):")
print(br.groupby("genislik", observed=True)["net"].agg(gun="count", net_bp=lambda x: x.mean() * 1e4, t=lambda x: ae._t(x.values)).round(2).to_string())
# SPY sinyali (piyasa geneli) ile diğer endeks ETF'lerinde işlem; ve ETF'nin kendi sinyalini SPY'ın da sinyal verip vermediğine göre ayır
ss = sig_S1(D["SPY"]); SP = []
for s in ["QQQ", "IWM", "DIA", "RSP", "MDY"]:
    for m in ("C0", "C1"):
        st_, tr = ae.full_eval(D[s], sig_S1(D[s]), 3, m, sym=s)
        f = ss.reindex(tr["sig_date"]).fillna(False).values.astype(bool)
        st2, _ = ae.full_eval(D[s], ss, 3, m, sym=s)
        SP.append({"sym": s, "mode": m, "kendi_sinyal_SPY_de_var_n": int(f.sum()), "net_bp_SPY_de_var": tr["net"][f].mean() * 1e4,
                   "t_SPY_de_var": ae._t(tr["net"][f].values), "kendi_sinyal_SPY_yok_n": int((~f).sum()), "net_bp_SPY_yok": tr["net"][~f].mean() * 1e4,
                   "t_SPY_yok": ae._t(tr["net"][~f].values), "SPY_sinyaliyle_n": st2["n"], "SPY_sinyaliyle_net_bp": st2["mean_net_bp"],
                   "SPY_sinyaliyle_t": st2["t"], "SPY_sinyaliyle_is": st2["is_net_bp"], "SPY_sinyaliyle_oos": st2["oos_net_bp"]})
sp = pd.DataFrame(SP); sp.to_csv(os.path.join(OUT, "aday_S1_spy_sinyali.csv"), index=False)
print("SPY sinyali ile diğer ETF'ler / kendi sinyalinin SPY'a göre ayrışması:"); print(sp.round(2).to_string(index=False))

# VIX rejimi (bilgi amaçlı; filtre seçimi yapılmadı)
VR = []
for s in ("SPY", "QQQ", "IWM"):
    for m in ("C0", "C1"):
        tr = tr1[(s, m)].copy()
        v = VIX.reindex(tr["sig_date"]).values
        for nm, msk in (("VIX<20", v < 20), ("VIX>=20", v >= 20)):
            x = tr[msk]["net"]
            VR.append({"sym": s, "mode": m, "rejim": nm, "n": len(x), "net_bp": x.mean() * 1e4, "t": ae._t(x.values), "win": (x > 0).mean()})
print("VIX rejimine göre S1 (h=3):"); print(pd.DataFrame(VR).round(2).to_string(index=False))

# kaldıraçlı araçla uygulama (sinyal dayanaktan)
LV = []
for base, lst in ae.LEV.items():
    for inst, Lx in lst:
        for m in ("C0", "O1", "C1"):
            st_, tr = ae.full_eval(D[inst], sig_S1(D[base]), 3, m, sym=inst)
            # en kötü 1 günlük kayıp pozisyondayken
            c = D[inst]["c"]; r = c.pct_change()
            worst_day = np.nan
            if len(tr):
                days = []
                for _, rr in tr.iterrows():
                    seg = r.loc[(r.index > rr["entry_date"]) & (r.index <= rr["exit_date"])]
                    if len(seg): days.append(seg.min())
                worst_day = min(days) * 1e4 if days else np.nan
            rw = ae.row(st_); rw.update({"dayanak": base, "kaldirac": Lx, "en_kotu_gun_bp": worst_day})
            LV.append(rw)
lv = pd.DataFrame(LV)
base_g = t1.set_index(["sym", "mode"])["mean_gross_bp"]
lv["brut_kaldirac_basina"] = lv["mean_gross_bp"] / lv["kaldirac"]
lv["dayanak_brut"] = [base_g.get((b, m), np.nan) for b, m in zip(lv["dayanak"], lv["mode"])]
lv.to_csv(os.path.join(OUT, "aday_S1_kaldiracli.csv"), index=False)
print("Kaldıraçlı uygulama (sinyal dayanakta, işlem araçta, h=3):")
print(lv[["dayanak", "sym", "kaldirac", "mode", "n", "mean_gross_bp", "dayanak_brut", "brut_kaldirac_basina", "mean_net_bp", "t",
          "is_net_bp", "oos_net_bp", "years_pos_frac", "maxdd", "worst_bp", "en_kotu_gun_bp"]].round(2).to_string(index=False))

# ======================= S2: 3 ardışık düşüş, ilk yükselen kapanışta çık (en çok 3 gün) =======================
print("=" * 30, "S2: 3 ardışık düşen kapanış -> al; ilk yükselen kapanışta (en geç 3. gün) çık", "=" * 30)
t2, tr2 = table(sig_S2, ae.CORE, 3, exitfn=exit_S2, label="S2")
print(t2[COLS].round(2).to_string(index=False))
t2f, _ = table(sig_S2, ae.FACTOR, 3, exitfn=exit_S2, label="S2_faktor")
print("Faktör ETF'leri:"); print(t2f[["sym", "mode", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
ALL += [t2.assign(aday="S2"), t2f.assign(aday="S2_faktor")]
for m in ("C0", "O1", "C1"):
    bt, bn, bm = ae.basket_t([tr2[(s, m)] for s in ae.CORE])
    print(f"Sepet t (6 çekirdek) {m}: t={bt:.2f} n_gün={bn} ort_net={bm:.1f}bp")
# S1 ile örtüşme
for s in ("SPY", "QQQ"):
    a = sig_S1(D[s]); b = sig_S2(D[s])
    print(f"{s}: S2 sinyal günlerinin S1 ile aynı gün olma oranı {(a & b).sum() / b.sum():.2f}; S1 günlerinin S2 olma oranı {(a & b).sum() / a.sum():.2f}")

# ======================= Elenen: CA_tatil_oncesi C1 h3 (tatil sonrası 2.-4. gün) tatile göre döküm =======================
print("=" * 30, "Kontrol: CA_tatil_oncesi C1 h=3 (= tatil sonrası 1. gün kapanışında gir, 3 gün tut)", "=" * 30)
hol = pd.read_csv(os.path.join(ae.ROOT, "data", "events", "nyse_tatil.csv"), parse_dates=["date"])
hol = hol[hol.event == "NYSE_tatil"]
for s in ("SPY", "QQQ", "IWM"):
    d = D[s]; ph = S.pre_holiday(d.index)
    st_, tr = ae.full_eval(d, ph, 3, "C1", sym=s)
    names = []
    for sd in tr["sig_date"]:
        nx = hol[hol.date > sd].head(1)
        names.append(nx["detail"].iloc[0].split(";")[0] if len(nx) else "?")
    tr["tatil"] = names
    g = tr.groupby("tatil")["net"].agg(["count", "mean"]); g["mean"] *= 1e4
    print(s, f"n={st_['n']} net={st_['mean_net_bp']:.1f} t={st_['t']:.2f}"); print(g.round(1).sort_values("mean").to_string())

res = pd.concat(ALL); res.to_csv(os.path.join(OUT, "aday_ozet.csv"), index=False)
print("yazıldı:", os.path.join(OUT, "aday_ozet.csv"))
