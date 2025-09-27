# Perfect Replication Status (Faithful Track)

Primary purpose: exact replication of the book’s methodology and tables, and faithful extension using the same definitions.

## Phase 1 (1958–1989)
- r′: Replicated with r = SP/(K×u) (MAE ~0.0026; corr ~0.994). See `src/analysis/replication/output/PERFECT_REPLICATION_REPORT.md`.
- s′u: Identity holds in both parts within tight thresholds.
- gK: Pending exact definition (In/K*, capital concept, deflation). Not claimed “perfect” yet.
- Integrity: Book values preserved exactly; authenticity check PASS (0 mismatches).

## Phase 2 (1990→)
- Policy: No model-based scaling. Use S&T-equivalent modern definitions and sources for SP, K, and u; stop and request expert input where mapping is unclear.
- Expert insertions: See `docs/EXPERT_INSERTION_POINTS.md` and `docs/appendices/APPENDIX_INDUSTRY_CORRESPONDENCE.md`.

## Claims discipline
- Only the variables with implemented book-exact definitions and passing validations are labeled “perfectly replicated.”
- Items with definitional gaps are “pending exact definition.”

## Next steps
- Implement gK with book’s exact In and K*.
- Finalize S&T-equivalent modern mappings for SP and K (config-first approach).
- Document and validate utilization and deflators/base-year conventions.
