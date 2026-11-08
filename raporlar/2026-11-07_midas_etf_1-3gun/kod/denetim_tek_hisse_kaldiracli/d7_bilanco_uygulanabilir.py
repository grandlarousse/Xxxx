"""Denetim: ajanın 'bilanço hariç' (C0 +84 bp, t 2,44) sonucu GERÇEKLEŞEN tutuşa göre filtreliyor (çıkış günü ileriki fiyata bağlı:
erken çıkan işlem tutulur, bilançoya taşınan atılır -> hafif ileriye bakma). Uygulanabilir iki muhafazakâr varyant:
 (a) ATLA: tepki günü (R) t+1..t+3 penceresindeyse (takvim önceden bilinir) sinyali alma;
 (b) ERKEN ÇIK: gir, ama R'den önceki gün (duyuru günü E) kapanışında çık (SMA5 çıkışı daha önce gelmediyse).
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d7_bilanco_uygulanabilir.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
import numpy as np, pandas as pd
import dk
from d2_S1_yeniden import earn_react_days, EXTRA

def main():
    R = earn_react_days()
    for mode in ("C0", "O1"):
        for var in ("ana", "atla", "erken_cik"):
            rows = []
            for st in dk.STK:
                sd = dk.load_stock(st); px = dk.synth(sd, extra_bp=EXTRA[st]); idx = sd.index
                sig = dk.signal(sd).copy(); exc = dk.exit_cond(sd).copy()
                react = np.array([d in R.get(st, set()) for d in idx])
                if var == "atla":
                    for i in np.where(sig)[0]:
                        if react[i + 1:i + 4].any(): sig[i] = False
                    tr = dk.sim(sig, exc, px["c"].values, px["o"].values, mode, 3)
                elif var == "erken_cik":
                    # tepki gününden önceki gün (E) zorunlu çıkış koşulu: exc[E] = True
                    exc2 = exc.copy(); ri = np.where(react)[0]; exc2[ri[ri > 0] - 1] = True
                    tr = dk.sim(sig, exc2, px["c"].values, px["o"].values, mode, 3)
                    # O1'de giriş günü = E ise (gün içi tutuş) kabul edilir
                else:
                    tr = dk.sim(sig, exc, px["c"].values, px["o"].values, mode, 3)
                c_bp = dk.cost(dk.ETF[st])
                for (i, e, x, g) in tr: rows.append((st, idx[i], g, g - c_bp / 1e4, x - e))
            A = pd.DataFrame(rows, columns=["stock", "sig_date", "gross", "net", "days"])
            s = dk.summary(A)
            print(f"  [{mode}] {var:9s}: n {s['n']} net {s['net_bp']:.1f} t {s['t']:.2f} IS {s['is_bp']:.1f} ({s['is_t']:.2f}) OOS {s['oos_bp']:.1f} ({s['oos_t']:.2f}) "
                  f"yıl+ (tarih) {s['yil_poz_tarih']:.2f} (işlem) {s['yil_poz_islem']:.2f} en kötü {s['en_kotu_bp']:.0f}")

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(dk.OUT, "d7_cikti.txt"), "w").write(txt)
