#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_guncel.py - KENAR/FILTRE sinyallerinin SON degerleri (06.11.2026 BIST kapanisi; ABD 05.11/06.11).
Uretim betigiyle ayni tanimlar icin uygulama/kod/gunluk_oneri.py (pr_koza, pr_altin, pr_baz) ve
bist_sinyal.py (k1_tetikler) ice aktarilir; fiyatlar leadlag2 onbelleginden (Is Yatirim), bulten leadlag2/viop.
TUPRS <- ABD rafinerileri: ABD tekil hisse verisi izinli kaynakta yok -> HESAPLANMAZ (TradingView tuprs_alarm.pine).
"""
import argparse, os, sys, math, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o
KOD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "uygulama", "kod"))
sys.path.insert(0, KOD)
import bist_tarama as bt  # noqa: E402
import bist_sinyal as bs  # noqa: E402
import gunluk_oneri as go  # noqa: E402


def px(k):
    d = pd.read_csv(os.path.join(o.V, "isy", k + ".csv"), index_col=0, parse_dates=True)
    return (d["adj"] if "adj" in d.columns else d["px"]).dropna()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cikti", required=True)
    a = ap.parse_args()
    out = {}
    L = []
    D = {k: px(k) for k in ["SAHOL", "AKBNK", "TRMET", "TRALT", "TRENJ", "XU030", "XU100", "ENJSA", "ENERY", "AHGAZ",
                            "KCHOL", "RYSAS", "RYGYO", "BRSAN", "TUPRS"]}
    son = D["XU100"].index[-1]
    L.append(f"Son BIST kapanisi: {son.date()}")
    # K1
    x = (np.log(D["SAHOL"]) - np.log(D["AKBNK"])).dropna()
    z = bs.z_seri(x, 60)
    tet = bs.k1_tetikler(D["SAHOL"], D["AKBNK"])
    out["K1_z"] = float(z.iloc[-1])
    L.append(f"K1 SAHOL/AKBNK z60 = {z.iloc[-1]:+.2f} (SAHOL {D['SAHOL'].iloc[-1]:.2f}, AKBNK {D['AKBNK'].iloc[-1]:.2f}); "
             f"tetikler (oburu sabit): z+2 SAHOL>={tet.get('SAHOL_z+2', np.nan):.2f} | AKBNK<={tet.get('AKBNK_z+2', np.nan):.2f}; "
             f"z-2 SAHOL<={tet.get('SAHOL_z-2', np.nan):.2f} | AKBNK>={tet.get('AKBNK_z-2', np.nan):.2f}")
    # Koza
    K = go.pr_koza({k: D[k] for k in ["TRMET", "TRALT", "TRENJ", "XU030"]}, 1_000_000, 0.0075)
    if K:
        Lk = K["L"]
        out["koza_z3"] = float(Lk.z3)
        L.append(f"Koza z3 = {Lk.z3:+.2f} (u {Lk.u*1e4:+.0f} bps, sd60 {Lk.sd60*1e4:.0f} bps, b_g {Lk.b_g:.2f}, bH {Lk.bH:.2f}); "
                 f"sonraki kapanis tetigi (TRALT/TRENJ yatay): AL TRMET>={K['tet_al']:.2f}, SAT TRMET<={K['tet_sat']:.2f}; "
                 f"kural pozisyonu: {('ACIK ' + str(K['pos'])) if K['pos'] else 'yok'}; son islemler: " +
                 "; ".join(f"{K['idx'][t['i0']].date()} {'AL' if t['s']>0 else 'SAT'} cikis {K['idx'][t['out']].date()}" for t in K["trades"][-3:]))
    # VIOP bultenleri
    B1, g1 = bt.viop_bulten(pd.Timestamp("2026-11-06"), o.V, geri=0)
    B0, g0 = bt.viop_bulten(pd.Timestamp("2026-11-05"), o.V, geri=0)
    if B1 is not None:
        A = go.pr_altin(B1, g1, {k: D[k] for k in ["TRALT", "XU030"]}, 1_000_000)
        if A:
            out["altin_z_viop"] = A["z"]
            L.append(f"Altin->TRALT (VIOP {A['kod']} uzlasma vekili; pratik sinyal 17:55 TVC:GOLD): g {A['g']*100:+.2f}%, z {A['z']:+.2f} "
                     f"(sigma %1,70); beta {A.get('beta', np.nan):.2f}, N {A.get('N')}")
        A0 = go.pr_altin(B0, g0, {k: D[k] for k in ["TRALT", "XU030"]}, 1_000_000)
        if A0:
            L.append(f"  05.11 ayni vekil: g {A0['g']*100:+.2f}%, z {A0['z']:+.2f}")
        Z = go.pr_baz(B1, g1, B0, g0, {"XU030": D["XU030"]})
        if Z:
            out["xu030_db_bps"] = Z["db"] * 1e4
            L.append(f"XU030 baz ({Z['kod']}, bulten KAPANIS fiyati vs spot kapanis): b {Z['b']*1e4:+.0f} bps, dun {Z['b0']*1e4:+.0f}, "
                     f"Db {Z['db']*1e4:+.0f} bps, z {Z['z']:+.2f} (esik |Db| > ~50 bps)")
        for kod in ["F_TUPRS1226", "F_TUPRS1126", "F_TRMET1226", "F_TRALT1226", "F_SAHOL1226", "F_AKBNK1226", "F_ENJSA1226", "F_KCHOL1226", "F_BRSAN1226"]:
            r = B1[B1["SOZLESME KODU"] == kod]
            if len(r):
                r = r.iloc[0]
                L.append(f"  {kod}: uzlasma {r['UZLASMA FIYATI']}, kapanis {r['KAPANIS FIYATI']}, hacim {r['ISLEM HACMI']/1e6:.0f} mn TL, AP {r['ACIK POZISYON']:.0f}")
    # RYSAS <- RYGYO
    cal = o.takvim()
    rg = o.bist_getiri("RYGYO", cal); sd = rg.rolling(250, min_periods=100).std().shift(1)
    zr = rg.iloc[-1] / sd.iloc[-1]
    out["rygyo_z"] = float(zr)
    L.append(f"RYGYO -> RYSAS: RYGYO 06.11 r {rg.iloc[-1]*100:+.2f}%, sd250 {sd.iloc[-1]*100:.2f}% -> z {zr:+.2f}; "
             f"yarinki esik: RYGYO kapanis >= {px('RYGYO').iloc[-1]*math.exp(sd.iloc[-1]):.2f} (z>+1) / <= {px('RYGYO').iloc[-1]*math.exp(-sd.iloc[-1]):.2f} (z<-1)")
    # ABD/EIA risk baglami
    spx = o.fred("SP500"); vix = o.cboe_vix(); br = o.fred("DCOILBRENTEU"); hh = o.fred("DHHNGSP")
    L.append(f"ABD: S&P 500 (FRED) son {spx.index[-1].date()} {spx.iloc[-1]:.2f} ({(spx.iloc[-1]/spx.iloc[-2]-1)*100:+.2f}%); "
             f"VIX (CBOE) {vix.index[-1].date()} {vix.iloc[-1]:.2f} (onceki {vix.iloc[-2]:.2f}, {vix.index[-3].date()} {vix.iloc[-3]:.2f}); "
             f"Brent (EIA) {br.index[-1].date()} {br.iloc[-1]:.2f}; Henry Hub {hh.index[-1].date()} {hh.iloc[-1]:.2f}")
    # K4 tetik uzakliklari
    tet4 = {"ENJSA": 127.00, "ENERY": 14.60, "AHGAZ": 48.70, "KCHOL": 225.50, "RYSAS": 30.28, "BRSAN": 769.50}
    for k, v in tet4.items():
        p = D[k].iloc[-1]
        L.append(f"K4 {k}: kapanis {p:.2f}, tetik {v:.2f}, gereken {(v/p-1)*100:+.1f}%")
    sma50 = D["KCHOL"].iloc[-50:].mean()
    L.append(f"KCHOL SMA50 (adj) {sma50:.2f}")
    # ENERY/AHGAZ ayni gun
    for k in ["ENERY", "AHGAZ", "ENJSA", "RYSAS", "RYGYO"]:
        s = D[k]
        L.append(f"  {k} {s.index[-1].date()} {s.iloc[-1]:.2f} ({(s.iloc[-1]/s.iloc[-2]-1)*100:+.2f}%)")
    txt = "\n".join(L)
    open(os.path.join(a.cikti, "guncel.txt"), "w").write(txt + "\n")
    json.dump(out, open(os.path.join(a.cikti, "guncel.json"), "w"), indent=1)
    print(txt)


if __name__ == "__main__":
    main()
