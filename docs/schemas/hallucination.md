# Hallucination Entry Schema

## Category Value
```
"category": "hallucination"
```

## Subcategory Values

| Subcategory | Description |
|---|---|
| `fabricated_citation` | Invented academic paper, article, or legal case |
| `false_biographical_claim` | Wrong facts about a real person |
| `false_medical_claim` | Wrong medical facts, dosages, or diagnoses |
| `false_historical_claim` | Wrong historical dates, events, or attributions |
| `false_statistical_claim` | Invented or wrong statistics presented as fact |
| `false_scientific_claim` | Wrong scientific facts or fabricated findings |
| `confabulation` | Plausible-sounding but entirely made-up narrative |
| `entity_confusion` | Mixing up two distinct real-world entities |
| `temporal_hallucination` | Wrong dates, timelines, or recency claims |
| `geographic_hallucination` | Wrong location, address, or geographic facts |

## Required Fields (hallucination-specific)

All standard fields plus:
- `failure_analysis.reference_check`: URL to authoritative source disconfirming the claim, or `null` if not available

## Severity Guidelines for Hallucinations

| Severity | Criteria |
|---|---|
| `critical` | Wrong medical/drug information, legal citations used in filings, safety-critical instructions |
| `high` | Academic citations, significant biographical errors, financial misinformation |
| `medium` | Historical inaccuracies, wrong statistics in low-stakes contexts |
| `low` | Minor factual errors, trivially verifiable wrong claims |
