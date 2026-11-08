"""Denetim: (1) günlük piyasa değerlemeli portföy (her hisseye 1/7) maxDD tarihleri; (2) C0'da RSI(2) eşiğe yakınlık
(kapanıştan dakikalar önce karar verilirken sinyalin dönme riski: RSI 7-10 arası sinyal ve 10-13 arası sinyal-olmayan günler).
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d8_dd_esik.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, dk
from d2_S1_yeniden import EXTRA
A = pd.read_csv(os.path.join(dk.OUT, "d2_islemler_C0.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
idx = dk.load_stock("AAPL").index; port = pd.Series(0.0, index=idx)
for st in dk.STK:
    sd = dk.load_stock(st); px = dk.synth(sd, extra_bp=EXTRA[st]); rc = px["c"].pct_change()
    for _, t in A[A.stock == st].iterrows():
        ie = idx.get_loc(t.entry_date); ix = idx.get_loc(t.exit_date)
        port.iloc[ie + 1:ix + 1] += rc.iloc[ie + 1:ix + 1].values / 7; port.loc[t.entry_date] -= t.cost_bp / 1e4 / 7
port = port.loc[A.sig_date.min():]; eq = (1 + port).cumprod(); dd = eq / eq.cummax() - 1
tmin = dd.idxmin(); tpk = eq.loc[:tmin].idxmax()
print(f"(1) günlük MTM maxDD {dd.min()*100:.1f}% tepe {tpk.date()} dip {tmin.date()}; 2020 dışı maxDD {dd[(dd.index.year!=2020)].min()*100:.1f}%")
for y in sorted(set(port.index.year)):
    e = (1 + port[port.index.year == y]).cumprod(); print(f"   {y}: getiri {(e.iloc[-1]-1)*100:6.1f}%  yıl içi maxDD {((e/e.cummax())-1).min()*100:6.1f}%")
near_sig = 0; nsig = 0; near_non = 0
for st in dk.STK:
    sd = dk.load_stock(st); c = sd["c"].values; r = dk.rsi_wilder(c, 2); tr = c > dk.sma(c, 200)
    s = (r < 10) & tr; nsig += s.sum(); near_sig += ((r >= 7) & (r < 10) & tr).sum(); near_non += ((r >= 10) & (r < 13) & tr).sum()
print(f"(2) trend üstü RSI2<10 günleri {nsig}; bunların RSI 7-10 arası (eşiğe yakın) {near_sig} ({near_sig/nsig*100:.0f}%); RSI 10-13 arası sinyal-olmayan {near_non}")
