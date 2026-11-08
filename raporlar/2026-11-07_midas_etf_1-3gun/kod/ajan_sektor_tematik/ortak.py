"""sektor_tematik ailesi: ortak tanımlar (küme haritası, yardımcı istatistikler).
lib.py / strategies.py değiştirilmez; burada genişletilir."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_sektor_tematik")
os.makedirs(OUT, exist_ok=True)

FAM = ("XLK XLF XLE XLV XLI XLY XLP XLU XLB XLRE XLC SMH SOXX KRE KBE XBI IBB XOP OIH XME ITB XHB XRT JETS IGV "
       "CIBR ITA XAR PAVE IYT VNQ KIE IYR FDN SOXL SOXS TECL TECS FAS FAZ LABU LABD ERX ERY GUSH DRIP NAIL DFEN "
       "FNGU FNGD CURE RETL UTSL ARKK ARKG ARKW TAN ICLN URA URNM LIT REMX COPX BOTZ ROBO QTUM KWEB BLOK NLR UFO "
       "HACK SKYY MOO WCLD DRIV").split()

# Kopya / yakın kopya kümeleri (2023+ günlük getiri korelasyonu > ~0.93 veya aynı dayanak; kaldıraçlı/ters
# ürünler dayanağının kümesine konur). Küme = bağımsız kanıt birimi. İlk eleman = kümenin temsilcisi
# (en likit, kaldıraçsız).
CLUSTERS = {
    "teknoloji": ["XLK", "TECL", "TECS"],
    "yari_iletken": ["SMH", "SOXX", "SOXL", "SOXS"],
    "yazilim_internet": ["IGV", "SKYY", "WCLD", "FDN", "FNGU", "FNGD"],
    "siber": ["CIBR", "HACK"],
    "finans": ["XLF", "FAS", "FAZ"],
    "bolgesel_banka": ["KRE", "KBE"],
    "sigorta": ["KIE"],
    "enerji": ["XLE", "ERX", "ERY"],
    "petrol_arama": ["XOP", "GUSH", "DRIP"],
    "petrol_hizmet": ["OIH"],
    "saglik": ["XLV", "CURE"],
    "biyotek": ["XBI", "IBB", "LABU", "LABD"],
    "genomik": ["ARKG"],
    "sanayi": ["XLI", "PAVE"],
    "savunma": ["ITA", "XAR", "DFEN"],
    "ulasim": ["IYT"],
    "havayolu": ["JETS"],
    "tuketici_ihtiyari": ["XLY"],
    "perakende": ["XRT", "RETL"],
    "temel_tuketim": ["XLP"],
    "kamu_hizmet": ["XLU", "UTSL"],
    "malzeme": ["XLB"],
    "metal_madencilik": ["XME"],
    "bakir": ["COPX"],
    "nadir_toprak_lityum": ["REMX", "LIT"],
    "gayrimenkul": ["VNQ", "XLRE", "IYR"],
    "konut": ["ITB", "XHB", "NAIL"],
    "iletisim": ["XLC"],
    "temiz_enerji": ["TAN", "ICLN"],
    "uranyum_nukleer": ["URA", "URNM", "NLR"],
    "inovasyon_ark": ["ARKK", "ARKW"],
    "robotik": ["BOTZ", "ROBO", "DRIV"],
    "kuantum": ["QTUM"],
    "cin_internet": ["KWEB"],
    "blokzincir": ["BLOK"],
    "uzay": ["UFO"],
    "tarim": ["MOO"],
}
CL_OF = {s: k for k, v in CLUSTERS.items() for s in v}
assert set(CL_OF) == set(FAM), set(FAM) ^ set(CL_OF)
REPS = [v[0] for v in CLUSTERS.values()]

# kaldıraçlı/ters -> dayanak (sinyal için)
UNDER = {"SOXL": "SOXX", "SOXS": "SOXX", "TECL": "XLK", "TECS": "XLK", "FAS": "XLF", "FAZ": "XLF",
         "LABU": "XBI", "LABD": "XBI", "ERX": "XLE", "ERY": "XLE", "GUSH": "XOP", "DRIP": "XOP",
         "NAIL": "ITB", "DFEN": "ITA", "CURE": "XLV", "RETL": "XRT", "UTSL": "XLU", "FNGU": "FDN", "FNGD": "FDN"}
LEV = {"SOXL": 3, "SOXS": -3, "TECL": 3, "TECS": -3, "FAS": 3, "FAZ": -3, "LABU": 3, "LABD": -3, "ERX": 2,
       "ERY": -2, "GUSH": 2, "DRIP": -2, "NAIL": 3, "DFEN": 3, "CURE": 3, "RETL": 3, "UTSL": 3, "FNGU": 3, "FNGD": -3}

SPDR11 = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
# kaldıraçsız sektör + tematik (bağımsızlık için küme temsilcileri ayrıca)
UNLEV = [s for s in FAM if s not in LEV]


def cost_for(df, pos):
    """pos USD pozisyon için gidiş-dönüş maliyet (bp) = 2*1.5/pos + tahmini makas."""
    return 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(df)


def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))


def p_of(t, n):
    return lib.t_to_p(t, n)


def clustered_t(tr, key="W-FRI", col="net"):
    """Aile havuzu: işlem düzeyi ortalamanın küme-sağlam (CR1) t'si; küme = sinyal haftası (key='W-FRI')
    ya da ayı (key='M'). Aynı haftadaki farklı ETF işlemleri (kesitsel bağımlılık) tek küme sayılır.
    Dönüş: (t, küme sayısı, ortalama_bp)."""
    if tr is None or len(tr) < 3: return np.nan, 0, np.nan
    x = tr[col].values.astype(float); ok = np.isfinite(x)
    x = x[ok]
    d = pd.to_datetime(tr["sig_date"]).values[ok]
    g = pd.PeriodIndex(pd.DatetimeIndex(d), freq=key)
    m = x.mean(); N = len(x)
    s = pd.Series(x - m).groupby(g.astype(str).values).sum().values
    G = len(s)
    if G < 3: return np.nan, G, m * 1e4
    var = (G / (G - 1)) * (s ** 2).sum() / N ** 2
    return (m / math.sqrt(var) if var > 0 else np.nan), G, float(m * 1e4)


def week_mean_t(tr, col="net"):
    """Alternatif tahmin hedefi: her hafta eşit ağırlık (hafta ortalamalarının t'si)."""
    d = pd.to_datetime(tr["sig_date"])
    s = tr.groupby(d.dt.to_period("W-FRI").values)[col].mean()
    return tstat(s.values), len(s), float(s.mean() * 1e4)


def full_stats(df, sig, h, mode, pos=2500.0, exit_sig=None, label=""):
    cost = cost_for(df, pos)
    s, tr = lib.evaluate(df, sig, h, mode, cost, exit_sig=exit_sig, label=label)
    s["p"] = lib.t_to_p(s.get("t", np.nan), s.get("n", 0))
    return s, tr
