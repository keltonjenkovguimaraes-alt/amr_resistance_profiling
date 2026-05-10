#!/usr/bin/env python3
"""Universal AMR Profiling — Works with any microorganism — Kelton Guimaraes 2026"""

import os, sys, gzip, json, base64
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import date

# ============================================================
# CONFIGURATION — Change these for your organism!
# ============================================================
VCF = "/path/to/variants.vcf.gz"
VEP = "/path/to/annotation.vep.txt"
ORGANISM = "Candida_albicans"  # Use underscore: Escherichia_coli, Klebsiella_pneumoniae
SAMPLE = "YourSample"

# Load AMR database
DB_FILE = "data/databases/amr_database.json"
with open(DB_FILE) as f:
    amr_db = json.load(f)

# ============================================================
# AUTO-DETECT or MANUAL SET organism
# ============================================================
def detect_organism():
    """Simple auto-detection from VEP or config"""
    # Could parse VCF/VEP for species-specific markers
    # For now, use configured organism
    return ORGANISM

organism = detect_organism()

if organism not in amr_db:
    print(f"Available organisms: {', '.join(amr_db.keys())}")
    print(f"Add '{organism}' to data/databases/amr_database.json")
    sys.exit(1)

amr_genes = amr_db[organism]["genes"]
print(f"Organism: {organism}")
print(f"Genes in database: {len(amr_genes)}")
# ============================================================
# SCREEN VEP FOR AMR GENES
# ============================================================
results = {}
for gene, info in amr_genes.items():
    variants = []
    with open(VEP) as f:
        for line in f:
            if line.startswith("##"): continue
            p = line.strip().split("\t")
            if len(p) < 14: continue
            if gene.upper() in p[3].upper():
                cons = p[6]
                impact = "HIGH" if any(x in cons for x in ["stop","frameshift","splice"]) else \
                         "MODERATE" if "missense" in cons else "LOW"
                variants.append({"cons": cons, "impact": impact})
    
    high = sum(1 for v in variants if v["impact"] == "HIGH")
    mod = sum(1 for v in variants if v["impact"] == "MODERATE")
    risk = "RESISTANT" if high > 0 else "POSSIBLE_RESISTANCE" if mod > 0 else "SUSCEPTIBLE"
    
    results[gene] = {
        "drug_class": info["drug_class"],
        "mechanism": info["mechanism"],
        "variants": len(variants),
        "high": high,
        "moderate": mod,
        "risk": risk
    }
# Print results
resistant_any = False
for gene, r in results.items():
    if r["risk"] != "SUSCEPTIBLE":
        resistant_any = True
        print(f"  {gene}: {r['risk']} — {r['drug_class']} ({r['high']} HIGH, {r['moderate']} MODERATE)")
    else:
        print(f"  {gene}: SUSCEPTIBLE")

# Overall assessment
overall = "RESISTANT DETECTED" if resistant_any else "PAN-SUSCEPTIBLE"
print(f"\nOverall: {overall}")

# Generate simple report
drug_classes = set(r["drug_class"] for r in results.values())
for dc in sorted(drug_classes):
    genes_in_class = [g for g, r in results.items() if r["drug_class"] == dc]
    resistant_in_class = [g for g in genes_in_class if results[g]["risk"] != "SUSCEPTIBLE"]
    status = "RESISTANT" if resistant_in_class else "SUSCEPTIBLE"
    print(f"  {dc}: {status}")

print(f"\nRun complete — {len(amr_genes)} genes screened across {len(drug_classes)} drug classes")
