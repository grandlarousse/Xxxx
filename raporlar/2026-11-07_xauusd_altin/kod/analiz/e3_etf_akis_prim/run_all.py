"""e3_etf_akis_prim: tüm analizleri baştan çalıştırır (kayıt dosyası sıfırlanır)."""
import os, subprocess, sys
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/e3_etf_akis_prim"
reg = f"{S}/out/registry/e3_etf_akis_prim.csv"
if os.path.exists(reg): os.remove(reg)
for f in ["parse_bist_byf.py", "a_flows.py", "b_premium.py", "c_cef.py", "d_letf.py", "d2_miners_robust.py", "e_bist_byf.py", "f_volume.py", "g_main_claim.py", "h_summary.py"]:
    print("=" * 20, f, flush=True)
    args = [sys.executable, "-W", "ignore"] + (["-I"] if f == "parse_bist_byf.py" else []) + [f"{OUT}/{f}"]
    with open(f"{OUT}/log_{f.replace('.py', '')}.txt", "w") as fh:
        r = subprocess.run(args, cwd=OUT, stdout=fh, stderr=subprocess.STDOUT)
    print(f, "->", r.returncode, flush=True)
