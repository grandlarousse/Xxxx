"""ADAY S1 — 10 yıllık Hazine ihalesi öncesi uzun vade zayıflığı (Lou, Yan & Zhang 2013 "ihale öncesi fiyat baskısı").
Kural: A = 10 yıllık Hazine ihale günü (TreasuryDirect/Hazine geçici takvimi; önceden ilan edilir).
       A'dan 3 işlem günü önceki gün (A-3) KAPANIŞINDA ters uzun vade ETF'i (TMV -3x / TBT -2x) al,
       A'dan 1 işlem günü önceki gün (A-1) KAPANIŞINDA sat (2 işlem günü tutuş; ihale günü tutulmaz).
Çalıştır: python3 -I kod/ajan_tahvil_doviz/strateji_S1_ihale_oncesi.py
Basılanlar: ana sonuç (TMV, TBT), maliyet duyarlılığı, C0/O1/C1, aile içi (uzun ETF'lerde brüt getiri negatif olmalı),
komşu pencereler, CPI/NFP içeren pencereler hariç, haftanın günü kontrolü, yıllara göre, son ve sıradaki sinyaller.
Çıktılar: sonuclar/aile_tahvil_doviz/S1_*.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200); pd.set_option("display.max_columns", 40)
IDX = lib.load("SPY").index
ev = pd.read_csv(os.path.join(td.ROOT, "data", "events", "hazine_ihale_10y30y.csv"), parse_dates=["date"])
a10 = pd.DatetimeIndex(sorted(ev[ev.event == "UST10Y_ihale"].date.unique()))
a30 = pd.DatetimeIndex(sorted(ev[ev.event == "UST30Y_ihale"].date.unique()))
cpi = td.events("cpi", ["CPI"]); nfp = td.events("nfp", ["NFP"])

def sig(dates, k):
    return td.ev_on_idx(dates, IDX, -k)

COLS = ["sym", "mode", "h", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "net_bp_1000", "net_bp_10000", "win", "pf", "t", "is_n", "is_net_bp",
        "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp", "edge_bp", "cost_bp"]
S = sig(a10, 3)
print("=== S1 ana kural: 10Y ihale A-3 kapanış -> A-1 kapanış (h=2) ===")
main = []; trs = {}
for sym in ["TMV", "TBT"]:
    for m in ("C0", "O1", "C1"):
        s, tr = td.full_eval(td.load(sym), S, 2, m, sym=sym, warm=0)
        main.append(td.row(s, {"var": "A10-3_h2"})); trs[(sym, m)] = tr
main = pd.DataFrame(main)
print(main[["var"] + COLS].round(2).to_string(index=False))
main.to_csv(os.path.join(td.OUT, "S1_ana.csv"), index=False)

print("\n=== Aynı pencere, uzun ETF'ler (brüt getiri NEGATİF beklenir; kısa yön yalnız ters ETF ile) ===")
fam = []
for sym in ["TLT", "EDV", "ZROZ", "TLH", "IEF", "IEI", "GOVT", "AGG", "LQD", "TIP", "MUB", "SHY", "HYG", "EMB", "TMF", "UBT", "TBT", "TMV"]:
    s, tr = td.full_eval(td.load(sym), S, 2, "C0", sym=sym, warm=0)
    fam.append(td.row(s))
fam = pd.DataFrame(fam)
print(fam[["sym", "n", "mean_gross_bp", "t_gross", "edge_bp", "t_edge", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
fam.to_csv(os.path.join(td.OUT, "S1_aile.csv"), index=False)

print("\n=== Komşu pencereler (TLT brüt; TMV net) — parametre seçimi değil, sağlamlık ===")
nb = []
for lab, dates, k, h in [("A10-4->A-1 (h3)", a10, 4, 3), ("A10-3->A-1 (h2) ANA", a10, 3, 2), ("A10-2->A-1 (h1)", a10, 2, 1),
                         ("A10-3->A-2 (h1)", a10, 3, 1), ("A10-3->A (h3, ihale günü dahil)", a10, 3, 3), ("A10-1->A (h1, ihale günü)", a10, 1, 1),
                         ("A10->A+2 (ihale sonrası)", a10, 0, 2), ("A30-3->A30-1 (h2)", a30, 3, 2), ("A30-1->A30 (h1)", a30, 1, 1),
                         ("A30->A30+2", a30, 0, 2)]:
    sg = sig(dates, k)
    for sym in ("TLT", "TMV"):
        s, _ = td.full_eval(td.load(sym), sg, h, "C0", sym=sym, warm=0)
        nb.append(td.row(s, {"pencere": lab}))
nb = pd.DataFrame(nb)
print(nb[["pencere", "sym", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
nb.to_csv(os.path.join(td.OUT, "S1_komsu.csv"), index=False)

print("\n=== Kontroller (TLT brüt, C0) ===")
tlt = td.load("TLT"); _, tt = td.full_eval(tlt, S, 2, "C0", sym="TLT", warm=0)
tm = trs[("TMV", "C0")].copy()
def window_has(tr, dates):
    d = set(pd.DatetimeIndex(dates))
    out = []
    for e, x in zip(tr.entry_date, tr.exit_date):
        days = tlt.index[(tlt.index > e) & (tlt.index <= x)]
        out.append(any(dd in d for dd in days))
    return np.array(out)
cpi_on = td.ev_on_idx(cpi, IDX); nfp_on = td.ev_on_idx(nfp, IDX)
cpi_d = IDX[cpi_on.values]; nfp_d = IDX[nfp_on.values]
fomc_d = IDX[td.ev_on_idx(td.events("fomc", ["FOMC_karar"]), IDX).values]
for lab, mask in (("pencerede CPI var", window_has(tt, cpi_d)), ("pencerede NFP var", window_has(tt, nfp_d)),
                  ("pencerede FOMC var", window_has(tt, fomc_d))):
    a = tt[mask]; b = tt[~mask]; at = tm[mask]; bt = tm[~mask]
    print(f"{lab:22s}: var n={len(a):3d} TLT brüt {a.gross.mean()*1e4:7.1f} bp (t {td._t(a.gross.values):5.2f}) TMV net {at.net.mean()*1e4:7.1f} | "
          f"yok n={len(b):3d} TLT brüt {b.gross.mean()*1e4:7.1f} bp (t {td._t(b.gross.values):5.2f}) TMV net {bt.net.mean()*1e4:7.1f} (t {td._t(bt.net.values):5.2f})")
# haftanın günü kontrolü: aynı gün bileşimli tüm 2 günlük pencereler (ihale haftası dışı) ile karşılaştır
r2 = tlt["c"].shift(-2) / tlt["c"] - 1
dow = pd.Series(tlt.index.dayofweek, index=tlt.index)
sigd = tt.sig_date
base = []
for d0 in sigd:
    w = dow[d0]
    same = r2[(dow == w) & ~tlt.index.isin(sigd)]
    base.append(same.mean())
print(f"Haftanın günü eşlenik koşulsuz 2g TLT ortalaması: {np.nanmean(base)*1e4:.1f} bp; sinyal: {tt.gross.mean()*1e4:.1f} bp -> fark {(tt.gross.mean()-np.nanmean(base))*1e4:.1f} bp")
print("Giriş günü dağılımı (A-3):", tt.sig_date.dt.day_name().value_counts().to_dict())
# 2020 ve 2022 hariç
for ex in (2020, 2022):
    m = tm.sig_date.dt.year != ex
    print(f"{ex} hariç TMV net: {tm[m].net.mean()*1e4:.1f} bp, t={td._t(tm[m].net.values):.2f}, n={m.sum()}")

print("\n=== Yıllara göre (TMV C0 net, TLT brüt) ===")
yy = pd.DataFrame({"TMV_net_bp": tm.groupby(tm.sig_date.dt.year).net.mean() * 1e4, "TMV_n": tm.groupby(tm.sig_date.dt.year).size(),
                   "TLT_brut_bp": tt.groupby(tt.sig_date.dt.year).gross.mean() * 1e4,
                   "TBT_net_bp": trs[("TBT", "C0")].groupby(trs[("TBT", "C0")].sig_date.dt.year).net.mean() * 1e4})
print(yy.round(1).to_string())
yy.to_csv(os.path.join(td.OUT, "S1_yillar.csv"))

print("\n=== En kötü 5 TMV işlemi ===")
print(tm.sort_values("net").head(5).assign(net_bp=lambda d: d.net * 1e4)[["sig_date", "entry_date", "exit_date", "net_bp"]].to_string(index=False))
tm.to_csv(os.path.join(td.OUT, "S1_islemler_TMV_C0.csv"), index=False)

print("\n=== Son 4 sinyal ve sıradaki ihaleler (takvim) ===")
print(tm.tail(4)[["sig_date", "entry_date", "exit_date"]].assign(net_bp=tm.tail(4).net * 1e4).round(1).to_string(index=False))
fut = ev[(ev.date >= pd.Timestamp("2026-11-01"))][["date", "event", "detail"]]
print(fut.to_string(index=False))

print("\n=== Plasebo: aynı pencere ±5 / ±10 işlem günü kaydırılmış (TLT brüt, TMV net) ===")
pl = []
for sh in (-10, -5, 0, 5, 10):
    sg = sig(a10, 3 - sh) if sh <= 3 else td.ev_on_idx(a10, IDX, sh - 3)
    for sym in ("TLT", "TMV"):
        s, _ = td.full_eval(td.load(sym), sg, 2, "C0", sym=sym, warm=0)
        pl.append(td.row(s, {"kaydirma_gun": sh}))
pl = pd.DataFrame(pl)
print(pl[["kaydirma_gun", "sym", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "t", "years_pos_frac"]].round(2).to_string(index=False))
pl.to_csv(os.path.join(td.OUT, "S1_plasebo.csv"), index=False)

print("\n=== Uygulama esnekliği: A-3 günü AÇILIŞTA giriş (sinyal A-4, O1, h=3 -> çıkış A-1 kapanış) ===")
ex = []
for sym in ("TMV", "TBT", "TLT"):
    s, _ = td.full_eval(td.load(sym), sig(a10, 4), 3, "O1", sym=sym, warm=0)
    ex.append(td.row(s, {"giris": "A-3 açılış"}))
ex = pd.DataFrame(ex)
print(ex[["giris", "sym", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
ex.to_csv(os.path.join(td.OUT, "S1_A3_acilis.csv"), index=False)

print("\n=== Aykırı değer duyarlılığı (TMV C0 net) ===")
x = tm.copy()
m16 = x.sig_date.dt.year > 2016
print(f"2016 (tek işlem) hariç: n={m16.sum()}, net {x[m16].net.mean()*1e4:.1f} bp, t={td._t(x[m16].net.values):.2f}")
xs = x.sort_values("net")
for k in (3, 5):
    y = xs.iloc[:-k]
    print(f"en iyi {k} işlem hariç: n={len(y)}, net {y.net.mean()*1e4:.1f} bp, t={td._t(y.net.values):.2f}")
print(f"medyan net: {x.net.median()*1e4:.1f} bp; kazanma oranı {(x.net>0).mean():.3f}")
