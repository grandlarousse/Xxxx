"""Nakit temettu: islem kurallari (onceden belirlenmis), verim kovasi DUYURU fiyatina gore (ileriye bakis yok):
 verim_duyuru = verim_hak * P(hak-1)/P(t0-1)  [P duzeltilmis; temettu hak gunune kadar duzeltmeyi etkilemez].
Kurallar: (a) Duyuru t0 -> hak-1 (temettu ALINMAZ; saf fiyat), (b) Duyuru t0 -> hak (temettu alinir; brut), (c) hak-10 -> hak-1
(hak gunu genel kurul/YK kararinda ilan edildiginden onceden bilinir; yine de 'kosullu'), (d) hak -> hak+5.
Kilit: HisseTekil olan hisselerde tavan kilitli giris atlanir/kaydirilir; ChartData-only hisselerde kilit bilgisi yok."""
import os, numpy as np, pandas as pd
import f20_es as E
from f31_calistir import md, P2, T, I, H as HP
OUT = f"{E.CACHE}/sonuc"; COST = 0.0025
M = E.matrisler(); cal = M["cal"]
tm = pd.read_pickle(f"{E.CACHE}/olaylar_temettu.pkl"); tm = tm[(tm.hak >= "2015-01-01") & (tm.verim > 0) & (tm.verim < 0.5)]
rec = []
for _, e in tm.iterrows():
    k = e.kod
    if k not in M["R"].columns: continue
    jh = E.day_idx(cal, e.hak); jp = E.t0_idx(cal, e.p1) if pd.notna(e.p1) else None
    if jh is None or jh < 15 or jh >= len(cal): continue
    r = M["R"][k]
    vd = np.nan
    if jp is not None and jp < jh:
        g = r.iloc[jp:jh]                         # t0..hak-1 (duyuru gunu dahil)
        if not g.isna().any(): vd = e.verim * float(np.prod(1 + g))
    for ad, ji, jo in [("Duyuru t0 -> hak-1", jp, jh - 1), ("Duyuru t0 -> hak", jp, jh), ("hak-10 -> hak-1", jh - 10, jh - 1), ("hak-1 -> hak", jh - 1, jh), ("hak -> hak+5", jh, jh + 5)]:
        if ji is None or jo is None or jo <= ji or jo >= len(cal): continue
        jg, gec = E.dolabilir_giris(M, k, ji, 5)
        if jg is None or jg >= jo: continue
        ham, xu = E.bhar(M, k, jg, jo)
        if pd.isna(ham): continue
        rec.append(dict(islem=ad, kod=k, giris=cal[jg], yil=e.hak.year, verim_hak=e.verim, verim_duyuru=vd, gun=jo - jg, ham=ham, bhar=ham - xu,
                        kilit_bilgisi=k in M["VWR"].columns, jg=jg, jo=jo))
D = pd.DataFrame(rec)
D["vgrp"] = pd.cut(D.verim_duyuru.fillna(D.verim_hak), [0, 0.02, 0.05, 1], labels=["<%2", "%2-5", ">=%5"]).astype(str)
D["donem"] = np.where(D.yil >= 2024, "2024-26", "2015-23")
rows = []
for kk, g in D.groupby(["islem", "vgrp", "donem"], sort=False):
    z = E.ozet(g.bhar, g.giris); rows.append(dict(islem=kk[0], verim=kk[1], donem=kk[2], N=z["N"], gun_med=g.gun.median(), bhar_ort=z["ort"], bhar_med=z["med"], t=z["t"],
                                                  isabet=z["isabet"], net_bhar=z["ort"] - COST, ham_ort=g.ham.mean()))
for kk, g in D.groupby(["islem", "vgrp"], sort=False):
    z = E.ozet(g.bhar, g.giris); rows.append(dict(islem=kk[0], verim=kk[1], donem="tum", N=z["N"], gun_med=g.gun.median(), bhar_ort=z["ort"], bhar_med=z["med"], t=z["t"],
                                                  isabet=z["isabet"], net_bhar=z["ort"] - COST, ham_ort=g.ham.mean()))
S = pd.DataFrame(rows).sort_values(["islem", "verim", "donem"])
ct = []
for (ad, v), g in D.groupby(["islem", "vgrp"]):
    if v != ">=%5": continue
    for per, m in [("tum", g.yil > 0), ("2024-26", g.yil >= 2024)]:
        z = E.takvim_portfoy(M, [(r.kod, int(r.jg), int(r.jo)) for r in g[m].itertuples()]); z.update(islem=ad, donem=per); ct.append(z)
CT = pd.DataFrame(ct)
s = "# Temettu islemleri (otomatik)\n\n" + md(S, ["islem", "verim", "donem", "N", "gun_med", "ham_ort", "bhar_ort", "bhar_med", "t", "isabet", "net_bhar"],
                                             dict(N=I, gun_med=lambda v: f"{v:.0f}", ham_ort=P2, bhar_ort=P2, bhar_med=P2, t=T, isabet=HP, net_bhar=P2))
s += "\n## Takvim-zamani (verim>=%5)\n\n" + md(CT, ["islem", "donem", "gun", "ort_poz", "gunluk_fazla", "t_nw", "gunluk_fazla_net", "t_nw_net", "yillik_fazla_net"],
                                            dict(gun=I, ort_poz=lambda v: f"{v:.1f}", gunluk_fazla=lambda v: f"{100*v:+.3f}%", t_nw=T, gunluk_fazla_net=lambda v: f"{100*v:+.3f}%", t_nw_net=T, yillik_fazla_net=lambda v: f"{100*v:+.1f}%"))
s += f"\nKilit bilgisi olan islem payi: {D.kilit_bilgisi.mean():.0%}\n"
open(f"{OUT}/temettu_islem.md", "w").write(s); print(s)
