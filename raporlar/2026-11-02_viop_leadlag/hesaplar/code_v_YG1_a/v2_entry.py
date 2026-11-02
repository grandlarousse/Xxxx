"""v2: Giriş/çıkış gerçekçiliği (h1 2023-11-30+ ve m5 son 60 gün) + mekanik (bid-ask/müzayede gürültüsü) ayrıştırması.
Sinyal: günlük gap (O / C_{-1}, adj düzeltmeli) — 10:00 TSİ'de bilinir.
Girişler: E0 = O (müzayede; iyimser) | TP1 = 06:30 h1 barı (h+l+c)/3 (kaynak ajanın 'ilk 30 dk VWAP vekili'; h/l açılış fiyatını içerir)
          | P0730 = 10:30 TSİ son fiyat | TP2 = 10:30–11:30 TSİ (h+l+c)/3 | P0830 = 11:30 TSİ
          | m5 (60 gün): VW_0730 = 07:00–07:30 UTC hacim ağırlıklı tipik fiyat; VW_0505 = 07:05–07:30 (07:00 barı hariç; müzayede eşleşmesi içermez); P0705.
Çıkışlar: C (kapanış müzayedesi) | P1430 = 17:30 TSİ (yıl boyu) | P1500 = 18:00 TSİ (yalnız yaz).
Çıktı: res/v2_h1_port.csv, res/v2_h1_stock.csv, res/v2_m5.csv, res/v2_pooled.csv
"""
import numpy as np, pandas as pd, vc
TG = vc.VIOP
D = {s: vc.decomp(s, start="2013-06-01") for s in TG + ["XU030"]}
H = {s: vc.h1_panel(s) for s in TG}
days = H["GARAN"].index
days = days[days.isin(vc.cal())]
half = days[len(days) // 2]
liq = pd.read_csv(vc.RES + "/v1_liq.csv", index_col=0); LIQ = list(liq.index[liq["rank"] <= 23]); ILL = list(liq.index[liq["rank"] > 23])

def F(fn): return pd.DataFrame({s: fn(s) for s in TG}).reindex(days)
G = F(lambda s: D[s]["gap"]); O = F(lambda s: D[s]["o"]); C = F(lambda s: D[s]["c"])
HALF = F(lambda s: H[s]["half"]).fillna(True).astype(bool)
h1o_ = F(lambda s: H[s]["h1_o"]); p1430_ = F(lambda s: H[s]["P1430"]); p0730_ = F(lambda s: H[s]["P0730"])
# h1–günlük tutarlılık filtresi (ör. HEKTS 2024-09-09..11-14 h1 bölünme düzeltmesi günlükle uyumsuz: ln(h1_o/O)=1,02)
cons = (np.abs(np.log(h1o_ / O)) < 0.02) & ~(np.abs(np.log(C / p1430_)) > 0.10) & ~(np.abs(np.log(p0730_ / O)) > 0.15)
print("h1-günlük tutarsız (atılan) hisse-gün:", int((~cons & G.notna()).sum().sum()))
ok = G.notna() & ~HALF & F(lambda s: D[s]["intra"]).notna() & cons
PX = {"E0_O": O, "TP1_kaynakE2": F(lambda s: H[s]["TP1"]), "P0730": F(lambda s: H[s]["P0730"]), "TP2_1030-1130": F(lambda s: H[s]["TP2"]), "P0830": F(lambda s: H[s]["P0830"])}
EX = {"C": C, "P1430": F(lambda s: H[s]["P1430"]), "P1500(yaz)": F(lambda s: H[s]["P1500"])}
# h1 fiyat tutarlılığı: h1 06:30 o ~ günlük O
h1o = F(lambda s: H[s]["h1_o"])
print("h1 06:30 o == günlük O oranı:", float((np.abs(np.log(h1o / O)) < 1e-4)[ok].sum().sum() / ok.sum().sum()))

PER = {"h1_tum": np.ones(len(days), bool), "1.yari": days < half, "2.yari": days >= half,
       "2024": days.year == 2024, "2025": days.year == 2025, "2026": days.year == 2026}
rows = []
def rec(spec, R):
    pp = R.mean(axis=1); o = dict(spec=spec)
    tot = R.sum(axis=1, min_count=1); cnt = R.notna().sum(axis=1)
    for pn, m in PER.items():
        x = pp[m].dropna(); mm, t, n = vc.nw_mean(x.values, 5)
        o[f"{pn}_bps"] = 1e4 * mm; o[f"{pn}_t"] = t
        # işlem ağırlıklı (sabit nominal/işlem): ΣPnL/Σişlem, t = günlük toplam PnL serisinin NW t'si
        xs = tot[m].dropna(); _, tt, _ = vc.nw_mean(xs.values, 5)
        o[f"{pn}_TW_bps"] = 1e4 * xs.sum() / max(cnt[m].sum(), 1); o[f"{pn}_TW_t"] = tt
    o["trades"] = int(R.notna().sum().sum()); o["days"] = int(pp.notna().sum())
    rows.append(o)

for thr in [0.01, 0.02]:
    pos = (-np.sign(G)).where((G.abs() > thr) & ok, 0.0).fillna(0.0)
    for uni, cols in [("47", TG), ("likit23", LIQ), ("illikit24", ILL)]:
        for en, Pin in PX.items():
            for ex, Pout in EX.items():
                if uni != "47" and ex != "C" and en not in ("E0_O", "P0730"): continue
                y = np.log(Pout / Pin)
                valid = y.notna() & (pos != 0)
                # aynı örneklem: tüm giriş/çıkışlar için ortak geçerli günler (çıkış bazında)
                R = (pos * y).where(valid)[cols]
                rec(f"|gap|>{thr:.0%} {uni} {en}->{ex}", R)
        # asimetri (E0->C ve P0730->C)
        for side, msk in [("UP-short", G > 0), ("DOWN-long", G < 0)]:
            for en in ["E0_O", "P0730", "TP2_1030-1130"]:
                y = np.log(C / PX[en]); R = (pos.where(msk, 0.0) * y).where((pos.where(msk, 0.0) != 0) & y.notna())[cols]
                rec(f"|gap|>{thr:.0%} {uni} {side} {en}->C", R)
    # ilk 30 dk'nın kendisi: O -> 10:30 fade getirisi (giriş gecikmesi maliyeti)
    y = np.log(PX["P0730"] / O); rec(f"|gap|>{thr:.0%} 47 O->P0730 (ilk saat fade payı)", (pos * y).where((pos != 0) & y.notna()))
PT = pd.DataFrame(rows); PT.to_csv(vc.RES + "/v2_h1_port.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 500)
print(PT[["spec", "h1_tum_bps", "h1_tum_t", "h1_tum_TW_bps", "h1_tum_TW_t", "1.yari_bps", "2.yari_bps", "2.yari_t", "2024_bps", "2025_bps", "2026_bps", "trades"]].round(2).to_string())

# giriş kaybı (slippage) = −s·ln(Pin/O)  (pozitif = açılışa göre daha kötü giriş)
pos = (-np.sign(G)).where((G.abs() > 0.01) & ok, 0.0).fillna(0.0)
print("\n=== Giriş kaybı vs açılış (|gap|>1%, bps; pozitif = kötü) ===")
for en, Pin in PX.items():
    sl = (pos * np.log(Pin / O)).where((pos != 0) & Pin.notna())  # fade yönünde: short'ta Pin<O kötü -> pos=-1, ln(Pin/O)<0 -> pozitif
    print(f"{en:16s} ortalama {1e4*np.nanmean(sl.values):7.2f}  medyan {1e4*np.nanmedian(sl.values):7.2f}  n {int(sl.notna().sum().sum())}")

# hisse bazında (CIMSA/OYAKC/ALARK + hepsi) h1 dönemi
srows = []
for s in TG:
    for en in ["E0_O", "TP1_kaynakE2", "P0730", "TP2_1030-1130"]:
        for ex in ["C", "P1430"]:
            y = np.log(EX[ex][s] / PX[en][s]); x = (pos[s] * y).where((pos[s] != 0) & y.notna()).dropna()
            mm, t, n = vc.nw_mean(x.values, 5)
            srows.append(dict(stock=s, entry=en, exit=ex, bps=1e4 * mm, t=t, n=n))
SR = pd.DataFrame(srows)
for (en, ex), g in SR.groupby(["entry", "exit"]):
    rej, _ = vc.bh(vc.t2p(g["t"].values)); SR.loc[g.index, "fdr"] = rej
SR.to_csv(vc.RES + "/v2_h1_stock.csv", index=False)
print("\n=== h1 dönemi hisse bazında (|gap|>1%) ===")
pv = SR.pivot_table(index="stock", columns=["entry", "exit"], values="bps")
print(pv.loc[["CIMSA", "OYAKC", "ALARK"]].round(1).to_string())
print(SR[SR.stock.isin(["CIMSA", "OYAKC", "ALARK"])].round(2).to_string())
print("FDR sayısı (giriş,çıkış):", SR.groupby(["entry", "exit"])["fdr"].sum().to_dict())
print("medyan hisse bps:", SR.groupby(["entry", "exit"])["bps"].median().round(1).to_dict())

# ===================== m5: gerçek VWAP ile vekil karşılaştırması (60 gün)
mrows = []
for s in TG:
    try:
        m = pd.read_parquet(f"{vc.DATA}/m5/{s}.IS.parquet")
    except Exception:
        continue
    m = m[~m.index.duplicated(keep="last")].sort_index()
    t = m.index.tz_convert(None); dd = t.normalize(); hm = t.hour * 100 + t.minute
    df = pd.DataFrame({"d": dd, "hm": hm, "tp": (m["h"] + m["l"] + m["c"]).values / 3, "v": m["v"].values, "c": m["c"].values})
    w1 = df[(df.hm >= 700) & (df.hm <= 725)]; w2 = df[(df.hm >= 705) & (df.hm <= 725)]
    vw1 = (w1.tp * w1.v).groupby(w1.d).sum() / w1.v.groupby(w1.d).sum()
    vw2 = (w2.tp * w2.v).groupby(w2.d).sum() / w2.v.groupby(w2.d).sum()
    p0705 = df[df.hm == 700].set_index("d")["c"]
    p0730m = df[df.hm == 725].set_index("d")["c"]
    X = pd.DataFrame({"vw1": vw1, "vw2": vw2, "p0705": p0705, "p0730m": p0730m})
    X["O"] = D[s]["o"].reindex(X.index); X["C"] = D[s]["c"].reindex(X.index); X["gap"] = D[s]["gap"].reindex(X.index)
    X["TP1"] = H[s]["TP1"].reindex(X.index); X["P0730"] = H[s]["P0730"].reindex(X.index)
    X = X.dropna(subset=["gap", "O", "C"]); X = X[np.abs(np.log(X["vw2"] / X["O"])) < 0.15]
    X["pos"] = (-np.sign(X["gap"])).where(X["gap"].abs() > 0.01, 0.0)
    X["stock"] = s
    mrows.append(X)
M = pd.concat(mrows); M = M[M.pos != 0]
print("\n=== m5 (son 60 gün, |gap|>1%) giriş kaybı vs O, bps (pozitif=kötü); n işlem", len(M), "===")
for k in ["TP1", "vw1", "vw2", "p0705", "P0730", "p0730m"]:
    sl = M["pos"] * np.log(M[k] / M["O"])
    print(f"{k:8s} ort {1e4*sl.mean():7.2f}  medyan {1e4*sl.median():7.2f}")
d_tp1_vw = M["pos"] * np.log(M["vw2"] / M["TP1"])
print("TP1 vekili ile gerçek 07:05–07:30 VWAP farkı (fade yönünde, pozitif=vekil iyimser):", round(1e4 * d_tp1_vw.mean(), 2), "bps; |fark| medyan", round(1e4 * np.abs(np.log(M.vw2 / M.TP1)).median(), 1))
print("P0730(h1) == m5 07:25 kapanışı:", float((np.abs(np.log(M.P0730 / M.p0730m)) < 1e-4).mean()))
for k in ["O", "TP1", "vw1", "vw2", "P0730"]:
    r = M["pos"] * np.log(M["C"] / M[k]); print(f"m5 dönemi fade {k}->C: {1e4*r.mean():7.2f} bps (gün-ort portföy {1e4*(r.groupby(level=0).mean()).mean():.2f})")
M.to_csv(vc.RES + "/v2_m5.csv")

# ===================== havuz regresyonu: yön (b) vs büyüklük (|gap|) etkisi, gün kümelenmiş
def ols_cl(y, X, g):
    X = np.column_stack([np.ones(len(y)), X]); iXX = np.linalg.pinv(X.T @ X); b = iXX @ X.T @ y; u = y - X @ b
    gi = pd.factorize(g)[0]; S = np.zeros((gi.max() + 1, X.shape[1])); np.add.at(S, gi, X * u[:, None])
    V = iXX @ (S.T @ S) @ iXX; return b, b / np.sqrt(np.diag(V))
idx = vc.cal(); idx = idx[idx >= "2014-01-01"]
GG = pd.DataFrame({s: D[s]["gap"] for s in TG}).reindex(idx); II = pd.DataFrame({s: D[s]["intra"] for s in TG}).reindex(idx)
gm = D["XU030"]["gap"].reindex(idx); im = D["XU030"]["intra"].reindex(idx)
L = []
for s in TG:
    L.append(pd.DataFrame({"d": idx, "s": s, "y": II[s].values, "g": GG[s].values, "gm": gm.values, "im": im.values}))
L = pd.concat(L).dropna()
L["idio"] = L.g - L.gm
prow = []
for pn, m in [("IS14-20", L.d < vc.SPLIT), ("IS16-20", (L.d >= "2016-01-01") & (L.d < vc.SPLIT)), ("OOS21-26", L.d >= vc.SPLIT), ("2024+", L.d >= "2024-01-01")]:
    x = L[m]
    for spec, cols in [("y~g", ["g"]), ("y~g+|g|", ["g", "ag"]), ("y~idio+gm+|idio|+|gm|", ["idio", "gm", "aidio", "agm"])]:
        X = x.assign(ag=x.g.abs(), aidio=x.idio.abs(), agm=x.gm.abs())[cols].values
        b, t = ols_cl(x.y.values, X, x.d.values)
        o = dict(period=pn, spec=spec, n=len(x))
        for i, cn in enumerate(cols): o[f"b_{cn}"] = b[i + 1]; o[f"t_{cn}"] = t[i + 1]
        prow.append(o)
    # yalnız |gap|>1% gözlemleri, ayrı eğimler: yukarı ve aşağı
    xx = x[x.g.abs() > 0.01]
    X = np.column_stack([xx.g.clip(lower=0), xx.g.clip(upper=0)]); b, t = ols_cl(xx.y.values, X, xx.d.values)
    prow.append(dict(period=pn, spec="|g|>1%: y~g+ , g-", n=len(xx), b_gpos=b[1], t_gpos=t[1], b_gneg=b[2], t_gneg=t[2], const=b[0], t_const=t[0]))
PR = pd.DataFrame(prow); PR.to_csv(vc.RES + "/v2_pooled.csv", index=False)
print("\n=== Havuz regresyonu (intra ~ ...; gün kümelenmiş t) ==="); print(PR.round(4).to_string())
print("Koşulsuz ortalama intra (tüm hisse-günler) IS/OOS bps:", round(1e4 * L[L.d < vc.SPLIT].y.mean(), 1), round(1e4 * L[L.d >= vc.SPLIT].y.mean(), 1))
for pn, m in [("IS", L.d < vc.SPLIT), ("OOS", L.d >= vc.SPLIT)]:
    x = L[m]
    print(pn, "ortalama intra bps | gap>1%:", round(1e4 * x[x.g > 0.01].y.mean(), 1), " gap<-1%:", round(1e4 * x[x.g < -0.01].y.mean(), 1), " |gap|<=1%:", round(1e4 * x[x.g.abs() <= 0.01].y.mean(), 1))
