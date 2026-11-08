"""sinyal_altin.py doğrulaması (test düzeneği, rapor değil).
(1) CLI'yi --panel modunda ≥30 geçmiş günde (TR ve ABD yarım günleri, takvim olay günleri, spotun olmadığı VİOP günleri dahil) çalıştırır.
(2) Her sinyalin değerini analistin KENDİ kod yoluyla üretilen seriyle karşılaştırır:
      A1-LOWMOM  : out/a1_zaman_serisi/a1_feats.expanding_pct + to_viop, a1_final.py lowmom_cal (satır 19-27)
      A3_QEND    : out/a3_takvim_olay/a3_derin.py cal_pos + qm&(tde==1) (satır 23-24, 89-102)
      A4-C1      : out/a4_abd_capraz/a4_common.zscale + s4_adaylar.py miner_resid (satır 16-19), eşleme uc_tercile (s4_adaylar.json)
                   + analistin kaydettiği P&L serisi s4_pnl_C1_GDXJ_artik.parquet ile lib_altin.backtest eşitliği
      A8-3       : out/a8_ml_kombinasyon/features.build() 'seg_last1h', 08_univ_bt.py pos=sign(x)
      E1-C2      : out/e1_etf_zaman_takvim/c_masks.pkl 'pre_hol' + f_final.py entry()
      E2-C2j/C2/C1: out/e2_etf_leadlag/s1_signals.pkl x serileri + e2_common.pos_from_signal (yalnız uzun: clip ≥0)
      E3-1       : out/e3_etf_akis_prim/g_main_claim.py m = ln(xau_cut/xau_close.shift(1)), pos=(m<0)
      E3-3/E3-4  : out/e3_etf_akis_prim/c_cef.py rolling_beta_resid, z60 (k=60), z.shift(1)
    ve hakem serileriyle (out/sentez/sinyal_viop_ham.parquet, sinyal_etf_ham.parquet, poz_*.parquet, bugun_2026_11_09.json).
(3) Toplu kontrol: modül içinden 2022-01..2026-11 her işlem gününde yeni dilim ve etkin pozisyonu hakem serileriyle karşılaştırır.
Çıktı: dogrulama_sinyal_betigi.csv (gün × sinyal × alan), dogrulama_sinyal_toplu.csv; özet stdout.
"""
import json, os, subprocess, sys, time, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/sentez"; TMP = f"{S}/sentez_probe/test_json"; os.makedirs(TMP, exist_ok=True)
sys.path.insert(0, f"{S}/code")
import lib_altin
V = lib_altin.load_viop(); SP = lib_altin.load_spot()
E = pd.read_parquet(f"{S}/panel/panel_etf.parquet"); E.index = pd.to_datetime(E.index)
HALF_TR = pd.to_datetime(pd.read_csv(f"{S}/out/a1_zaman_serisi_rep/half_days.csv", header=None)[0].iloc[1:].values)

# ------------------------------------------------------------------ analist serileri
A = {}
sys.path.insert(0, f"{S}/out/a1_zaman_serisi"); from a1_feats import expanding_pct, to_viop
lp = np.log(SP.s_p15); r_s = lp.diff(); q_cal = expanding_pct(r_s.rolling(20).std())
low_cal = np.sign(lp - lp.shift(5)).where(q_cal < 1 / 3, 0.0).where(q_cal.notna())
A["low_pos"] = to_viop(pd.DataFrame({"x": low_cal}), V.index).x
A["low_q"] = to_viop(pd.DataFrame({"x": q_cal}), V.index).x
A["low_x5"] = to_viop(pd.DataFrame({"x": lp - lp.shift(5)}), V.index).x
def cal_pos(idx):  # a3_derin.py satır 23-24 (birebir)
    g = pd.Series(np.arange(len(idx)), index=idx).groupby([idx.year, idx.month]); tdm = g.cumcount() + 1; n = g.transform("size"); return tdm.values, (n - tdm).values
tdm, tde = cal_pos(V.index); qm = np.isin(V.index.month, [3, 6, 9, 12])
A["qend_pos"] = pd.Series((qm & (tde == 1)).astype(float), index=V.index)
sys.path.insert(0, f"{S}/out/a4_abd_capraz"); from a4_common import zscale
def miner_resid(df, m, beta_win=60):  # s4_adaylar.py satır 16-19 (birebir)
    rm = np.log(df[m]).diff(); rg = np.log(df["y_GLD"]).diff()
    b = rm.rolling(beta_win, min_periods=40).cov(rg).shift(1) / rg.rolling(beta_win, min_periods=40).var().shift(1)
    return zscale(rm - b * rg)
