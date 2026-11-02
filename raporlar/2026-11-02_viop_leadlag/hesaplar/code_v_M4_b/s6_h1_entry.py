"""s6: Saatlik veriyle alternatif giris: ilk saatlik barin KAPANISI (~07:30 UTC = 10:30 TSI) -> gunluk kapanis. 2023-11..2026-10.
Ayrica acilis->07:30 parcasi. Gunluk o ile h1 ilk bar acilisinin uyumu."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
cA, _ = vb.comp(vb.JP_AU); z = vb.zpast(cA.dropna())
rows = []
for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS", "XU100.IS"]:
    h = vb.raw(s, "h1").copy(); h.index = pd.DatetimeIndex(h.index).tz_convert("UTC")
    h["d"] = h.index.normalize().tz_localize(None); h["hm"] = h.index.strftime("%H:%M")
    first = h[h.hm == "06:30"].groupby("d").first()
    d = vb.bist(s)
    df = pd.DataFrame({"o": d.o, "c": d.c, "intra": d.intra}).join(first[["o", "c"]].rename(columns={"o": "h1o", "c": "h1c730"}), how="inner")
    df["eq_open"] = (abs(df.o / df.h1o - 1) < 1e-4)
    df["r_730_close"] = np.log(df.c / df.h1c730); df["r_open_730"] = np.log(df.h1c730 / df.o)
    df["z"] = z.reindex(df.index); df = df.dropna(subset=["z", "intra", "r_730_close"])
    df["pos"] = np.sign(df.z).where(df.z.abs() > 1, 0)
    a = df[df.pos != 0]
    for tgt in ("intra", "r_open_730", "r_730_close"):
        g = a.pos * a[tgt]
        r, t, n = vb.corr_t(df.z, df[tgt])
        rows.append(dict(stock=s, target=tgt, n_days=len(df), n_tr=len(a), gross_bps=1e4 * g.mean(), net15=1e4 * g.mean() - 15, t_net15=vb.nwt(g - 15e-4),
                         net8=1e4 * g.mean() - 8, corr_z=r, corr_t=t, eq_open_share=df.eq_open.mean()))
R = pd.DataFrame(rows); R.to_csv(os.path.join(vb.OUT, "res_s6_h1_entry.csv"), index=False)
pd.set_option("display.width", 250); print(R.round(3).to_string())
