# Methodological Divergences: Shaikh & Tonak Extension to Present Day

**Date**: September 22, 2025
**Purpose**: Document every divergence from original S&T (1994) methodology in Phase 2 extension
**Principle**: Transparent adaptation with explicit rationale for all changes

---

## Critical Requirement: Zero Undocumented Divergences

This document catalogs **every single methodological change** required to extend Shaikh & Tonak (1994) to present day (1990-2025). Any deviation from the original methodology must be:

1. **Documented** with explicit description
2. **Justified** with clear rationale  
3. **Quantified** with impact assessment
4. **Validated** through sensitivity analysis
5. **Expert-approved** where discretionary choices exist

---

## Classification of Divergences

### **Type A: Forced Adaptations** 
*Required due to data/definitional changes - no choice*

### **Type B: Methodological Choices**
*Expert discretion required - multiple valid approaches*

### **Type C: Technical Implementations**
*Computational/processing differences - same conceptual approach*

---

## **TYPE A: FORCED ADAPTATIONS**

### A1. Industry Classification System Change

**Original S&T Method**: 
- Used Standard Industrial Classification (SIC) system
- Industries based on 1980s economic structure
- 12 major industry categories as per S&T Appendix A

**Required Modern Adaptation**:
- Must use North American Industry Classification System (NAICS)
- NAICS implemented starting 1997, fully adopted by 2002
- 20+ major NAICS sectors vs 12 S&T categories

**Rationale**: 
- SIC system discontinued - no choice but to use NAICS
- Government data only available in NAICS format post-1997
- Required for consistent time series 1990-2025

**Implementation**:
- Create correspondence mapping: SIC-based S&T categories → NAICS sectors
- Expert input required for aggregation decisions
- Document all mapping choices in expert input spreadsheet

**Impact**: 
- May affect sector-level surplus and composition calculations
- Could introduce measurement differences vs historical period
- Requires validation through sensitivity analysis

**Status**: ✓ Framework created, expert input required

---

### A2. Service Sector Structural Changes

**Original S&T Method**:
- Single "Services" category (ST_11)
- Reflected 1980s service sector structure
- Services ~25% of economy in S&T period

**Required Modern Adaptation**:
- Services now ~70% of economy (2025)
- NAICS creates 9 distinct service sectors:
  - Information (51) - didn't exist in 1980s
  - Professional Services (54)
  - Management Services (55) 
  - Administrative Services (56)
  - Educational Services (61)
  - Health Care (62)
  - Arts/Entertainment (71)
  - Accommodation/Food (72)
  - Other Services (81)

**Rationale**:
- Economic structure fundamentally changed since 1980s
- Cannot ignore Information sector (tech boom)
- Service heterogeneity now critical for surplus analysis

**Implementation Options** (Expert Decision Required):
1. **Aggregate All**: Combine all service NAICS into single S&T Services category
2. **Selective Disaggregation**: Separate Information sector, aggregate others
3. **Full Disaggregation**: Treat major service sectors separately

**Impact**: 
- Choice affects service sector surplus calculations
- May change overall economy surplus composition
- Critical for analyzing post-1990 structural changes

**Status**: ⚠️ Expert decision required

---

### A3. Data Source Institutional Changes

**Original S&T Method**:
- Used BEA data as available in early 1990s
- Fixed-weight price indices
- Different corporate profits definitions
- Capital stock measurement conventions of 1980s

**Required Modern Adaptation**:
- BEA methodology evolved significantly:
  - Chain-weighted price indices (introduced 1996)
  - Enhanced corporate profits detail by industry
  - Improved capital stock measurement
  - Different depreciation methodologies

**Rationale**:
- Must use contemporary BEA methodology for consistency
- Historical data revised using modern methodology
- Cannot replicate exact 1994 data processing

**Implementation**:
- Use current BEA methodology for entire 1990-2025 period
- Apply same methodology to 1958-1989 for consistency check
- Document any temporal inconsistencies

**Impact**:
- May create artificial break at 1989-1990 transition
- Could affect deflation and real value calculations
- Requires validation for trend continuity

**Status**: ⚠️ Implementation needed

---

## **TYPE B: METHODOLOGICAL CHOICES**

### B1. Information Sector Treatment

**Issue**: NAICS Information sector (51) didn't exist in S&T period

**Expert Decision Required**:
- **Option 1**: Include in Services aggregate (maintain S&T structure)
- **Option 2**: Treat as separate sector (reflect modern economy)
- **Option 3**: Distribute across other sectors based on function

**S&T Framework Implications**:
- Information sector often high-surplus, low-capital intensity
- Could significantly affect economy-wide surplus rate
- May require separate theoretical treatment

**Recommendation**: Expert input required - significant impact on results

**Status**: ⚠️ Expert decision pending

---

### B2. Manufacturing Durable/Nondurable Split

**Original S&T Method**:
- Separated durable goods manufacturing (ST_04)
- Separated nondurable goods manufacturing (ST_05)
- Used SIC-based definitions

**Modern Challenge**:
- NAICS Manufacturing (31-33) can be subdivided differently
- Modern durable/nondurable definitions may differ
- Some products hard to classify (electronics, etc.)

**Expert Decision Required**:
- **Option 1**: Use BEA's durable/nondurable classification
- **Option 2**: Create custom classification matching S&T intent
- **Option 3**: Treat manufacturing as single sector

**Impact**: Affects manufacturing sector surplus analysis consistency

**Status**: ⚠️ Expert decision required

---

### B3. Government Sector Boundaries

**Original S&T Method**:
- Government sector (ST_12) 
- 1980s definition of government activities

