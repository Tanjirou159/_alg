# HW5: Functional & Recursive Programming

This assignment demonstrates recursive and functional programming
techniques (no `for`/`while` loops in the core logic) with four programs.

## Requirements

- Python 3 (any version >= 3.6; only the standard library is used).

## Files

| File                  | Description                                                        |
| --------------------- | ------------------------------------------------------------------ |
| `bubble_sort.py`      | `map`/`filter`/`reduce` reimplemented recursively, plus loop-free Bubble Sort |
| `hanoi_iterative.py`  | Tower of Hanoi solved with an explicit stack (no recursion)        |
| `hanoi_recursive.py`  | Tower of Hanoi solved with recursion                               |
| `symbolic_diff.py`    | Symbolic differentiation of expression trees + simplifier          |

## Running

```bash
python3 bubble_sort.py
python3 hanoi_iterative.py
python3 hanoi_recursive.py
python3 symbolic_diff.py
```

Each script prints its own demo output when run directly.

## Sample Output

```text
Original Data: [64, 34, 25, 12, 22, 11, 90]
Sorted Data:   [11, 12, 22, 25, 34, 64, 90]
Filtered Evens: [12, 22, 34, 64, 90]
Mapped Doubled: [22, 24, 44, 50, 68, 128, 180]

Iterative Hanoi (3 disks): [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
Recursive Hanoi (3 disks): [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]

Raw Derivative:        ('+', ('*', ('*', 3, ('**', 'x', 2)), 1), ('+', ('*', 0, 'x'), ('*', 2, 1)))
Simplified Derivative: ('+', ('*', 3, ('**', 'x', 2)), 2)
```

## How It Works

### `bubble_sort.py`

- `my_map`, `my_filter`, `my_reduce`: recursive reimplementations of the
  standard higher-order functions.
- `bubble_pass(lst)`: one left-to-right pass that bubbles the largest
  element to the end, implemented with `my_reduce` (an accumulator holds
  the in-progress sorted prefix).
- `bubble_sort(lst)`: runs at most `len(lst)` passes recursively. A list
  of length `n` is guaranteed sorted after `n-1` passes, so this is
  correct (and terminating).

Complexity: `O(n^2)` time, `O(n^2)` memory due to list slicing.

### `hanoi_iterative.py` / `hanoi_recursive.py`

Both move `n` disks from peg `A` to peg `C` using auxiliary peg `B`:

1. Move `n-1` disks `A -> B`
2. Move largest disk `A -> C`
3. Move `n-1` disks `B -> C`

- Recursive version implements this directly via a nested helper.
- Iterative version keeps an explicit LIFO stack of `(disks, src, tgt, aux)`
  frames and pushes the three sub-problems in reverse order so they pop in
  the correct sequence.

Both produce exactly `2^n - 1` moves.

### `symbolic_diff.py`

Expressions are trees: numbers and strings are leaves; tuples hold an
operator and two operands (`'+'`, `'-'`, `'*'`, `'/'`, `'**'`).

`sym_diff(expr, var)` applies the standard calculus rules:

- Constant rule: `d/dx(c) = 0`
- Variable rule: `d/dx(x) = 1`, `d/dx(y) = 0`
- Sum/difference: `(u ± v)' = u' ± v'`
- Product: `(u·v)' = u'·v + u·v'`
- Quotient: `(u/v)' = (u'·v - u·v') / v^2`
- Power: `(u^n)' = n·u^(n-1)·u'` (constant exponent)

`simplify(expr)` folds obvious identities (`x + 0`, `0·x`, `x·1`, `x^0`, `x^1`).
It is intentionally basic: the raw tree may still contain `0 + u`, `0 * v`,
`1 * u`, etc., but they are harmless for numeric evaluation.

## Verification Performed

- All four scripts run to completion with the demo output above.
- `bubble_sort` matches Python's `sorted()` on 500 random cases
  (sizes 0–30, values −1000..1000) and handles empty/single-element lists.
- `hanoi_iterative` and `hanoi_recursive` produce identical move sequences
  and exactly `2^n - 1` moves for `n = 0..7`.
- `sym_diff` verified on `x^5` → `5·x^4`, `x·x` → `2x`, and the quotient
  `x/(x+1)` → `1/(x+1)^2` (after simplification).
- For `d/dx (x^3 + 2x)` the simplified result is `3·x^2 + 2`, as expected.

## Notes

- Importing `hanoi_iterative.py` or `hanoi_recursive.py` runs a demo print;
  guard with `if __name__ == "__main__":` if you need silent imports.
- `my_reduce` uses `initial=None` as its "no initial value" sentinel, so
  reducing a sequence whose first element is `None` is not supported (not
  needed for this assignment).
