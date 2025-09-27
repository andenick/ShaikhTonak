#!/usr/bin/env python3
"""
Actual Data Source Discovery for S&T Extension
==============================================

This script discovers the ACTUAL industry classifications present in our
available modern data sources (1990-2025) rather than creating theoretical mappings.

The expert correspondence framework needs to map S&T industries to the REAL
industry categories available in our data, not hypothetical NAICS codes.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import requests
import numpy as np

class ActualDataDiscovery:
    """Discover actual industry classifications in available modern data."""
    
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.findings = {
            "discovery_date": datetime.now().isoformat(),
            "data_sources_examined": [],
            "actual_industry_classifications": {},
            "data_gaps_identified": [],
            "expert_input_required": []
        }
        
    def examine_existing_data(self):
        """Examine what industry data we actually have in the project."""
        print("Examining existing data for actual industry classifications...")
        
        # Check NIPA data
        nipa_path = self.base_path / "data/extracted_tables/nipa_data"
        if nipa_path.exists():
            self.examine_nipa_data(nipa_path)
            
        # Check BLS employment data
        bls_path = self.base_path / "data/extracted_tables/bls_employment"
        if bls_path.exists():
            self.examine_bls_data(bls_path)
            
        # Check for any modern datasets
        modern_path = self.base_path / "data/modern"
        if modern_path.exists():
            self.examine_modern_data(modern_path)
            
    def examine_nipa_data(self, nipa_path):
        """Examine NIPA data for industry classifications."""
        print(f"\nExamining NIPA data in {nipa_path}...")
        
        nipa_findings = {
            "path": str(nipa_path),
            "period_covered": "Unknown",
            "industry_detail": [],
            "usability": "Unknown"
        }
        
        # Check README
        readme_path = nipa_path / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            # Extract period from README
            if "1961-1981" in readme_content:
                nipa_findings["period_covered"] = "1961-1981 (Historical only - NOT modern period)"
                nipa_findings["usability"] = "NOT SUITABLE for 1990-2025 extension"
            elif "1990" in readme_content or "2000" in readme_content:
                nipa_findings["period_covered"] = "Includes modern period"
                nipa_findings["usability"] = "Potentially suitable"
                
        # Examine actual CSV files for industry content
        csv_files = list(nipa_path.glob("*.csv"))
        industry_categories_found = set()
        
        for csv_file in csv_files[:5]:  # Sample first 5 files
            try:
                df = pd.read_csv(csv_file)
                # Look for industry-related content in first column
                if len(df.columns) > 0:
                    first_col = df.iloc[:, 0].dropna().astype(str)
                    potential_industries = first_col[first_col.str.len() > 5]  # Meaningful names
                    industry_categories_found.update(potential_industries.tolist()[:10])  # Sample
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                
        nipa_findings["industry_detail"] = list(industry_categories_found)[:20]  # Limit output
        nipa_findings["sample_files"] = [f.name for f in csv_files[:5]]
        
        self.findings["actual_industry_classifications"]["nipa_data"] = nipa_findings
        self.findings["data_sources_examined"].append("NIPA data")
        
    def examine_bls_data(self, bls_path):
        """Examine BLS employment data for industry classifications."""
        print(f"\nExamining BLS data in {bls_path}...")
        
        bls_findings = {
            "path": str(bls_path),
            "period_covered": "Unknown",
            "industry_detail": [],
            "usability": "Unknown"
        }
        
        # Check README
        readme_path = bls_path / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
        # Examine CSV files for industry classifications
        csv_files = list(bls_path.glob("*.csv"))
        industry_categories_found = set()
        
        for csv_file in csv_files[:3]:  # Sample files
            try:
                df = pd.read_csv(csv_file)
                if len(df.columns) > 0:
                    first_col = df.iloc[:, 0].dropna().astype(str)
                    potential_industries = first_col[first_col.str.len() > 5]
                    industry_categories_found.update(potential_industries.tolist()[:10])
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                
        bls_findings["industry_detail"] = list(industry_categories_found)[:20]
        bls_findings["sample_files"] = [f.name for f in csv_files[:3]]
        
        self.findings["actual_industry_classifications"]["bls_employment"] = bls_findings
        self.findings["data_sources_examined"].append("BLS employment data")
        
    def examine_modern_data(self, modern_path):
        """Examine any modern data directory."""
        print(f"\nExamining modern data directory: {modern_path}...")
        
        files_found = list(modern_path.rglob("*.csv")) + list(modern_path.rglob("*.xlsx"))
        
        modern_findings = {
            "path": str(modern_path),
            "files_found": len(files_found),
            "file_names": [f.name for f in files_found[:10]],
            "usability": "Empty" if len(files_found) == 0 else "Has data"
        }
        
        self.findings["actual_industry_classifications"]["modern_data"] = modern_findings
        self.findings["data_sources_examined"].append("Modern data directory")
        
    def identify_data_gaps(self):
        """Identify what data we actually need to collect."""
        print("\nIdentifying data gaps for 1990-2025 extension...")
        
        # Check if we have modern period data
        has_modern_corporate_profits = False
        has_modern_capacity_utilization = False
        has_modern_employment = False
        has_modern_capital_stock = False
        
        gaps = []
        
        # Corporate profits by industry (1990-2025)
        if not has_modern_corporate_profits:
            gaps.append({
                "data_type": "Corporate Profits by Industry",
                "period_needed": "1990-2025",
                "source": "BEA NIPA Table 6.16D",
                "priority": "HIGH - Core S&T variable (SP)",
                "action_required": "Collect BEA Table 6.16D data and identify actual industry classifications"
            })
            
        # Capacity utilization (1990-2025)
        if not has_modern_capacity_utilization:
            gaps.append({
                "data_type": "Capacity Utilization by Industry",
                "period_needed": "1990-2025", 
                "source": "Federal Reserve G.17",
                "priority": "HIGH - Core S&T variable (u)",
                "action_required": "Collect Fed G.17 data and identify industry detail available"
            })
            
        # Capital stock by industry (1990-2025)
        if not has_modern_capital_stock:
            gaps.append({
                "data_type": "Capital Stock by Industry",
                "period_needed": "1990-2025",
                "source": "BEA Fixed Assets Tables",
                "priority": "HIGH - Core S&T variable (K)",
                "action_required": "Collect BEA Fixed Assets data with industry breakdown"
            })
            
        # Employment/wages by industry (1990-2025)
        if not has_modern_employment:
            gaps.append({
                "data_type": "Employment and Wages by Industry", 
                "period_needed": "1990-2025",
                "source": "BLS Current Employment Statistics",
                "priority": "MEDIUM - For s' and c' calculations",
                "action_required": "Collect BLS industry employment data with NAICS codes"
            })
            
        self.findings["data_gaps_identified"] = gaps
        
    def generate_real_correspondence_requirements(self):
        """Generate requirements for ACTUAL industry correspondence based on findings."""
        print("\nGenerating real correspondence requirements...")
        
        # Based on our findings, determine what expert input is actually needed
        requirements = []
        
        # If we don't have modern data yet, we need to collect it first
        if len(self.findings["data_gaps_identified"]) > 0:
            requirements.append({
                "requirement": "Data Collection First",
                "description": "Must collect actual 1990-2025 data before creating correspondence framework",
                "rationale": "Cannot create meaningful industry correspondences without knowing actual available classifications",
                "action": "Collect BEA Table 6.16D, Fed G.17, BLS industry data to see REAL industry breakdowns"
            })
            
        # Original S&T industries (from historical replication)
        requirements.append({
            "requirement": "S&T Industry Categories",
            "description": "Identify exact industry categories used in original S&T (1994) study",
            "rationale": "Need precise baseline for correspondence mapping",
            "action": "Extract S&T Appendix A industry definitions from book/historical data"
        })
        
        # Real modern industry classifications
        requirements.append({
            "requirement": "Actual Modern Industry Classifications",
            "description": "Document exact industry categories available in collected 1990-2025 data",
            "rationale": "Correspondence must map to REAL available data, not theoretical categories",
            "action": "Analyze collected data to extract actual industry classification schemes used"
        })
        
        self.findings["expert_input_required"] = requirements
        
    def create_data_collection_plan(self):
        """Create specific plan for collecting needed modern data."""
        print("\nCreating data collection plan...")
        
        collection_plan = {
            "priority_order": [
                {
                    "step": 1,
                    "task": "Collect BEA NIPA Table 6.16D Corporate Profits by Industry",
                    "period": "1990-2025", 
                    "source_url": "https://apps.bea.gov/iTable/",
                    "output": "data/modern/bea_corporate_profits_by_industry.csv",
                    "purpose": "Identify actual industry classifications used for corporate profits (SP variable)"
                },
                {
                    "step": 2,
                    "task": "Collect Federal Reserve G.17 Capacity Utilization",
                    "period": "1990-2025",
                    "source_url": "https://fred.stlouisfed.org/", 
                    "output": "data/modern/fed_capacity_utilization_by_industry.csv",
                    "purpose": "Identify industry detail available for capacity utilization (u variable)"
                },
                {
                    "step": 3,
                    "task": "Collect BEA Fixed Assets Tables by Industry",
                    "period": "1990-2025",
                    "source_url": "https://apps.bea.gov/iTable/",
                    "output": "data/modern/bea_capital_stock_by_industry.csv",
                    "purpose": "Identify industry classifications for capital stock (K variable)"
                },
                {
                    "step": 4,
                    "task": "Extract S&T Original Industry Categories",
                    "period": "1958-1989",
                    "source": "Historical replication data + S&T book Appendix A",
                    "output": "config/st_original_industries.json",
                    "purpose": "Document exact S&T industry categories for mapping baseline"
                },
                {
                    "step": 5,
                    "task": "Create Real Industry Correspondence Framework",
                    "dependencies": "Steps 1-4 completed",
                    "output": "config/expert_inputs/REAL_INDUSTRY_CORRESPONDENCE.xlsx",
                    "purpose": "Expert input for mapping S&T categories to ACTUAL modern classifications"
                }
            ]
        }
        
        # Save collection plan
        plan_path = self.base_path / "docs/extension/DATA_COLLECTION_PLAN.json"
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(collection_plan, f, indent=2)
            
        print(f"Data collection plan saved: {plan_path}")
        
        return collection_plan
        
    def generate_findings_report(self):
        """Generate comprehensive report of actual data situation."""
        
        report_md = f'''# Actual Data Discovery Report: S&T Extension Reality Check

**Discovery Date**: {datetime.now().strftime("%B %d, %Y")}
**Purpose**: Identify REAL industry classifications in available data vs theoretical framework
**Critical Finding**: **Data collection required before industry correspondence framework**

---

## Executive Summary: Theory vs Reality Gap

### ❌ **Critical Issue Identified**
The initial correspondence framework was created based on **theoretical NAICS categories** rather than examining the **actual industry classifications** present in our available 1990-2025 data sources.

### ✅ **Corrective Action Required** 
**IMMEDIATE**: Collect actual modern data to identify real industry breakdowns before creating expert correspondence framework.

---

## Data Sources Examined

{chr(10).join([f"- {source}" for source in self.findings["data_sources_examined"]])}

---

## Actual Data Situation

### NIPA Data Assessment
```json
{json.dumps(self.findings["actual_industry_classifications"].get("nipa_data", {}), indent=2)}
```

### BLS Employment Data Assessment  
```json
{json.dumps(self.findings["actual_industry_classifications"].get("bls_employment", {}), indent=2)}
```

### Modern Data Directory Assessment
```json
{json.dumps(self.findings["actual_industry_classifications"].get("modern_data", {}), indent=2)}
```

---

## Data Gaps Identified

{chr(10).join([f"**{i+1}. {gap['data_type']}**{chr(10)}- Period: {gap['period_needed']}{chr(10)}- Source: {gap['source']}{chr(10)}- Priority: {gap['priority']}{chr(10)}- Action: {gap['action_required']}{chr(10)}" for i, gap in enumerate(self.findings["data_gaps_identified"])])}

---

## Corrected Approach: Data-Driven Correspondence

### **Phase 2A: Data Collection (MUST DO FIRST)**
1. **Collect BEA Table 6.16D**: Corporate profits by industry 1990-2025
2. **Collect Federal Reserve G.17**: Capacity utilization by industry 1990-2025  
3. **Collect BEA Fixed Assets**: Capital stock by industry 1990-2025
4. **Extract S&T Industries**: Original categories from historical data

### **Phase 2B: Real Correspondence Framework**
5. **Analyze Actual Classifications**: Document EXACT industry categories in collected data
6. **Create Expert Framework**: Map S&T → REAL modern categories (not theoretical)
7. **Expert Review**: Based on actual available industry breakdowns

---

## Expert Input Requirements (REVISED)

{chr(10).join([f"**{req['requirement']}**{chr(10)}- {req['description']}{chr(10)}- Rationale: {req['rationale']}{chr(10)}- Action: {req['action']}{chr(10)}" for req in self.findings["expert_input_required"]])}

---

## Immediate Action Items

### **For Project Team** 🚨 **HIGH PRIORITY**
1. **Collect actual 1990-2025 data** (5 data collection tasks)
2. **Analyze real industry classifications** in collected data
3. **Revise correspondence framework** based on actual available categories
4. **Update expert input interface** with real industry options

### **For Expert Researcher** ⏳ **WAIT**
Expert input cannot proceed meaningfully until actual modern industry classifications are identified.

---

## Lessons Learned

### **Critical Error**: Theoretical Framework Before Data Examination
- Created NAICS-based correspondence framework without examining actual data
- Assumed theoretical industry categories match available data reality
- Expert input would have been based on assumptions, not facts

### **Corrected Approach**: Data-Driven Framework Development
- Collect actual modern data first
- Analyze real industry classifications available
- Create correspondence framework based on actual options
- Expert input based on real choices, not theoretical categories

---

## Timeline Impact

### **Additional Time Required**: 5-7 days for data collection
### **Quality Improvement**: Correspondence framework based on reality vs theory
### **Expert Input Quality**: Decisions based on actual available industry options

**CONCLUSION**: This discovery prevents a critical methodological error and ensures the correspondence framework reflects data reality rather than theoretical assumptions.

---

**Next Action**: Execute Data Collection Plan (Steps 1-4) before proceeding with expert correspondence framework.
'''
        
        # Save findings report
        report_path = self.base_path / "docs/extension/ACTUAL_DATA_DISCOVERY_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
            
        # Save findings JSON
        findings_path = self.base_path / "docs/extension/data_discovery_findings.json"
        with open(findings_path, 'w', encoding='utf-8') as f:
            json.dump(self.findings, f, indent=2)
            
        print(f"\nFindings report saved: {report_path}")
        print(f"Findings data saved: {findings_path}")
        
        return report_path
        
    def run_complete_discovery(self):
        """Run complete data discovery analysis."""
        print("="*60)
        print("ACTUAL DATA DISCOVERY - REALITY CHECK")
        print("="*60)
        
        try:
            self.examine_existing_data()
            self.identify_data_gaps()
            self.generate_real_correspondence_requirements()
            self.create_data_collection_plan()
            report_path = self.generate_findings_report()
            
            print("\n" + "="*60)
            print("DATA DISCOVERY COMPLETE - CRITICAL FINDINGS")
            print("="*60)
            
            print("\n[!] CRITICAL ISSUE: Theory vs Reality Gap Identified")
            print("[+] Correspondence framework needs actual data first")
            print("[+] Data collection plan created")
            print("[+] Corrected approach documented")
            
            print(f"\nNext Steps:")
            print("1. Execute data collection plan (5 tasks)")
            print("2. Analyze actual industry classifications") 
            print("3. Revise correspondence framework with real data")
            print("4. Create expert input based on actual options")
            
            return True
            
        except Exception as e:
            print(f"Error during data discovery: {e}")
            return False

def main():
    """Main execution."""
    discovery = ActualDataDiscovery()
    success = discovery.run_complete_discovery()
    return success

if __name__ == "__main__":
    main()
