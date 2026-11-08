"""Adım 6: a priori bileşik (C1) ayrıştırması. Soru: C1'in zamanlama Sharpe'ı kısa vadeli öngörüden mi, yoksa yavaş trend (yıl düzeyi drift'i yakalama) mı?
 - Bileşenler tek tek: pos = sign(a priori işaret × x)
 - C1 'hızlı' (momentum hariç 4 bileşen) ve 'yavaş' (yalnız r20, r250)
 - Yıl-içi demeaned Sharpe: getiriden HER YILIN kendi ortalaması çıkarılır (yalnızca atıf tanısı; yıl düzeyi trendi ayıklar)
 - Uzun örneklem: spot panel 2011–2026, genişleyen standardizasyonla (ileriye bakmasız) C1 sabit kural, hedef s_ret.
Kayıt: 'a8_c1_components'."""
from common import *
from features import build
from models import C1

clear_family(["a8_c1_components"])
Xs, XV, info, s, d = build()


def ystd_dm(ret):
    return ret - ret.groupby(ret.index.year).transform("mean")


def evalpos(pos, ret, y, h, label, reg=True, x_for_ic=None):
    out = dict(label=label, h=h)
    for pn, (a, b) in {"ALL": ("2020-01-01", "2026-12-31"), "VAL": ("2020-01-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31"), "PRE2020": ("2011-01-01", "2019-12-31")}.items():
        rr = ret.loc[a:b].dropna()
        if len(rr) < 100: continue
        p = pos.reindex(rr.index).fillna(0)
        bb = bt_block(p, rr, h); yd = backtest(p, ystd_dm(rr), h)
        out.update({f"{pn}_sh": bb["sharpe"], f"{pn}_shdm": bb["sharpe_dm"], f"{pn}_sh_yrdm": round(yd["sharpe"], 3), f"{pn}_long": bb["long_sharpe"], f"{pn}_short": bb["short_sharpe"],
                    f"{pn}_bh": bb["bh_sharpe"], f"{pn}_expo_long": round(float((p > 0).mean()), 3)})
    if reg:
        xi = x_for_ic if x_for_ic is not None else pos
        st = split_stats(xi.loc["2017-03-01":], y.loc["2017-03-01":], h)
        register(AGENT, "a8_c1_components", f"c1c_{label}_h{h}", label, h, st, note=f"VİOP; ALL zamanlama Sharpe={out.get('ALL_sh')} yıl-içi dm={out.get('ALL_sh_yrdm')}")
        out.update(ic=st["ic"], t=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], yrs=f"{st['yrs_same_sign']}/{st['yrs']}")
    return out


rows = []
for h in (1, 3, 5):
    y = d[f"fwd{h}"]; ret = d.v_ret
    for c, sg in C1.items():
        x = XV[c] * sg
        rows.append(evalpos(np.sign(x), ret, y, h, f"bilesen_{c}", x_for_ic=x))
    # walk-forward C1 skoru (preds_V1) ve yıl-içi demeaned tanısı
    P_ = pd.read_parquet(f"{OUT}/preds_V1.parquet"); P_["date"] = pd.to_datetime(P_["date"])
    sc = P_[(P_.model == "c1_apriori_score") & (P_.h == h)].set_index("date").yhat
    rows.append(evalpos(np.sign(sc), ret, y, h, "C1_walkforward_V1", reg=False))
    # genişleyen standardizasyonlu sabit C1 (VİOP günlerinde) + hızlı/yavaş alt kümeler
    def comp(cols):
        zs = []
        for c in cols:
            x = XV[c] * C1[c]; mu = x.expanding(250).mean().shift(1); sd = x.expanding(250).std().shift(1)
            zs.append(((x - mu) / sd).clip(-3, 3))
        return pd.concat(zs, axis=1).mean(axis=1)
    for nm, cols in {"C1_sabit": list(C1), "C1_hizli(momentum_haric)": [c for c in C1 if c not in ("px_r20", "px_r250")], "C1_yavas(r20+r250)": ["px_r20", "px_r250"]}.items():
        z = comp(cols)
        rows.append(evalpos(np.sign(z), ret, y, h, nm, x_for_ic=z))
    # uzun örneklem (spot panel, s_ret hedefi): 2011–2019 ve 2020+
    zs = []
    for c in C1:
        x = Xs[c] * C1[c]; mu = x.expanding(250).mean().shift(1); sd = x.expanding(250).std().shift(1)
        zs.append(((x - mu) / sd).clip(-3, 3))
    zsp = pd.concat(zs, axis=1).mean(axis=1)
    o = evalpos(np.sign(zsp), s.s_ret, s[f"sfwd{h}"], h, "C1_sabit_spot", reg=False)
    st = split_stats(zsp.loc["2011":"2019"], s[f"sfwd{h}"].loc["2011":"2019"], h)
    register(AGENT, "a8_c1_components", f"c1c_C1_sabit_spot2011_19_h{h}", "C1 sabit (spot 2011-2019)", h, dict(ic=st["ic"], t=st["t"], n=st["n"]), note=f"spot erken; Sharpe={o.get('PRE2020_sh')} yıl-içi dm={o.get('PRE2020_sh_yrdm')}")
    o.update(ic=st["ic"], t=st["t"], yrs=f"{st['yrs_same_sign']}/{st['yrs']}")
    rows.append(o)
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/c1_decomp.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 60)
cols = ["label", "h", "ic", "t", "t_is", "t_oos", "yrs", "ALL_sh", "ALL_shdm", "ALL_sh_yrdm", "ALL_long", "ALL_short", "ALL_expo_long", "VAL_sh", "OOS_sh", "OOS_shdm", "OOS_sh_yrdm", "PRE2020_sh", "PRE2020_sh_yrdm", "PRE2020_bh"]
print(R[[c for c in cols if c in R]].to_string(index=False))
