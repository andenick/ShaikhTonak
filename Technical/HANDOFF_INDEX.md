# Project Handoff — Shaikh & Tonak Replication and Faithful Extension

Date: 2025-09-22

Purpose
- Provide a concise, actionable handoff so a new maintainer can run, audit, and extend the replication and faithful modern update without guesswork.

## 1) What this repo delivers

- Phase 1: Methodology-faithful replication of the book-era results (1958–1989)
  - r′ replicated using r = SP/(K×u) with near-perfect alignment
  - Identity checks (e.g., s′u) validated tightly
  - gK implemented per book intent as In/K* (with ΔK/K as diagnostic fallback)
- Phase 2: Faithful modern extension (1990+)
  - Uses only S&T-consistent inputs and the same identity: r = SP/(K×u)
  - Modern SP from BEA NIPA flat files; modern K from BEA Fixed Assets; u from Fed G.17
  - Raw and normalized variants preserved side-by-side

## 2) Run guide (one-liners)

- Integrate modern data (writes integrated CSV + metadata):
  - VS Code Task: "Run independent validator by path" (phase2_data_integration.py)
  - Or terminal: python "src/extension/phase2_data_integration.py"
- Build faithful combined series (historical + modern):
  - VS Code Task: "Run faithful S&T-only update" (run_phase2_faithful.py)
  - Or terminal: python "run_phase2_faithful.py"
- Run perfect replication engine (historical diagnostics + gK exact):
  - VS Code Task: "Run independent validator by path" for core engine if configured, or
  - Terminal: python "src/core/perfect_replication_engine.py"

Outputs will declare locations at the end of each run. See Artifacts Map below.

## 3) Artifacts map (key outputs)

- Historical replication outputs
  - src/analysis/replication/output/table_5_4_perfect_replication.csv
  - src/analysis/replication/output/PERFECT_REPLICATION_REPORT.md
  - src/analysis/replication/output/perfect_vs_authentic_comparison.csv
- Faithful extension outputs
  - data/modern/final_results_faithful/shaikh_tonak_faithful_1958_1989.csv
  - data/modern/final_results_faithful/shaikh_tonak_faithful_1958_2025.csv
  - results/extension/FAITHFUL_UPDATE_REPORT.md
  - results/extension/plots/*
- Integration outputs
  - data/modern/integrated/complete_st_timeseries_1958_2025.csv
  - data/modern/integrated/integration_metadata.json
- Builders (modern inputs)
  - data/modern/bea_nipa/modern_sp_st_consistent_1990_2025.csv
  - data/modern/processed/bea_fixed_assets/private_net_stock_current_cost.csv

## 4) Methodology highlights

- Profit rate identity: r = SP / (K × u)
  - Historical: r′ from book preserved; diagnostics confirm identity
  - Modern: computed only when S&T-consistent SP, K, and u exist
- gK definition (historical): Preferred In/K* (book-period capital K* = KK ∪ K; In from I/I!); ΔK/K used as diagnostic fallback
- Normalization: Raw SP/K retained; `_norm` columns added for scope/unit alignment. Faithful updater prefers `_norm`.

## 5) Expert insertion points (edit without code changes)

- Normalization policy (SP/K): docs/extension/NORMALIZATION_NOTES.md
- gK definition and data lineage: docs/extension/GK_DEFINITION_NOTES.md
- Phase 2 parameters (for broader experiments, if desired): config/expert_inputs/ (add new JSONs as needed). Current faithful path does not depend on growth/ratio proxies.

## 6) Quality gates (last run)

- Phase 2 integration + faithful update: exit code 0
- Perfect replication engine: exit code 0
- Validation summary (historical):
  - r′: MAE ≈ 0.00263; Corr ≈ 0.9938
  - gK (preferred In/K* else ΔK/K): MAE ≈ 0.01194; Corr ≈ 0.6012
  - s′u: MAE ≈ 0.00345–0.00369; Corr ≈ 0.985–0.989

## 7) Known limitations and guardrails

- Modern coverage is strict: modern r only emitted when SP, K, and u all present (no interpolation)
- SP/K normalization `_norm` currently equals raw; any scope/valuation updates must be documented and applied only to `_norm`
- Historical gK alignment depends on the exact In and K* concepts—if the book’s net investment differs from I/I!, swap it in via a small change to the engine

## 8) Where to look in the code

- Historical replication: src/core/perfect_replication_engine.py
- Faithful modern update: src/extension/phase2_faithful_st_only.py and run_phase2_faithful.py
- Integration: src/extension/phase2_data_integration.py
- Builders: src/extension/build_modern_sp_from_nipa.py, src/extension/extract_modern_k_from_fixed_assets.py

## 9) Quick troubleshooting

- Missing BEA flat files: Ensure archive paths exist for NIPA and Fixed Assets flat files
- u units issue (percent vs fraction): Faithful updater detects and converts when needed; double-check capacity_utilization median
- Columns missing in integration: Confirm builder outputs exist and re-run integration

## 10) Suggested next steps

- Finalize SP/K normalization rules if scope differences are confirmed; populate `_norm` columns and re-run
- If the book specifies a different In or a stricter K* valuation, wire it into the engine for gK
- Add a small CLI wrapper (argparse) for reproducible batch runs + a pinned environment file

---
Signature
- Signed by: OpenAI LLM (model identifier unavailable in this environment)
- Date: 2025-09-22
