# -*- coding: utf-8 -*-
"""ek2_ortak_RF1b.py - YONTEM Ek 2 (muzayede maliyet senaryosu) icin ortak yardimcilar (gorev RF1b).
Aile betikleri (ek2_K4a/K4b/K5/K6/K9.py) bunlari kullanir. motor.py / yukle.py degistirilmez."""
import math
import os

import numpy as np
import pandas as pd

import motor as M

SCR = "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2"
os.makedirs(SCR, exist_ok=True)
VERI = M.VERI_DIZIN
F_ADAY = os.path.join(VERI, "aday_ek2_RF1b.csv")
F_SONUC = os.path.join(VERI, "sonuc_ek2_RF1b.csv")
KOMS = ("hisse", "muzayede")


def t_karar(row, cok):
    return row["t_kume"] if cok else row["t_olcekli"]


def alt_ozet(m, isl, kom, mask):
    """motorun kendi _ozet islevi ile islem listesinin bir alt kumesi (ayni t tanimlari)."""
    mask = np.asarray(mask, bool)
    tpos = isl["t_pos"].to_numpy()
    net = isl["net_" + kom].to_numpy()
    o = m._ozet(net[mask], isl["brut"].to_numpy()[mask], (net - isl["islemmal_" + kom].to_numpy())[mask],
                isl["anormal"].to_numpy()[mask], isl["olcekli_" + kom].to_numpy()[mask], tpos[mask],
                isl["yon"].to_numpy()[mask], isl["bolum"].to_numpy()[mask],
                (m.idx.year * 12 + m.idx.month).to_numpy()[tpos][mask], m.idx.year.to_numpy()[tpos][mask],
                np.abs(isl["beta"].to_numpy(float))[mask])
    o.pop("_yil_n", None)
    return o


def donem_isl_maskesi(m, isl, donem):
    return M.donem_maskesi(m.idx, donem)[isl["t_pos"].to_numpy()]


def ayrinti(m, isl, kom, donem, cok):
    """Ek 2 (e) ve ek dokumler: en iyi %5 cikarilinca, uzun/kisa bacak, VIX>30, yillar."""
    dm = donem_isl_maskesi(m, isl, donem)
    net = isl["net_" + kom].to_numpy()
    out = {}
    idx = np.flatnonzero(dm)
    n = idx.size
    if n == 0:
        return out
    k = max(3, int(math.ceil(0.05 * n)))
    sira = idx[np.argsort(net[idx])[::-1]]
    m5 = dm.copy()
    m5[sira[:k]] = False
    o5 = alt_ozet(m, isl, kom, m5) if m5.sum() else {"net_bps": np.nan, "n_islem": 0}
    out["en_iyi5suz_bps"] = o5.get("net_bps", np.nan)
    out["en_iyi5suz_n_cikan"] = k
    yon = isl["yon"].to_numpy(float)
    for ad, msk in (("uzun", yon > 0), ("kisa", yon < 0)):
        mm_ = dm & msk
        if mm_.sum():
            o = alt_ozet(m, isl, kom, mm_)
            out[f"{ad}_n"], out[f"{ad}_net_bps"] = o["n_islem"], o["net_bps"]
            out[f"{ad}_t"] = o.get("t_kume" if cok else "t_olcekli", np.nan)
    v30 = dm & (isl["kova_no"].to_numpy() == 2)
    out["v30_n"] = int(v30.sum())
    out["v30_net_bps"] = float(net[v30].mean() * 1e4) if v30.sum() else np.nan
    yil = m.idx.year.to_numpy()[isl["t_pos"].to_numpy()]
    out["yillar"] = "; ".join(f"{y}:{net[dm & (yil == y)].mean() * 1e4:.0f}({int((dm & (yil == y)).sum())})"
                              for y in sorted(set(yil[dm])))
    return out


def bolum30(m, isl, kom, donem):
    dm = donem_isl_maskesi(m, isl, donem)
    x = isl[dm]
    if not len(x):
        return {}
    try:
        tab, oz = m.bolum_ozeti(x, kom)
    except Exception as e:  # noqa: BLE001
        return {"hata": str(e)}
    return {"bolum_sayisi": oz.get("bolum_sayisi"), "bolum_net_bps": oz.get("net_bps"),
            "bolum_pozitif_oran": float((tab["net_bps"] > 0).mean()) if len(tab) else np.nan}


def yaz_is(df, aile, parca=""):
    df.to_pickle(os.path.join(SCR, f"is_{aile}{parca}.pkl"))


def ozetle(m, a, res, isl, gecer_fn, donemler, aile):
    """Bir aday icin OOS/SON satirlarini duz sozluge cevirir. res: ilgili h/cikis/rejim=hepsi satirlari;
    isl: Giris K islem listesi (ayni h/cikis, korunma). gecer_fn(row) -> bool."""
    sat = dict(aile_g=aile, anahtar=a["anahtar"], ki=a["ki"], h=int(a["h"]), cikis=a["cikis"])
    for _, x in res.iterrows():
        tag = f"{x.giris}_{x.donem}_{x.komisyon}"
        sat[f"{tag}_n"], sat[f"{tag}_net"] = x.n_islem, x.net_bps
        sat[f"{tag}_t"] = x.t_kume if a["cok"] else x.t_olcekli
        sat[f"{tag}_tan"], sat[f"{tag}_an"] = x.t_anormal, x.anormal_bps
        sat[f"{tag}_p"], sat[f"{tag}_ns"] = x.p_bootstrap, x.net_sigma
        sat[f"{tag}_gecer"] = bool(gecer_fn(x)) if x.n_islem > 0 else False
    if isl is not None:
        for dn in donemler:
            for kk, v in ayrinti(m, isl, "muzayede", dn, a["cok"]).items():
                sat[f"{dn}_{kk}"] = v
            for kk, v in bolum30(m, isl, "muzayede", dn).items():
                sat[f"{dn}_{kk}"] = v
    return sat
