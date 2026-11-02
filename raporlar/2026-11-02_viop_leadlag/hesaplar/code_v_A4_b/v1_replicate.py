"""v1: AIR sinyalini iki hizalamayla kur (C: kendi takvim; A: BIST takvimine ffill+shift), başlık rakamlarını tekrar üret."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *

def ret_cal_A(sym):
    s = close_own(sym)
    c = bist_cal(); c = c[c >= s.index[0]]
    p = s.reindex(s.index.union(c)).ffill().reindex(c)
    r = np.log(p).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1)
    r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r.where(r != 0)

def sig_A():
    def bk(ss):
        X = pd.concat([ret_cal_A(s) for s in ss], axis=1); return X.mean(1).where(X.notna().sum(1) >= 2)
    eu = bk(EU_AIR); us = bk(US_AIR)
    def rr(y, x):
        df = pd.concat([y.rename("y"), x.rename("x")], axis=1)
        b = (df.y.rolling(250, min_periods=120).cov(df.x) / df.x.rolling(250, min_periods=120).var()).shift(1)
        return df.y - b * df.x
    def z(x):
        mu = x.rolling(250, min_periods=60).mean().shift(1); sd = x.rolling(250, min_periods=60).std().shift(1); return (x - mu) / sd
    a = z(rr(eu, ret_cal_A("^STOXX"))).clip(-3, 3) + z(rr(us, ret_cal_A("^GSPC"))).clip(-3, 3)
    return a.shift(1)

if __name__ == "__main__":
    P = sector_signal(EU_AIR, US_AIR)
    AIR_C = (P["EU"] + P["US"]).rename("AIR_C")
    AIR_A = sig_A().rename("AIR_A")
    tur = to_bist(zs(ret_own("TUR")).clip(-3, 3))
    pd.DataFrame({"AIR_C": AIR_C, "AIR_A": AIR_A, "zEU_C": P["EU"], "zUS_C": P["US"], "zTUR_C": tur}).to_parquet(RES + "/signals.parquet")
    j = pd.concat([AIR_C, AIR_A], axis=1).dropna()
    print("corr(C,A) =", round(j.corr().iloc[0, 1], 4), "pozisyon uyumu:",
          round(((np.sign(j.AIR_C) * (j.AIR_C.abs() > 1)) == (np.sign(j.AIR_A) * (j.AIR_A.abs() > 1))).mean(), 4), "n", len(j))
    rows = []
    for st in ["THYAO", "PGSUS", "TAVHL", "XU100", "XU030"]:
        y = bist_day(st + ".IS").intra
        for nm, s in [("C", AIR_C), ("A", AIR_A), ("COMBO_C", AIR_C - tur)]:
            for cost in [8, 15]:
                for per, r in bt_periods(s, y, cost, 1.0, ("IS", "OOS", "ALL")).items():
                    rows.append({"tgt": st, "sig": nm, "cost": cost, "per": per, **r})
    T = pd.DataFrame(rows)
    pd.set_option("display.width", 220)
    print(T[T.cost == 8].round(2).to_string(index=False))
    print(T[(T.cost == 15) & (T.sig == "C")].round(2).to_string(index=False))
    T.to_csv(RES + "/v1_replicate.csv", index=False)
