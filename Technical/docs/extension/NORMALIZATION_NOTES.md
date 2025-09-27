# Normalization Notes (SP/K)

This note documents how we treat normalization for SP and K in the faithful pipeline.

Principles
- Preserve raw (as-extracted) series unchanged.
- Add normalized variants alongside raw to make unit/scope alignment explicit.
- Prefer normalized variants in the modern identity r = SP/(K×u); keep raw for transparency and auditing.

What exists now
- SP (modern, BEA NIPA construction):
  - Raw: `modern_SP_st_consistent`
  - Normalized: `modern_SP_st_consistent_norm` (currently equal to raw)
- K (modern, BEA Fixed Assets):
  - Raw: `modern_K_st_consistent`
  - Normalized: `modern_K_st_consistent_norm` (currently equal to raw)

Rationale for normalized variants
- Ensures SP and K are in the same valuation and scope when computing r.
- Enables future adjustments (e.g., scope filtering, re-valuation) without breaking provenance of raw data.

When normalized will diverge from raw
- If SP scope is narrowed/expanded to match the K concept (e.g., excluding sectors not in private fixed assets stock).
- If valuation adjustments are needed to ensure consistent price basis between SP and K.

Auditability
- Integration metadata (`data/modern/integrated/integration_metadata.json`) records units for both raw and normalized columns.
- Faithful update prefers `_norm` columns when present.

Open items
- Confirm exact scope alignment between NIPA Business NDP minus compensation and Fixed Assets private net stock.
- If adjustments are required, implement them only in the `_norm` columns and record the rules here.

---
Signature
- Signed by: OpenAI LLM (model identifier unavailable in this environment)
- Date: 2025-09-22
