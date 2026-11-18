AI usage: yes — code and README were produced with AI assistance.

# HW11 — Numerical Differentiation, Integration, and Monte Carlo

## Overview

This project implements the four requested groups of methods for

```text
f(x) = x_1^2 + x_2^2 + ... + x_n^2,    low = 0, high = 1
```

1. numerical derivative and integral in one variable,
2. Monte Carlo integration in one variable,
3. numerical gradient and Riemann (hypervolume) integral in `n` variables,
4. Monte Carlo integration in `n` variables,

and evaluates them for `n = 1, 2, 5, 100`. The exact answers are

```text
integral over [0,1]^n of f dV = n/3
gradient of f at x          = 2x
```

because every coordinate contributes `integral from 0 to 1 of x^2 dx = 1/3`.
These closed forms are used to measure the error of every method.

## Files

| File | Contents |
|---|---|
| `numerical.py` | `derivative`, `simpson`, `gradient`, shared evaluation and box-validation helpers |
| `riemann.py` | `choose_subdivisions` and the required `integral(f, low, high)` midpoint Riemann rule |
| `monte_carlo.py` | `mc_integral`, `mc_integral_1d`, and the `MCResult` dataclass |
| `main.py` | Runs every demo, prints the comparison tables, command-line options |
| `test_hw11.py` | 20 `unittest` checks against the closed-form answers |
| `README.md` | This document |

## Quick start

```bash
cd HW11

python3 main.py                    # full run: 10^6 samples / grid budget
python3 main.py --quick            # 10^4 samples / budget, for slow machines
python3 -m unittest -v test_hw11   # 20 unit tests
```

Useful options:

```bash
python3 main.py --dims 1 2 5 100
python3 main.py --samples 2000000 --points 2000000
python3 main.py --seed 7
```

`--dims` accepts any positive dimensions, `--samples` controls Monte Carlo,
`--points` controls the automatic Riemann grid budget, and `--seed` makes the
Monte Carlo results reproducible.

## Methods

### 1. Single-variable derivative

Central difference:

```text
f'(x) ~= [f(x + h) - f(x - h)] / (2h)
h = eps^(1/3) * max(1, |x|)         (about 6.06e-6 in float64)
```

The truncation error is `O(h^2)` and the round-off error is `O(eps/h)`, so the
step is chosen near the balance point. A separate `h` can be passed to study
that trade-off. For `f(x) = x^2` the third derivative is zero, so the central
difference is exact in exact arithmetic; the table below therefore shows only
floating-point round-off.

### 2. Single-variable integral

Composite Simpson rule with `n = 10,000` subintervals:

```text
integral from a to b ~= h/3 * [f0 + 4(f1 + f3 + ...) + 2(f2 + f4 + ...) + fn]
h = (b - a) / n
```

Its error is `O(h^4)`, and it is exact for polynomials up to degree three.

### 3. n-variable gradient

Coordinate-wise central differences:

```text
df/dx_i ~= [f(x + h_i e_i) - f(x - h_i e_i)] / (2 h_i)
```

This costs `2n` function evaluations. The demo evaluates the gradient at
`x_i = (i + 1)/(n + 1)` for each dimension.

### 4. Riemann n-variable integral

`riemann.py` provides the requested function:

```python
integral(f, low, high)              # automatic grid
integral(f, low, high, subdiv=20)   # explicit cells per axis
```

It uses the midpoint rule on a tensor grid. With `m` cells per axis,

```text
integral over [low, high] ~= (product of h_j) *
    sum over k_1 ... k_n of f(low + (k + 0.5) h),
h_j = (high_j - low_j) / m.
```

The automatic `m` is the largest integer with `m^n <= max_points`
(default `max_points = 10^6`). This keeps the evaluation count bounded, and
the program reports both `m` and the actual number of grid points.

Two implementation details matter:

- NumPy arrays are limited to 64 dimensions, so an `n = 100` mesh cannot be
  built with `np.indices` or `np.meshgrid`. Instead, flat cell indices are
  decoded with mixed radix in chunks of shape `(B, n)`. This works for any
  `n` and keeps memory bounded.
- The user function may be vectorised (`(B, n) -> (B,)`, using `axis=-1`) or
  scalar-style (one point per call). `eval_batch` detects the vectorised form
  and falls back to a loop when necessary.

For the test function, the midpoint error has a closed form that is useful for
checking the implementation:

```text
per-axis midpoint error for x^2 = 1/(12 m^2)
total absolute error            = n/(12 m^2)
```

### 5. Monte Carlo n-variable integral

Uniform samples are drawn from the box:

```text
I ~= V * mean(f(U_i)),    V = product of (high_j - low_j)
standard error ~= V * s / sqrt(N)
```

