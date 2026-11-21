"""L5 ön hesap: trend / momentum / rotasyon filtrelerinin 1-3 günlük kapanış-kapanış etkisi.
Kullanım: python3 ek/literatur/l5_on_hesap.py [aqr_tsmom.xlsx]
Çıktı: ek/literatur/l5_on_hesap_sonuc.txt
Not: ön hesap; işlem maliyeti yok, çoklu test düzeltmesi yok. Kesin test backtest ajanında.
"""
import sys, numpy as np, pandas as pd
K = "/home/user/Xxxx/raporlar/2026-11-21_abd_sektor_emtia_leadlag/"
out = []
def p(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# ---------- 1. AQR TSMOM faktörü: dönemlere göre ----------
if len(sys.argv) > 1:
    x = pd.read_excel(sys.argv[1], header=None)
    hdr = x.index[x[1].astype(str).str.strip().eq("TSMOM")][0]
    cols = ["Date"] + [str(c).strip() for c in x.iloc[hdr, 1:]]
    d = x.iloc[hdr + 1:].copy(); d.columns = cols
    d = d[pd.to_datetime(d["Date"], errors="coerce").notna()]
    d["Date"] = pd.to_datetime(d["Date"]); d = d.set_index("Date").apply(pd.to_numeric, errors="coerce")
    p("== AQR TSMOM (aylık fazla getiri), yıllık ortalama % / oynaklık % / Sharpe / t")
    for a, b in [("1985", "2009"), ("2010", "2014"), ("2015", "2026"), ("2020", "2026")]:
        s = d.loc[a:b]
        for c in d.columns:
            r = s[c].dropna()
            if len(r) < 24: continue
            m, v = r.mean() * 12, r.std() * np.sqrt(12)
            p(f"{a}-{b} {c:10s} n={len(r)} ort={100*m:6.2f} vol={100*v:6.2f} SR={m/v:5.2f} t={r.mean()/r.std()*np.sqrt(len(r)):5.2f}")

# ---------- 2. Yahoo paneli ----------
C = pd.read_parquet(K + "veri/panel_adjclose.parquet")
O = pd.read_parquet(K + "veri/panel_ao.parquet")
SEK = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]
EMT = ["GLD", "SLV", "USO", "UNG", "DBA", "DBC", "DBB", "CPER"]
EVR = SEK + EMT + ["SPY", "QQQ", "IWM", "SMH", "XBI", "XME", "GDX", "XOP", "KRE", "ITB"]
EVR = [s for s in EVR if s in C]
r1 = C[EVR].pct_change()
f1 = r1.shift(-1)                                   # t kapanış -> t+1 kapanış
f3 = C[EVR].shift(-3) / C[EVR] - 1                  # t -> t+3
gece = (O[EVR].shift(-1) / C[EVR] - 1)              # t kapanış -> t+1 açılış
gun = (C[EVR].shift(-1) / O[EVR].shift(-1) - 1)     # t+1 açılış -> t+1 kapanış

def stat(mask, fwd, step=1):
    v = fwd[mask].stack().dropna()
    if step > 1:
        v = fwd[mask].iloc[::step].stack().dropna()
    if len(v) < 50: return "n<50"
    return f"n={len(v):6d} ort={1e4*v.mean():6.1f}bp t={v.mean()/v.std()*np.sqrt(len(v)):5.2f} isabet={100*(v>0).mean():4.1f}% sd={1e4*v.std():5.0f}bp"

sma200 = C[EVR].rolling(200).mean(); sma50 = C[EVR].rolling(50).mean()
ret252 = C[EVR] / C[EVR].shift(252) - 1; ret20 = C[EVR] / C[EVR].shift(20) - 1
hi252 = C[EVR].rolling(252).max()
sinyaller = {
    "fiyat>SMA200": C[EVR] > sma200, "fiyat<SMA200": C[EVR] < sma200,
    "SMA50>SMA200": sma50 > sma200, "SMA50<SMA200": sma50 < sma200,
    "12a getiri>0": ret252 > 0, "12a getiri<0": ret252 < 0,
    "20g getiri>0": ret20 > 0, "20g getiri<0": ret20 < 0,
    "52h zirveye %2 yakın": C[EVR] >= 0.98 * hi252, "52h zirveden %20+ aşağı": C[EVR] <= 0.80 * hi252,
}
DON = [("2005", "2014"), ("2015", "2026")]
for grup, ad in [(SEK, "SEKTÖR ETF"), ([e for e in EMT if e in C], "EMTİA ETF")]:
    p(f"\n== {ad}: {grup}")
    for a, b in DON:
        p(f"-- {a}-{b}  koşulsuz 1g: {stat(pd.DataFrame(True, index=C.index, columns=EVR)[grup].loc[a:b], f1[grup].loc[a:b])}")
        for k, m in sinyaller.items():
            mm = m[grup].loc[a:b]
            p(f"{k:24s} 1g {stat(mm, f1[grup].loc[a:b])} | 3g(örtüşmesiz) {stat(mm, f3[grup].loc[a:b], 3)}")
        for k in ["fiyat>SMA200", "fiyat<SMA200"]:
            mm = sinyaller[k][grup].loc[a:b]
            p(f"  {k} gece {stat(mm, gece[grup].loc[a:b])} | gün içi {stat(mm, gun[grup].loc[a:b])}")

