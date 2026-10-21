# C(n,k): Recursion (non-DP) vs. Dynamic Programming

Number of ways to choose `k` items out of `n`, also written as
`C(n,k) = n! / (k! (n-k)!)`. It can be computed with a simple recurrence,
which makes it a perfect playground for comparing a **non-DP** approach
(naive recursion) with a **DP** approach (bottom-up table).

```
C(n,k) = C(n-1, k-1) + C(n-1, k)
```

Base cases: `C(n,0) = 1`, `C(n,n) = 1`.

Pascal's triangle is exactly this recurrence — each entry is the sum of
the two entries above it:

```
n=0               1
n=1             1   1
n=2           1   2   1
n=3         1   3   3   1
n=4       1   4   6   4   1
n=5     1   5  10  10   5   1
```

## Files

| File | What it does |
|---|---|
| `recursive.py` | Non-DP solution: naive recursion |
| `dp.py`        | DP solution: Pascal's triangle with a rolling array |
| `main.py`      | Runner: computes, verifies vs `math.comb`, benchmarks |

## How to run

```bash
python main.py 10 3        # C(10,3), both ways, with verification
python main.py --bench 30  # benchmark n = 5..30 with k = n//2
```

Example output for `python main.py 10 3`:

```
C(10,3) = 120
  recursive (non-DP): 120
    calls  : 239
    time   : 0.000054 s
  DP (rolling array): 120
    time   : 0.000003 s
  correctness: recursive OK, DP OK
```

## Approach 1: Naive recursion (non-DP)

```python
def comb_recursive(n, k):
    if k == 0 or k == n:
        return 1
    return comb_recursive(n - 1, k - 1) + comb_recursive(n - 1, k)
```

### Principle

Translate the recurrence directly into code. The call tree of `C(5,2)`
looks like this:

```
                          C(5,2)
                    /               \
              C(4,1)                C(4,2)
             /     \               /     \
        C(3,0)    C(3,1)        C(3,1)    C(3,2)
                  /   \         /   \
             C(2,0)  C(2,1) C(2,0)  C(2,1)
                      ...           ...
```

Notice that `C(3,1)`, `C(2,1)`, ... appear **many times**. The naive
recursion recomputes every one of them from scratch. The problem has
*overlapping subproblems*, and this approach solves each occurrence
independently.

### Complexity

The number of recursive calls is `2*C(n,k) - 1`, i.e.

- **Time: O(C(n,k))** — exponential. For `k = n/2`,
  `C(n, n/2) ~ 2^n / sqrt(n)`, so `C(30,15) → 310 million` calls and
  `C(40,20) → 276 billion` calls — completely impractical.
- **Space: O(n)** — only the recursion stack.

## Approach 2: Dynamic programming (bottom-up)

```python
def comb_dp(n, k):
    k = min(k, n - k)          # symmetry: C(n,k) = C(n,n-k)
    dp = [0] * (k + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):   # right-to-left!
            dp[j] = dp[j] + dp[j - 1]
    return dp[k]
```

### Principle

Build Pascal's triangle **row by row**, storing one row in an array
`dp[j] = C(i, j)`. Each subproblem is computed **exactly once** and then
reused by later rows:

- After processing row `i`, `dp[j]` holds `C(i, j)`.
- Row `i+1` is produced by `dp[j] = dp[j] + dp[j-1]`, i.e. each entry is
  the sum of the two entries above it.
- The inner loop goes **right-to-left** so that `dp[j-1]` still holds the
  value from the *previous* row when it is read.
- Because `C(n,k) = C(n,n-k)`, we only need columns `0..min(k, n-k)`.

### Complexity

- **Time: O(n·k)** — each of the `n` rows updates at most `k` cells.
  `C(40,20)` takes ~800 trivial additions instead of 137 billion calls.
- **Space: O(k)** — only one row is kept (rolling array), no recursion.

## Comparison

| | Naive recursion (non-DP) | Dynamic programming |
|---|---|---|
| Strategy | Recompute every subproblem on demand | Compute each subproblem once, store & reuse |
| Time | **O(C(n,k))** — exponential | **O(n·k)** — polynomial |
| Space | O(n) (stack) | O(k) (one row) |
| Overlapping subproblems | Wasted: solved many times | Exploited: solved once |
| Easy to write? | Very (direct translation) | Slightly more care (order, rolling array) |
| Feasible at k = n/2 | up to about n = 24 | up to n in the millions (with big ints) |

### Why DP wins here

The recurrence is *fixed* and the subproblems overlap heavily, so
remembering answers turns an exponential blow-up into a small polynomial
computation. The price is the O(k) table (memory instead of repeated
computation).

### When the naive recursion is still useful

- Tiny inputs, or `k` very close to 0 or `n` (few branches).
- When clarity of the code matters more than speed.
- It also shows why memoization exists: adding a cache to the recursion
  (top-down DP) keeps the same intuitive code but drops the time to
  O(n·k), at the cost of O(n·k) memory for the cache.

## Verification

`main.py` checks both implementations against Python's `math.comb`.
`--bench` shows the gap growing as `n` increases:

```
   n    k |  recursive s        DP s        calls
   5    2 |     0.000008     0.000002            19
  10    5 |     0.000051     0.000002           503
  15    7 |     0.001284     0.000003         12869
  20   10 |     0.030749     0.000003        369511
  25   12 |     0.817437     0.000004      10400599
  30   15 |    32.1 s        0.000056    310235039
```

(Approximate figures; your machine will differ. `--bench 25` is a safe
default — `n = 30` already takes ~half a minute in the naive recursion.)
