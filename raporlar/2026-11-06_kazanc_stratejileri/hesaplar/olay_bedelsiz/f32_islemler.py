"""Onceden belirlenmis islem kurallari (kapanistan kapanisa; tavan kilitli giris doldurulmaz -> ilk kilitsiz kapanis; taban kilitli cikis kaydirilir).
Maliyet: gidis-donus 25 bp. Ciktilar: sonuc/islem_*.csv, sonuc/islem_tablolar.md"""
import os, numpy as np, pandas as pd
import f20_es as E, f30_analiz as A
from f31_calistir import md, P, P2, T, I, H as HP
OUT = A.OUT
def kurallar():
    R = []
    for h in [1, 5, 10, 20, 60]:
        R.append((f"YK t0 -> +{h}g", lambda x: x.j_p1, (lambda hh: (lambda x, j: j + hh))(h)))
    R.append(("YK t0 -> hak-1", lambda x: x.j_p1, lambda x, j: x.j_hak - 1))
    R.append(("Basvuru t0 -> onay t0", lambda x: x.j_p2, lambda x, j: x.j_p3))
    R.append(("Basvuru t0 -> hak-1", lambda x: x.j_p2, lambda x, j: x.j_hak - 1))
    R.append(("Onay t0 -> hak-1", lambda x: x.j_p3, lambda x, j: x.j_hak - 1))
    R.append(("Onay t0 -> hak", lambda x: x.j_p3, lambda x, j: x.j_hak))
    for h in [5, 10, 20]:
        R.append((f"Onay t0 -> hak+{h}", lambda x: x.j_p3, (lambda hh: (lambda x, j: x.j_hak + hh))(h)))
    R.append(("Hak-1 -> hak", lambda x: x.j_hak - 1, lambda x, j: x.j_hak))
    for h in [5, 10, 20, 60]:
        R.append((f"Hak -> hak+{h}", lambda x: x.j_hak, (lambda hh: (lambda x, j: x.j_hak + hh))(h)))
    return R
def main():
    M = E.matrisler(); Hh = pd.read_pickle(f"{OUT}/H.pkl")
    for c in ["j_p1", "j_p2", "j_p3", "j_hak"]: Hh[c] = Hh[c].astype("float")
    def safe(f):
        def g(x, *a):
            v = f(x, *a)
            return None if (v is None or pd.isna(v)) else int(v)
        return g
    allT = []
    for ad, gf, cf in kurallar():
        Tt = A.islem(M, Hh, ad, safe(gf), safe(cf)); Tt = Tt[Tt.gun > 0]; allT.append(Tt)
    TT = pd.concat(allT, ignore_index=True)
    TT["oran_g"] = TT.oran.map(A.oran_grup)
    TT["boy_g"] = pd.cut(TT.pd_yuzdelik, [0, 1/3, 2/3, 1.0001], labels=["kucuk", "orta", "buyuk"]).astype(str)
    TT["donem"] = np.where(TT.yil >= 2024, "2024-26", np.where(TT.yil >= 2020, "2020-23", "2015-19"))
    TT.to_pickle(f"{OUT}/TT.pkl")
    S = {"genel": A.islem_ozet(TT)}
    for by in ["oran_g", "boy_g", "donem", "yil"]: S[by] = A.islem_ozet(TT, by)
    for k, v in S.items(): v.to_csv(f"{OUT}/islem_{k}.csv", index=False)
    # takvim-zamani portfoyu (dolabilir giris/cikis)
    ct = []
    for ad, g in TT.groupby("islem", sort=False):
        tr = [(r.kod, int(r.jg), int(r.j_out)) for r in g.itertuples() if pd.notna(r.jg) and r.jg < r.j_out]
        z = E.takvim_portfoy(M, tr); z["islem"] = ad; ct.append(z)
        for per, lo, hi in [("2024-26", "2024-01-01", "2026-12-31")]:
            tr2 = [(r.kod, int(r.jg), int(r.j_out)) for r in g.itertuples() if pd.notna(r.jg) and r.jg < r.j_out and str(r.giris) >= lo]
            z = E.takvim_portfoy(M, tr2); z["islem"] = ad + " [" + per + "]"; ct.append(z)
    CT = pd.DataFrame(ct); CT.to_csv(f"{OUT}/takvim_portfoy.csv", index=False)
    return TT, S, CT
if __name__ == "__main__":
    TT, S, CT = main()
    F = dict(ham_ort=P2, ham_med=P2, bhar_ort=P2, bhar_med=P2, t=T, isabet=HP, bhar_dol_ort=P2, bhar_dol_med=P2, t_dol=T, isabet_dol=HP,
             net_ham_dol_ort=P2, net_bhar_dol_ort=P2, net_bhar_dol_med=P2, p5=P, p95=P, N=I, N_dol=I, kilitli_giris_pay=HP, gun_med=lambda v: f"{v:.0f}")
    cols = ["islem", "N", "gun_med", "kilitli_giris_pay", "ham_ort", "bhar_ort", "bhar_med", "t", "isabet", "N_dol", "bhar_dol_ort", "bhar_dol_med", "t_dol", "isabet_dol", "net_bhar_dol_ort", "p5", "p95"]
    s = "# Islem tablolari (otomatik)\n\n## Genel\n\n" + md(S["genel"], cols, F)
    for by in ["oran_g", "boy_g", "donem"]:
        s += f"\n## {by}\n\n" + md(S[by], ["islem", by, "N", "bhar_dol_ort", "bhar_dol_med", "t_dol", "isabet_dol", "net_bhar_dol_ort"], F)
    s += "\n## Takvim-zamani portfoyu (XU100 fazlasi, dolabilir)\n\n" + md(CT, ["islem", "gun", "ort_poz", "gunluk_fazla", "t_nw", "gunluk_fazla_net", "t_nw_net", "yillik_fazla_net"],
          dict(gun=I, ort_poz=lambda v: f"{v:.1f}", gunluk_fazla=lambda v: f"{100*v:+.3f}%", t_nw=T, gunluk_fazla_net=lambda v: f"{100*v:+.3f}%", t_nw_net=T, yillik_fazla_net=P))
    open(f"{OUT}/islem_tablolar.md", "w").write(s); print(s[:6000])
