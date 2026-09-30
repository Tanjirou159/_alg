# HW4 — Iterative Methods / 迭代法

This directory contains a small Python project demonstrating **iterative numerical methods**:

- `iterative3.py` — solves `f(x) = x³ − x − 2 = 0` with the **Newton-Raphson method**
- `iter_framework.py` — a reusable framework containing
  1. the core abstract iteration engine `generic_iterator`,
  2. the high-level scalar solver `solve_iterative` (used by `iterative3.py`), and
  3. nine demo implementations of classic iterative algorithms

---

## 1. Project Structure

```
HW4/
├── iterative3.py        # Newton-Raphson root finder (entry point)
└── iter_framework.py    # generic iteration framework + algorithm demos
```

The two files are decoupled: `iterative3.py` does not re-implement any iteration
loop. It only defines the problem (`f`, `df`, `newton_step`) and delegates the
iteration to `solve_iterative` from the framework. This is an example of the
"pass a function to a generic engine" pattern.

---

## 2. `iterative3.py` — Newton-Raphson Root Finder

### 2.1 Problem

Find the root of

```
f(x) = x³ − x − 2 = 0
```

which has the real root `x* ≈ 1.5213797068`.

### 2.2 How it works

1. **`f(x)`** — the target function.
2. **`df(x)`** — its derivative, `f′(x) = 3x² − 1`.
3. **`newton_step(x)`** — one Newton-Raphson update:

   ```
   x_{n+1} = x_n − f(x_n) / f′(x_n)
   ```

   It guards against a (nearly) zero derivative, which would make the
   iteration undefined, by raising `ZeroDivisionError` when `|f′(x)| < 1e-12`.
4. **`main()`** — sets up the problem and calls the framework:

   ```python
   result = solve_iterative(
       step_func=newton_step,   # the update rule
       x0=1.5,                  # initial guess
       tol=1e-8,                # convergence tolerance
       max_iter=50,             # safety cap on iterations
       criterion="absolute",    # stop when |x_n − x_{n−1}| < tol
       verbose=True             # print every iteration
   )
   ```

   `solve_iterative` returns a dict with keys `solution`, `iterations`,
   `converged`, which `main()` prints as the final summary along with the
   residual `f(x*)`.

### 2.3 Why Newton-Raphson converges so fast

The method uses the local linearization of `f` at each step, so near the root
the error squares every iteration (quadratic convergence). The observed run
takes only 4 iterations from `x0 = 1.5`.

### 2.4 Expected output

```
==================================================
   Problem Solver: Root Finding via Newton-Raphson
   Target Equation: f(x) = x^3 - x - 2 = 0
==================================================

  Iteration   1: x =  1.521739130435   |x_1 - x_0| = 2.1739e-02
  Iteration   2: x =  1.521379805965   |x_2 - x_1| = 3.5932e-04
  Iteration   3: x =  1.521379706805   |x_3 - x_2| = 9.9160e-08
  Iteration   4: x =  1.521379706805   |x_4 - x_3| = 7.5495e-15

=== Execution Summary ===
Converged Solution (x*) : 1.5213797068
Residual Value f(x*)    : 0.0000000000e+00
Total Iteration Count   : 4
Convergence Achieved    : True
```

Run it with:

```bash
python3 iterative3.py
```

---

## 3. `iter_framework.py` — Generic Iteration Framework

### 3.1 Core abstraction: `generic_iterator`

```python
generic_iterator(transition_func, is_converged, initial_state, max_iter=1000)
```

Every iterative algorithm can be expressed as:

- a **state** (scalar, vector, matrix, or tuple),
- a **transition function** `g(state) → next_state`,
- a **convergence test** `is_converged(state, next_state, iteration) → bool`.

The engine simply repeats

```python
state ← g(state)
```

until the convergence test passes or `max_iter` is reached, then returns
`(final_state, iteration_count)`. All nine demos below are instances of this
single pattern — only the state type and the two functions change.

### 3.2 High-level wrapper: `solve_iterative`

```python
solve_iterative(step_func, x0, tol=1e-8, max_iter=100, criterion="absolute", verbose=False)
```

This is the scalar-friendly wrapper used by `iterative3.py`. It:

- starts from the initial guess `x0`,
- applies `step_func` repeatedly,
- stops when the step size `|x_n − x_{n−1}|` drops below `tol`
  (`criterion="absolute"`), or when the relative step
  `|x_n − x_{n−1}| / max(|x_n|, 1e-12)` drops below `tol`
  (`criterion="relative"`),
- optionally logs every iteration when `verbose=True`,
- prints a warning if `max_iter` is reached without convergence,
- returns `{"solution", "iterations", "converged"}`.

### 3.3 Demo algorithms

Running `iter_framework.py` directly executes all nine demos, which showcase
how different classic iterative algorithms map onto the same engine:

| # | Demo | Method | State | Transition |
|---|------|--------|-------|------------|
| 1 | Fixed-point iteration (2-D) | linear system solver | vector | `x ← 0.5·x − 0.2·y + 0.3` style affine map |
| 2 | Newton's method | root finding of `x² − 4 = 0` | scalar | `x ← x − f(x)/f′(x)` |
| 3 | Gauss-Seidel | solve `Ax = b` | vector | in-place coordinate relaxation |
| 4 | Power iteration | dominant eigenvector | vector | `v ← Av / ‖Av‖` |
| 5 | QR algorithm | all eigenvalues | matrix | `A ← R·Q` (from QR decomposition) |
| 6 | RK4 | ODE `dy/dt = y − t + 1` | tuple `(t, y)` | one Runge-Kutta step |
| 7 | PageRank | stationary web distribution | vector | `r ← G·r` on Google matrix |
| 8 | K-Means | 2-cluster centroids | matrix | E-step label assignment + M-step centroid update |
| 9 | EM (two-coin) | latent probability estimates | tuple `(θ_A, θ_B)` | E-step likelihood weights + M-step MLE update |

These demos show that seemingly unrelated algorithms (root finding, linear
solvers, eigenproblems, ODEs, clustering) all share the same skeleton:

```
initialize state
repeat:
    state ← transition(state)
until converged(state) or out of iterations
```

Run them with:

```bash
python3 iter_framework.py
```

---

## 4. Requirements

- Python 3
- NumPy (imported by `iter_framework.py`)
