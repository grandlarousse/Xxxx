"""cin ajanı - Adım 2: Çin vadeli işlem ORİJİNAL verisi (Sina Finance kamuya açık API).
 (a) Sürekli ana kontrat serisi  <CODE>0   (2006/2013+, roll sıçramalı, düzeltilmemiş)
 (b) Tekil kontratlar <CODE><YYMM> (Sina'da ~2018-05'ten sonra vadesi dolanlar mevcut) -> max-açık-pozisyon kuralıyla
     roll-düzeltilmiş getiri serisi (c03'te kurulur).
Kaynak: https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/InnerFuturesNewService.getDailyKLine?symbol=I0
Alanlar: d(tarih, Pekin işlem günü; gece seansı ertesi işlem gününe yazılır), o,h,l,c (kapanış 15:00 Pekin = 07:00 UTC), v, p(açık poz.), s(uzlaşma)
Veri dizini: scratchpad/data_cin/sina/ (indirilen = güvenilmeyen veri; sadece JSON ayrıştırılır)
"""
import os, re, json, time, sys, requests, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUT = SCR + "/data_cin/sina"; os.makedirs(OUT, exist_ok=True)
URL = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/InnerFuturesNewService.getDailyKLine?symbol={}"
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
# kod: (açıklama, borsa, kontrat ayları)
M3 = [1, 5, 9]; MALL = list(range(1, 13))
COMS = {
 "I": ("DCE demir cevheri", "DCE", M3), "J": ("DCE metalurjik kok", "DCE", M3), "JM": ("DCE koklaşabilir kömür", "DCE", M3),
 "RB": ("SHFE inşaat demiri", "SHFE", [1, 5, 10]), "HC": ("SHFE sıcak haddelenmiş rulo (HRC)", "SHFE", [1, 5, 10]),
 "CU": ("SHFE bakır", "SHFE", MALL), "AL": ("SHFE alüminyum", "SHFE", MALL), "NI": ("SHFE nikel", "SHFE", MALL),
 "ZN": ("SHFE çinko", "SHFE", MALL), "AU": ("SHFE altın", "SHFE", [2, 4, 6, 8, 10, 12]), "SS": ("SHFE paslanmaz", "SHFE", MALL),
 "TA": ("ZCE PTA", "ZCE", M3), "EG": ("DCE MEG (etilen glikol)", "DCE", M3), "PF": ("ZCE polyester elyaf", "ZCE", MALL),
 "PX": ("ZCE paraksilen", "ZCE", MALL), "FG": ("ZCE cam", "ZCE", M3), "SA": ("ZCE soda külü", "ZCE", M3), "UR": ("ZCE üre", "ZCE", M3),
 "MA": ("ZCE metanol", "ZCE", M3), "PP": ("DCE polipropilen", "DCE", M3), "L": ("DCE LLDPE", "DCE", M3), "V": ("DCE PVC", "DCE", M3),
 "EB": ("DCE stiren", "DCE", MALL), "SC": ("INE ham petrol (Orta Doğu sour)", "INE", MALL), "LU": ("INE düşük kükürtlü fuel oil", "INE", MALL),
 "FU": ("SHFE fuel oil", "SHFE", [1, 5, 9]), "BU": ("SHFE bitüm", "SHFE", [6, 12]), "SI": ("GFEX endüstriyel silisyum", "GFEX", MALL),
 "LC": ("GFEX lityum karbonat", "GFEX", MALL),
}
def get(sym):
    p = os.path.join(OUT, sym + ".json")
    if os.path.exists(p): return json.load(open(p)), True
    for a in range(4):
        try:
            r = S.get(URL.format(sym), timeout=30)
            m = re.search(r"\((\[.*\])\)", r.text, re.S)
            d = json.loads(m.group(1)) if m else []
            json.dump(d, open(p, "w")); return d, False
        except Exception as e:
            time.sleep(2 + 2 * a)
    return [], False

if __name__ == "__main__":
    only = sys.argv[1:] or list(COMS)
    for c in only:
        d, cached = get(c + "0"); print(c + "0", len(d), d[0]["d"] if d else "", d[-1]["d"] if d else "", flush=True)
        if not cached: time.sleep(0.3)
        _, _, months = COMS[c]
        for yy in range(18, 28):
            for mm in months:
                sym = f"{c}{yy:02d}{mm:02d}"
                if (yy, mm) > (27, 12): continue
                d, cached = get(sym)
                if not cached: time.sleep(0.25)
        print(c, "done", flush=True)
