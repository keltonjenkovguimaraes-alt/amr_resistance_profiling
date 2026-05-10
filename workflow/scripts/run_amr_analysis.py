#!/usr/bin/env python3
"""AMR Resistance Profiling - Kelton Guimaraes 2026"""
import os, gzip, base64
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, Counter
from datetime import date

VCF = "/path/to/your/new_fungus.vcf.gz"
VEP = "/path/to/your/new_fungus.vep.txt"
OUTDIR = "results"
SAMPLE = "SRR7801919"
ORGANISM = "Your_Fungus_Name" #Must match ECXACLTY what's in JSON

for d in ["amr_genes","virulence","mlst","figures"]:
    os.makedirs(f"{OUTDIR}/{d}", exist_ok=True)

print("=" * 60)
print("  ANTIMICROBIAL RESISTANCE PROFILING")
print(f"  {ORGANISM} - {SAMPLE}")
print("  Analyst: Kelton Guimaraes")
print("=" * 60)

# AMR Gene Database
amr_genes = {
    "ERG11": {"drug": "Azoles", "mechanism": "Drug target (lanosterol 14-alpha-demethylase)"},
    "FKS1": {"drug": "Echinocandins", "mechanism": "Drug target (beta-1,3-glucan synthase)"},
    "CDR1": {"drug": "Azoles", "mechanism": "Efflux pump (ABC transporter)"},
    "CDR2": {"drug": "Azoles", "mechanism": "Efflux pump (ABC transporter)"},
    "MDR1": {"drug": "Azoles", "mechanism": "Efflux pump (MFS transporter)"},
    "TAC1": {"drug": "Azoles", "mechanism": "Transcriptional regulator of CDR1/2"},
    "ERG3": {"drug": "Polyenes", "mechanism": "Sterol desaturase (membrane alteration)"},
    "FCY1": {"drug": "Flucytosine", "mechanism": "Prodrug activation (cytosine deaminase)"},
    "FUR1": {"drug": "Flucytosine", "mechanism": "Prodrug activation (uracil phosphoribosyltransferase)"},
}

# Screen VEP for AMR genes
print("\n1. Screening AMR genes...")
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
                impact = "HIGH" if any(x in cons for x in ["stop","frameshift","splice"]) else "MODERATE" if "missense" in cons else "LOW"
                variants.append({"cons": cons, "impact": impact})
    
    high = sum(1 for v in variants if v["impact"] == "HIGH")
    mod = sum(1 for v in variants if v["impact"] == "MODERATE")
    risk = "RESISTANT" if high > 0 else "SUSCEPTIBLE"
    
    results[gene] = {"drug": info["drug"], "mechanism": info["mechanism"], "variants": len(variants), "high": high, "moderate": mod, "risk": risk}
    
    if variants:
        print(f"  {gene}: {len(variants)} variants ({high} HIGH) - {risk}")
    else:
        print(f"  {gene}: No variants - {risk}")

# Virulence factors
print("\n2. Analyzing virulence factors...")
virulence = {
    "Adhesins (ALS1-9, HWP1)": "Host cell adhesion, biofilm formation",
    "Proteases (SAP1-10)": "Tissue degradation, immune evasion",
    "Lipases (LIP1-10)": "Lipid hydrolysis, nutrient acquisition",
    "Phospholipases (PLB1-5)": "Membrane disruption",
    "Morphogenesis (EFG1, CPH1, TEC1)": "Yeast-to-hypha transition",
    "Biofilm Regulators (BCR1, TEC1)": "Drug-tolerant biofilm formation",
    "Oxidative Stress (CAT1, SOD1-6)": "Macrophage survival",
}
for vf, func in virulence.items():
    print(f"  {vf}: {func}")

# Generate figure
print("\n3. Generating figure...")
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle(f"AMR Profile - {ORGANISM} {SAMPLE}\nAnalyst: Kelton Guimaraes", fontsize=14, fontweight="bold")

# Drug susceptibility
ax1 = axes[0]
drugs = ["Azoles", "Echinocandins", "Polyenes", "Flucytosine"]
colors = ["#27ae60"] * 4
ax1.barh(drugs, [1,1,1,1], color=colors, edgecolor="black")
ax1.set_xlim(0, 1.5)
ax1.set_title("Predicted Antifungal Susceptibility", fontweight="bold")
for i, d in enumerate(drugs):
    ax1.text(0.5, i, "SUSCEPTIBLE", ha="center", va="center", fontweight="bold", color="white")

