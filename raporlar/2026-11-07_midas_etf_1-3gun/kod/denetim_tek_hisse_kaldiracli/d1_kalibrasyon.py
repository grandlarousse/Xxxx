"""Sentetik 2x'in gerçek ETF'e göre ek günlük geri kalışı (yalnız 2x döneminde), bağımsız ölçüm."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dk, numpy as np, pandas as pd, lib
rows=[]
for st in dk.STK+["MSTR","COIN"]:
    e=dk.ETF[st]; sd=dk.load_stock(st); syn=dk.synth(sd,extra_bp=0.0)
    et=lib.load(e)
    d0=pd.Timestamp(dk.SWITCH[e])
    rs=syn["c"].pct_change().reindex(et.index); re_=et["c"].pct_change()
    m=(et.index>=d0)
    diff=(re_-rs)[m].dropna()
    # gerçek kaldıraç: r_ETF ~ b r_stock
    rst=sd["c"].pct_change().reindex(et.index)[m]
    b=np.polyfit(rst.dropna().values, re_[m].reindex(rst.dropna().index).values,1)[0]
    co=np.corrcoef(rs[m].dropna(), re_[m].reindex(rs[m].dropna().index))[0,1]
    rows.append((st,e,len(diff),diff.mean()*1e4,diff.median()*1e4,b,co))
R=pd.DataFrame(rows,columns=["stock","etf","n_gun","ek_surukleme_ort_bp","medyan_bp","beta_2x_donem","corr"])
print(R.round(3).to_string(index=False))
R.to_csv(dk.OUT+"/d1_kalibrasyon.csv",index=False)
