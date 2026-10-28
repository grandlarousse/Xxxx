"""BIST30 opsiyonlarının işlem (kapanış/AOF) ve uzlaşma fiyatlarından ima edilen volatilite.
Kaynak: Borsa İstanbul günlük VİOP bülteni CSV. Kullanım: python3 -I iv_surface.py <csv> [r]
"""
import csv, sys, datetime as dt, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs import iv76

path = sys.argv[1]
r = float(sys.argv[2]) if len(sys.argv) > 2 else 0.36
rows = []
with open(path, encoding="windows-1254", errors="replace") as f:
    rd = csv.reader(f, delimiter=";")
    hdr = [h.strip() for h in next(rd)]; next(rd)
    for x in rd:
        if len(x) >= 23:
            rows.append(dict(zip(hdr, x)))
fl = lambda s: float(s) if s not in ("", None) else 0.0
tdate = dt.date.fromisoformat(rows[0]["TARIH"])
fut = {x["VADE TARIHI"]: x for x in rows if x["SOZLESME KODU"].startswith("F_XU030")}
print("Tarih", tdate, "r", r)
for exp in sorted(fut):
    fx = fut[exp]
    Fs, Fc = fl(fx["UZLASMA FIYATI"]), fl(fx["KAPANIS FIYATI"]) or fl(fx["UZLASMA FIYATI"])
    T = (dt.date.fromisoformat(exp) - tdate).days / 365
    print(f"\nVade {exp} T={T:.4f}  vadeli uzl {Fs} kapanış {Fc}")
    print(f"{'Strike':>7s} {'T':1s} {'uzl':>8s} {'IVuzl':>6s} {'kap':>8s} {'IVkap':>6s} {'AOF':>8s} {'IVaof':>6s} {'adet':>6s} {'AP':>6s}")
    opts = [x for x in rows if x["SOZLESME KODU"].startswith("O_XU030E") and x["VADE TARIHI"] == exp]
    opts.sort(key=lambda x: (x["SOZLESME KODU"][12], float(x["SOZLESME KODU"][13:])))
    for o in opts:
        code = o["SOZLESME KODU"]; cp = code[12]; K = float(code[13:])
        if abs(K / Fs - 1) > 0.12:
            continue
        us, cl, vw = fl(o["UZLASMA FIYATI"]), fl(o["KAPANIS FIYATI"]), fl(o["AGIRLIKLI ORTALAMA FIYAT"])
        ivs = iv76(us, Fs, K, T, r, cp)
        ivc = iv76(cl, Fc, K, T, r, cp) if cl > 0 else float("nan")
        ivv = iv76(vw, Fc, K, T, r, cp) if vw > 0 else float("nan")
        print(f"{K:7.0f} {cp} {us:8.2f} {ivs*100:6.1f} {cl:8.2f} {ivc*100:6.1f} {vw:8.2f} {ivv*100:6.1f} {o['ISLEM MIKTARI']:>6s} {o['ACIK POZISYON']:>6s}")