A["a4_z"] = miner_resid(V, "y_GDXJ"); A["a4_pos"] = np.sign(A["a4_z"]).where(A["a4_z"].abs() > 0.43, 0.0)
pnl_ref = pd.read_parquet(f"{S}/out/a4_abd_capraz/s4_pnl_C1_GDXJ_artik.parquet").pnl
pnl_my = lib_altin.backtest(A["a4_pos"], V.v_ret, 3)["pnl"]
A4_PNL_MAXDIFF = float((pnl_my.reindex(pnl_ref.index) - pnl_ref).abs().max())
sys.path.insert(0, f"{S}/out/a8_ml_kombinasyon"); from features import build
_, XV, _, _, _ = build(); A["last_x"] = XV["seg_last1h"]; A["last_pos"] = np.sign(A["last_x"])
sys.path.insert(0, f"{S}/out/e1_etf_zaman_takvim")
MK = pd.read_pickle(f"{S}/out/e1_etf_zaman_takvim/c_masks.pkl")
A["e1_pos"] = MK["pre_hol"].reindex(E.index).fillna(False).astype(float).shift(-1).fillna(0)  # f_final.py entry()
SIG1 = pd.read_pickle(f"{S}/out/e2_etf_leadlag/s1_signals.pkl")
sys.path.insert(0, f"{S}/out/e2_etf_leadlag"); from e2_common import pos_from_signal
for nm, key, q in (("c2j", ("GDXJ~GLD+SPY", 1), 0.7), ("c2", ("GDX~GLD+SPY", 3), 0.7), ("c1", ("GDX~GLD+SPY", 10), 0.8)):
    A[f"{nm}_x"] = SIG1[key]; A[f"{nm}_pos"] = pos_from_signal(SIG1[key], +1, q).clip(lower=0)
m = np.log(E.xau_cut / E.xau_close.shift(1)); A["m"] = m; A["m_pos"] = (m < 0).astype(float).where(m.notna(), 0.0)
def lr(px): return np.log(px).diff()
def rolling_beta_resid(y, X, win=250):  # c_cef.py satır 13-21 (birebir)
    dd = pd.concat([y.rename("y"), X], axis=1).dropna(); out = pd.Series(np.nan, index=dd.index)
    Y = dd.y.values; XX = np.column_stack([np.ones(len(dd)), dd.iloc[:, 1:].values])
    for i in range(win, len(dd)):
        b = np.linalg.lstsq(XX[i - win:i], Y[i - win:i], rcond=None)[0]; out.iloc[i] = Y[i] - XX[i, 1:] @ b[1:]
    return out
rG = lr(E.c_GLD); rSL = lr(E.c_SLV); rC = lr(E.c_CEF)
eC = rolling_beta_resid(rC, pd.concat([rG.rename("g"), rSL.rename("s")], axis=1))
for nm, lvl in (("phys", np.log(E.c_PHYS / E.c_GLD)), ("cef", eC.reindex(E.index).fillna(0).cumsum().where(eC.reindex(E.index).notna()))):
    dev = lvl - lvl.rolling(60, min_periods=30).median(); z = dev / dev.rolling(250, min_periods=120).std(); A[f"{nm}_z"] = z.shift(1)
# hakem serileri
VR = pd.read_parquet(f"{OUT}/sinyal_viop_ham.parquet"); VP = pd.read_parquet(f"{OUT}/poz_viop.parquet")
ER = pd.read_parquet(f"{OUT}/sinyal_etf_ham.parquet"); EP = pd.read_parquet(f"{OUT}/poz_etf.parquet")
for X in (VR, VP, ER, EP): X.index = pd.to_datetime(X.index)
print(f"analist serileri hazır; A4-C1 analist P&L ile lib_altin.backtest farkı (maks |Δ|): {A4_PNL_MAXDIFF:.2e}", flush=True)

