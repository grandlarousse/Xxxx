"""hisse ajanı — veri katmanı. Ortak kütüphane (ll.py) SALT OKUNUR kullanılır.
Çıktı (cache/): cc.parquet, gap.parquet, intra.parquet (BIST takvimi, 2014+ ; cc ayrıca 2005+ cc_long.parquet),
                tov.parquet (TL işlem hacmi = c*v), zero.parquet (sıfır getiri/işlem yok bayrağı), meta.json
Kullanım: nice -n 10 python3 hdata.py   (bir kez); diğer betikler hdata.load() çağırır.
"""
import sys, os, json, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ll, universe as U
HERE = os.path.dirname(os.path.abspath(__file__)); CACHE = os.path.join(HERE, "cache"); RES = os.path.join(HERE, "res")
OUT = SCR + "/out"
VIOP = list(U.VIOP)
IDX = ["XU100", "XU030", "XBANK", "XUSIN"]
START = "2014-01-01"; SPLIT = "2021-01-01"
# Resmi sektör endeksi (günlük veride yalnız XBANK ve XUSIN mevcut; diğerleri Yahoo'da yok)
BANKS = ["AKBNK", "GARAN", "HALKB", "ISCTR", "VAKBN", "YKBNK", "TSKB"]
XUSIN_MEM = ["AEFES", "ARCLK", "ASELS", "ASTOR", "BRSAN", "CIMSA", "EREGL", "FROTO", "GUBRF", "HEKTS", "KRDMD", "OYAKC",
             "PETKM", "SASA", "SISE", "TOASO", "TUPRS", "ULKER", "VESTL"]
def sector_index(t):
    return "XBANK" if t in BANKS else ("XUSIN" if t in XUSIN_MEM else None)

# Yaklaşık sektör etiketi (yorum ve ekonomik çiftler için; kümeleme veriden yapılır)
SECT = {}
for s in "AKBNK GARAN HALKB ISCTR VAKBN YKBNK TSKB ALBRK SKBNK QNBTR ICBCT KLNMA".split(): SECT[s] = "banka"
for s in "AKGRT ANHYT ANSGR TURSG ISMEN GARFA ISFIN KTLEV".split(): SECT[s] = "sigorta/finans"
for s in "KCHOL SAHOL ALARK DOHOL AGHOL GLYHO BINHO GRTHO RALYH VERUS INVEO BERA ECZYT BRYAT KUYAS".split(): SECT[s] = "holding"
for s in "EREGL KRDMD KRDMA KRDMB ISDMR BRSAN KCAER KBORU".split(): SECT[s] = "celik"
for s in "TRALT TRMET TRENJ CVKMD".split(): SECT[s] = "madencilik"
for s in "CIMSA OYAKC AKCNS NUHCM BUCIM AFYON BTCIM BSOKE GOLTS KONYA LMKDC".split(): SECT[s] = "cimento"
for s in "FROTO TOASO DOAS OTKAR TTRAK ASUZU KARSN BFREN EGEEN FMIZP JANTS DITAS BRISA KORDS PARSN TMSN KATMR".split(): SECT[s] = "otomotiv"
for s in "AKSEN ENJSA ODAS ZOREN AYDEM ENERY CANTE BIOEN GWIND IZENR AKFYE MOGAN ENTRA SAYAS TATEN".split(): SECT[s] = "enerji"
for s in "ASTOR EUPWR GESAN CWENE SMRTG ALFAS KONTR YEOTK".split(): SECT[s] = "enerji-ekipman"
for s in "TUPRS PETKM AYGAZ SASA AKSA ALKIM GUBRF BAGFS HEKTS EGGUB KMPUR".split(): SECT[s] = "kimya/petrol"
for s in "BIMAS MGROS SOKM MAVI VAKKO".split(): SECT[s] = "perakende"
for s in "ULKER AEFES CCOLA TUKAS TABGD BALSU KAYSE OBAMS YYLGD".split(): SECT[s] = "gida/icecek"
for s in "ARCLK VESTL VESBE".split(): SECT[s] = "dayanikli"
for s in "ASELS KAREL ARDYZ MIATK SDTTR ALTNY PATEK REEDR LILAK".split(): SECT[s] = "savunma/teknoloji"
for s in "TCELL TTKOM".split(): SECT[s] = "telekom"
for s in "THYAO PGSUS TAVHL CLEBI DOCO GRSEL PASEU TUREX".split(): SECT[s] = "ulastirma"
for s in "EKGYO ISGYO ALGYO AKFGY PEKGY PSGYO RYGYO SNGYO RGYAS DAPGM".split(): SECT[s] = "gyo"
for s in "ENKAI TKFEN BOBET QUAGR KLSER BIENY EUREN".split(): SECT[s] = "insaat/yapi"
for s in "SISE ISKPL".split(): SECT[s] = "cam/plastik"
for s in "BJKAS FENER GSRAY TSPOR".split(): SECT[s] = "spor"
for s in "SELEC MPARK ECILC".split(): SECT[s] = "saglik"
for s in "AGROT YIGIT".split(): SECT[s] = "diger"

