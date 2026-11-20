"""D1 adim 3: dogrulama. Kullanim: python3 -I 03_dogrula.py <RAW_DIR> <PANEL_FULL> <PANEL_DEV> [DEV_CUT=2025-06-30]
Cikti: stdout + <PANEL_FULL>/dogrulama_d1.txt, <PANEL_FULL>/yahoo_isy_fark.csv"""
import os, sys, json, io
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1lib import load_isy_stock, load_yahoo, load_isy_index, tick_size
from universe import STOCKS, XELKT_MEMBERS, IDX_ISY, IDX_YAHOO
RAW, PF, PD_ = sys.argv[1:4]
DEV_CUT = pd.Timestamp(dict(a.split("=") for a in sys.argv[4:] if "=" in a).get("DEV_CUT", "2025-06-30"))
pd.set_option("display.width", 220); pd.set_option("display.max_rows", 300)
buf = io.StringIO()
def P(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
L = lambda n, d=PF: pd.read_parquet(os.path.join(d, n + ".parquet"))
px = L("px"); rcc = L("ret_cc"); rco = L("ret_co"); roc = L("ret_oc"); craw = L("close_raw"); vol = L("vol_tl")
lu, ld, lut, ldt = L("lim_up"), L("lim_dn"), L("lim_up_touch"), L("lim_dn_touch")
ca, dv, ipo, trd, zv = L("ca_day"), L("div_day"), L("ipo_n"), L("tradable"), L("zero_vol")
idx, idr, ido = L("idx"), L("idx_ret"), L("idx_open")
cal = rcc.index; syms = list(rcc.columns)
m = pd.Series(np.where(cal >= pd.Timestamp("2020-03-13"), 0.10, 0.20), index=cal)

P("== (0) butunluk ==")
P("gun", len(cal), cal[0].date(), cal[-1].date(), "hisse", len(syms), "px", len(px), "tekrar satir", int(px.duplicated(["date", "sym"]).sum()))
bad = px[(px.h_raw < px.c_raw - 1e-9) | (px.l_raw > px.c_raw + 1e-9) | (px.l_raw <= 0) | (px.c_raw <= 0)]
P("h<c ya da l>c ya da <=0 satir:", len(bad), "| c NaN:", int(px.c.isna().sum()), "| acilis NaN:", int(px.o.isna().sum()), f"({px.o.isna().mean():.2%})")
g = px.assign(y=px.date.dt.year).groupby("y").agg(n=("c", "size"), acilis_dolu=("o", lambda x: x.notna().mean()))
P("acilis dolu orani (yil):", g.acilis_dolu.round(3).to_dict())
ident = ((1 + rco) * (1 + roc) - (1 + rcc)).abs().max().max(); P("max |(1+co)(1+oc)-(1+cc)|:", f"{ident:.2e}")
P("Yahoo'dan yamalanan Is Yatirim deligi (hisse-gun):", int((px.kaynak == "yahoo_yama").sum()), "| tarihler:", px[px.kaynak == "yahoo_yama"].groupby(px.date.dt.strftime("%Y-%m-%d")).size().to_dict())
po = px[(px.date >= "2021-01-01") & px.o_raw.notna() & (px.adjf.round(6) == 1)]; tko = tick_size(po.o_raw.values, po.date.values)
P("acilis saglamasi (son duzeltmeden sonraki gunler, n=%d): fiyat adimina oturan acilis orani:" % len(po), round(float((np.abs(po.o_raw.values / tko - np.round(po.o_raw.values / tko)) < 1e-4).mean()), 4),
  "| acilis = onceki kapanis orani:", round(float((rco.stack() == 0).mean()), 4), "| medyan |ret_co| (2018+ yillik):", rco.abs().stack().groupby(lambda i: i[0].year).median().loc[2018:].round(4).to_dict())
P("askidaki gunler (listeli, satir yok):", int((ipo.gt(0) & craw.isna()).sum().sum()), "| sifir hacim (satir var):", int((px.vol_tl <= 0).sum()))
P("endeks eksik gun:", idx.isna().sum().to_dict(), "| idx_open dolu:", ido.notna().mean().round(4).to_dict())
P("endeks sifir getirili gun:", (idr == 0).sum().to_dict())
for c in IDX_YAHOO:
    y = load_yahoo(RAW, c)[0].c.reindex(cal); d = (y / y.shift(1) - 1 - idr[c]).dropna()
    P(f"  ISY-Yahoo endeks getiri farki {c}: n={len(d)} |fark|>0.2%: {(d.abs() > 0.002).sum()} corr={np.corrcoef(d + idr[c].reindex(d.index), idr[c].reindex(d.index))[0, 1]:.5f}")
# fiyat adimi tablosu kontrolu (2021+)
p = px[(px.date >= "2021-01-01") & (px.kaynak != "yahoo_yama")]; tk = tick_size(p.c_raw.values, p.date.values); r = np.abs(p.c_raw.values / tk - np.round(p.c_raw.values / tk))
P("fiyat adimi tablosuna uyan ham kapanis orani (2021+):", f"{(r < 1e-6).mean():.4f}", "| dilimlere gore:", pd.Series(r < 1e-6).groupby(tk).mean().round(4).to_dict())

P("\n== (a) Yahoo - Is Yatirim gunluk getiri farki (2010+) ==")
rows = []
for s in syms:
    y, sp, dvy, _ = load_yahoo(RAW, s); a = load_isy_stock(RAW, s)
    ry = (y.adj / y.adj.shift(1) - 1); j = pd.DataFrame({"ri": rcc[s], "ry": ry.reindex(cal)})
    j["yv"] = y.v.reindex(cal); j["yc"] = y.c.reindex(cal); j["cr"] = craw[s]
    q = j.cr / j.yc; S = q.rolling(41, center=True, min_periods=5).median()
    j["yc_raw"] = j.yc * S
    hh = a.h_raw.reindex(cal); ll = a.l_raw.reindex(cal)
    j["y_disinda"] = (j.yc_raw > hh * 1.004) | (j.yc_raw < ll * 0.996)         # Yahoo kapanisi Is Yatirim gun araliginin disinda
    j["y_esit"] = (j.yc_raw / j.cr - 1).abs() < 0.0035                          # iki kaynagin kapanisi ayni
    ydates = y.index; j["y_onceki_yok"] = ~pd.Series(cal, index=cal).shift(1).isin(ydates)
    j["y_fazla_gun"] = pd.Series([len(ydates[(ydates > a_) & (ydates < b_)]) > 0 for a_, b_ in zip(cal[:-1], cal[1:])] and
                                 [False] + [len(ydates[(ydates > a_) & (ydates < b_)]) > 0 for a_, b_ in zip(cal[:-1], cal[1:])], index=cal)
    j["ca"] = (ca[s] | dv[s]); j["ca"] = j.ca | j.ca.shift(1, fill_value=False) | j.index.isin(sp.index) | j.index.isin(dvy.index)
    j = j.dropna(subset=["ri", "ry"]); j["d"] = j.ri - j.ry; j["sym"] = s
    b = j[j.d.abs() > 0.01].copy(); b["n_ortak"] = len(j)
    rows.append(b)
B = pd.concat(rows); B.index.name = "date"; B = B.reset_index()
cnt_day = B.groupby("date").sym.count(); nlist = ipo.gt(0).sum(axis=1)
B["piyasa_geneli"] = B.date.map((cnt_day / nlist.reindex(cnt_day.index) >= 0.3) & (cnt_day >= 3))
prev_out = B.set_index(["sym", "date"]).y_disinda
def cat(r):
    if r.ca: return "1_kurumsal_islem_gunu"
    if r.yv == 0 or r.y_fazla_gun or r.y_onceki_yok: return "2_yahoo_bayat/tatil_satiri"
    if r.piyasa_geneli: return "3_yahoo_piyasa_geneli_hatali_gun"
    if r.y_disinda: return "4_yahoo_kapanisi_gun_araligi_disinda"
    if r.y_esit: return "5_bugun_ayni_dunku_yahoo_kapanisi_farkli"
    return "6_yahoo_kapanisi_aralik_icinde_ama_farkli"
B["kategori"] = B.apply(cat, axis=1)
B.to_csv(os.path.join(PF, "yahoo_isy_fark.csv"), index=False)
ntot = sum(b.n_ortak.iloc[0] if len(b) else 0 for b in rows)
P("ortak hisse-gun (yaklasik):", int(rcc.notna().sum().sum()), "| |fark|>%1:", len(B), "| 2020+:", int((B.date >= "2020-01-01").sum()), "| 2023+:", int((B.date >= "2023-01-01").sum()))
P(B.groupby("kategori").agg(n=("d", "size"), n_2020=("date", lambda x: (x >= "2020-01-01").sum()), medyan_abs=("d", lambda x: x.abs().median()), maks_abs=("d", lambda x: x.abs().max())).round(4).to_string())
P("yila gore:", B.groupby(B.date.dt.year).size().to_dict())
P("piyasa geneli Yahoo hatali gunler:", sorted(set(B[B.piyasa_geneli].date.dt.strftime("%Y-%m-%d"))))
P("kurumsal islem gunu farklari (hangi kaynak marj icinde?):")
C = B[B.kategori.str.startswith("1")].copy(); C["marj"] = C.date.map(m)
P(C[["date", "sym", "ri", "ry", "d", "marj"]].assign(date=lambda x: x.date.dt.strftime("%Y-%m-%d"), isy_marj_ici=lambda x: x.ri.abs() <= x.marj + 0.006, yahoo_marj_ici=lambda x: x.ry.abs() <= x.marj + 0.006).round(4).to_string(index=False))
# hakem: XELKT. Ihtilafli gunlerde uye sepetini iki kaynakla kur, XELKT getirisine hangisi yakin?
mem = [s for s in XELKT_MEMBERS if s in syms]
mc = px.pivot(index="date", columns="sym", values="mcap_tl").reindex(cal)[mem].shift(1)
alt = rcc[mem].copy()
for _, r in B[B.sym.isin(mem) & ~B.kategori.str.startswith("1")].iterrows(): alt.loc[r.date, r.sym] = r.ry
def bask(R):
    w = mc.where(R.notna()); return (R * w).sum(axis=1) / w.sum(axis=1)
bx = idr["XELKT"]; b_isy = bask(rcc[mem])
def arb(lab, sel):
    Bs = B[sel & B.sym.isin(mem) & ~B.kategori.str.startswith("1")]
    if len(Bs) == 0: return
    alt = rcc[mem].copy()
    for r in Bs.itertuples(): alt.loc[r.date, r.sym] = r.ry
    dd = sorted(set(Bs.date)); t = pd.DataFrame({"x": bx.reindex(dd), "i": b_isy.reindex(dd), "y": bask(alt).reindex(dd)}).dropna()
    P(f"  hakem XELKT [{lab}] ihtilaf={len(Bs)} gun={len(t)}: PD agirlikli uye sepeti - XELKT RMSE  Is Yatirim={np.sqrt(((t.i - t.x) ** 2).mean()):.5f}  Yahoo ikameli={np.sqrt(((t.y - t.x) ** 2).mean()):.5f}"
          f" | corr Is Yatirim={t.i.corr(t.x):.4f} Yahoo={t.y.corr(t.x):.4f}")
arb("tum", B.date >= "2010"); arb("2010-2017", B.date < "2018"); arb("2018-2020", (B.date >= "2018") & (B.date < "2021")); arb("2021+", B.date >= "2021")
for k in sorted(B.kategori.unique())[1:]: arb(k, B.kategori == k)

P("\n== (b) |getiri| > marj kalan gunler ==")
big = rcc.abs().gt((m + 0.006).values.reshape(-1, 1) if False else pd.DataFrame(np.repeat((m.values + 0.006)[:, None], len(syms), 1), index=cal, columns=syms))
st = big.stack(); st = st[st]
R = pd.DataFrame({"r": rcc.stack().reindex(st.index), "ca": ca.stack().reindex(st.index), "div": dv.stack().reindex(st.index), "ipo_n": ipo.stack().reindex(st.index)}).reset_index()
R.columns = ["date", "sym", "r", "ca", "div", "ipo_n"]
P("toplam:", len(R), "| sermaye islemi gunu:", int(R.ca.sum()), "| temettu gunu:", int(R["div"].sum()), "| diger:", int((~R.ca & ~R["div"]).sum()))
P(R.assign(date=R.date.dt.strftime("%Y-%m-%d")).round(4).to_string(index=False))

P("\n== (c) esit agirlikli elektrik sepeti ile XELKT getirisi korelasyonu ==")
ew = rcc[mem].mean(axis=1); vw = bask(rcc[mem]); x = idr["XELKT"]
t = pd.DataFrame({"ew": ew, "vw": vw, "x": x, "n": rcc[mem].notna().sum(axis=1)}).dropna()
gy = t.groupby(t.index.year)
P(pd.DataFrame({"n_gun": gy.size(), "uye_ort": gy.n.mean().round(1), "corr_EW": gy.apply(lambda d: d.ew.corr(d.x)).round(3), "corr_PD_agirlikli": gy.apply(lambda d: d.vw.corr(d.x)).round(3),
                "izleme_hatasi_PD_gunluk": gy.apply(lambda d: (d.vw - d.x).std()).round(4)}).T.to_string())
P("tum donem corr EW:", round(t.ew.corr(t.x), 4), "PD agirlikli:", round(t.vw.corr(t.x), 4), "| 2021+ EW:", round(t.loc["2021":].ew.corr(t.loc["2021":].x), 4))

P("\n== (d) tavan/taban sayilari ==")
yy = cal.year
P(pd.DataFrame({"hisse_gun": craw.notna().groupby(yy).sum().sum(axis=1), "tavan_kap": lu.groupby(yy).sum().sum(axis=1), "taban_kap": ld.groupby(yy).sum().sum(axis=1),
                "tavan_deg": lut.groupby(yy).sum().sum(axis=1), "taban_deg": ldt.groupby(yy).sum().sum(axis=1)}).assign(tavan_oran=lambda d: (d.tavan_kap / d.hisse_gun).round(4), taban_oran=lambda d: (d.taban_kap / d.hisse_gun).round(4)).T.to_string())
ru = rcc.where(lu).stack(); rd = rcc.where(ld).stack()
P("tavan kapanis gunlerinde getiri dagilimi 2020-03-13+:", ru[ru.index.get_level_values(0) >= "2020-03-13"].describe().round(4).to_dict())
P("taban kapanis gunlerinde getiri dagilimi 2020-03-13+:", rd[rd.index.get_level_values(0) >= "2020-03-13"].describe().round(4).to_dict())
lue, lde = L("lim_up_exact"), L("lim_dn_exact"); post = cal >= "2020-03-13"
P("2020-03-13+ tavan_kap:", int(lu[post].sum().sum()), "| kapanisi hesaplanan tavan fiyatina tam esit:", int((lu & lue)[post].sum().sum()), "| taban_kap:", int(ld[post].sum().sum()), "| tam esit:", int((ld & lde)[post].sum().sum()),
  "| exact ama kural disi (tavan, taban):", int((lue & ~lu & ~ca & ~dv)[post].sum().sum()), int((lde & ~ld & ~ca & ~dv)[post].sum().sum()))
P("kacan aday: |r|>=marj-%0.6 ama bayraksiz (kapanis=uc degil) gun sayisi:", int((rcc.abs().ge(pd.DataFrame(np.repeat((m.values - 0.006)[:, None], len(syms), 1), index=cal, columns=syms)) & ~lu & ~ld & ~ca & ~dv).sum().sum()))
rng = np.random.RandomState(7)
cand = pd.concat([lu.stack()[lambda v: v].rename("up"), ld.stack()[lambda v: v].rename("dn")], axis=1)
pick = list(cand[cand.up == True].sample(3, random_state=rng).index) + list(cand[cand.dn == True].sample(2, random_state=rng).index)
P("elle kontrol (ham json satirlari; 3 tavan + 2 taban):")
for d, s in pick:
    v = json.load(open(os.path.join(RAW, "isy_hisse", s + ".json")))["value"]
    k = [i for i, r in enumerate(v) if r["HGDG_TARIH"] == d.strftime("%d-%m-%Y")][0]
    a, b_ = v[k - 1], v[k]
    yj, _, _, _ = load_yahoo(RAW, s); yr = yj.loc[d] if d in yj.index else None
    P(f"  {s} {d.date()} {'TAVAN' if lu.loc[d, s] else 'TABAN'}: onceki kap={a['HG_KAPANIS']} | kap={b_['HG_KAPANIS']} yuksek={b_['HG_MAX']} dusuk={b_['HG_MIN']} -> ham getiri={b_['HG_KAPANIS'] / a['HG_KAPANIS'] - 1:.4f}"
      f" | teorik uc={a['HG_KAPANIS'] * (1 + (1 if lu.loc[d, s] else -1) * m[d]):.4f} | Yahoo c/h/l={None if yr is None else (round(float(yr.c), 4), round(float(yr.h), 4), round(float(yr.l), 4))} | ca={bool(ca.loc[d, s] or dv.loc[d, s])}")

P("\n== (e) panel_dev ==")
ok = True
for n in ["px", "ret_cc", "ret_co", "ret_oc", "vol_tl", "close_raw", "lim_up", "lim_dn", "lim_up_touch", "lim_dn_touch", "lim_up_exact", "lim_dn_exact", "zero_vol", "ipo_n", "ca_day", "div_day", "tradable", "idx", "idx_ret", "idx_open"]:
    d_ = L(n, PD_); last = d_.date.max() if n == "px" else d_.index.max()
    if last != DEV_CUT: ok = False; P("  HATA", n, last)
    if n not in ("px",):
        f = L(n).reindex(index=d_.index, columns=d_.columns)
        if d_.dtypes.iloc[0] == float: df_ = (d_ - f).abs().max().max()
        else: df_ = int((d_ != f).sum().sum())
        if df_ > 1e-9: P(f"  {n}: full ile fark = {df_}")
dm = pd.read_csv(os.path.join(PD_, "meta.csv")); fm = pd.read_csv(os.path.join(PF, "meta.csv"))
P("dev son tarih tum dosyalarda", DEV_CUT.date(), ":", ok, "| dev gun:", len(L("ret_cc", PD_)), "| dev hisse:", L("ret_cc", PD_).shape[1], "| dev meta son_tarih max:", dm.son_tarih.max(),
  "| dev px max:", L("px", PD_).date.max().date(), "| dev'de olmayan hisseler:", sorted(set(fm.sym) - set(dm.sym)))
P("dev ca_events max tarih:", pd.read_csv(os.path.join(PD_, "ca_events.csv")).date.max())
open(os.path.join(PF, "dogrulama_d1.txt"), "w").write(buf.getvalue())
