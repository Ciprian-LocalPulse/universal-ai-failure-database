# Legal Error Entry Schema

## Category Value
```
"category": "legal-error"
```

## Subcategory Values

| Subcategory | Description |
|---|---|
| `fabricated_case_citation` | Invented case name, citation, or holding |
| `misstatement_of_holding` | Real case cited but holding mischaracterised |
| `wrong_jurisdiction` | Law or case from wrong jurisdiction applied |
| `overturned_precedent` | Citing a case that has been overruled |
| `misstatement_of_statute` | Wrong statutory text or wrong statute cited |
| `wrong_standard_of_review` | Incorrect legal standard applied |
| `fabricated_regulation` | Invented regulatory provision |
| `wrong_burden_of_proof` | Wrong party or wrong standard for burden |
| `criminal_civil_confusion` | Applying criminal law concepts to civil context or vice versa |
| `international_law_error` | Wrong characterisation of treaty or international law |

## Additional Required Fields

```json
"jurisdiction": "US-Federal / US-NY / UK / EU / etc.",
"practice_area": "Aviation / Contract / Criminal / etc."
```

## Severity Guidelines

| Severity | Criteria |
|---|---|
| `critical` | Fabricated citation used or likely to be used in an actual filing |
| `high` | Wrong statement of law in a practitioner-facing context |
| `medium` | Legal error in a general research or educational context |
| `low` | Minor jurisdictional confusion or trivially correctable error |
