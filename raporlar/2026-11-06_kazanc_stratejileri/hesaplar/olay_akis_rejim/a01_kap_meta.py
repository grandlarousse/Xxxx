"""KAP bildirim sorgu API'si (sitenin kendi arama ucu) -> konu bazli aylik metadata. Varsayilan istek basliklari, tek tek, 1.2 sn bekleme.
POST https://www.kap.org.tr/tr/api/disclosure/members/byCriteria
Konular (KAP konu listesi, kardes ajanin kap_subjects.json dosyasindan):
  GA  = 'Paylarin Geri Alinmasina Iliskin Bildirim'  4028328d6233239a01629b43e4694fae
  PAS = 'Pay Alim Satim Bildirimi'                   8aca490d50286f620150287614ae005c
Kullanim: python3 -I a01_kap_meta.py GA|PAS [BAS=2018-01] [SON=2026-11] [HALF=1]
Cikti: <CACHE>/kap_<konu>/<YYYY-MM>[_a|_b].json"""
import os, sys, json, time, requests, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/akis_rejim"
U = "https://www.kap.org.tr/tr/api/disclosure/members/byCriteria"
OID = {"GA": "4028328d6233239a01629b43e4694fae", "PAS": "8aca490d50286f620150287614ae005c"}
S = requests.Session()
def q(oid, a, b):
    body = {"fromDate": a, "toDate": b, "memberType": "IGS", "mkkMemberOidList": [], "disclosureClass": "", "subjectList": [oid],
            "isLate": "", "mainSector": "", "sector": "", "subSector": "", "marketOidList": [], "index": "", "bdkReview": "",
            "bdkMemberOidList": [], "year": "", "term": "", "ruleType": "", "period": "", "fromSrc": False, "srcCategory": "", "discIndex": []}
    for k in range(3):
        try:
            r = S.post(U, json=body, timeout=120)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"): return r.json()
            print("status", r.status_code, a, b, r.headers.get("Retry-After"), flush=True)
            if r.status_code == 429: time.sleep(int(r.headers.get("Retry-After", "60") or 60) + 5)
        except Exception as e: print("err", e, flush=True)
        time.sleep(5 * (k + 1))
    return None
def pieces(p, n):
    """Ayi n parcaya bol (API kapasite sinirina karsi)."""
    s = p.start_time.normalize(); e = p.end_time.normalize(); days = pd.date_range(s, e, freq="D")
    k = len(days); cut = [days[int(i * k / n)] for i in range(n)] + [e + pd.Timedelta(days=1)]
    return [(cut[i], cut[i + 1] - pd.Timedelta(days=1)) for i in range(n)]
if __name__ == "__main__":
    konu = sys.argv[1]; kw = dict(x.split("=") for x in sys.argv[2:] if "=" in x)
    d0 = pd.Period(kw.get("BAS", "2018-01"), "M"); d1 = pd.Period(kw.get("SON", "2026-11"), "M"); n = int(kw.get("PARCA", "1"))
    out = f"{CACHE}/kap_{konu}"; os.makedirs(out, exist_ok=True)
    for p in pd.period_range(d0, d1, freq="M"):
        for j, (a, b) in enumerate(pieces(p, n)):
            f = f"{out}/{p}.json" if n == 1 else f"{out}/{p}_{j}.json"
            if os.path.exists(f): continue
            d = q(OID[konu], a.strftime("%Y-%m-%d"), b.strftime("%Y-%m-%d"))
            if d is None: print("FAIL", p, j, flush=True); time.sleep(3); continue
            json.dump(d, open(f, "w"), ensure_ascii=False); print(p, j, len(d), flush=True); time.sleep(1.5)
