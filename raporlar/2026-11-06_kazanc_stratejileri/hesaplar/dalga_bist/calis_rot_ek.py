"""Ek rotasyon ızgarası: 12 ay (r252) ve 12-1 ay (r252s21) göreli güç (Moskowitz-Grinblatt sektör momentumu tanımı).
Tanı testinde (calis_tani.py) 12 aylık IC en güçlü çıktığı için eklendi -> veri gözetleme riski raporda belirtildi."""
import os, sys, itertools, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
COST = float(os.environ.get("COST", "0.0025")); LAG = int(os.environ.get("LAG", "1")); SUF = os.environ.get("SUF", "")
P, R, sup = panel("2026-11-05")
C, NU = kume_getiri(R); rf, _ = rf_gunluk(C.index)
V = M.Veri(P, R, C, NU, rf, KUMELER); usd = P["USDTRY"].ffill()
BAS, BAS24 = "2012-01-02", "2024-01-02"
rows = []; SER = {}
for skor, K, fr, absf, mktf, lid, buf in itertools.product(["r252", "r252s21"], [2, 3], ["W", "M"], [0, 1], [0, 1], [0, 1], [0, 2]):
    r, inv, to, We = M.rotasyon(V, skor, K, fr, bool(absf), bool(mktf), bool(lid), buf, L=LAG, c=COST)
    o = M.olcu(r, inv, to, V, BAS, usd=usd); o24 = M.olcu(r, inv, to, V, BAS24, usd=usd)
    y = M.yillik(r.loc[BAS:], V)
    key = f"{skor}|K{K}|{fr}|abs{absf}|mktf{mktf}|{'lider' if lid else 'sepet'}|buf{buf}".replace("mktf", "mkt")
    SER['R:' + key] = r; SER['R:' + key + ':inv'] = inv
    rows.append(dict(kural=key, skor=skor, K=K, frekans=fr, absf=absf, mktf=mktf, surum="lider" if lid else "sepet", buf=buf,
                     **o, **{k + "_24": v for k, v in o24.items()},
                     yil_xu_yenen=(y.strateji > y.xu100).mean(), yil_rf_yenen=(y.strateji > y.rf).mean()))
    print(key, f"cagr={o['cagr']:.3f} a_rf={o['a_rf']:.3f} a_xu={o['a_xu']:.3f} dd={o['maxdd']:.2f} 24: {o24['cagr']:.3f}", flush=True)
pd.DataFrame(rows).to_csv(os.path.join(OUT, f"izgara_rot_ek{SUF}.csv"), index=False, float_format="%.4f")
pd.DataFrame(SER).to_parquet(f"/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist/seriler_ek{SUF}.parquet")
