# HW 2: Recurrence Equations — Exact Values and Big O

Solve the four recurrence equations by deriving the closed form, then verify each
closed form against a step-by-step simulation of the recurrence.

## Answers

| Recurrence              | Closed form        | Big O       |
| ----------------------- | ------------------ | ----------- |
| T(n) = T(n-1) + 8       | 8n - 7             | O(n)        |
| T(n) = 2 T(n-1) + 9     | 10·2^(n-1) - 9     | O(2^n)      |
| T(n) = 2 T(n/2) + 1     | 2n - 1             | O(n)        |
| T(n) = T(n/2) + 1       | log2(n) + 1        | O(log n)    |

All with base case T(1) = 1. The divide cases assume n = 2^k.

### Derivations

1. T(n) = T(n-1) + 8: unrolls to T(1) + 8(n-1) = 8n - 7, so O(n).
2. T(n) = 2 T(n-1) + 9: solves to (T(1) + 9)·2^(n-1) - 9 = 10·2^(n-1) - 9, so O(2^n).
3. T(n) = 2 T(n/2) + 1: T(2^k) = 2^(k+1) - 1 = 2n - 1, so O(n).
4. T(n) = T(n/2) + 1: T(2^k) = k + 1 = log2(n) + 1, so O(log n).

## Files

- `recurrences.py` — closed-form solvers, iterative simulator, demo output
- `test_recurrences.py` — standalone test suite (no dependencies)

## Usage

```bash
python3 HW2/recurrences.py
python3 HW2/test_recurrences.py
```

The demo prints the exact T(n) values for several n and the Big O complexity for
each recurrence. The test suite checks the closed forms against the brute-force
simulation and against hand-computed values.
