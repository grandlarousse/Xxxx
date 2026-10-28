import json, sys, datetime
import pandas as pd
D="/tmp/claude-0/-home-user-Xxxx/e9cebbab-b80e-5b61-827f-5051f73327e4/scratchpad/dl2/"
def load(name):
    d=json.load(open(D+name))
    r=d['chart']['result'][0]
    ts=pd.to_datetime(r['timestamp'],unit='s')+pd.Timedelta(hours=3)
    q=r['indicators']['quote'][0]
    df=pd.DataFrame({'o':q['open'],'h':q['high'],'l':q['low'],'c':q['close'],'v':q['volume']},index=ts.normalize())
    df=df[~df.index.duplicated(keep='last')].dropna(subset=['c'])
    return df
x100=load('XU100.IS.json'); x30=load('XU030.IS.json'); fx=load('TRY=X.json')
