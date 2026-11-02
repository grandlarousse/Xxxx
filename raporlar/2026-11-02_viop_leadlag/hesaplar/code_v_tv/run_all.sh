#!/bin/sh
# v_tv yeniden üretim: yeni f_*.csv eklenirse bu betiği çalıştır.
# 1) değerlendirme + doğrulanacak yeni kod listesi  2) yeni kodların halka açık TV sayfalarını oku (curl, ~1 istek/sn)
# 3) tv_final.csv + uyusmazliklar.csv + f_tv_duzeltme_esleme.csv  4) biçim denetimi
set -e
cd "$(dirname "$0")"
nice -n 10 python3 audit.py --fetchlist
nice -n 10 python3 -I fetch.py codes_batch2.txt
nice -n 10 python3 build_final.py
# tv_final'de okunmamış kod kaldıysa onları da oku ve yeniden üret
python3 -c "
import json,pandas as pd
from common import tv_tokens
f=pd.read_csv('../tv_final.csv',dtype=str)
fc={json.loads(l)['code'] for l in open('fetch_cache.jsonl')}
need=[c for col in ['tv_kodu','tv_alternatif'] for s in f[col].dropna() for c,_ in tv_tokens(s) if c not in fc and '<KOD>' not in c]
open('codes_extra.txt','w').write('\n'.join(dict.fromkeys(need))+'\n')"
nice -n 10 python3 -I fetch.py codes_extra.txt
nice -n 10 python3 build_final.py
nice -n 10 python3 lint.py
