"""Görev 3: aileye özgü hipotezler (hipotezler.csv ST01-ST06 + yönlendirme: SPY'a göre kalıntı dönüşü,
sektör içi çiftler, kaldıraçlı ürünlerde dayanak sinyali). Parametreler önceden sabitlendi (tarama yok):
  eşik z=-2 (literatürdeki standart 2 sd), beta/sd penceresi 60 gün, h∈{1,2,3}, mod∈{C0,O1,C1}.
Her test satırı tests_hipotez.csv'ye yazılır (p: havuzlanmışlarda hafta-kümeli t'den).
Çıktılar: sonuclar/aile_sektor_tematik/tests_hipotez.csv, st05_kaldirac_kaybi.csv"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *

t0 = time.time()
MODES = ("C0", "O1", "C1"); HS = (1, 2, 3)
rows = []


def rec(fam, hyp, label, tr, h, mode, extra=None):
    r = summarize(tr, label)
    r.update({"grup": fam, "hipotez": hyp, "h": h, "mode": mode})
    if extra: r.update(extra)
    rows.append(r)
    return r


def lr(sym):
    return np.log(D(sym)["c"]).diff()


SPY_R = lr("SPY")


def resid_z(sym, ref="SPY", k=1, n=60):
    """k günlük kalıntı (r - beta*r_ref) z skoru; beta ve sd t-1'e kadar (60 gün)."""
    a = lr(sym); b = lr(ref).reindex(a.index)
    beta = (a.rolling(n).cov(b) / b.rolling(n).var()).shift(1)
    e = a - beta * b
    sd = e.rolling(n).std().shift(1)
    ek = e.rolling(k).sum()
    return ek / (sd * math.sqrt(k))


# ---------------- ST01: sektör IBS<0.2 & C>SMA200, C0 h=1 (birincil); diğer mod/h sağlamlık -------------
ST01 = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC", "SMH", "XBI", "KRE"]
for mode in MODES:
    for h in HS:
        trs = []
        for s in ST01:
            df = D(s); sig = (lib.ibs(df) < 0.2) & (df["c"] > lib.sma(df["c"], 200))
            trs.append(run_sym(s, sig, h, mode))
        rec("ST01", "ST01_sektor_IBS", f"ST01 {mode} h{h}", pd.concat(trs, ignore_index=True), h, mode,
            {"birincil": mode == "C0" and h == 1})

# ---------------- KALINTI: SPY'a göre beta60 kalıntı z1 < -2 -> al (37 küme temsilcisi + SPDR11 ayrıca) ----
for uni_name, uni in (("REPS37", REPS), ("SPDR11", SPDR11)):
    for mode in MODES:
        for h in HS:
            trs = []
            for s in uni:
                z = resid_z(s, "SPY", 1)
                trs.append(run_sym(s, z < -2, h, mode))
            rec("KALINTI", f"kalinti_z1_lt_m2_{uni_name}", f"kalinti z1<-2 {uni_name} {mode} h{h}",
                pd.concat(trs, ignore_index=True), h, mode)
    # kontrol: aşırı alınan (z1>2) -> al (devam mı dönüş mü)
    for h in HS:
        trs = [run_sym(s, resid_z(s, "SPY", 1) > 2, h, "C0") for s in uni]
        rec("KALINTI", f"kalinti_z1_gt_2_{uni_name}_kontrol", f"kalinti z1>2 {uni_name} C0 h{h}",
            pd.concat(trs, ignore_index=True), h, "C0")

# ---------------- ST02 / ST03: kesitsel (11 SPDR) ------------------------------------------------------
C = pd.DataFrame({s: D(s)["c"] for s in SPDR11}).reindex(D("SPY").index)
R1 = np.log(C).diff().sub(SPY_R, axis=0)          # SPY'a göre 1 gün
R5 = np.log(C / C.shift(5))                       # 5 günlük getiri
def rank_sig(M, k, worst=True):
    rk = M.rank(axis=1, ascending=worst, method="first")
    ok = M.notna().sum(axis=1) >= 9
    return (rk <= k) & ok.values[:, None]
sel = {"ST02_en_kotu2_1g": rank_sig(R1, 2, True), "ST02_kontrol_en_iyi2_1g": rank_sig(R1, 2, False),
       "ST03_5g_en_iyi3": rank_sig(R5, 3, False), "ST03_kontrol_5g_en_kotu3": rank_sig(R5, 3, True)}
