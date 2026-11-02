#!/bin/bash
# kullanım: probe.sh SYM1 SYM2 ... (EXCH:SYM)
python3 -I /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_tv/tvpage.py "$@" 2>&1 | python3 -c "
import sys,json
for l in sys.stdin:
  try: d=json.loads(l)
  except Exception: print(l); continue
  i=d['info']; print(d['tv'],d['http'],'|',i.get('resolved_symbol'),'|',i.get('description'),'|',i.get('type'),i.get('typespecs'),i.get('currency'),i.get('source'))
"