The samples are generated in memory-bounded chunks, so `n = 100` with
`N = 10^6` does not allocate an `N x n` array at once. `mc_integral_1d` is a
one-variable wrapper around the same estimator.

## Results

All numbers below come from one full run of `python3 main.py` with seed 42 on
the machine used to prepare this README. Times are in seconds and are
machine-dependent.

### 1-D derivative, `f(x) = x^2`

| x | exact `2x` | numerical | absolute error | relative error |
|---:|---:|---:|---:|---:|
| 0.5 | 1.0000000000 | 1.0000000000 | 1.656e-12 | 1.656e-12 |
| 1.0 | 2.0000000000 | 2.0000000000 | 1.706e-11 | 8.532e-12 |
| 2.0 | 4.0000000000 | 4.0000000000 | 3.413e-11 | 8.532e-12 |
| 3.0 | 6.0000000000 | 6.0000000000 | 5.355e-12 | 8.925e-13 |

Step-size sweep at `x = 3` for `f(x) = exp(x)`:

| h | numerical | absolute error |
|---:|---:|---:|
| 1.0e-03 | 20.0855402708 | 3.348e-06 |
| 1.0e-05 | 20.0855369236 | 4.431e-10 |
| 1.0e-06 | 20.0855369261 | 2.930e-09 |
| 1.0e-07 | 20.0855368959 | 2.727e-08 |
| 1.0e-09 | 20.0855385657 | 1.643e-06 |

The error first falls as `h^2` (truncation dominates) and then rises as
`1/h` (round-off dominates). The best value is near `h = 1e-5`, as expected.

### 1-D integral, `f(x) = x^2` on `[0, 1]`, exact `1/3`

| Method | Estimate | Absolute error | Relative error | Time |
|---|---:|---:|---:|---:|
| Simpson, `n = 10,000` | 0.333333333333 | 5.551e-17 | 1.665e-16 | 0.0005 |
| Riemann midpoint, `m = 10^6` | 0.333333333333 | 8.338e-14 | 2.501e-13 | 0.0550 |
| Monte Carlo, `N = 10^6` | 0.333336884885 | 3.552e-06 | 1.065e-05 | 0.0322 |

Monte Carlo standard error: `2.982e-04`. Simpson wins in one dimension, as
expected from its fourth-order accuracy. This particular Monte Carlo estimate
is unusually close to the exact value (about `0.012` standard errors); repeated
seeds would scatter by roughly the standard error. The Riemann row calls the
general `integral(f, [0.0], [1.0])` with `n = 1`, and the Monte Carlo row calls
`mc_integral_1d`.

### n-D gradient

Gradient at `x_i = (i + 1)/(n + 1)`, exact `gradient = 2x`:

| n | max absolute error | max relative error | f evaluations | Time |
|---:|---:|---:|---:|---:|
| 1 | 1.656e-12 | 1.656e-12 | 2 | 0.0002 |
| 2 | 5.264e-12 | 3.948e-12 | 4 | 0.0001 |
| 5 | 2.097e-11 | 3.145e-11 | 10 | 0.0002 |
| 100 | 4.301e-10 | 1.200e-08 | 200 | 0.0011 |

The absolute error stays below `5e-10` even at `n = 100`. The largest relative
error (`1.2e-8`) occurs at the smallest coordinate, where `2x` is small; the
growth comes from accumulating 100 terms in `f` and from the division by the
small step.

### n-D Riemann integral

`f(x) = sum(x_i^2)` on `[0,1]^n`, exact `n/3`:

| n | m | Grid points | Estimate | Exact | Relative error | Time |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,000,000 | 1,000,000 | 0.3333333333 | 0.3333333333 | 2.501e-13 | 0.0794 |
| 2 | 1,000 | 1,000,000 | 0.6666665000 | 0.6666666667 | 2.500e-07 | 0.1193 |
| 5 | 15 | 759,375 | 1.6648148148 | 1.6666666667 | 1.111e-03 | 0.1248 |
| 100 | 1 | 1 | 25.0000000000 | 33.3333333333 | 2.500e-01 | 0.0007 |

The `n = 100` result is intentionally the one-cell midpoint value. It is
explained in the next section.

### n-D Monte Carlo integral

Same function and box, `N = 10^6` samples:

| n | Samples | Estimate | Exact | Standard error | Relative error | Time |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,000,000 | 0.3333368849 | 0.3333333333 | 2.982e-04 | 1.065e-05 | 0.0526 |
| 2 | 1,000,000 | 0.6664325513 | 0.6666666667 | 4.218e-04 | 3.512e-04 | 0.1096 |
| 5 | 1,000,000 | 1.6663558068 | 1.6666666667 | 6.668e-04 | 1.865e-04 | 0.1610 |
| 100 | 1,000,000 | 33.3330304757 | 33.3333333333 | 2.981e-03 | 9.086e-06 | 2.4069 |

