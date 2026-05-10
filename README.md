# 🍄 Fungal Antimicrobial Resistance Profiling

A comprehensive AMR gene screening pipeline for pathogenic fungi. Screens variant calls against curated, literature-backed resistance gene databases to predict antifungal susceptibility.

---

## Supported Pathogenic Fungi

| Species | Genes | Drug Classes | Clinical Relevance |
|---------|-------|-------------|-------------------|
| **Candida albicans** | 73 | Azoles, Echinocandins, Polyenes, Flucytosine | Most common fungal pathogen |
| **Candida auris** | 27 | Azoles, Echinocandins, Polyenes, Flucytosine | Emerging MDR threat (WHO Critical) |
| **Aspergillus fumigatus** | 35 | Azoles, Echinocandins, Polyenes | Invasive aspergillosis, azole resistance |
| **Cryptococcus neoformans** | 30 | Azoles, Polyenes, Flucytosine | Meningitis in immunocompromised |
| **Pneumocystis jirovecii** | 10 | Azoles, Sulfonamides, Atovaquone | Pneumonia in HIV/AIDS |
| **Trichophyton rubrum** | 15 | Azoles, Allylamines, Echinocandins | Dermatophytosis (skin/nail) |
| **Total** | **200+** | **8 drug classes** | |

---

## How It Works

VCF + VEP annotations
↓
Auto-detect fungal species → load correct database
↓
Screen all variants against resistance gene panel
↓
Classify: HIGH impact = RESISTANT | MODERATE = POSSIBLE | none = SUSCEPTIBLE
↓
Generate clinical report with drug-specific recommendations

---

## Gene Categories Screened

| Category | C. albicans | C. auris | A. fumigatus | C. neoformans | What It Detects |
|----------|-----------|----------|-------------|---------------|-----------------|
| **Ergosterol Pathway** | 20 | 9 | 10 | 17 | Azole target mutations |
| **Efflux Pumps** | 19 | 3 | 8 | 3 | Transporter resistance |
| **Regulators** | 6 | 4 | 3 | 2 | Overexpression mechanisms |
| **Echinocandin Targets** | 8 | 2 | 1 | 1 | FKS hotspot mutations |
| **Cell Wall** | 12 | 2 | 7 | 0 | Compensatory mechanisms |
| **Drug Tolerance** | 15 | 5 | 4 | 4 | Hsp90, calcineurin |
| **Flucytosine** | 3 | 2 | 0 | 2 | Prodrug activation |
| **Allylamines** | 0 | 0 | 0 | 0 | Squalene epoxidase |

---

## Adding a New Fungus

Add entries to `data/databases/amr_database.json`:

```json
{
  "Your_Fungus": {
    "genes": {
      "GENE1": {"drug_class": "Azoles", "mechanism": "Drug target"},
      "GENE2": {"drug_class": "Echinocandins", "mechanism": "Cell wall synthesis"}
    }
  }
}
git clone https://github.com/keltonjenkovguimaraes-alt/amr_resistance_profiling.git
cd amr_resistance_profiling

# Edit paths in workflow/scripts/run_amr_analysis.py
# Set your organism
python workflow/scripts/run_amr_analysis.py
Results — C. albicans SRR7801919
Metric	Value
Genes screened	73
Drug classes	6
HIGH impact mutations	0
Result	PAN-SUSCEPTIBLE
Gene Sources
All genes are verified against:

CGD — Candida Genome Database (candidagenome.org)

KEGG — Sterol biosynthesis pathways

CARD — Comprehensive Antibiotic Resistance Database

Published literature — PMID: 23133674, 19181814, 17158934, 30670423

WHO Fungal Priority Pathogens List (2022)

Author
Kelton Guimaraes — Implementation & Analysis

License
MIT
