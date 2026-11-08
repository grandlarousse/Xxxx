"""placebo_lead: öne çıkan öngörücüler gelecek bilgisi içeriyor mu? (shift<0 = gelecek, yasak; shift>0 = daha eski bilgi)"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
F = pd.read_pickle(f"{O}/a_feats.pkl")
rows = []
for nm, t, x, h in [("GLD nc mom1 (15:00 ET hareketi)", "GLD", F[("GLD", "nc", "mom1")], 1), ("GLD strict mom1", "GLD", F[("GLD", "strict", "mom1")], 1),
                    ("GDX streak (t-1)", "GDX", F[("GDX", "strict", "streak")], 1), ("GDX streak<=-5", "GDX", (F[("GDX", "strict", "streak")] <= -5).astype(float), 1),
                    ("GLD BollZ (t-1)", "GLD", F[("GLD", "strict", "bbz")], 5), ("GLD mom250 (t-1)", "GLD", F[("GLD", "strict", "mom250")], 1)]:
    pl = placebo_lead(x, R[t], h); rows.append(dict(ongorucu=nm, etf=t, h=h, **{f"s{k}": v for k, v in pl.items()}))
P = pd.DataFrame(rows); P.to_csv(f"{O}/g_placebo_lead.csv", index=False); print(P.to_string())
