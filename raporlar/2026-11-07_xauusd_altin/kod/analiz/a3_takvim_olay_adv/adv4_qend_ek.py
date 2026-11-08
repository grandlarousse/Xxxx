"""Hakem: QEND ek kontroller (Aralık ayrımı spot 2010-2026, geniş çeyrek başı penceresi). python3 -W ignore adv4_qend_ek.py"""
import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *
d = load_viop(); s = load_spot(); V = d.index; SPA = s.index
def tsimple(z): z = pd.Series(z).dropna(); return z.mean() / z.std() * np.sqrt(len(z))
def cal_pos(idx):
    g = pd.Series(np.arange(len(idx)), index=idx).groupby([idx.year, idx.month]); tdm = g.cumcount() + 1; n = g.transform("size"); return tdm.values, (n - tdm).values
tdm_s, tde_s = cal_pos(SPA); m_ok = SPA < "2026-11-01"
for lab, months in [("Aralık", [12]), ("Mar/Haz/Eyl", [3, 6, 9]), ("hepsi", [3, 6, 9, 12])]:
    Ds = pd.Series((np.isin(SPA.month, months) & (tde_s == 1) & m_ok).astype(float), index=SPA)
    for lo, hi in [(2010, 2016), (2017, 2026), (2010, 2026)]:
        m = (SPA.year >= lo) & (SPA.year <= hi); e = s.sfwd3[(Ds == 1) & m]; ne = s.sfwd3[(Ds == 0) & m]
        xx = e - ne.mean(); print(f"spot {lab:12s} {lo}-{hi}: n={len(e):2d} diff={xx.mean()*1e4:6.1f} t={tsimple(xx):5.2f} isabet={(e>0).mean():.2f}")
# geniş pencere: TDE1 girişinden 12 gün (yeni çeyreğin ~10. gününe kadar)
tdm, tde = cal_pos(V); qm = np.isin(V.month, [3, 6, 9, 12])
D = pd.Series((qm & (tde == 1)).astype(float), index=V)
for h in (3, 6, 9, 12):
    y = sum(d.v_ret.shift(-k) for k in range(1, h + 1)); e = y[D == 1]; ne = y[D == 0]
    out = []
    for lo, hi in [(2017, 2021), (2022, 2026)]:
        m = (e.index.year >= lo) & (e.index.year <= hi); mn = (ne.index.year >= lo) & (ne.index.year <= hi)
        out.append(f"{lo}-{hi} diff={(e[m]-ne[mn].mean()).mean()*1e4:.0f} t={tsimple(e[m]-ne[mn].mean()):.2f}")
    print(f"VİOP TDE1 giriş h={h:2d}: diff={(e-ne.mean()).mean()*1e4:6.1f} t={tsimple(e-ne.mean()):.2f} | " + " | ".join(out))
# fwd3 sonrası (gün 4..12) ayrı: olay penceresinden sonra devam mı
y = sum(d.v_ret.shift(-k) for k in range(4, 13)); e = y[D == 1]; ne = y[D == 0]
print(f"gün 4-12 katkısı: diff={(e-ne.mean()).mean()*1e4:.1f} t={tsimple(e-ne.mean()):.2f}")
# Spot 2010-2016 geniş pencere
Ds = pd.Series((np.isin(SPA.month, [3, 6, 9, 12]) & (tde_s == 1) & m_ok).astype(float), index=SPA)
for h in (3, 12):
    y = sum(s.s_ret.shift(-k) for k in range(1, h + 1)); m = SPA.year <= 2016
    e = y[(Ds == 1) & m]; ne = y[(Ds == 0) & m]; print(f"spot 2010-2016 h={h}: diff={(e-ne.mean()).mean()*1e4:.1f} t={tsimple(e-ne.mean()):.2f}")
