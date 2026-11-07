#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""05_md_tablolar.py - aile_P.csv / aile_S.csv -> Markdown (Ek B). Etiketler burada, sonuclara gore elle verildi (gerekce raporda)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

TV = {"AHGAZ": "BIST:AHGAZ", "ENERY": "BIST:ENERY", "ENJSA": "BIST:ENJSA", "AKSEN": "BIST:AKSEN", "AYGAZ": "BIST:AYGAZ",
      "XELKT": "BIST:XELKT", "XUTUMx": "BIST:XUTUM−BIST:XU100", "USDTRY": "FX:USDTRY (BIST:USDTRY1!)",
      "HH": "NYMEX:NG1! (veri: FRED DHHNGSP)", "BRENT": "ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)", "RYGYO": "BIST:RYGYO",
      "XGMYO": "BIST:XGMYO", "XULAS": "BIST:XULAS", "FF_OILx": "AMEX:XLE−β·SP:SPX (veri: FF49 Oil)", "SP500": "SP:SPX (veri: FRED SP500)",
      "AKBNK": "BIST:AKBNK", "VIX": "CBOE:VIX", "FF_STEELx": "AMEX:SLX−β·SP:SPX (veri: FF49 Steel)", "BRYAT": "BIST:BRYAT",
      "KOZAGRP": "(BIST:TRALT+BIST:TRENJ)/2", "FF_GOLDx": "AMEX:GDX−β·SP:SPX (veri: FF49 Gold)"}
ETP = {("RYSAS", "RYGYO", 1): "FILTRE (kenar adayı)", ("TUPRS", "FF_OILx", 1): "FILTRE", ("TUPRS", "FF_OILx", 2): "FILTRE",
       ("SAHOL", "AKBNK", 1): "FILTRE (zayıf)"}
ETS = {("ENERY", "AHGAZ"): "FILTRE", ("AHGAZ", "ENERY"): "FILTRE", ("ENERY", "XELKT"): "FILTRE", ("AHGAZ", "XELKT"): "FILTRE",
       ("ENERY", "XUTUMx"): "FILTRE", ("AHGAZ", "XUTUMx"): "FILTRE", ("ENERY", "HH"): "RISK (zayıf)", ("RYSAS", "RYGYO"): "FILTRE",
       ("RYSAS", "XGMYO"): "FILTRE", ("RYSAS", "XUTUMx"): "FILTRE", ("RYSAS", "XULAS"): "FILTRE (zayıf)", ("TUPRS", "FF_OILx"): "RISK",
       ("TRALT", "FF_GOLDx"): "RISK", ("SAHOL", "AKBNK"): "FILTRE", ("BRSAN", "BRYAT"): "FILTRE", ("TRMET", "KOZAGRP"): "FILTRE",
       ("ENERY", "AKSEN"): "YOK (pc 0,09)"}


def f(x, d=1, plus=True):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "–"
    s = f"{x:+.{d}f}" if plus else f"{x:.{d}f}"
    return s.replace(".", ",")


def main():
    S0 = os.path.join(o.V, "sonuc")
    P = pd.read_csv(os.path.join(S0, "aile_P.csv")); S = pd.read_csv(os.path.join(S0, "aile_S.csv"))
    L = ["## Ek B. Yeni testler: tam tablolar", "",
         "### B1. Aile P — öngörü (38 test, BH-FDR aile içinde)", "",
         "Model: r_hedef(t→t+1) = a + b·L_t + c·r_hedef,t + d·r_XU100,t; NW(5) t. Etki = b·sd(L), bps/1σ. ABD/EIA serileri ABD günü d'den sonraki ilk BIST gününe (t) eşlendi. "
         "Kural: |z_L|>1 → yön = işaret(b_IS)·işaret(z), hedef − β250·XU100, 1 gün (ufuk 2: 2 gün, örtüşmesiz); maliyet spot 25+3, VİOP 12,5+3 bps.", "",
         "| Hedef | Lider (TradingView) | Ufuk | n | Etki bps/1σ | t | t IS / OOS / 2024+ | q | İşlem n | Brüt | Net (t) | Net OOS (t) | Net 2024+ | Etiket |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in P.iterrows():
        e = ETP.get((r.hedef, r.lider, int(r.ufuk)), "YOK")
        L.append(f"| {r.hedef} | `{TV.get(r.lider, r.lider)}` | {int(r.ufuk)} | {int(r.n)} | {f(r.etki_bps_1sd)} | {f(r.t, 2)} | "
                 f"{f(r.t_IS, 2)} / {f(r.t_OOS, 2)} / {f(r.t_2024, 2)} | {f(r.q_BH, 2, False)} | {int(r.islem_n)} | {f(r.brut)} | "
                 f"{f(r.net)} ({f(r.net_t, 2)}) | {f(r.net_OOS)} ({f(r.net_OOS_t, 2)}) | {f(r.net_2024)} | **{e}** |")
    L += ["", "### B2. Aile S — senkron / gap günü kısmi korelasyonu (XU100 kontrollü; 36 test)", "",
          "| Hedef | Lider | Ölçü | n | pc | IS / OOS / son 1y | q | Etiket |", "|---|---|---|---|---|---|---|---|"]
    for _, r in S.iterrows():
        e = ETS.get((r.hedef, r.lider), "YOK")
        L.append(f"| {r.hedef} | `{TV.get(r.lider, r.lider)}` | {r.olcu} | {int(r.n)} | {f(r.pc, 3)} | {f(r.pc_IS, 2)} / {f(r.pc_OOS, 2)} / {f(r.pc_son1y, 2)} | {f(r.q_BH, 3, False)} | {e} |")
    txt = "\n".join(L) + "\n"
    open(os.path.join(S0, "ek_testler.md"), "w").write(txt)
    print(len(txt))


if __name__ == "__main__":
    main()
