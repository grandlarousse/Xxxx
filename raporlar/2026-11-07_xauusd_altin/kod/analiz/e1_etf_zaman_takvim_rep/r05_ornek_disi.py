"""5) Analistin görmediği veriyle sağlamlık:
(a) ÖRNEK ÖNCESİ (1995–2007): NYSE'de işlem gören altın madencisi hisselerinin eşit ağırlıklı sepeti ve tek tek hisseler
    -> takvim sepeti (ayın ilk işlem günü ∪ tatil öncesi), ≥5 gün düşüş sonrası 1 gün. SPY kontrol.
(b) Kesit: 2008–2026 diğer madenci ETF'leri (RING, SGDM, GOEX, SIL, SILJ) ve madenci olmayan plasebolar (XLE, COPX, EEM, SPY).
(c) GLD Ocak ve BollZ<-2: GLD 2005–2007 ve GC=F 2001–2007 (örnek öncesi)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
pd.set_option("display.width", 250)

CAL2 = xc.get_calendar("XNYS", start="1993-01-01", end="2027-12-31")
SS = CAL2.sessions_in_range("1994-01-03", END); SS = pd.DatetimeIndex(SS.tz_localize(None) if SS.tz is not None else SS)
rows = []
for rule in CAL2.regular_holidays.rules:
    for d in rule.dates(pd.Timestamp("1993-12-01"), pd.Timestamp("2027-01-31")):
        if d.dayofweek < 5: rows.append((pd.Timestamp(d), rule.name))
HH = pd.DataFrame(rows, columns=["date", "name"]).drop_duplicates("date").set_index("date").sort_index()
HH = HH[~HH.index.isin(SS)]
ix = pd.Series(SS, index=SS); ym = ix.dt.to_period("M"); FIRST = ym != ym.shift(1); FIRST.iloc[0] = False
nxt = ix.shift(-1)
PRE = pd.Series([((HH.index > d) & (HH.index < n)).any() if pd.notna(n) else False for d, n in zip(SS, nxt)], index=SS)
BASKET = FIRST | PRE
print("1994+ seans", len(SS), " tatil öncesi", int(PRE.sum()), " ilk gün", int(FIRST.sum()))

def lr(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); y.index = pd.to_datetime(y.index)
    a = y.adjclose.reindex(SS); r = np.log(a).diff()
    r[(r.abs() > 0.5)] = np.nan   # bariz veri hatası
    return r

def test(r, M, a, b, L=5):
    q = pd.concat([r.rename("y"), M.astype(float).rename("x")], axis=1).dropna()
    q = q[(q.index >= a) & (q.index <= b)]
    if len(q) < 200 or q.x.sum() < 10: return dict(n=len(q), n_ev=int(q.x.sum()), ev_bps=np.nan, oth_bps=np.nan, t=np.nan, yrs="")
    bb, tt = nw_ols(q.y.values, q.x.values, L)
    yr = q.groupby(q.index.year).apply(lambda g: g.y[g.x == 1].mean() - g.y[g.x == 0].mean())
    return dict(n=len(q), n_ev=int(q.x.sum()), ev_bps=round(q.y[q.x == 1].mean() * 1e4, 1), oth_bps=round(q.y[q.x == 0].mean() * 1e4, 1),
                t=round(tt[1], 2), yrs=f"{int((yr > 0).sum())}/{int(yr.notna().sum())}")

def bt_simple(r, M, a, b, cost=10):
    """getiri günü maskesi M -> yalnız uzun, 1 gün; maliyet giriş başına cost bps (ardışık günlerde tek)."""
    q = pd.concat([np.expm1(r).rename("y"), M.astype(float).rename("x")], axis=1).dropna(); q = q[(q.index >= a) & (q.index <= b)]
    entry = (q.x.diff().fillna(q.x) == 1).astype(float)
    p = q.x * q.y - entry * cost / 1e4
    return round(p.mean() * 252 / (p.std() * np.sqrt(252)), 2)

MINERS = ["NEM", "AEM", "KGC", "GFI", "HMY", "B", "AU", "RGLD", "AGI", "EGO", "IAG"]
RR = pd.DataFrame({t: lr(t) for t in MINERS})
cnt = RR.notna().sum(axis=1)
EW = RR.mean(axis=1).where(cnt >= 4)
print("EW madenci sepeti hisse sayısı (1995, 2005, 2015):", cnt.loc["1995"].mean().round(1), cnt.loc["2005"].mean().round(1), cnt.loc["2015"].mean().round(1))
SPY = lr("SPY"); GDX = lr("GDX"); GDXJ = lr("GDXJ")

out = []
WIN = [("1995-2007 (örnek öncesi)", "1995-01-01", "2007-12-31"), ("1995-2001", "1995-01-01", "2001-12-31"), ("2002-2007", "2002-01-01", "2007-12-31"),
       ("2008-2017", "2008-01-01", "2017-12-31"), ("2018-2026", "2018-01-01", END)]
for lab, M in [("sepet", BASKET), ("ilk_gun", FIRST), ("tatil_oncesi", PRE), ("son_gun", (ym != ym.shift(-1)))]:
    for nm, r in [("EW_madenci", EW), ("SPY", SPY), ("GDX", GDX), ("GDXJ", GDXJ)] + [(t, RR[t]) for t in ["NEM", "AEM", "KGC", "GFI", "HMY", "B", "AU", "RGLD"]]:
        for w, a, b in WIN:
            o = test(r, M, a, b)
            if o["n"] < 200: continue
            o.update(test=lab, seri=nm, donem=w, sh_net10=bt_simple(r, M, a, b))
            out.append(o)
O = pd.DataFrame(out); O.to_csv(f"{OUT}/r05_ornek_oncesi_takvim.csv", index=False)
print(O[O.seri.isin(["EW_madenci", "SPY", "GDX", "GDXJ"])].pivot_table(index=["test", "seri"], columns="donem", values="t", aggfunc="first").to_string())
print(O[O.seri.isin(["EW_madenci", "SPY"])][["test", "seri", "donem", "n_ev", "ev_bps", "oth_bps", "t", "yrs", "sh_net10"]].to_string())
# SPY kontrollü EW madenci (örnek öncesi)
q = pd.concat([EW.rename("y"), SPY.rename("s"), PRE.astype(float).rename("pre"), FIRST.astype(float).rename("first")], axis=1).dropna()
for w, a, b in WIN:
    qq = q[(q.index >= a) & (q.index <= b)]
    bb, tt = nw_ols(qq.y.values, qq[["s", "pre", "first"]].values, 5)
    print(f"EW madenci SPY kontrollü {w}: pre {bb[2]*1e4:.1f} bps t={tt[2]:.2f} | first {bb[3]*1e4:.1f} bps t={tt[3]:.2f}")
# tek tek hisseler, örnek öncesi sepet
print("\nÖrnek öncesi (1995-2007) tek hisse — sepet:")
print(O[(O.test == "sepet") & (O.donem == "1995-2007 (örnek öncesi)")][["seri", "n_ev", "ev_bps", "oth_bps", "t", "yrs", "sh_net10"]].to_string())

# (b) kesit 2008-2026
xs = []
for t in ["RING", "SGDM", "GOEX", "SIL", "SILJ", "GOAU", "XLE", "COPX", "EEM", "SPY", "GLD", "SLV"]:
    r = lr(t)
    for lab, M in [("sepet", BASKET), ("ilk_gun", FIRST), ("tatil_oncesi", PRE)]:
        o = test(r, M, "2008-01-01", END); o.update(test=lab, seri=t, sh_net10=bt_simple(r, M, "2008-01-01", END)); xs.append(o)
X = pd.DataFrame(xs); X.to_csv(f"{OUT}/r05_kesit_2008plus.csv", index=False)
print("\nKesit 2008+ (t):"); print(X.pivot_table(index="seri", columns="test", values="t").round(2).to_string())

# (c) C3 GDX ≥5 gün düşüş: örnek öncesi EW madenci ve tek hisseler
def streak(r):
    s = np.sign(r).fillna(0).values; o = np.zeros(len(s))
    for i in range(len(s)):
        if s[i] == 0: o[i] = 0
        elif i > 0 and np.sign(o[i - 1]) == s[i]: o[i] = o[i - 1] + s[i]
        else: o[i] = s[i]
    return pd.Series(o, index=r.index)
st_rows = []
for nm, r in [("EW_madenci", EW), ("GDX", GDX), ("GDXJ", GDXJ)] + [(t, RR[t]) for t in ["NEM", "AEM", "KGC", "GFI", "HMY", "B", "AU", "RGLD"]]:
    k = streak(r.fillna(0)).where(r.notna())
    for n_ in [4, 5]:
        pos = (k.shift(1) <= -n_).astype(float).where(k.shift(1).notna())
        y = r.shift(-1)
        for w, a, b in WIN:
            q = pd.concat([y.rename("y"), pos.rename("x")], axis=1).dropna(); q = q[(q.index >= a) & (q.index <= b)]
            if len(q) < 200 or q.x.sum() < 5: continue
            bb, tt = nw_ols(q.y.values, q.x.values, 5)
            st_rows.append(dict(seri=nm, n=n_, donem=w, n_sig=int(q.x.sum()), sig_bps=round(q.y[q.x == 1].mean() * 1e4, 1), t=round(tt[1], 2)))
SR = pd.DataFrame(st_rows); SR.to_csv(f"{OUT}/r05_seri_ornek_oncesi.csv", index=False)
print("\n≥n gün düşüş sonrası (t-1'e kadar) -> t kapanışı->t+1 (t):")
print(SR.pivot_table(index=["seri", "n"], columns="donem", values="t").round(2).to_string())
print(SR[SR.seri == "EW_madenci"].to_string())

# (d) GLD/GC=F Ocak ve BollZ, örnek öncesi
GLD = lr("GLD"); GC = lr("GC_F")
JAN = pd.Series(SS.month == 1, index=SS)
print("\nOcak (getiri günü maskesi):")
for nm, r in [("GLD", GLD), ("GC_F", GC)]:
    for w, a, b in [("2001-2007", "2001-01-01", "2007-12-31"), ("2005-2007", "2005-01-01", "2007-12-31"), ("2008-2017", "2008-01-01", "2017-12-31"), ("2018-2026", "2018-01-01", END), ("2008-2026", "2008-01-01", END)]:
        o = test(r, JAN, a, b); print(f"  {nm} {w}: n_ev={o['n_ev']} ev={o['ev_bps']} oth={o['oth_bps']} t={o['t']} yrs={o['yrs']}")
print("\nBollZ(20,2)_{t-1}<-2 -> 5 gün (t kapanışından):")
for nm, t_ in [("GLD", "GLD"), ("GC_F", "GC_F")]:
    y = pd.read_parquet(f"{S}/panel/yahoo/{t_}.parquet"); y.index = pd.to_datetime(y.index); c = y.adjclose.reindex(SS)
    r = np.log(c).diff(); r[r.abs() > 0.5] = np.nan
    z = (c - c.rolling(20).mean()) / c.rolling(20).std()
    pos = (z.shift(1) < -2).astype(float).where(z.shift(1).notna()); f5 = sum(r.shift(-k) for k in range(1, 6))
    for w, a, b in [("2001-2007", "2001-01-01", "2007-12-31"), ("2005-2007", "2005-01-01", "2007-12-31"), ("2008-2017", "2008-01-01", "2017-12-31"), ("2018-2026", "2018-01-01", END)]:
        q = pd.concat([f5.rename("y"), pos.rename("x")], axis=1).dropna(); q = q[(q.index >= a) & (q.index <= b)]
        if len(q) < 200 or q.x.sum() < 3: print(f"  {nm} {w}: yetersiz"); continue
        bb, tt = nw_ols(q.y.values, q.x.values, 5)
        print(f"  {nm} {w}: n_sig={int(q.x.sum())} sig={q.y[q.x==1].mean()*1e4:.1f} bps uncond={q.y.mean()*1e4:.1f} t={tt[1]:.2f}")
