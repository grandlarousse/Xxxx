"""TEST 3 (+ TEST 5'in PEAD kismi): Chen-Zimmermann 212 anomalinin yayin sonrasi bozulmasi.
Veri: OpenSourceAP CrossSection, Data-Release-2026.10 (Hugging Face), PredictorLSretWide (OP tarzi uzun-kisa, aylik %, 1926-2025)
     + LiqScreen_ME_gt_NYSE20pct ve LiqScreen_VWforce alternatif portfoyleri (daha uygulanabilir versiyonlar).
Donemler (McLean-Pontiff 2016 tarzi): IS = SampleStartYear..SampleEndYear ; OOS-yayin-oncesi = SampleEnd+1..Year ;
          Yayin-sonrasi = Year+1..2025.  (Year = makalenin yayin yili; ay hassasiyeti yok.)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from ortak import CZ, OUT, fmt_pct, md_table

doc = pd.read_csv(os.path.join(CZ, "SignalDoc.csv"))
doc = doc[doc["Cat.Signal"] == "Predictor"].set_index("Acronym")
W = pd.read_parquet(os.path.join(CZ, "PredictorLSretWide.parquet"))
W["date"] = pd.to_datetime(W["date"]); W = W.set_index("date")


def alt_wide(fname):
    a = pd.read_parquet(os.path.join(CZ, fname))
    a = a[a.port == "LS"]
    a["date"] = pd.to_datetime(a["date"])
    return a.pivot_table(index="date", columns="signalname", values="ret")


ALT = {"ME>NYSE20p": alt_wide("PredictorAltPorts_LiqScreen_ME_gt_NYSE20pct.parquet"),
       "VWforce": alt_wide("PredictorAltPorts_LiqScreen_VWforce.parquet")}

FAM = {
    "momentum": "Momentum/trend", "lead lag": "Momentum/trend",
    "short-term reversal": "Kisa vade reversal", "long term reversal": "Uzun vade reversal",
    "earnings event": "Kazanc/analist (PEAD ailesi)", "earnings forecast": "Kazanc/analist (PEAD ailesi)",
    "earnings growth": "Kazanc/analist (PEAD ailesi)", "recommendation": "Kazanc/analist (PEAD ailesi)",
    "sales growth": "Kazanc/analist (PEAD ailesi)",
    "valuation": "Deger (value)",
    "profitability": "Karlilik/kalite", "profitability alt": "Karlilik/kalite", "composite accounting": "Karlilik/kalite",
    "investment": "Yatirim/ihrac", "investment alt": "Yatirim/ihrac", "investment growth": "Yatirim/ihrac",
    "external financing": "Yatirim/ihrac", "asset composition": "Yatirim/ihrac", "accruals": "Tahakkuk (accruals)",
    "liquidity": "Likidite/hacim/sahiplik", "volume": "Likidite/hacim/sahiplik", "informed trading": "Likidite/hacim/sahiplik",
    "short sale constraints": "Likidite/hacim/sahiplik", "ownership": "Likidite/hacim/sahiplik", "size": "Likidite/hacim/sahiplik",
    "risk": "Risk/volatilite/kaldirac", "volatility": "Risk/volatilite/kaldirac", "optionrisk": "Risk/volatilite/kaldirac",
    "default risk": "Risk/volatilite/kaldirac", "cash flow risk": "Risk/volatilite/kaldirac", "leverage": "Risk/volatilite/kaldirac",
}


def family(sig):
    c = doc.loc[sig, "Cat.Economic"]
    if c == "other":
        return "Mevsimsellik (MomSeason vb.)" if sig.startswith("Mom") else "Diger"
    return FAM.get(c, "Diger")


def tstat(x):
    x = x.dropna()
    return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 and x.std() > 0 else np.nan


rows = []
for sig in W.columns:
    if sig not in doc.index:
        continue
    r = W[sig].dropna()
    if len(r) < 60:
        continue
    d = doc.loc[sig]
    s0, s1, py = int(d.SampleStartYear), int(d.SampleEndYear), int(d.Year)
    is_ = r[(r.index.year >= s0) & (r.index.year <= s1)]
    oos = r[(r.index.year > s1) & (r.index.year <= py)]
    post = r[r.index.year > py]
    p10 = r[r.index.year >= 2010]
    p16 = r[r.index.year >= 2016]
    p21 = r[r.index.year >= 2021]
    row = dict(sig=sig, fam=family(sig), year=py, IS=is_.mean(), OOS=oos.mean() if len(oos) >= 12 else np.nan,
               POST=post.mean() if len(post) >= 24 else np.nan, nPOST=len(post), tIS=tstat(is_), tPOST=tstat(post),
               R10=p10.mean(), t10=tstat(p10), SR10=p10.mean() / p10.std() * np.sqrt(12) if len(p10) > 12 else np.nan,
               R16=p16.mean(), R21=p21.mean(), ER_OP=d.Return)
    for k, A in ALT.items():
        if sig in A:
            x = A[sig].dropna()
            row[f"R10_{k}"] = x[x.index.year >= 2010].mean()
            row[f"POST_{k}"] = x[x.index.year > py].mean() if (x.index.year > py).sum() >= 24 else np.nan
            row[f"IS_{k}"] = x[(x.index.year >= s0) & (x.index.year <= s1)].mean()
    rows.append(row)
R = pd.DataFrame(rows)
R["ratio_post"] = R.POST / R.IS
R["ratio_oos"] = R.OOS / R.IS
R.to_csv(os.path.join(OUT, "t3_sinyal_bazli.csv"), index=False)

md = []
# --- genel ozet
v = R.dropna(subset=["POST"])
summ = pd.DataFrame([
    dict(Olcu="Sinyal sayisi (yayin sonrasi >=24 ay)", Deger=f"{len(v)} / {len(R)}"),
    dict(Olcu="IS ortalama aylik LS getiri, medyan", Deger=f"{R.IS.median():.2f}%"),
    dict(Olcu="OOS (orneklem sonu..yayin) medyan", Deger=f"{R.OOS.median():.2f}%"),
    dict(Olcu="Yayin sonrasi medyan", Deger=f"{v.POST.median():.2f}%"),
    dict(Olcu="Yayin sonrasi / IS orani: medyan (sinyal bazli)", Deger=f"{v.ratio_post.median():.2f}"),
    dict(Olcu="Yayin sonrasi / IS orani: ort(POST)/ort(IS) (havuzlanmis)", Deger=f"{v.POST.mean() / v.IS.mean():.2f}"),
    dict(Olcu="OOS / IS orani (havuzlanmis)", Deger=f"{R.OOS.mean() / R.IS.mean():.2f}"),
    dict(Olcu="Yayin sonrasi t>2 olan pay", Deger=fmt_pct((v.tPOST > 2).mean())),
    dict(Olcu="Yayin sonrasi ortalama negatif olan pay", Deger=fmt_pct((v.POST < 0).mean())),
    dict(Olcu="2010-2025 medyan aylik LS (OP tarzi)", Deger=f"{R.R10.median():.2f}%  (yillik ~{12 * R.R10.median():.1f}%)"),
    dict(Olcu="2010-2025 t>2 olan pay", Deger=fmt_pct((R.t10 > 2).mean())),
    dict(Olcu="2016-2025 medyan aylik LS", Deger=f"{R.R16.median():.2f}%"),
    dict(Olcu="2021-2025 medyan aylik LS", Deger=f"{R.R21.median():.2f}%"),
    dict(Olcu="2010-2025 medyan, ME>NYSE20p likidite filtresi", Deger=f"{R['R10_ME>NYSE20p'].median():.2f}%"),
    dict(Olcu="2010-2025 medyan, VWforce (deger agirlikli)", Deger=f"{R['R10_VWforce'].median():.2f}%"),
    dict(Olcu="IS medyan, VWforce", Deger=f"{R['IS_VWforce'].median():.2f}%"),
])
md += ["\n#### Genel ozet (aylik uzun-kisa getiri, %, maliyet oncesi)\n", md_table(summ, pct_cols=())]

# --- aile bazli
g = R.groupby("fam").agg(n=("sig", "size"), IS=("IS", "mean"), POST=("POST", "mean"), R10=("R10", "mean"),
                         R10_med=("R10", "median"), pos10=("R10", lambda x: (x > 0).mean()),
                         t2_10=("t10", lambda x: (x > 2).mean()), SR10=("SR10", "median"),
                         R10_liq=("R10_ME>NYSE20p", "mean"), R10_vw=("R10_VWforce", "mean"), R21=("R21", "mean"))
g["POST/IS"] = g.POST / g.IS
g["R10/IS"] = g.R10 / g.IS
g = g.sort_values("R10", ascending=False).reset_index()
out = g.copy()
for c in ["IS", "POST", "R10", "R10_med", "R10_liq", "R10_vw", "R21"]:
    out[c] = out[c].map(lambda x: f"{x:.2f}")
for c in ["POST/IS", "R10/IS", "SR10"]:
    out[c] = out[c].map(lambda x: f"{x:.2f}")
for c in ["pos10", "t2_10"]:
    out[c] = out[c].map(fmt_pct)
out = out.rename(columns={"fam": "Aile", "IS": "IS ort %/ay", "POST": "Yayin-sonr %/ay", "R10": "2010-25 ort %/ay",
                          "R10_med": "2010-25 medyan", "pos10": "2010-25 >0 pay", "t2_10": "2010-25 t>2 pay",
                          "SR10": "2010-25 medyan Sharpe", "R10_liq": "2010-25 ME>NYSE20p", "R10_vw": "2010-25 VWforce",
                          "R21": "2021-25 ort"})
md += ["\n#### Aile bazli (OP tarzi uzun-kisa, maliyet oncesi, %/ay); 2010-2025 ortalamaya gore sirali\n", md_table(out, pct_cols=())]

# --- en iyi 15 sinyal 2010-2025 (bilgi; secim yanliligi uyarisi)
top = R.sort_values("t10", ascending=False).head(15)[["sig", "fam", "year", "IS", "POST", "R10", "t10", "R10_ME>NYSE20p", "R10_VWforce"]]
for c in ["IS", "POST", "R10", "R10_ME>NYSE20p", "R10_VWforce"]:
    top[c] = top[c].map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
top["t10"] = top["t10"].map(lambda x: f"{x:.2f}")
md += ["\n#### 2010-2025 t-istatistigine gore ilk 15 sinyal (EX-POST secim: 212 icinden en iyiler; coklu test yanliligi var)\n", md_table(top, pct_cols=())]

# --- PEAD / kazanc sinyalleri ayrintisi
pead = ["AnnouncementReturn", "EarningsSurprise", "EarningsStreak", "EarnSupBig", "RevenueSurprise", "AnalystRevision",
        "REV6", "ChangeInRecommendation", "EarningsConsistency", "NumEarnIncrease", "STreversal", "IndMom", "Mom12m", "Mom6m",
        "ResidualMomentum", "IntMom", "MomSeason"]
rows = []
for s in pead:
    if s not in W:
        continue
    r = W[s].dropna()
    d = doc.loc[s]
    dec = {}
    for a, b in [(1970, 1989), (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2025)]:
        x = r[(r.index.year >= a) & (r.index.year <= b)]
        dec[f"{a}-{str(b)[2:]}"] = f"{x.mean():.2f}" if len(x) > 12 else ""
    liq = ALT["ME>NYSE20p"].get(s)
    rows.append(dict(Sinyal=s, Yayin=int(d.Year), Agirlik=d["Stock Weight"], **dec,
                     **{"2010-25 ME>NYSE20p": f"{liq[liq.index.year >= 2010].mean():.2f}" if liq is not None else ""}))
md += ["\n#### PEAD/kazanc ve momentum sinyallerinin on yillara gore ortalama aylik LS getirisi (%/ay, maliyet oncesi)\n",
       md_table(pd.DataFrame(rows), pct_cols=())]

# --- yayin yilina gore bozulma: erken vs gec yayinlananlar
R["yayin_grup"] = pd.cut(R.year, [1970, 1995, 2005, 2016], labels=["<=1995", "1996-2005", "2006-2016"])
yg = R.groupby("yayin_grup", observed=True).agg(n=("sig", "size"), IS=("IS", "mean"), POST=("POST", "mean"), R10=("R10", "mean")).reset_index()
yg["POST/IS"] = yg.POST / yg.IS
for c in ["IS", "POST", "R10", "POST/IS"]:
    yg[c] = yg[c].map(lambda x: f"{x:.2f}")
md += ["\n#### Yayin donemine gore\n", md_table(yg, pct_cols=())]

# --- esit agirlikli tum-anomali portfoyu (her ay mevcut tum sinyallerin ortalamasi) yillik
ew = W[[c for c in W.columns if c in doc.index]].loc["1963":]
ewm = ew.mean(axis=1) / 100
ann = (1 + ewm).groupby(ewm.index.year).prod() - 1
blocks = {f"{a}-{b}": ann.loc[a:b].mean() for a, b in [(1963, 1979), (1980, 1999), (2000, 2009), (2010, 2019), (2020, 2025)]}
md += ["\n#### Tum anomalilerin esit agirlikli ortalamasi (her ay mevcut sinyaller), ortalama yillik getiri\n",
       md_table(pd.DataFrame([{k: fmt_pct(v) for k, v in blocks.items()}]), pct_cols=())]
open(os.path.join(OUT, "t3_tablolar.md"), "w").write("\n".join(md))
print("\n".join(md))
