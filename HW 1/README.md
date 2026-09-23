# HW 1: SAT Solver via Truth Table

GEMINI LINK : https://share.gemini.google/a89qtYGwhWM4

A Boolean satisfiability (SAT) solver that determines satisfiability by systematically enumerating all `2^n` truth assignments and printing a truth table.

## Files

- `sat.py` — solver implementation
- `test_sat.py` — standalone test suite (no dependencies)

## Usage

```python
from sat import solve_sat_truth_table

assignments = solve_sat_truth_table(
    ["A", "B", "C"],
    "(A or B) and (not A or C) and (not B or not C)",
)
```

Or run the built-in example directly:

```bash
python3 sat.py
```

## API

```python
solve_sat_truth_table(variables, formula_str) -> list[dict[str, bool]]
```

- `variables`: list of variable name strings, e.g. `["A", "B", "C"]`
- `formula_str`: boolean expression using Python operators `and`, `or`, `not`
- Returns a list of satisfying assignments, each a dict mapping variable names to `True`/`False`. Empty list means UNSAT.

The function also prints the full truth table and a `SATISFIABLE`/`UNSATISFIABLE` summary to stdout.

## How It Works

1. Generate all `2^n` combinations with `itertools.product([True, False], repeat=n)`
2. Evaluate the formula under each assignment using `eval` with builtins disabled
3. Print each table row; collect assignments that evaluate to `True`

## Running the Tests

```bash
python3 "HW 1/test_sat.py"
```

The suite covers:

- the example formula (2 satisfying assignments)
- unsatisfiable formula (`A and not A`)
- tautology (`A or not A`)
- unit formula with unused variables
- empty variable list
- 5-variable formula

Each test is verified against a brute-force re-evaluation of every assignment, asserting that all returned assignments evaluate to `True` and all others to `False`.

## Limitations

- `formula_str` is passed to `eval` with builtins disabled, so it accepts any Python expression; only pass trusted, well-formed boolean formulas.
- Variable names that are Python keywords (e.g. `is`) or shadow names like `True` will break evaluation.
