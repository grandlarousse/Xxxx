"""cin ajanı - Adım 3: Yahoo'nun BOZUK döndüğü (n=1) Çin endeksleri ve USD/CNH için Sina kaynağı.
Yahoo 000300.SS / 000016.SS / 000905.SS / 399006.SZ / XIN9.FGI / CNH=X -> tüm range seçeneklerinde 1 satır (31.10.2026 testi).
 - A-pay endeksleri: money.finance.sina.com.cn CN_MarketData.getKLineData (günlük kapanış 15:00 Pekin = 07:00 UTC)
 - USD/CNH: vip.stock.finance.sina.com.cn NewForexService.getDayKLine fx_susdcnh (2014-11+; kapanış saati belirsiz -> Pekin gece yarısı civarı varsayımı, DÜŞÜK güven hizalama)
Çapraz kontrol: sh000001 (Sina) vs 000001.SS (Yahoo).
"""
import os, re, json, time, requests, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUT = SCR + "/data_cin/sina_idx"; os.makedirs(OUT, exist_ok=True)
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
IDX = {"sh000300": "CSI 300", "sh000016": "SSE 50", "sh000905": "CSI 500", "sz399006": "ChiNext", "sh000001": "SSE Composite", "sz399001": "SZSE Component"}
if __name__ == "__main__":
    for s in IDX:
        r = S.get(f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={s}&scale=240&ma=no&datalen=10000", timeout=40)
        d = json.loads(r.text)
        df = pd.DataFrame(d); df["c"] = df["close"].astype(float); df["ldate"] = pd.to_datetime(df["day"])
        df[["ldate", "c"]].to_parquet(os.path.join(OUT, s + ".parquet")); print(s, len(df), df.ldate.min().date(), df.ldate.max().date()); time.sleep(0.4)
    r = S.get("https://vip.stock.finance.sina.com.cn/forex/api/jsonp.php/var%20_x=/NewForexService.getDayKLine?symbol=fx_susdcnh&_=1", timeout=40)
    m = re.search(r'\("(.*)"\)', r.text, re.S); rows = [x.split(",") for x in m.group(1).split("|") if x.strip()]
    df = pd.DataFrame([(x[0], float(x[4])) for x in rows if len(x) >= 5], columns=["day", "c"]); df["ldate"] = pd.to_datetime(df["day"])
    df[["ldate", "c"]].to_parquet(os.path.join(OUT, "USDCNH.parquet")); print("USDCNH", len(df), df.ldate.min().date(), df.ldate.max().date())
