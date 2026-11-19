#!/usr/bin/env python3
"""Sonradan eklenen (post hoc) sağlamlık kontrolleri — ana ajan tarafından.

Neden: M0'da geriye kurulan sipariş birikimi 1990 öncesinde güvenilmez çıktı (1987 öncesi <= 0).
Bu yüzden birikime dayanmayan bir sipariş göstergesi (sipariş/teslimat oranı) ve Y1 sonucunun
tek tek yıllara ve erken döneme duyarlılığı ayrıca sınandı. Bu kontroller önceden belirlenmiş
planın parçası DEĞİLDİR; raporda öyle etiketlenir.

Kullanım: python3 hesap/02b_ek_kontrol.py   (02_analiz.py'yi içe çalıştırır, ~5 sn)
Çıktı  : hesap/sonuclar_ek.md
"""
import pathlib
import runpy

import numpy as np
import pandas as pd
import statsmodels.api as sm

KOK = pathlib.Path(__file__).resolve().parent.parent
g = runpy.run_path(str(KOK / "hesap" / "02_analiz.py"))
dl, dxy, ctrl_ii, ctrl_iii = g["dl"], g["dlnY_dxy"], g["ctrl_ii"], g["ctrl_iii"]
Dtot, Otot, LN10 = g["Dtot"], g["Otot"], g["LN10"]
assert abs(LN10 - np.log(1.1)) < 1e-12

out = ["# Sonradan eklenen sağlamlık kontrolleri (post hoc)\n",
       "Bu tablolar önceden belirlenmiş planın dışında, veri kalitesi sorunu görüldükten sonra eklendi. "
       "Hüküm verirken ana tablolarla birlikte ve temkinle okunmalı.\n"]

# (a) Y6: sipariş/teslimat oranı (book-to-bill), birikim gerektirmez
y6 = (Otot / Dtot).loc[1974:2025]
rows = []
for ad, cf in {"(i) kontrolsüz": None, "(ii) +resesyon+imalat": ctrl_ii(), "(iii) +olay yılı": ctrl_iii()}.items():
    r = dl(y6, dxy, 3, cf, 3, level=True)
    rows.append([ad, "1975-2025", r["n"], r["toplam"] * LN10, r["ga"][0] * LN10, r["ga"][1] * LN10, r["wald_p"], r["r2"]])
for lab, (a, b) in {"1978-1999": (1978, 1999), "2000-2025": (2000, 2025), "1986-2025": (1986, 2025)}.items():
    r = dl(y6[(y6.index >= a) & (y6.index <= b)], dxy, 3, ctrl_ii(), 3, level=True)
    rows.append(["(ii) +resesyon+imalat", lab, r["n"], r["toplam"] * LN10, r["ga"][0] * LN10, r["ga"][1] * LN10, r["wald_p"], r["r2"]])
t = pd.DataFrame(rows, columns=["varyant", "dönem", "n", "DXY +%10 etkisi (oran puanı)", "GA alt", "GA üst", "Wald p", "R2"])
out.append("## (a) Y6: toplam net sipariş / toplam teslimat (düzey)\n")
out.append(f"Ortalama oran {y6.mean():.2f}, medyan {y6.median():.2f} (1974-2025).\n")
out.append(t.round(3).to_markdown(index=False) + "\n")

# (b) Y1 (ii): erken dönem hariç ve t-dağılımı ile
y1 = np.log(Dtot.loc[:2025]).diff()
rows = []
for lab, (a, b) in {"1975-2025 (ana)": (1975, 2025), "1986-2025": (1986, 2025), "1990-2025": (1990, 2025)}.items():
    r = dl(y1[(y1.index >= a) & (y1.index <= b)], dxy, 3, ctrl_ii(), 3)
    rows.append([lab, r["n"], r["etki10"], r["etki10_ga"][0], r["etki10_ga"][1], r["wald_p"]])
t = pd.DataFrame(rows, columns=["dönem", "n", "DXY +%10 etkisi (%)", "GA alt", "GA üst", "Wald p"])
out.append("## (b) Y1 toplam teslimat, varyant (ii): başlangıç yılına duyarlılık\n")
out.append(t.round(3).to_markdown(index=False) + "\n")

# küçük örneklem: HAC + t dağılımı (n-k serbestlik derecesi)
df = pd.DataFrame({"y": y1})
for k in range(4):
    df[f"L{k}"] = dxy.shift(k)
df = df.join(ctrl_ii(), how="left").dropna()
X = sm.add_constant(df.drop(columns="y"))
res = sm.OLS(df["y"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3, "use_correction": True}, use_t=True)
Rv = np.array([1.0 if c.startswith("L") else 0.0 for c in X.columns])
tt = res.t_test(Rv)
out.append(f"Küçük örneklem düzeltmeli HAC ve t dağılımıyla Y1 (ii): toplam b = {float(tt.effect[0]):.3f}, "
           f"p = {float(tt.pvalue):.3f}, n = {int(res.nobs)}.\n")
res0 = sm.OLS(df["y"], X).fit()
tt0 = res0.t_test(Rv)
out.append(f"Klasik OLS standart hatasıyla: p = {float(tt0.pvalue):.3f}.\n")

