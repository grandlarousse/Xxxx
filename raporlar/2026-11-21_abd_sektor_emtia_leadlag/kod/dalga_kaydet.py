"""İş akışı günlüklerinden (journal.jsonl) ajan dönüşlerini ek/<dalga>/<id>.json olarak kaydeder ve kısa döküm basar.
Kullanım: python3 kod/dalga_kaydet.py <dalga_adi> <journal.jsonl> [<journal.jsonl> ...]"""
import json, os, sys
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dalga, yollar = sys.argv[1], sys.argv[2:]
os.makedirs(os.path.join(KOK, "ek", dalga), exist_ok=True)
for y in yollar:
    etiket = {}
    for satir in open(y):
        try:
            j = json.loads(satir)
        except Exception:
            continue
        if j.get("type") == "started":
            etiket[j.get("key")] = j.get("label")
    for satir in open(y):
        try:
            j = json.loads(satir)
        except Exception:
            continue
        if j.get("type") != "result":
            continue
        r = j.get("result") or j.get("value") or {}
        if isinstance(r, str):
            try: r = json.loads(r)
            except Exception: r = {"ozet": r}
        ad = etiket.get(j.get("key")) or r.get("id") or "bilinmeyen"
        ad = str(ad).replace(" (tekrar)", "").replace("/", "_")
        json.dump(r, open(os.path.join(KOK, "ek", dalga, ad + ".json"), "w"), ensure_ascii=False, indent=1)
        print(f"{ad}: arac={r.get('arac')} | ozet {len(str(r.get('ozet','')).split())} kelime | defter {len(r.get('kilit_defter') or [])} satir | dosyalar {len(r.get('dosyalar') or [])}")
