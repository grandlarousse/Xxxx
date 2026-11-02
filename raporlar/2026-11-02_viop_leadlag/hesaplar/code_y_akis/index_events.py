"""Endeks dönem değişiklikleri olay listesi (web kaynaklı; kaynaklar rapor ekinde). ann_react = ilk tam tepki günü (duyuru seans sonrası ise ertesi iş günü);
intra_ann=True: duyuru seans içinde (tepki duyuru günü başlar). eff_eve = yürürlük öncesi son işlem günü (endeks fonlarının kapanışta dengelediği gün)."""
EV = [
 dict(q='2024Q4', ann='2024-09-21', react='2024-09-23', intra_ann=False, eff_eve='2024-09-30', src='foreks 66eee6e7 (ObjectId zaman damgası 2024-09-21 15:31 UTC)',
      BIST30_in=['MGROS', 'TTKOM', 'ULKER'], BIST30_out=['BRSAN', 'GUBRF', 'OYAKC']),
 dict(q='2025Q3', ann='2025-06-20', react='2025-06-23', intra_ann=False, eff_eve='2025-06-30', src='borsagundem 20.06.2025 22:42 + getmidas',
      BIST30_in=['GUBRF'], BIST30_out=['HEKTS'], BIST50_in=['DSTKF', 'KUYAS'], BIST50_out=['ENJSA', 'ZOREN']),
 dict(q='2025Q4', ann='2025-09-12', react='2025-09-15', intra_ann=False, eff_eve='2025-09-30', src='borsagundem 12.09.2025 21:37',
      BIST30_in=['DSTKF'], BIST30_out=['CIMSA'], BIST100_in=['DAPGM', 'ECILC', 'PATEK', 'TSPOR', 'TUKAS'], BIST100_out=['ALFAS', 'AVPGY', 'BERA', 'LMKDC', 'SMRTG']),
 dict(q='2026Q1', ann='2025-12-23', react='2025-12-23', intra_ann=True, eff_eve='2025-12-31', src='infoyatirim 23.12.2025 17:33 TSİ (seans içi)',
      BIST50_in=['BTCIM', 'PASEU'], BIST50_out=['TKFEN', 'VESTL'], BIST100_in=['IZENR', 'KLRHO', 'QUAGR'], BIST100_out=['BINHO', 'CLEBI', 'IEYHO']),
 dict(q='2026Q2', ann='2026-03-19', react='2026-03-23', intra_ann=False, eff_eve='2026-03-31', src='cnbce h27000 19.03.2026 15:59 (arife yarım gün, seans kapalı)',
      BIST30_in=['VAKBN'], BIST30_out=['ULKER'], BIST50_in=['CANTE', 'TURSG'], BIST50_out=['DOHOL', 'SOKM'],
      BIST100_in=['CVKMD', 'EUREN', 'PAHOL', 'PSGYO', 'SARKY'], BIST100_out=['EGEEN', 'KCAER', 'TSPOR', 'TTRAK', 'YEOTK']),
 dict(q='2026Q4', ann='2026-09-21', react='2026-09-22', intra_ann=False, eff_eve='2026-09-30', src='genelekonomi 21.09.2026',
      BIST30_in=['TRMET'], BIST30_out=['DSTKF'], BIST50_in=['CVKMD', 'CWENE', 'DOAS', 'ENERY', 'MAVI', 'TSKB'], BIST50_out=['DSTKF', 'EFOR', 'KTLEV', 'KUYAS', 'MIATK', 'PASEU'],
      BIST100_in=['AGHOL', 'AHGAZ', 'AKCNS', 'AKFYE', 'ALBRK', 'ANHYT', 'AYGAZ', 'BINHO', 'ECZYT', 'EGEEN', 'EGGUB', 'ENTRA', 'GLYHO', 'GWIND', 'ISDMR', 'KARSN', 'KATMR', 'KCAER', 'KORDS', 'LMKDC', 'RGYAS', 'RYSAS', 'SNGYO', 'TABGD', 'TCKRC', 'TRGYO', 'TTRAK'],
      BIST100_out=['BALSU', 'BSOKE', 'DAPGM', 'DSTKF', 'EFOR', 'ESEN', 'EUPWR', 'GENIL', 'GESAN', 'GRTHO', 'GSRAY', 'IEYHO', 'IZENR', 'KLRHO', 'KTLEV', 'KUYAS', 'MAGEN', 'MIATK', 'ODINE', 'PASEU', 'PATEK', 'PSGYO', 'QUAGR', 'RALYH', 'REEDR', 'SARKY', 'SKBNK']),
]
