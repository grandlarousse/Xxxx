import csv, sys, collections, re, json
path=sys.argv[1]
rows=[]
with open(path, encoding="windows-1254", errors="replace") as f:
    rd=csv.reader(f, delimiter=";")
    hdr=[h.strip() for h in next(rd)]; next(rd)
    for r in rd:
        if len(r)<20: continue
        rows.append(dict(zip(hdr,r)))
print(hdr)
def fl(x):
    try: return float(x.replace(',','.')) if isinstance(x,str) else float(x)
    except: return 0.0
agg=collections.defaultdict(lambda:[0,0.0,0])
for r in rows:
    c=r["SOZLESME KODU"].strip()
    m=re.match(r"^F_([A-Z0-9]+?)(E?)(\d{4})$",c)
    if not m: continue
    u=m.group(1)
    a=agg[u]; a[0]+=1; a[1]+=fl(r["ISLEM HACMI"]); a[2]+=int(fl(r["ACIK POZISYON"]))
for k,v in sorted(agg.items(), key=lambda x:-x[1][1]):
    print(f"{k:12s} n={v[0]:2d} hacimTL={v[1]/1e6:10.1f}mn OI={v[2]}")
json.dump({k:v for k,v in agg.items()}, open(sys.argv[2],'w'))
