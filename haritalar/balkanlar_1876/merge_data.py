#!/usr/bin/env python3
"""Bölge veri setlerini birleştirir ve bölge sınırlarındaki çift sayımları ayıklar.

Kullanım: python3 merge_data.py kaynak1.json kaynak2.json ... -o data/
Her dosya {"region", "clusters", "vilayet_stats", "sources", ...} biçiminde.
Bölgelerin kapsamı kesiştiği yerlerde (ör. Drama sancağı: Edirne ↔ Makedonya,
Niş sancağı: Tuna ↔ Bosna/Kosova) aynı yeri anlatan kümeler, sancak sahibi
bölgede bırakılır.
"""
import argparse
import json
import math
import os
import re

# sancak (küçük harf, ilk kelime) -> veri sahibi bölge anahtarı
OWNER = {
    "drama": "makedonya", "selanik": "makedonya", "serez": "makedonya", "üsküp": "makedonya",
    "manastır": "makedonya", "görice": "arnavut_yunan", "elbasan": "arnavut_yunan",
    "niş": "tuna", "sofya": "tuna", "prizren": "bosna_kosova", "yenipazar": "bosna_kosova",
    "gümülcine": "edirne", "filibe": "edirne",
}


# (bölge, sancak) -> bu isim kalıbına uyan kümeler o bölgede kalabilir
EXCEPT = {("bosna_kosova", "niş"): r"vran|ivran|preşev|bujanov"}


def key_of(path):
    b = os.path.basename(path).replace(".json", "")
    return re.sub(r"^(revise|research|verify)_", "", b)


def dist_km(a, b):
    dy = (a["lat"] - b["lat"]) * 111.2
    dx = (a["lon"] - b["lon"]) * 111.2 * math.cos(math.radians((a["lat"] + b["lat"]) / 2))
    return math.hypot(dx, dy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", default="data")
    a = ap.parse_args()
    sets = {key_of(p): json.load(open(p, encoding="utf-8")) for p in a.files}
    for k, d in sets.items():
        for c in d["clusters"]:
            c["_region"] = k
    # bir bölgenin, başka bölgenin sahip olduğu sancakta kalan kümeleri
    # (isimde istisna kalıbı yoksa) doğrudan atılır
    for k, d in sets.items():
        kept = []
        for c in d["clusters"]:
            s = (c.get("sancak") or "").lower().split()
            s = s[0] if s else ""
            own = OWNER.get(s)
            exc = EXCEPT.get((k, s))
            covered = own in sets and any(dist_km(c, o) < max(15, 0.9 * c["radius_km"]) for o in sets[own]["clusters"])
            if own and own != k and covered and not (exc and re.search(exc, c["name"].lower())):
                print(f"sancak sahibi {own}: [{k}] {c['name']} atıldı")
                continue
            kept.append(c)
        d["clusters"] = kept
    allc = [c for d in sets.values() for c in d["clusters"]]
    drop = set()
    for i, c1 in enumerate(allc):
        for j in range(i + 1, len(allc)):
            c2 = allc[j]
            if c1["_region"] == c2["_region"]:
                continue
            d = dist_km(c1, c2)
            if d > 0.55 * min(c1["radius_km"], c2["radius_km"]) + 4:
                continue
            # aynı yer: sancak sahibine göre karar ver
            s1 = (c1.get("sancak") or "").lower().split()[0] if c1.get("sancak") else ""
            s2 = (c2.get("sancak") or "").lower().split()[0] if c2.get("sancak") else ""
            own = OWNER.get(s1) or OWNER.get(s2)
            if own == c1["_region"]:
                loser = j
            elif own == c2["_region"]:
                loser = i
            else:
                # sahibi bilinmiyorsa küçük nüfuslu/az güvenilir olanı at
                loser = j if (c1.get("population", 0) >= c2.get("population", 0)) else i
            drop.add(loser)
            w, l = (c1, c2) if loser == j else (c2, c1)
            print(f"çift: [{l['_region']}] {l['name']}  ~  [{w['_region']}] {w['name']}  ({d:.0f} km) -> atıldı: {l['_region']}")
    os.makedirs(a.out, exist_ok=True)
    for k, d in sets.items():
        keep = [c for c in d["clusters"] if not any(c is allc[i] for i in drop)]
        for c in keep:
            c.pop("_region", None)
        d = dict(d)
        d["clusters"] = keep
        json.dump(d, open(os.path.join(a.out, f"{k}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{k}: {len(keep)} küme, nüfus {sum(c.get('population', 0) for c in keep):,}")


if __name__ == "__main__":
    main()