for nm, M in sel.items():
    for mode in MODES:
        for h in HS:
            trs = [run_sym(s, M[s], h, mode) for s in SPDR11]
            rec("ST02_03", nm, f"{nm} {mode} h{h}", pd.concat(trs, ignore_index=True), h, mode,
                {"birincil": (mode == "C0" and h == 3 and "kontrol" not in nm)})
# koşulsuz (her gün her SPDR) referans
for mode in ("C0",):
    for h in HS:
        trs = [run_sym(s, pd.Series(True, index=D(s).index), h, mode) for s in SPDR11]
        rec("ST02_03", "kosulsuz_SPDR_ortalama", f"kosulsuz {mode} h{h}", pd.concat(trs, ignore_index=True), h, mode)

# ---------------- ST04: büyük->küçük endüstri içi ----------------------------------------------------
ST04 = [("IBB", "XBI"), ("XLE", "XOP"), ("SPY", "RSP"), ("XLF", "KRE")]
for big, small in ST04:
    d = (lr(big) - lr(small).reindex(lr(big).index))
    for mode in MODES:
        for h in HS:
            tr = run_sym(small, d >= 0.015, h, mode)
            rec("ST04", f"ST04_{big}_{small}", f"ST04 {big}->{small} {mode} h{h}", tr, h, mode,
                {"birincil": mode == "C0" and h == 1})

# ---------------- ST06: tematik sert düşüş r<=-2σ20 & C>SMA50, C0 h=2 -------------------------------
ST06 = ["ARKK", "TAN", "URA", "LIT", "KWEB", "JETS", "ITB", "XHB"]
for mode in MODES:
    for h in HS:
        trs = []
        for s in ST06:
            df = D(s); r = df["c"].pct_change(); sd = r.rolling(20).std().shift(1)
            sig = (r <= -2 * sd) & (df["c"] > lib.sma(df["c"], 50))
            trs.append(run_sym(s, sig, h, mode))
        rec("ST06", "ST06_tematik_sert_dusus", f"ST06 {mode} h{h}", pd.concat(trs, ignore_index=True), h, mode,
            {"birincil": mode == "C0" and h == 2})

# ---------------- ÇİFTLER: A'nın B'ye göre kalıntı z'si ---------------------------------------------
PAIRS = [("KRE", "XLF"), ("XBI", "IBB"), ("SMH", "QQQ"), ("SOXX", "SMH"), ("XOP", "XLE"), ("OIH", "XLE"),
         ("ITB", "XHB"), ("IGV", "XLK")]
for k in (1, 5):
    for mode in MODES:
        for h in HS:
            trA, trB = [], []
            for a, b in PAIRS:
                z = resid_z(a, b, k)
                ta = run_sym(a, z < -2, h, mode); ta["pair"] = f"{a}/{b}"; trA.append(ta)
                tb = run_sym(b, z > 2, h, mode); tb["pair"] = f"{a}/{b}"; trB.append(tb)
                rec("CIFT", f"cift_{a}_{b}_z{k}_A_geride", f"{a}/{b} z{k}<-2 al {a} {mode} h{h}", ta, h, mode, {"tek_cift": True})
                rec("CIFT", f"cift_{a}_{b}_z{k}_B_geride", f"{a}/{b} z{k}>2 al {b} {mode} h{h}", tb, h, mode, {"tek_cift": True})
            rec("CIFT", f"cift_havuz_z{k}_A_geride", f"8 cift z{k}<-2 al A {mode} h{h}", pd.concat(trA, ignore_index=True), h, mode)
            rec("CIFT", f"cift_havuz_z{k}_B_geride", f"8 cift z{k}>2 al B {mode} h{h}", pd.concat(trB, ignore_index=True), h, mode)

# ---------------- KALDIRAÇLI ARAÇ: dayanak sinyali -> kaldıraçlı ETF'de işlem ------------------------
LEVP = [("SOXX", "SOXL"), ("SMH", "SOXL"), ("XLK", "TECL"), ("XLF", "FAS"), ("XBI", "LABU"), ("XOP", "GUSH"), ("ITB", "NAIL")]
SIGF = {"IBS_lt02": lambda d: lib.ibs(d) < 0.2,
        "RSI2_lt10": lambda d: lib.rsi(d["c"], 2) < 10,
        "IBS_lt01_dusus": lambda d: (lib.ibs(d) < 0.1) & (d["c"] < d["c"].shift(1))}
