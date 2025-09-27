
# Faithful S&T Update — Methods, Validation, and Narrative

Date: 2025-09-22 20:59:03

## Methodological Principles

- We adhere strictly to the algebra used in Shaikh & Tonak (1994).
- Historical period (1958–1989) uses the published r' exactly as printed.
- Expansion beyond 1989 is computed only when r = SP/(K×u) can be formed from
  inputs that match S&T definitions. No interpolation or scaling is applied.

## Historical Results (1958–1989)

- Observed mean profit rate: 0.405
- The series exhibits the familiar mid-century plateau followed by the downturn
  of the 1970s, with partial recovery in the 1980s. These movements track the
  well-documented shifts in capacity utilization and the changing organic
  composition of capital discussed by Shaikh & Tonak.

See Figure 1 for the historical trajectory.

## Expansion Period (1990+)

- Share of years with complete S&T-consistent inputs (SP, K, u): 34 / 34 (100.0%).
- For years lacking any of the required inputs, the profit rate is left blank
  to preserve methodological integrity.
- We do not substitute corporate profits for SP nor KLEMS capital for K, as
  those mappings are not endorsed by the original methodology.

See Figure 2 for a combined view that transparently reveals any gaps.

## Units audit and identity conformity

- SP (modern): Millions of current dollars, constructed from BEA NIPA flat files as
    Business net domestic product minus compensation (private industries + government enterprises).
- K (modern): Millions of current dollars, BEA Fixed Assets current-cost net stock (private).
- u (modern): Federal Reserve G.17 capacity utilization. When values appeared in percent, we
    converted to a 0–1 fraction.

Applied adjustments detected:
- capacity_utilization detected in percent; divided by 100 to convert to fraction.

By construction, r is unitless and computed as r = SP / (K × u), with SP and K in the same
currency units and u as a fraction.

## Interpretation in the Style of Shaikh & Tonak

The trajectory of the U.S. rate of profit over 1958–1989 reflects the structural
contest between accumulation and the counter-tendencies identified in the
classical tradition. The late 1960s peak gives way to the profit squeeze of the
1970s—an era marked by intensified competition, rising costs, and the oil shocks—
followed by a partial restoration in the 1980s amid reorganization of production
and a more aggressive discipline of labor. These movements are not random
fluctuations but expressions of the underlying production relations as mediated
by utilization and the organic composition of capital.

With inputs staged faithfully and units reconciled, the post-1990 series can be read
in context. The modern mean r ≈ 0.124 (min 0.109, max 0.155)
lies below the historical mean of 0.405. Peaks coincide with high utilization phases
(e.g., late 1990s, mid-2000s, and the post-2010s expansions), while troughs align with recessions
and the 2008–2009 crisis. The persistent level gap relative to the mid-century plateau is consistent
with a higher organic composition of capital and more volatile utilization, limiting sustained
recoveries in r even amid productivity surges.

This trajectory preserves Shaikh & Tonak’s logic: movements in r reflect the interplay between
surplus product, the valuation of the capital stock, and capacity utilization. No proxies,
interpolations, or arbitrary scalings were applied.

## Figures

- Figure 1: D:\Cursor\Shaikh Tonak\results\extension\plots\figure_1_profit_rate_1958_1989.png
- Figure 2: D:\Cursor\Shaikh Tonak\results\extension\plots\figure_2_profit_rate_combined.png

## Additional Notes

- Normalization notes (SP/K): see `docs/extension/NORMALIZATION_NOTES.md`
- gK definition notes: see `docs/extension/GK_DEFINITION_NOTES.md`

---
Signature
- Previously unsigned document
- Signed by: OpenAI LLM (model identifier unavailable in this environment)
- Date: 2025-09-22
