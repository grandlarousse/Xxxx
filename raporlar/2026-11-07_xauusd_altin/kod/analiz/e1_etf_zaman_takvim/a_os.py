"""(a) 'Aşırı satım sonrası al' (yalnız uzun bacak) tanım ızgarası: madenciler vs altın/gümüş. Bilgi: kapanış t-1 (strict).
Tanımlar önceden sabit (literatürdeki standart eşikler); IS'te seçim yapılmaz, tutarlılık ızgara genelinde okunur."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("a3_")
F = pd.read_pickle(f"{O}/a_feats.pkl")
rows = []
for t in ["GDX", "GDXJ", "GLD", "SLV"]:
    defs = {"streak<=-3": F[(t, "strict", "streak")] <= -3, "streak<=-4": F[(t, "strict", "streak")] <= -4, "streak<=-5": F[(t, "strict", "streak")] <= -5,
            "BollZ<-2": F[(t, "strict", "bbz")] < -2, "BollZ<-1.5": F[(t, "strict", "bbz")] < -1.5,
            "RSI2<5": F[(t, "strict", "rsi2")] < 5, "RSI2<10": F[(t, "strict", "rsi2")] < 10, "z1<-2": F[(t, "strict", "z1")] < -2}
    valid = F[(t, "strict", "bbz")].notna() & F[(t, "strict", "streak")].notna()
    for nm, m in defs.items():
        s = m.astype(float).where(valid)
        for h in [1, 3, 5]:
            y = fwd(R[t], h); st = rstats(s, y, h)
            reg("a3_os", f"a3_os|{t}|{nm}|h{h}", f"oversold {nm}", h, st, "yalnız uzun bacak: sinyal günü vs diğer")
            on = y[s == 1]
            rows.append(dict(target=t, rule=nm, h=h, n_sig=int(s.sum()), mean_sig_bps=round(on.mean() * 1e4, 1), mean_all_bps=round(y.mean() * 1e4, 1), hit=round((on > 0).mean(), 3),
                             t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), t_22=round(st["t_22"], 2), yrs=f"{st['yrs_same_sign']}/{st['yrs']}"))
T = pd.DataFrame(rows); T.to_csv(f"{O}/a_oversold_grid.csv", index=False)
pd.set_option("display.width", 250); print(T.to_string())
g = T.groupby(["target", "h"]).apply(lambda q: pd.Series(dict(pos_full=(q.t > 0).sum(), pos_is=(q.t_is > 0).sum(), pos_oos=(q.t_oos > 0).sum(), n=len(q), med_t=q.t.median())))
print(g)
