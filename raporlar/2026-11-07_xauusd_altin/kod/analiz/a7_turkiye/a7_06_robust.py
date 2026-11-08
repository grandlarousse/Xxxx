"""Sağlamlık: IS seçimli kural backtest'leri (aile a), aday ilişkilerin dışlama testleri, 2010-2016 erken dönem, yarım gün sızıntısı, USDTRY carry zamanlaması ayrıntısı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
import json
FAM = "e_robust"
reset_family(FAM)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
p, f = build()
r = p.v_ret
isx = p.index <= L.IS_END

# ---------- R1: aile (a) — yalnız IS'e göre seçim, OOS'ta tek değerlendirme ----------
A = pd.read_csv(f"{OUT}/a_ic_table.csv")
A = A[~A.K]  # kapanışta hesaplananları dışarıda bırak (temiz sürümler)
sel = A.reindex(A.t_is.abs().sort_values(ascending=False).index).head(3)
print("R1. IS |t| en yüksek 3 (öngörücü,h) — seçim yalnız IS t'ye göre:")
print(sel[["pred", "h", "ic_is", "t_is", "ic_oos", "t_oos"]].round(3).to_string(index=False))
R1 = []
for _, s in sel.iterrows():
    x = f[s.pred]; h = int(s.h)
    med = x[isx].median()
    pos = (np.sign(s.ic_is) * np.sign(x - med)).fillna(0)
    for cost in (5, 10):
        bs = L.bt_summary(pos, r, h, cost)
        lg = legs(pos, r, h, cost)
        R1.append(dict(pred=s.pred, h=h, cost=cost, IS_sh=bs["is"]["sharpe"], OOS_sh=bs["oos"]["sharpe"], OOS_sh_dm=bs["oos"]["sharpe_demeaned"],
                       full_sh=bs["full"]["sharpe"], full_dm=bs["full"]["sharpe_demeaned"], bh=bs["buyhold_sharpe_full"], long_oos=lg["long"]["oos"], short_oos=lg["short"]["oos"],
                       turnover=bs["full"]["turnover"]))
    a = L.backtest(pos[~isx], r[~isx], h, 5)
    L.register(AG, FAM, f"IS_selected_rule::{s.pred}", s.pred, h, dict(ic=s.ic_oos, t=a["t_daily"], n=a["n_days"], t_is=s.t_is, t_oos=a["t_daily"]), "IS'te seçilmiş ±1 kural, OOS net 5bps")
print(pd.DataFrame(R1).to_string(index=False))
bhs = {seg: L.backtest(pd.Series(1.0, index=r.index)[m], r[m], 1, 0)["sharpe"] for seg, m in [("IS", isx), ("OOS", ~isx)]}
print("buy&hold Sharpe IS/OOS:", {k: round(v, 2) for k, v in bhs.items()})

# ---------- R2: aday ilişkiler — dışlama testleri ----------
print("\nR2. Aday ilişkiler — dışlamalı IC (tam dönem)")
def roll_in(h):
    return sum((p.v_code.shift(-k) != p.v_code.shift(-k + 1)).astype(int) for k in range(1, h + 1)) > 0
tl_cris = ((p.index >= "2018-08-01") & (p.index <= "2018-09-30")) | ((p.index >= "2021-11-15") & (p.index <= "2022-01-15"))
hol = f.half_day | (f.gap > 0) | f.half_day.shift(-1, fill_value=False) | (f.gap.shift(-1, fill_value=0) > 0)
CANDS = [("usd_fut_l1", 3), ("goi_d1_l1", 3), ("goi_d1_l1", 1), ("xu_l1", 1), ("premz_l1", 5)]
rows = []
for nm, h in CANDS:
    y = f[f"fwd{h}"]; x = f[nm]
    base = ic(x, y, max(h, 5))
    out = dict(pred=nm, h=h, tam=f"{base['ic']:+.3f} ({base['t']:+.2f})")
    for lab, m in [("roll_yok", ~roll_in(h)), ("tatil/yarım_yok", ~hol), ("uç_yok", ~f.extreme), ("TLkriz_yok", ~tl_cris)]:
        q = ic(x[m], y[m], max(h, 5)); out[lab] = f"{q['ic']:+.3f} ({q['t']:+.2f})"
    out["placebo"] = placebo_lead(x, r, h)
    rows.append(out)
print(pd.DataFrame(rows).to_string(index=False))

# ---------- R3: erken dönem 2010-2016 (spot panel) ----------
print("\nR3. Erken dönem (spot panel, hedef sfwd = 15:00->15:00 spot). XU030 ve USDTRY Yahoo kapanışları t-1 (bilgi: t-1 akşamı).")
sp = L.load_spot()
xu_s = np.log(sp.y_XU030_IS).diff(); usd_s = np.log(sp.y_USDTRY_X).diff()
# aynı kapanış tekrarı (tatil) -> 0 fark; bunları NaN yap
xu_s = xu_s.where(xu_s != 0); usd_s = usd_s.where(usd_s != 0)
for nm, x in [("yahoo_xu030_1g", xu_s), ("yahoo_usdtry_1g", usd_s), ("yahoo_usdtry_3g", np.log(sp.y_USDTRY_X).diff(3))]:
    for h in (1, 3, 5):
        y = sp[f"sfwd{h}"]
        e = ic(x[:"2016-12-31"], y[:"2016-12-31"], max(h, 5)); l8 = ic(x["2017-03-01":], y["2017-03-01":], max(h, 5))
        print(f"  {nm:16s} h={h}: 2010-2016 IC {e['ic']:+.3f} (t {e['t']:+.2f}, n {e['n']}) | 2017+ IC {l8['ic']:+.3f} (t {l8['t']:+.2f})")
        L.register(AG, FAM, f"early::{nm}", nm, h, dict(ic=e["ic"], t=e["t"], n=e["n"], t_oos=l8["t"]), "2010-2016 spot panel; t_oos alanı=2017+ spot")
# TL şoku (erken dönem): |yahoo usdtry| > 2.5%
sh = usd_s.abs() > 0.025
for h in (3, 5):
    y = sp[f"sfwd{h}"]; e = (y[sh] - y.mean())[:"2016-12-31"].dropna()
    t = e.mean() / (e.std() / np.sqrt(len(e)))
    print(f"  TL şoku (Yahoo |Δ|>2.5%) 2010-2016 h={h}: n={len(e)} fazla {e.mean()*1e4:+.1f} bps t={t:+.2f}")
    L.register(AG, FAM, "early::TL_shock", "TL şoku Yahoo", h, dict(ic=np.nan, t=t, n=len(e)), "2010-2016 erken tekrar")

# ---------- R4: olay kümelenmesine dayanıklı kriz testi ----------
print("\nR4. Kriz şoku 'herhangi' — epizot kümelemeli t (10 iş günü içindeki olaylar tek epizot)")
sh_any = (f.usd_spot_1.abs() > 0.025) | (f.xu_l1 < -0.05)
idx = np.where(sh_any.values)[0]
ep = np.zeros(len(idx), int)
for k in range(1, len(idx)):
    ep[k] = ep[k - 1] + (idx[k] - idx[k - 1] > 10)
for h in (3, 5):
    y = f[f"fwd{h}"]
    e = pd.Series((y.iloc[idx] - y.mean()).values, index=p.index[idx])
    epm = e.groupby(ep).mean().dropna()
    t = epm.mean() / (epm.std() / np.sqrt(len(epm)))
    print(f"  h={h}: epizot sayısı {len(epm)}, epizot ort fazla {epm.mean()*1e4:+.1f} bps, t={t:+.2f}, negatif epizot oranı {(epm<0).mean():.2f}")
    L.register(AG, FAM, "crisis_any_clustered", "TL/XU030 şoku (epizot kümeli)", h, dict(ic=np.nan, t=t, n=len(epm)), "epizot ortalamaları")

# ---------- R5: yarım gün sızıntısı (bütün proje için uyarı) ----------
print("\nR5. Yarım gün sızıntısı: 15:00 UTC bilgisiyle kurulan sinyallerde yarım günler ileriye bakar")
mom = np.log(p.xau_p15 / p.xau_p07); mom2 = np.log(p.xau_p15 / p.xau_p12)
for nm, x in [("xau 07->15 UTC", mom), ("xau 12->15 UTC", mom2)]:
    a = ic(x, f.fwd1, 5); b = ic(x[~f.half_day], f.fwd1[~f.half_day], 5)
    print(f"  {nm}: tüm günler IC {a['ic']:+.4f} (t {a['t']:+.2f}) | yarım günler hariç IC {b['ic']:+.4f} (t {b['t']:+.2f}) | fark t {a['t']-b['t']:+.2f}")
    L.register(AG, FAM, f"diag_halfday_leak::{nm}", nm, 1, dict(ic=a["ic"], t=a["t"], n=a["n"], t_oos=b["t"]), "tanı: t_oos alanı = yarım günler hariç t")

# ---------- R6: USDTRY carry zamanlaması — ayrıntı ----------
print("\nR6. USDTRY vadeli carry zamanlaması (t-1): demeaned, bacaklar, 10 bps, yıl yıl, bileşenler, KKM günü")
lfx = np.log(p.dk_USDTRY_p15)
dte = p.vo_usdtry_dte.clip(lower=3)
basis_pd = np.log(p.vo_usdtry_settle / p.dk_USDTRY_p15) / dte
drift20 = lfx.diff().rolling(20).mean()
sig1 = (drift20 - basis_pd * 1.4).shift(1)
ur = p.vo_usdtry_ret
pos = np.sign(sig1).fillna(0)
for h in (1, 5):
    for cost in (5, 10):
        bs = L.bt_summary(pos, ur, h, cost); lg = legs(pos, ur, h, cost)
        print(f"  h={h} cost={cost}: tam {bs['full']['sharpe']} (dm {bs['full']['sharpe_demeaned']}), IS {bs['is']['sharpe']} (dm {bs['is']['sharpe_demeaned']}), OOS {bs['oos']['sharpe']} (dm {bs['oos']['sharpe_demeaned']}), "
              f"B&H(uzun USDTRY) {bs['buyhold_sharpe_full']}, uzun bacak {lg['long']}, kısa bacak {lg['short']}")
a = L.backtest(pos, ur, 1, 5)
yr = a["pnl"].groupby(a["pnl"].index.year).apply(lambda s: s.mean() / s.std() * np.sqrt(252))
print("  yıl yıl Sharpe (h=1, 5bps):", yr.round(2).to_dict())
print("  KKM 21.12.2021 günü pozisyon:", pos.loc["2021-12-21"], " getiri:", round(ur.loc["2021-12-21"] * 100, 2), "%")
ex = ~((p.index >= "2021-12-20") & (p.index <= "2021-12-24"))
b2 = L.backtest(pos[ex], ur[ex], 1, 5); print("  KKM haftası hariç tam Sharpe:", round(b2["sharpe"], 2))
for nm, s in [("yalnız sürüklenme (momentum)", drift20.shift(1)), ("yalnız -taşıma", (-basis_pd).shift(1))]:
    for h in (1, 5):
        st = test(FAM, f"usdtry_component::{nm}", s, fwd(ur, h), h, note="t-1")
        print(f"  {nm:28s} h={h}: {fmt(st)}")
# Bu sinyal ons altın VİOP'u öngörüyor mu? (çapraz kontrol)
for h in (1, 3, 5):
    st = test(FAM, "usdtry_carry_sig_l1->xau", sig1, f[f"fwd{h}"], h, note="t-1; ons altın hedef")
    print(f"  carry sinyali -> XAUUSD fwd{h}: {fmt(st)}")
# placebo ve dışlamalar (carry sinyali, USDTRY vadeli hedef)
print("  placebo (USDTRY vadeli hedef, h=1/5):", placebo_lead(sig1, ur, 1), placebo_lead(sig1, ur, 5))
for lab, m in [("TL krizleri hariç", ~tl_cris), ("uç dönemler hariç", ~f.extreme), ("roll yok (USDTRY kodu t+1..t+5 sabit)", ~(sum((p.vo_usdtry_code.shift(-k) != p.vo_usdtry_code.shift(-k + 1)).astype(int) for k in range(1, 6)) > 0)),
               ("yalnız 2023-06+", p.index >= "2023-06-01"), ("yalnız 2017-2021", p.index <= "2021-12-31")]:
    for h in (1, 5):
        q = ic(sig1[m], fwd(ur, h)[m], max(h, 5))
        print(f"  {lab:40s} h={h}: IC {q['ic']:+.3f} t {q['t']:+.2f} n {q['n']}")
