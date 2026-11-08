"""5) Aday stratejilerin tekrar üretilebilir değerlendirmesi (sayıları basar). Çalıştır: python3 -I kod/ajan_kripto/05_adaylar.py
Önce 02, 03, 04 çalışmış olmalı (FDR için onların test tablolarını okur).

kripto_S1  Perşembe gün içi ters BTC: Perşembe açılışında SBIT (−2x BTC) al, aynı gün kapanışta sat. (alternatif: BITI −1x)
           Kaynak: genel kütüphane CA_car (Çarşamba sinyali, O1 h=1) aile içinde FDR'yi geçen tek takvim satırı (BTC_ET, BITO).
kripto_S2  BTC trend filtresi: kapanış > SMA10 ve SMA10 > SMA50 (genel kütüphane MO_trend_10_50) -> IBIT long, 3 işlem günü.
           Dayanak uzun testi BTC_D (2016-11..2026-11) üzerinde; ETF'ye aktarım BTC 16:00 ET / IBIT kendi grafiği.
Çıktı: sonuclar/aile_kripto/aday_ozet.csv, aday_<id>_islemler.csv, aday_<id>_detay.csv, fdr_tum.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import kr, lib
import strategies as S

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 50); pd.set_option("display.max_rows", 300)
OUT = kr.OUT
BTC_D = kr.crypto_daily_proxy("BTC-USD"); ETH_D = kr.crypto_daily_proxy("ETH-USD")
BTC_ET = kr.crypto_et_proxy("BTC-USD"); ETH_ET = kr.crypto_et_proxy("ETH-USD")
SER = {"BTC_D": BTC_D, "ETH_D": ETH_D, "BTC_ET": BTC_ET, "ETH_ET": ETH_ET}
def ser(nm): return SER[nm] if nm in SER else lib.load(nm)
def spread(nm): return kr.spread_bp({"BTC_D": "IBIT", "BTC_ET": "IBIT", "ETH_D": "ETHA", "ETH_ET": "ETHA"}.get(nm, nm))

def ev(nm, sig, h, mode, label):
    df = ser(nm)
    s, tr = kr.full_eval(df, sig.reindex(df.index).fillna(False), h, mode, spread(nm), label=label)
    s["seri"] = nm
    return s, tr

def line(s):
    if s.get("n", 0) == 0: return "n=0"
    return (f"n={s['n']}, brüt {s['mean_gross_bp']:.1f} bp, net {s['mean_net_bp']:.1f} bp, t={s['t']:.2f}, kazanma {s['win']:.2f}, "
            f"PF {s['pf']:.2f}, IS {s.get('is_net_bp', np.nan):.1f} / OOS {s.get('oos_net_bp', np.nan):.1f} bp, yıl+ {s['years_pos_frac']:.2f}, "
            f"maxDD {s['maxdd']:.3f}, en kötü {s['worst_bp']:.0f} bp, kenar {s.get('edge_bp', np.nan):.1f} bp (t={s.get('t_edge', np.nan):.2f})")

rows = []
# =================================================================================================
print("=" * 100); print("kripto_S1: Perşembe gün içi ters BTC (SBIT; alternatif BITI)"); print("=" * 100)
def wed(df): return pd.Series(df.index.dayofweek == 2, index=df.index)   # Çarşamba sinyali -> O1 = Perşembe açılış, h=1 -> Perşembe kapanış
S1 = {}
for nm in ["SBIT", "BITI"]:
    df = ser(nm)
    for mode, h in (("O1", 1), ("C0", 1), ("C1", 1)):
        s, tr = ev(nm, wed(df), h, mode, f"S1 {nm} {mode}")
        S1[(nm, mode)] = (s, tr)
        print(f"{nm} {mode} h={h} (C0=Çar kapanış->Per kapanış, C1=Per kapanış->Cum kapanış): ", line(s))
        if mode == "O1":
            print(f"   maliyet duyarlılığı net: 1.000$ {s['net_1000']:.1f} | 2.500$ {s['net_2500']:.1f} | 10.000$ {s['net_10000']:.1f} bp; ilk yarı {s['h1_net_bp']:.1f} / ikinci yarı {s['h2_net_bp']:.1f} bp")
        s.update({"aday": "kripto_S1", "rol": "işlem" if mode == "O1" else "mod_sağlamlık"}); rows.append(s)
# dayanak / aile: long araçlarda Perşembe gün içi (negatif = ters ürün lehine)
print("\nDayanak ve aile (long ürünlerde Perşembe gün içi; NEGATİF değer ters ürün lehine):")
for nm in ["BTC_ET", "ETH_ET", "IBIT", "BITO", "BITX", "ETHA", "MSTU", "CONL", "BLOK", "SPY", "QQQ"]:
    df = ser(nm)
    s, tr = ev(nm, wed(df), 1, "O1", f"S1 aile {nm}")
    print(f"  {nm:7s}", line(s))
    s.update({"aday": "kripto_S1", "rol": "aile/dayanak (long; negatif=ters lehine)"}); rows.append(s)
    if nm == "BITO":
        tb = tr.copy(); tb["yil"] = tb.sig_date.dt.year
        print("     BITO yıllık (gün içi, bp):", (tb.groupby("yil").gross.mean() * 1e4).round(1).to_dict(), " n:", tb.groupby("yil").size().to_dict())
        pre = tb[tb.sig_date < "2023-06-01"]
        print(f"     BITO keşif dönemi ÖNCESİ (2021-10..2023-05, saatlik BTC verisi yokken): n={len(pre)}, ort {pre.gross.mean()*1e4:.1f} bp, t={kr.tstat(pre.gross):.2f}  (pozitif = ters ürün ALEYHİNE)")
# SBIT yıllık ve uç değer kontrolü
s_, tr1 = S1[("SBIT", "O1")]
tr1.to_csv(os.path.join(OUT, "aday_kripto_S1_islemler.csv"), index=False)
t1 = tr1.copy(); t1["yil"] = t1.sig_date.dt.year
print("\nSBIT O1 yıllık net bp:", (t1.groupby("yil").net.mean() * 1e4).round(1).to_dict(), " n:", t1.groupby("yil").size().to_dict())
srt = t1.net.sort_values(ascending=False)
print(f"SBIT en iyi 5 işlem hariç net ort {srt.iloc[5:].mean()*1e4:.1f} bp (t={kr.tstat(srt.iloc[5:]):.2f}); medyan {t1.net.median()*1e4:.1f} bp")
# CPI günleri hariç
cpi = set(pd.to_datetime(pd.read_csv(os.path.join(kr.ROOT, "data", "events", "cpi.csv")).date))
m = ~t1.entry_date.isin(cpi)
print(f"SBIT CPI günü olan Perşembeler hariç: n={m.sum()}, net {t1.net[m].mean()*1e4:.1f} bp, t={kr.tstat(t1.net[m]):.2f}")
# diğer günlerde aynı gün içi ters işlem (seçim yanlılığı kontrolü)
print("SBIT gün içi (O1 h=1) haftanın diğer günleri (seçim kontrolü):")
for dw, nmw in ((0, "Pzt"), (1, "Sal"), (2, "Çar"), (3, "Per"), (4, "Cum")):
    df = ser("SBIT"); sg = pd.Series(df.index.dayofweek == (dw - 1) % 5 if dw > 0 else df.index.dayofweek == 4, index=df.index)
    s, tr = ev("SBIT", sg, 1, "O1", "")
    print(f"   {nmw}: n={s['n']}, net {s['mean_net_bp']:.1f}, t={s['t']:.2f}")

# =================================================================================================
print("\n" + "=" * 100); print("kripto_S2: BTC trend filtresi (kapanış>SMA10 ve SMA10>SMA50) -> IBIT long 3 gün"); print("=" * 100)
trend = S.LIB["MO_trend_10_50"]
S2 = {}
def tsig(df):
    sg = trend(df, None).fillna(False); sg.iloc[:60] = False; return sg
for nm, modes in (("BTC_D", ("C0", "C1")), ("ETH_D", ("C0", "C1")), ("BTC_ET", ("C0", "O1", "C1")), ("ETH_ET", ("C0", "O1", "C1"))):
    for mode in modes:
        s, tr = ev(nm, tsig(ser(nm)), 3, mode, f"S2 {nm} {mode}")
        S2[(nm, mode)] = (s, tr)
        print(f"{nm:6s} {mode} h=3: ", line(s))
        s.update({"aday": "kripto_S2", "rol": "dayanak uzun test" if nm.endswith("_D") else "dayanak 16:00 ET"}); rows.append(s)
s, tr = S2[("BTC_D", "C0")]
u = lib.uncond(BTC_D, 3, "C0").dropna()
for nmp, a, b in (("IS", "2016-01-01", "2021-12-31"), ("OOS", "2022-01-01", "2026-12-31")):
    tt = tr[(tr.sig_date >= a) & (tr.sig_date <= b)]; uu = u[a:b]
    print(f"   BTC_D C0 {nmp}: n={len(tt)}, net {tt.net.mean()*1e4:.1f} bp (t={kr.tstat(tt.net):.2f}); koşulsuz 3g {uu.mean()*1e4:.1f} bp -> kenar {(tt.gross.mean()-uu.mean())*1e4:.1f} bp")
tb = tr.copy(); tb["yil"] = tb.sig_date.dt.year
print("   BTC_D C0 yıllık net bp:", (tb.groupby("yil").net.mean() * 1e4).round(0).to_dict())
# komşu parametreler (yalnız raporlama; seçim yapılmadı)
print("   Komşu parametreler BTC_D C0 h=3 (SMA kısa/uzun): ", end="")
for a_, b_ in ((5, 50), (10, 30), (10, 50), (20, 50), (10, 100)):
    c = BTC_D["c"]; sg = (c > c.rolling(a_).mean()) & (c.rolling(a_).mean() > c.rolling(b_).mean()); sg.iloc[:60] = False
    s2, _ = ev("BTC_D", sg, 3, "C0", "")
    print(f"({a_},{b_}): net {s2['mean_net_bp']:.0f} t={s2['t']:.2f} IS {s2['is_net_bp']:.0f} OOS {s2['oos_net_bp']:.0f}; ", end="")
print()
# ETF'ye aktarım: (i) IBIT kendi grafiği, (ii) BTC 16:00 ET sinyali IBIT'te
print("\nETF'ye aktarım:")
for etf, base in (("IBIT", None), ("IBIT", "BTC_ET"), ("FBTC", None), ("BITX", "BTC_ET"), ("ETHA", None), ("ETHA", "ETH_ET"), ("ETHU", "ETH_ET"),
                  ("BLOK", None), ("MSTU", None), ("CONL", None), ("BITO", None)):
    df = ser(etf)
    sg = tsig(df) if base is None else tsig(ser(base)).reindex(df.index).fillna(False)
    for mode in ("C0", "O1", "C1"):
        s, tr = ev(etf, sg, 3, mode, f"S2 {etf} sinyal={base or 'kendi'} {mode}")
        print(f"  {etf:5s} sinyal={base or 'kendi':6s} {mode}: ", line(s))
        if etf == "IBIT" and base == "BTC_ET" and mode == "C0":
            print(f"     maliyet duyarlılığı net: 1.000$ {s['net_1000']:.1f} | 2.500$ {s['net_2500']:.1f} | 10.000$ {s['net_10000']:.1f} bp")
            tr.to_csv(os.path.join(OUT, "aday_kripto_S2_islemler.csv"), index=False)
        s.update({"aday": "kripto_S2", "rol": f"ETF aktarım (sinyal {base or 'kendi'})"}); rows.append(s)

A = pd.DataFrame(rows)
A.to_csv(os.path.join(OUT, "aday_detay.csv"), index=False)

# =================================================================================================
# Tüm testler üzerinde BH-FDR (q=0.10)
print("\n" + "=" * 100); print("BH-FDR (q=0.10) — ailenin tüm testleri"); print("=" * 100)
P = []
g = pd.read_csv(os.path.join(OUT, "genel_aile_satirlar.csv"))
P += [("genel", f"{r.sym}|{r.sig}|{r['mode']}|h{r.h}|{r.exit}", r.p, r.mean_net_bp) for _, r in g.iterrows()]
h = pd.read_csv(os.path.join(OUT, "hipotez_testleri.csv"))
P += [("hipotez", f"{r.hipotez}|{r.seri}|{r['mode']}|h{r.h}", r.p, r.mean_net_bp) for _, r in h.iterrows()]
e = pd.read_csv(os.path.join(OUT, "leadlag_ek_testler.csv"))
for _, r in e.iterrows():
    for c in ("lag_t_kendi_kontrollu", "yetisme_t_kendi_kontrollu"):
        P.append(("leadlag_ek", f"{r.hedef}<-{r.oncu}|{c}|h{r.h}", r["p_" + c], np.nan))
k = pd.read_csv(os.path.join(OUT, "leadlag_kural_testleri.csv"))
P += [("leadlag_kural", f"{r.label}|{r['mode']}", r.p, r.mean_net_bp) for _, r in k.iterrows()]
# aday ek satırları (komşu, aktarım)
P += [("aday", r.label, r.p, r.mean_net_bp) for _, r in A.iterrows() if isinstance(r.label, str) and r.label]
F = pd.DataFrame(P, columns=["kaynak", "test", "p", "net_bp"]).dropna(subset=["p"])
n_sweep = 765 * 4
F["fdr"] = lib.bh_fdr(F.p.values, 0.10)
thr = F[F.fdr].p.max() if F.fdr.any() else np.nan
F.to_csv(os.path.join(OUT, "fdr_tum.csv"), index=False)
print(f"Kendi p'li test sayısı: {len(F)} (+ leadlag_sweep aile satırları {n_sweep} test, orada 0 FDR) -> toplam ~{len(F) + n_sweep}")
print(f"FDR geçen: {int(F.fdr.sum())}, p eşiği {thr}")
print(F[F.fdr].sort_values("p").to_string(index=False))
# toplam (sweep dahil) eşik: sweep p'lerini ekleyerek
L = pd.read_csv(os.path.join(kr.ROOT, "sonuclar", "leadlag_sweep.csv")); L = L[L.target.isin(kr.FAM)]
pp = np.concatenate([F.p.values] + [L["p_" + c].dropna().values for c in ["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]])
ff = lib.bh_fdr(pp, 0.10)
print(f"Sweep dahil toplam {len(pp)} test: FDR geçen {int(ff.sum())}, p eşiği {pp[ff].max() if ff.any() else np.nan}")
for lab in ["S1 SBIT O1", "S1 BITI O1", "S1 aile BTC_ET", "S1 aile BITO", "S2 BTC_D C0", "S2 BTC_D C1", "S2 IBIT sinyal=BTC_ET C0"]:
    r = F[F.test == lab]
    if len(r): print(f"  {lab}: p={r.p.iloc[0]:.5f}, FDR={'GEÇTİ' if r.fdr.iloc[0] else 'geçmedi'}")
gg = F[(F.kaynak == "genel") & F.test.str.contains(r"BTC_ET\|CA_car\|O1\|h1|BITO\|CA_car\|O1\|h1|ETH_ET\|CA_car\|O1\|h1")]
print(gg.to_string(index=False))
