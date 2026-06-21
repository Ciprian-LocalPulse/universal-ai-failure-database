# Logic Error Entry Schema

## Category Value
```
"category": "logic-error"
```

## Subcategory Values

| Subcategory | Description |
|---|---|
| `affirming_the_consequent` | Fallacy: (P→Q), Q, therefore P |
| `denying_the_antecedent` | Fallacy: (P→Q), ¬P, therefore ¬Q |
| `false_dichotomy` | Presenting a false either/or choice |
| `circular_reasoning` | Conclusion used as a premise |
| `ad_hoc_reasoning` | Invented special pleading to save a claim |
| `invalid_generalisation` | Wrong induction from limited examples |
| `hasty_generalisation` | Overgeneralising from insufficient data |
| `self_contradiction` | Model contradicts itself within one response |
| `category_error` | Applying properties of one type to an incompatible type |
| `modus_ponens_failure` | Failing to correctly apply valid modus ponens |
| `invalid_deduction` | Non-sequitur conclusion from given premises |
| `scope_confusion` | Confusing quantifier scopes (all/some/none) |

## Severity Guidelines

| Severity | Criteria |
|---|---|
| `critical` | Used in medical, legal, or safety-critical reasoning system |
| `high` | Significant reasoning chain built on the invalid inference |
| `medium` | Isolated logic error in a consequential context |
| `low` | Trivially detectable logical slip |
