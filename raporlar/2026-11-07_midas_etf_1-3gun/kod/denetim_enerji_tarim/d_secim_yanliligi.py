"""Denetim: genel tarama seçim yanlılığı.
(1) MR_bb20_alt C1 h2 tüm evrende (yalnız USO'ya özgü mü?)
(2) Ailede 'IS'e göre seç, OOS'ta bak' yürüyüşü: IS t'sine göre en iyi satırların OOS ortalaması.
(3) USO MR_bb20_alt C1 h2'nin yalnız IS'e göre sıralamadaki yeri.
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_secim_yanliligi.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D

pd.set_option("display.width", 250)
g = pd.read_csv(os.path.join(D.ROOT, "sonuclar", "genel_tum.csv"))
fam = pd.read_csv(os.path.join(D.ROOT, "sonuclar", "aile_enerji_tarim", "genel_aile.csv"))
print("genel_tum satır:", len(g), "| aile satır:", len(fam), "| aile ETF:", fam["sym"].nunique(), "| sinyal:", fam["sig"].nunique(), "| exit türleri:", fam["exit"].unique())

# (1) MR_bb20_alt C1 h2 evrende
x = g[(g["sig"] == "MR_bb20_alt") & (g["mode"] == "C1") & (g["h"] == 2) & (g["exit"] == "sabit")]
print("\n(1) MR_bb20_alt C1 h2 sabit, kategori bazında: ETF sayısı, ort net bp, t>2 olan oranı, ort t")
print(x.groupby("cat").agg(n_etf=("sym", "size"), ort_net=("mean_net_bp", "mean"), ort_t=("t", "mean"), t_gt2=("t", lambda v: (v > 2).mean())).round(2).to_string())
print("Evren geneli: ort t %.2f, t>2 oranı %.3f, t<-2 oranı %.3f (n=%d)" % (x["t"].mean(), (x["t"] > 2).mean(), (x["t"] < -2).mean(), len(x)))
print("Diğer modlar (USO):"); print(g[(g.sym == "USO") & (g.sig == "MR_bb20_alt")][["mode", "h", "exit", "n", "mean_net_bp", "t", "is_t", "oos_t"]].round(2).to_string(index=False))

# (2) seç-IS / bak-OOS yürüyüşü (aile, sabit çıkış, n>=40)
f = fam[(fam["n"] >= 40)].copy()
f = f[np.isfinite(f["is_t"]) & np.isfinite(f["oos_net_bp"])]
print(f"\n(2) Ailede IS'e göre seçim (n>=40 satır: {len(f)})")
for top in (10, 25, 50, 100):
    s = f.nlargest(top, "is_t")
    print(f"  IS t'ye göre en iyi {top}: IS ort net {s['is_net_bp'].mean():.1f} bp, OOS ort net {s['oos_net_bp'].mean():.1f} bp, OOS>0 oranı {(s['oos_net_bp']>0).mean():.2f}, OOS ort t {s['oos_t'].mean():.2f}")
print(f"  Tüm satırlar: OOS ort net {f['oos_net_bp'].mean():.1f} bp, OOS>0 oranı {(f['oos_net_bp']>0).mean():.2f}")
print("  Corr(IS t, OOS t) = %.3f (Spearman %.3f)" % (f["is_t"].corr(f["oos_t"]), f["is_t"].corr(f["oos_t"], method="spearman")))
# (3) USO satırının IS sırası
r = f.assign(rk=f["is_t"].rank(ascending=False))
row = r[(r.sym == "USO") & (r.sig == "MR_bb20_alt") & (r["mode"] == "C1") & (r.h == 2) & (r["exit"] == "sabit")]
print("\n(3) USO MR_bb20_alt C1 h2 IS t sırası:", row[["is_t", "rk"]].to_dict("records"), "/", len(f))
# Tüm sinyal için OOS t'ye göre en iyiler arasında petrol kümesi yoğunluğu
oil = ["USO", "BNO", "USL", "DBO", "UCO", "UGA"]
best = fam.nlargest(30, "t"); print("  Tam örneklem t'ye göre en iyi 30 satırın petrol kümesinden olanı:", int(best["sym"].isin(oil).sum()))
# Bonferroni/BH: aile satırları + aileye özel
p1 = fam["p1"].to_numpy() if "p1" in fam else None
if p1 is not None:
    ok = np.isfinite(p1)
    print("  Aile genel satırlarında tek yönlü BH(q=0,10) geçen:", int(D.bh(p1[ok]).sum()), "/", ok.sum(), "| en küçük p1:", np.nanmin(p1))
