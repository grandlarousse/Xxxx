#!/bin/bash
# Bağımsız yeniden üretim (lib_altin / analist kodu kullanılmaz). ~10 sn.
cd "$(dirname "$0")"
python3 -W ignore r1_veri.py > /dev/null
python3 -W ignore r2_iddialar.py > /dev/null
python3 -W ignore r3_derin.py > /dev/null
python3 -W ignore r4_ek.py > r4_log.txt