# ---------- 3. Sektör rotasyonu (kesitsel, 9 SPDR) ----------
p("\n== Sektör rotasyonu: 9 SPDR, sıralama penceresi L gün, en iyi 3 - eşit ağırlık, 1 gün tutma (günlük yeniden)")
R = r1[SEK]; ew = R.mean(axis=1)
for L in [1, 5, 20, 60, 120, 252]:
    sc = C[SEK] / C[SEK].shift(L) - 1
    rk = sc.rank(axis=1)
    top = (rk >= 7).astype(float); bot = (rk <= 3).astype(float)
    top = top.div(top.sum(axis=1), axis=0); bot = bot.div(bot.sum(axis=1), axis=0)
    lt = (top * R.shift(-1)).sum(axis=1, min_count=1) - ew.shift(-1)
    lb = (bot * R.shift(-1)).sum(axis=1, min_count=1) - ew.shift(-1)
    turn = top.diff().abs().sum(axis=1)
    for a, b in DON:
        s, q, tt = lt.loc[a:b].dropna(), lb.loc[a:b].dropna(), turn.loc[a:b].mean()
        p(f"L={L:3d} {a}-{b} en iyi3-EW: {1e4*s.mean():5.2f}bp/g t={s.mean()/s.std()*np.sqrt(len(s)):5.2f} yıllık={252*100*s.mean():5.2f}% | en kötü3-EW: {1e4*q.mean():5.2f}bp/g t={q.mean()/q.std()*np.sqrt(len(q)):5.2f} | günlük ciro={tt:4.2f}")

# ---------- 4. SPY trend filtresi: risk mi getiri mi ----------
p("\n== SPY: fiyat>SMA200 iken / değilken sonraki gün")
s = "SPY"
for a, b in DON:
    up = (C[s] > sma200[s]).loc[a:b]; fw = f1[s].loc[a:b]
    for k, m in [("üstü", up), ("altı", ~up & sma200[s].loc[a:b].notna())]:
        v = fw[m].dropna()
        p(f"{a}-{b} SMA200 {k}: gün oranı={100*m.mean():4.1f}% ort={1e4*v.mean():5.1f}bp sd={1e4*v.std():4.0f}bp yıllık SR={v.mean()/v.std()*np.sqrt(252):5.2f}")

# ---------- 5. Kaldıraçlı ETF erimesi: 3x ETF'in yıllık getirisi - 3 x endeks yıllık getirisi ----------
p("\n== Kaldıraçlı ETF: yıllık getiri farkı (LETF - L*taban) ve taban yıllık varyansı")
for le, ba, L in [("SOXL", "SOXX", 3), ("TQQQ", "QQQ", 3), ("UPRO", "SPY", 3), ("ERX", "XLE", 2), ("NUGT", "GDX", 2), ("UCO", "USO", 2)]:
    if le not in C or ba not in C: continue
    yy = []
    for y in range(2011, 2026):
        cy = C[[le, ba]].loc[str(y)].dropna()
        if len(cy) < 200: continue
        rl = cy[le].iloc[-1] / cy[le].iloc[0] - 1; rb = cy[ba].iloc[-1] / cy[ba].iloc[0] - 1
        var = (cy[ba].pct_change().var() * 252)
        yy.append((y, rl, L * rb, var))
    if yy:
        df = pd.DataFrame(yy, columns=["y", "letf", "Lbaz", "var"])
        teori = -(L * L - L) / 2 * df["var"]
        p(f"{le}/{ba} L={L}: ort fark={100*(df.letf-df.Lbaz).mean():6.1f}%/yıl, ort teorik oynaklık terimi -(L²-L)/2·σ²={100*teori.mean():6.1f}%, LETF<L×baz olan yıl {(df.letf<df.Lbaz).sum()}/{len(df)}")

open(K + "ek/literatur/l5_on_hesap_sonuc.txt", "w").write("\n".join(out))

# ---------- 6. Sağlamlık: gün kümelenmeli t (her gün koşulu sağlayan ETF'lerin ortalaması = bir gözlem) ----------
p("\n== Gün kümelenmeli t (aynı gün ETF'ler arası korelasyonu hesaba katar)")
def kume(mask, fwd, a, b, step=1):
    m = mask.loc[a:b]; f = fwd.loc[a:b]
    s = f.where(m).mean(axis=1).dropna()
    if step > 1: s = s.iloc[::step]
    return f"gün={len(s):5d} ort={1e4*s.mean():6.1f}bp t={s.mean()/s.std()*np.sqrt(len(s)):5.2f}"
EM = [e for e in EMT if e in C]
for grup, ad, ks in [(SEK, "SEK", ["fiyat>SMA200", "fiyat<SMA200", "12a getiri<0", "52h zirveden %20+ aşağı"]),
                     (EM, "EMT", ["fiyat>SMA200", "fiyat<SMA200", "SMA50>SMA200", "SMA50<SMA200", "12a getiri>0", "52h zirveye %2 yakın"])]:
    for a, b in DON:
        for k in ks:
            p(f"{ad} {a}-{b} {k:24s} 1g {kume(sinyaller[k][grup], f1[grup], a, b)} | 3g {kume(sinyaller[k][grup], f3[grup], a, b, 3)}")
# emtia: trend üstü - trend altı farkı, gün bazında uzun-kısa (SMA50>SMA200 al, altında sat), eşit ağırlık
for a, b in DON:
    L_ = f1[EM].where(sinyaller["SMA50>SMA200"][EM]).mean(axis=1); S_ = f1[EM].where(sinyaller["SMA50<SMA200"][EM]).mean(axis=1)
    d_ = (L_.fillna(0) - S_.fillna(0)).loc[a:b].dropna()
    p(f"EMT {a}-{b} uzun(SMA50>200)-kısa(SMA50<200) EW: {1e4*d_.mean():5.2f}bp/g yıllık SR={d_.mean()/d_.std()*np.sqrt(252):5.2f} t={d_.mean()/d_.std()*np.sqrt(len(d_)):5.2f}")
open(K + "ek/literatur/l5_on_hesap_sonuc.txt", "w").write("\n".join(out))
