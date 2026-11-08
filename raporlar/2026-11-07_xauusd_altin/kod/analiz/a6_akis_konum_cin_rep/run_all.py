"""Sırayla: r1 (özellikler) -> r2..r9 (testler). Her betiğin çıktısı log_<ad>.txt."""
import subprocess, sys, os
d = os.path.dirname(os.path.abspath(__file__))
for f in ["r1_cn.py", "r2_cn_tests.py", "r3_cn_mimic.py", "r4_cn_robust.py", "r5_lagprofile.py", "r6_subwindow.py", "r7_gpr.py", "r8_oi.py", "r9_extra.py"]:
    out = subprocess.run([sys.executable, "-W", "ignore", f"{d}/{f}"], capture_output=True, text=True, cwd=d)
    open(f"{d}/log_{f[:-3]}.txt", "w").write(out.stdout + out.stderr); print(f, "ok" if out.returncode == 0 else "HATA")