def stock_list():
    c = pd.read_csv(SCR + "/data/catalog.csv")
    b = c[c.group.isin(["VIOP", "BIST_other"]) & (c.n > 0)]
    s = [x[:-3] for x in b.sym if not x.startswith("X")]
    return sorted(s)

def build():
    stocks = stock_list(); print("hisse sayısı", len(stocks))
    cal = ll.bist_cal(); cal = cal[cal >= pd.Timestamp("2005-01-01")]
    CC, GP, IN, TOV, VOL0 = {}, {}, {}, {}, {}
    for s in stocks + IDX:
        d = ll.decomp(s + ".IS").reindex(cal)
        CC[s] = d["cc"]; GP[s] = d["gap"]; IN[s] = d["intra"]
        r = ll.raw(s + ".IS"); r = r.copy(); r.index = pd.DatetimeIndex(r["ldate"].values); r = r[~r.index.duplicated(keep="last")]
        TOV[s] = (r["c"] * r["v"]).reindex(cal)
        VOL0[s] = (r["v"].fillna(0) <= 0).reindex(cal)
    cc = pd.DataFrame(CC); gap = pd.DataFrame(GP); intra = pd.DataFrame(IN); tov = pd.DataFrame(TOV)
    cc.to_parquet(os.path.join(CACHE, "cc_long.parquet"))
    st = pd.Timestamp(START)
    cc.loc[cc.index >= st].to_parquet(os.path.join(CACHE, "cc.parquet"))
    gap.loc[gap.index >= st].to_parquet(os.path.join(CACHE, "gap.parquet"))
    intra.loc[intra.index >= st].to_parquet(os.path.join(CACHE, "intra.parquet"))
    tov.to_parquet(os.path.join(CACHE, "tov.parquet"))
    # özet likidite
    t2 = tov.loc[tov.index >= pd.Timestamp("2021-01-01")]; t1 = tov.loc[(tov.index >= st) & (tov.index < pd.Timestamp(SPLIT))]
    c2 = cc.loc[cc.index >= st]
    liq = pd.DataFrame({"tov_med_oos_mnTL": t2.median() / 1e6, "tov_med_is_mnTL": t1.median() / 1e6,
                        "zero_frac": (c2 == 0).sum() / c2.notna().sum(), "nan_frac": c2.isna().mean(),
                        "n": c2.notna().sum(), "first": c2.apply(lambda x: x.first_valid_index())})
    liq["viop"] = liq.index.isin(VIOP); liq["sector"] = [SECT.get(s, "?") for s in liq.index]
    liq.to_csv(os.path.join(CACHE, "liq.csv"))
    print(liq.sort_values("tov_med_oos_mnTL").head(30).to_string())
    print(cc.shape, gap.shape)

def load():
    D = {k: pd.read_parquet(os.path.join(CACHE, k + ".parquet")) for k in ["cc", "gap", "intra"]}
    D["liq"] = pd.read_csv(os.path.join(CACHE, "liq.csv"), index_col=0)
    D["tov"] = pd.read_parquet(os.path.join(CACHE, "tov.parquet")).reindex(D["cc"].index)
    return D

if __name__ == "__main__":
    build()
