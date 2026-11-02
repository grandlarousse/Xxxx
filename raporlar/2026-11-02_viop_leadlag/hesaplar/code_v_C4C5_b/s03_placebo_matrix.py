"""s03: Plasebo matrisi. Asya sinyali D_t (07:00 / 08:00 UTC kapanış) x BIST gün-içi hedefi (47 VİOP hissesi + XU100 + XU030).
Soru 1: altın-dışı Asya sinyalleri de TRALT gün-içini 'tahmin ediyor' mu? (ortak Asya/risk faktörü veya açılış artefaktı)
Soru 2: altın sinyalleri (600547, 1787, 2899, 518880 altın ETF) altın-dışı hisseleri de tahmin ediyor mu?"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
VIOP = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()
TG = VIOP + ["XU100", "XU030"]
GOLD = ["600547.SS", "1787.HK", "2899.HK", "601899.SS", "518880.SS", "603993.SS", "3993.HK"]
NONG = ["000300.SS", "000001.SS", "600019.SS", "600028.SS", "601857.SS", "600585.SS", "600690.SS", "600104.SS", "601088.SS", "^HSI", "0700.HK", "0005.HK", "0939.HK", "1398.HK", "0941.HK", "2318.HK", "0883.HK", "0857.HK", "^N225", "^KS11", "^AXJO"]
rows = []
tg = {s: bist_dec(s + ".IS").intra for s in TG}
for sig in GOLD + NONG:
    try:
        Dt = to_bist(loc_ret(sig, "adj"), "zero")
    except Exception as e:
        print("yok", sig, e); continue
    Dt = Dt[Dt.index >= "2014-01-01"]
    for s in TG:
        b, t, n = nw_t(tg[s], Dt)
        rows.append(dict(sig=sig, gold=sig in GOLD, tgt=s, r=b, t=t, n=n))
R = pd.DataFrame(rows); R.to_csv(sys.path[0] + "/s03_placebo_matrix.csv", index=False)
P = R.pivot(index="tgt", columns="sig", values="t")
print("TRALT/TRMET satırı (t):")
print(P.loc[["TRALT", "TRMET", "XU100", "KRDMD", "EREGL"]].T.round(2).to_string())
print("\nHer sinyal için: TRALT t, diğer 46 hisse t medyan / %90 / maks, TRALT'ın sırası")
for sig in P.columns:
    o = P[sig].drop(["TRALT", "TRMET", "XU100", "XU030"])
    print(f"{sig:10s} gold={sig in GOLD!s:5s} TRALT t={P.at['TRALT', sig]:+.2f}  TRMET t={P.at['TRMET', sig]:+.2f} | diğer: med {o.median():+.2f} p90 {o.quantile(.9):+.2f} max {o.max():+.2f} ({o.idxmax()}) | #t>2: {(o>2).sum()}/{len(o)}")
print("\nTüm hedeflerde ortalama t: altın sinyalleri", R[R.gold].groupby("tgt").t.mean().sort_values().tail(8).round(2).to_dict())
print("Tüm hedeflerde ortalama t: altın-dışı", R[~R.gold].groupby("tgt").t.mean().sort_values().tail(8).round(2).to_dict())
print("Altın-dışı sinyallerin TRALT t dağılımı:", R[(~R.gold) & (R.tgt == "TRALT")].t.describe().round(2).to_dict())
print("Tüm 48 hedefte, altın-dışı sinyallerin t ortalaması (genel Asya->BIST gün-içi):", R[~R.gold].t.mean().round(2), " altın sinyalleri:", R[R.gold].t.mean().round(2))
