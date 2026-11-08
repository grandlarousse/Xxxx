"""VİOP XAUUSD OI 5g % değişimi × sign(5g uzlaşma getirisi), t-1 bülteni. Ham viop_long'dan.
OI değişimi: vadesi o gün dolan kontrat hariç (expiry > date) bütün vadelerin oi_chg toplamı / (oi - oi_chg) toplamı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
T = viop_target(); days = T.index; r = T.ret
L = pd.read_parquet(f"{P}/viop_long.parquet"); x = L[L.root == "XAUUSD"].copy(); x["date"] = pd.to_datetime(x.date); x["expiry"] = pd.to_datetime(x.expiry)
# oi_chg ham sütunu kendi hesabımla tutarlı mı? (aynı kontrat oi farkı)
x = x.sort_values(["code", "date"]); x["oi_prev_own"] = x.groupby("code").oi.shift(1)
own = (x.oi - x.oi_prev_own); print("oi_chg == oi - oi_prev (aynı kontrat) oranı:", float(((own - x.oi_chg).abs() < 0.5)[own.notna() & x.oi_chg.notna()].mean()))
live = x[x.expiry > x.date]
agg = live.groupby("date").agg(doi=("oi_chg", "sum"), oi=("oi", "sum")).reindex(days)
drel = agg.doi / (agg.oi - agg.doi)
oi5 = drel.rolling(5).sum(); r5 = r.rolling(5).sum()
xt = (oi5 * np.sign(r5)).shift(1)                 # t-1 bülteni
xt0 = (oi5 * np.sign(r5))                         # aynı gün (uygulanamaz)
# alternatif: OI seviyesinden yüzde değişim (5 gün)
alt = (np.log(agg.oi).diff(5) * np.sign(r5)).shift(1)
A = pd.read_csv(f"{S}/out/a6_akis_konum_cin/e_viop_features_t1.csv", index_col=0, parse_dates=True)["oi_d5_x_sgnret5"]
print("corr(benim, analist):", round(xt.corr(A.reindex(days)), 5))
G15 = pd.Series(gold_at(days + pd.Timedelta(hours=15)), index=days); G07 = pd.Series(gold_at(days + pd.Timedelta(hours=7)), index=days)
C = pd.DataFrame({"s_r1": np.log(G15 / G15.shift(1)), "s_r5": np.log(G15 / G15.shift(5)), "s_0715": np.log(G15 / G07), "v_r1": r.shift(1)})
rows = []
for lab, s in [("t-1 (ana)", xt), ("aynı gün", xt0), ("logOI d5 alt", alt), ("t-2", xt.shift(1))]:
    for h in (1, 5):
        st = split(s, T[f"fwd{h}"], h)
        sgn = np.sign(split(s[s.index <= IS_END], T[f"fwd{h}"][T.index <= IS_END], h)["ic"])
        pos = (sgn * np.sign(s)).fillna(0.0); o = periods(pos, r, h, 5.0); o10 = periods(pos, r, h, 10.0)
        xz = (s - s.mean()) / s.std(); d = pd.concat([T[f"fwd{h}"].rename("y"), xz.rename("x"), C], axis=1).dropna()
        b, tt, n = nw_t(d.y.values, np.column_stack([np.ones(len(d)), d.drop(columns="y").values]), max(h, 5))
        dO = d[d.index > IS_END]; bO, tO, _ = nw_t(dO.y.values, np.column_stack([np.ones(len(dO)), dO.drop(columns="y").values]), max(h, 5))
        pn = stagger(pos, r, h)["pnl"]; yr = pn.groupby(pn.index.year).apply(lambda q: q.mean() / q.std() * np.sqrt(252)).round(2).to_dict()
        rows.append(dict(ver=lab, h=h, ic=st["ic"], t=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], yrs=st["yrs"], is_sign=sgn, t_ctrl=tt[1], t_ctrl_oos=tO[1],
                         sh_is=o["is"]["LS"], sh_oos=o["oos"]["LS"], sh_oos_dm=o["oos"]["LS_dm"], sh_oos10=o10["oos"]["LS"], long_oos=o["oos"]["long"], short_oos=o["oos"]["short"],
                         chg=(pos.diff().abs() > 0).sum() / len(pos) * 252, yearly_sh=yr))
df = pd.DataFrame(rows); pd.set_option("display.width", 300); print(df.drop(columns="yearly_sh").round(3).to_string(index=False))
print(df.iloc[1].yearly_sh); df.to_csv(f"{OUT}/r8_oi.csv", index=False)
