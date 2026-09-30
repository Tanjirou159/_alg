# HW3: SAT Solver via Truth-Table Enumeration

## Overview

`solve_sat_truth_table(variables, formula_str)` determines whether a Boolean
formula is satisfiable (SAT) by exhaustively enumerating all `2^N` truth
assignments, where `N` is the number of variables. This is the simplest
complete SAT algorithm; it always terminates and gives a definitive answer,
but its runtime is exponential in the number of variables, so it is only
practical for small formulas.

## How It Works

1. **Generate assignments** — `itertools.product([True, False], repeat=n)`
   produces every possible combination of truth values for the `N` variables.

2. **Bind variables** — Each combination is turned into an environment
   (a `dict` mapping variable names to `True`/`False`) using
   `dict(zip(variables, values))`.

3. **Evaluate the formula** — The formula string is evaluated with Python's
   built-in `eval()` inside a **restricted environment**:

   ```python
   eval(formula_str, {"__builtins__": {}}, environment)
   ```

   - `{"__builtins__": {}}` disables access to Python built-ins (e.g.
     `open`, `__import__`), so the formula can only use the logical
     operators `and`, `or`, `not` and the provided variables.
   - `environment` supplies the current variable bindings.
   - `bool(...)` coerces the result to a truth value.

4. **Collect models** — Assignments that evaluate to `True` are appended to
   `satisfying_assignments`.

5. **Print truth table & verdict** — Every row of the truth table is printed,
   followed by a final status: `SATISFIABLE` (with the list of models) or
   `UNSATISFIABLE`.

## Complexity

- **Time:** `O(2^N)` formula evaluations — exponential in the number of
  variables.
- **Space:** `O(2^N)` in the worst case for storing all satisfying models.

## Test Cases

The `__main__` block demonstrates two cases:

| Case | Formula                                   | Expected Result |
|------|-------------------------------------------|-----------------|
| 1    | `(A or B) and (not A or C) and (not B or not C)` | SAT with 2 models: `{A:T, B:F, C:T}`, `{A:F, B:T, C:F}` |
| 2    | `A and not A`                             | UNSAT           |

## Usage

```bash
python3 sat.py
```

Or import it as a module:

```python
from sat import solve_sat_truth_table

models = solve_sat_truth_table(
    ['A', 'B'],
    "(A or B) and (not A or not B)"   # XOR
)
```
