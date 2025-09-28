# Shaikh & Tonak Methodology Reconstruction Plan
## Complete Framework for Modern Data Extension (1990-2025)

### **CRITICAL OBJECTIVE**
Reconstruct modern period (1990-2025) using **Shaikh's exact methodology** from the 1994 book, maintaining perfect theoretical consistency with the historical period (1958-1989).

---

## **1. Shaikh's Exact Formula and Variable Definitions**

### **Core Profit Rate Formula**
```
r* = S*/(C* + V*)
```

### **Variable Definitions from Book**
From table_p342_camelot_0.csv and table_p347_camelot_0.csv:

#### **S\* (Surplus Value)**
```
S* = VA* - V* = surplus value (in money form)
```
Where:
- **VA\***: Marxian Net Value Added (productive sectors only)
- **V\***: Variable Capital (productive worker wages)

#### **Alternative S\* Calculation**
```
S* = SP* = FP* - NP* = surplus product
```
Where:
- **FP\***: Marxian Final Product
- **NP\***: Necessary Product = V\* (productive worker consumption)

#### **C\* (Constant Capital)**
```
C* = M'P = Materials inputs into production
```
From book methodology: Marxian constant capital (means of production)

#### **V\* (Variable Capital)**
```
V* = Wp = total variable capital = productive worker wage bill
```
From table_p336_camelot_0.csv line 40: "Total variable capital = V* = Wp"

---

## **2. Exact Sector Definitions**

### **Productive Sectors (Included)**
From book methodology:
- Manufacturing
- Mining
- Construction
- Transportation
- Agriculture
- Utilities

### **Unproductive Sectors (Excluded)**
From book text: *"nonfarm business minus finance, insurance, and real estate minus government enterprise minus professional services"*

**Exact Exclusions:**
1. Finance, insurance, and real estate
2. Government enterprises
3. Professional services
4. Trade (wholesale and retail)
5. Personal services

### **Modern NAICS to 1994 SIC Mapping**
Must create correspondence table mapping:
- 2025 NAICS industry codes → 1994 SIC codes → Shaikh's productive/unproductive classification

---

## **3. Modern Data Source Mapping**

### **For S\* (Surplus Value) Construction**

#### **Option A: VA\* - V\* Method**
```
S* = VA* - V*
```

**Modern Sources:**
- **VA\***: BEA Gross Value Added by Industry (productive sectors only)
- **V\***: BLS Employment Cost Index + Hours (productive sectors only)

#### **Option B: Property Income Method**
```
S* ≈ Corporate Profits + Proprietors' Income + Rental Income + Net Interest
```
**BUT**: Apply Shaikh's sector exclusions (remove unproductive sectors)

**Modern Sources:**
- BEA Corporate Profits by Industry
- BEA Proprietors' Income by Industry
- BEA Rental Income by Industry
- BEA Net Interest by Industry

### **For C\* (Constant Capital) Construction**

#### **Method: Intermediate Inputs**
```
C* = Intermediate goods and services (productive sectors only)
```

**Modern Sources:**
- BEA Input-Output Tables: Intermediate inputs by industry
- Apply Shaikh's sector exclusions
- Use appropriate deflators to maintain consistency

### **For V\* (Variable Capital) Construction**

#### **Method: Productive Worker Compensation**
```
V* = Compensation of productive workers only
```

**Modern Sources:**
- BLS Employment and Earnings by Industry
- BEA Compensation of Employees by Industry
- Apply productive/unproductive worker distinction
- Use Shaikh's sector definitions

---

## **4. Critical Implementation Requirements**

### **A. Maintain Book's Data Construction Rules**

1. **No Interpolation**: Preserve gaps where data unavailable
2. **Sector Purity**: Strict adherence to productive/unproductive distinction
3. **Vintage Consistency**: Use contemporaneous data sources when possible
4. **Deflator Methods**: Follow book's price adjustment methodology

### **B. Variable Calculation Sequence**

1. **Step 1**: Identify productive sectors using NAICS→SIC mapping
2. **Step 2**: Extract industry-level data for productive sectors only
3. **Step 3**: Calculate V\* = sum of productive worker compensation
4. **Step 4**: Calculate C\* = sum of productive sector intermediate inputs
5. **Step 5**: Calculate VA\* = sum of productive sector value added
6. **Step 6**: Calculate S\* = VA\* - V\*
7. **Step 7**: Calculate r\* = S\*/(C\* + V\*)

### **C. Quality Control Measures**

1. **Continuity Check**: Verify 1989-1990 transition makes economic sense
2. **Trend Validation**: Ensure modern results follow Marxian profit rate theory
3. **Cross-Validation**: Compare with alternative S\* calculation methods
4. **Historical Consistency**: Verify methodology produces book values for historical period

---

## **5. Data Sources and Implementation**

### **Primary Modern Sources**
1. **BEA Industry Economic Accounts** (Annual Industry Accounts)
2. **BLS Current Employment Statistics** (Industry employment/wages)
3. **BEA Input-Output Tables** (Intermediate inputs, 5-year benchmarks)
4. **Federal Reserve Industrial Production** (Capacity utilization weights)

### **Implementation Approach**

#### **Phase 1: Sector Mapping**
- Create definitive NAICS→SIC→Shaikh classification
- Validate against book's industry tables
- Handle industry evolution (new industries, mergers, etc.)

#### **Phase 2: Variable Construction**
- Build modern V\*, C\*, S\* for each year 1990-2025
- Apply exact book formulas and definitions
- Maintain theoretical consistency

#### **Phase 3: Validation**
- Compare 1989 book values with reconstructed 1989 using modern sources
- Verify methodology produces consistent results
- Check for structural breaks or anomalies

#### **Phase 4: Final Series Creation**
- Merge historical (1958-1989) with reconstructed modern (1990-2025)
- Create unified 67-year series using consistent r\* = S\*/(C\* + V\*) formula
- Generate comprehensive documentation and validation reports

---

## **6. Expected Outcomes**

### **Theoretical Consistency**
- Entire 1958-2025 series uses identical formula: r\* = S\*/(C\* + V\*)
- All variables constructed using Shaikh's exact definitions
- Sector exclusions applied consistently throughout

### **Resolution of Current Gap**
- Eliminate the artificial 39% vs 11% discontinuity
- Create economically meaningful transition at 1989-1990
- Enable valid long-term trend analysis

### **Scientific Validity**
- Restore project's credibility through methodological consistency
- Enable proper interpretation of profit rate movements
- Support valid conclusions about economic trends

---

## **7. Implementation Timeline**

### **Week 1: Sector Classification**
- Complete NAICS→SIC→Shaikh mapping
- Validate against historical data
- Create industry correspondence files

### **Week 2: Variable Construction**
- Build V\*, C\*, S\* calculation modules
- Implement exact book formulas
- Test against historical period

### **Week 3: Modern Data Integration**
- Apply methodology to 1990-2025 period
- Generate modern profit rate series
- Validate results and check consistency

### **Week 4: Final Integration**
- Merge historical and modern series
- Create final unified dataset
- Generate comprehensive documentation

---

## **Critical Success Factors**

1. **Exact Formula Adherence**: Never deviate from r\* = S\*/(C\* + V\*)
2. **Sector Definition Purity**: Maintain strict productive/unproductive distinction
3. **Variable Definition Consistency**: Use exact book definitions throughout
4. **Quality Control**: Extensive validation at each step
5. **Documentation**: Complete transparency in all methodological choices

This reconstruction will restore the project's scientific integrity and enable valid analysis of profit rate trends over the complete 67-year period.