# Appendix: Industry Correspondence (SIC → NAICS)

This appendix curates the working correspondence between S&T’s industry categories (SIC-era) and modern NAICS groupings used for the faithful extension.

- Base mapping file: `config/industry_correspondences/st_naics_correspondence.json`
- Status: Some correspondences are high confidence (e.g., Agriculture, Utilities). “Services” is low confidence and requires expert decision.

## Guidance for expert edits
- Start by reviewing the `mappings` list in the JSON; each entry shows S&T code → NAICS codes and a confidence level.
- For “Services,” decide whether to:
  - Keep as an aggregate for continuity, or
  - Split into sub-aggregates (e.g., Information; Professional & Technical; Health; etc.) if required by the analysis
- For FIRE (Finance, Insurance, Real Estate), S&T grouped these; NAICS splits 52 and 53. Confirm your aggregation rule.

## Review checklist
- Does the aggregation reproduce sensible sector shares vs. S&T-era shares when applied to modern data?
- Do sector-level surplus and capital ratios land in plausible ranges?
- Are any sectors missing or double-counted due to NAICS evolution?

## Where this is used
- Future faithful extension steps will read this mapping to build sectoral aggregates and to choose utilization weights consistent with S&T coverage assumptions.

## Provenance
- Source for original S&T sector definitions: Book Appendix A (cite exact pages when available).
- NAICS definitions: US Census/BEA NAICS documentation.
