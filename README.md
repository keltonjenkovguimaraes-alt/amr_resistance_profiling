# 🍄 Fungal Antimicrobial Resistance Profiling

A comprehensive AMR gene screening pipeline for pathogenic fungi. Screens variant calls against curated resistance gene databases to predict antifungal susceptibility.

## Supported Fungi

| Species | Genes Screened | Drug Classes |
|---------|---------------|-------------|
| **Candida albicans** | 73 | Azoles, Echinocandins, Polyenes, Flucytosine |
| **Candida auris** | Coming soon | Multidrug resistance |
| **Aspergillus fumigatus** | Coming soon | Azoles |
| **Cryptococcus neoformans** | Coming soon | Azoles, Polyenes |

## How It Works

VCF + VEP annotations
↓
Load species-specific AMR gene database (JSON)
↓
Screen all variants against 73 resistance genes
↓
Classify: HIGH impact = RESISTANT, MODERATE = POSSIBLE
↓
Generate clinical report with drug recommendations

## Gene Categories Screened

| Category | Genes | What It Detects |
|----------|-------|-----------------|
| **Ergosterol Pathway** | 20 | Azole target mutations, bypass mechanisms |
| **Efflux Pumps** | 19 | ABC & MFS transporter-mediated resistance |
| **Regulators** | 6 | Overexpression of efflux genes |
| **Echinocandin Targets** | 8 | FKS1 hotspot mutations |
| **Cell Wall Compensation** | 12 | Chitin synthase upregulation |
| **Drug Tolerance** | 15 | HSP90, calcineurin, stress pathways |
| **Flucytosine** | 3 | Prodrug activation defects |

## Quick Start

```bash
git clone https://github.com/keltonjenkovguimaraes-alt/amr_resistance_profiling.git
cd amr_resistance_profiling

# Edit VCF and VEP paths in workflow/scripts/run_amr_analysis.py
# Choose your organism in config

python workflow/scripts/run_amr_analysis.py
Adding a New Fungus
Add entries to data/databases/amr_database.json:
{
  "Aspergillus_fumigatus": {
    "genes": {
      "cyp51A": {"drug_class": "Azoles", "mechanism": "Drug target (14α-demethylase)"},
      "cyp51B": {"drug_class": "Azoles", "mechanism": "Alternative demethylase"},
      "atrF": {"drug_class": "Azoles", "mechanism": "ABC efflux transporter"}
    }
  }
}
Results — C. albicans SRR7801919
Metric	Value
Genes screened	73
Drug classes	6
HIGH impact mutations	0
Result	PAN-SUSCEPTIBLE
Author
Kelton Guimaraes — Implementation & Analysis

Sources
CGD: Candida Genome Database (candidagenome.org)

KEGG: Sterol biosynthesis pathway

CARD: Comprehensive Antibiotic Resistance Database

Published AMR literature (PMID: 23133674, 19181814, 17158934)
