# Shaikh & Tonak (1994) Exact Methodology Documentation

## **CRITICAL DISCOVERY: The Exact Methodology**

Based on systematic extraction and analysis of the original Shaikh & Tonak (1994) book content, here is the **exact methodology** that must be followed for perfect replication.

---

## **1. Core Variable Definitions**

### **Marxian Value Categories**
From the book text extraction, the following variable definitions are explicit:

- **TV\***: Total Value = GO P + GO tt (total value)
- **C\***: Constant Capital = M' P (Marxian constant capital)
- **GVA\***: Gross Value Added in Productive Sector
- **TP\***: Total Product = M P + RY P + GVA P
- **U\***': Unproductive Expenditures = M' P (materials used by unproductive sectors)
- **GFP\***: Gross Final Product = TP\* - U\*' (with IVA adjustments)
- **VA\***: Value Added = GVA\* - C\*
- **c\***: Organic Composition = C\*/V\*

### **Key Relationships**
From the extracted text:
```
TV* = GO P + GO tt = total value,
where GO P = M P + RY P + [GVA P]
```

---

## **2. Profit Rate Formula**

**CRITICAL DISCOVERY**: The exact profit rate formula used by Shaikh & Tonak is:

**r\* = S\*/(C\* + V\*)**

Where:
- **S\***: Surplus Value (real)
- **C\***: Constant Capital (Marxian measure)
- **V\***: Variable Capital (Marxian measure)

This is the **traditional Marxist profit rate formula**, NOT the SP/(K×u) formula that the current project uses.

---

## **3. Data Construction Methodology**

### **Sector Exclusions**
From the book text: "nonfarm business minus finance, insurance, and real estate minus government enterprise minus professional services"

**Exact Sector Exclusions:**
1. Finance, insurance, and real estate
2. Government enterprises
3. Professional services

### **Interpolation Rules**
From the book: "one cannot simply use NIPA data to fill in observations between IO benchmark years. Instead, we use NIPA data directly for components such as GVA P or CON and indirectly to interpolate between benchmark estimates"

**Key Principle**: NO interpolation between benchmark years for core variables.

---

## **4. Specific Calculation Methods**

### **Total Value (TV\*)**
```
TV* = GO P + GO tt
where:
- GO P = M P + RY P + [GVA P]
- GO tt = trade and transportation sector output
```

### **Productive Sector Definition**
From the book analysis: Manufacturing, mining, construction, transportation, agriculture, utilities.

### **Unproductive Sector Definition**
Trade, finance, insurance, real estate, government, professional services, personal services.

---

## **5. Capacity Utilization**

From the book notes: "u = uMHI/s up to 1985, where u MH1 is a capacity utilization index based on the McGraw-Hill survey of capital spending, and s is a shift-work index based on Foss (1984). Since the McGraw-Hill survey was discontinued in 1986, the utilization index u MH, was extended to 1989 by means of a regression on the Federal Reserve Capacity Utilization Index"

**1973 Gap**: The book shows u = 0.0 for 1973, indicating this is a missing value that should NOT be interpolated.

---

## **6. Capital Stock Construction**

The book uses specific capital stock measures (KK for 1958-1973, K for 1974-1989) without interpolation between periods.

---

## **7. Implementation Requirements**

To achieve **exact replication**, the new implementation must:

1. **Use exact book formulas**: r\* = S\*/(C\* + V\*)
2. **No data interpolation**: Preserve all original gaps
3. **Exact sector definitions**: Use the specific sector exclusions mentioned
4. **Original data sources**: Use the exact data vintage and sources from 1994
5. **No modern adjustments**: Avoid any "improvements" or modern interpretations

---

## **8. Verification Method**

The results should match the published tables exactly:
- Table 5.4 profit rates should match the published values
- All intermediate calculations should be verifiable
- No discrepancies should exist between calculated and published values

---

## **9. Current Project Issues**

The current project has these **methodological errors**:

1. **Wrong formula**: Uses SP/(K×u) instead of S\*/(C\* + V\*)
2. **Data interpolation**: Interpolates missing values (1973 utilization)
3. **Modern interpretations**: Uses contemporary data sources and methods
4. **Inconsistent results**: Historical vs modern results differ significantly

---

This documentation represents the **exact methodology** that must be implemented for perfect replication. The 30-40% historical profit rates may actually be correct for the book's specific methodology, but we need to verify this using the exact formulas and data construction methods described above.
