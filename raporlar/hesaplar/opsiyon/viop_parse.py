"""Borsa İstanbul günlük VİOP bülteni (viop_YYYYMMDD.csv) ayrıştırıcı.
Kaynak: https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv
Kullanım: python3 -I viop_parse.py <csv> [--chain]
"""
import csv, sys, collections

path = sys.argv[1]
show_chain = "--chain" in sys.argv
rows = []
with open(path, encoding="windows-1254", errors="replace") as f:
    rd = csv.reader(f, delimiter=";")
    hdr = next(rd); next(rd)
    for r in rd:
        if len(r) < 23:
            continue
        rows.append(dict(zip([h.strip() for h in hdr], r)))

def fl(x):
    try:
        return float(x)
    except Exception:
        return 0.0

date = rows[0]["TARIH"]
# Ürün bazında toplamlar
agg = collections.defaultdict(lambda: [0, 0.0, 0.0, 0, 0, 0])  # seri sayısı, işlem hacmi TL, prim hacmi, miktar, işlem sayısı, açık poz
for r in rows:
    code = r["SOZLESME KODU"]
    if code.startswith("O_XU030") or code.startswith("O_XU030M"):
        key = "BIST30 opsiyon" if not code.startswith("O_XU030M") else "Mini BIST30 opsiyon"
    elif code.startswith("F_XU030"):
        key = "BIST30 vadeli"
    elif code.startswith("O_USDTRY"):
        key = "USDTRY opsiyon"
    elif code.startswith("O_"):
        key = "Pay opsiyon"
    elif code.startswith("F_USDTRY"):
        key = "USDTRY vadeli"
    elif code.startswith("F_"):
        key = "Diğer vadeli"
    else:
        key = "Diğer"
    a = agg[key]
    a[0] += 1; a[1] += fl(r["ISLEM HACMI"]); a[2] += fl(r["PRIM HACMI"]); a[3] += int(fl(r["ISLEM MIKTARI"])); a[4] += int(fl(r["ISLEM SAYISI"])); a[5] += int(fl(r["ACIK POZISYON"]))
print("Tarih", date)
print(f"{'Ürün':22s} {'seri':>5s} {'İşl.hacmi mnTL':>14s} {'Prim mnTL':>10s} {'Sözleşme':>10s} {'İşlem#':>8s} {'AçıkPoz':>10s}")
for k, a in sorted(agg.items(), key=lambda x: -x[1][1]):
    print(f"{k:22s} {a[0]:5d} {a[1]/1e6:14.1f} {a[2]/1e6:10.2f} {a[3]:10d} {a[4]:8d} {a[5]:10d}")

# BIST30 vadeli
print("\nBIST30 vadeli:")
for r in rows:
    if r["SOZLESME KODU"].startswith("F_XU030"):
        print(r["SOZLESME KODU"], r["VADE TARIHI"], "uzl", r["UZLASMA FIYATI"], "önc", r["ONCEKI UZLASMA FIYATI"], "kap", r["KAPANIS FIYATI"], "L/H", r["EN DUSUK FIYAT"], r["EN YUKSEK FIYAT"], "hacim mnTL", round(fl(r["ISLEM HACMI"]) / 1e6, 1), "adet", r["ISLEM MIKTARI"], "AP", r["ACIK POZISYON"])

if show_chain:
    print("\nBIST30 opsiyon zinciri (yalnız AP>0 veya işlem>0):")
    ch = [r for r in rows if r["SOZLESME KODU"].startswith("O_XU030")]
    ch.sort(key=lambda r: (r["VADE TARIHI"], r["SOZLESME KODU"]))
    for r in ch:
        if fl(r["ACIK POZISYON"]) > 0 or fl(r["ISLEM MIKTARI"]) > 0 or "1226" in r["SOZLESME KODU"] or "1126" in r["SOZLESME KODU"]:
            print(f"{r['SOZLESME KODU']:28s} vade {r['VADE TARIHI']} uzl {r['UZLASMA FIYATI']:>9s} önc {r['ONCEKI UZLASMA FIYATI']:>9s} kap {r['KAPANIS FIYATI']:>8s} vwap {r[' AGIRLIKLI ORTALAMA FIYAT'] if ' AGIRLIKLI ORTALAMA FIYAT' in r else r.get('AGIRLIKLI ORTALAMA FIYAT',''):>8s} adet {r['ISLEM MIKTARI']:>6s} işl# {r['ISLEM SAYISI']:>4s} AP {r['ACIK POZISYON']:>6s} prim {fl(r['PRIM HACMI'])/1e3:8.1f}k")
    # Pay opsiyonlarında en çok AP
    po = [r for r in rows if r["SOZLESME KODU"].startswith("O_") and not r["SOZLESME KODU"].startswith("O_XU030") and not r["SOZLESME KODU"].startswith("O_USDTRY")]
    byund = collections.defaultdict(lambda: [0, 0, 0.0])
    for r in po:
        u = r["DAYANAK VARLIK"]
        byund[u][0] += int(fl(r["ACIK POZISYON"])); byund[u][1] += int(fl(r["ISLEM MIKTARI"])); byund[u][2] += fl(r["PRIM HACMI"])
    print("\nPay opsiyonları (dayanak: AP, işlem adedi, prim TL) ilk 12:")
    for u, v in sorted(byund.items(), key=lambda x: -x[1][0])[:12]:
        print(u, v[0], v[1], round(v[2]))
