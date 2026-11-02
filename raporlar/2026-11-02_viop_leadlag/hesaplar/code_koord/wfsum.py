import json, sys, glob
for jf in sys.argv[1:]:
    print("=====", jf.split("/")[-2])
    for line in open(jf):
        try: j = json.loads(line)
        except: continue
        if j.get("type") != "result": continue
        v = j.get("result") or j.get("value") or {}
        if isinstance(v, str):
            try: v = json.loads(v)
            except: print("STR", v[:300]); continue
        lab = j.get("label") or j.get("agent_label") or ""
        if isinstance(v, dict) and "verdicts" in v:
            for x in v["verdicts"]:
                print(f"[{lab}] {x.get('claim_id')}: {x.get('verdict')} / {x.get('new_confidence')} | {x.get('corrected_claim','')[:420]}")
            for g in v.get("general_issues", [])[:8]: print("   GEN:", g[:300])
        elif isinstance(v, dict) and "claim_id" in v:
            print(f"[{lab}] {v.get('claim_id')}: {v.get('verdict')} / {v.get('new_confidence')} | {v.get('corrected_claim','')[:700]}")
        elif isinstance(v, dict) and "summary" in v:
            print(f"[{lab}] SUMMARY: {v['summary'][:1500]}"); [print("  CH:", c[:300]) for c in v.get("changed_conclusions", [])]
        else:
            print(f"[{lab}] keys={list(v)[:6] if isinstance(v, dict) else type(v)}")
