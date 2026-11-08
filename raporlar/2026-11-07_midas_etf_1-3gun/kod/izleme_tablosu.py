"""IZLEME_LISTESI.md: nihai izleme listesinin tek tablo özeti (kademe, TradingView, maliyet, sürücüler, gerçek zamanlı izleme, kurallar).
Kullanım: python3 -I kod/izleme_tablosu.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import kartlar as K

ROOT = K.ROOT
FAM_ORDER = K.ORDER

def main():
    son = pd.read_csv(os.path.join(ROOT, "sonuclar", "izleme_son.csv"))
    son = son[son.karar.isin(["kabul", "yedek"])]
    L = ["# İzleme listesi — Midas ETF 1-3 gün (07.11.2026)", "",
         "Kademe: **A** = denetimden geçmiş kural var · **B** = kural var ama kanıt zayıf (küçük boyut / kağıt üstünde) · **C** = kural yok, sürücüleriyle takip.",
         "Karar: **kabul** = ana izleme · **yedek** = alternatif/kopya/kaldıraçlı araç. Ayrıntı ve tam lead-lag: `kartlar/<SYM>.md`. TradingView içe aktarma: `izleme_listeleri/`.",
         "⚠ = PTP/K-1 ürünü (Midas'ta satışta %10 brüt kesinti riski). Maliyet = 2.500$ pozisyonda gidiş-dönüş (komisyon 12 bp + makas).", ""]
    for fam in FAM_ORDER:
        res, den = K.load_fam(fam)
        if not res: continue
        sv, ov = K.verdict_maps(den)
        sub = son[son.aile == fam]
        if sub.empty: continue
        L += [f"## {K.FAM_TR[fam]}", "", "| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |", "|---|---|---|---|---|---|---|---|---|"]
        sub = sub.assign(_o=sub.karar.map({"kabul": 0, "yedek": 1}), _k=sub.kademe.map({"A": 0, "B": 1, "C": 2})).sort_values(["_o", "_k", "sym"])
        for _, r in sub.iterrows():
            sym = r.sym
            tv = K.TV_ETF.get(sym, "")
            tr = K.TAR.loc[sym] if sym in K.TAR.index else None
            ll = next((x for x in res.get("leadlag", []) if x["sym"].upper() == sym), {})
            dr = ", ".join(f"`{d['tv']}`" for d in (ll.get("suruculer") or [])[:2] if d.get("tv"))
            rt = ", ".join(f"`{g['tv']}`" for g in (ll.get("gercek_zamanli") or [])[:2] if g.get("tv"))
            rules = []
            for s in res.get("stratejiler", []):
                tools = [x.split(" ")[0].upper() for x in (s.get("islem_etf") or [])] + [(s.get("sinyal_etf") or "").split(" ")[0].replace("AMEX:", "").upper()]
                k = sv.get(s["id"], {}).get("karar")
                if sym in tools and k in ("dogrulandi", "zayif"):
                    rules.append(f"{s['ad'].split('—')[0].strip()[:48]} ({'doğrulandı' if k == 'dogrulandi' else 'zayıf'})")
            if sym == "SOXX": rules.append("SMH IBS<0,20 kopya aracı")
            ptp = " ⚠" if sym in K.PTP else ""
            L.append(f"| **{sym}**{ptp} | `{tv}` | {r.karar} | {r.kademe} | {K.num(tr['cost_rt_bp'],'{:.0f}') if tr is not None else '—'} | {K.num(tr['vol_1d_bp'],'{:.0f}') if tr is not None else '—'} | {'; '.join(rules) or '—'} | {dr or '—'} | {rt or '—'} |")
        L.append("")
    L.append("*Yatırım tavsiyesi değildir. Geçmiş performans geleceği garanti etmez.*")
    open(os.path.join(ROOT, "IZLEME_LISTESI.md"), "w").write("\n".join(L) + "\n")
    print("yazıldı", len(son))

if __name__ == "__main__":
    main()