### Convergence

Riemann midpoint in 2-D, where the exact integral is `2/3`:

| m | Grid points | Estimate | Absolute error | Error ratio |
|---:|---:|---:|---:|---:|
| 10 | 100 | 0.6650000000 | 1.667e-03 | — |
| 20 | 400 | 0.6662500000 | 4.167e-04 | 4.00 |
| 40 | 1,600 | 0.6665625000 | 1.042e-04 | 4.00 |
| 100 | 10,000 | 0.6666500000 | 1.667e-05 | 6.25 |
| 200 | 40,000 | 0.6666625000 | 4.167e-06 | 4.00 |

Doubling `m` divides the error by about four, which is the expected
`O(m^-2)`. The `40 -> 100` row has ratio `6.25` because `m` grows by a factor
of `2.5`, and `2.5^2 = 6.25`.

Monte Carlo in 100-D, where the exact integral is `100/3`:

| N | Estimate | Absolute error | Standard error | abs(error)/stderr |
|---:|---:|---:|---:|---:|
| 1,000 | 33.3868800533 | 5.355e-02 | 9.664e-02 | 0.554 |
| 10,000 | 33.3336884885 | 3.552e-04 | 2.975e-02 | 0.012 |
| 100,000 | 33.3249736851 | 8.360e-03 | 9.389e-03 | 0.890 |
| 1,000,000 | 33.3330304757 | 3.029e-04 | 2.981e-03 | 0.102 |

The standard error falls by about `sqrt(10) = 3.16` each time `N` grows by
10. The actual error fluctuates around it, as it must for a random estimator.

## Why the 100-D Riemann result is 25.0

A tensor grid with `m` cells per axis has `m^n` points. For `n = 100`, even
`m = 2` requires

```text
2^100 = 1,267,650,600,228,229,401,496,703,205,376  (~1.27e30)
```

evaluations, which is impossible. With the one-million-point budget the
largest feasible choice is `m = 1`: a single midpoint cell at
`(0.5, ..., 0.5)`. There,

```text
f(0.5, ..., 0.5) = 100 * 0.25 = 25
cell volume      = 1
Riemann estimate = 25
exact integral   = 100/3 = 33.3333...
relative error   = 25%
```

This is not a coding error. It is the curse of dimensionality: the number of
tensor-grid points grows exponentially with dimension, while the budget is
fixed. The program deliberately reports `m` and the grid size so that this
loss of resolution is visible.

The analytical midpoint error for this particular `f` is `n/(12 m^2)`. At
`n = 100, m = 1`, that is `100/12 = 8.3333`, exactly the difference between
`33.3333` and `25`.

## Riemann versus Monte Carlo at the same budget

Using the full-run relative errors:

| n | Riemann relative error | Monte Carlo relative error | Winner |
|---:|---:|---:|---|
| 1 | 2.501e-13 | 1.065e-05 | Riemann |
| 2 | 2.500e-07 | 3.512e-04 | Riemann |
| 5 | 1.111e-03 | 1.865e-04 | Monte Carlo |
| 100 | 2.500e-01 | 9.086e-06 | Monte Carlo |

The reason is the error scaling with the number of evaluations `N`:

```text
Riemann midpoint:  O(N^(-2/n))        (tensor grid, N = m^n)
Monte Carlo:       O(N^(-1/2))        (independent of n)
```

For this test function the constants are also known. The midpoint error is
`n/(12 m^2)`, and the variance of `f` over the box is `4n/45`, so the Monte
Carlo standard error is

```text
sqrt(4n / (45 N))
```

For example, `n = 100, N = 10^6` gives `sqrt(400 / (45 * 10^6)) = 2.981e-03`,
which matches the measured standard error in the table. Monte Carlo is already
better than the one-million-point Riemann rule at `n = 5`, and it is the only
practical option at `n = 100`.

## Tests

`test_hw11.py` contains 20 tests:

- central difference against `2x` and `cos(x)`,
- Simpson against `1/3`, including a scalar-only `math.sin` function and an
  odd interval count,
- gradient against `2x` for `n = 1, 2, 5`,
- Riemann integration for `n = 1, 2, 5`,
- the expected `25.0` one-cell value for `n = 100`,
- the scalar-function fallback for the n-D Riemann rule,
- Monte Carlo in 1-D and 100-D using a `5 * stderr` tolerance,
- invalid boxes, lengths, and sample counts.

Run:

```bash
python3 -m unittest -v test_hw11
```

Result:

```text
Ran 20 tests in 1.139s

OK
```

## Reproducibility and limitations

