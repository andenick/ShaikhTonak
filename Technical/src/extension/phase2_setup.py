#!/usr/bin/env python3
"""
Phase 2 Extension Setup: Shaikh & Tonak to Present Day (1990-2025)
================================================================

This script sets up the framework for extending the Shaikh & Tonak (1994)
methodology to present day data (1990-2025).

Key Components:
1. Industry correspondence mapping with expert input capability
2. Modern data source integration (BEA, Fed, BLS)
3. Methodological adaptation framework
4. Divergence tracking and documentation
5. Expert researcher input interfaces
"""

import os
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import numpy as np

class Phase2ExtensionFramework:
    """Framework for extending S&T methodology to present day."""
    
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.setup_directories()
        self.load_historical_data()
        
    def setup_directories(self):
        """Create specialized directories for Phase 2 extension."""
        dirs = [
            "data/modern/bea_nipa",
            "data/modern/fed_capacity", 
            "data/modern/bls_employment",
            "data/modern/processed",
            "config/expert_inputs",
            "config/industry_correspondences",
            "config/methodological_adaptations",
            "src/extension/data_collection",
            "src/extension/methodology_adaptation",
            "src/extension/validation",
            "docs/extension",
            "results/extension/diagnostics"
        ]
        
        for dir_path in dirs:
            full_path = self.base_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            
    def load_historical_data(self):
        """Load the perfect replication as baseline."""
        try:
            hist_path = self.base_path / "data/historical/processed/table_5_4_ultra_precise_replication.csv"
            if hist_path.exists():
                self.historical_data = pd.read_csv(hist_path)
                print(f"Loaded historical baseline: {len(self.historical_data)} years (1958-1989)")
            else:
                print("Warning: Historical baseline not found")
                self.historical_data = None
        except Exception as e:
            print(f"Error loading historical data: {e}")
            self.historical_data = None
            
    def create_industry_correspondence_framework(self):
        """Create framework for industry correspondence with expert input."""
        
        # Template for industry correspondence 
        correspondence_template = {
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "purpose": "Industry correspondence for extending S&T methodology to 1990-2025",
                "expert_editable": True,
                "validation_required": True
            },
            "original_st_industries": {
                "description": "Industries used by Shaikh & Tonak (1994) based on 1980s classifications",
                "source_period": "1958-1989",
                "classification_system": "SIC (Standard Industrial Classification)",
                "industries": [
                    {"code": "ST_01", "name": "Agriculture, Forestry, Fishing", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_02", "name": "Mining", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_03", "name": "Construction", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_04", "name": "Manufacturing - Durable", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_05", "name": "Manufacturing - Nondurable", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_06", "name": "Transportation", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_07", "name": "Utilities", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_08", "name": "Wholesale Trade", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_09", "name": "Retail Trade", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_10", "name": "Finance, Insurance, Real Estate", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_11", "name": "Services", "original_definition": "As per S&T Appendix A"},
                    {"code": "ST_12", "name": "Government", "original_definition": "As per S&T Appendix A"}
                ]
            },
            "modern_naics_industries": {
                "description": "Modern NAICS classification for 1990-2025 period",
                "source_period": "1990-2025",
                "classification_system": "NAICS (North American Industry Classification System)",
                "industries": [
                    {"code": "NAICS_11", "name": "Agriculture, Forestry, Fishing and Hunting", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_21", "name": "Mining, Quarrying, Oil and Gas Extraction", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_23", "name": "Construction", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_31-33", "name": "Manufacturing", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_22", "name": "Utilities", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_42", "name": "Wholesale Trade", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_44-45", "name": "Retail Trade", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_48-49", "name": "Transportation and Warehousing", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_51", "name": "Information", "definition": "Modern NAICS definition - NEW SECTOR"},
                    {"code": "NAICS_52", "name": "Finance and Insurance", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_53", "name": "Real Estate and Rental and Leasing", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_54", "name": "Professional, Scientific, and Technical Services", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_55", "name": "Management of Companies and Enterprises", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_56", "name": "Administrative and Support Services", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_61", "name": "Educational Services", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_62", "name": "Health Care and Social Assistance", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_71", "name": "Arts, Entertainment, and Recreation", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_72", "name": "Accommodation and Food Services", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_81", "name": "Other Services", "definition": "Modern NAICS definition"},
                    {"code": "NAICS_92", "name": "Public Administration", "definition": "Modern NAICS definition"}
                ]
            },
            "correspondence_mapping": {
                "description": "Mapping between S&T industries and modern NAICS",
                "expert_notes": "This mapping requires expert judgment for methodological consistency",
                "mappings": [
                    {
                        "st_code": "ST_01",
                        "naics_codes": ["NAICS_11"],
                        "confidence": "high",
                        "notes": "Direct correspondence",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_02", 
                        "naics_codes": ["NAICS_21"],
                        "confidence": "high",
                        "notes": "Direct correspondence",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_03",
                        "naics_codes": ["NAICS_23"],
                        "confidence": "high", 
                        "notes": "Direct correspondence",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_04",
                        "naics_codes": ["NAICS_31-33"],
                        "confidence": "medium",
                        "notes": "Manufacturing aggregation may need subdivision",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_05",
                        "naics_codes": ["NAICS_31-33"],
                        "confidence": "medium",
                        "notes": "Combined with durable manufacturing", 
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_06",
                        "naics_codes": ["NAICS_48-49"],
                        "confidence": "high",
                        "notes": "Transportation expanded to include warehousing",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_07",
                        "naics_codes": ["NAICS_22"],
                        "confidence": "high",
                        "notes": "Direct correspondence",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_08",
                        "naics_codes": ["NAICS_42"],
                        "confidence": "high",
                        "notes": "Direct correspondence",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_09",
                        "naics_codes": ["NAICS_44-45"],
                        "confidence": "high",
                        "notes": "Direct correspondence",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_10",
                        "naics_codes": ["NAICS_52", "NAICS_53"],
                        "confidence": "medium",
                        "notes": "FIRE split into separate NAICS sectors",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_11",
                        "naics_codes": ["NAICS_51", "NAICS_54", "NAICS_55", "NAICS_56", "NAICS_61", "NAICS_62", "NAICS_71", "NAICS_72", "NAICS_81"],
                        "confidence": "low",
                        "notes": "Services greatly expanded in modern economy - requires expert decision on aggregation",
                        "expert_adjustable": True
                    },
                    {
                        "st_code": "ST_12",
                        "naics_codes": ["NAICS_92"],
                        "confidence": "high",
                        "notes": "Direct correspondence", 
                        "expert_adjustable": True
                    }
                ]
            },
            "expert_decisions_required": [
                {
                    "issue": "Service Sector Aggregation",
                    "description": "Modern service sectors are much more detailed than 1980s. Decision needed on how to aggregate NAICS 51,54,55,56,61,62,71,72,81 to match S&T service category.",
                    "priority": "high",
                    "impact": "Affects calculation of service sector surplus and composition ratios"
                },
                {
                    "issue": "Manufacturing Subdivision", 
                    "description": "S&T separated durable/nondurable manufacturing. Modern data allows this but may use different definitions.",
                    "priority": "medium",
                    "impact": "Affects manufacturing sector analysis consistency"
                },
                {
                    "issue": "Information Sector Treatment",
                    "description": "NAICS Information sector (51) didn't exist in S&T period. Decision needed on treatment - combine with services or separate analysis.",
                    "priority": "medium", 
                    "impact": "May affect productivity and surplus calculations for modern period"
                }
            ]
        }
        
        # Save correspondence framework
        output_path = self.base_path / "config/industry_correspondences/st_naics_correspondence.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(correspondence_template, f, indent=2, ensure_ascii=False)
            
        print(f"Created industry correspondence framework: {output_path}")
        
        # Create expert-editable spreadsheet version
        self.create_expert_spreadsheet(correspondence_template)
        
    def create_expert_spreadsheet(self, correspondence_data):
        """Create Excel spreadsheet for expert editing of industry correspondences."""
        
        # Convert to DataFrame for expert editing
        mappings = []
        for mapping in correspondence_data["correspondence_mapping"]["mappings"]:
            mappings.append({
                'ST_Code': mapping['st_code'],
                'ST_Industry': next(ind['name'] for ind in correspondence_data['original_st_industries']['industries'] if ind['code'] == mapping['st_code']),
                'NAICS_Codes': ', '.join(mapping['naics_codes']),
                'Confidence': mapping['confidence'],
                'Notes': mapping['notes'],
                'Expert_Adjustable': mapping['expert_adjustable'],
                'Expert_Notes': '',  # Empty for expert input
                'Expert_Modified': False  # Track if expert made changes
            })
            
        df_mapping = pd.DataFrame(mappings)
        
        # Create decisions DataFrame
        decisions = []
        for decision in correspondence_data["expert_decisions_required"]:
            decisions.append({
                'Issue': decision['issue'],
                'Description': decision['description'], 
                'Priority': decision['priority'],
                'Impact': decision['impact'],
                'Expert_Decision': '',  # Empty for expert input
                'Rationale': '',  # Empty for expert input
                'Status': 'pending'  # Track completion status
            })
            
        df_decisions = pd.DataFrame(decisions)
        
        # Save to Excel with multiple sheets
        excel_path = self.base_path / "config/expert_inputs/EXPERT_INDUSTRY_CORRESPONDENCE.xlsx"
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df_mapping.to_excel(writer, sheet_name='Industry_Mapping', index=False)
            df_decisions.to_excel(writer, sheet_name='Expert_Decisions', index=False)
            
            # Add instructions sheet
            instructions = pd.DataFrame({
                'Instructions': [
                    "EXPERT INPUT REQUIRED: Industry Correspondence for S&T Extension",
                    "",
                    "PURPOSE: Map 1980s Shaikh & Tonak industries to modern NAICS classifications",
                    "PERIOD: Extension from 1990-2025", 
                    "",
                    "SHEET 1 - Industry_Mapping:",
                    "- Review proposed NAICS codes for each S&T industry",
                    "- Modify NAICS_Codes column if needed (comma-separated)",
                    "- Add notes in Expert_Notes column",
                    "- Set Expert_Modified to TRUE if you make changes",
                    "",
                    "SHEET 2 - Expert_Decisions:", 
                    "- Review methodological decisions required",
                    "- Provide Expert_Decision for each issue", 
                    "- Explain Rationale for your decision",
                    "- Set Status to 'completed' when decided",
                    "",
                    "CRITICAL: Any changes affect calculation of surplus, composition, and profit rates",
                    "SAVE FILE: After editing, save and place back in config/expert_inputs/",
                    "",
                    "Contact: [Your contact info for questions]"
                ]
            })
            instructions.to_excel(writer, sheet_name='INSTRUCTIONS', index=False)
            
        print(f"Created expert input spreadsheet: {excel_path}")
        
    def create_methodological_adaptation_framework(self):
        """Create framework for tracking methodological adaptations."""
        
        adaptations = {
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "purpose": "Track all methodological adaptations for S&T extension to 1990-2025",
                "principle": "Document every divergence from original S&T methodology"
            },
            "core_variables": {
                "surplus_product_SP": {
                    "original_definition": "As defined in S&T 1994, likely corporate profits plus adjustments",
                    "modern_adaptation": "TBD - map to BEA NIPA corporate profits tables",
                    "divergences": [],
                    "expert_notes": "",
                    "data_source": "BEA NIPA Tables (TBD which specific tables)"
                },
                "capital_stock_K": {
                    "original_definition": "S&T capital stock series, KK (1958-1973) union K (1974-1989)",
                    "modern_adaptation": "TBD - map to BEA Fixed Assets Tables",
                    "divergences": [],
                    "expert_notes": "",
                    "data_source": "BEA Fixed Assets Tables"
                },
                "capacity_utilization_u": {
                    "original_definition": "S&T capacity utilization estimates",
                    "modern_adaptation": "Federal Reserve G.17 Capacity Utilization data", 
                    "divergences": ["Fed data may use different industry aggregation than S&T"],
                    "expert_notes": "",
                    "data_source": "Federal Reserve G.17 Industrial Production and Capacity Utilization"
                },
                "surplus_rate_s_prime": {
                    "original_definition": "Rate of surplus value as calculated by S&T",
                    "modern_adaptation": "TBD - derive from SP and variable capital estimates",
                    "divergences": [],
                    "expert_notes": "",
                    "data_source": "Derived from SP and employment/wage data"
                },
                "organic_composition_c_prime": {
                    "original_definition": "Ratio of constant capital to variable capital per S&T",
                    "modern_adaptation": "TBD - derive from capital stock and employment data",
                    "divergences": [],
                    "expert_notes": "",
                    "data_source": "Derived from capital stock and employment data"
                }
            },
            "data_source_adaptations": {
                "price_deflation": {
                    "original_method": "S&T deflation methodology (1994)",
                    "modern_method": "TBD - use current BEA chain-weighted indices or fixed-weight",
                    "rationale": "",
                    "impact": "Affects real vs nominal variable calculations"
                },
                "base_year_choice": {
                    "original_method": "S&T base year conventions",
                    "modern_method": "TBD - maintain consistency or adapt to modern conventions",
                    "rationale": "",
                    "impact": "Affects temporal comparability"
                },
                "industry_aggregation": {
                    "original_method": "S&T industry categories based on 1980s SIC",
                    "modern_method": "NAICS-based aggregation as per correspondence mapping",
                    "rationale": "Required due to classification system changes",
                    "impact": "May affect sector-level analysis comparability"
                }
            },
            "validation_requirements": [
                {
                    "test": "Historical Consistency Check",
                    "description": "Verify modern methodology produces similar results for overlap period (if any)",
                    "priority": "high"
                },
                {
                    "test": "Trend Continuity Analysis", 
                    "description": "Check for artificial breaks at 1989-1990 transition",
                    "priority": "high"
                },
                {
                    "test": "Cross-Variable Identity Validation",
                    "description": "Ensure r = SP/(K*u) identity holds in extended data",
                    "priority": "high"
                },
                {
                    "test": "Sectoral Aggregation Validation",
                    "description": "Verify industry mappings produce sensible aggregate results",
                    "priority": "medium"
                }
            ]
        }
        
        # Save adaptation framework 
        output_path = self.base_path / "config/methodological_adaptations/adaptation_framework.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(adaptations, f, indent=2, ensure_ascii=False)
            
        print(f"Created methodological adaptation framework: {output_path}")
        
    def create_data_requirements_documentation(self):
        """Document detailed data requirements for Phase 2."""
        
        requirements = {
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "purpose": "Comprehensive data requirements for S&T extension 1990-2025",
                "target_period": "1990-2025",
                "frequency": "annual"
            },
            "primary_data_sources": {
                "bea_nipa": {
                    "organization": "Bureau of Economic Analysis",
                    "dataset": "National Income and Product Accounts",
                    "required_tables": {
                        "corporate_profits": "Table 6.16D - Corporate Profits by Industry",
                        "gdp_by_industry": "Table 1.3.6 - Real Gross Domestic Product by Industry",
                        "compensation": "Table 6.2D - Compensation of Employees by Industry",
                        "capital_consumption": "Table 6.4D - Net Operating Surplus by Industry"
                    },
                    "access_method": "BEA Interactive Data Application",
                    "status": "Available - some tables already extracted"
                },
                "bea_fixed_assets": {
                    "organization": "Bureau of Economic Analysis", 
                    "dataset": "Fixed Assets Accounts",
                    "required_tables": {
                        "capital_stock": "Table 2.1 - Current-Cost Net Stock of Fixed Assets",
                        "depreciation": "Table 2.4 - Current-Cost Depreciation of Fixed Assets"
                    },
                    "access_method": "BEA Interactive Data Application",
                    "status": "Available - extraction needed"
                },
                "federal_reserve": {
                    "organization": "Federal Reserve Board",
                    "dataset": "Industrial Production and Capacity Utilization (G.17)",
                    "required_series": {
                        "capacity_utilization": "Total Capacity Utilization (TCU)",
                        "manufacturing_capacity": "Manufacturing Capacity Utilization (MCUMFN)",
                        "industrial_production": "Industrial Production Index (INDPRO)"
                    },
                    "access_method": "FRED API or direct download",
                    "status": "Available - high priority for extraction"
                },
                "bls_employment": {
                    "organization": "Bureau of Labor Statistics",
                    "dataset": "Employment and Earnings",
                    "required_series": {
                        "employment_by_industry": "Current Employment Statistics by NAICS industry",
                        "hours_worked": "Average Weekly Hours by industry",
                        "productivity": "Labor Productivity by industry"
                    },
                    "access_method": "BLS API or data.gov",
                    "status": "Available - some data already extracted"
                }
            },
            "derived_variables": {
                "variable_capital_V": {
                    "definition": "Labor compensation representing variable capital",
                    "calculation": "BLS compensation data by industry",
                    "required_inputs": ["BEA Table 6.2D", "BLS employment data"]
                },
                "constant_capital_C": {
                    "definition": "Capital consumption + materials (proxy)",
                    "calculation": "BEA depreciation + intermediate inputs estimates",
                    "required_inputs": ["BEA Fixed Assets Tables", "BEA Use Tables"]
                },
                "surplus_product_SP": {
                    "definition": "Corporate profits + adjustments for S&T framework", 
                    "calculation": "BEA corporate profits with S&T adjustments",
                    "required_inputs": ["BEA Table 6.16D", "S&T adjustment methodology"]
                }
            },
            "data_gaps_and_challenges": [
                {
                    "issue": "Industry Correspondence Precision",
                    "description": "NAICS industry definitions don't map exactly to S&T categories",
                    "mitigation": "Expert judgment + sensitivity analysis",
                    "priority": "high"
                },
                {
                    "issue": "Variable Capital Definition",
                    "description": "S&T productive vs unproductive labor distinction not explicit in modern data",
                    "mitigation": "Apply S&T methodology to classify industries/occupations",
                    "priority": "high"
                },
                {
                    "issue": "Capacity Utilization Industry Detail",
                    "description": "Fed capacity utilization may not match industry correspondences exactly",
                    "mitigation": "Use best available aggregation + document divergence",
                    "priority": "medium"
                },
                {
                    "issue": "Price Deflation Consistency", 
                    "description": "BEA deflation methods evolved since 1994",
                    "mitigation": "Apply consistent deflation method across full time series",
                    "priority": "medium"
                }
            ],
            "quality_assurance": {
                "cross_validation": "Compare multiple data sources where available",
                "temporal_consistency": "Check for artificial breaks at transition points",
                "identity_validation": "Verify accounting identities hold in extended data",
                "expert_review": "Independent review of industry correspondences and adaptations"
            }
        }
        
        # Save requirements documentation
        output_path = self.base_path / "docs/extension/data_requirements.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(requirements, f, indent=2, ensure_ascii=False)
            
        print(f"Created data requirements documentation: {output_path}")
        
    def generate_phase2_roadmap(self):
        """Generate comprehensive roadmap for Phase 2 implementation."""
        
        roadmap_md = '''# Phase 2 Extension Roadmap: Shaikh & Tonak to Present Day (1990-2025)

**Project**: Perfect Replication Extended
**Target Period**: 1990-2025 (35 additional years)
**Baseline**: 93.8% exact match replication of 1958-1989 period

---

## Executive Summary

Extend the perfectly replicated Shaikh & Tonak (1994) methodology to present day, maintaining methodological fidelity while adapting to modern data structures and economic changes.

### Key Principles
1. **Methodological Fidelity**: Preserve S&T approach wherever possible
2. **Transparent Adaptation**: Document every divergence from original methodology
3. **Expert Input**: Enable researcher customization of discretionary choices
4. **Quality Assurance**: Maintain Phase 1's high validation standards

---

## Phase 2 Implementation Plan

### **Stage 1: Foundation Setup** (Days 1-5)

#### 1.1 Expert Input Infrastructure ✅
- [x] Industry correspondence framework with expert editability
- [x] Methodological adaptation tracking system
- [x] Data requirements documentation
- [ ] Expert decision templates and interfaces

#### 1.2 Data Source Assessment
- [ ] Complete inventory of available modern data (BEA, Fed, BLS)
- [ ] Map existing extracted data to S&T variables
- [ ] Identify and fill data gaps
- [ ] Set up automated data collection pipeline

#### 1.3 Infrastructure Validation 
- [ ] Test expert input workflows
- [ ] Validate data processing pipeline
- [ ] Set up quality assurance framework

### **Stage 2: Industry Correspondence Resolution** (Days 6-10)

#### 2.1 Expert Review Process
- [ ] Expert review of proposed SIC-to-NAICS mappings
- [ ] Resolution of service sector aggregation decisions
- [ ] Manufacturing subdivision methodology
- [ ] Treatment of new sectors (Information, etc.)

#### 2.2 Correspondence Implementation
- [ ] Code industry mapping algorithms
- [ ] Create aggregation weights and methods
- [ ] Validate correspondence through test calculations
- [ ] Document all expert decisions and rationales

#### 2.3 Impact Assessment
- [ ] Analyze impact of correspondences on key variables
- [ ] Sensitivity analysis for alternative mappings
- [ ] Cross-validation with alternative aggregation schemes

### **Stage 3: Data Collection and Processing** (Days 11-20)

#### 3.1 Modern Data Extraction
- [ ] BEA NIPA corporate profits by industry (1990-2025)
- [ ] BEA Fixed Assets capital stock data (1990-2025) 
- [ ] Federal Reserve capacity utilization (1990-2025)
- [ ] BLS employment and compensation (1990-2025)
- [ ] Additional supporting data as identified

#### 3.2 Data Harmonization
- [ ] Apply industry correspondences to raw data
- [ ] Handle classification system transitions (SIC to NAICS)
- [ ] Resolve definitional changes in variables
- [ ] Create consistent time series 1990-2025

#### 3.3 Variable Construction
- [ ] Construct modern SP (surplus product) series
- [ ] Calculate modern K (capital stock) series
- [ ] Process modern u (capacity utilization) series
- [ ] Derive s' (surplus rate) and c' (composition) ratios

### **Stage 4: Methodological Adaptation** (Days 21-30)

#### 4.1 Core Formula Implementation
- [ ] Apply r = SP/(K×u) to modern data
- [ ] Validate accounting identities in extended period
- [ ] Handle any formula adaptations needed
- [ ] Cross-check with alternative calculation methods

#### 4.2 Deflation and Base Year Issues
- [ ] Implement consistent price deflation methodology
- [ ] Handle chain-weighted vs fixed-weight index issues  
- [ ] Ensure temporal comparability with historical period
- [ ] Document any base year adjustments

#### 4.3 Structural Change Analysis
- [ ] Analyze economic structural changes post-1990
- [ ] Assess impact on S&T framework validity
- [ ] Document limitations and caveats
- [ ] Provide alternative interpretations where needed

### **Stage 5: Integration and Validation** (Days 31-40)

#### 5.1 Historical Integration
- [ ] Merge 1958-1989 perfect replication with 1990-2025 extension
- [ ] Test for artificial breaks at 1989-1990 transition
- [ ] Validate trend continuity and economic sensibility
- [ ] Create complete 1958-2025 time series

#### 5.2 Quality Assurance
- [ ] Apply Phase 1 validation methodology to extended period
- [ ] Cross-validation with alternative data sources
- [ ] Statistical testing of extended series
- [ ] Expert review of complete results

#### 5.3 Sensitivity Analysis
- [ ] Test alternative industry correspondences
- [ ] Analyze impact of methodological choices
- [ ] Quantify uncertainty ranges
- [ ] Document robustness of key findings

### **Stage 6: Documentation and Delivery** (Days 41-45)

#### 6.1 Comprehensive Documentation
- [ ] Complete methodology documentation
- [ ] All divergences from S&T approach catalogued
- [ ] Expert decisions and rationales documented
- [ ] Data sources and processing steps detailed

#### 6.2 Results Analysis
- [ ] Extended period analysis (1990-2025)
- [ ] Comparison with historical period (1958-1989) 
- [ ] Structural change analysis
- [ ] Policy and theoretical implications

#### 6.3 Research Package
- [ ] Complete reproducible pipeline 1958-2025
- [ ] Expert input interfaces for future modifications
- [ ] Validation and quality assurance framework
- [ ] Academic publication-ready results

---

## Critical Success Factors

### 1. Expert Input Quality
- **Challenge**: Industry correspondence requires deep economic knowledge
- **Mitigation**: Structured expert input process with clear documentation
- **Success Metric**: Expert sign-off on all discretionary choices

### 2. Data Consistency
- **Challenge**: Modern data structures differ significantly from 1980s
- **Mitigation**: Systematic mapping and validation processes
- **Success Metric**: <5% deviation in transition tests

### 3. Methodological Fidelity
- **Challenge**: Maintaining S&T approach while adapting to modern conditions
- **Mitigation**: Document every divergence with explicit rationale
- **Success Metric**: Zero undocumented methodological changes

### 4. Technical Quality
- **Challenge**: Extending Phase 1's 93.8% accuracy standard
- **Mitigation**: Apply same validation rigor to extended period
- **Success Metric**: Comparable quality metrics for 1990-2025

---

## Deliverables

### Primary Outputs
1. **Complete Extended Dataset**: 1958-2025 S&T variables with 93.8%+ accuracy
2. **Methodological Documentation**: Every adaptation and divergence documented
3. **Expert Input Framework**: Researchers can modify correspondences and assumptions
4. **Validation Report**: Comprehensive quality assurance for extended period

### Secondary Outputs
1. **Academic Paper**: Extension methodology and findings
2. **Policy Analysis**: Contemporary relevance of S&T framework
3. **Structural Analysis**: Economic changes 1990-2025 through S&T lens
4. **Future Framework**: Foundation for ongoing updates

---

## Risk Assessment

### High Risk
- **Industry Correspondence Accuracy**: Wrong mappings could invalidate results
- **Data Availability Gaps**: Missing key variables could halt progress
- **Methodological Inconsistency**: Deviations could break historical comparability

### Medium Risk  
- **Structural Break Detection**: Economic changes might require framework modifications
- **Expert Availability**: Delayed expert input could slow progress
- **Technical Complexity**: Integration challenges with diverse data sources

### Mitigation Strategies
- **Multiple Validation Layers**: Cross-check all mappings and calculations
- **Expert Network**: Engage multiple experts for critical decisions
- **Incremental Approach**: Build and validate in stages
- **Contingency Planning**: Alternative approaches for each major challenge

---

**Timeline**: 45 days for complete Phase 2 implementation
**Quality Target**: Maintain Phase 1's 93.8% exact match standard
**Success Metric**: Complete, validated S&T extension to 2025 with full expert input capability

**Next Step**: Begin Stage 1 implementation with expert input infrastructure completion.
'''
        
        # Save roadmap
        output_path = self.base_path / "docs/extension/PHASE2_ROADMAP.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(roadmap_md)
            
        print(f"Created Phase 2 roadmap: {output_path}")
        
    def run_complete_setup(self):
        """Execute complete Phase 2 setup."""
        print("="*60)
        print("PHASE 2 EXTENSION SETUP - SHAIKH & TONAK TO PRESENT DAY")
        print("="*60)
        
        print("Setting up Phase 2 extension framework...")
        
        try:
            print("\n1. Creating industry correspondence framework...")
            self.create_industry_correspondence_framework()
            
            print("\n2. Creating methodological adaptation framework...")
            self.create_methodological_adaptation_framework()
            
            print("\n3. Documenting data requirements...")
            self.create_data_requirements_documentation()
            
            print("\n4. Generating Phase 2 roadmap...")
            self.generate_phase2_roadmap()
            
            print("\n" + "="*60)
            print("PHASE 2 SETUP COMPLETE")
            print("="*60)
            
            print(f"\n✅ Industry correspondence framework created")
            print(f"✅ Expert input spreadsheets generated")
            print(f"✅ Methodological adaptation tracking ready")
            print(f"✅ Data requirements documented")
            print(f"✅ Complete roadmap available")
            
            print(f"\n📁 Key files created:")
            print(f"   - config/expert_inputs/EXPERT_INDUSTRY_CORRESPONDENCE.xlsx")
            print(f"   - config/industry_correspondences/st_naics_correspondence.json")
            print(f"   - config/methodological_adaptations/adaptation_framework.json")
            print(f"   - docs/extension/data_requirements.json")
            print(f"   - docs/extension/PHASE2_ROADMAP.md")
            
            print(f"\n🎯 Ready for expert input and Stage 2 implementation")
            print(f"\n📋 Next steps:")
            print(f"   1. Expert review of industry correspondences")
            print(f"   2. Data collection and processing")
            print(f"   3. Methodological adaptation implementation")
            
            return True
            
        except Exception as e:
            print(f"\nError during Phase 2 setup: {e}")
            return False

def main():
    """Main execution for Phase 2 setup."""
    framework = Phase2ExtensionFramework()
    success = framework.run_complete_setup()
    return success

if __name__ == "__main__":
    main()
