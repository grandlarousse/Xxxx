"""r4: (i) C5 farkinin nedeni: NY-satir tabanli (analist tarzi) Asya artigini ham veriden kur ve karsilastir;
(ii) kayittaki p'lerden BH-FDR q'yu kendi kodumla yeniden hesapla; (iii) aday sinyaller arasi korelasyon (bagimsizlik);
(iv) OOS Sharpe'larin t'si (SR*sqrt(yil)); (v) B&H'nin ilk gun dahil/haric farki."""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag_rep")
from rep_lib import *
Z = pd.read_pickle(f"{OUT}/r1_signals.pkl"); SIG, R, LP, cal = Z["SIG"], Z["R"], Z["LP"], Z["cal"]
out = {}
# (i) NY-satir tabanli Asya artigi
ph, pm = gold_price_series()
t07 = pd.DatetimeIndex(cal).tz_localize("UTC") + pd.Timedelta(hours=7)
g07 = pd.Series(price_at(ph, pm, t07)[0].values, index=cal)
pan = pd.read_parquet(f"{P}/panel_etf.parquet"); pan.index = pd.to_datetime(pan.index)
out["xau07_vs_panel_maxreldiff"] = float((g07 / pan["xau_07utc"] - 1).abs().max())
ES = []
for stk, idx in (("2899.HK", "_HSI"), ("1818.HK", "_HSI"), ("600547.SS", "000001.SS")):
    ps = yahoo(stk); pi = yahoo(idx)
    ip = ps.index.searchsorted(cal, side="right") - 1          # tarih <= t olan son yerel kapanis
    asof = pd.Series(ps.values[ip], index=cal); dts = pd.Series(ps.index[ip], index=cal)
    asofi = pd.Series(pi.reindex(ps.index).values[ip], index=cal)
    fresh = dts.ne(dts.shift(1))
    rs = np.log(asof).diff().where(fresh); rm = np.log(asofi).diff().where(fresh)
    last = np.log(g07).where(fresh).ffill().shift(1)
    rg = (np.log(g07) - last).where(fresh)
    X = pd.concat([rg.rename("g"), rm.rename("m")], axis=1)
    B = roll_ols(rs, X, 250, 120).shift(1)
    ES.append((rs - B["g"] * rg - B["m"] * rm).rename(stk))
E = pd.concat(ES, axis=1); compNY = E.mean(axis=1)
y3 = fwd_ret(LP["GLD"], 3)
for nm, x in (("yerel_takvim(benim)", SIG["asia1"]), ("NY_satir(analist_tarzi)", compNY)):
    st = stats_block(x, y3, 3); out[f"C5_{nm}"] = {k: round(st[k], 3) for k in ("ic", "t", "t_is", "t_oos", "t_22", "yrs_same", "yrs", "n")}
out["C5_iki_insa_korelasyonu"] = float(pd.concat([SIG["asia1"], compNY], axis=1).dropna().corr().iloc[0, 1])
# analistin s7 sinyaliyle (yalniz karsilastirma icin okunur) korelasyon
try:
    A7 = pd.read_pickle(f"{S}/out/e2_etf_leadlag/s7_signals.pkl")[1]
    out["C5_benim_NYsatir_vs_analist_korr"] = float(pd.concat([compNY, A7], axis=1).dropna().corr().iloc[0, 1])
    out["C5_benim_yerel_vs_analist_korr"] = float(pd.concat([SIG["asia1"], A7], axis=1).dropna().corr().iloc[0, 1])
except Exception as e:
    out["C5_analist_okuma_hata"] = str(e)
# (ii) FDR
reg = pd.read_csv(f"{S}/out/registry/e2_etf_leadlag.csv")
p = reg["p"].fillna(1).values; n = len(p); o = np.argsort(p)
q = np.empty(n); q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]; reg["q_rep"] = np.clip(q, 0, 1)
pick = reg[reg.test_id.str.startswith("s6_") & reg.test_id.str.contains("secilen")][["test_id", "t", "p", "q_rep"]]
out["registry_n"] = int(n); out["q_lt_005"] = int((reg.q_rep < 0.05).sum()); out["q_lt_010"] = int((reg.q_rep < 0.10).sum())
out["secilen_q"] = {r.test_id: round(r.q_rep, 4) for r in pick.itertuples()}
# p'yi kendi t'mden yeniden: iki yonlu normal
from scipy.stats import norm
# (iii) korelasyonlar
K = pd.concat({"C1": SIG[("GDXres", 10, 60)], "C2": SIG[("GDXres", 3, 60)], "C2j": SIG[("GDXJres", 1, 60)], "C5": SIG["asia1"], "C4": -SIG["PL_d5"], "C3": -SIG["gi"]}, axis=1)
out["sinyal_spearman_korr"] = K.rank().corr().round(3).to_dict()
# (iv) OOS Sharpe t
Tt = pd.read_csv(f"{OUT}/r3_strateji.csv")
oo = Tt[(Tt["mode"] == "B") & (Tt.cost == "base") & (Tt.period == "oos")].set_index("id")
yrs_oos = (cal > IS_END).sum() / 252
out["oos_sharpe_t"] = {i: {k: round(oo.loc[i, k] * np.sqrt(yrs_oos), 2) for k in ("ideal", "ideal_dm", "long", "long_dm", "long_inv")} for i in oo.index}
# (v) B&H ilk gun
bhx = {}
for und in ("GLD", "GDX", "GDXJ"):
    for a in ("2018-01-01", "2022-01-01"):
        r = R[und][R[und].index >= a].dropna()
        bhx[f"{und}_{a[:4]}+"] = dict(ilk_gun_dahil=round(sharpe(r), 3), ilk_gun_haric=round(sharpe(r.iloc[1:]), 3), ilk_gun_getiri=round(float(r.iloc[0]), 4))
out["bh_ilk_gun"] = bhx
# C2j uzun-yalniz ile C2 / C1 gunluk pnl korelasyonu (ayni fenomen mi?)
json.dump(out, open(f"{OUT}/r4_ek.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
