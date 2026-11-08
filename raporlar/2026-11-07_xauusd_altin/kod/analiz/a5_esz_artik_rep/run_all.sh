#!/bin/bash
# Bağımsız yeniden üretim (lib_altin/a5_lib kullanılmaz). Sıra önemli: rep01 veriyi kurar.
cd "$(dirname "$0")"
for f in rep01_data.py rep02_c1.py rep03_settle_time.py rep03c_settle_level.py rep04_cfamily.py rep05_b_a.py rep06_agrid_panelfx.py rep07_b1_early.py rep08_extra_checks.py rep09_ratio_pt.py; do
  echo "=== $f"; python3 -W ignore "$f" > "log_${f%.py}.txt" 2>&1 || echo "HATA $f"
done
