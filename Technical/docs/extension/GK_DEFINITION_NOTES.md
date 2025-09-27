# gK Definition Notes (In/K*)

Purpose
- Document the exact treatment of gK in the replication and clarify its separation from SP/K normalization.

Definition implemented
- Preferred: gK_exact = In / K*, where
  - K* = KK for 1958–1973 (book Part 1 capital) and K for 1974–1989 (book Part 2 capital)
  - In = book investment series, preferring `I` if available, else `I!`
- Diagnostic fallback: gK_delta = ΔK / K using the unified capital series K_unified = KK ∪ K.
- Preferred gK = gK_exact when available; otherwise use gK_delta for transparency.

Why separate from normalization
- gK uses the book-period capital concept (K*) and book investment (In); it does not depend on modern SP/K normalization choices.
- SP/K normalization affects the modern profit-rate extension. gK pertains to the historical book table replication.

Coverage (from latest run)
- gK_exact years (In/K*): 16
- gK_delta years (ΔK/K diagnostic): 31
- Preferred gK coverage: 31

Next steps (if desired)
- If the book specifies a different net investment series (e.g., a dedicated net flow distinct from `I`/`I!`), substitute it into In.
- If K* differs in valuation or coverage across subperiods beyond KK/K, map those specifics into the K* build.
- Report side-by-side (published gK vs. gK_exact vs. gK_delta) is available in `src/analysis/replication/output/perfect_vs_authentic_comparison.csv`.

---
Signature
- Signed by: OpenAI LLM (model identifier unavailable in this environment)
- Date: 2025-09-22
