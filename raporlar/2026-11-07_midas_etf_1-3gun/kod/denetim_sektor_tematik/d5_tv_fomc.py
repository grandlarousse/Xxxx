"""Denetim: (1) ajanın çıktısındaki TradingView kodlarının doğrulama dosyalarında durumu,
(2) FOMC karar günü faize duyarlı sektörler iddiası, (3) S1'in oynaklık rejimine göre dağılımı (bugünkü rejim).
python3 -I kod/denetim_sektor_tematik/d5_tv_fomc.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *

pd.set_option("display.width", 250)
J = json.load(open(os.path.join(ROOT, "sonuclar/aile_sektor_tematik/sonuc.json")))
te = pd.read_csv(os.path.join(ROOT, "sonuclar/tv_etf.csv")); tv = pd.read_csv(os.path.join(ROOT, "sonuclar/tv_dogrulama.csv"))
ok_etf = dict(zip(te["tv"], te["durum"])); ok_ld = dict(zip(tv["ticker"], tv["durum"]))
GOOD = {"dogrulandi", "dogrulandi_kanonik"}
codes = []
for w in J["izleme"]:
    codes.append(("izleme", w["sym"], w["tv"]))
for L in J["leadlag"]:
    for k in ("suruculer", "onculer", "gercek_zamanli"):
        for x in L.get(k, []):
            codes.append((k, L["sym"], x.get("tv")))
rows = []
for kind, sym, code in codes:
    st_ = ok_etf.get(code) or ok_ld.get(code) or "LISTEDE_YOK"
    rows.append({"tur": kind, "etf": sym, "tv": code, "durum": st_})
C = pd.DataFrame(rows).drop_duplicates(["tv"])
bad = C[~C["durum"].isin(GOOD)]
print("Toplam benzersiz kod:", len(C), " doğrulanmış:", int(C["durum"].isin(GOOD).sum()))
print("DOĞRULANMAMIŞ / LİSTEDE OLMAYAN KODLAR:"); print(bad.to_string())
C.to_csv(os.path.join(OUT, "d5_tv_kodlari.csv"), index=False)

# (2) FOMC: karar günü O1 (açılış->kapanış) ve C0 (önceki kapanış->karar kapanışı) getirisi, 6 faize duyarlı ETF
fomc = pd.read_csv(os.path.join(lib.DATA, "events", "fomc.csv"))
print("\nfomc.csv sütunları:", fomc.columns.tolist(), fomc.head(3).to_dict("records"))
dcol = [c for c in fomc.columns if "date" in c.lower() or "tarih" in c.lower()][0]
fd = pd.to_datetime(fomc[dcol]).dt.normalize()
grp = ["KRE", "XLF", "ITB", "VNQ", "XLU", "KIE"]
rows = []
for s in grp + ["SPY"]:
    df = D(s); intr = df["c"] / df["o"] - 1
    m = df.index.isin(fd)
    rows.append({"etf": s, "n_fomc": int(m.sum()), "gun_ici_fomc_bp": intr[m].mean() * 1e4, "gun_ici_diger_bp": intr[~m].mean() * 1e4,
                 "t_fark": (intr[m].mean() - intr[~m].mean()) / (intr[m].std(ddof=1) / np.sqrt(m.sum())),
                 "is_bp": intr[m & (df.index <= IS_END)].mean() * 1e4, "oos_bp": intr[m & (df.index > IS_END)].mean() * 1e4})
F = pd.DataFrame(rows); print("\nFOMC karar günü gün içi (O1 açılış->kapanış) brüt:"); print(F.round(2).to_string())
# havuz: 6 ETF eşit ağırlık sepet
bask = pd.concat([D(s)["c"] / D(s)["o"] - 1 for s in grp], axis=1).mean(axis=1)
spy = D("SPY"); spy_i = (spy["c"] / spy["o"] - 1).reindex(bask.index)
m = bask.index.isin(fd)
print(f"Sepet: FOMC n={m.sum()} ort {bask[m].mean()*1e4:.1f} bp (t {tt(bask[m].values):.2f}); diğer günler {bask[~m].mean()*1e4:.1f}; "
      f"SPY aynı günler {spy_i[m].mean()*1e4:.1f} bp; sepet-SPY {((bask-spy_i)[m]).mean()*1e4:.1f} bp (t {tt((bask-spy_i)[m].values):.2f})")
# rastgele gün permütasyonu (sepet)
rng = np.random.default_rng(7); vals = bask.dropna().values; k = int(m.sum()); obs = bask[m].mean()
perm = np.array([rng.choice(vals, k, replace=False).mean() for _ in range(10000)])
print(f"Sepet FOMC permütasyon p (tek yönlü, <=): {(np.sum(perm <= obs)+1)/10001:.4f}")

# (3) S1 oynaklık rejimi
smh = D("SMH"); sig = my_ibs(smh) < 0.2
tr = sim(smh, sig, 1, "C0", cost("SMH"))
vol20 = np.log(smh["c"]).diff().rolling(20).std() * np.sqrt(252)
q = pd.qcut(vol20, 5, labels=["Q1 düşük", "Q2", "Q3", "Q4", "Q5 yüksek"])
tr["vq"] = q.reindex(tr.sig_date).values
g = tr.groupby("vq", observed=True).agg(n=("net", "size"), net_bp=("net", lambda x: x.mean() * 1e4), t=("net", lambda x: tt(x)),
                                       en_kotu=("net", lambda x: x.min() * 1e4))
print("\nS1 sonuç / 20g yıllık oynaklık beşliği:"); print(g.round(2).to_string())
print("Beşlik sınırları (yıllık):", [round(float(x), 3) for x in vol20.quantile([.2, .4, .6, .8]).values], " bugünkü (2026-11-06):", round(float(vol20.iloc[-1]), 3))
json.dump({"tv_dogrulanmamis": bad.to_dict("records"), "fomc": F.round(3).to_dict("records"),
           "s1_vol": g.round(3).reset_index().astype(str).to_dict("records")}, open(os.path.join(OUT, "d5_sonuc.json"), "w"), ensure_ascii=False, indent=1)
