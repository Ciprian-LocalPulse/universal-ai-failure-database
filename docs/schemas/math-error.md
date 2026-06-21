# Math Error Entry Schema

## Category Value
```
"category": "math-error"
```

## Subcategory Values

| Subcategory | Description |
|---|---|
| `arithmetic_error` | Basic computation mistake (+, -, ×, ÷) |
| `algebra_error` | Wrong algebraic manipulation or equation solving |
| `probability_error` | Incorrect probability calculation or interpretation |
| `statistics_error` | Wrong statistical computation or interpretation |
| `calculus_error` | Wrong derivative, integral, or limit |
| `geometry_error` | Wrong geometric computation |
| `unit_conversion_error` | Wrong unit conversion or dimensional analysis |
| `order_of_operations_error` | Wrong PEMDAS/BODMAS application |
| `non_deterministic_arithmetic` | Inconsistent results across runs for same computation |
| `floating_point_misrepresentation` | Wrong handling of floating-point precision |

## Severity Guidelines

| Severity | Criteria |
|---|---|
| `critical` | Medical dosage calculation, structural engineering, flight navigation |
| `high` | Financial calculations, scientific research, legal damages computations |
| `medium` | Educational examples, moderate-stakes computations |
| `low` | Trivial arithmetic errors, low-stakes context |
