"""Aile: tek_hisse_kaldiracli — ortak yardımcılar (lib.py / strategies.py DEĞİŞTİRİLMEZ, yalnız kullanılır).

Zamanlama: lib.py ZAMANLAMA SÖZLEŞMESİ'ne uyulur (sinyal t kapanışına kadarki bilgi; C0/O1/C1).
Dayanak hisseler data/stock/<SYM>.parquet (Nasdaq, bölünme düzeltmeli, temettüsüz o/h/l/c/v).
Sentetik kaldıraçlı ETF: günlük sıfırlamalı L x dayanak, (ücret + finansman) sürüklemesi düşülerek
kurulur; açılış/yüksek/düşük önceki kapanışa göre L katı ölçeklenir. Böylece kurallar 2016+ dönemde
(IS 2016-11..2021, OOS 2022..2026-11) test edilip gerçek ETF verisiyle (2022+) karşılaştırılır.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
ROOT = os.path.dirname(KOD)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib
import strategies

OUT = os.path.join(ROOT, "sonuclar", "aile_tek_hisse_kaldiracli")
os.makedirs(OUT, exist_ok=True)

FAM = ["NVDL", "TSLL", "MSTU", "CONL", "NVDU", "TSLQ", "NVDS", "AAPU", "AMZU", "METU", "MSFU", "GGLL"]
UNDER = {"NVDL": "NVDA", "NVDU": "NVDA", "NVDS": "NVDA", "TSLL": "TSLA", "TSLQ": "TSLA", "MSTU": "MSTR",
         "CONL": "COIN", "AAPU": "AAPL", "AMZU": "AMZN", "METU": "META", "MSFU": "MSFT", "GGLL": "GOOGL"}
# Dayanak başına birincil (en likit/ucuz) uzun 2x ETF; bağımsız kanıt birimi = dayanak hisse
PRIMARY = {"NVDA": "NVDL", "TSLA": "TSLL", "MSTR": "MSTU", "COIN": "CONL", "AAPL": "AAPU", "AMZN": "AMZU",
           "META": "METU", "MSFT": "MSFU", "GOOGL": "GGLL"}
STOCKS = list(PRIMARY)
INVERSE = ["TSLQ", "NVDS"]
TV_STOCK = {"NVDA": "NASDAQ:NVDA", "TSLA": "NASDAQ:TSLA", "MSTR": "NASDAQ:MSTR", "COIN": "NASDAQ:COIN",
            "AAPL": "NASDAQ:AAPL", "AMZN": "NASDAQ:AMZN", "META": "NASDAQ:META", "MSFT": "NASDAQ:MSFT",
            "GOOGL": "NASDAQ:GOOGL"}
COST_LEVELS = {"1000": 1000.0, "2500": 2500.0, "10000": 10000.0}

_tarama = None
def tarama():
    global _tarama
    if _tarama is None:
        _tarama = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")
    return _tarama

def spread_bp(etf):
    return float(tarama().loc[etf, "spread_bp"])

def cost_for(etf, pos=2500.0):
    """Gidiş-dönüş maliyet bp: 2 x 1,5 USD komisyon / pozisyon + tarama.csv makas tahmini."""
    return 2 * lib.COMM_USD / pos * 1e4 + spread_bp(etf)

def load_stock(sym):
    df = pd.read_parquet(os.path.join(ROOT, "data", "stock", sym + ".parquet"))
    df = df[df["c"] > 0].copy()
    o = df["o"].where(df["o"] > 0).fillna(df["c"].shift(1)).fillna(df["c"])
    h = pd.concat([df["h"].where(df["h"] > 0).fillna(df["c"]), o, df["c"]], axis=1).max(axis=1)
    l = pd.concat([df["l"].where(df["l"] > 0).fillna(df["c"]), o, df["c"]], axis=1).min(axis=1)
    out = pd.DataFrame({"o": o, "h": h, "l": l, "c": df["c"], "raw_c": df["c"], "v": df["v"]}, index=df.index)
    out["dv"] = out["c"] * out["v"]; out["div"] = 0.0
    return out

_rf = None
def rf_daily(idx):
    global _rf
    if _rf is None:
        s = lib.fred("DGS3MO")
        _rf = (s / 100.0).dropna() if s is not None else pd.Series(dtype=float)
    r = _rf.reindex(idx, method="ffill").fillna(0.02) if len(_rf) else pd.Series(0.02, index=idx)
    return r / 252.0

# Gerçek ETF'in (2x döneminde) sentetiğe göre ek günlük geri kalışı (bp/gün; t1 doğrulaması, kapanıştan kapanışa ort. fark).
# Yalnız maliyet düzeyini kalibre eder (sinyali etkilemez); sentetik dayanak testini muhafazakâr yapar.
EXTRA_DRAG_BP = {"NVDA": 2.8, "TSLA": 2.7, "MSTR": 13.0, "COIN": 5.1, "AAPL": 1.3, "AMZN": 2.1, "META": 1.8,
                 "MSFT": 1.1, "GOOGL": 1.6}

def synth_letf(sdf, L=2.0, fee_ann=0.0105, spread_fin=0.005, extra_bp=0.0):
    """Günlük sıfırlamalı sentetik L x ETF (OHLC). Sürükleme: (gider oranı + (L-1)*(rf+swap marjı))/252 (L>0);
    L<0 için nakit teminat ~rf kazanır, swap marjı |L|*marj ödenir. extra_bp: kalibre ek günlük sürükleme
    (gece/açılışa yüklenir, çünkü gerçek farkın çoğu açılış boşluğunda görülüyor)."""
    c = sdf["c"]; pc = c.shift(1)
    rf = rf_daily(sdf.index)
    if L > 0:
        drag = fee_ann / 252 + (L - 1) * (rf + spread_fin / 252)
    else:
        drag = fee_ann / 252 + abs(L) * spread_fin / 252 - rf  # ters: nakit teminat ~ rf kazanır, swap marjı ödenir
    drag = drag + extra_bp / 1e4
    r = (c / pc - 1) * L - drag
    r.iloc[0] = 0.0
    P = 100 * (1 + r).cumprod()
    Pp = P.shift(1).fillna(100.0)
    o = Pp * (1 + L * (sdf["o"] / pc - 1) - drag).fillna(1.0)
    if L > 0:
        h = Pp * (1 + L * (sdf["h"] / pc - 1) - drag); l = Pp * (1 + L * (sdf["l"] / pc - 1) - drag)
    else:
        h = Pp * (1 + L * (sdf["l"] / pc - 1) - drag); l = Pp * (1 + L * (sdf["h"] / pc - 1) - drag)
    o = o.clip(lower=1e-6); h = h.fillna(P).clip(lower=1e-6); l = l.fillna(P).clip(lower=1e-6)
    h = pd.concat([h, o, P], axis=1).max(axis=1); l = pd.concat([l, o, P], axis=1).min(axis=1)
    out = pd.DataFrame({"o": o, "h": h, "l": l, "c": P, "raw_c": P, "v": sdf["v"], "dv": sdf["dv"], "div": 0.0},
                       index=sdf.index)
    out.iloc[0, out.columns.get_loc("o")] = 100.0
    return out

def synth_for(stock, L=2.0):
    """Kalibre sentetik 2x (birincil ETF'e göre)."""
    return synth_letf(load_stock(stock), L, extra_bp=EXTRA_DRAG_BP.get(stock, 0.0) if L > 0 else 0.0)

def ctx():
    """strategies.LIB için VIX/VIX3M bağlamı."""
    return {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}

def p_of(t, n):
    return lib.t_to_p(t, n)

def full_stats(df, sig, h, mode, cost, exit_sig=None, label=""):
    s, tr = lib.evaluate(df, sig, h=h, mode=mode, cost=cost, exit_sig=exit_sig, label=label)
    s["p"] = p_of(s.get("t", np.nan), s.get("n", 0))
    return s, tr

def pooled_date_t(trs, col="net"):
    """Birden çok dayanaktaki işlemleri tarih kümelemeli birleştir: aynı sinyal tarihindeki işlemlerin ortalaması
    tek gözlem sayılır (dayanaklar arası eşzamanlı korelasyonu cezalandırır). Dönüş: (n_islem, n_tarih, ort_bp, t)."""
    trs = [t for t in trs if t is not None and len(t)]
    if not trs: return 0, 0, np.nan, np.nan
    a = pd.concat(trs, ignore_index=True)
    if len(a) < 3: return len(a), len(a), np.nan, np.nan
    g = a.groupby("sig_date")[col].mean()
    m = g.mean(); sd = g.std(ddof=1)
    t = m / (sd / math.sqrt(len(g))) if sd > 0 else np.nan
    return len(a), len(g), m * 1e4, t

def year_pos(tr):
    if tr is None or len(tr) == 0: return np.nan
    y = tr.groupby(tr["sig_date"].dt.year)["net"].sum()
    return float((y > 0).mean())

def stats_from_trades(tr, cost_bp_new=None, cost_bp_old=None):
    """Hazır işlem tablosundan özet (maliyet değiştirilebilir)."""
    if tr is None or len(tr) == 0: return {"n": 0}
    t2 = tr.copy()
    if cost_bp_new is not None:
        t2["net"] = t2["gross"] - cost_bp_new / 1e4
    s = lib.stats(t2)
    s["p"] = p_of(s.get("t", np.nan), s.get("n", 0))
    return s