# ------------------------------------------------------------------ test günleri
nz = lambda s: [str(d.date()) for d in s.index[s != 0]]
G = set()
G |= {"2017-08-31", "2019-10-28", "2021-07-19", "2023-04-20", "2024-04-09", "2024-10-28", "2025-06-05", "2025-10-28", "2026-03-19", "2026-05-26", "2026-10-28"}  # TR yarım
G |= {"2018-07-03", "2019-11-29", "2023-07-03", "2024-07-03", "2024-11-29", "2024-12-24", "2025-07-03", "2025-11-28", "2025-12-24"}  # ABD yarım
G |= set(nz(VR.V_QEND_h3)[-3:]) | set(nz(ER.E_GDXTATIL_h1)[-4:])
lw = nz(VR.V_LOWMOM_h1); G |= {lw[i] for i in (len(lw) // 5, 2 * len(lw) // 5, 3 * len(lw) // 5, -1)}
G |= {"2024-12-25", "2025-12-25", "2026-04-03", "2025-01-01"}  # spot yok / NYSE kapalı / TR tatili
G |= {"2017-06-15", "2018-03-21", "2019-09-10", "2020-03-16", "2020-08-07", "2021-11-23", "2022-02-24", "2022-09-28", "2023-03-13", "2023-10-09",
      "2024-05-20", "2025-01-27", "2025-04-07", "2025-09-02", "2026-01-30", "2026-02-02", "2026-08-14", "2026-11-02", "2026-11-05", "2026-11-06", "2026-11-09"}
G = sorted(G)
print(f"{len(G)} test günü", flush=True)

rows = []
PANEL_SON = "2026-11-06"
def add(gun, sid, alan, betik, ref, kaynak, tol=1e-9, not_="", nan0=False):
    if gun > PANEL_SON and "bugun" not in kaynak: return  # panel sonrası: yalnız hakemin Pazartesi tablosuyla karşılaştırılır
    b = np.nan if betik is None else float(betik)
    if nan0 and np.isnan(b): b = 0.0  # hakem kuralı: hesaplanamayan dilim = 0
    r = np.nan if ref is None or (isinstance(ref, float) and np.isnan(ref)) else float(ref)
    if np.isnan(b) and np.isnan(r): ok = True
    elif np.isnan(b) or np.isnan(r): ok = False
    else: ok = abs(b - r) <= tol * max(1.0, abs(r))
    rows.append(dict(gun=gun, sinyal=sid, alan=alan, betik=b, referans=r, kaynak=kaynak, esit=ok, not_=not_))

def ref_at(s, d):
    d = pd.Timestamp(d)
    return float(s.loc[d]) if d in s.index and pd.notna(s.loc[d]) else np.nan

t0 = time.time()
for g in G:
    fn = f"{TMP}/{g}.json"
    r = subprocess.run([sys.executable, "-W", "ignore", f"{OUT}/sinyal_altin.py", "--panel", "--tarih", g, "--json", fn, "--sessiz"], capture_output=True, text=True)
    if r.returncode != 0:
        print("HATA", g, r.stderr[-2000:]); continue
    J = json.load(open(fn))
    vd, ed = J["viop"]["tarih"], J["etf"]["tarih"]
    ihlal = [x for x in J["denetim"] if x["sonuc"] == "İHLAL"]
    rows.append(dict(gun=g, sinyal="DENETIM", alan="ihlal_sayisi", betik=len(ihlal), referans=0, kaynak="zaman damgası", esit=len(ihlal) == 0, not_=""))
    yarim_tr = pd.Timestamp(vd) in HALF_TR
    if not J["viop"].get("kapali"):
        Sg = {s["id"]: s for s in J["viop"]["sinyaller"]}
        s = Sg["A1-LOWMOM-h1"]
        if s["durum"] != "DEVRE DIŞI":
            add(vd, "A1-LOWMOM-h1", "q", s["ek"].get("q"), ref_at(A["low_q"], vd), "analist a1")
            add(vd, "A1-LOWMOM-h1", "x5", s["ek"].get("x5"), ref_at(A["low_x5"], vd), "analist a1")
            add(vd, "A1-LOWMOM-h1", "pos", s["yeni_dilim"], ref_at(A["low_pos"].fillna(0), vd), "analist a1")
        add(vd, "A1-LOWMOM-h1", "pos", s["yeni_dilim"], ref_at(VR.V_LOWMOM_h1, vd), "hakem", nan0=True)
        add(vd, "A1-LOWMOM-h1", "etkin", s["etkin"], ref_at(VP.V_LOWMOM_h1, vd), "hakem")
        if s["ek"].get("h5"): add(vd, "A1-LOWMOM-h5", "etkin", s["ek"]["h5"]["etkin"], ref_at(VP.V_LOWMOM_h5, vd), "hakem")
        s = Sg["A3_QEND_h3"]
        add(vd, "A3_QEND_h3", "pos", s["yeni_dilim"], ref_at(A["qend_pos"], vd), "analist a3")
        add(vd, "A3_QEND_h3", "pos", s["yeni_dilim"], ref_at(VR.V_QEND_h3, vd), "hakem")
        add(vd, "A3_QEND_h3", "etkin", s["etkin"], ref_at(VP.V_QEND_h3, vd), "hakem")
        s = Sg["A4-C1_GDXJ_artik_h3"]
        add(vd, "A4-C1_GDXJ_artik_h3", "z", s["ek"].get("z"), ref_at(A["a4_z"], vd), "analist a4", tol=1e-7)
        add(vd, "A4-C1_GDXJ_artik_h3", "pos", s["yeni_dilim"], ref_at(A["a4_pos"].fillna(0), vd), "analist a4")
        add(vd, "A4-C1_GDXJ_artik_h3", "pos", s["yeni_dilim"], ref_at(VR.V_GDXJRES_h3, vd), "hakem")
        add(vd, "A4-C1_GDXJ_artik_h3", "etkin", s["etkin"], ref_at(VP.V_GDXJRES_h3, vd), "hakem")
        s = Sg["A8-3_seg_last1h_h5"]
        if s["durum"] != "DEVRE DIŞI":
            add(vd, "A8-3_seg_last1h_h5", "x", s["deger"], ref_at(A["last_x"], vd), "analist a8")
            add(vd, "A8-3_seg_last1h_h5", "pos", s["yeni_dilim"], ref_at(A["last_pos"].fillna(0), vd), "analist a8")
        add(vd, "A8-3_seg_last1h_h5", "pos", s["yeni_dilim"], ref_at(VR.V_LAST1H_h5, vd), "hakem", nan0=True)
        add(vd, "A8-3_seg_last1h_h5", "etkin", s["etkin"], ref_at(VP.V_LAST1H_h5, vd), "hakem")
    if not J["etf"].get("kapali"):
        Sg = {s["id"]: s for s in J["etf"]["sinyaller"]}
        s = Sg["E1-C2_GDX_tatil_oncesi"]
        add(ed, "E1-C2_GDX_tatil_oncesi", "pos", s["yeni_dilim"], ref_at(A["e1_pos"], ed), "analist e1")
        add(ed, "E1-C2_GDX_tatil_oncesi", "pos", s["yeni_dilim"], ref_at(ER.E_GDXTATIL_h1, ed), "hakem")
        for sid, nm, hk in (("E2-C2j_GDXJ_artik_h3", "c2j", "E_C2J_h3"), ("E2-C2_GDX_artik_h3", "c2", "E_C2_h3"), ("E2-C1_madenci_oncu_GLD_h5", "c1", "E_C1_h5")):
            s = Sg[sid]
            add(ed, sid, "x", s["ek"].get("x"), ref_at(A[f"{nm}_x"], ed), "analist e2", tol=1e-7)
            add(ed, sid, "pos", s["yeni_dilim"], ref_at(A[f"{nm}_pos"], ed), "analist e2")
            add(ed, sid, "pos", s["yeni_dilim"], ref_at(ER[hk], ed), "hakem")
            add(ed, sid, "etkin", s["etkin"], ref_at(EP[hk], ed), "hakem")
            if nm == "c1": add(ed, sid, "kaplama", s["ek"].get("kaplama_poz"), ref_at(ER.E_C1kap_h5, ed), "hakem")
        s = Sg["E3-1_altin_gunici_GDXJ_donus"]
        if s["durum"] != "DEVRE DIŞI":
            add(ed, "E3-1_altin_gunici_GDXJ_donus", "m", s["ek"].get("m"), ref_at(A["m"], ed), "analist e3")
            add(ed, "E3-1_altin_gunici_GDXJ_donus", "pos", s["yeni_dilim"], ref_at(A["m_pos"], ed), "analist e3")
        add(ed, "E3-1_altin_gunici_GDXJ_donus", "pos", s["yeni_dilim"] if s["durum"] != "DEVRE DIŞI" else 0.0, ref_at(ER.E_M_GDXJ_h1, ed), "hakem", nan0=True)
        add(ed, "E3-3_PHYS_GLD_iskonto", "z", Sg["E3-3_PHYS_GLD_iskonto"]["ek"].get("z"), ref_at(A["phys_z"], ed), "analist e3", tol=1e-7)
        add(ed, "E3-4_CEF_artik", "z", Sg["E3-4_CEF_artik"]["ek"].get("z"), ref_at(A["cef_z"], ed), "analist e3", tol=1e-7)
print(f"CLI {len(G)} gün, {time.time() - t0:.0f} sn", flush=True)

# 2026-11-09: hakemin Pazartesi tablosu
B = json.load(open(f"{OUT}/bugun_2026_11_09.json"))["bugun"]
J = json.load(open(f"{TMP}/2026-11-09.json"))
Sv = {s["id"]: s for s in J["viop"]["sinyaller"]}; Se = {s["id"]: s for s in J["etf"]["sinyaller"]}
add("2026-11-09", "A4-C1_GDXJ_artik_h3", "z", round(Sv["A4-C1_GDXJ_artik_h3"]["ek"]["z"], 2), B["V_GDXJRES_h3"]["z"], "hakem bugun json", tol=1e-9)
add("2026-11-09", "A4-C1_GDXJ_artik_h3", "etkin", round(Sv["A4-C1_GDXJ_artik_h3"]["etkin"], 3), B["V_GDXJRES_h3"]["etkin_poz_pazartesi_sonrasi"], "hakem bugun json")
add("2026-11-09", "A8-3_seg_last1h_h5", "acik_toplam_5te", Sv["A8-3_seg_last1h_h5"]["ek"]["acik_toplam_5te"], B["V_LAST1H_h5"]["acik_dilim_toplami_bes_te"], "hakem bugun json")
add("2026-11-09", "A1-LOWMOM-h1", "rv20", round(Sv["A1-LOWMOM-h1"]["ek"]["rv20"], 3), 0.210, "hakem bugun json (rv20 %21,0)", tol=1e-9)
for sid, hk in (("E2-C2j_GDXJ_artik_h3", "E_C2J_h3"), ("E2-C2_GDX_artik_h3", "E_C2_h3"), ("E2-C1_madenci_oncu_GLD_h5", "E_C1_h5")):
    add("2026-11-09", sid, "x_pct", round(Se[sid]["ek"]["x"] * 100, 3), B[hk]["x"], "hakem bugun json")
    add("2026-11-09", sid, "etkin", round(Se[sid]["etkin"], 3), B[hk]["etkin_poz_pazartesi_sonrasi"], "hakem bugun json")
add("2026-11-09", "E3-1_altin_gunici_GDXJ_donus", "esik_fiyat", round(Se["E3-1_altin_gunici_GDXJ_donus"]["ek"]["esik_fiyat"], 2), 4065.68, "hakem bugun json")
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/dogrulama_sinyal_betigi.csv", index=False)
pd.set_option("display.width", 220); pd.set_option("display.max_rows", 200)
print("\n=== (1)-(2) CLI karşılaştırması: sinyal × kaynak × alan ===")
T = R.groupby(["sinyal", "kaynak", "alan"]).agg(n=("esit", "size"), esit=("esit", "sum")).reset_index()
print(T.to_string(index=False))
F = R[~R.esit]
print(f"\nFark sayısı: {len(F)} / {len(R)}")
if len(F): print(F.to_string(index=False))

# ------------------------------------------------------------------ (3) toplu kontrol (modül içinden)
sys.path.insert(0, OUT)
import sinyal_altin as SA
K = SA.PanelKaynak(f"{S}/panel", log=lambda *a, **k: None)
simdi = pd.Timestamp("2262-01-01", tz="UTC")
bas = pd.Timestamp(sys.argv[1] if len(sys.argv) > 1 else "2022-01-01")
TR = []
t0 = time.time()
for d in V.index[V.index >= max(bas, pd.Timestamp("2017-03-06"))]:
    SA.DENETIM.clear()
    o = SA.viop_sinyalleri(K, d.date(), simdi)
    Sg = {s["id"]: s for s in o["sinyaller"]}
    for sid, hk in (("A1-LOWMOM-h1", "V_LOWMOM_h1"), ("A3_QEND_h3", "V_QEND_h3"), ("A4-C1_GDXJ_artik_h3", "V_GDXJRES_h3"), ("A8-3_seg_last1h_h5", "V_LAST1H_h5")):
        s = Sg[sid]; yd = s["yeni_dilim"] if s["durum"] != "DEVRE DIŞI" else 0.0
        yd = 0.0 if yd is None or not np.isfinite(yd) else yd
        TR.append(dict(cephe="VIOP", gun=d.date(), sinyal=sid, pos_esit=yd == VR.loc[d, hk], etkin_fark=abs(s["etkin"] - VP.loc[d, hk]),
                       onceki_fark=abs(float(s["etkin_onceki"] or 0) - float(VP[hk].shift(1).fillna(0).loc[d])), durum=s["durum"]))
    if any(x["sonuc"] == "İHLAL" for x in SA.DENETIM): TR.append(dict(cephe="VIOP", gun=d.date(), sinyal="DENETIM", pos_esit=False, etkin_fark=np.nan, durum="İHLAL"))
for d in E.index[E.index >= bas]:
    SA.DENETIM.clear()
    o = SA.etf_sinyalleri(K, d.date(), simdi)
    Sg = {s["id"]: s for s in o["sinyaller"]}
    for sid, hk in (("E1-C2_GDX_tatil_oncesi", "E_GDXTATIL_h1"), ("E2-C2j_GDXJ_artik_h3", "E_C2J_h3"), ("E2-C2_GDX_artik_h3", "E_C2_h3"),
                    ("E2-C1_madenci_oncu_GLD_h5", "E_C1_h5"), ("E3-1_altin_gunici_GDXJ_donus", "E_M_GDXJ_h1")):
        s = Sg[sid]; yd = s["yeni_dilim"] if s["durum"] != "DEVRE DIŞI" else 0.0
        yd = 0.0 if yd is None or not np.isfinite(yd) else yd
        TR.append(dict(cephe="ETF", gun=d.date(), sinyal=sid, pos_esit=yd == ER.loc[d, hk], etkin_fark=abs(s["etkin"] - EP.loc[d, hk]) if sid != "E3-1_altin_gunici_GDXJ_donus" else abs(yd - EP.loc[d, hk]),
                       onceki_fark=abs(float(s["etkin_onceki"] or 0) - float(EP[hk].shift(1).fillna(0).loc[d])), durum=s["durum"]))
    # kaplama (E_C1kap_h5): kademeli etkin pozisyon
    s = Sg["E2-C1_madenci_oncu_GLD_h5"]
    if "kaplama_etkin" in s["ek"]:
        TR.append(dict(cephe="ETF", gun=d.date(), sinyal="E2-C1_kaplama", pos_esit=s["ek"]["kaplama_poz"] == ER.loc[d, "E_C1kap_h5"],
                       etkin_fark=abs(s["ek"]["kaplama_etkin"] - EP.loc[d, "E_C1kap_h5"]), onceki_fark=abs(s["ek"]["kaplama_etkin_onceki"] - float(EP["E_C1kap_h5"].shift(1).fillna(0).loc[d])), durum=s["durum"]))
    if any(x["sonuc"] == "İHLAL" for x in SA.DENETIM): TR.append(dict(cephe="ETF", gun=d.date(), sinyal="DENETIM", pos_esit=False, etkin_fark=np.nan, durum="İHLAL"))
TR = pd.DataFrame(TR); TR.to_csv(f"{OUT}/dogrulama_sinyal_toplu.csv", index=False)
print(f"\n=== (3) toplu kontrol {bas.date()}..2026-11-06 ({time.time() - t0:.0f} sn) ===")
print(TR.groupby(["cephe", "sinyal"]).agg(gun=("pos_esit", "size"), pos_esit=("pos_esit", "sum"), etkin_maks_fark=("etkin_fark", "max"), onceki_maks_fark=("onceki_fark", "max")).to_string())
FF = TR[~TR.pos_esit | (TR.etkin_fark > 1e-9) | (TR.onceki_fark > 1e-9)]
print(f"Toplu fark: {len(FF)}")
if len(FF): print(FF.head(40).to_string(index=False))
