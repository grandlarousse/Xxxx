"""Aile (d): Yurt içi kriz günleri etrafında VİOP ons altın bazı, hacmi, gram primi ve sonrası getiriler."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
FAM = "d_crisis"
reset_family(FAM)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
p, f = build()
r = p.v_ret
EV = {  # ilk şok günü (VİOP günü); kaynak: veri (USDTRY/XU030 uç hareketleri) + bilinen olaylar
    "2018-08-10 TL krizi (Brunson)": "2018-08-10",
    "2021-03-22 TCMB başkanı görevden alındı": "2021-03-22",
    "2021-11-23 TL çöküşü": "2021-11-23",
    "2021-12-20 KKM (21.12 TL +%35)": "2021-12-21",
    "2023-02-07 deprem (XU030 -%7)": "2023-02-07",
    "2023-03 altın ithalat kotası/prim": "2023-03-01",
    "2023-05-15 seçim (XU030 -%10)": "2023-05-15",
    "2023-06-07 seçim sonrası devalüasyon": "2023-06-07",
    "2025-03-19 İmamoğlu gözaltısı": "2025-03-19",
    "2026-09-16 XU030 -%7,6": "2026-09-16",
}
volz = zs(np.log(p.v_volume), 20).shift(0)
xb = f.xbasis_dev_K * 1e4
pr = p.tr_prem_matched * 1e4
mu = {h: f[f"fwd{h}"].mean() for h in (1, 3, 5)}
rows = []
for nm, d in EV.items():
    d = pd.Timestamp(d)
    i = p.index.get_indexer([d], method="bfill")[0]; d = p.index[i]
    w = p.index[max(0, i - 5): i + 6]
    rows.append(dict(olay=nm, gun=d.date(), usdtry_spot_1g=f.usd_spot_1.iloc[i] * 100, xu030=p.vo_xu030_ret.iloc[i] * 100, xau_v_ret=r.iloc[i] * 100,
                     xau_basis_dev_bps=xb.iloc[i], xau_basis_dev_max_abs_pm5=xb.loc[w].abs().max(), normal_basis_abs=xb.abs().median(),
                     xau_volz=volz.iloc[i], prem_bps=pr.iloc[i], prem_chg_5g_bps=pr.iloc[min(i + 5, len(pr) - 1)] - pr.iloc[i - 1],
                     fwd1=(f.fwd1.iloc[i]) * 100, fwd3=f.fwd3.iloc[i] * 100, fwd5=f.fwd5.iloc[i] * 100))
E = pd.DataFrame(rows)
print("D1. Olay tablosu (yüzde; baz ve prim bps). fwd = olay günü uzlaşmasında gir, h gün sonra çık")
print(E.round(2).to_string(index=False)); E.round(3).to_csv(f"{OUT}/d1_event_table.csv", index=False)
print("olaylar ort fwd1/3/5 (%):", E[["fwd1", "fwd3", "fwd5"]].mean().round(2).to_dict(), " koşulsuz ort:", {h: round(mu[h] * 100, 2) for h in mu})

# D2: Sistematik şok tanımı (gün t 15:00 bilinebilir): |USDTRY spot 1g| > %2,5  ya da t-1 XU030 VİOP < -%5
sh_fx = (f.usd_spot_1.abs() > 0.025)
sh_xu = (f.xu_l1 < -0.05)
for nm, s in [("TL şoku |usd_spot_1|>2.5% (t 15:00)", sh_fx), ("XU030 VİOP t-1 < -5%", sh_xu), ("herhangi", sh_fx | sh_xu)]:
    print(f"\nD2. {nm}: olay sayısı {int(s.sum())}")
    for h in (1, 3, 5):
        y = f[f"fwd{h}"]; e = (y[s] - y.mean()).dropna()
        # örtüşen olaylar için kaba düzeltme: NW yerine olay-kümelenmesi göz ardı; t yaklaşık
        t = e.mean() / (e.std() / np.sqrt(len(e))) if len(e) > 2 else np.nan
        isn = e[e.index <= L.IS_END]; oon = e[e.index > L.IS_END]
        ti = isn.mean() / (isn.std() / np.sqrt(len(isn))) if len(isn) > 2 else np.nan
        to = oon.mean() / (oon.std() / np.sqrt(len(oon))) if len(oon) > 2 else np.nan
        print(f"   h={h}: fazla ort {e.mean()*1e4:+.1f} bps t={t:+.2f} (IS n={len(isn)} t={ti:+.2f}; OOS n={len(oon)} t={to:+.2f}), isabet {(y[s]>0).mean():.2f}")
        L.register(AG, FAM, f"shock::{nm}", nm, h, dict(ic=np.nan, t=t, n=len(e), t_is=ti, t_oos=to), "olay; drift düzeltilmiş ortalama")
# D3: baz sapması — şok günlerinde VİOP ons altın yurt içinde primli/iskontolu mu?
print("\nD3. VİOP XAUUSD baz sapması (bps) — şok günleri vs normal")
for nm, s in [("normal", ~(sh_fx | sh_xu)), ("TL şoku", sh_fx), ("XU030 şoku (t-1)", sh_xu)]:
    b = xb[s].dropna()
    print(f"   {nm:16s} n={len(b)} ort {b.mean():+.1f} |ort| {b.abs().mean():.1f} sd {b.std():.1f}")
# D4: baz sapması (t-1) öngörü gücü şok dönemlerinde (koşullu IC)
print("\nD4. Koşullu: xbasis_dev_l1 -> fwd1, son 20 günde TL şoku olan günlerde")
recent = (sh_fx | sh_xu).rolling(20, min_periods=1).max().astype(bool)
for h in (1, 3):
    st = test(FAM, "xbasis_dev_l1|kriz20g", f.xbasis_dev_l1.where(recent), f[f"fwd{h}"], h, note="kriz penceresi koşullu")
    print("   ", h, fmt(st))
# D5: gram altın primi kriz sonrası (TL şoku günü sonrası 5 ve 20 günde prim değişimi)
print("\nD5. TL şoku sonrası gram altın primi (bps)")
for k in (1, 5, 20):
    ch = (pr.shift(-k) - pr)[sh_fx].dropna()
    print(f"   +{k}g: ort {ch.mean():+.1f}, medyan {ch.median():+.1f}, n={len(ch)} (koşulsuz ort {(pr.shift(-k)-pr).mean():+.1f})")
