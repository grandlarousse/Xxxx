"""Açılış verisi kalitesi: yıllara göre o==önceki c, o==h, o==l oranları; raw_gap vs gap farkı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
for s in ["CIMSA", "OYAKC", "THYAO", "GARAN"]:
    d = load_daily(s); d = d[d.index >= "2008-01-01"]
    pc = d.c.shift(1)
    q = pd.DataFrame({"o_eq_pc": (d.o == pc), "o_eq_h": (d.o == d.h), "o_eq_l": (d.o == d.l), "absgap>1%": (np.log(d.o / pc).abs() > 0.01)})
    print(s); print(q.groupby(d.index.year).mean().round(3).T.to_string())
