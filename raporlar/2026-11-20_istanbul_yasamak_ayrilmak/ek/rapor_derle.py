#!/usr/bin/env python3
"""Taslaktaki defter kimliklerini ([K03-07]) numaralı kaynaklara çevirir ve doğrulama partilerini hazırlar.

Kullanım:
  python3 rapor_derle.py derle  <taslak.md> <defter.json> <RAPOR.md>
  python3 rapor_derle.py parti  <taslak.md> <defter.json> <parti_klasoru> [parti_boyu=20]

- derle: [Kxx-yy] kimliklerini [n] biçimine çevirir, <!--KAYNAKLAR--> işaretine kaynak listesini yazar,
  gövde kelime sayısını (tablo ve kaynaklar hariç) bildirir.
- parti: taslakta kullanılan satırları kaynağa göre gruplayıp en çok parti_boyu satırlık JSON dosyalarına böler.
"""
import json
import os
import re
import sys

KIMLIK = re.compile(r"\[((?:K\d{2}-\d{2})(?:\s*,\s*K\d{2}-\d{2})*)\]")


def anahtar(url):
    u = url.strip().lower()
    u = re.sub(r"#.*$", "", u)
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u.rstrip("/")


def yukle(defter_yolu):
    return {s["id"]: s for s in json.load(open(defter_yolu, encoding="utf-8"))}


def kullanilan(taslak, defter):
    sira, bilinmeyen = [], []
    for m in KIMLIK.finditer(taslak):
        for k in re.split(r"\s*,\s*", m.group(1)):
            if k not in defter:
                bilinmeyen.append(k)
            elif k not in sira:
                sira.append(k)
    return sira, bilinmeyen


def derle(taslak_yolu, defter_yolu, cikti_yolu):
    taslak = open(taslak_yolu, encoding="utf-8").read()
    defter = yukle(defter_yolu)
    sira, bilinmeyen = kullanilan(taslak, defter)
    if bilinmeyen:
        print("BİLİNMEYEN KİMLİK:", sorted(set(bilinmeyen)))
        sys.exit(1)
    no, kaynaklar = {}, []
    for k in sira:
        a = anahtar(defter[k]["url"])
        if a not in no:
            no[a] = len(kaynaklar) + 1
            kaynaklar.append(defter[k])

    def degistir(m):
        ns = sorted({no[anahtar(defter[k]["url"])] for k in re.split(r"\s*,\s*", m.group(1))})
        return "[" + ", ".join(str(n) for n in ns) + "]"

    metin = KIMLIK.sub(degistir, taslak)
    liste = []
    for i, s in enumerate(kaynaklar, 1):
        ad = s["kaynak_adi"].replace("[", "(").replace("]", ")").strip()
        liste.append(f"{i}. [{ad}]({s['url'].strip()})")
    if "<!--KAYNAKLAR-->" not in metin:
        print("UYARI: <!--KAYNAKLAR--> işareti yok; liste sona eklendi")
        metin += "\n\n" + "\n".join(liste) + "\n"
    else:
        metin = metin.replace("<!--KAYNAKLAR-->", "\n".join(liste))
    open(cikti_yolu, "w", encoding="utf-8").write(metin)

    govde = metin.split("## Kaynaklar")[0]
    kelime = 0
    for satir in govde.splitlines():
        if satir.lstrip().startswith("|"):
            continue
        kelime += len(re.findall(r"[^\W\d_]{2,}", satir, flags=re.UNICODE))
    print(f"satır kimliği: {len(sira)} | kaynak: {len(kaynaklar)} | gövde kelime (tablo ve kaynak hariç): {kelime}")


def parti(taslak_yolu, defter_yolu, klasor, boy=20):
    taslak = open(taslak_yolu, encoding="utf-8").read()
    defter = yukle(defter_yolu)
    sira, bilinmeyen = kullanilan(taslak, defter)
    if bilinmeyen:
        print("BİLİNMEYEN KİMLİK:", sorted(set(bilinmeyen)))
        sys.exit(1)
    # Raporda geçtiği cümleyi de ekle (doğrulayıcı aşırı iddiayı görebilsin)
    cumle = {}
    for satir in taslak.splitlines():
        for m in KIMLIK.finditer(satir):
            for k in re.split(r"\s*,\s*", m.group(1)):
                cumle.setdefault(k, satir.strip()[:600])
    gruplar = {}
    for k in sira:
        gruplar.setdefault(anahtar(defter[k]["url"]), []).append(k)
    # Aynı kaynağın satırları aynı partide kalsın; kaynakları alan adına göre sırala
    sirali = sorted(gruplar.items(), key=lambda kv: (kv[0].split("/")[0], kv[0]))
    partiler, simdiki = [], []
    for _, ks in sirali:
        if simdiki and len(simdiki) + len(ks) > boy:
            partiler.append(simdiki)
            simdiki = []
        simdiki += ks
    if simdiki:
        partiler.append(simdiki)
    os.makedirs(klasor, exist_ok=True)
    for i, ks in enumerate(partiler, 1):
        veri = [{"id": k, "iddia": defter[k]["iddia"], "kaynak_adi": defter[k]["kaynak_adi"], "url": defter[k]["url"],
                 "alinti": defter[k]["alinti"], "uretici_gordu": defter[k]["gorulen"], "raporda_gectigi_yer": cumle.get(k, "")}
                for k in ks]
        json.dump(veri, open(os.path.join(klasor, f"parti_{i:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"kullanılan satır: {len(sira)} | kaynak: {len(gruplar)} | parti: {len(partiler)} | boylar: {[len(p) for p in partiler]}")


if __name__ == "__main__":
    komut = sys.argv[1]
    if komut == "derle":
        derle(*sys.argv[2:5])
    elif komut == "parti":
        parti(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 20)
    else:
        print(__doc__)
