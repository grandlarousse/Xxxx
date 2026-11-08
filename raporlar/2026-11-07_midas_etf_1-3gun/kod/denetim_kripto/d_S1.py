"""Denetim kripto_S1: Perşembe gün içi ters BTC (SBIT, alternatif BITI).
Çalıştır: python3 -I kod/denetim_kripto/d_S1.py   (lib.trades/evaluate kullanılmaz)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
ROOT = dk.ROOT; OUT = dk.OUT
R = []   # özet satırları
def rep(tr, label, extra=None):
    s = dk.summ(tr, label)
    if extra: s.update(extra)
    R.append(s)
    print(f"{label:55s} n={s['n']:4d} brüt {s.get('brut_bp', np.nan):7.1f} net {s.get('net_bp', np.nan):7.1f} t={s.get('t', np.nan):5.2f} "
          f"t_brüt={s.get('t_brut', np.nan):5.2f} kaz {s.get('kazanma', np.nan):.2f} PF {s.get('pf', np.nan):.2f} maxDD {s.get('maxdd', np.nan):.3f} "
          f"en kötü {s.get('en_kotu_bp', np.nan):.0f} yıl+ {s.get('yil_pozitif', np.nan):.2f} best5- {s.get('en_iyi5_haric_net_bp', np.nan):.1f} (t {s.get('en_iyi5_haric_t', np.nan):.2f})")
    return s

def intraday_trades(df, mask, cost):
    """Gerçek gün seçimi: maske True olan günde açılışta al, aynı gün kapanışta sat."""
    d = df[mask.reindex(df.index).fillna(False).values]
    g = d["c"] / d["o"] - 1
    return pd.DataFrame({"sig_date": d.index, "entry_date": d.index, "exit_date": d.index, "gross": g.values, "net": g.values - cost / 1e4})

def thu(df): return pd.Series(df.index.dayofweek == 3, index=df.index)

SP = {s: dk.tarama_spread(s) for s in ["SBIT", "BITI", "IBIT", "ETHA", "BITO", "BITX", "BLOK", "GBTC", "SPY", "QQQ"]}
print("tarama makasları:", SP)
SB = lib.load("SBIT"); BI = lib.load("BITI"); IB = lib.load("IBIT")
cost = lambda sym, pos=2500: dk.comm_bp(pos) + SP[sym]

print("\n=== 1) Yeniden üretim ===")
# (a) ajanın tanımı: Çarşamba sinyali -> O1 h=1 (sonraki işlem gününün açılış->kapanışı)
wed = pd.Series(SB.index.dayofweek == 2, index=SB.index)
trA = dk.sim(SB, wed, 1, "O1", cost("SBIT"))
sA = rep(trA, "SBIT ajan tanımı (Çar sinyali, O1 h1)")
ag = pd.read_csv(os.path.join(ROOT, "sonuclar", "aile_kripto", "aday_kripto_S1_islemler.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
mm = trA.merge(ag, on="entry_date", how="outer", suffixes=("_ben", "_ajan"), indicator=True)
print("ajan işlem listesiyle eşleşme:", mm._merge.value_counts().to_dict(), " maks brüt farkı:", float((mm.gross_ben - mm.gross_ajan).abs().max()))
nonthu = trA[trA.entry_date.dt.dayofweek != 3]
print("Ajan listesinde Perşembe OLMAYAN giriş günleri (tatil kayması):", [str(d.date()) + " " + d.day_name() for d in nonthu.entry_date])
# (b) gerçek Perşembe
trT = intraday_trades(SB, thu(SB), cost("SBIT"))
sT = rep(trT, "SBIT gerçek Perşembe (açılış->kapanış)")
trT.to_csv(os.path.join(OUT, "S1_SBIT_persembe_islemler.csv"), index=False)

print("\n=== 2) Maliyet duyarlılığı (gerçek Perşembe) ===")
for pos in (1000, 2500, 10000):
    t_ = intraday_trades(SB, thu(SB), cost("SBIT", pos)); rep(t_, f"SBIT Per maliyet {pos}$ ({cost('SBIT', pos):.0f} bp)")

print("\n=== 3) Mod sağlamlığı (SBIT) ===")
thu_sig = thu(SB); wed_sig = wed
for lab, sg, h, mode in (("C0: Çar kapanış -> Per kapanış", wed_sig, 1, "C0"), ("O1: Per açılış -> Per kapanış", wed_sig, 1, "O1"),
                         ("C1: Per kapanış -> Cum kapanış", wed_sig, 1, "C1"), ("Gece: Çar kapanış -> Per açılış", None, 0, "ON")):
    if mode == "ON":
        d = SB.copy(); g = (d["o"].shift(-1) / d["c"] - 1)[wed_sig].dropna()
        t_ = pd.DataFrame({"sig_date": g.index, "entry_date": g.index, "exit_date": g.index, "gross": g.values, "net": g.values - cost("SBIT") / 1e4})
    else:
        t_ = dk.sim(SB, sg, h, mode, cost("SBIT"))
    rep(t_, "SBIT " + lab)

print("\n=== 4) Yıl yıl ve alt dönemler (SBIT gerçek Perşembe) ===")
print(dk.yearly(trT).T.to_string())
trT["yarıyıl"] = trT.sig_date.dt.year.astype(str) + "H" + ((trT.sig_date.dt.month > 6) + 1).astype(str)
print((trT.groupby("yarıyıl").net.agg(["mean", "count"]) * [1e4, 1]).round(0).T.to_string())
print("Son 12 ay (2025-11-07+):"); rep(trT[trT.sig_date >= "2025-11-07"], "SBIT Per son 12 ay")
print("2026:"); rep(trT[trT.sig_date >= "2026-01-01"], "SBIT Per 2026")

print("\n=== 5) En büyük 5 kazanç (tarih tarih) ===")
vk = pd.read_csv(os.path.join(ROOT, "sonuclar", "veri_kalitesi.csv")); vd = pd.read_csv(os.path.join(ROOT, "sonuclar", "veri_duzeltmeleri.csv"))
cpi = set(pd.to_datetime(pd.read_csv(os.path.join(ROOT, "data", "events", "cpi.csv")).date))
top = trT.sort_values("gross", ascending=False).head(5)
for _, r in top.iterrows():
    d = r.entry_date; ds = str(d.date())
    ib = IB.loc[d]; ibid = ib.c / ib.o - 1; ibgap = ib.o / IB.c.shift(1).loc[d] - 1
    flag = [x for x in vk[(vk.date == ds) & vk.sym.isin(["SBIT", "IBIT"])].sym] + [x for x in vd[(vd.date == ds) & vd.sym.isin(["SBIT", "IBIT"])].sym]
    print(f"  {ds}: SBIT gün içi {r.gross*1e4:7.0f} bp | IBIT gün içi {ibid*1e4:6.0f} bp, IBIT açılış boşluğu {ibgap*1e4:6.0f} bp | CPI günü: {d in cpi} | veri_kalitesi/düzeltme: {flag}")

print("\n=== 6) SBIT açılış fiyatı tutarlılığı (IBIT'ten türetilen −2x gün içi ile) ===")
x = pd.DataFrame({"sb_o": SB.o, "sb_c": SB.c, "ib_o": IB.o, "ib_c": IB.c, "ib_pc": IB.c.shift(1)}).dropna()
Ro = x.ib_o / x.ib_pc - 1; Rc = x.ib_c / x.ib_pc - 1
x["impl"] = (1 - 2 * Rc) / (1 - 2 * Ro) - 1
x["act"] = x.sb_c / x.sb_o - 1
xt = x[x.index.dayofweek == 3]
print(f"  Perşembe: n={len(xt)}, korelasyon {xt.act.corr(xt.impl):.4f}, ort gerçek {xt.act.mean()*1e4:.1f} bp, ort türetilmiş {xt.impl.mean()*1e4:.1f} bp, "
      f"fark ort {(xt.act-xt.impl).mean()*1e4:.1f} bp (t={dk.tt(xt.act-xt.impl):.2f}), |fark| medyan {(xt.act-xt.impl).abs().median()*1e4:.1f} bp")
print(f"  Tüm günler: fark ort {(x.act-x.impl).mean()*1e4:.1f} bp (t={dk.tt(x.act-x.impl):.2f})")

print("\n=== 7) Rastgele giriş permütasyonu (aynı sayıda rastgele gün, gün içi tutuş, 10.000 tekrar) ===")
pool = (SB.c / SB.o - 1).values
p1, mu, p95 = dk.perm_random_entry(pool, len(trT), trT.gross.mean(), reps=10000)
print(f"  SBIT: gözlenen brüt {trT.gross.mean()*1e4:.1f} bp; rastgele ort {mu*1e4:.1f} bp, %95 dilim {p95*1e4:.1f} bp; tek yönlü p={p1:.4f}; 5 gün seçimi için Bonferroni ×5 -> {min(1, p1*5):.3f}")
# Haftalık blok: hafta içindeki gün etiketlerini karıştır (hafta etkisi korunur)
rng = np.random.default_rng(11)
d = pd.DataFrame({"r": SB.c / SB.o - 1}); d["wk"] = d.index.to_period("W"); d["thu"] = d.index.dayofweek == 3
obs = d.r[d.thu].mean(); cnt = 0; reps = 5000
grp = [g.r.values for _, g in d.groupby("wk") if g.thu.any()]
for k in range(reps):
    m = np.mean([gg[rng.integers(len(gg))] for gg in grp])
    cnt += m >= obs
print(f"  Hafta içi etiket permütasyonu (her haftadan rastgele 1 gün): p={cnt/reps:.4f}")
# max-istatistik: 5 günden en iyisi bu kadar iyi olur mu
cnt = 0
dows = d.index.dayofweek.values; r = d.r.values
for k in range(reps):
    lab = dows.copy()
    for wk_idx in d.groupby("wk").indices.values():
        lab[wk_idx] = rng.permutation(lab[wk_idx])
    best = max(r[lab == j].mean() for j in range(5))
    cnt += best >= obs
print(f"  5 günün EN İYİSİ (seçim düzeltmeli, hafta içi permütasyon): p={cnt/reps:.4f}")

print("\n=== 8) Dayanak satırları: DOĞRU sıfır hipotezi (brüt; long maliyeti düşülmeden) ===")
BS = dk.btc_session("BTC-USD"); ES = dk.btc_session("ETH-USD")
rows8 = []
for nm, df in (("BTC 16:00ET (09:30 tahmini)", BS), ("ETH 16:00ET", ES), ("IBIT", IB), ("ETHA", lib.load("ETHA")), ("BITO", lib.load("BITO")),
               ("BITX", lib.load("BITX")), ("BLOK", lib.load("BLOK")), ("SPY", lib.load("SPY")), ("QQQ", lib.load("QQQ"))):
    for per, a, b in (("tüm", "2016-01-01", "2026-12-31"), ("2023-06+", "2023-06-01", "2026-12-31"), ("SBIT dönemi 2024-04+", "2024-04-02", "2026-12-31")):
        z = (df["c"] / df["o"] - 1)[a:b]
        zt = z[z.index.dayofweek == 3]; zo = z[z.index.dayofweek != 3]
        if len(zt) < 20: continue
        t_ = dk.tt(zt); rows8.append({"seri": nm, "donem": per, "n": len(zt), "per_brut_bp": zt.mean() * 1e4, "t_brut": t_, "p_brut": dk.pval(t_, len(zt)),
                                      "diger_gun_bp": zo.mean() * 1e4, "fark_t": (zt.mean() - zo.mean()) / np.sqrt(zt.var() / len(zt) + zo.var() / len(zo))})
T8 = pd.DataFrame(rows8); print(T8.round(4).to_string(index=False)); T8.to_csv(os.path.join(OUT, "S1_dayanak_brut.csv"), index=False)
# Ajanın FDR tablosunu brüt p ile yeniden kur: long ürünlerin net p'si yerine brüt p
F = pd.read_csv(os.path.join(ROOT, "sonuclar", "aile_kripto", "fdr_tum.csv"))
print(f"  Ajan fdr_tum: {len(F)} test, geçen {int(F.fdr.sum())}; geçenlerin net_bp<0 olanı {int((F.fdr & (F.net_bp < 0)).sum())}")
for lab in ["S1 aile BTC_ET", "S1 aile IBIT", "S1 aile BITO", "S1 aile ETHA", "S1 aile BITX", "S1 aile BLOK"]:
    r_ = F[F.test == lab]
    print(f"   {lab}: ajan p(net)={r_.p.iloc[0]:.6f}")
thr_agent = F[F.fdr].p.max()
print(f"  Ajanın sweep hariç BH eşiği p<={thr_agent:.6f}; sweep dahil p<=0.000100.  Brüt p'ler yukarıdaki tabloda (2023-06+ satırları): "
      + ", ".join(f"{r.seri} p={r.p_brut:.4f}" for r in T8[T8.donem == "2023-06+"].itertuples()))

print("\n=== 9) Uzun geçmiş: SBIT öncesi ve 2023 öncesi Perşembe gün içi (brüt, long; negatif = ters ürün lehine) ===")
G = lib.load("GBTC", clean=False); EE = lib.load("ETHE", clean=False)
def stock(sym):
    d = pd.read_parquet(os.path.join(ROOT, "data", "stock", sym + ".parquet")); return d[d["c"] > 0]
rows9 = []
for nm, df, a, b in (("GBTC tröst (OTC, ABD seansı)", G, "2019-01-17", "2024-01-10"), ("ETHE tröst", EE, "2019-05-21", "2024-07-22"),
                     ("BITO", lib.load("BITO"), "2021-10-19", "2024-04-01"), ("BITI (ters, −1x)", BI, "2022-06-21", "2024-04-01"),
                     ("BTC 16:00ET 2023-06..2024-03", BS, "2023-06-01", "2024-04-01"), ("MSTR hisse", stock("MSTR"), "2020-08-11", "2024-04-01"),
                     ("COIN hisse", stock("COIN"), "2021-04-14", "2024-04-01"), ("BLOK", lib.load("BLOK"), "2018-01-17", "2024-04-01"),
                     ("QQQ", lib.load("QQQ"), "2016-11-07", "2024-04-01")):
    z = (df["c"] / df["o"] - 1)[a:b]; z = z[np.isfinite(z)]
    zt = z[z.index.dayofweek == 3]; zo = z[z.index.dayofweek != 3]
    yr = (zt.groupby(zt.index.year).mean() * 1e4).round(0).to_dict()
    rows9.append({"seri": nm, "donem": f"{a}..{b}", "n": len(zt), "per_bp": zt.mean() * 1e4, "t": dk.tt(zt), "diger_bp": zo.mean() * 1e4,
                  "fark_t": (zt.mean() - zo.mean()) / np.sqrt(zt.var() / len(zt) + zo.var() / len(zo)), "yillik": yr})
T9 = pd.DataFrame(rows9); print(T9.round(2).to_string(index=False)); T9.to_csv(os.path.join(OUT, "S1_uzun_gecmis.csv"), index=False)
# GBTC tröst gün içi ile BTC seans getirisinin uyumu (2023-06..2024-01)
z = pd.DataFrame({"g": G.c / G.o - 1, "b": BS.c / BS.o - 1}).dropna()["2023-06-01":"2024-01-10"]
print(f"  GBTC tröst gün içi ~ BTC 09:30-16:00 korelasyonu (2023-06..2024-01): {z.g.corr(z.b):.3f} (n={len(z)})")
# SBIT-eşdeğeri: −2 × GBTC tröst Perşembe gün içi, maliyet 16 bp
zt = (G.c / G.o - 1)["2019-01-17":"2024-01-10"]; zt = zt[zt.index.dayofweek == 3]
eq = -2 * zt - cost("SBIT") / 1e4
print(f"  SBIT-eşdeğeri (−2×GBTC tröst gün içi, 16 bp) 2019-2023: n={len(eq)}, net {eq.mean()*1e4:.1f} bp, t={dk.tt(eq):.2f}; yıllık: {(eq.groupby(eq.index.year).mean()*1e4).round(0).to_dict()}")

print("\n=== 10) Hisse piyasası etkisi: IBIT ve BTC Perşembe gün içi ~ QQQ gün içi (2023-06+/2024-01+) ===")
Q = lib.load("QQQ")
for nm, df, a in (("IBIT", IB, "2024-01-11"), ("BTC 16:00ET", BS, "2023-06-01"), ("SBIT", SB, "2024-04-02")):
    z = pd.DataFrame({"y": df.c / df.o - 1, "q": Q.c / Q.o - 1}).dropna()[a:]
    z["thu"] = (z.index.dayofweek == 3).astype(float)
    X = np.column_stack([np.ones(len(z)), z.q.values, z.thu.values])
    b, *_ = np.linalg.lstsq(X, z.y.values, rcond=None); e = z.y.values - X @ b
    V = np.linalg.inv(X.T @ X) * (e @ e) / (len(z) - 3); tb = b / np.sqrt(np.diag(V))
    X0 = np.column_stack([np.ones(len(z)), z.thu.values]); b0, *_ = np.linalg.lstsq(X0, z.y.values, rcond=None)
    print(f"  {nm}: Perşembe kukla (QQQ'suz) {b0[1]*1e4:.1f} bp; QQQ kontrollü {b[2]*1e4:.1f} bp (t={tb[2]:.2f}); QQQ beta {b[1]:.2f}; "
          f"QQQ Perşembe ort {z.q[z.thu==1].mean()*1e4:.1f} bp")

print("\n=== 11) Perşembe CPI/PPI/olay günleri ve tatil kayması ===")
m = ~trT.entry_date.isin(cpi)
rep(trT[m].copy(), "SBIT Per CPI hariç")
print("\n=== 12) BITI (−1x) gerçek Perşembe ===")
for a, b, lab in (("2022-06-21", "2026-12-31", "tüm"), ("2022-06-21", "2024-04-01", "SBIT öncesi"), ("2024-04-02", "2026-12-31", "SBIT dönemi")):
    rep(intraday_trades(BI[a:b], thu(BI[a:b]), cost("BITI")), f"BITI Per {lab}")

pd.DataFrame(R).to_csv(os.path.join(OUT, "S1_ozet.csv"), index=False)
