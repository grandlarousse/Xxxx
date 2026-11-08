"""Bütün a6 betiklerini sırayla çalıştırır; kayıt (registry) dosyasını sıfırlar (yinelenen kayıt olmasın)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
REG = f"{S}/out/registry/a6_akis_konum_cin.csv"
if os.path.exists(REG): os.remove(REG)
for f in ["a_cot.py", "b_shfe.py", "c_asia.py", "d_gpr.py", "e_viop_pos.py", "f_deep.py", "g_cn_robust.py", "h_fdr.py", "i_tables.py"]:
    if not os.path.exists(f"{HERE}/{f}"): continue
    print("=" * 20, f, flush=True)
    with open(f"{HERE}/log_{f[:-3]}.txt", "w") as lg:
        r = subprocess.run([sys.executable, "-W", "ignore", f"{HERE}/{f}"], cwd=HERE, stdout=lg, stderr=subprocess.STDOUT)
    print(f, "rc", r.returncode, flush=True)
