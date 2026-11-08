"""Denetim S1/S2: bağımsız yeniden üretim + sağlamlık.
python3 -I kod/denetim_sektor_tematik/d1_s1_s2.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
rng = np.random.default_rng(20261107)
RES = {}

smh = D("SMH"); soxl = D("SOXL"); soxx = D("SOXX"); qqq = D("QQQ")
ib = my_ibs(smh)
# 0) IBS düzeltilmiş fiyatla ham fiyattan aynı mı?
r = raw("SMH"); ib_raw = ((r["c"] - r["l"]) / (r["h"] - r["l"]).where(lambda x: x > 0)).clip(0, 1).reindex(smh.index)
dif = (ib - ib_raw).abs()
print("IBS düzeltilmiş vs ham: max fark", round(float(dif.max()), 6), " sinyal uyuşmazlığı", int(((ib < .2) != (ib_raw < .2)).sum()))
# lib.ibs ile karşılaştır (yalnız kontrol amaçlı)
print("lib.ibs ile max fark", float((lib.ibs(smh) - ib).abs().max()))
sig = ib < 0.20

c_smh = cost("SMH"); c_soxl = cost("SOXL")
print(f"maliyet SMH {c_smh:.2f} bp, SOXL {c_soxl:.2f} bp (2.500 $)")

# 1) Ana yeniden üretim
tr1 = sim(smh, sig, 1, "C0", c_smh); s1 = st(tr1, "S1 SMH C0 h1")
tr2 = sim(soxl, sig.reindex(soxl.index), 1, "C0", c_soxl); s2 = st(tr2, "S2 SOXL C0 h1")
print(pd.DataFrame([s1, s2]).round(3).T.to_string())
# ajanın işlem listesiyle birebir karşılaştır
ag = pd.read_csv(os.path.join(ROOT, "sonuclar/aile_sektor_tematik/aday_sektor_tematik_S1_islemler.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
m = tr1.merge(ag, on="sig_date", suffixes=("", "_ag"), how="outer", indicator=True)
print("ajan listesiyle eşleşme:", m["_merge"].value_counts().to_dict(), " brüt max fark",
      float((m["gross"] - m["gross_ag"]).abs().max()))
RES["S1_ana"] = s1; RES["S2_ana"] = s2

# 2) Pratik 'tut' kuralı (ardışık sinyalde satma)
th = sim_hold(smh, sig, c_smh); sh = st(th, "S1 tut-kurali")
sh["ort_gun"] = float(th["days"].mean()); sh["net_per_gun_bp"] = th["net"].sum() / th["days"].sum() * 1e4
print("\nTUT kuralı (pozisyon başına bir maliyet):"); print(pd.Series({k:(round(v,3) if isinstance(v,(int,float)) else v) for k,v in sh.items()}).to_string())
RES["S1_tut"] = sh

# 3) Maliyet duyarlılığı ve mod
rows = []
for pos in (1000, 2500, 10000):
    for sym, df in (("SMH", smh), ("SOXL", soxl)):
        rows.append({"sym": sym, "poz": pos, **st(sim(df, sig.reindex(df.index), 1, "C0", cost(sym, pos)))})
cm = pd.DataFrame(rows)[["sym", "poz", "n", "net_bp", "t", "is_net_bp", "oos_net_bp", "yil_poz"]]
print("\nMALİYET:"); print(cm.round(2).to_string()); RES["maliyet"] = cm.round(2).to_dict("records")
rows = []
for sym, df in (("SMH", smh), ("SOXL", soxl)):
    for mo in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            t_ = sim(df, sig.reindex(df.index), h, mo, cost(sym)); s_ = st(t_)
            # koşulsuz aynı yapı
            c = df["c"]; o = df["o"]
            u = (c.shift(-h) / c - 1) if mo == "C0" else (c.shift(-h) / o.shift(-1) - 1) if mo == "O1" else (c.shift(-1 - h) / c.shift(-1) - 1)
            u = u[u.index >= t_["sig_date"].min()].dropna()
            rows.append({"sym": sym, "mod": mo, "h": h, "n": s_["n"], "brut": s_["brut_bp"], "kosulsuz": u.mean() * 1e4,
                         "kenar": s_["brut_bp"] - u.mean() * 1e4, "net": s_["net_bp"], "t": s_["t"], "is": s_["is_net_bp"],
                         "oos": s_["oos_net_bp"], "is_t": s_["is_t"], "oos_t": s_["oos_t"], "yil_poz": s_["yil_poz"]})
mm = pd.DataFrame(rows); print("\nMOD/TUTUŞ:"); print(mm.round(2).to_string()); RES["modlar"] = mm.round(2).to_dict("records")

# 4) Komşu eşik plato
rows = []
for thr in (0.10, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, 0.275, 0.30):
    for mo in ("C0", "O1"):
        s_ = st(sim(smh, ib < thr, 1, mo, c_smh))
        rows.append({"esik": thr, "mod": mo, "n": s_["n"], "net": s_["net_bp"], "t": s_["t"], "is": s_["is_net_bp"], "oos": s_["oos_net_bp"]})
nb = pd.DataFrame(rows); print("\nEŞİK KOMŞULUĞU:"); print(nb.round(2).to_string()); RES["esik"] = nb.round(2).to_dict("records")

# 5) Yıl yıl ve dışlamalar
d = tr1["sig_date"].dt.year
yy = tr1.groupby(d).agg(n=("net", "size"), net_bp=("net", lambda x: x.mean() * 1e4), t=("net", lambda x: tt(x)))
print("\nYIL YIL:"); print(yy.round(2).to_string())
rows = []
for nm, msk in (("tum", d > 0), ("2020 hariç", d != 2020), ("2022 hariç", d != 2022), ("2020+2022 hariç", ~d.isin([2020, 2022])),
                ("2020+2026 hariç", ~d.isin([2020, 2026])), ("2017-2019", d.isin([2017, 2018, 2019])), ("2023-2026", d >= 2023)):
    for lbl, tx in (("S1", tr1), ("S2", tr2)):
        dd = tx["sig_date"].dt.year
        mk = msk.values if lbl == "S1" else (dd > 0).values & (msk.values)
        s_ = st(tx[mk]); rows.append({"kume": nm, "str": lbl, "n": s_["n"], "net": s_["net_bp"], "t": s_["t"]})
ex = pd.DataFrame(rows); print("\nDIŞLAMALAR:"); print(ex.round(2).to_string()); RES["dislama"] = ex.round(2).to_dict("records")

# 6) En iyi 5 / en kötü 5 + veri kontrolü (SMH-SOXX kalıntısı: bozuk kapanış testi)
rs = smh["c"].pct_change(); rx = soxx["c"].pct_change(); rq = qqq["c"].pct_change()
vk = pd.read_csv(os.path.join(ROOT, "sonuclar/veri_kalitesi.csv"))
vd = pd.read_csv(os.path.join(ROOT, "sonuclar/veri_duzeltmeleri.csv"))
for lbl, tx in (("S1", tr1), ("S2", tr2)):
    best = tx.nlargest(5, "net").copy()
    best["net_bp"] = best["net"] * 1e4
    best["SMH_t"] = rs.reindex(best.sig_date).values * 1e4; best["SOXX_t"] = rx.reindex(best.sig_date).values * 1e4
    best["SMH_t1"] = rs.reindex(best.exit_date).values * 1e4; best["SOXX_t1"] = rx.reindex(best.exit_date).values * 1e4
    best["QQQ_t1"] = rq.reindex(best.exit_date).values * 1e4
    best["IBS_SMH"] = ib.reindex(best.sig_date).values; best["IBS_SOXX"] = my_ibs(soxx).reindex(best.sig_date).values
    best["veri_kalitesi"] = [bool(((vk.sym.isin(["SMH", "SOXL", "SOXX"])) & (vk.date.isin([str(a.date()), str(b.date())]))).any())
                             for a, b in zip(best.sig_date, best.exit_date)]
    print(f"\n{lbl} EN İYİ 5:"); print(best[["sig_date", "exit_date", "net_bp", "IBS_SMH", "IBS_SOXX", "SMH_t", "SOXX_t", "SMH_t1", "SOXX_t1", "QQQ_t1", "veri_kalitesi"]].round(1).to_string())
    k = st(tx.drop(best.index)); print(f"{lbl} en iyi 5 hariç: n={k['n']} net={k['net_bp']:.1f} t={k['t']:.2f} IS={k['is_net_bp']:.1f} OOS={k['oos_net_bp']:.1f}")
    RES[lbl + "_eniyi5"] = best[["sig_date", "exit_date", "net_bp"]].astype(str).to_dict("records")
    RES[lbl + "_eniyi5_haric"] = {kk: k[kk] for kk in ("n", "net_bp", "t", "is_net_bp", "oos_net_bp")}
    k10 = st(tx.drop(tx.nlargest(10, "net").index)); RES[lbl + "_eniyi10_haric"] = {kk: k10[kk] for kk in ("n", "net_bp", "t")}
    print(f"{lbl} en iyi 10 hariç: net={k10['net_bp']:.1f} t={k10['t']:.2f}")
# bozuk kapanış testi: sinyal günü SMH-SOXX ayrışması ertesi gün tersine dönüyor mu?
res_t = (rs - rx).reindex(tr1.sig_date).values; res_t1 = (rs - rx).reindex(tr1.exit_date).values
print("\nSinyal günleri SMH-SOXX kalıntısı: t günü ort", round(np.nanmean(res_t) * 1e4, 1), "bp; t+1 ort", round(np.nanmean(res_t1) * 1e4, 1),
      "bp; |t kalıntı|>2% sayısı", int((np.abs(res_t) > 0.02).sum()))
both = sig & (my_ibs(soxx) < 0.2)
s_b = st(sim(smh, both, 1, "C0", c_smh)); s_o = st(sim(smh, sig & ~(my_ibs(soxx) < 0.2), 1, "C0", c_smh))
print(f"SMH&SOXX ikisi de IBS<0.2: n={s_b['n']} net={s_b['net_bp']:.1f} t={s_b['t']:.2f} | yalnız SMH: n={s_o['n']} net={s_o['net_bp']:.1f}")
RES["veri_capraz"] = {"ikisi": {k: s_b[k] for k in ("n", "net_bp", "t")}, "yalniz_smh": {k: s_o[k] for k in ("n", "net_bp", "t")}}

# 7) Permütasyon testleri (S1, C0 h1, brüt ortalama)
fwd = (smh["c"].shift(-1) / smh["c"] - 1)
start = tr1["sig_date"].min()
elig = fwd[(fwd.index >= start)].dropna()
obs = tr1["gross"].mean(); n = len(tr1); R = 10000
vals = elig.values
perm = np.array([rng.choice(vals, n, replace=False).mean() for _ in range(R)])
p_plain = (np.sum(perm >= obs) + 1) / (R + 1)
# yıl tabakalı
yrs = elig.index.year; cnt = tr1["sig_date"].dt.year.value_counts()
groups = {y: elig.values[yrs == y] for y in cnt.index}
perm_y = np.array([np.concatenate([rng.choice(groups[y], cnt[y], replace=False) for y in cnt.index]).mean() for _ in range(R)])
p_year = (np.sum(perm_y >= obs) + 1) / (R + 1)
# oynaklık rejimi tabakalı (20g oynaklık beşlikleri, t'ye kadar bilgi)
vol20 = np.log(smh["c"]).diff().rolling(20).std()
q = pd.qcut(vol20.reindex(elig.index), 5, labels=False)
qs = q.reindex(tr1["sig_date"]).values; cntq = pd.Series(qs).value_counts()
gq = {k: elig.values[(q == k).values] for k in cntq.index}
perm_v = np.array([np.concatenate([rng.choice(gq[k], cntq[k], replace=False) for k in cntq.index]).mean() for _ in range(R)])
p_vol = (np.sum(perm_v >= obs) + 1) / (R + 1)
# 1 günlük getiri beşlikleri tabakalı (IBS, basit 1g dönüşten fazlası mı?)
r1 = smh["c"].pct_change()
qr = pd.qcut(r1.reindex(elig.index), 10, labels=False)
qrs = qr.reindex(tr1["sig_date"]).values; cntr = pd.Series(qrs).value_counts()
gr = {k: elig.values[(qr == k).values] for k in cntr.index}
perm_r = np.array([np.concatenate([rng.choice(gr[k], min(cntr[k], len(gr[k])), replace=False) for k in cntr.index]).mean() for _ in range(R)])
p_r1 = (np.sum(perm_r >= obs) + 1) / (R + 1)
pr = {"gozlenen_brut_bp": obs * 1e4, "rastgele_ort_bp": perm.mean() * 1e4, "p_duz": p_plain, "p_yil_tabakali": p_year,
      "p_oynaklik_tabakali": p_vol, "rastgele_vol_ort_bp": perm_v.mean() * 1e4, "p_1g_getiri_desil_tabakali": p_r1,
      "rastgele_r1_ort_bp": perm_r.mean() * 1e4, "R": R}
print("\nPERMÜTASYON (S1 brüt):"); print(pd.Series({k:round(v,5) for k,v in pr.items()}).to_string()); RES["permutasyon"] = pr

# 8) Regresyon: r(t+1) ~ IBS düşük + 1g getiri z + QQQ IBS düşük (NW)
z1 = lib.zret(smh["c"], 1, 60)
y = fwd * 1e4
X = pd.DataFrame({"c": 1.0, "ibs_lt02": sig.astype(float), "z1": z1, "dn": (r1 < 0).astype(float)}).reindex(y.index)
b, t_, nn = nw_t(y.values, X.values)
print("\nREGRESYON r(t+1)[bp] ~ sabit + IBS<0.2 + z1 + düşüş günü:", dict(zip(X.columns, np.round(b, 2))), "t:", dict(zip(X.columns, np.round(t_, 2))), "n", nn)
RES["regresyon_ibs_z1"] = {"b": dict(zip(X.columns, np.round(b, 2).tolist())), "t": dict(zip(X.columns, np.round(t_, 2).tolist()))}
iq = my_ibs(qqq).reindex(smh.index)
X2 = pd.DataFrame({"c": 1.0, "smh_ibs_lt02": sig.astype(float), "qqq_ibs_lt02": (iq < 0.2).astype(float)}).reindex(y.index)
b2, t2, _ = nw_t(y.values, X2.values)
print("REGRESYON SMH IBS vs QQQ IBS:", dict(zip(X2.columns, np.round(b2, 2))), "t:", dict(zip(X2.columns, np.round(t2, 2))))
RES["regresyon_smh_qqq"] = {"b": dict(zip(X2.columns, np.round(b2, 2).tolist())), "t": dict(zip(X2.columns, np.round(t2, 2).tolist()))}
# QQQ sinyaliyle SMH ve QQQ
for nm, sg, df, sym in (("QQQ IBS<0.2 -> SMH", iq < 0.2, smh, "SMH"), ("QQQ IBS<0.2 -> QQQ", my_ibs(qqq) < 0.2, qqq, "QQQ"),
                        ("SMH<0.2 & QQQ<0.2 -> SMH", sig & (iq < 0.2), smh, "SMH"), ("SMH<0.2 & QQQ>=0.2 -> SMH", sig & (iq >= 0.2), smh, "SMH")):
    s_ = st(sim(df, sg, 1, "C0", cost(sym))); print(f"  {nm:28s} n={s_['n']} net={s_['net_bp']:.1f} t={s_['t']:.2f} IS={s_['is_net_bp']:.1f} OOS={s_['oos_net_bp']:.1f}")
    RES["ayristirma_" + nm] = {k: s_[k] for k in ("n", "net_bp", "t", "is_net_bp", "oos_net_bp")}

# 9) Aynı kural ailede (kendi IBS'i) — ajanın 39 ETF listesi
fam = ["XLK", "SMH", "IGV", "CIBR", "XLF", "KRE", "KIE", "XLE", "XOP", "OIH", "XLV", "XBI", "ARKG", "XLI", "ITA", "IYT", "JETS", "XLY",
       "XRT", "XLP", "XLU", "XLB", "XME", "COPX", "REMX", "VNQ", "ITB", "XLC", "TAN", "URA", "ARKK", "BOTZ", "QTUM", "KWEB", "BLOK",
       "UFO", "MOO", "SOXX", "QQQ"]
rows = []
for s in fam:
    df = D(s); s_ = st(sim(df, my_ibs(df) < 0.2, 1, "C0", cost(s)))
    rows.append({"etf": s, "n": s_["n"], "net": s_["net_bp"], "t": s_["t"], "is": s_["is_net_bp"], "oos": s_["oos_net_bp"],
                 "p": p_from_t(s_["t"], s_["n"])})
fa = pd.DataFrame(rows).sort_values("t", ascending=False)
fa["bonf_39"] = fa["p"] < 0.05 / len(fa)
print("\nAİLEDE AYNI KURAL:"); print(fa.round(2).to_string())
RES["aile"] = fa.round(3).to_dict("records")

# 10) 1.000 $ ve O1 kombinasyonu (en kötü pratik senaryo)
for pos in (1000, 2500):
    s_ = st(sim(smh, sig, 1, "O1", cost("SMH", pos))); print(f"O1 h1 {pos}$: net={s_['net_bp']:.1f} t={s_['t']:.2f} IS={s_['is_net_bp']:.1f} OOS={s_['oos_net_bp']:.1f}")
    RES[f"O1_{pos}"] = {k: s_[k] for k in ("n", "net_bp", "t", "is_net_bp", "oos_net_bp")}

# 11) S2 risk eşdeğeri: SOXL'ü SMH tutarının 1/3'üyle
s3 = st(sim(soxl, sig.reindex(soxl.index), 1, "C0", cost("SOXL", 833.33)))
print(f"S2 833$ SOXL: net {s3['net_bp']:.1f} bp -> {s3['net_bp']*833.33/1e4:.2f} $/işlem ; S1 2500$: {s1['net_bp']*2500/1e4:.2f} $/işlem")
# SOXL'ün 3xSOXX'ten sapması sinyal günlerinde
rl = soxl["c"].pct_change(); dev = (rl - 3 * rx).reindex(tr2.exit_date)
print("SOXL - 3xSOXX (çıkış günü) sinyal işlemlerinde ort bp:", round(float(dev.mean() * 1e4), 1))
RES["S2_833"] = {"net_bp": s3["net_bp"], "usd_islem": s3["net_bp"] * 833.33 / 1e4, "S1_usd_islem": s1["net_bp"] * 0.25}

tr1.to_csv(os.path.join(OUT, "d_S1_islemler.csv"), index=False); tr2.to_csv(os.path.join(OUT, "d_S2_islemler.csv"), index=False)
json.dump(RES, open(os.path.join(OUT, "d1_sonuc.json"), "w"), ensure_ascii=False, indent=1, default=str)
print("yazıldı", OUT)