- Python 3.12.3, NumPy 2.5.3; only NumPy is used beyond the standard library.
- Monte Carlo uses `numpy.random.default_rng(seed)` with seed 42 (or `--seed`).
- Times depend on the machine; the numerical estimates do not.
- The Riemann rule is a fixed uniform tensor grid; it is not adaptive and does
  not use sparse grids. This is deliberate, because the assignment asks for a
  Riemann sum.
- Monte Carlo uses plain uniform sampling; no variance reduction is applied.
- The central-difference step is fixed by the standard `eps^(1/3)` rule; the
  h-sweep shows the truncation/round-off trade-off.

<details>
<summary>Full output of <code>python3 main.py</code></summary>

```text
HW11 - Numerical differentiation/integration and Monte Carlo
Python 3.12.3, NumPy 2.5.3
dimensions=[1, 2, 5, 100], samples=1,000,000, Riemann budget=1,000,000, seed=42

1. Single-variable numerical derivative
   f(x) = x^2, central difference, h = eps^(1/3) * max(1, |x|)
       x          exact        numerical    abs error    rel error
     0.5   1.0000000000     1.0000000000    1.656e-12    1.656e-12
     1.0   2.0000000000     2.0000000000    1.706e-11    8.532e-12
     2.0   4.0000000000     4.0000000000    3.413e-11    8.532e-12
     3.0   6.0000000000     6.0000000000    5.355e-12    8.925e-13

   h sweep at x = 3 for f(x) = exp(x):
            h          numerical    abs error
      1.0e-03      20.0855402708    3.348e-06
      1.0e-05      20.0855369236    4.431e-10
      1.0e-06      20.0855369261    2.930e-09
      1.0e-07      20.0855368959    2.727e-08
      1.0e-09      20.0855385657    1.643e-06

2. Single-variable numerical integration
   f(x) = x^2 on [0, 1], exact = 1/3
   method                                     estimate    abs error    rel error   time (s)
   Simpson (n=10,000)                   0.333333333333    5.551e-17    1.665e-16     0.0005
   Riemann midpoint (m=1,000,000)       0.333333333333    8.338e-14    2.501e-13     0.0550
   Monte Carlo (N=1,000,000)            0.333336884885    3.552e-06    1.065e-05     0.0322
   Monte Carlo standard error: 2.982e-04

3. n-D numerical gradient
   f(x) = sum(x_i^2), x_i = (i+1)/(n+1), exact gradient = 2x
      n   max abs error   max rel error  f evals   time (s)
      1       1.656e-12       1.656e-12        2     0.0002
      2       5.264e-12       3.948e-12        4     0.0001
      5       2.097e-11       3.145e-11       10     0.0002
    100       4.301e-10       1.200e-08      200     0.0011

4. n-D Riemann integral (midpoint rule)
   f(x) = sum(x_i^2) on [0, 1]^n, exact = n/3
      n        m    grid points         estimate            exact    rel error   time (s)
      1  1000000        1000000     0.3333333333     0.3333333333    2.501e-13     0.0794
      2     1000        1000000     0.6666665000     0.6666666667    2.500e-07     0.1193
      5       15         759375     1.6648148148     1.6666666667    1.111e-03     0.1248
    100        1              1    25.0000000000    33.3333333333    2.500e-01     0.0007

5. n-D Monte Carlo integral
   f(x) = sum(x_i^2) on [0, 1]^n, exact = n/3
      n    samples         estimate            exact       stderr    rel error   time (s)
      1  1,000,000     0.3333368849     0.3333333333    2.982e-04    1.065e-05     0.0526
      2  1,000,000     0.6664325513     0.6666666667    4.218e-04    3.512e-04     0.1096
      5  1,000,000     1.6663558068     1.6666666667    6.668e-04    1.865e-04     0.1610
    100  1,000,000    33.3330304757    33.3333333333    2.981e-03    9.086e-06     2.4069

6. Convergence checks

   Riemann midpoint in 2-D (f = x1^2 + x2^2), error should fall ~4x
        m  grid points         estimate    abs error    ratio
       10          100     0.6650000000    1.667e-03        -
       20          400     0.6662500000    4.167e-04     4.00
       40         1600     0.6665625000    1.042e-04     4.00
      100        10000     0.6666500000    1.667e-05     6.25
      200        40000     0.6666625000    4.167e-06     4.00

   Monte Carlo in 100-D (f = sum x_i^2), error ~ 1/sqrt(N)
            N         estimate    abs error       stderr  |err|/stderr
        1,000    33.3868800533    5.355e-02    9.664e-02         0.554
       10,000    33.3336884885    3.552e-04    2.975e-02         0.012
      100,000    33.3249736851    8.360e-03    9.389e-03         0.890
    1,000,000    33.3330304757    3.029e-04    2.981e-03         0.102
```

</details>
