# Contributing to Universal AI Failure Database

Thank you for helping make AI systems safer and more transparent. This document explains everything you need to know to contribute effectively.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [What We Accept](#what-we-accept)
- [What We Do Not Accept](#what-we-do-not-accept)
- [Submission Process](#submission-process)
- [Entry Format](#entry-format)
- [Severity Rating Guide](#severity-rating-guide)
- [Verification Process](#verification-process)
- [Development Setup](#development-setup)
- [Tooling](#tooling)

---

## Code of Conduct

This project follows a simple standard: **be constructive, be honest, be kind**. We are a research community, not a competition. Criticism of AI systems is the point — criticism of contributors is not welcome.

---

## What We Accept

- **Real failure instances** with reproducible prompts and documented responses
- **Verified hallucinations**: Factual claims that are demonstrably false and confidently stated
- **Mathematical errors**: Wrong arithmetic, incorrect proofs, flawed statistical reasoning
- **Logic errors**: Invalid inferences, self-contradictions, category errors
- **Legal errors**: Misstatements of law, fabricated case citations, jurisdictional mistakes
- **Security vulnerabilities**: Successful prompt injections, jailbreaks, safety bypass demonstrations
- **Tooling improvements**: Better validators, query tools, exporters, visualisers
- **Documentation improvements**: Clearer schemas, better guides, translations

---

## What We Do Not Accept

- Entries containing **personally identifiable information (PII)**
- **Active zero-day exploits** without prior responsible disclosure coordination (see SECURITY.md)
- Entries that are **fabricated or not reproducible**
- Content designed to **harm individuals** or specific organisations
- Political or ideological framing that goes beyond documenting objective failures

---

## Submission Process

### Step 1 — Check for Duplicates
Search existing entries before submitting:
```bash
python tools/query.py --search "your failure description"
```

### Step 2 — Create Your Entry
Copy the appropriate template from `docs/templates/` into the correct `data/` subdirectory:

```bash
cp docs/templates/hallucination-template.json data/hallucinations/UAIFD-HAL-XXXX.json
```

### Step 3 — Fill in the Schema
Edit your JSON file following the schema for that category. All fields marked as required must be present and non-empty.

### Step 4 — Validate
```bash
python tools/validate.py data/hallucinations/UAIFD-HAL-XXXX.json
```
Fix any validation errors before proceeding.

### Step 5 — Open a Pull Request
- Branch name: `entry/category-brief-description` (e.g. `entry/hallucination-gpt4-legal-citation`)
- PR title: `[CATEGORY] Brief description of failure`
- Fill in the PR template

---

## Entry Format

See `docs/schemas/` for the full JSON schema for each category. Required fields across all categories:

| Field | Type | Description |
|---|---|---|
| `id` | string | Auto-assigned by maintainers on merge (leave as `"PENDING"`) |
| `category` | enum | One of: `hallucination`, `math-error`, `logic-error`, `legal-error`, `vulnerability` |
| `subcategory` | string | Specific failure type within the category |
| `severity` | enum | `critical`, `high`, `medium`, `low` |
| `model.name` | string | Model name (e.g. `"GPT-4"`) |
| `model.provider` | string | Provider name |
| `model.api_date` | string | ISO 8601 date of the interaction |
| `prompt` | string | The exact prompt that triggered the failure |
| `response` | string | The exact model response (or relevant excerpt) |
| `failure_analysis.type` | string | Classification of the failure mechanism |
| `failure_analysis.description` | string | Substantive explanation of why this is a failure |
| `failure_analysis.verified_by` | string | How the failure was confirmed |
| `tags` | array | Relevant search tags |
| `submitted_by` | string | GitHub username or `"anonymous"` |
| `submission_date` | string | ISO 8601 date |
| `verified` | boolean | Set to `false` on initial submission |
| `license` | string | Always `"CC0-1.0"` |

---

## Severity Rating Guide

| Level | Criteria | Examples |
|---|---|---|
| **Critical** | Could cause direct harm, legal liability, or medical/safety consequences | Fabricated drug dosage, false emergency instructions, working jailbreak enabling CSAM |
| **High** | Significant factual error with real-world impact potential | Fabricated legal precedent used in a case, wrong financial calculation, major historical distortion |
| **Medium** | Meaningful error but limited direct harm potential | Incorrect scientific claim, reasoning error in low-stakes context, partial safety bypass |
| **Low** | Minor inaccuracy, stylistic failure, or trivially wrong claim | Wrong minor date, slightly incorrect statistic, confusion of similar terms |

---

## Verification Process

All submitted entries go through a two-stage review:

1. **Schema validation** (automated) — CI checks run on every PR
2. **Content verification** (human) — A maintainer or community verifier independently attempts to reproduce or confirm the failure

Entries are merged with `"verified": false` and updated to `"verified": true` once independent confirmation is received. This separation ensures transparency about the verification status of each entry.

To become a community verifier, open a Discussion with the label `verifier-application`.

---

## Development Setup

```bash
git clone https://github.com/yourusername/universal-ai-failure-database.git
cd universal-ai-failure-database

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 tools/ scripts/
```

---

## Tooling

| Tool | Purpose |
|---|---|
| `tools/validate.py` | Validate a single entry against its schema |
| `tools/validate_all.py` | Validate all entries in the database |
| `tools/query.py` | Search and filter the database |
| `tools/export.py` | Export to CSV, JSONL, Parquet, or HuggingFace format |
| `tools/stats.py` | Generate database statistics |
| `scripts/assign_ids.py` | Assign IDs to pending entries (maintainer only) |

---

*Questions? Open a [GitHub Discussion](https://github.com/yourusername/universal-ai-failure-database/discussions).*
