"""Madde 3 sade sagleme: sabit etkisiz ham tablolar (sinyal sonrasi 1 gunluk getiri vs diger butun gunler).
Ayrica veri/sonuc/yeniden_kodlama.csv son halini yazar. Yalniz kod/yeniden_kodlama.py'ye dayanir."""
import os
import sys
import types
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yeniden_kodlama as yk

KOK = yk.KOK
ayar = types.SimpleNamespace(fiyat="bolunmemis", f3="ge3", maske="acik", bozuk="kesin", ciro="dahil", son12="p3")
s, TR, araclar, ct = yk.calistir(ayar)

# --- son sonuc dosyasi ---
kor = pd.read_csv(os.path.join(KOK, "veri", "sonuc", "yeniden_kodlama_kor.csv"))
son = s.copy()
son = son.merge(kor[["test_id", "n_islem", "alfa_bps"]].rename(columns={"n_islem": "kor_n_islem", "alfa_bps": "kor_alfa_bps"}),
                on="test_id", how="left")
hedef = pd.read_csv(os.path.join(KOK, "veri", "sonuc", "BIRLESIK_sonuc.csv"))[["test_id", "n_islem", "alfa_bps", "t_kume", "q_bh", "etiket"]]
hedef = hedef.rename(columns={"n_islem": "hedef_n_islem", "alfa_bps": "hedef_alfa_bps", "t_kume": "hedef_t_kume"})
son = son.merge(hedef, on="test_id", how="left")
son["fark_n_yuzde"] = (son.n_islem / son.hedef_n_islem - 1) * 100
son["fark_alfa_bps"] = son.alfa_bps - son.hedef_alfa_bps
ok = (son.fark_n_yuzde.abs() <= 1) & (son.fark_alfa_bps.abs() <= 1)
son["karar"] = np.where(ok, "TUTTU", "TUTMADI")
son["fark_nedeni"] = np.where(ok, "yok (kor turda birebir)", "incele")
ilk = ["test_id", "n_islem", "alfa_bps", "t_kume", "alfa_P1", "alfa_P2", "alfa_P3", "alfa_son12", "kor_n_islem",
       "kor_alfa_bps", "hedef_n_islem", "hedef_alfa_bps", "hedef_t_kume", "fark_n_yuzde", "fark_alfa_bps", "karar", "fark_nedeni"]
son = son[ilk + [c for c in son.columns if c not in ilk]]
son.round(4).to_csv(os.path.join(KOK, "veri", "sonuc", "yeniden_kodlama.csv"), index=False)

# --- sade tablolar ---
def fwd_tablo(kodlar, tr):
    """Her arac icin tum gunlerin 1 gunluk ileri getirisi; sinyal gunu = islem giris gunu."""
    satir = []
    for k in kodlar:
        a = araclar[k]
        f = (a.df["AClose"].shift(-1) / a.df["AClose"] - 1) * 1e4
        d = pd.DataFrame({"kod": k, "tarih": a.idx, "f": f.values}).dropna()
        d = d[d.tarih >= pd.Timestamp("2010-01-01")]
        g = set(tr.loc[tr.kod == k, "giris"])
        d["sinyal"] = d.tarih.isin(g)
        satir.append(d)
    return pd.concat(satir)


def tablo(d, anahtar):
    g = d.groupby([anahtar, "sinyal"])["f"].agg(["mean", "count"]).unstack()
    out = pd.DataFrame({
        "sinyal_ort_bps": g[("mean", True)], "sinyal_n": g[("count", True)].fillna(0).astype(int),
        "diger_ort_bps": g[("mean", False)], "diger_n": g[("count", False)].astype(int)})
    out["fark_bps"] = out.sinyal_ort_bps - out.diger_ort_bps
    return out


def md(df):
    df = df.round(1)
    cols = [str(c) for c in df.reset_index().columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.reset_index().iterrows():
        lines.append("| " + " | ".join(str(x) for x in r.values) + " |")
    return "\n".join(lines)


parcalar = []
for ad, kodlar, tid in [("F1a_T (IBS < 0,2)", yk.T_EVREN, "F1a_T_h1"), ("F3_T (3+ dusuk kapanis)", yk.T_EVREN, "F3_T_h1"),
                        ("F11a (^SOX <= -%3 -> SMH)", ["SMH"], "F11a_SMH_h1")]:
    d = fwd_tablo(kodlar, TR[tid])
    d["yil"] = d.tarih.dt.year
    ta = tablo(d, "kod")
    ty = tablo(d, "yil")
    toplam = tablo(d.assign(hepsi="toplam"), "hepsi")
    poz = int((ty.fark_bps > 0).sum())
    nyil = int(ty.sinyal_n.gt(0).sum())
    parcalar.append(f"### {ad}\n\nArac arac (2010-2026, sinyal gunu sonrasi 1 gunluk ortalama getiri vs diger butun gunler):\n\n"
                    f"{md(pd.concat([ta, toplam]))}\n\nYil yil (araclar havuzlanmis):\n\n{md(ty)}\n\n"
                    f"Farkin pozitif oldugu yil: **{poz} / {nyil}** (sinyal olan yillar). "
                    f"Sinyal gunu ortalamasinin kendisi pozitif olan yil: {int((ty.sinyal_ort_bps > 0).sum())} / {nyil}.\n")
yol = os.path.join(KOK, "veri", "sonuc", "yeniden_kodlama_sade.md")
open(yol, "w").write("\n".join(parcalar))
print(son[["test_id", "n_islem", "alfa_bps", "t_kume", "hedef_n_islem", "hedef_alfa_bps", "fark_n_yuzde", "fark_alfa_bps", "karar"]].round(2).to_string(index=False))
print(yol)
