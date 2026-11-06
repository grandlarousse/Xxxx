"""Dalga bazında yakalama: seçilen kurallar her dalganın göreli log hareketinin ne kadarını aldı, girişte gecikme
(dipten ilk pozisyona gün), çıkışta gecikme (tepeden pozisyon kapanışına gün). Dalga özet istatistikleri."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER
from dalga import dalgalar
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 300)
P, R, sup = panel("2026-11-05")
C, NU = kume_getiri(R); rf, _ = rf_gunluk(C.index)
V = M.Veri(P, R, C, NU, rf, KUMELER)
W = dalgalar(V.RelD.where(V.elig).loc["2011-06-01":], D=0.15, esik=0.30)
W["ia"] = [V.cal.get_loc(d) for d in W.dip]; W["ib"] = [V.cal.get_loc(d) for d in W.tepe]
W = W[W.dip >= pd.Timestamp("2012-01-02")].reset_index(drop=True)
# dalga özetleri
print("Dalga sayısı:", len(W), "| yıllık:", W.groupby(W.dip.dt.year).size().to_dict())
print("küme başına:", W.groupby("kume").size().sort_values(ascending=False).to_dict())
print("medyan gün=%.0f, medyan göreli=%.2f, ort göreli=%.2f, medyan max6ay=%.2f" % (W.gun.median(), W.rel.median(), W.rel.mean(), W.max6ay.median()))
lR = np.log(V.Rel); dl = np.diff(lR, axis=0, prepend=np.nan)
# dalga içi pay: kümelerin toplam pozitif göreli hareketinin ne kadarı dalga günlerinde
inw = np.zeros_like(lR, bool); kidx = {c: i for i, c in enumerate(V.kumeler)}
for _, w in W.iterrows(): inw[w.ia + 1:w.ib + 1, kidx[w.kume]] = True
ok = V.elig & (V.yas >= 1); okd = ok.copy(); okd[:V.t0] = False
print("dalga günlerinin payı (küme-gün): %.2f ; bu günlerdeki toplam göreli log getiri=%.1f, dalga dışı=%.1f" % (
    inw[okd].mean(), np.nansum(dl[okd & inw]), np.nansum(dl[okd & ~inw])))
def pozisyon(kural):
    if kural.startswith("rot:"):
        _, skor, K, fr, a, m = kural.split(":")
        r, inv, to, We = M.rotasyon(V, skor, int(K), fr, a == "1", m == "1", False, 0, L=1, c=0.0025)
        return (We > 0).astype(float)
    _, g, x, f = kural.split(":")
    S = M.durum_makinesi(V, g, x, int(f)); Se = np.zeros_like(S, float); Se[2:] = S[:-2]; return Se
KR = {"A rot12 K3 M": "rot:r252:3:M:0:0", "B rot12 K3 M abs+mkt": "rot:r252:3:M:1:1", "D rot6 K3 M": "rot:r126:3:M:0:0",
      "E rs126|rstr10|f1": "olay:rs126:rstr10:1", "F rs63|tr15|f0": "olay:rs63:tr15:0", "G dm6|tr15|f1": "olay:dm6:tr15:1"}
pos = {ad: pozisyon(k) for ad, k in KR.items()}
rows = []
for _, w in W.iterrows():
    k = kidx[w.kume]; a, b = w.ia, w.ib; tot = lR[b, k] - lR[a, k]
    d = dict(kume=w.kume, dip=w.dip.date(), tepe=w.tepe.date(), gun=w.gun, rel=w.rel)
    for ad, Pz in pos.items():
        got = np.nansum(Pz[a + 1:b + 1, k] * dl[a + 1:b + 1, k]); d[ad] = got / tot
        on = np.where(Pz[a + 1:b + 1, k] > 0)[0]
        d[ad + "_gir"] = on[0] + 1 if len(on) else np.nan
        # tepeden sonra çıkış gecikmesi ve tepe sonrası verilen göreli
        if Pz[b, k] > 0:
            off = np.where(Pz[b + 1:, k] == 0)[0]; e = b + 1 + off[0] if len(off) else len(V.cal) - 1
            d[ad + "_cik"] = e - b; d[ad + "_geri"] = np.exp(np.nansum(dl[b + 1:e + 1, k])) - 1
        else:
            d[ad + "_cik"] = np.nan; d[ad + "_geri"] = np.nan
    rows.append(d)
Y = pd.DataFrame(rows); Y.to_csv(os.path.join(OUT, "dalga_yakalama.csv"), index=False, float_format="%.3f")
ozet = pd.DataFrame({ad: {"yakalama_ort": Y[ad].mean(), "yakalama_med": Y[ad].median(), "hic_girmedi": Y[ad + "_gir"].isna().mean(),
                          "giris_gecikme_med_gun": Y[ad + "_gir"].median(), "tepede_icerde": Y[ad + "_cik"].notna().mean(),
                          "cikis_gecikme_med_gun": Y[ad + "_cik"].median(), "tepe_sonrasi_geri_verilen_med": Y[ad + "_geri"].median(),
                          "yakalama_ort_2024+": Y[pd.to_datetime(Y.dip) >= "2024-01-01"][ad].mean(),
                          "buyuk_dalga(rel>=%60)_yakalama": Y[Y.rel >= 0.6][ad].mean()} for ad in KR})
print(ozet.round(3).to_string())
ozet.to_csv(os.path.join(OUT, "dalga_yakalama_ozet.csv"), float_format="%.4f")
sec = Y[(pd.to_datetime(Y.dip) >= "2022-01-01") | (Y.rel >= 1.0)]
print(sec[["kume", "dip", "tepe", "gun", "rel"] + list(KR)].round(2).to_string(index=False))
# sızıntı: pozisyonun dalga içi kazancı vs dalga dışı kaybı (göreli log, küme-gün toplamı; slot sınırı yok)
rows = []
for ad, Pz in pos.items():
    m = okd & np.isfinite(dl)
    gi = np.nansum((Pz * dl)[m & inw]); go = np.nansum((Pz * dl)[m & ~inw])
    rows.append(dict(kural=ad, dalga_ici_kazanc=gi, dalga_ici_pay=gi / np.nansum(dl[m & inw]), dalga_disi=go,
                     dalga_disi_pay=go / np.nansum(dl[m & ~inw]), net=gi + go, pozisyon_gunu_payi=Pz[m].mean(),
                     pozisyonda_dalga_gunu_orani=(Pz[m & inw].sum() / Pz[m].sum())))
L = pd.DataFrame(rows).set_index("kural"); print(L.round(3).to_string()); L.to_csv(os.path.join(OUT, "dalga_sizinti.csv"), float_format="%.4f")
