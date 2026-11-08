"""(a) ETF kendi zaman serisi: momentum/dönüş, MA, Donchian, RSI(2)/Connors, Bollinger, ardışık seriler, >2σ günler.
Bilgi zamanı: 'strict' = ETF kapanışları t-1 ve öncesi (t-1 16:00 ET; yazın 20:00, kışın 21:00 UTC).
'nc' (kapanışa yakın) = son nokta gün t 15:00 ET tahmini fiyat p15 = c_{t-1}·xau_cut_t/xau_close_{t-1} (altın) ya da XAG cut-cut (gümüş);
xau_cut = Dukascopy spot 15:00 ET (yazın 19:00, kışın 20:00 UTC) -> karar anında bilinir.
"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("a_")
TG = ["GLD", "GDX", "GDXJ", "SLV"]; NC = ["GLD", "SLV"]; HS = [1, 3, 5]
rows = []

def logc(t): return np.log(D[f"c_{t}"])

def add(fam, t, ver, name, x, h, kind="ic", note=""):
    y = fwd(R[t], h)
    st = split_stats(x, y, h) if kind == "ic" else rstats(x, y, h)
    tid = f"{fam}|{t}|{ver}|{name}|h{h}"
    reg(fam, tid, f"{name}[{ver}]", h, st, note)
    rows.append(dict(family=fam, target=t, ver=ver, pred=name, h=h, kind=kind, ic=st.get("ic"), t=st.get("t"), t_is=st.get("t_is"), t_oos=st.get("t_oos"),
                     t_22=st.get("t_22"), yrs_same=st.get("yrs_same_sign"), yrs=st.get("yrs"), n=st.get("n"), nsig=int((x.fillna(0) != 0).sum()) if kind == "rule" else None))

# ---- yardımcı göstergeler: 'strict' -> seri t-1'e kadar, sonra shift(1); 'nc' -> son nokta p15_t
def rsi_wilder(p, n=2):
    d = p.diff(); up = d.clip(lower=0); dn = (-d).clip(lower=0)
    au = up.ewm(alpha=1 / n, adjust=False).mean(); ad = dn.ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + au / ad.replace(0, np.nan)), au, ad

def nc_sma(c, q, n):  # c = kapanış fiyat serisi, q = p15 fiyatı; pencere [c_{t-n+1..t-1}, q_t]
    return (c.rolling(n - 1).sum().shift(1) + q) / n

def nc_std(c, q, n):
    s1 = c.rolling(n - 1).sum().shift(1) + q; s2 = (c ** 2).rolling(n - 1).sum().shift(1) + q ** 2
    return np.sqrt(np.maximum(s2 / n - (s1 / n) ** 2, 0) * n / (n - 1))

def streak(sign_series):
    s = sign_series.fillna(0).values; out = np.zeros(len(s))
    for i in range(len(s)):
        if s[i] == 0: out[i] = 0
        elif i > 0 and np.sign(out[i - 1]) == s[i]: out[i] = out[i - 1] + s[i]
        else: out[i] = s[i]
    return pd.Series(out, index=sign_series.index)

feats = {}
for t in TG:
    lc = logc(t); c = np.exp(lc); r = R[t]
    vers = [("strict", None)] + ([("nc", p15(t))] if t in NC else [])
    for ver, lq in vers:
        # "son" log fiyat ve "son" getiri
        if ver == "strict":
            last = lc.shift(1); rlast = r.shift(1); prev_lc = lambda k: lc.shift(1 + k)
        else:
            last = lq; rlast = lq - lc.shift(1); prev_lc = lambda k: lc.shift(k)
        q = np.exp(last)
        # 1) momentum / dönüş (sürekli, Spearman IC)
        for k in [1, 2, 3, 5, 10, 20, 60, 120, 250]:
            x = last - prev_lc(k); feats[(t, ver, f"mom{k}")] = x
            for h in HS: add("a_mom", t, ver, f"mom{k}", x, h, note="IC>0 momentum, <0 dönüş")
        # 2) MA filtreleri (±1)
        for n in [10, 20, 50, 100, 200]:
            sma = (c.rolling(n).mean().shift(1)) if ver == "strict" else nc_sma(c, q, n)
            x = np.sign(q - sma).where(sma.notna()); feats[(t, ver, f"ma{n}")] = x
            for h in HS: add("a_ma", t, ver, f"P>SMA{n}", x, h, "rule")
        for f_, s_ in [(5, 20), (10, 50), (20, 100), (50, 200)]:
            if ver == "strict": a = c.rolling(f_).mean().shift(1); b = c.rolling(s_).mean().shift(1)
            else: a = nc_sma(c, q, f_); b = nc_sma(c, q, s_)
            x = np.sign(a - b).where(b.notna()); feats[(t, ver, f"x{f_}_{s_}")] = x
            for h in HS: add("a_ma", t, ver, f"SMA{f_}>SMA{s_}", x, h, "rule")
        # 3) Donchian (durum: üst kırılımda +1, alt kırılımda -1, ters kırılıma kadar tut)
        for N in [20, 55]:
            hi = c.rolling(N).max().shift(1); lo = c.rolling(N).min().shift(1)   # t-1 penceresi (son nokta hariç)
            if ver == "strict": cl = c.shift(1); hi = hi.shift(1); lo = lo.shift(1)
            else: cl = q
            ev = pd.Series(np.where(cl > hi, 1.0, np.where(cl < lo, -1.0, np.nan)), index=IDX)
            x = ev.ffill().where(hi.notna()); feats[(t, ver, f"don{N}")] = x
            for h in HS: add("a_don", t, ver, f"Donchian{N}_state", x, h, "rule")
        # 4) RSI(2) / Connors
        rs, au, ad = rsi_wilder(c, 2)
        if ver == "strict": rsi = rs.shift(1); sma200 = c.rolling(200).mean().shift(1)
        else:
            d0 = q - c.shift(1); au2 = 0.5 * au.shift(1) + 0.5 * d0.clip(lower=0); ad2 = 0.5 * ad.shift(1) + 0.5 * (-d0).clip(lower=0)
            rsi = 100 - 100 / (1 + au2 / ad2.replace(0, np.nan)); sma200 = nc_sma(c, q, 200)
        feats[(t, ver, "rsi2")] = rsi
        for thr in [5, 10, 20]:
            for filt in [True, False]:
                L = (rsi < thr) & ((q > sma200) if filt else True); Sx = (rsi > 100 - thr) & ((q < sma200) if filt else True)
                x = pd.Series(np.where(L, 1.0, np.where(Sx, -1.0, 0.0)), index=IDX).where(rsi.notna() & sma200.notna())
                nm = f"RSI2<{thr}{'&SMA200' if filt else ''}"; feats[(t, ver, nm)] = x
                for h in HS: add("a_rsi", t, ver, nm, x, h, "rule", "+1 aşırı satım al, -1 aşırı alım (ters ETF)")
        # 5) Bollinger(20,2)
        if ver == "strict": m = c.rolling(20).mean().shift(1); sd = c.rolling(20).std().shift(1)
        else: m = nc_sma(c, q, 20); sd = nc_std(c, q, 20)
        z = (q - m) / sd; feats[(t, ver, "bbz")] = z
        for h in HS: add("a_boll", t, ver, "BollZ20", z, h, note="sürekli")
        x = pd.Series(np.where(z < -2, 1.0, np.where(z > 2, -1.0, 0.0)), index=IDX).where(z.notna()); feats[(t, ver, "boll2")] = x
        for h in HS: add("a_boll", t, ver, "Boll2_revert", x, h, "rule", "+1 alt bant altı, -1 üst bant üstü")
        # 6) ardışık seriler
        sg = np.sign(r)
        stk = streak(sg)
        if ver == "strict": sk = stk.shift(1)
        else:
            s0 = np.sign(rlast); prev = stk.shift(1)
            sk = pd.Series(np.where(s0 == 0, 0, np.where(np.sign(prev) == s0, prev + s0, s0)), index=IDX).where(prev.notna())
        feats[(t, ver, "streak")] = sk
        for h in HS: add("a_streak", t, ver, "streak", sk, h, note="sürekli")
        for n_ in [3, 4, 5]:
            x = pd.Series(np.where(sk <= -n_, 1.0, np.where(sk >= n_, -1.0, 0.0)), index=IDX).where(sk.notna())
            feats[(t, ver, f"streak{n_}")] = x
            for h in HS: add("a_streak", t, ver, f"streak>={n_}_revert", x, h, "rule", "+1 n gün düşüş sonrası al")
        # 7) >2σ günler (σ20 son günden önce bilinen)
        sig20 = r.rolling(20).std()
        zz = (rlast / (sig20.shift(2) if ver == "strict" else sig20.shift(1)))
        feats[(t, ver, "z1")] = zz
        for thr in [2.0, 3.0]:
            x = pd.Series(np.where(zz > thr, -1.0, np.where(zz < -thr, 1.0, 0.0)), index=IDX).where(zz.notna())
            feats[(t, ver, f"sig{thr:g}")] = x
            for h in HS: add("a_sigma", t, ver, f">{thr:g}sigma_revert", x, h, "rule", "+1 büyük düşüş sonrası al (dönüş), -1 büyük yükseliş sonrası")

tab = pd.DataFrame(rows)
from scipy import stats as sst
tab["p"] = 2 * (1 - sst.norm.cdf(tab.t.abs())); tab["q_fdr_family"] = bh_fdr(tab.p.fillna(1).values)
tab.to_csv(f"{O}/a_ts_all.csv", index=False)
pd.to_pickle(feats, f"{O}/a_feats.pkl")
print("test sayısı (a):", len(tab))
print(tab.sort_values("t", key=abs, ascending=False).head(40).to_string())
