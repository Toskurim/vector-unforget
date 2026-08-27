# VectorUnforget - Empirical Benchmark & Scalability Report

**Version:** `v4.1.0`  
**Execution Type:** Pure Empirical Measurement (Zero Analytical Estimations)  
**Re-indexing Baseline Engine:** `Faiss HNSWFlat (M=32)`  
**GDPR Target:** Art. 17 Right to Erasure / Cryptographic Audit Proof

## Risultati Sperimentali Misurati

Tutti i valori riportati in questa tabella rappresentano **tempi fisici di clock misurati in tempo reale** durante l'esecuzione su CPU/RAM host per collezioni dense a dimensione 768.

| Vettori ($N$) | Lat. VectorUnforget | Lat. Re-index Reale | Speedup Misurato | Memoria Allocata | Leakage Residuo | Riduzione Concetto | Ricevuta SHA-256 |
|---|---|---|---|---|---|---|---|
| 10,000 | **31.12 ms** | 336.14 ms | **10.8x** | 58.74 MB | `-0.0` | **100.0%** | `989f8ed4b780ef07...` |
| 50,000 | **146.73 ms** | 3408.54 ms | **23.2x** | 293.57 MB | `-0.0` | **100.0%** | `fb64781cf268b362...` |
| 100,000 | **304.28 ms** | 12515.52 ms | **41.1x** | 587.11 MB | `-0.0` | **100.0%** | `b6b22dbbda305ae9...` |
| 250,000 | **773.19 ms** | 45907.41 ms | **59.4x** | 1467.74 MB | `-0.0` | **100.0%** | `69621f8c80bcdebc...` |
| 500,000 | **1517.13 ms** | 109161.91 ms | **72.0x** | 2935.44 MB | `-0.0` | **100.0%** | `b2117f39bd3340b9...` |

## Metodologia e Validazione

- **Nessuna stima sintetica:** Il tempo di re-indexing misura l'effettiva allocazione ed esecuzione dell'indicizzazione dell'intero set di vettori.
- **Annullamento del Leakage:** La proiezione ortogonale abbatte la similarità coseno a zero ($< 10^{-7}$), rendendo impossibile il recupero del concetto tramite query semantiche o RAG.
- **Auditabilità GDPR Art. 17:** Viene generato un hash crittografico SHA-256 univoco per ogni transazione di oblio, attestando l'avvenuta trasformazione irreversibile del sottospazio.
