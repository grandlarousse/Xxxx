"""KAP bildirim sorgu (sitenin kendi arama API'si) -> konu bazli aylik metadata.
POST https://www.kap.org.tr/tr/api/disclosure/members/byCriteria  (varsayilan basliklar, tek tek, 1 sn bekleme)
Kullanim: python3 f02_kap_meta.py CA|KPD  [BAS=2014-01] [SON=2026-11]
  CA  = 'Sermaye Artirimi/Azaltimi' (4028328d5988e2630159d5fd68661ff4)
  KPD = 'Kar Payi Dagitimi' (4028328d5988e2630159d5fb51c81fe6)
Cikti: <CACHE>/kap_<konu>/<YYYY-MM>.json"""
import os, sys, json, time, requests, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz"
U = "https://www.kap.org.tr/tr/api/disclosure/members/byCriteria"
OID = {"CA": "4028328d5988e2630159d5fd68661ff4", "KPD": "4028328d5988e2630159d5fb51c81fe6"}
S = requests.Session()
def q(oid, a, b):
    body = {"fromDate": a, "toDate": b, "memberType": "IGS", "mkkMemberOidList": [], "disclosureClass": "", "subjectList": [oid],
            "isLate": "", "mainSector": "", "sector": "", "subSector": "", "marketOidList": [], "index": "", "bdkReview": "",
            "bdkMemberOidList": [], "year": "", "term": "", "ruleType": "", "period": "", "fromSrc": False, "srcCategory": "", "discIndex": []}
    for k in range(3):
        try:
            r = S.post(U, json=body, timeout=120)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"): return r.json()
            print("status", r.status_code, a, b, flush=True)
        except Exception as e: print("err", e, flush=True)
        time.sleep(5 * (k + 1))
    return None
if __name__ == "__main__":
    konu = sys.argv[1]; kw = dict(x.split("=") for x in sys.argv[2:] if "=" in x)
    d0 = pd.Period(kw.get("BAS", "2014-01"), "M"); d1 = pd.Period(kw.get("SON", "2026-11"), "M")
    out = f"{CACHE}/kap_{konu}"; os.makedirs(out, exist_ok=True)
    for p in pd.period_range(d0, d1, freq="M"):
        f = f"{out}/{p}.json"
        if os.path.exists(f): continue
        a = p.start_time.strftime("%Y-%m-%d"); b = p.end_time.strftime("%Y-%m-%d")
        d = q(OID[konu], a, b)
        if d is None: print("FAIL", p, flush=True); time.sleep(2); continue
        json.dump(d, open(f, "w"), ensure_ascii=False); print(p, len(d), flush=True); time.sleep(1.0)
