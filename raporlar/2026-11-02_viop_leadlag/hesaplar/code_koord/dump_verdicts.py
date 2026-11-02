import json, sys, os
W, out = sys.argv[1], sys.argv[2]
allv = []
for wf in sorted(os.listdir(W)):
    jf = os.path.join(W, wf, "journal.jsonl")
    if not os.path.exists(jf): continue
    for line in open(jf):
        try: j = json.loads(line)
        except: continue
        if j.get("type") != "result": continue
        v = j.get("result") or j.get("value")
        if isinstance(v, str):
            try: v = json.loads(v)
            except: continue
        if isinstance(v, dict) and "verdicts" in v:
            for x in v["verdicts"]: x["_wf"] = wf; x["_kind"] = "batch"; allv.append(x)
            if v.get("general_issues"): allv.append({"_wf": wf, "_kind": "general_issues", "items": v["general_issues"]})
        elif isinstance(v, dict) and "claim_id" in v:
            v["_wf"] = wf; v["_kind"] = "stage"; allv.append(v)
        elif isinstance(v, dict) and "summary" in v:
            v["_wf"] = wf; v["_kind"] = "sensitivity"; allv.append(v)
json.dump(allv, open(out, "w"), ensure_ascii=False, indent=1)
print(len(allv), "kayıt")
