"""Black-76 / Black-Scholes yardımcıları (scipy yok; math.erf ile)."""
import math

def N(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def n(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

def b76(F, K, T, r, sig, cp):
    """Black-76: vadeli fiyat F üzerinden Avrupa opsiyonu. cp='C' veya 'P'. Prim endeks puanı."""
    DF = math.exp(-r * T)
    if T <= 0 or sig <= 0:
        return DF * max(0.0, (F - K) if cp == "C" else (K - F))
    s = sig * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * s * s) / s
    d2 = d1 - s
    if cp == "C":
        return DF * (F * N(d1) - K * N(d2))
    return DF * (K * N(-d2) - F * N(-d1))

def greeks76(F, K, T, r, sig, cp):
    """Delta (vadeliye göre, iskontolu), gamma, vega(1 vol puanı), theta (günlük)."""
    DF = math.exp(-r * T)
    s = sig * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * s * s) / s
    d2 = d1 - s
    delta = DF * N(d1) if cp == "C" else -DF * N(-d1)
    gamma = DF * n(d1) / (F * s)
    vega = DF * F * n(d1) * math.sqrt(T) / 100
    p = b76(F, K, T, r, sig, cp)
    theta = (b76(F, K, max(T - 1 / 365, 1e-9), r, sig, cp) - p)
    return dict(delta=delta, gamma=gamma, vega=vega, theta=theta, d2=d2)

def iv76(price, F, K, T, r, cp, lo=1e-4, hi=3.0):
    intrinsic = b76(F, K, T, r, 1e-9, cp)
    if price <= intrinsic + 1e-9:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if b76(F, K, T, r, mid, cp) > price:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def prob_above(F, K, T, sig):
    """Risk-nötr P(F_T > K) (lognormal, drift yok)."""
    s = sig * math.sqrt(T)
    d2 = (math.log(F / K) - 0.5 * s * s) / s
    return N(d2)
