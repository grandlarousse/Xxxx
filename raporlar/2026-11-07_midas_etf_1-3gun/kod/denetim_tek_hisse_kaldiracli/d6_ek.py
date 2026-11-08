"""Denetim ek testleri:
(1) Kaçırılan araç: S1 sinyalini doğrudan HİSSEYLE uygulamak (Midas'ta ABD hisseleri kesin var; ETF bulunurluğu doğrulanmadı).
    1x hisse, maliyet 2x1,5$/pozisyon + 1 bp makas; 2.500$ ve 5.000$ (5.000$ hisse = 2.500$ 2x ETF ile aynı dolar maruziyeti).
(2) AMZN/GOOGL <- SPY negatif gecikme bulgusunun tek hisse kuralı: SPY günlük getirisi < -1 sd (60g, t'ye kadar) -> 2x long C0, 1 gün.
(3) Güncel durum (06.11.2026 kapanışı) bağımsız RSI ile.
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d6_ek.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib, math
import numpy as np, pandas as pd
import dk, lib
EXTRA = {"NVDA": 2.84, "TSLA": 2.75, "AAPL": 1.28, "AMZN": 2.13, "META": 1.80, "MSFT": 1.10, "GOOGL": 1.55}

def main():
    print("(1) S1 sinyali, işlem aracı HİSSENİN KENDİSİ (1x):")
    for mode in ("C0", "O1"):
        for pos in (2500.0, 5000.0):
            rows = []
            for st in dk.STK:
                sd = dk.load_stock(st); px = sd[["o", "c"]]
                tr = dk.sim(dk.signal(sd), dk.exit_cond(sd), px["c"].values, px["o"].values, mode, 3)
                cst = 2 * 1.5 / pos * 1e4 + 1.0
                for (i, e, x, g) in tr: rows.append((st, sd.index[i], g, g - cst / 1e4, x - e))
            A = pd.DataFrame(rows, columns=["stock", "sig_date", "gross", "net", "days"])
            s = dk.summary(A)
            print(f"  [{mode}] {int(pos)}$: n {s['n']} brüt {s['brut_bp']:.1f} net {s['net_bp']:.1f} t {s['t']:.2f} IS {s['is_bp']:.1f} ({s['is_t']:.2f}) OOS {s['oos_bp']:.1f} ({s['oos_t']:.2f}) "
                  f"en kötü {s['en_kotu_bp']:.0f} | dolar başına net (5.000$ hisse ~ 2.500$ 2x): {s['net_bp'] * pos / 2500:.1f} bp/2.500$")
    print("  Karşılaştırma: 2x ETF 2.500$ C0 net 111,0 bp/2.500$ (sentetik, swap sürüklemesi dahil); 5.000$ hisse ile aynı maruziyet ~2x net bp/5.000$.")

    print("\n(2) SPY sert düşüş günü (r_SPY < -1 sd60) -> tek hisse 2x long C0, 1 gün (sentetik 2x, 16 bp):")
    spy = lib.load("SPY")["c"]; r = np.log(spy).diff(); z = r / r.rolling(60).std()
    for st in ("AMZN", "GOOGL", "AAPL", "MSFT"):
        sd = dk.load_stock(st); px = dk.synth(sd, extra_bp=EXTRA[st])
        for thr in (-1.0, -1.5, -2.0):
            sig = (z.reindex(sd.index) < thr).values.copy()
            sig[:200] = False
            for mode in ("C0", "O1"):
                tr = dk.sim(sig, None, px["c"].values, px["o"].values, mode, 1)
                g = np.array([x[3] for x in tr]); net = g - 16 / 1e4
                d = np.array([sd.index[x[0]] for x in tr]); isn = d <= dk.IS_END
                print(f"  {st:5s} z<{thr:+.1f} [{mode}] n {len(g):3d} net {net.mean() * 1e4:6.1f} t {dk.tstat(net):5.2f} IS {net[isn].mean() * 1e4:6.1f} OOS {net[~isn].mean() * 1e4:6.1f}")

    print("\n(3) Güncel durum (son veri):")
    for st in dk.STK:
        sd = dk.load_stock(st); c = sd["c"].values
        r2 = dk.rsi_wilder(c, 2)[-1]; m200 = dk.sma(c, 200)[-1]; m5 = dk.sma(c, 5)[-1]
        print(f"  {st:5s} {sd.index[-1].date()} kapanış {c[-1]:8.2f} RSI2 {r2:5.1f} SMA200 {m200:8.2f} ({'üstünde' if c[-1] > m200 else 'ALTINDA'}) SMA5 {m5:8.2f}")

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(dk.OUT, "d6_cikti.txt"), "w").write(txt)
