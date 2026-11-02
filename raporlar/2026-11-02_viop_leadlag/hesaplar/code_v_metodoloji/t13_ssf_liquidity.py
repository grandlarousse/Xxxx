# T13: VİOP pay vadelisi (SSF) likiditesi 2025-11..2026-10: günlük işlem değeri, işlem sayısı, işlemsiz gün oranı (ön ay+toplam). İşlenebilirlik bağlamı.
import warnings; warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
v=pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/viop_panel.parquet')
v=v[(v.segment=='SSF')&(v.date>='2025-11-01')]
g=v.groupby(['und','date']).agg(val=('value_tl','sum'),tr=('trades','sum')).reset_index()
s=g.groupby('und').agg(gun=('date','nunique'),med_deger_mnTL=('val',lambda x: x.median()/1e6),med_islem=('tr','median'),islemsiz_gun_pct=('tr',lambda x:(x<=0).mean()*100),az_islem_lt20_pct=('tr',lambda x:(x<20).mean()*100)).sort_values('med_deger_mnTL',ascending=False)
pd.set_option('display.width',200); print(s.round(1).to_string())
idx=v[(v.code.str.contains('XU030'))]
print('XU030 endeks vadelisi (segment var mı?):', v.segment.unique()[:10])
