"""cin - ek Yahoo sembolleri (proxy adayları). ydl.fetch (cached ise atlar). Çıktı: yahoo_fetch_status_b.csv"""
import sys, os, time; SCR="/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"; sys.path.insert(0, SCR+"/code")
import ydl, pandas as pd
X = ["NIC.AX","S32.AX","IGO.AX","MEOH","WLK","OLN","DOW","AMR","HCC","CEOHF","KARS","LIT","ALB","SQM","DRIV","AA","CENX","FCX","SCCO","GDX","GLD",
     "5401.T","MT","XME","UUP","EEM","NHY.OL","CNH=F","WHC.AX","TECK","GUBRF.IS","XLE","5201.T","GLW","SGO.PA","SISE.IS","ARCLK.IS","VESTL.IS"]
rows=[]
for s in X:
    r = ydl.fetch(s, "daily"); p = os.path.join(SCR, "data/daily", s + ".parquet")
    n = len(pd.read_parquet(p)) if os.path.exists(p) else 0
    rows.append((s, r, n)); 
    if r != "cached": time.sleep(0.25)
pd.DataFrame(rows, columns=["sym","status","n"]).to_csv("yahoo_fetch_status_b.csv", index=False)
print([x for x in rows if x[2] < 300])
