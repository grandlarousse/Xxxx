"""v2: PLASEBO / ÖZGÜLLÜK testleri.
 (a) Hedef kesiti: AIR -> tüm BIST hisseleri (47 VİOP + diğer) gün-içi; havacılık hisselerinin sırası.
 (b) Sürücü plasebosu: sektör sepetleri (AB+ABD, aynı artık/z/eşik kuralı) -> THYAO/PGSUS/TAVHL.
 (c) Rastgele sepet null'u: 7 AB + 6 ABD havacılık/turizm DIŞI hisse, 400 çekiliş.
 (d) Rastgele işaret / blok karıştırma null'u ve bayatlatma (t-2, t-3).
"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
pd.set_option("display.width", 250)
SG = pd.read_parquet(RES + "/signals.parquet")
AIR = SG.AIR_C
cat = pd.read_csv(S + "/data/catalog.csv")
TGT = ["THYAO", "PGSUS", "TAVHL"]
Y = {st: bist_day(st + ".IS").intra for st in TGT}

def summ(sig, y, cost=8):
    r = bt_periods(sig, y, cost, 1.0, ("IS", "OOS", "ALL"))
    return {f"{p}_{k}": r[p][k] for p in r for k in ["n", "bps", "t", "gross"]}

def cont_t(sig, y):
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna(); df = df[df.index >= "2014-01-01"]
    r, n = ols_nw(df.y, df[["s"]]); return r.loc["s", "t"]

out = []
# ---------- (a) hedef kesiti
bist = cat[(cat.group.isin(["VIOP", "BIST_other"])) & (cat.type == "EQUITY")].sym.tolist()
viop = set(cat[cat.group == "VIOP"].sym)
rows = []
for s in bist:
    d = bist_day(s)
    if d is None or d.intra.notna().sum() < 750: continue
    y = d.intra
    # likidite: medyan TL hacim (son 2y)
    tl = (d.c * d.v)[d.index >= "2024-11-01"].median()
    r = summ(AIR, y); rows.append({"sym": s, "viop": s in viop, "tl_med_mn": tl / 1e6, "cont_t": cont_t(AIR, y), **r})
A = pd.DataFrame(rows)
A["rk_gross_ALL"] = A.ALL_gross.rank(ascending=False); A["rk_contt"] = A.cont_t.rank(ascending=False)
A.to_csv(RES + "/v2a_crosssection.csv", index=False)
print("== (a) AIR -> gün-içi, hedef kesiti: n hisse =", len(A), "| VİOP =", A.viop.sum())
cols = ["sym", "viop", "tl_med_mn", "cont_t", "IS_gross", "IS_t", "OOS_gross", "OOS_t", "ALL_gross", "ALL_bps", "rk_contt"]
print(A.sort_values("cont_t", ascending=False)[cols].head(25).round(2).to_string(index=False))
print("... dağılım cont_t: medyan %.2f, %%90 %.2f, %%95 %.2f; cont_t>2 olan hisse %d / %d; VİOP içinde cont_t>2: %d/%d" % (
    A.cont_t.median(), A.cont_t.quantile(.9), A.cont_t.quantile(.95), (A.cont_t > 2).sum(), len(A), (A[A.viop].cont_t > 2).sum(), A.viop.sum()))
print("ALL_gross medyan %.1f bps (tüm hisseler), VİOP medyan %.1f" % (A.ALL_gross.median(), A[A.viop].ALL_gross.median()))
print(A[A.sym.isin(["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "CLEBI.IS", "DOCO.IS"])][cols].round(2).to_string(index=False))
V = A[A.viop].sort_values("cont_t", ascending=False).reset_index(drop=True)
print("VİOP 47 içinde sıra (cont_t):", {s: int(V.index[V.sym == s][0]) + 1 for s in ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"]})
print("VİOP 47 içinde OOS net>0 & t>2 olanlar:", V[(V.OOS_t > 2)].sym.tolist())

# ---------- (b) sektör sepetleri
eu_tz = cat.tz.fillna("").str.startswith("Europe/") & (cat.tz != "Europe/Istanbul")
us_tz = cat.tz == "America/New_York"
travel_words = "Cruise|Carnival|Royal Caribbean|Norwegian Cruise|Hotel|Hilton|Marriott|Booking|Expedia|Airbnb|TUI|Meli|Accor|Hyatt|InterContinental|Whitbread|Trip|Aeroport|Airport|Flughafen|Fraport|Aena|Air|Jet|Wizz|Ryanair|Lufthansa|Delta|United Airlines|Southwest|Alaska|Copa|easyJet|Finnair|Norwegian Air|Aegean"
eq = cat[(cat.type == "EQUITY")]
rows = []
for g in ["bank", "auto", "steel", "chem", "cement", "oil", "tel", "util", "cons", "def", "re"]:
    eu = eq[eu_tz & (eq.group == g)].sym.tolist(); us = eq[us_tz & (eq.group == g)].sym.tolist()
    if len(eu) < 3 or len(us) < 3: continue
    P = sector_signal(eu, us); sg = P["EU"] + P["US"]
    for st in TGT:
        rows.append({"basket": g, "n_eu": len(eu), "n_us": len(us), "tgt": st, "cont_t": cont_t(sg, Y[st]), "corr_AIR": sg.corr(AIR), **summ(sg, Y[st])})
# havacılık-dışı turizm/seyahat (otel, kruvaziyer, online seyahat) — yakın plasebo
trav_eu = ["TUI1.DE", "MEL.MC", "AC.PA", "IHG.L", "WTB.L"]; trav_us = ["CCL", "RCL", "NCLH", "BKNG", "EXPE", "MAR", "HLT"]
trav_eu = [s for s in trav_eu if raw(s) is not None]; trav_us = [s for s in trav_us if raw(s) is not None]
P = sector_signal(trav_eu, trav_us); sg = P["EU"] + P["US"]
for st in TGT:
    rows.append({"basket": "travel_nonair", "n_eu": len(trav_eu), "n_us": len(trav_us), "tgt": st, "cont_t": cont_t(sg, Y[st]), "corr_AIR": sg.corr(AIR), **summ(sg, Y[st])})
for st in TGT:
    rows.append({"basket": "AIR", "n_eu": 7, "n_us": 6, "tgt": st, "cont_t": cont_t(AIR, Y[st]), "corr_AIR": 1.0, **summ(AIR, Y[st])})
B = pd.DataFrame(rows); B.to_csv(RES + "/v2b_sector.csv", index=False)
print("\n== (b) Sektör sepeti plasebosu (aynı kural, 8 bps) ==  travel_nonair:", trav_eu, trav_us)
print(B[["basket", "n_eu", "n_us", "tgt", "corr_AIR", "cont_t", "IS_bps", "IS_t", "OOS_bps", "OOS_t", "ALL_gross"]].round(2).to_string(index=False))

# ---------- (c) rastgele sepet null'u
pool_eu = [s for s in eq[eu_tz & ~eq.group.isin(["air"]) & ~eq.name.fillna("").str.contains(travel_words)].sym if raw(s) is not None]
pool_us = [s for s in eq[us_tz & ~eq.group.isin(["air", "tr_abroad"]) & ~eq.name.fillna("").str.contains(travel_words)].sym if raw(s) is not None]
REU = pd.concat({s: r for s in pool_eu if (r := ret_own(s)) is not None and r.index[0] < pd.Timestamp("2013-01-01")}, axis=1)
RUS = pd.concat({s: r for s in pool_us if (r := ret_own(s)) is not None and r.index[0] < pd.Timestamp("2013-01-01")}, axis=1)
sx = ret_own("^STOXX"); sp = ret_own("^GSPC")
print("\n== (c) rastgele sepet havuzu: AB", REU.shape[1], "ABD", RUS.shape[1])
rng = np.random.default_rng(42)
def sig_from(cols_eu, cols_us):
    e = REU[cols_eu]; e = e.mean(1).where(e.notna().sum(1) >= 2).dropna()
    u = RUS[cols_us]; u = u.mean(1).where(u.notna().sum(1) >= 2).dropna()
    return to_bist(zs(rresid(e, sx)).clip(-3, 3)) + to_bist(zs(rresid(u, sp)).clip(-3, 3))
NR = 400; rows = []
for i in range(NR):
    ce = list(rng.choice(REU.columns, 7, replace=False)); cu = list(rng.choice(RUS.columns, 6, replace=False))
    sg = sig_from(ce, cu)
    rec = {"i": i}
    for st in TGT:
        r = bt_periods(sg, Y[st], 8, 1.0, ("IS", "OOS", "ALL"))
        rec[f"{st}_ALL_t"] = r["ALL"]["t"]; rec[f"{st}_OOS_t"] = r["OOS"]["t"]; rec[f"{st}_IS_t"] = r["IS"]["t"]; rec[f"{st}_ALL_gross"] = r["ALL"]["gross"]
    rows.append(rec)
N = pd.DataFrame(rows); N.to_csv(RES + "/v2c_random_baskets.csv", index=False)
for st in TGT:
    obs = bt_periods(AIR, Y[st], 8, 1.0, ("IS", "OOS", "ALL"))
    for p in ["IS", "OOS", "ALL"]:
        nul = N[f"{st}_{p}_t"]
        print(f"{st} {p}: gözlenen t={obs[p]['t']:.2f}; null medyan {nul.median():.2f}, %95 {nul.quantile(.95):.2f}, %99 {nul.quantile(.99):.2f}; p(null>=obs)={(nul >= obs[p]['t']).mean():.4f}")
    print(f"   {st} ALL brüt: gözlenen {obs['ALL']['gross']:.1f}; null medyan {N[f'{st}_ALL_gross'].median():.1f}, %95 {N[f'{st}_ALL_gross'].quantile(.95):.1f}")
# ortak: 3 hissenin ortalama t'si
N["avg_ALL_t"] = N[[f"{s}_ALL_t" for s in TGT]].mean(1)
obs_avg = np.mean([bt(AIR, Y[s], 8, 1.0)["t"] for s in TGT])
print(f"3 hisse ort. ALL t: gözlenen {obs_avg:.2f}; null %95 {N.avg_ALL_t.quantile(.95):.2f}; p={(N.avg_ALL_t >= obs_avg).mean():.4f}")

# ---------- (d) bayatlatma ve rastgele işaret
print("\n== (d) Bayatlatma (AIR'i k BIST günü daha geç kullan) ==")
rows = []
for st in TGT:
    for k in [0, 1, 2, 3, 5]:
        r = bt_periods(AIR.shift(k), Y[st], 8, 1.0, ("IS", "OOS", "ALL"))
        rows.append({"tgt": st, "extra_lag": k, **{f"{p}_{m}": r[p][m] for p in r for m in ["bps", "t"]}})
print(pd.DataFrame(rows).round(2).to_string(index=False))
print("\n== (d2) Rastgele işaret null'u: aynı işlem günleri, işaret yıl içinde karıştırılır (2000 tekrar) ==")
for st in TGT:
    df = pd.concat([AIR.rename("s"), Y[st].rename("y")], axis=1).dropna(); df = df[df.s.abs() > 1]
    obs = (np.sign(df.s) * df.y).mean()
    yrs = df.index.year.values; sg = np.sign(df.s.values); yv = df.y.values
    nul = []
    for i in range(2000):
        sh = sg.copy()
        for yy in np.unique(yrs):
            m = yrs == yy; sh[m] = rng.permutation(sh[m])
        nul.append((sh * yv).mean())
    nul = np.array(nul)
    print(f"{st}: gözlenen brüt {1e4*obs:.1f} bps; null medyan {1e4*np.median(nul):.1f}, %99 {1e4*np.quantile(nul,.99):.1f}; p={(nul>=obs).mean():.4f}")
