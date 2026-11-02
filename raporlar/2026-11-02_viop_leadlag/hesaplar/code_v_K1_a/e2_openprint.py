"""(b) Açılış fiyatı ne? günlük o vs h1 06:30 bar o / m5 06:55 bar (açılış seansı) / m5 07:00 bar o. Günlük c vs h1 15:00 bar."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
rows = []
for s in VIOP:
    d = load_daily(s); H = h1(s); M = m5(s)
    if H is None: continue
    f = H[H.hm == 630].set_index("day"); l = H[H.hm == 1500].set_index("day")
    j = d.join(f[["o", "c", "v"]].add_prefix("h_"), how="inner").join(l[["c", "v"]].add_prefix("k_"), how="left")
    r = dict(sym=s, n_h1=len(j), o_eq_h1o=float(np.isclose(j.o, j.h_o, rtol=1e-4).mean()),
             c_eq_h1500c=float(np.isclose(j.c, j.k_c, rtol=1e-4).mean()), med_abs_o_vs_h1o_bps=float(1e4 * np.log(j.o / j.h_o).abs().median()))
    if M is not None:
        a = M[M.hm == 655].set_index("day"); b = M[M.hm == 700].set_index("day")
        jm = d.join(a[["o", "c", "v"]].add_prefix("a_"), how="inner").join(b[["o", "c"]].add_prefix("b_"), how="inner")
        r.update(n_m5=len(jm), o_eq_m5_0655=float(np.isclose(jm.o, jm.a_o, rtol=1e-4).mean()), o_eq_m5_0700o=float(np.isclose(jm.o, jm.b_o, rtol=1e-4).mean()),
                 m5_0655_vol0=float((jm.a_v == 0).mean()), med_abs_o_vs_0700o_bps=float(1e4 * np.log(jm.o / jm.b_o).abs().median()),
                 med_abs_o_vs_0700c_bps=float(1e4 * np.log(jm.o / jm.b_c).abs().median()))
    rows.append(r)
R = pd.DataFrame(rows); R.to_csv(OUT + "/res_e2_openprint.csv", index=False)
pd.set_option("display.width", 250); print(R.round(3).to_string(index=False)); print(R.mean(numeric_only=True).round(3))
# örnek gün dökümü
M = m5("CIMSA"); d = load_daily("CIMSA")
for day in M.day.unique()[-3:]:
    x = M[M.day == day]; print(pd.Timestamp(day).date(), "günlük o/h/l/c:", d.loc[day, ["o", "h", "l", "c"]].round(2).tolist()); print(x[x.hm <= 715][["o", "h", "l", "c", "v"]].round(2).to_string())
