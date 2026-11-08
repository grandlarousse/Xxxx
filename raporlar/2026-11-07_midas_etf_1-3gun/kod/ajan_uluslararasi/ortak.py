"""Uluslararası aile: ortak tanımlar (evren, kopya grupları, bağımsız temsilciler, yardımcılar).
lib.py / strategies.py DEĞİŞTİRİLMEZ; burada yalnız genişletilir."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_uluslararasi")
os.makedirs(OUT, exist_ok=True)

FAM = ["EEM","VWO","IEMG","EFA","VEA","IEFA","VGK","EZU","FXI","MCHI","ASHR","EWJ","DXJ","EWZ","EWW","INDA","EPI",
       "EWT","EWY","EWG","EWU","EWQ","EWI","EWP","EWC","EWA","EWH","EWS","EIDO","EPHE","THD","EZA","TUR","ARGT","EPOL",
       "ILF","EWM","VNM","ECH","EPU","KSA","EWL","EWN","EWD","GREK","EWK","EIS","QAT","UAE","EWO","NORW","EDEN","EFNL",
       "ENZL","KEMQ","CQQQ","CHIQ","YINN","YANG","EDC","EDZ","EURL","BRZU","INDL","MEXX","KORU","CHAU","CWEB"]

# Kopya / yakın kopya grupları (ilk eleman = temsilci). Kaldıraçlılar dayanağının grubunda.
GROUPS = {
    "EM_genis":   ["EEM", "VWO", "IEMG", "EDC", "EDZ"],
    "EAFE":       ["EFA", "VEA", "IEFA"],
    "Avrupa":     ["VGK", "EZU", "EURL"],
    "Cin_buyuk":  ["FXI", "MCHI", "YINN", "YANG"],
    "Cin_A":      ["ASHR", "CHAU"],
    "Cin_tekno":  ["CQQQ", "CWEB", "KEMQ"],    # CWEB dayanağı KWEB endeksi (KWEB başka ailede); KEMQ EM internet
    "Japonya":    ["EWJ", "DXJ"],
    "Brezilya":   ["EWZ", "BRZU", "ILF"],      # ILF ~%60 Brezilya
    "Meksika":    ["EWW", "MEXX"],
    "Hindistan":  ["INDA", "EPI", "INDL"],
    "Kore":       ["EWY", "KORU"],
}
SYM2GRP = {}
for g, v in GROUPS.items():
    for s in v: SYM2GRP[s] = g
for s in FAM:
    SYM2GRP.setdefault(s, s)
LEV = {"YINN": 3, "YANG": -3, "EDC": 3, "EDZ": -3, "EURL": 3, "BRZU": 2, "INDL": 2, "MEXX": 3, "KORU": 3, "CHAU": 2, "CWEB": 2}
UNDERLYING = {"YINN": "FXI", "YANG": "FXI", "EDC": "EEM", "EDZ": "EEM", "EURL": "VGK", "BRZU": "EWZ", "INDL": "INDA",
              "MEXX": "EWW", "KORU": "EWY", "CHAU": "ASHR", "CWEB": "KWEB"}

# Bağımsız 1x temsilciler (her kopya grubundan bir tane; kaldıraçlılar hariç)
def independent(min_dv=None):
    scr = screen()
    reps = []
    for s in FAM:
        if s in LEV: continue
        g = SYM2GRP[s]
        if g in GROUPS and GROUPS[g][0] != s: continue
        if min_dv is not None and scr.loc[s, "med_dollar_vol_m"] < min_dv: continue
        reps.append(s)
    return reps

# Bölge (eşzamansızlık derecesi): ABD seansıyla örtüşme
REGION = {}
for s in ["EWJ","DXJ","EWY","KORU","EWT","FXI","MCHI","YINN","YANG","ASHR","CHAU","CQQQ","CWEB","CHIQ","EWH","EWA","ENZL","EWS",
          "EWM","THD","EIDO","EPHE","VNM","INDA","EPI","INDL","KEMQ"]:
    REGION[s] = "asya"
for s in ["VGK","EZU","EURL","EWG","EWU","EWQ","EWI","EWP","EWL","EWN","EWD","EWK","EWO","NORW","EDEN","EFNL","GREK","EPOL",
          "TUR","EIS","EZA","KSA","QAT","UAE","EFA","VEA","IEFA"]:
    REGION[s] = "avrupa_ortadogu_afrika"   # yerel kapanış ~ ABD 10:00-11:30 ET; kısmi örtüşme
for s in ["EWZ","BRZU","ILF","EWW","MEXX","EWC","ARGT","ECH","EPU"]:
    REGION[s] = "amerika"                  # neredeyse tam örtüşme
for s in ["EEM","VWO","IEMG","EDC","EDZ"]:
    REGION[s] = "karma_em"

_SCR = None
def screen():
    global _SCR
    if _SCR is None:
        _SCR = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")
    return _SCR

_TV = None
def tv(sym):
    global _TV
    if _TV is None:
        a = pd.read_csv(os.path.join(ROOT, "sonuclar", "tv_etf.csv")).set_index("sym")
        _TV = a
    if sym in _TV.index and str(_TV.loc[sym, "durum"]).startswith("dogrulandi"):
        return _TV.loc[sym, "tv"]
    return None

def tv_ok_leaders():
    d = pd.read_csv(os.path.join(ROOT, "sonuclar", "tv_dogrulama.csv"))
    return set(d[d["durum"].isin(["dogrulandi", "dogrulandi_kanonik"])]["ticker"])

def cost_for(df, pos):
    """Gidiş-dönüş maliyet (bp) verilen pozisyon büyüklüğünde."""
    return 2 * lib.COMM_USD / pos * 1e4 + lib.spread_bp_tier(df)

def full_stats(df, sig, h, mode, exit_sig=None, label="", sym=""):
    """lib.evaluate + 1.000/10.000$ maliyet duyarlılığı."""
    out = {}
    s, tr = lib.evaluate(df, sig, h, mode, exit_sig=exit_sig, label=label)
    s["sym"] = sym
    for pos, nm in ((1000, "net_1000"), (10000, "net_10000")):
        c = cost_for(df, pos)
        s[nm + "_bp"] = s.get("mean_gross_bp", np.nan) - c if s.get("n", 0) else np.nan
    s["p"] = lib.t_to_p(s.get("t", np.nan), s.get("n", 0))
    return s, tr

def pooled(trs, h):
    """Aile havuzu: işlemler sinyal tarihine göre kümelenir (aynı gün işlem yapan ETF'lerin ortalaması = 1 gözlem);
    ortalama, Newey-West t (gecikme=h), IS/OOS, yıl pozitif oranı, PF. trs: sütunlar sig_date, net, gross, sym."""
    if trs is None or len(trs) == 0: return {"n_trades": 0}
    d = trs.groupby("sig_date").agg(net=("net", "mean"), gross=("gross", "mean"), k=("sym", "nunique")).sort_index()
    x = d["net"].values
    out = {"n_trades": len(trs), "n_dates": len(d), "k_etf": trs["sym"].nunique(), "mean_gross_bp": d["gross"].mean() * 1e4,
           "mean_net_bp": x.mean() * 1e4, "t_nw": nw_tstat(x, max(1, h)), "win_dates": float((x > 0).mean()),
           "per_trade_net_bp": trs["net"].mean() * 1e4, "worst_date_bp": x.min() * 1e4}
    isx = d[d.index <= lib.IS_END]["net"].values; oos = d[d.index > lib.IS_END]["net"].values
    out["is_n"] = len(isx); out["oos_n"] = len(oos)
    out["is_net_bp"] = isx.mean() * 1e4 if len(isx) else np.nan
    out["oos_net_bp"] = oos.mean() * 1e4 if len(oos) else np.nan
    out["is_t"] = nw_tstat(isx, max(1, h)) if len(isx) > 10 else np.nan
    out["oos_t"] = nw_tstat(oos, max(1, h)) if len(oos) > 10 else np.nan
    yrs = d.groupby(d.index.year)["net"].sum()
    out["years_pos_frac"] = float((yrs > 0).mean()) if len(yrs) else np.nan
    wins = x[x > 0].sum(); loss = -x[x < 0].sum()
    out["pf"] = wins / loss if loss > 0 else np.inf
    eq = np.cumprod(1 + x); out["maxdd"] = float((eq / np.maximum.accumulate(eq) - 1).min())
    return out

def nw_tstat(x, lags=3):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    if n < 10: return np.nan
    m = x.mean(); e = x - m
    s = (e @ e) / n
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); s += 2 * w * (e[l:] @ e[:-l]) / n
    return m / math.sqrt(s / n) if s > 0 else np.nan
