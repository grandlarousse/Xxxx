"""Denetim kripto_S2: BTC trend filtresi (c > SMA10 > SMA50) -> IBIT 3 gün long.
Çalıştır: python3 -I kod/denetim_kripto/d_S2.py   (lib.trades/evaluate kullanılmaz)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dk, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
ROOT = dk.ROOT; OUT = dk.OUT
R = []
def rep(tr, label):
    s = dk.summ(tr, label); R.append(s)
    print(f"{label:52s} n={s['n']:4d} brüt {s.get('brut_bp', np.nan):7.1f} net {s.get('net_bp', np.nan):7.1f} t={s.get('t', np.nan):5.2f} "
          f"kaz {s.get('kazanma', np.nan):.2f} PF {s.get('pf', np.nan):.2f} IS {s.get('is_net_bp', np.nan):6.1f} (t {s.get('is_t', np.nan):.2f}) "
          f"OOS {s.get('oos_net_bp', np.nan):6.1f} (t {s.get('oos_t', np.nan):.2f}) yıl+ {s.get('yil_pozitif', np.nan):.2f} maxDD {s.get('maxdd', np.nan):.3f} "
          f"en kötü {s.get('en_kotu_bp', np.nan):.0f} best5- {s.get('en_iyi5_haric_net_bp', np.nan):.1f}")
    return s

def trend(c, a=10, b=50):
    sa = c.rolling(a).mean(); sb = c.rolling(b).mean()
    s = (c > sa) & (sa > sb); s.iloc[:max(a, b)] = False
    return s.fillna(False)

SP_IBIT = dk.tarama_spread("IBIT"); SP_ETHA = dk.tarama_spread("ETHA")
cI = lambda pos=2500: dk.comm_bp(pos) + SP_IBIT
BD = dk.btc_daily_on_nyse("BTC-USD"); ED = dk.btc_daily_on_nyse("ETH-USD")
print(f"BTC_D (benim): {BD.index[0].date()}..{BD.index[-1].date()} n={len(BD)}; maliyet IBIT {cI():.2f} bp")
# Ajanın serisiyle karşılaştırma (yalnız kontrol amaçlı okunur)
sys.path.insert(0, os.path.join(dk.KOD, "ajan_kripto"))
import kr
AB = kr.crypto_daily_proxy("BTC-USD")
j = pd.DataFrame({"ben": BD.c, "ajan": AB.c}).dropna()
print(f"Ajan BTC_D ile: ortak {len(j)} gün, maks göreli fark {(j.ben/j.ajan-1).abs().max():.2e}; yalnız bende {len(BD.index.difference(AB.index))}, yalnız ajanda {len(AB.index.difference(BD.index))}")

print("\n=== 1) Yeniden üretim (BTC_D, C0 h=3, IBIT maliyeti) ===")
sig = trend(BD.c)
tr = dk.sim(BD, sig, 3, "C0", cI()); s0 = rep(tr, "BTC_D C0 h3")
tr.to_csv(os.path.join(OUT, "S2_BTC_D_C0_islemler.csv"), index=False)
ag = pd.read_csv(os.path.join(ROOT, "sonuclar", "aile_kripto", "aday_detay.csv"))
r_ = ag[ag.label == "S2 BTC_D C0"].iloc[0]
print(f"  ajan: n={r_.n}, net {r_.mean_net_bp:.1f}, t={r_.t:.2f}, IS {r_.is_net_bp:.1f}, OOS {r_.oos_net_bp:.1f}")
rep(dk.sim(BD, sig, 3, "C1", cI()), "BTC_D C1 h3")
for pos in (1000, 10000):
    rep(dk.sim(BD, sig, 3, "C0", cI(pos)), f"BTC_D C0 h3 maliyet {pos}$")
print("  yıllık (C0):", dk.yearly(tr)["mean"].to_dict())
print("  yıllık işlem sayısı:", dk.yearly(tr)["count"].to_dict())

print("\n=== 2) Dönem hariç ve uç değerler ===")
for lab, m in (("2020 hariç", tr.sig_date.dt.year != 2020), ("2022 hariç", tr.sig_date.dt.year != 2022),
               ("2020 ve 2022 hariç", ~tr.sig_date.dt.year.isin([2020, 2022])), ("2017 hariç (ilk boğa)", tr.sig_date.dt.year != 2017),
               ("2023+ (spot ETF öncesi/sonrası birebir dönem)", tr.sig_date >= "2023-01-01"), ("2024-01-11+ (IBIT dönemi)", tr.sig_date >= "2024-01-11")):
    rep(tr[m].copy(), "BTC_D C0 " + lab)
top = tr.sort_values("gross", ascending=False).head(5)
print("  En iyi 5 işlem:", [(str(a.date()), round(g * 1e4)) for a, g in zip(top.sig_date, top.gross)], " toplam katkı:", round(top.net.sum() / tr.net.sum(), 3), "(net toplamın payı)")

print("\n=== 3) Rastgele giriş permütasyonu (aynı n, aynı 3 gün tutuş, 10.000 tekrar) ===")
fwd = (BD.c.shift(-3) / BD.c - 1)
for lab, a, b in (("tüm", "2016-01-01", "2026-12-31"), ("IS", "2016-01-01", "2021-12-31"), ("OOS", "2022-01-01", "2026-12-31")):
    tt_ = tr[(tr.sig_date >= a) & (tr.sig_date <= b)]
    pool = fwd[a:b].dropna()
    # havuzu sinyalin olabileceği günlerle sınırla (ilk 50 gün hariç)
    pool = pool[pool.index >= sig[sig].index.min()]
    p, mu, p95 = dk.perm_random_entry(pool.values, len(tt_), tt_.gross.mean(), reps=10000)
    print(f"  {lab}: gözlenen brüt {tt_.gross.mean()*1e4:.1f} bp (n={len(tt_)}); rastgele ort {mu*1e4:.1f}, %95 {p95*1e4:.1f}; tek yönlü p={p:.4f}")

print("\n=== 4) Parametre komşuluğu (yalnız IS'te seçim; IS/OOS raporu) ===")
rows = []
for a in (5, 7, 10, 13, 15, 20):
    for b in (30, 40, 50, 60, 75, 100):
        if a >= b: continue
        t_ = dk.sim(BD, trend(BD.c, a, b), 3, "C0", cI()); s = dk.summ(t_)
        rows.append({"kisa": a, "uzun": b, "n": s["n"], "net": s["net_bp"], "t": s["t"], "is": s["is_net_bp"], "is_t": s["is_t"], "oos": s["oos_net_bp"], "oos_t": s["oos_t"]})
G = pd.DataFrame(rows); G.to_csv(os.path.join(OUT, "S2_komsuluk.csv"), index=False)
print(G.pivot(index="kisa", columns="uzun", values="oos").round(0).to_string()); print("  ^ OOS net bp")
print(G.pivot(index="kisa", columns="uzun", values="oos_t").round(2).to_string()); print("  ^ OOS t")
print(f"  OOS net>0 olan kombinasyon: {(G.oos>0).sum()}/{len(G)}; OOS t>=2: {(G.oos_t>=2).sum()}; IS'te en iyi: {G.sort_values('is_t').iloc[-1][['kisa','uzun','is','oos']].to_dict()}")
for h in (1, 2, 3, 5):
    rep(dk.sim(BD, sig, h, "C0", cI()), f"BTC_D C0 h{h} (tutuş komşuluğu)")

print("\n=== 5) Zaman kayması: 00:00 UTC (BTC_D) yerine 16:00 ET (2023-06+ ortak dönem) ===")
BS = dk.btc_session("BTC-USD")
sigS = trend(BS.c)
for lab, df, sg in (("BTC_D 2023-06+", BD["2023-03-01":], trend(BD.c)["2023-03-01":]), ("BTC 16:00ET 2023-06+", BS, sigS)):
    t_ = dk.sim(df, sg, 3, "C0", cI()); t_ = t_[t_.sig_date >= "2023-08-01"]; rep(t_, lab + " C0")
    t_ = dk.sim(df, sg, 3, "C1", cI()); t_ = t_[t_.sig_date >= "2023-08-01"]; rep(t_, lab + " C1")
t_ = dk.sim(BS, sigS, 3, "O1", cI()); rep(t_[t_.sig_date >= "2023-08-01"], "BTC 16:00ET O1 (09:30 tahmini)")

print("\n=== 6) ETF dönemi: IBIT (kendi grafiği ve BTC 16:00 ET sinyali) ===")
IB = lib.load("IBIT")
for lab, sg in (("IBIT kendi sinyali", trend(IB.c)), ("IBIT <- BTC 16:00ET sinyali", sigS.reindex(IB.index).fillna(False))):
    for mode in ("C0", "O1", "C1"):
        rep(dk.sim(IB, sg, 3, mode, cI()), f"{lab} {mode}")
GB = lib.load("GBTC"); rep(dk.sim(GB, trend(GB.c), 3, "C0", dk.comm_bp(2500) + dk.tarama_spread("GBTC")), "GBTC (ETF) kendi C0")
# IBIT'te ham sinyal eşleşmesi: IBIT kendi sinyali ile BTC_D sinyalinin aynı gün uyumu
z = pd.DataFrame({"ib": trend(IB.c), "bd": trend(BD.c).reindex(IB.index)}).dropna()
print(f"  IBIT kendi sinyali ~ BTC_D sinyali günlük uyum: {(z.ib == z.bd).mean():.3f}")

print("\n=== 7) ETH_D (aile versiyonu) ===")
cE = dk.comm_bp(2500) + SP_ETHA
tE = dk.sim(ED, trend(ED.c), 3, "C0", cE); rep(tE, "ETH_D C0 h3")
print("  yıllık:", dk.yearly(tE)["mean"].to_dict())
rep(dk.sim(ED, trend(ED.c), 3, "C1", cE), "ETH_D C1 h3")
EA = lib.load("ETHA")
for mode in ("C0", "O1", "C1"):
    rep(dk.sim(EA, trend(EA.c), 3, mode, cE), f"ETHA kendi {mode}")

print("\n=== 8) Drift: koşulsuz 3 gün ve 'kenar' ===")
for lab, a, b in (("IS", "2016-01-01", "2021-12-31"), ("OOS", "2022-01-01", "2026-12-31")):
    tt_ = tr[(tr.sig_date >= a) & (tr.sig_date <= b)]; u = fwd[a:b].dropna()
    print(f"  {lab}: strateji brüt {tt_.gross.mean()*1e4:.1f}; koşulsuz 3g {u.mean()*1e4:.1f}; kenar {(tt_.gross.mean()-u.mean())*1e4:.1f} bp; "
          f"kenar t~{(tt_.gross.mean()-u.mean())/(tt_.gross.std(ddof=1)/np.sqrt(len(tt_))):.2f}")
# Al-tut ile karşılaştırma: pozisyonda olma oranı ve aynı dönemde maruziyet başına getiri
days_in = len(tr) * 3; tot_days = len(BD[BD.index >= tr.sig_date.min()])
print(f"  Piyasada olma oranı: {days_in/tot_days:.2f}")

pd.DataFrame(R).to_csv(os.path.join(OUT, "S2_ozet.csv"), index=False)
