#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01b_onbellek.py - Is Yatirim baglantisi 07.11.2026 gecesi kopuyordu (proxy: ws_closed_mid_exchange, connection reset).
Kural geregi zorlanmadi; bunun yerine AYNI KAYNAKTAN (Is Yatirim HisseTekil/ChartData, varsayilan basliklar) bu oturumun
onceki adimlarinda indirilmis onbellekler leadlag2/isy/ altina birlestirilir:
  * hisse: <scratch>/data/bist_test/hisse/<K>.parquet (HisseTekil: adj, raw, hi, lo, vol_tl; 2009 -> 05.11.2026)
           RYSAS icin <scratch>/data/akis_rejim/hisse/RYSAS.parquet (ayni format)
           06.11.2026 kapanisi <scratch>/data/sinyal/px/<K>.csv (ChartData duzeltilmis kapanis) oranindan eklenir
  * endeks/kur: <scratch>/data/bist_test/endeks/<K>.csv (ChartData; 2005 -> 06.11.2026)
Kullanim: python3 01b_onbellek.py --scratch /tmp/.../scratchpad/data --veri /tmp/.../scratchpad/data/leadlag2
"""
import argparse, os
import numpy as np, pandas as pd

HISSE = ["ENERY", "AHGAZ", "RYSAS", "RYGYO", "ENJSA", "AKSEN", "AYGAZ", "TUPRS", "KCHOL", "SAHOL", "AKBNK",
         "BRSAN", "BRYAT", "TRMET", "TRALT", "TRENJ"]
ENDEKS = ["XU100", "XU030", "XUTUM", "XELKT", "XGMYO", "XULAS", "USDTRY"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True); ap.add_argument("--veri", required=True)
    a = ap.parse_args()
    out = os.path.join(a.veri, "isy"); os.makedirs(out, exist_ok=True)
    log = []
    for k in HISSE:
        f1 = os.path.join(a.scratch, "bist_test", "hisse", k + ".parquet")
        f2 = os.path.join(a.scratch, "akis_rejim", "hisse", k + ".parquet")
        f = f1 if os.path.exists(f1) else f2
        d = pd.read_parquet(f)[["adj", "raw", "hi", "lo", "vol_tl"]].copy()
        d.index = pd.to_datetime(d.index).normalize(); d.index.name = "tarih"
        d = d[~d.index.duplicated(keep="last")].sort_index()
        fs = os.path.join(a.scratch, "sinyal", "px", k + ".csv")
        ek = ""
        if os.path.exists(fs):
            s = pd.read_csv(fs, index_col=0, parse_dates=True)["px"]
            son = d.index[-1]
            mts = pd.Timestamp(os.path.getmtime(fs), unit="s") + pd.Timedelta(hours=3)
            yeni = s[(s.index > son) & ((s.index < mts.normalize()) | (mts.hour >= 19))]
            if len(yeni) and son in s.index:
                # ChartData oranini HisseTekil adj'ye zincirle (yalniz eksik kuyruk)
                for t, v in yeni.items():
                    oran = v / s.loc[:t].iloc[-2]
                    d.loc[t] = [d["adj"].iloc[-1] * oran, np.nan, np.nan, np.nan, np.nan]
                ek = f" + ChartData {len(yeni)} gun ({yeni.index[-1].date()})"
        d.to_csv(os.path.join(out, k + ".csv"))
        log.append(f"{k}: {os.path.relpath(f, a.scratch)} {d.index[0].date()} -> {d.index[-1].date()} n={len(d)}{ek}")
    for k in ENDEKS:
        f = os.path.join(a.scratch, "bist_test", "endeks", k + ".csv")
        s = pd.read_csv(f, index_col=0, parse_dates=True)["px"]
        s.index = s.index.normalize(); s = s[~s.index.duplicated(keep="last")].sort_index()
        # DUZELTME: bist_test/endeks 06.11 12:59 TSI'de (seans icinde) indirildi -> o gunun degeri KAPANIS DEGIL.
        # Dosya tarihinden (TSI) itibaren satirlar atilir; kapanis sonrasi (20:53 TSI) yazilan sinyal/px varsa oradan eklenir.
        mt = pd.Timestamp(os.path.getmtime(f), unit="s") + pd.Timedelta(hours=3)
        kes = mt.normalize() if mt.hour < 19 else mt.normalize() + pd.Timedelta(days=1)
        s = s[s.index < kes]
        ek = ""
        fs = os.path.join(a.scratch, "sinyal", "px", k + ".csv")
        if os.path.exists(fs):
            mts = pd.Timestamp(os.path.getmtime(fs), unit="s") + pd.Timedelta(hours=3)
            q = pd.read_csv(fs, index_col=0, parse_dates=True)["px"]
            q = q[(q.index > s.index[-1]) & ((q.index < mts.normalize()) | (mts.hour >= 19))]
            if len(q):
                s = pd.concat([s, q]); ek = f" + sinyal/px {len(q)} gun ({q.index[-1].date()}, kapanis sonrasi indirme)"
        s.rename("px").to_frame().rename_axis("tarih").to_csv(os.path.join(out, k + ".csv"))
        log.append(f"{k}: bist_test/endeks {s.index[0].date()} -> {s.index[-1].date()} n={len(s)} (seans ici satir atildi: >= {kes.date()}){ek}")
    print("\n".join(log))
    open(os.path.join(a.veri, "onbellek_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
