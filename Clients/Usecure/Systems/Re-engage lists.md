---
type: system
client: Usecure
pattern: "[[Suppression list]]"
variant: "open lead OR contacted <30d OR in sequence"
enabled: true
built: 2026-08-19
verified: 2026-08-20
---
# Re-engage lists

MSP contacts who enquired since Jan 2025 and never bought.

| List | Purpose | Size |
|---|---|---|
| 3851 | main re-engage | 916 |
| 3854 | NFR subset | 159 |
| 3856 | suppression | 6,219 |

Suppression rules added 20 August at Scott's request - see
[[2026-08-20 Suppress recently contacted and sequenced]]. That removed 80 from the main
list and 33 from NFR. Overlap between send lists and suppression verified at zero.

Building these surfaced two API behaviours worth remembering:
[[List API constraints]] and [[Association type IDs worth knowing]].
