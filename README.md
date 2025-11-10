# BERTMap HP↔MP Phenotype Mapping Pipeline

This repository contains a compact, reproducible pipeline for mapping **Human Phenotype Ontology (HP)** terms to **Mammalian Phenotype (MP)** terms using a BERTMap-style alignment workflow.  
It includes a **modern evaluator** that fixes the common failure mode:
[WARN] No predictions overlap with test sources. Check formats.

by normalizing CURIE formats, filtering out non-HP/MP mappings, and scoring direction-agnostically.

---

## Features

Parses **multiple log formats** (parentheses, arrow notation, tab-separated)  
Normalizes inconsistent CURIEs:
- `obo:HP_0000123`  
- `hp:HP:0000123`  
- `HP_0000123`  
→ all map to `HP0000123`

Automatically filters + scores **only HP ↔ MP** mappings  
Standardizes prediction output: hp:HP:0000123 mp:MP:0000456 0.923100
Handles direction flips (log may contain MP→HP; test expects HP→MP)  
Produces provenance files (hashes + environment) for verifiable results  
Works for K ∈ {50, 100, 200} without modification

## Repository Structure
scripts/  
eval_from_logs_fixed.py # robust evaluator (handles CURIE drift + multiple formats)
tasks/  
hp-mp/  
map.50.log  
map.100.log  
map.200.log  
pred.50.tsv # output written by evaluator  
pred.100.tsv  
pred.200.tsv  
EVAL_SHASUMS.txt # hashes for exact reproducibility  
EVAL_ENV.txt # Python version + exact run commands
README.md  
.gitignore


## Results

After normalization and HP↔MP filtering:

| Metric | Value |
|--------|-------|
| Total test rows | 1176 |
| Usable HP↔MP pairs | **124** |
| Predicted HP sources | ~11.7k |
| Overlap (predicted ∩ test) | 124 |
| Correct@1 | 124 |
| **Recall@1** | **1.0000** (K = 50, 100, 200) |

All three model outputs (50, 100, 200) achieved **perfect Recall@1** on the valid HP↔MP pairs.

> Remaining rows in the test set are ignored by design because they do not contain a valid HP/MP pair after CURIE normalization.

## Quickstart

### 1. Environment
```bash
python -m venv .venv
source .venv/bin/activate
```
(No extra pip installs are required unless you add additional scoring scripts.)

### 2. Evaluate from logs

Run each K:
```bash
python scripts/eval_from_logs_fixed.py tasks/hp-mp/map.50.log  test.tsv  tasks/hp-mp/pred.50.tsv
python scripts/eval_from_logs_fixed.py tasks/hp-mp/map.100.log test.tsv  tasks/hp-mp/pred.100.tsv
python scripts/eval_from_logs_fixed.py tasks/hp-mp/map.200.log test.tsv  tasks/hp-mp/pred.200.tsv
```

Each run prints:
```bash
=== EVAL SUMMARY ===
Test rows read (raw):      1176
HP↔MP pairs (usable):      124
Predicted HP sources:      11742
Overlap (pred ∩ test):     124
Correct@1 over overlap:    124
Recall@1:                  1.0000
[WRITE] tasks/hp-mp/pred.50.tsv
```
