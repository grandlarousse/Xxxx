import pandas as pd, glob, os, sys, re
O = sys.argv[1]
fr = []
for f in sorted(glob.glob(os.path.join(O, "f_*.csv"))):
    ag = os.path.basename(f)[2:-4]
    try: d = pd.read_csv(f)
    except Exception as e: print("ERR", f, e); continue
    d.insert(0, "agent", ag); fr.append(d)
M = pd.concat(fr, ignore_index=True, sort=False)
def norm(c):
    c = str(c).upper()
    lead = re.split(r"[\s(/,;]", c.strip())[0] if c.strip() else ""
    for k, v in [("ÇOK", "COK_DUSUK"), ("COK", "COK_DUSUK"), ("YÜKSEK", "YUKSEK"), ("YUKSEK", "YUKSEK"), ("ORTA", "ORTA"), ("DÜŞÜK", "DUSUK"), ("DUSUK", "DUSUK"), ("HIGH", "YUKSEK"), ("MEDIUM", "ORTA"), ("LOW", "DUSUK")]:
        if lead.startswith(k): return v
    if re.search(r"ÇOK|SPEK", c): return "COK_DUSUK"
    if re.search(r"YÜKSEK|YUKSEK", c): return "YUKSEK"
    if re.search(r"\bORTA\b", c): return "ORTA"
    if re.search(r"DÜŞÜK|DUSUK", c): return "DUSUK"
    return "?"
M["conf_norm"] = M["confidence"].map(norm) if "confidence" in M else "?"
M.to_csv(os.path.join(O, "master_findings_r1.csv"), index=False)
print(M.shape); print(pd.crosstab(M["agent"], M["conf_norm"]))
print(M["relation"].value_counts().head(15) if "relation" in M else "")