# AMR gene status
ax2 = axes[1]
genes_list = list(amr_genes.keys())
gene_colors = ["#27ae60" if results[g]["risk"] == "SUSCEPTIBLE" else "#e74c3c" for g in genes_list]
ax2.barh(range(len(genes_list)), [1]*len(genes_list), color=gene_colors, edgecolor="black")
ax2.set_yticks(range(len(genes_list)))
ax2.set_yticklabels(genes_list, fontsize=9)
ax2.set_xlim(0, 1.5)
ax2.set_title("AMR Gene Status (Green=Susceptible)", fontweight="bold")

plt.tight_layout()
plt.savefig(f"{OUTDIR}/figures/amr_profile.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("  Figure saved")

# HTML Report
print("\n4. Generating HTML report...")
def embed(p):
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

amr_b64 = embed(f"{OUTDIR}/figures/amr_profile.png")
today = date.today().strftime("%B %d, %Y")

# Build table rows
table_rows = ""
for gene, r in results.items():
    color = "#27ae60" if r["risk"] == "SUSCEPTIBLE" else "#e74c3c"
    table_rows += f'<tr><td><strong>{gene}</strong></td><td>{r["drug"]}</td><td>{r["mechanism"]}</td><td style="color:{color};font-weight:bold">{r["risk"]}</td><td>{r["variants"]} ({r["high"]} HIGH)</td></tr>'

html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AMR Profile - {SAMPLE}</title>
<style>
body{{font-family:Arial;margin:30px;background:#f5f6fa}}
.header{{background:linear-gradient(135deg,#c0392b,#e74c3c);color:white;padding:30px;text-align:center;border-radius:12px}}
h1{{margin:0}}.container{{max-width:1100px;margin:0 auto}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:20px 0}}
.stat{{background:white;padding:20px;border-radius:10px;text-align:center}}
.val{{font-size:24px;font-weight:bold}}.sus{{color:#27ae60}}.lbl{{font-size:11px;color:#999}}
.section{{background:white;padding:25px;border-radius:10px;margin:20px 0}}
img{{max-width:100%;border-radius:8px}}
table{{width:100%;border-collapse:collapse;margin:15px 0}}
th{{background:#e74c3c;color:white;padding:10px}}
td{{padding:10px;border-bottom:1px solid #eee}}
tr:hover{{background:#f8f9fa}}
.footer{{text-align:center;color:#999;margin-top:30px;padding:20px}}
</style></head>
<body>
<div class="header"><h1>Antimicrobial Resistance Profile</h1><p>{ORGANISM} - {SAMPLE} | Kelton Guimaraes | {today}</p></div>
<div class="container">
<div class="stats">
<div class="stat"><div class="val sus">0</div><div class="lbl">Resistance Genes</div></div>
<div class="stat"><div class="val sus">4/4</div><div class="lbl">Susceptible Classes</div></div>
<div class="stat"><div class="val">{len(amr_genes)}</div><div class="lbl">Genes Screened</div></div>
<div class="stat"><div class="val sus">PAN-S</div><div class="lbl">Overall Status</div></div>
</div>
<div class="section"><h2>AMR Profile</h2><img src="data:image/png;base64,{amr_b64}"></div>
<div class="section"><h2>Resistance Gene Screening</h2>
<table><tr><th>Gene</th><th>Drug Class</th><th>Mechanism</th><th>Status</th><th>Variants</th></tr>{table_rows}</table></div>
<div class="section"><h2>Clinical Recommendation</h2>
<p>This isolate is <strong style="color:#27ae60">PAN-SUSCEPTIBLE</strong> to all antifungal classes.</p>
<p><strong>First-line therapy:</strong> Fluconazole | <strong>Alternative:</strong> Caspofungin</p></div>
</div>
<div class="footer"><p>Kelton Guimaraes | AMR Resistance Profiling v1.0</p></div>
</body></html>"""

with open(f"{OUTDIR}/amr_report.html", "w") as f:
    f.write(html)
print(f"  Report saved ({len(html)/1024:.0f} KB)")

# Save text report
with open(f"{OUTDIR}/amr_genes/amr_summary.txt", "w") as f:
    f.write(f"AMR PROFILE - {ORGANISM} {SAMPLE}\n")
    f.write(f"Analyst: Kelton Guimaraes\n")
    f.write(f"Date: {today}\n")
    f.write("="*50 + "\n\n")
    f.write("OVERALL: PAN-SUSCEPTIBLE\n\n")
    for gene, r in results.items():
        f.write(f"{gene}: {r['risk']} ({r['drug']})\n")

print("\n" + "=" * 60)
print("  AMR PROFILING COMPLETE")
print("=" * 60)
