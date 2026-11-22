# -*- coding: utf-8 -*-
"""ek2_RF1a_detay.py - Ek 2 olcutleri (b)-(f) ve ek dokumler: yalniz OOS'ta ayni yon ve ilgili t >= 2 olanlar.
ek2_RF1a.py 'detay <aile>' asamasindan cagrilir."""
import os
import json
import numpy as np
import pandas as pd
import ek2_RF1a as E
import motor as M


def _bul(r, donem, giris, x, kom):
    y = r[(r["donem"] == donem) & (r["giris"] == giris) & (r["komisyon"] == kom) & (r["h"] == x["h"])
          & (r["cikis"] == x["cikis"]) & (r["korunma"] == x["korunma"]) & (r["rejim"] == x["rejim"])]
    return y.iloc[0] if len(y) else None


def _f(v):
    return None if v is None or (isinstance(v, float) and not np.isfinite(v)) else (float(v) if isinstance(v, (float, np.floating, int, np.integer)) else v)


def calis(aile, saatlik_fn=None):
    O = pd.read_pickle(os.path.join(E.ARA, f"oos_{aile}.pkl"))
    G = O[O["oos_t2"]] if len(O) else O
    out_j = {}
    if not len(G):
        json.dump({}, open(os.path.join(E.ARA, f"detay_{aile}.json"), "w"))
        print(f"{aile}: OOS'ta t>=2 olan yok")
        return
    a = E.AILELER[aile]()
    sat = []
    for _, x in G.iterrows():
        b = x["birim"]
        yeni = x["hat"] == "yeni"
        dn = ["IS2", "OOS2"] if yeni else ["IS", "OOS", "SON", "TUM", "OOS-2020", "OOS-2022", "OOS-SubNis2020"]
        combos = [(int(x["h"]) if x["cikis"] == "kapanis" else 1, x["cikis"])]
        rej = x["rejim"] != "hepsi"
        r, isl = a.calis(b, dn, combos=combos, korunma=(x["korunma"],), giris=("K", "A"), komisyon=(E.KOM, "hisse"),
                         rejimler=True if rej else False, bootstrap=True, islem_dondur=True)
        r = r.copy()
        r["birim"] = b
        r["aile_kod"] = aile
        sat.append(r)
        oosd, sond = ("OOS2", "OOS2") if yeni else ("OOS", "SON")
        o = _bul(r, oosd, "K", x, E.KOM)
        sn = _bul(r, sond, "K", x, E.KOM)
        ga = _bul(r, oosd, "A", x, E.KOM) if x["cikis"] == "kapanis" else None
        cok = E.cok_hedef(o)
        hk = 0 if x["cikis"] == "acilis" else int(x["h"])
        ik = None
        for k, d in isl.items():
            if k[0] == "K" and k[2] == x["cikis"] and k[3] == x["korunma"] and (k[1] == hk or k[1] == int(x["h"])):
                ik = d
        ik = ik.copy()
        if rej:
            ik = ik[ik["rejim"].astype(str).str.contains(x["rejim"].split("|")[0], regex=False)] if "rejim" in ik else ik
        ik["yil"] = pd.DatetimeIndex(ik["t"]).year
        yil = ik.groupby("yil")["net_" + E.KOM].agg(["count", "mean"])
        tab, boz = a.m.bolum_ozeti(ik, E.KOM)
        oo = ik[ik["donem"] == oosd] if "donem" in ik else ik
        uz = oo[oo["yon"] > 0]["net_" + E.KOM]
        ks = oo[oo["yon"] < 0]["net_" + E.KOM]
        bilgi = {
            "b_oos_t": _f(E._t(o, cok)), "b": bool(E._t(o, cok) >= 2.5), "esik_yeni_yapi_3": bool(E._t(o, cok) >= 3.0),
            "c_son_net_bps": _f(sn["net_bps"]) if sn is not None else None,
            "c_son_t": _f(E._t(sn, cok)) if sn is not None else None, "c_son_n": _f(sn["n_islem"]) if sn is not None else None,
            "c": bool(sn is not None and sn["net_bps"] > 0),
            "d_girisA_oos_net_bps": _f(ga["net_bps"]) if ga is not None else None,
            "d_girisA_oos_t": _f(E._t(ga, cok)) if ga is not None else None,
            "d_a": bool(ga is not None and ga["net_bps"] > 0 and E._t(ga, cok) >= 1.5),
            "e_en_iyi5suz_bps": _f(o["en_iyi5suz_bps"]), "e": bool(o["en_iyi5suz_bps"] > 0),
            "f_net_bps": _f(o["net_bps"]), "f_net_sigma": _f(o["net_sigma"]),
            "f": bool(o["net_bps"] >= 10 and o["net_sigma"] >= 0.10),
            "oos_uzun_bps": _f(uz.mean() * 1e4) if len(uz) else None, "oos_uzun_n": int(len(uz)),
            "oos_kisa_bps": _f(ks.mean() * 1e4) if len(ks) else None, "oos_kisa_n": int(len(ks)),
            "vix30_bolum": {k: _f(v) for k, v in boz.items()},
            "yil_net_bps": {int(y): [int(q["count"]), round(float(q["mean"] * 1e4), 1)] for y, q in yil.iterrows()},
            "birincil_hisse_oos_net_bps": _f(_bul(r, oosd, "K", x, "hisse")["net_bps"]),
            "birincil_hisse_oos_t": _f(E._t(_bul(r, oosd, "K", x, "hisse"), cok)),
            "oos_p_wilcoxon": _f(o["p_wilcoxon"]), "oos_p_bootstrap": _f(o["p_bootstrap"]),
        }
        for d in ("OOS-2020", "OOS-2022", "OOS-SubNis2020", "TUM", "IS"):
            y = _bul(r, d, "K", x, E.KOM)
            if y is not None:
                bilgi[f"{d}_net_bps"], bilgi[f"{d}_t"] = _f(y["net_bps"]), _f(E._t(y, cok))
        if saatlik_fn is not None:
            bilgi["s1530"] = saatlik_fn(a, x, ik)
        out_j[f"{b}|{x['h']}|{x['cikis']}|{x['korunma']}|{x['rejim']}"] = bilgi
        print(b, json.dumps(bilgi, default=str)[:1500], flush=True)
    pd.concat(sat, ignore_index=True).to_pickle(os.path.join(E.ARA, f"detay_{aile}.pkl"))
    json.dump(out_j, open(os.path.join(E.ARA, f"detay_{aile}.json"), "w"), indent=1, default=str)
