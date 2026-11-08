"""(a) aday kuralların uygulanabilir backtest'i: yalnız uzun / ters ETF / kaldıraçlı uzun; uzun ve kısa bacak ayrımı; Connors klasik."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("a2_")
F = pd.read_pickle(f"{O}/a_feats.pkl")
tabs = []; legs = []

def legs_test(name, t, x, h):
    y = fwd(R[t], h)
    for leg, m in [("uzun", (x > 0)), ("kisa", (x < 0))]:
        s = m.astype(float).where(x.notna())
        st = rstats(s, y, h); reg("a2_leg", f"a2_leg|{name}|{t}|{leg}|h{h}", f"{name}:{leg}", h, st, "bacak: sinyal günü vs diğer günler")
        on = y[s == 1]; off = y[s == 0]
        legs.append(dict(rule=name, target=t, h=h, leg=leg, n_sig=int(s.sum()), mean_sig_bps=round(on.mean() * 1e4, 1), mean_other_bps=round(off.mean() * 1e4, 1),
                         t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), t_22=round(st["t_22"], 2) if pd.notna(st["t_22"]) else None,
                         yrs=f"{st['yrs_same_sign']}/{st['yrs']}"))

C = {}
# 1) GLD kapanışa yakın 1 günlük dönüş: bugün 15:00'e kadar düştüyse al
C["GLD_nc_rev1"] = ("GLD", 1, -np.sign(F[("GLD", "nc", "mom1")]))
C["GLD_nc_streakrev"] = ("GLD", 1, -np.sign(F[("GLD", "nc", "streak")]))
# 2) Bollinger dönüş (madenciler)
for t in ["GDX", "GDXJ"]:
    for h in [3, 5]: C[f"{t}_boll2_h{h}"] = (t, h, F[(t, "strict", "boll2")])
C["GDX_streak4_h3"] = ("GDX", 3, F[("GDX", "strict", "streak4")]); C["GDX_streak4_h5"] = ("GDX", 5, F[("GDX", "strict", "streak4")])
# 3) trend filtreleri (yaygın kullanılan, referans)
for t in ["GLD", "GDX", "SLV"]:
    C[f"{t}_mom250_h5"] = (t, 5, np.sign(F[(t, "strict", "mom250")]))
    C[f"{t}_ma200_h5"] = (t, 5, F[(t, "strict", "ma200")])
    C[f"{t}_x50_200_h5"] = (t, 5, F[(t, "strict", "x50_200")])
C["GLD_ma10_h1"] = ("GLD", 1, F[("GLD", "strict", "ma10")])   # IS'te en iyi (t_is 2,5) -> OOS çöküş örneği
C["GLD_rsi2_10f_nc_h3"] = ("GLD", 3, F[("GLD", "nc", "RSI2<10&SMA200")])
# 4) Connors klasik (GLD, kapanışa yakın karar): RSI2<10 & P>SMA200 -> al; P>SMA5 olunca sat. Simetrik kısa: RSI2>90 & P<SMA200, P<SMA5 olunca kapat.
c = D.c_GLD; q = np.exp(p15("GLD"))
rsi = F[("GLD", "nc", "rsi2")]; sma200 = (c.rolling(199).sum().shift(1) + q) / 200; sma5 = (c.rolling(4).sum().shift(1) + q) / 5
posL = np.zeros(len(IDX)); posS = np.zeros(len(IDX))
for i in range(1, len(IDX)):
    if posL[i - 1] == 1: posL[i] = 0 if q.iloc[i] > sma5.iloc[i] else 1
    else: posL[i] = 1 if (rsi.iloc[i] < 10 and q.iloc[i] > sma200.iloc[i]) else 0
    if posS[i - 1] == 1: posS[i] = 0 if q.iloc[i] < sma5.iloc[i] else 1
    else: posS[i] = 1 if (rsi.iloc[i] > 90 and q.iloc[i] < sma200.iloc[i]) else 0
conn = pd.Series(posL - posS, index=IDX)
C["GLD_connors_classic"] = ("GLD", 1, conn)
st = rstats(conn, fwd(R.GLD, 1), 1); reg("a2_connors", "a2_connors|GLD|nc|classic|h1", "Connors RSI2<10&SMA200, çıkış SMA5 (nc)", 1, st)
st2 = rstats(pd.Series(posL, index=IDX), fwd(R.GLD, 1), 1); reg("a2_connors", "a2_connors|GLD|nc|classic_long|h1", "Connors yalnız uzun bacak (nc)", 1, st2)

for nm, (t, h, x) in C.items():
    legs_test(nm, t, x, h)
    df = strat_table(x, h, t, nm); tabs.append(df)
    # IAU ve GLDM ile aynı sinyal (GLD sinyali)
    if t == "GLD" and nm in ("GLD_nc_rev1", "GLD_mom250_h5", "GLD_ma200_h5"):
        for alt in ["IAU", "GLDM"]: tabs.append(strat_table(x, h, alt, nm + f"@{alt}", lev=False))

T = pd.concat(tabs); T.to_csv(f"{O}/a_strat_all.csv", index=False)
L = pd.DataFrame(legs); L.to_csv(f"{O}/a_strat_legs.csv", index=False)
pv = pivot_short(T); pv.to_csv(f"{O}/a_strat_pivot.csv")
pd.set_option("display.width", 250)
print(pv.to_string()); print(L.to_string())
# işlem sıklığı
print(T[(T.cost == "temel") & (T.period == "full") & (T.version == "long_only")][["strategy", "rt_yr", "sh", "bh_sh", "mdd"]].to_string())