for und, lev in LEVP:
    for sn, f in SIGF.items():
        sig = f(D(und))
        for mode in MODES:
            for h in HS:
                tl = run_sym(lev, sig, h, mode)
                tu = run_sym(und, sig, h, mode)
                rec("KALDIRAC", f"lev_{und}_{sn}_{lev}", f"{und} {sn} -> {lev} {mode} h{h}", tl, h, mode,
                    {"arac": lev, "dayanak": und, "dayanak_net_bp": tu["net"].mean() * 1e4 if len(tu) else np.nan,
                     "dayanak_gross_bp": tu["gross"].mean() * 1e4 if len(tu) else np.nan})

res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, "tests_hipotez.csv"), index=False)
print("hipotez test sayısı:", len(res), "süre", round(time.time() - t0), "sn")

# ---------------- ST05 ölçüm: kaldıraç kaybı -------------------------------------------------------
# log tanımı: e_log = ln(1+r_Lx) - L*ln(1+r_baz)  (teorik ≈ -(L²-L)/2 * Σσ²  -> hipotezdeki -3hσ² (L=3))
# basit tanım: e = r_Lx - L*r_baz (yatırımcının gördüğü fark; otokorelasyon yoksa beklenen ≈ ücret+finansman)
out = []
for und, lev in [("SOXX", "SOXL"), ("XBI", "LABU"), ("XLF", "FAS"), ("XLK", "TECL"), ("XLE", "ERX"), ("XOP", "GUSH"), ("ITB", "NAIL")]:
    L = LEV[lev]; cu = D(und)["c"]; cl = D(lev)["c"].reindex(cu.index)
    sg = cu.pct_change().rolling(20).std()          # t'de bilinen σ_g (20 gün)
    for h in HS:
        ru = cu.shift(-h) / cu - 1; rl = cl.shift(-h) / cl - 1
        e = rl - L * ru
        el = np.log1p(rl) - L * np.log1p(ru)
        theo = -(L * L - L) / 2 * h * sg ** 2
        dfx = pd.DataFrame({"e": e, "el": el, "theo": theo, "sg": sg}).dropna()
        for b, m in (("tum", dfx.sg > 0), ("sg<1.5%", dfx.sg < 0.015), ("1.5-3%", (dfx.sg >= 0.015) & (dfx.sg < 0.03)), ("sg>=3%", dfx.sg >= 0.03)):
            x = dfx[m]
            if len(x) < 20: continue
            out.append({"arac": lev, "dayanak": und, "L": L, "h": h, "sigma_bin": b, "n": len(x),
                        "ort_basit_sapma_bp": x.e.mean() * 1e4, "medyan_basit_sapma_bp": x.e.median() * 1e4,
                        "ort_log_sapma_bp": x.el.mean() * 1e4, "teorik_log_bp": x.theo.mean() * 1e4, "sd_basit_sapma_bp": x.e.std() * 1e4})
st5 = pd.DataFrame(out); st5.to_csv(os.path.join(OUT, "st05_kaldirac_kaybi.csv"), index=False)

pd.set_option("display.width", 260); pd.set_option("display.max_rows", 400)
cols = ["label", "n", "mean_gross_bp", "mean_net_bp", "t_cl", "t_cl_ay", "is_net_bp", "oos_net_bp", "is_t_cl", "oos_t_cl",
        "years_pos_frac", "pos_sym_frac", "mean_hedged_bp", "t_hedged_cl", "win", "pf"]
for gname in ["ST01", "KALINTI", "ST02_03", "ST04", "ST06"]:
    print("\n==", gname); print(res[res.grup == gname][cols].round(2).to_string())
print("\n== CIFT havuz"); print(res[(res.grup == "CIFT") & res.hipotez.str.contains("havuz")][cols].round(2).to_string())
c1 = res[(res.grup == "CIFT") & ~res.hipotez.str.contains("havuz") & (res.mode == "C0")]
print("\n== CIFT tek, C0, t_cl>=2"); print(c1[c1.t_cl >= 2][cols].round(2).to_string())
k = res[res.grup == "KALDIRAC"]
print("\n== KALDIRAC (C0/O1/C1 h1-3) t>=2 veya en iyi 30"); print(k.sort_values("t_cl", ascending=False)[cols + ["dayanak_net_bp", "dayanak_gross_bp"]].head(40).round(2).to_string())
print("\n== ST05"); print(st5.round(1).to_string())
