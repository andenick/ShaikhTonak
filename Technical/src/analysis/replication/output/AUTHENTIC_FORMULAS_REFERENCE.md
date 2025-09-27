# Authentic Formulas Reference for Table 5.4

This reference lists the algebraic identities used in the authentic phase. No interpolation is applied; missing inputs yield missing outputs.

Notation: s' (rate of surplus value), c' (organic composition), u (capacity utilization), SP (surplus product), S (surplus), K/KK (capital stock).

1) Utilization-adjusted surplus
    s_u_calc_t = s'_t × u_t
    Domain: s' and u present.

2) Identity profit rate (textbook)
    r_calc_t = s'_t / (1 + c'_t)
    Domain: c' present and (1+c') ≠ 0.

3) Unified capital naming (no inference)
    K_unified_t = KK_t if present, else K_t if present, else NaN.

4) Diagnostic capital growth
    gK_from_K_unified_t = (K_unified_t − K_unified_{t−1}) / K_unified_{t−1}

5) Profit rate candidate consistent with published r'
    r_sp_over_Ku_t = SP_t / (K_unified_t × u_t)

6) Derivations via SP
    V_from_SP_t = SP_t / s'_t
    C_from_SP_t = c'_t × V_from_SP_t

7) Alternative derivations via S
    V_from_S_t = S_t / s'_t
    C_from_S_t = c'_t × V_from_S_t

8) Diagnostic checks
    r_from_cv(SP)_t = SP_t / (C_from_SP_t + V_from_SP_t)
    r_from_cv(S)_t  =  S_t / (C_from_S_t  + V_from_S_t)

Policy: If inputs are missing or denominators are zero, results are NaN. No interpolation or smoothing is performed.
