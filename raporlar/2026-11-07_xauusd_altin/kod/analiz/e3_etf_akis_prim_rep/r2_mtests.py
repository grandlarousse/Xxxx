"""E3-1 / E3-2: m_t -> madenci ETF'leri IC testleri (bağımsız)."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)
sig = pd.read_parquet(f"{OUT}/sig_m.parquet"); days = sig.index
def half_days(days):
    hd = []
    for y in range(2008, 2027):
        nov = pd.date_range(f"{y}-11-01", f"{y}-11-30"); thx = nov[nov.dayofweek == 3][3]
        hd += [thx + pd.Timedelta(days=1), pd.Timestamp(f"{y}-12-24"), pd.Timestamp(f"{y}-07-03")]
    return pd.DatetimeIndex([d for d in hd if d in days])
HD = half_days(days); print("yarım gün sayısı:", len(HD))
rows = []
def R(t):
    c = yh(t).reindex(days); return np.log(c).diff()
targets = ["GDXJ", "GDX", "JNUG", "NUGT", "AEM", "KGC", "RING", "SGDM", "GLD", "SLV"]
for tgt in targets:
    r = R(tgt)
    for h in (1, 3, 5):
        y = fwd(r, h)
        for nm in ["zm", "m", "zm14"]:
            st = stats(sig[nm], y, h); st.update(target=tgt, h=h, pred=nm); rows.append(st)
res = pd.DataFrame(rows)[["target", "pred", "h", "n", "ic", "t", "ic_is", "t_is", "ic_oos", "t_oos", "t_22", "yrs"]]
res.to_csv(f"{OUT}/r2_mtests.csv", index=False)
print(res[(res.pred != "m") & res.target.isin(["GDXJ","GDX"])].to_string())
# GDXJ h1 ayrıntı: yarım günler hariç, eski sinyal, placebo kaydırmalar
r = R("GDXJ"); y1 = fwd(r, 1)
nohd = ~sig.index.isin(HD)
# yarım gün t ve t-1 yarım gün sonrası (xau_close_{t-1} anı ETF kapanışından sonra)
print("GDXJ h1 yarım günler hariç (t):", stats(sig.zm[nohd], y1[nohd], 1))
prev_hd = pd.Series(sig.index.isin(HD), index=sig.index).shift(1).fillna(False).astype(bool).values
print("GDXJ h1 yarım gün t ve t-1 hariç:", stats(sig.zm[nohd & ~prev_hd], y1[nohd & ~prev_hd], 1))
for k in (-1, 1, 2, 3):
    print(f"placebo zm.shift({k}) -> GDXJ h1:", ic(sig.zm.shift(k), y1, 5))
for tgt in ["GDXJ", "GDX"]:
    yy = fwd(R(tgt), 1)
    print(tgt, "m14 h1:", stats(sig.zm14, yy, 1))
# yıl yıl GDXJ IC
d = pd.concat([sig.zm, y1], axis=1).dropna(); d.columns = ["x", "y"]
print("GDXJ yıllık IC:", d.groupby(d.index.year).apply(lambda g: round(g.x.corr(g.y, method="spearman"), 3)).to_dict())
# göreli: GDXJ - beta*GLD, beta geçmiş 250 gün
rg = R("GLD")
for tgt in ["GDXJ", "GDX"]:
    rt = R(tgt)
    beta = (rt.rolling(250, min_periods=120).cov(rg) / rg.rolling(250, min_periods=120).var()).shift(1)
    rel = rt - beta * rg
    for h in (1, 5):
        print(f"göreli {tgt}-b*GLD h{h}:", stats(sig.zm, fwd(rel, h), h))
