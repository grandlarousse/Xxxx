"""D1: S1-S5'in bağımsız yeniden üretimi + işlem listesi karşılaştırması + ileriye bakma kontrolleri.
Çalıştır: python3 -I kod/denetim_metal_madenci/d1_yeniden.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M

AG = os.path.join(M.ROOT, "sonuclar", "aile_metal_madenci")

def ibs_sig(d, thr=0.10, down=True):
    rng = d["h"] - d["l"]
    ib = (d["c"] - d["l"]) / rng.where(rng > 0)
    s = ib < thr
    if down: s &= d["c"] < d["c"].shift(1)
    return s.fillna(False)

def month_end(d):
    idx = d.index; ym = idx.year * 100 + idx.month
    last = pd.Series(ym).shift(-1).values != ym
    s = pd.Series(last, index=idx); s.iloc[-1] = False   # veri kesiti: son bar ay sonu sayılmaz
    return s

def bb_sig(d, n=20, k=2.0):
    c = d["c"]; return (c < c.rolling(n).mean() - k * c.rolling(n).std()).fillna(False)

CANDS = {"S1": ("GDX", month_end, 3, "C0"), "S2": ("GLD", month_end, 3, "C0"), "S3": ("GDXJ", ibs_sig, 3, "C0"),
         "S4": ("GLD", ibs_sig, 3, "C0"), "S5": ("SILJ", bb_sig, 3, "C1")}
AGENT = {"S1": (111, 84.5, 2.20, 82.3, 86.5), "S2": (111, 39.9, 2.45, 33.8, 45.4), "S3": (240, 107.2, 3.39, 85.4, 127.6),
         "S4": (140, 39.3, 2.07, 54.6, 27.4), "S5": (48, 192.6, 3.10, 189.4, 195.3)}

def main():
    rows = []
    # NYSE takvim kontrolü: veride eksik işlem günü var mı (ay sonu tespitini bozar)
    hol = pd.read_csv(os.path.join(M.ROOT, "data", "events", "nyse_tatil.csv"))
    hol = pd.to_datetime(hol.loc[hol.event == "NYSE_tatil", "date"])
    for sym in ("GDX", "GLD", "GDXJ", "SILJ"):
        d = M.px(sym)
        bd = pd.bdate_range(d.index[0], d.index[-1]); bd = bd[~bd.isin(hol)]
        miss = bd.difference(d.index); extra = d.index.difference(bd)
        print(f"[takvim] {sym}: NYSE günlerinden eksik {len(miss)} {list(miss.date)[:6]} | fazladan {len(extra)} {list(extra.date)[:6]}")
    for k, (sym, f, h, mode) in CANDS.items():
        d = M.px(sym); s = f(d)
        cst = M.cost_static(d); cdy = M.cost_dynamic(d)
        for warm in (200, 0):
            s2 = s.copy()
            if warm: s2.iloc[:warm] = False
            tr = M.sim(d, s2, h, mode, cst)
            r = M.summ(tr, f"{k} {sym} {mode} h{h} warm{warm}"); r.update(id=k, sym=sym, warm=warm, cost=cst, maliyet="statik")
            rows.append(r)
            if warm == 200:
                trd = M.sim(d, s2, h, mode, cdy); rd = M.summ(trd, f"{k} dinamik maliyet"); rd.update(id=k, sym=sym, warm=warm, maliyet="dinamik", cost=float(cdy.reindex(trd["entry"]).mean()))
                rows.append(rd)
                trs = M.sim(d, s2, h, mode, cst, strict=True); rs = M.summ(trs, f"{k} katı çakışma"); rs.update(id=k, sym=sym, warm=warm, maliyet="statik_kati", cost=cst)
                rows.append(rs)
                # ajanın işlem listesiyle karşılaştır
                a = pd.read_csv(os.path.join(AG, f"aday_islemler_metal_madenci_{k}.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
                same = set(a["sig_date"]) == set(tr["sig"])
                mg = a.merge(tr, left_on="sig_date", right_on="sig", how="outer", indicator=True)
                dif = (mg["gross_x"] - mg["gross_y"]).abs().max()
                print(f"[{k}] ajan n={AGENT[k][0]} net={AGENT[k][1]} t={AGENT[k][2]} IS={AGENT[k][3]} OOS={AGENT[k][4]}")
                print(f"     denetim n={r['n']} brüt={r['gross_bp']:.1f} net={r['net_bp']:.1f} t={r['t']:.2f} IS={r['is_net_bp']:.1f}(t{r['is_t']:.2f}) OOS={r['oos_net_bp']:.1f}(t{r['oos_t']:.2f}) "
                      f"yıl+={r['yil_poz']:.2f} PF={r['pf']:.2f} maxDD={r['maxdd']:.3f} enkötü={r['worst_bp']:.0f} maliyet={cst:.1f}")
                print(f"     işlem tarihleri aynı mı: {same}; eşleşmeyen: {(mg['_merge']!='both').sum()}; maks brüt fark: {dif:.2e}")
                print(f"     dinamik maliyet: net={rd['net_bp']:.1f} t={rd['t']:.2f} (ort maliyet {rd['cost']:.1f} bp) | katı çakışma: n={rs['n']} net={rs['net_bp']:.1f} t={rs['t']:.2f}")
            else:
                print(f"     ısınma=0 (ilk 200 gün dahil): n={r['n']} net={r['net_bp']:.1f} t={r['t']:.2f} IS={r['is_net_bp']:.1f}(t{r['is_t']:.2f}) OOS={r['oos_net_bp']:.1f}")
    pd.DataFrame(rows).to_csv(os.path.join(M.OUTD, "d1_yeniden.csv"), index=False)

if __name__ == "__main__":
    main()