# (c) birer yıl dışarıda bırakma
rows = []
for yil in df.index:
    d2 = df.drop(index=yil)
    r2 = sm.OLS(d2["y"], sm.add_constant(d2.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    tot = float(r2.params[[f"L{k}" for k in range(4)]].sum())
    rows.append([yil, (np.exp(tot * LN10) - 1) * 100, float(r2.t_test(Rv).pvalue)])
loo = pd.DataFrame(rows, columns=["dışarıda bırakılan yıl", "etki", "p"])
out.append("## (c) Y1 (ii): birer yıl dışarıda bırakınca DXY +%10 etkisi\n")
out.append(f"Aralık {loo.etki.min():.1f}% .. {loo.etki.max():.1f}%; p < 0,05 kalan: {(loo.p < 0.05).sum()}/{len(loo)}; "
           f"p < 0,10 kalan: {(loo.p < 0.10).sum()}/{len(loo)}.\n")
uc = pd.concat([loo.nsmallest(3, "etki"), loo.nlargest(3, "etki")])
out.append("En etkili yıllar:\n\n" + uc.round(3).to_markdown(index=False) + "\n")

# (d) özet tablo: rapora girecek sayılar tek yerden üretilir (elle aktarma hatasını önlemek için)
R = g["R"]
def f1(v): return f"{v:+.1f}".replace(".", ",")
def f2(v): return f"{v:+.2f}".replace(".", ",")
def fp(p): return "<0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")
def satir(ad, donem, r, birim="%"):
    return [ad, donem, r["n"], f1(r["etki10"]) + " " + birim, f"[{f1(r['etki10_ga'][0])}; {f1(r['etki10_ga'][1])}]", fp(r["wald_p"])]
def alt(key):  # M1_alt etki GA'sını toplam b GA'sından hesapla
    r = dict(R["M1_alt"][key]); lo, hi = r["ga"]
    r["etki10_ga"] = [(np.exp(lo * LN10) - 1) * 100, (np.exp(hi * LN10) - 1) * 100]
    return r
ii = "(ii) +resesyon+imalat"
oz = [satir("Toplam teslimat (Airbus+Boeing)", "1975-2025", R["M1"][f"Y1 dln toplam teslimat|{ii}"]),
      satir("", "2000-2025", alt("Y1|2000-2025")),
      satir("Airbus teslimat", "1975-2025", R["M1"][f"Y2 dln Airbus teslimat|{ii}"]),
      satir("", "2000-2025", alt("Y2|2000-2025")),
      satir("Boeing teslimat", "1975-2025", R["M1"][f"Y3 dln Boeing teslimat|{ii}"]),
      satir("", "2000-2025", alt("Y3|2000-2025")),
      satir("ABD uçak ve parça üretimi (çeyreklik)", "1973-2026", R["M2"]["ABD G336411T3|1973Q1-2026Q3"]),
      satir("", "2000-2026", R["M2"]["ABD G336411T3|2000Q1-2026Q3"]),
      satir("Birikim/teslimat oranı (bekleme süresi)", "2000-2025", alt("Y4|2000-2025"))]
r86 = dl(y1[(y1.index >= 1986) & (y1.index <= 2025)], dxy, 3, ctrl_ii(), 3)
oz.insert(1, satir("", "1986-2025 (sonradan)", r86))
for lab, (a, b) in {"1975-2025 (sonradan)": (1975, 2025), "2000-2025 (sonradan)": (2000, 2025)}.items():
    r = dl(y6[(y6.index >= a) & (y6.index <= b)], dxy, 3, ctrl_ii(), 3, level=True)
    oz.append(["Sipariş/teslimat oranı (ort. 1,47)" if a == 1975 else "", lab, r["n"], f2(r["toplam"] * LN10) + " puan",
               f"[{f2(r['ga'][0] * LN10)}; {f2(r['ga'][1] * LN10)}]", fp(r["wald_p"])])
ozt = pd.DataFrame(oz, columns=["Gösterge", "Dönem", "n", "DXY +%10 sonrası toplam etki", "%95 güven aralığı", "p"])
out.append("## (d) Özet tablo (rapor için)\n")
out.append(ozt.to_markdown(index=False) + "\n")

# (e) G10: dolar ve sipariş/teslimat oranı
plt = g["plt"]; fig = g["fig_"](5.6); a1, a2 = fig.subplots(2, 1, sharex=True)
x1 = g["DXYy"].loc[1975:2025]; a1.plot(x1.index, x1.values, color=g["BLUE"], lw=1.8); a1.set_ylabel("DXY, yıllık ort.")
a1.set_title("Dolar endeksi (DXY)", loc="left", fontsize=9.5, fontweight="semibold")
yy = y6.loc[1975:2025]
a2.bar(yy.index, yy.values, color=g["ORNG"], width=0.75)
a2.axhline(1.0, color="#333333", lw=0.9)
a2.set_title("Net sipariş / teslimat oranı (Airbus + Boeing); yatay çizgi: sipariş = teslimat", loc="left", fontsize=9.5, fontweight="semibold")
a2.set_ylabel("Oran"); a2.set_xlim(1974.3, 2025.7)
g["finish"](fig, "Dolar endeksi ve uçak siparişleri, 1975-2025",
            "Kaynak: Yahoo Finance (DXY); Airbus-Boeing net sipariş ve teslimat (Wikipedia). Oran 1'in üstündeyse sipariş defteri büyür.")
g["save"](fig, "G10_dxy_siparis.png")

(KOK / "hesap" / "sonuclar_ek.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[-3:]))