**Modern Challenge**:
- Government outsourcing increased significantly
- Public-private partnerships
- Government enterprises vs administration

**Expert Decision Required**:
- How to handle privatized formerly-government activities
- Treatment of government enterprises
- Boundary definition consistency

**Status**: ⚠️ Expert decision required

---

## **TYPE C: TECHNICAL IMPLEMENTATIONS**

### C1. Capacity Utilization Source Change

**Original S&T Method**:
- S&T estimated capacity utilization rates
- Industry-specific methodology (details in S&T text)

**Modern Implementation**:
- Use Federal Reserve G.17 capacity utilization data
- Fed methodology may differ from S&T approach
- More detailed industry breakdown available

**Rationale**:
- Fed data is standard, widely-accepted measure
- Consistent methodology across full time period
- Higher quality than attempting to replicate S&T estimates

**Impact**: 
- May affect profit rate calculations (r = SP/(K×u))
- Different utilization rates → different profit rates
- Requires cross-validation

**Status**: ✓ Fed data to be used, validation needed

---

### C2. Price Deflation Methodology

**Original S&T Method**:
- Used price deflation methods available in 1994
- Likely fixed-weight indices
- Specific base year choices

**Modern Implementation**:
- Use BEA's current chain-weighted deflation
- Modern base year conventions
- More sophisticated deflation methodology

**Rationale**:
- Modern methodology is superior
- Ensures consistency across full time period
- Avoids index number problems

**Impact**:
- May affect real vs nominal variable relationships
- Could change temporal patterns
- Requires validation for economic sensibility

**Status**: ✓ Modern BEA methodology to be used

---

### C3. Corporate Profits Definition Evolution

**Original S&T Method**:
- Used corporate profits as defined by BEA circa 1994
- Specific adjustments for S&T framework (details in text)

**Modern Implementation**:
- Use current BEA corporate profits by industry
- Map to S&T "Surplus Product" (SP) definition
- Apply comparable adjustments using modern data

**Rationale**:
- BEA corporate profits concepts evolved
- Enhanced industry detail now available
- Need consistency with S&T conceptual framework

**Impact**:
- Core variable for profit rate calculation
- Must maintain conceptual consistency with S&T SP
- Critical for replication validity

**Status**: ⚠️ Implementation and validation needed

---

## **EXPERT INPUT REQUIREMENTS**

### High Priority Decisions (Must be resolved first)

1. **Service Sector Aggregation** (Impact: High)
   - How to map 9 NAICS service sectors to S&T Services category
   - Treatment of Information sector
   - Expert input spreadsheet: Sheet "Expert_Decisions" Row 1

2. **Manufacturing Subdivision** (Impact: Medium)
   - Durable/nondurable split methodology
   - Consistency with S&T intent
   - Expert input spreadsheet: Sheet "Expert_Decisions" Row 2

3. **Industry Correspondence Validation** (Impact: High)
   - Review all 12 S&T → NAICS mappings
   - Expert input spreadsheet: Sheet "Industry_Mapping"

### Medium Priority Decisions

4. **Government Sector Boundaries** (Impact: Medium)
5. **Corporate Profits Adjustments** (Impact: High - but can be iterative)
6. **Base Year and Deflation Choices** (Impact: Medium)

---

## **VALIDATION REQUIREMENTS**

For each divergence, the following validation must be performed:

### 1. Transition Continuity Test
- Check for artificial breaks at 1989-1990 boundary
- Ensure smooth trend continuation where economically expected

### 2. Cross-Variable Identity Validation
- Verify r = SP/(K×u) identity holds in extended data
- Check accounting relationships remain valid

### 3. Economic Sensibility Test
- Extended series should show reasonable economic patterns
- Major economic events should be reflected appropriately

### 4. Sensitivity Analysis
- Test alternative choices for each Type B divergence
- Quantify impact on key results

### 5. Expert Review
- Independent expert validation of all discretionary choices
- Sign-off on final methodology

---

## **IMPLEMENTATION CHECKLIST**

### Stage 1: Expert Input Collection ⚠️ **IN PROGRESS**
- [ ] Expert review of industry correspondences
- [ ] Service sector aggregation decision
- [ ] Manufacturing subdivision decision
- [ ] Government boundaries decision
- [ ] All expert decisions documented and justified

### Stage 2: Technical Implementation
- [ ] Industry mapping algorithms coded
- [ ] Modern data collection pipeline
- [ ] Variable construction following adaptations
- [ ] Corporate profits → SP mapping
- [ ] Capacity utilization integration

### Stage 3: Validation and Quality Assurance
- [ ] Transition continuity tests
- [ ] Identity validation
- [ ] Economic sensibility checks
- [ ] Sensitivity analysis for all Type B choices
- [ ] Expert sign-off on final results

### Stage 4: Documentation
- [ ] Final divergences catalog
- [ ] Impact quantification for each divergence
- [ ] Rationale documentation for all choices
- [ ] Validation results summary

---

## **SUCCESS CRITERIA**

1. **Zero Undocumented Divergences**: Every change from S&T methodology explicitly cataloged
2. **Expert Validation**: All Type B choices reviewed and approved by expert
3. **Quality Maintenance**: Extended series meets Phase 1 quality standards
4. **Economic Validity**: Results make economic sense for 1990-2025 period
5. **Reproducibility**: Complete methodology allows independent replication

---

**Document Status**: ⚠️ ACTIVE - Expert input required for completion
**Next Action**: Expert review of industry correspondences and methodological choices
**Timeline**: Expert decisions needed within 5 days for on-schedule Phase 2 completion

**Expert Contact**: [Contact information for questions and clarifications]
