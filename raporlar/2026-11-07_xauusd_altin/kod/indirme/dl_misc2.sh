#!/bin/bash
S=$1
fetch() { # url out
  for a in 1 2 3 4 5 6; do
    code=$(curl -sS -L -A "Mozilla/5.0" --max-time 90 -o "$2.part" -w "%{http_code}" "$1" 2>/dev/null)
    if [ "$code" = "200" ] && [ -s "$2.part" ]; then mv "$2.part" "$2"; return 0; fi
    rm -f "$2.part"; sleep $((a*3))
  done
  echo "FAIL $1"
}
mkdir -p $S/data/cftc
for y in hist_2006_2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026; do
  [ -s $S/data/cftc/fut_disagg_txt_$y.zip ] || fetch "https://www.cftc.gov/files/dea/history/fut_disagg_txt_$y.zip" $S/data/cftc/fut_disagg_txt_$y.zip
done
echo "cftc done"
fetch "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls" $S/data/misc/gpr_daily.xls
fetch "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/InnerFuturesNewService.getDailyKLine?symbol=AU0" $S/data/misc/sina_AU0.txt
fetch "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/InnerFuturesNewService.getDailyKLine?symbol=AG0" $S/data/misc/sina_AG0.txt
fetch "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm" $S/data/misc/fomc_calendar.html
fetch "https://www.spdrgoldshares.com/assets/dynamic/GLD/GLD_US_archive_EN.csv" $S/data/misc/gld_archive.csv
for sid in DFII10 DFII5 T10YIE T5YIE T5YIFR DGS10 DGS2 DGS3MO DGS30 DTWEXBGS DTWEXAFEGS DTWEXEMEGS VIXCLS GVZCLS OVXCLS BAMLH0A0HYM2 BAMLC0A0CM DFF SOFR USEPUINDXD T10Y2Y T10Y3M DCOILBRENTEU DCOILWTICO NFCI WALCL RRPONTSYD DEXCHUS DEXINUS DEXJPUS DEXUSEU DEXSZUS DEXSFUS SP500 NASDAQCOM CPIAUCSL CPILFESL UNRATE PAYEMS ICSA M2SL STLFSI4 DTB3 EFFR; do
  [ -s $S/data/fred/$sid.csv ] || fetch "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$sid" $S/data/fred/$sid.csv
  sleep 0.5
done
echo "fred done $(ls $S/data/fred | wc -l)"
echo "ALL DONE"
