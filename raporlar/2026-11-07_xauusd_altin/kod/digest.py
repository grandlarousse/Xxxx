import json, sys
f = sys.argv[1]
t = open(f).read()
try:
    data = json.loads(t); data = data["result"] if isinstance(data, dict) else data
except Exception:
    i = t.index("["); data = json.loads(t[i:t.rindex("]") + 1])
for x in data:
    res = x.get("res") or {}
    print("=" * 100); print("AİLE:", x.get("key"), "| test sayısı:", res.get("n_tests"), "| rapor:", res.get("report"))
    vr = {v["id"]: v for v in ((x.get("rep") or {}).get("verdicts") or [])}
    va = {v["id"]: v for v in ((x.get("adv") or {}).get("verdicts") or [])}
    for c in res.get("claims", []):
        cid = c["id"]
        keys = ["target","predictor","h","ic","t_full","t_is","t_oos","yrs_same_sign","sharpe_oos_net","sharpe_oos_demeaned","sharpe_oos_net_longonly","sharpe_oos_net_inverse","trades_per_year","confidence"]
        print(f"\n  [{cid}] " + " | ".join(f"{k}={c.get(k)}" for k in keys if c.get(k) is not None))
        print("     kural:", (c.get("rule") or "")[:600])
        print("     bilgi zamanı:", (c.get("info_time_utc") or c.get("info_time") or "")[:250])
        for nm, vv in (("REP", vr), ("ADV", va)):
            v = vv.get(cid)
            if v: print(f"     {nm}: {v['verdict']} → {v['confidence_after']} | {v['reproduced'][:350]} || SORUN: {v['issues'][:600]}")
    print("\n  NEGATİFLER:"); [print("   -", n[:300]) for n in res.get("negatives", [])]
    for nm in ("rep", "adv"):
        g = (x.get(nm) or {}).get("general")
        if g: print(f"  {nm.upper()} GENEL:", g[:1200])
