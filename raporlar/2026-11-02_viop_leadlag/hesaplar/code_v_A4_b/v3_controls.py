"""v3: ortak faktör kontrolleri, alt dönem istikrarı, uç değer bağımlılığı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
pd.set_option("display.width", 250)
SG = pd.read_parquet(RES + "/signals.parquet")
AIR = SG.AIR_C; AIRA = SG.AIR_A
TGT = ["THYAO", "PGSUS", "TAVHL"]
D = {st: bist_day(st + ".IS") for st in TGT}
X1 = bist_day("XU100.IS"); X3 = bist_day("XU030.IS")

# ---------- kontrol değişkenleri (hepsi BIST t açılışından önce bilinir)
def drv(sym):
    return to_bist(ret_own(sym))
C = pd.DataFrame({
    "XU100_cc_l1": X1.cc.shift(1), "XU100_intra_l1": X1.intra.shift(1), "XU100_gap_t": X1.gap,
    "TUR_l1": drv("TUR"), "EEM_l1": drv("EEM"), "ES_l1": drv("ES=F"), "USDTRY_l1": drv("TRY=X"),
    "BRENT_l1": drv("BZ=F"), "VIX_l1": drv("^VIX"), "STOXX_l1": drv("^STOXX"), "SPX_l1": drv("^GSPC"), "JETS_l1": drv("JETS"),
    "EURUSD_l1": drv("EURUSD=X"),
})
# USDTRY / TL getiri: TL kirliliği için hedef USD bazında da
fx_t = to_bist(ret_own("TRY=X"))  # t-1 sonu; aynı gün gün-içi kur hareketi yok -> USD-bazlı gün-içi için saatlik yok; atlanıyor
print("AIR ile kontrollerin korelasyonu:\n", C.corrwith(AIR).round(3).to_string())

rows = []
for st in TGT:
    d = D[st]
    base = pd.DataFrame({"AIR": AIR, "own_cc_l1": d.cc.shift(1), "own_intra_l1": d.intra.shift(1), "own_gap_t": d.gap})
    specs = {
        "S0_yalın": ["AIR"],
        "S1_+kendi&XU100 gecikme": ["AIR", "own_cc_l1", "own_intra_l1", "XU100_cc_l1", "XU100_intra_l1"],
        "S2_+gap_t": ["AIR", "own_cc_l1", "own_intra_l1", "XU100_cc_l1", "XU100_intra_l1", "own_gap_t", "XU100_gap_t"],
        "S3_+küresel(TUR,EEM,ES,VIX,STOXX,SPX)": ["AIR", "TUR_l1", "EEM_l1", "ES_l1", "VIX_l1", "STOXX_l1", "SPX_l1"],
        "S4_+makro(USDTRY,EURUSD,Brent)": ["AIR", "USDTRY_l1", "EURUSD_l1", "BRENT_l1"],
        "S5_HEPSİ": ["AIR", "own_cc_l1", "own_intra_l1", "XU100_cc_l1", "XU100_intra_l1", "own_gap_t", "XU100_gap_t", "TUR_l1", "EEM_l1", "ES_l1", "VIX_l1", "STOXX_l1", "SPX_l1", "USDTRY_l1", "EURUSD_l1", "BRENT_l1"],
        "S6_HEPSİ+JETS(2015+)": ["AIR", "own_cc_l1", "XU100_cc_l1", "own_gap_t", "XU100_gap_t", "TUR_l1", "EEM_l1", "ES_l1", "VIX_l1", "USDTRY_l1", "BRENT_l1", "JETS_l1"],
    }
    M = pd.concat([base, C], axis=1)
    for nm, cols in specs.items():
        for per, a, b in [("ALL", "2014-01-01", "2027"), ("IS", "2014-01-01", "2021-01-01"), ("OOS", "2021-01-01", "2027")]:
            y = d.intra[(d.index >= a) & (d.index < b)]
            r, n = ols_nw(y, M[cols])
            rows.append({"tgt": st, "spec": nm, "per": per, "coef": r.loc["AIR", "coef"], "t": r.loc["AIR", "t"], "n": n})
    # eşzamanlı (işlenemez) piyasa kontrolü: hisseye özgü mü?
    M2 = pd.concat([base, C, pd.DataFrame({"XU100_intra_t": X1.intra})], axis=1)
    for per, a, b in [("ALL", "2014-01-01", "2027"), ("IS", "2014-01-01", "2021-01-01"), ("OOS", "2021-01-01", "2027")]:
        y = d.intra[(d.index >= a) & (d.index < b)]
        r, n = ols_nw(y, M2[["AIR", "XU100_intra_t", "own_cc_l1", "XU100_cc_l1", "TUR_l1"]])
        rows.append({"tgt": st, "spec": "S7_+XU100_intra_t(eşzamanlı)", "per": per, "coef": r.loc["AIR", "coef"], "t": r.loc["AIR", "t"], "n": n})
R = pd.DataFrame(rows); R.to_csv(RES + "/v3_controls.csv", index=False)
print("\n== Ortak faktör kontrollü sürekli regresyon: intra_t ~ AIR + kontroller (std katsayı, NW-5 t) ==")
print(R.pivot_table(index=["tgt", "spec"], columns="per", values="t", sort=False).round(2).to_string())
print(R[R.per == "ALL"].pivot_table(index="spec", columns="tgt", values="coef", sort=False).round(4).to_string())

# ---------- kontrollü backtest: hedef = gün-içi artığı (XU100 eşzamanlı beta ile; hisseye özgü kısım) ve piyasa kısmı
print("\n== Ayrıştırma: brüt bps = beta*XU100 kısmı + hisseye özgü kısım ==")
for st in TGT:
    y = D[st].intra; m = X1.intra
    df = pd.concat([y.rename("y"), m.rename("m")], axis=1).dropna()
    b = (df.y.rolling(250, min_periods=120).cov(df.m) / df.m.rolling(250, min_periods=120).var()).shift(1)
    spec_ = df.y - b * df.m; mk = b * df.m
    for per in ["IS", "OOS", "ALL"]:
        a_ = bt(AIR, y, 0, 1.0, *PER[per]); s_ = bt(AIR, spec_, 0, 1.0, *PER[per]); k_ = bt(AIR, mk, 0, 1.0, *PER[per])
        print(f"{st} {per}: toplam brüt {a_['gross']:.1f} (t {a_['t_g']:.2f}) = piyasa {k_['gross']:.1f} (t {k_['t_g']:.2f}) + özgü {s_['gross']:.1f} (t {s_['t_g']:.2f})")

# ---------- alt dönemler
print("\n== Alt dönemler (8 bps net; brüt parantez) — hizalama C ve A ==")
rows = []
for st in TGT:
    for nm, s in [("C", AIR), ("A", AIRA)]:
        for per in ["14-17", "18-20", "21-23", "24-26", "IS", "OOS"]:
            r = bt(s, D[st].intra, 8, 1.0, *PER[per]); rows.append({"tgt": st, "sig": nm, "per": per, "n": r["n"], "bps": r["bps"], "t": r["t"], "gross": r["gross"]})
    # COVID hariç, 2020 hariç
    for nm, s in [("C", AIR), ("A", AIRA)]:
        y = D[st].intra
        y1 = y[~((y.index >= "2020-02-01") & (y.index < "2021-07-01"))]
        y2 = y[y.index.year != 2020]
        for lab, yy in [("noCOVID_IS", y1[y1.index < SPLIT]), ("noCOVID_ALL", y1), ("no2020_ALL", y2)]:
            r = bt(s, yy, 8, 1.0); rows.append({"tgt": st, "sig": nm, "per": lab, "n": r["n"], "bps": r["bps"], "t": r["t"], "gross": r["gross"]})
SP = pd.DataFrame(rows); SP.to_csv(RES + "/v3_subperiods.csv", index=False)
print(SP.pivot_table(index=["tgt", "sig"], columns="per", values="bps", sort=False).round(1).to_string())
print(SP.pivot_table(index=["tgt", "sig"], columns="per", values="t", sort=False).round(2).to_string())
print(SP.pivot_table(index=["tgt", "sig"], columns="per", values="n", sort=False).to_string())
# yıllar
print("\n== Yıllar (C, 8 bps net bps/işlem) ==")
yy = {}
for st in TGT:
    g, pos = pnl_series(AIR, D[st].intra); g = g[g.index >= "2014-01-01"] - 8e-4
    yy[st] = (1e4 * g.groupby(g.index.year).mean()).round(1)
    yy[st + "_n"] = g.groupby(g.index.year).size()
print(pd.DataFrame(yy).T.to_string())

# ---------- uç değer bağımlılığı
print("\n== Uç değer bağımlılığı (C, 8 bps; ALL / OOS) ==")
for st in TGT:
    g, pos = pnl_series(AIR, D[st].intra); g = g[g.index >= "2014-01-01"]
    for per, gg in [("ALL", g), ("OOS", g[g.index >= SPLIT]), ("IS", g[g.index < SPLIT])]:
        net = gg - 8e-4; n = len(net)
        def tt(x): return x.mean() / x.std() * np.sqrt(len(x))
        top = net.sort_values(ascending=False)
        d10 = top.iloc[10:]; d20 = top.iloc[20:]
        both = net.drop(top.index[:10]).drop(top.index[-10:])
        lo, hi = gg.quantile(.01), gg.quantile(.99); w = gg.clip(lo, hi) - 8e-4
        # hedefi winsorize (pozisyondan bağımsız): intraday'i %1/%99'da kırp
        y = D[st].intra; yw = y.clip(y.quantile(.01), y.quantile(.99))
        gw, _ = pnl_series(AIR, yw); gw = gw[gw.index >= "2014-01-01"]
        if per == "OOS": gw = gw[gw.index >= SPLIT]
        if per == "IS": gw = gw[gw.index < SPLIT]
        gw = gw - 8e-4
        hit = (gg > 0).mean(); from math import erf, sqrt
        z_hit = (hit - 0.5) / np.sqrt(0.25 / n)
        print(f"{st} {per}: n={n} net {1e4*net.mean():.1f} (t {tt(net):.2f}) | en iyi 10 çıkar {1e4*d10.mean():.1f} (t {tt(d10):.2f}) | en iyi 20 çıkar {1e4*d20.mean():.1f} (t {tt(d20):.2f}) | "
              f"en iyi+en kötü 10 çıkar {1e4*both.mean():.1f} (t {tt(both):.2f}) | hedef %1-99 winsor {1e4*gw.mean():.1f} (t {tt(gw):.2f}) | medyan brüt {1e4*gg.median():.1f} | isabet {hit:.3f} (z {z_hit:.2f})")
    g, pos = pnl_series(AIR, D[st].intra); g = g[g.index >= "2014-01-01"]
    print("   en iyi 10 gün:", [(str(i.date()), round(1e4 * v)) for i, v in g.sort_values(ascending=False).head(10).items()])

# ---------- uzun/kısa, düz günlere göre
print("\n== Uzun/kısa ayrımı (brüt gün-içi ortalama, bps) ==")
for st in TGT:
    df = pd.concat([AIR.rename("s"), D[st].intra.rename("y")], axis=1).dropna()
    for per, m in [("IS", df.index < SPLIT), ("OOS", df.index >= SPLIT)]:
        x = df[m]
        L = x.y[x.s > 1]; Sh = x.y[x.s < -1]; F = x.y[x.s.abs() <= 1]
        print(f"{st} {per}: uzun günler {1e4*L.mean():.1f} (n {len(L)}), kısa günler {1e4*Sh.mean():.1f} (n {len(Sh)}), düz {1e4*F.mean():.1f} (n {len(F)}) -> uzun-düz {1e4*(L.mean()-F.mean()):.1f}, düz-kısa {1e4*(F.mean()-Sh.mean()):.1f}")
