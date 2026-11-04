"""Güncel veri: Yahoo günlük (SAHOL, AKBNK, XU100, XU030, XBANK) -> dl_k_sahol_a/daily ; ortak veriye dokunmaz.
VİOP bültenleri (02.11, 03.11.2026) dl_k_sahol_a/viop altına curl ile indirildi; burada ayrıştırılır -> dl_k_sahol_a/viop_new.parquet"""
import sys, os, time, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ydl_k, pandas as pd, numpy as np
for s in ['SAHOL.IS', 'AKBNK.IS', 'XU100.IS', 'XU030.IS', 'XBANK.IS']:
    print(s, ydl_k.fetch(s, 'daily', force=True), flush=True); time.sleep(0.5)
# VİOP ayrıştırma (02_parse.py ile aynı alan eşlemesi)
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_y_viop')
import importlib.util
spec = importlib.util.spec_from_file_location('vp', '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_y_viop/02_parse.py'); vp = importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)
D = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_k_sahol_a/viop'
fs = sorted(f for f in os.listdir(D) if f.endswith('.csv'))
F = pd.concat([vp.parse(os.path.join(D, f))[0] for f in fs], ignore_index=True)
F['date'] = pd.to_datetime(F['date']); F['expiry'] = pd.to_datetime(F['expiry'], errors='coerce'); F['und'] = F['und_raw'].map(vp.und_std)
m = F['code'].str.extract(r'^F_(.*?)(\d{4})$'); F['root'] = m[0]
for c in vp.NUM:
    if c not in F: F[c] = np.nan
F['mult'] = F['value_tl'] / (F['qty'] * F['vwap'])
F = F[['date', 'code', 'root', 'und', 'und_raw', 'market', 'segment', 'ctype', 'expiry'] + [c for c in vp.NUM if c != 'prem_tl'] + ['mult']]
F.to_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_k_sahol_a/viop_new.parquet', index=False)
x = F[F.root.isin(['SAHOL', 'AKBNK']) & (F.ctype == 'D_EQ_FPD')]
print(x[['date', 'code', 'expiry', 'settle', 'prev_settle', 'open', 'close', 'vwap', 'value_tl', 'qty', 'oi']].to_string())
for s in ['SAHOL.IS', 'AKBNK.IS', 'XU100.IS']:
    d = pd.read_parquet(f'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_k_sahol_a/daily/{s}.parquet'); print(s); print(d.tail(6).to_string())
