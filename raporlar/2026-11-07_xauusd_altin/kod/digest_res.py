import json, sys
d = json.load(open(sys.argv[1])); r = d["result"]
items = r["reports"] if isinstance(r, dict) and "reports" in r else r
for x in items:
    vs = x.get("verdicts", [])
    cnt = {}
    for v in vs: cnt[v["verdict"]] = cnt.get(v["verdict"], 0) + 1
    print("=" * 80); print(x["key"], cnt)
    for v in vs:
        if v["verdict"] in ("yanlis", "kismen"):
            print(f"  [{v['id']}] {v['verdict']}: {v['correction'][:700]}")
    if x.get("missed"): print("  EKSİK:", " | ".join(m[:200] for m in x["missed"][:8]))
if isinstance(r, dict) and r.get("critic"): print("\nELEŞTİRMEN:", json.dumps(r["critic"], ensure_ascii=False)[:4000])
if isinstance(r, dict) and r.get("gaps"): print("\nBOŞLUKLAR:", json.dumps(r["gaps"], ensure_ascii=False)[:3000])
