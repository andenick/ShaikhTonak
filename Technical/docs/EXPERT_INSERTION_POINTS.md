# Expert Insertion Points (Faithful Track)

All discretionary decisions must be visible, editable, and validated. Do not embed judgments in code. This document lists the expert inputs and where they live.

## 1) SP (Surplus Product) definition mapping
- Purpose: Map modern NIPA lines to the S&T SP concept.
- Config (to be added): `config/expert_inputs/sp_mapping.yaml`
- Decisions:
  - Table IDs and line numbers; add/subtract items per S&T; nominal vs real; price base alignment.
- Validator: Compare resulting SP against Phase 1 SP on overlap years (if any) and check internal identities.

## 2) K (Capital) definition mapping
- Purpose: Map modern BEA Fixed Assets lines to S&T capital concept (K* if defined as net, etc.).
- Config (to be added): `config/expert_inputs/capital_mapping.yaml`
- Decisions:
  - Net vs gross; structures/equipment composition; price base; deflator series and rebase rules.
- Validator: Confirm r = SP/(K×u) holds with reasonable residuals; check trend continuity at 1989→1990.

## 3) u (Utilization) selection
- Purpose: Select series and weights that best match the S&T utilization concept.
- Config (to be added): `config/expert_inputs/utilization_mapping.yaml`
- Decisions:
  - Specific Fed series; sector weights; treatment of services vs goods sectors.
- Validator: Boundary behavior (1989→1990), identity checks with SP and K.

## 4) Industry aggregation (SIC→NAICS)
- Purpose: Align modern NAICS categories to S&T’s SIC-based sectors.
- Current scaffold: `config/industry_correspondences/st_naics_correspondence.json`
- Appendix: `docs/appendices/APPENDIX_INDUSTRY_CORRESPONDENCE.md` (curates and flags low-confidence areas)
- Validator: Sector shares and aggregates compare sensibly to S&T-era patterns.

## 5) Deflators & base-year conventions
- Purpose: Harmonize real/nominal consistency with S&T.
- Config (to be added): `config/expert_inputs/deflators.yaml`
- Decisions:
  - Chain-weighted vs fixed; base year; handling of revisions.
- Validator: Stability of ratios; absence of artificial structural breaks.

## 6) Sensitivity & provenance
- Keep a `decisions_log.json` (auto-generated) capturing current config versions and derived metrics.
- Run a short sensitivity analysis on key toggles (utilization weights, deflators) and store summary to `results/validation/faithful_sensitivity.json`.

## Workflow pattern
1. Fill configs (YAML/JSON) with explicit choices and citations.
2. Run validators to generate a decision log and boundary tests.
3. Review outcomes; if acceptable, lock the config versions and tag the run.
