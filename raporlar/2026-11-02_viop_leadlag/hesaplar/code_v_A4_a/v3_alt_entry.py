"""v3: Alternatif giriş — (i) saatlik ilk bar (06:30-07:30 UTC) KAPANIŞINDAN giriş (≈10:30 TSİ) -> günlük kapanış (kapanış seansı);
(ii) 2. bar kapanışı (≈11:30 TSİ) -> kapanış; (iii) açılış -> ilk bar kapanışı (ilk saatte ne kadarı gerçekleşiyor?);
(iv) VİOP pay vadelisi (en yüksek hacimli kontrat) açılış->kapanış getirisi (bülten verisi, 2023 + 2025-26).
Aynı günlerde Yahoo açılış girişli sonuçla eşleştirilmiş karşılaştırma. Çıktı: res/v3_*.csv, v3.log"""
import sys, glob; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_a")
from vcore import *
pd.set_option("display.width", 250)
ST = ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "XU030.IS"]
SA = pd.read_parquet(OUTD + "/v1_signals_A.parquet")
sig = SA.AIR.shift(1)

def h1_legs(sym):
    d = bist_day(sym)
    h = raw(sym, "h1").copy(); h["hm"] = h.index.strftime("%H:%M"); h.index = pd.DatetimeIndex(h.ldate)
    b1 = h[h.hm == "06:30"]; b1 = b1[~b1.index.duplicated()]
    b2 = h[h.hm == "07:30"]; b2 = b2[~b2.index.duplicated()]
    df = pd.DataFrame({"o": d.o, "c": d.c, "intra": d.intra}).join(b1[["o", "c"]].rename(columns={"o": "o1", "c": "c1"}), how="inner").join(b2[["c"]].rename(columns={"c": "c2"}), how="left")
    df = df[df.intra.notna()]
    df["first"] = np.log(df.c1 / df.o); df["rest1"] = np.log(df.c / df.c1); df["rest2"] = np.log(df.c / df.c2)
    df["o_match"] = (df.o1 / df.o - 1).abs() < 5e-4
    return df

def stats_line(lab, s, y, cost):
    o, pnl, pos = bt(s, y, cost, 1.0, split=pd.Timestamp("2100-01-01"))
    d = o["ALL"]
    return {"leg": lab, "cost": cost, "n": d.get("n"), "bps": d.get("bps"), "t_nw": d.get("t_nw"), "gross_bps": d.get("gross_bps"), "t_gross": d.get("t_gross"), "hit": d.get("hit")}

if __name__ == "__main__":
    rows = []
    for s in ST:
        L = h1_legs(s)
        print(s, "saatlik gün:", len(L), L.index.min().date(), L.index.max().date(), "Yahoo o == h1 ilk bar o oranı:", round(L.o_match.mean(), 3))
        for cost in [8, 15]:
            for lab, col in [("A: açılış(Yahoo o)->kapanış [aynı günler]", "intra"), ("B: ilk saatlik bar kapanışı(~10:30 TSİ)->kapanış", "rest1"),
                             ("C: 2. bar kapanışı(~11:30 TSİ)->kapanış", "rest2"), ("D: açılış->ilk bar kapanışı (sadece ilk saat)", "first")]:
                if cost == 15 and col == "first": continue
                r = stats_line(lab, sig, L[col], cost); r["target"] = s; rows.append(r)
    H = pd.DataFrame(rows); H.to_csv(OUTD + "/v3_h1_entry.csv", index=False)
    print("\n=== Saatlik veri dönemi (2023-11-30..2026-10-30), AIR t-1, |s|>1 ===")
    print(H.set_index(["target", "cost", "leg"]).round(2).to_string())
    # yıllara göre (8 bps) B bacağı
    print("\n=== B (10:30 giriş) yıllara göre, 8 bps net, bps/işlem ===")
    for s in ST[:3]:
        L = h1_legs(s)
        o, _, _ = bt(sig, L["rest1"], 8, 1.0, split=pd.Timestamp("2100-01-01")); oa, _, _ = bt(sig, L["intra"], 8, 1.0, split=pd.Timestamp("2100-01-01"))
        print(s, "B:", o["years"], "n", o["years_n"], "| A:", oa["years"])

    # VİOP bülteni: pay vadelisi açılış->kapanış (en yüksek işlem hacimli kontrat)
    print("\n=== VİOP pay vadelisi (bülten) açılış->kapanış hedefi ===")
    files = sorted(glob.glob(S + "/data/viop/viop_*.csv"))
    recs = []
    for f in files:
        try:
            x = pd.read_csv(f, sep=";", encoding="windows-1254", skiprows=[1], dtype=str)
        except Exception:
            continue
        x.columns = [c.strip() for c in x.columns]
        x = x[x["PAZAR SEGMENTI"].isin(["SSF"])]
        for und in ["THYAO", "PGSUS", "TAVHL"]:
            y = x[x["DAYANAK VARLIK"] == und + ".E"].copy()
            if y.empty: continue
            for c in ["ACILIS FIYATI", "KAPANIS FIYATI", "ISLEM HACMI", "UZLASMA FIYATI", "ISLEM SAYISI", "ACILIS SEANSI FIYATI"]:
                if c not in y.columns: y[c] = np.nan
                y[c] = pd.to_numeric(y[c].astype(str).str.replace(",", "."), errors="coerce")
            y = y.sort_values("ISLEM HACMI", ascending=False).iloc[0]
            recs.append({"date": pd.Timestamp(y["TARIH"]), "und": und, "o": y["ACILIS FIYATI"], "c": y["KAPANIS FIYATI"], "settle": y["UZLASMA FIYATI"],
                         "tv": y["ISLEM HACMI"], "ntr": y["ISLEM SAYISI"], "o_sess": y["ACILIS SEANSI FIYATI"], "code": y["SOZLESME KODU"]})
    V = pd.DataFrame(recs); V.to_csv(OUTD + "/v3_viop_front.csv", index=False)
    rows = []
    for und in ["THYAO", "PGSUS", "TAVHL"]:
        v = V[V.und == und].set_index("date").sort_index(); v = v[(v.o > 0) & (v.c > 0)]
        v["fintra"] = np.log(v.c / v.o); v["fintra_settle"] = np.log(v.settle / v.o)
        sp = bist_day(und + ".IS")
        j = v.join(sp[["intra", "o"]].rename(columns={"o": "spot_o"}), how="inner")
        print(und, "gün", len(j), "ort. işlem hacmi (mn TL)", round(v.tv.median() / 1e6, 1), "medyan işlem sayısı", int(v.ntr.median()),
              "corr(vadeli gün-içi, spot gün-içi)", round(j.fintra.corr(j.intra), 3), "medyan |vadeli açılış/spot açılış - 1| bps", round(1e4 * (j.o / j.spot_o - 1).abs().median(), 1))
        for cost in [8, 15]:
            for lab, col in [("VİOP vadeli açılış->kapanış", "fintra"), ("VİOP vadeli açılış->uzlaşma", "fintra_settle"), ("spot açılış->kapanış (aynı günler)", "intra")]:
                r = stats_line(lab, sig, j[col], cost); r["target"] = und; r["period"] = f"{j.index.min().date()}..{j.index.max().date()}"; rows.append(r)
    VV = pd.DataFrame(rows); VV.to_csv(OUTD + "/v3_viop_bt.csv", index=False)
    print(VV.set_index(["target", "cost", "leg"]).round(2).to_string())
    print("ok")
