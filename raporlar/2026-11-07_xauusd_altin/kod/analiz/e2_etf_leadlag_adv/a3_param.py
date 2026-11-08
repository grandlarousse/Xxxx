"""Hakem: parametre duyarlılığı (q, h, k, beta penceresi, tek faktör), giriş zamanlaması (açılış), kademesiz uygulama ve sabit komisyon."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
ADV = f"{S}/out/e2_etf_leadlag_adv"
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
X2 = pd.concat([R["GLD"], R["SPY"]], axis=1); X2.columns = ["GLD", "SPY"]
def lo(pos, r, h, c, dm=False): return backtest(pos.clip(lower=0), r, h, c, demean=dm)
def split(r, a, b=None):
    m = r.index >= a if b is None else (r.index >= a) & (r.index <= b); return r[m].dropna()
for und in ["GDXJ", "GDX"]:
    print(f"\n######## {und} ########")
    E = {}
    for W in (60, 120, 250, 500):
        B = roll_beta2(R[und], X2, W, min(60, W)).shift(1)
        E[W] = R[und] - B["GLD"] * R["GLD"] - B["SPY"] * R["SPY"]
    b1 = roll_beta(R[und], R["GLD"], 250, 60).shift(1); E["1f_GLD"] = R[und] - b1 * R["GLD"]
    rI = split(R[und], "2008-01-01", "2017-12-31"); rO = split(R[und], "2018-01-01"); r22 = split(R[und], "2022-01-01")
    print("beta penceresi / model duyarliligi (k=1 ve k=3, h=3, q=0.7): IC t tam/IS/OOS | OOS L, Ldm, I | 2022+ L, BH")
    for W, e in E.items():
        for k in (1, 3):
            x = e.rolling(k, min_periods=k).sum().shift(1); st = split_stats(x, fwd(R[und], 3), 3)
            pos = pos_from_signal(x, 1, 0.7)
            print(f"  W={W} k={k}: t {st['t']:+.2f}/{st['t_is']:+.2f}/{st['t_oos']:+.2f} | OOS L {lo(pos, rO, 3, 10)['sharpe']:.2f} Ldm {lo(pos, rO, 3, 10, True)['sharpe']:.2f} I {backtest(pos, rO, 3, 10)['sharpe']:.2f} | 22+ L {lo(pos, r22, 3, 10)['sharpe']:.2f}")
    e = E[250]
    print("q x h ızgarası (k=1 ve k=3; W=250): IS ideal | OOS L | OOS Ldm  [10bp]")
    for k in (1, 2, 3, 5):
        x = e.rolling(k, min_periods=k).sum().shift(1)
        for h in (1, 2, 3, 4, 5):
            row = []
            for q in (0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9):
                pos = pos_from_signal(x, 1, q)
                row.append(f"q{q}: {backtest(pos, rI, h, 10)['sharpe']:+.2f}/{lo(pos, rO, h, 10)['sharpe']:+.2f}/{lo(pos, rO, h, 10, True)['sharpe']:+.2f}")
            print(f"  k{k} h{h} " + " ".join(row))
    bh = backtest(pd.Series(1.0, index=rO.index), rO, 1, 0)["sharpe"]; print("  OOS B&H", round(bh, 2))
# ---- giriş zamanlaması: C2j sinyali (t-1 kapanışında bilinir), giriş gün t AÇILIŞ, çıkış t+3 kapanış / t+3 açılış
yj = pd.read_parquet(f"{P}/yahoo/GDXJ.parquet"); yj.index = pd.to_datetime(yj.index)
f = (yj.adjclose / yj.close)  # temettü+bölünme faktörü -> açılışa uygula
oj = (yj.open * f).reindex(d.index); cj = d["c_GDXJ"]
x = pd.read_pickle(f"{OUT}/s1_signals.pkl")[("GDXJ~GLD+SPY", 1)]
for nm, y in [("close_t->close_t+3 (analist)", np.log(cj.shift(-3) / cj)),
              ("open_t->close_t+3", np.log(cj.shift(-3) / oj)),
              ("open_t->open_t+3", np.log(oj.shift(-3) / oj)),
              ("close_t-1->close_t+2 (sinyal aninda giris)", np.log(cj.shift(-2) / cj.shift(1))),
              ("open_t->close_t (gun t ici)", np.log(cj / oj)),
              ("close_t-1->open_t (gece)", np.log(oj / cj.shift(1)))]:
    st = split_stats(x, y, 3)
    print(f"[giris] {nm}: ic {st['ic']:+.3f} t {st['t']:+.2f} is {st['t_is']:+.2f} oos {st['t_oos']:+.2f}")
# ---- kademesiz uygulama + sabit komisyon: sinyal > q70 ise tam pozisyon al, 3 gün tut (yeni sinyal süreyi uzatır)
rO = split(R["GDXJ"], "2018-01-01")
pos = pos_from_signal(x, 1, 0.7).clip(lower=0)
hold = pd.Series(0.0, index=pos.index); left = 0
for i, (t, p) in enumerate(pos.items()):
    if p > 0: left = 3
    hold.iloc[i] = 1.0 if left > 0 else 0.0
    left = max(left - 1, 0)
for c in (10, 20, 40):
    a = backtest(hold, rO, 1, c); print(f"[kademesiz] GDXJ OOS {c}bp: Sharpe {a['sharpe']:.2f} ann {a['ann_ret']*100:.1f}% expo {a['exposure']:.2f} turn/yr {a['turnover_per_yr']:.1f}")
# sabit 1.5 USD/emir: kademeli uygulamada emir sayısı = eff değişen gün sayısı (her alt portföy ayrı emir değil netleştirilmiş)
eff = sum(pos.shift(k).fillna(0) for k in range(3)) / 3
ch = (eff.diff().abs() > 1e-9)
ch = ch[ch.index >= "2018-01-01"]; yrs = (rO.index[-1] - rO.index[0]).days / 365.25
print(f"[komisyon] kademeli: yılda emir {ch.sum()/yrs:.0f}; kademesiz: yılda emir {(hold.diff().abs()>0)[hold.index>='2018-01-01'].sum()/yrs:.0f}")
for acct in (2000, 5000, 20000):
    for nm, nord, gross in [("kademeli", ch.sum() / yrs, lo(pos, rO, 3, 0)), ("kademesiz", (hold.diff().abs() > 0)[hold.index >= '2018-01-01'].sum() / yrs, backtest(hold, rO, 1, 0))]:
        drag = nord * 1.5 / acct     # yıllık getiri kaybı (komisyon), spread ayrı: ~3 bp gidiş-dönüş
        spread = gross["turnover_per_yr"] / 2 * 3 / 1e4
        net = gross["ann_ret"] - drag - spread
        print(f"   hesap {acct} USD {nm}: brüt {gross['ann_ret']*100:.1f}%/yıl, komisyon {drag*100:.1f}%, spread {spread*100:.2f}% -> net Sharpe {net/gross['ann_vol']:.2f}")
