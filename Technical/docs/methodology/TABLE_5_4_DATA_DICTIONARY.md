# Table 5.4 Data Dictionary (Authentic Phase)

This document describes the columns included in `src/analysis/replication/output/table_5_4_authentic.csv`.

- year: Calendar year (int)
- I: Fixed investment (book value; units per book)
- I!: Alternative investment indicator (book value)
- K: Capital stock (Part 2 period; book value)
- K g: Capital growth rate (book value label; appears as `K g` in Part 2)
- KK: Capital stock (Part 1 period; book value)
- Pn: Nominal price index or price level (book value; Part 2 missing in extraction)
- S: Surplus (book value)
- SP: Surplus product or surplus-based measure (book series used for identities)
- b: Productive labor share (book value)
- c': Organic composition of capital ratio (book value)
- fn: Productivity factor (book value)
- gK: Growth rate of capital (book value; Part 1 row corrected from unnamed)
- r': Published rate of profit (book value)
- s: Surplus mass or related series (book value)
- s': Rate of surplus value (book value)
- s'u: s' adjusted by utilization (book value Part 1)
- s'«u: s' adjusted by utilization (book value Part 2 typographical variant)
- u: Capacity utilization (book value)

Derived identity-based columns (added; no interpolation):

- s_u_calc: s' × u (computed only where both inputs exist)
- V_from_SP: SP / s' (derived variable V)
- C_from_SP: c' × V_from_SP (derived variable C)
- r_prime_calc: SP / (K_unified × u), where K_unified = KK (1958–1973) ∪ K (1974–1989)

Notes:
- All original book columns are preserved exactly as extracted and cleaned in `table_5_4_authentic_raw_merged.csv`.
- No interpolation is performed; missing values remain missing.