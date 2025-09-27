# Profit Rate Definition Investigation

## Executive Summary

This investigation examines why the published profit rate r' in Shaikh & Tonak (1994) Table 5.4
does not match the textbook Marxian identity r = s'/(1+c'), and identifies which alternative
definition best explains the observed values.

## Key Findings

### Best Matching Definition

**r = S/(K×u)**
- Description: Surplus over capital-utilization product
- MAE vs published r': 0.001433
- Max absolute error: 0.004650
- Correlation: 0.9969
- Observations: 15

## Alternative Definitions Tested

| Formula | Description | MAE | Max Error | Correlation | Obs |
|---------|-------------|-----|-----------|-------------|-----|
| r = s'/(1+c') | Standard textbook Marxian profit rate | 0.306753 | 0.394731 | -0.3735 | 32 |
| r = SP/(K×u) | Surplus product over capital-utilization product | 0.002219 | 0.007456 | 0.9968 | 31 |
| r = S/(K×u) | Surplus over capital-utilization product | 0.001433 | 0.004650 | 0.9969 | 15 |
| r = SP/K | Surplus product over capital stock | 0.045931 | 0.109837 | 0.7413 | 32 |
| r = SP/(C+V) where C=V×c'/(1-c'), V=SP/s' | Alternative organic composition interpretation | 0.372463 | 0.450400 | -0.3792 | 32 |

## Utilization Gap Analysis

Missing utilization data: [1973]

- 1973: Could interpolate as 0.915

## Period-Specific Analysis

### Part 1 (1958-1973) vs Part 2 (1974-1989)

The profit rate definition may work differently across periods due to:
- Different capital stock measures (KK vs K)
- Methodological changes in national accounts
- Economic structural changes

| Definition | Part 1 MAE | Part 2 MAE | Part 1 Corr | Part 2 Corr |
|------------|-------------|-------------|--------------|-------------|
| r = s'/(1+c') | 0.332208 | 0.281298 | -0.8353 | -0.6196 |
| r = SP/(K×u) | 0.001391 | 0.002995 | 0.9970 | 0.9823 |
| r = SP/K | 0.039409 | 0.052453 | -0.0544 | 0.5796 |
| r = SP/(C+V) where C=V×c'/(1-c'), V=SP/s' | 0.398425 | 0.346500 | -0.8324 | -0.6191 |

## Recommendations for Perfect Replication

1. **Use the best-matching definition** (r = S/(K×u)) for calculating profit rates from raw data
2. **Investigate the 1973 utilization gap** - consider whether to interpolate or leave as missing
3. **Validate period consistency** - ensure the same definition works across both periods
4. **Cross-reference with book text** - confirm theoretical justification for the empirical definition

## Technical Notes

- All calculations preserve authentic book values exactly
- Missing values are not interpolated in this analysis
- Error metrics calculated only on years with complete data
- Results suggest specific definitional conventions in Shaikh & Tonak's methodology
