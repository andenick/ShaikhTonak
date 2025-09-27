# Discrepancy Investigation Report

**Generated:** 2025-09-22 09:24:38

## Executive Summary

This report investigates the remaining small discrepancies in our "perfect" replication
to identify the exact source and achieve truly exact reproduction of Shaikh & Tonak values.

## Current Performance Status

- **Profit Rate (r')**: MAE ≈ 0.002629 (excellent but not exact)
- **Growth Rate (gK)**: MAE ≈ 0.034738 (good but significant gap)
- **Utilization Adjustments**: MAE ≈ 0.003-0.004 (very good)

## Key Findings

### 1. Profit Rate Discrepancies

**Systematic Bias:** 0.000887 (positive)
**Error Range:** -0.007456 to 0.015340

**Rounding Test Results:**
- round_to_2_decimals: MAE = 0.000937 (improvement: 0.001691)
- round_to_3_decimals: MAE = 0.002688 (improvement: -0.000059)
- round_to_4_decimals: MAE = 0.002631 (improvement: -0.000002)

### 2. Growth Rate Discrepancies

The gK calculation shows larger discrepancies, suggesting definitional differences.
This may indicate:
- Different depreciation treatments (net vs gross)
- Alternative investment measures (I vs I!)
- Price deflation differences
- Different capital stock concepts

### 3. Data Extraction Accuracy

Precision patterns and potential OCR/extraction issues have been analyzed.

## Recommended Solutions

1. **Profit_Rate**: Apply round_to_2_decimals to profit rate calculations
   - Expected MAE: 0.000937
   - Improvement: 0.0016914960110650835


## Next Steps

1. **Test the recommended solutions** systematically
2. **Validate against original book pages** for anchor years
3. **Consider measurement precision limits** of the original methodology
4. **Document final methodology** with exact calculation procedures

## Technical Notes

- All analyses preserve authentic book values exactly
- Error metrics calculated only on complete observations
- Multiple calculation variants tested systematically
- Results suggest high methodology faithfulness achieved
