"""Rapor icin markdown tablolarini cikti/*.csv dosyalarindan uretir (stdout)."""
import os, json, numpy as np, pandas as pd
O = "/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/bist_test/cikti"
def pct(v): return "-" if pd.isna(v) else f"{100*v:.1f}%"
def num(v, k=2): return "-" if pd.isna(v) else f"{v:.{k}f}"
def md(df, cols, fm):
    h = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for _, r in df.iterrows(): h += "| " + " | ".join(fm.get(c, str)(r[c]) for c in cols) + " |\n"
    return h
F = {"CAGR": pct, "Fazla": pct, "Vol": pct, "Sharpe": num, "MaxDD": pct, "Isabet": pct, "CAGR_2024_26": pct, "Fazla_2024_26": pct, "CAGR_24_26": pct,
     "Fazla_24_26": pct, "zaman_ici": pct, "islem_yil": lambda v: num(v, 1), "turnover": num, "turnover_ay": num}
print("## T04"); d = pd.read_csv(f"{O}/t04_ozet.csv")
d = d[(d.maliyet.isin(["-", "VIOP12.5bp"]))]
for cur in ("TL", "USD"):
    x = d[(d.para == cur) & ~d.kural.str.contains("volhedef")]
    print(f"### {cur}"); print(md(x, ["endeks", "kural", "zaman_ici", "islem_yil", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_2024_26", "Fazla_2024_26"], F))
x = d[(d.para == "TL") & d.kural.str.contains("volhedef")]; print("### volhedef TL"); print(md(x, ["endeks", "kural", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD"], F))
print(json.dumps({k: {a: round(b, 2) for a, b in v.items()} for k, v in json.load(open(f"{O}/t04_placebo.json")).items()}, indent=0))
y = pd.read_csv(f"{O}/t04_yillik.csv", index_col=0)
c = [c for c in y.columns if c in ("XU100 AL-TUT TL", "XU100 TSMOM_12ay TL", "XU100 A_P>SMA200 TL", "XU100 AL-TUT USD", "XU100 TSMOM_12ay USD", "rf TL rf TL")]
print(y[c].apply(lambda s: s.map(pct)).to_markdown())
for suf in ("", "_buyuk"):
    p = f"{O}/t05_ozet{suf}.csv"
    if not os.path.exists(p): continue
    print(f"## T05{suf}"); d = pd.read_csv(p)
    for cur in ("TL", "USD"):
        x = d[(d.para == cur) & ~d.strateji.str.contains("50bp")]
        print(f"### {cur}"); print(md(x, ["strateji", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "Isabet", "CAGR_24_26", "Fazla_24_26", "turnover_ay"], F))
    print(json.dumps({k: {a: round(b, 3) for a, b in v.items()} for k, v in json.load(open(f"{O}/t05_placebo{suf}.json")).items()}, indent=0))
    y = pd.read_csv(f"{O}/t05_yillik{suf}.csv", index_col=0)
    c = [c for c in y.columns if c.endswith(" TL") and any(k in c for k in ("MOM12ay top3 25bp TL", "MOM3ay top2 25bp TL", "EW tum", "XU100", "TL rf TL"))]
    print(y[c].apply(lambda s: s.map(pct)).to_markdown())
p = f"{O}/t01_ozet.csv"
if os.path.exists(p):
    print("## T01"); d = pd.read_csv(p); T = d[d.para == "TL"]
    print(md(T[T.test == "kiyas"], ["strateji", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26"], F))
    rows = []
    for t in ("MOM", "MOM-EW", "MOM-LS", "MOM-rejim", "REV", "REV-EW", "KMOM", "KMOM-EW"):
        for cur in ("TL", "USD"):
            g = d[(d.test == t) & (d.para == cur) & (d.maliyet == "25bp")]
            if len(g) == 0: continue
            rows.append(dict(test=t, para=cur, n=len(g), **g[["CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26"]].median().to_dict(),
                             en_iyi_CAGR=g.CAGR.max(), en_kotu_CAGR=g.CAGR.min()))
    print(md(pd.DataFrame(rows), ["test", "para", "n", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26", "en_iyi_CAGR", "en_kotu_CAGR"], dict(F, n=str, en_iyi_CAGR=pct, en_kotu_CAGR=pct)))
    g = T[T.test.isin(["MOM"]) & (T.maliyet == "25bp") & (T.evren == 150)]
    print(md(g, ["strateji", "turnover", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "Isabet", "CAGR_24_26", "Fazla_24_26"], F))
    g = T[T.test.isin(["REV"]) & (T.maliyet == "25bp")]
    print(md(g, ["strateji", "turnover", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26"], F))
    g = T[T.test.isin(["KMOM", "KMOM-EW"])]
    print(md(g, ["strateji", "turnover", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26"], F))
    g = T[T.test.isin(["MOM-EW"]) & (T.evren == 150)]
    print(md(g, ["strateji", "CAGR", "Sharpe", "MaxDD", "CAGR_24_26"], F))
    print(json.dumps({k: {a: round(b, 3) for a, b in v.items()} for k, v in json.load(open(f"{O}/t01_placebo.json")).items()}, indent=0))
for suf in ("", "_gercekci", "_top75", "_kohort2009"):
    p = f"{O}/t03_islem_ozet{suf}.csv"
    if not os.path.exists(p): continue
    print(f"## T03{suf}"); d = pd.read_csv(p)
    print(md(d, ["sinyal", "cikis", "N", "islem_yil", "ort_gun", "ort_net", "medyan_net", "isabet", "payoff", "carpiklik", "p05", "p95", "ort_rf_ustu", "ort_evren_ustu(placebo)", "t_evren_ustu(ay-kume)", "ort_net_2024_26", "evren_ustu_2024_26", "N_2024_26"],
             {"N": lambda v: str(int(v)), "N_2024_26": lambda v: str(int(v)), "islem_yil": lambda v: num(v, 0), "ort_gun": lambda v: num(v, 0), "ort_net": pct, "medyan_net": pct, "isabet": pct, "payoff": num, "carpiklik": num, "p05": pct, "p95": pct,
              "ort_rf_ustu": pct, "ort_evren_ustu(placebo)": pct, "t_evren_ustu(ay-kume)": num, "ort_net_2024_26": pct, "evren_ustu_2024_26": pct}))
    f = pd.read_csv(f"{O}/t03_portfoy{suf}.csv")
    print(md(f, ["sinyal", "cikis", "para", "islem", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26", "MaxDD_24_26"] + [c for c in ("placebo_p95_CAGR", "yuzdelik_Sharpe") if c in f],
             dict(F, islem=lambda v: str(int(v)), MaxDD_24_26=pct, placebo_p95_CAGR=pct, yuzdelik_Sharpe=num)))
    y = pd.read_csv(f"{O}/t03_portfoy_yillik_TL{suf}.csv", index_col=0)
    print(y.apply(lambda s: s.map(pct)).to_markdown())
    p2 = f"{O}/t03_yillik_islem_S2_iz15{suf}.csv"
    if os.path.exists(p2): print(pd.read_csv(p2).round(3).to_markdown(index=False))
