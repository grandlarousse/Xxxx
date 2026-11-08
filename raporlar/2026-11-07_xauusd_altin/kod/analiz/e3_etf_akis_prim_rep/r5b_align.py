"""BIST BYF saatlik bar zaman hizası: yaz (14:30 barı var) ve kış (yok) dönemlerinde BYF bar kapanışlarının gram altınla hizası."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
def duka(sym):
    x = pd.read_parquet(f"{P}/duka/{sym}.parquet")["c"]; x.index = x.index + pd.Timedelta(hours=1); return x[~x.index.duplicated()]
xau = xau_hourly(); usd = duka("USDTRY")
yu = pd.read_parquet(f"{P}/yahoo_h/USDTRY_X.parquet")["close"]; yu.index = yu.index + pd.Timedelta(hours=1)
usd = usd.combine_first(yu[yu.index > usd.index.max()])
gram = (np.log(xau) + np.log(usd.reindex(xau.index))).dropna()
for t in ["GLDTR", "ZGOLD"]:
    h = pd.read_parquet(f"{OUT}/bist_{t}_1h.parquet"); h["day"] = h.index.normalize(); h["hm"] = h.index.strftime("%H:%M")
    has = h.groupby("day").hm.apply(lambda s: (s == "14:30").any())
    h["summer"] = h.day.map(has)
    h = h[h.hm != "15:00"]
    out = []
    for seas in [True, False]:
        g = h[h.summer == seas].copy()
        # ardışık barlar (aynı gün) arası BYF log getirisi; bar kapanış anı hipotezi T = label + 1h + shift
        g["lc"] = np.log(g.close); g["r"] = g.groupby("day").lc.diff()
        g = g.dropna(subset=["r"])
        for shift_h in (-1, 0, 1):
            # bar k kapanışı T_k = label_k + 1h + shift; gram getirisi [T_{k-1}, T_k] için iki komşu tam saat ortalaması
            T = g.index + pd.Timedelta(hours=1 + shift_h)
            T0 = T - pd.Timedelta(hours=1)
            def gat(ts):
                fl = ts.floor("h"); ce = ts.ceil("h")
                return 0.5 * (gram.reindex(fl).values + gram.reindex(ce).values)
            rg = gat(T) - gat(T0)
            ok = ~np.isnan(rg)
            out.append(dict(etf=t, summer=seas, shift_h=shift_h, n=int(ok.sum()), corr=round(np.corrcoef(g.r.values[ok], rg[ok])[0, 1], 3)))
    print(pd.DataFrame(out).to_string())
