# HW8: Traveling Salesman Problem — Five Algorithms

Given `n` cities in the plane, the **Traveling Salesman Problem (TSP)**
asks for the shortest closed tour that visits every city exactly once
and returns to the start. TSP is **NP-hard**: the only exact solution is
to try all `(n-1)!` tours, which explodes around `n = 11`. This project
solves the same random instance with **five heuristic algorithms** and
compares them:

| # | Method | Chinese name | Core idea |
|---|---|---|---|
| 1 | Greedy | 貪婪演算法 | always go to the closest unvisited city |
| 2 | Improvement (2-opt) | 改良法 | repeatedly apply the first shortening 2-opt move to a known tour |
| 3 | Hill climbing | 爬山演算法 | local search from random starts, accept only improvements |
| 4 | Simulated annealing | 模擬退火法 | hill climbing + accept worse moves with probability `exp(-ΔE/T)` |
| 5 | Gradient descent | 梯度下降法 | discrete adaptation: steepest descent on the finite-difference gradient |

A tour is a list of city indices, e.g. `[0, 3, 1, 2]` = `0 -> 3 -> 1 -> 2 -> 0`.
Its energy is

```
E(tour) = d(tour[0], tour[1]) + d(tour[1], tour[2]) + ... + d(tour[n-1], tour[0])
```

where `d(i, j)` is the Euclidean distance between cities `i` and `j`.
Every method tries to minimize `E`.

## Files

| File | What it does |
|---|---|
| `tsp_utils.py` | cities, distance matrix, tour length, swap / 2-opt moves, brute force |
| `greedy.py` | Method 1: nearest neighbour (single start or all starts) |
| `improvement.py` | Method 2: first-improvement 2-opt local search |
| `hill_climbing.py` | Method 3: random-restart hill climbing (swap or 2-opt moves) |
| `simulated_annealing.py` | Method 4: Metropolis algorithm with geometric cooling |
| `gradient_descent.py` | Method 5: steepest descent on the finite-difference gradient |
| `main.py` | runner: builds one instance, runs all five methods, compares them |

Pure Python 3 standard library, no dependencies.

## How to run

```bash
python main.py                          # 20 random cities, all five methods
python main.py --n 8 --optimal          # small case + brute-force optimum
python main.py --n 50 --restarts 200    # bigger instance, more hill-climb restarts
python main.py --seed 7 --csv tour.csv  # different cities, export best tour
python main.py --single-start           # greedy uses city 0 instead of all starts
```

Sample output (`python main.py`, n = 20, seed = 42):

```
method                             length   time (s)       gap
---------------------------------------------------------------
greedy (all starts)                353.78     0.0004     0.42%
improvement (2-opt, first)         352.32     0.0003     0.00%
hill climbing                      352.32     0.0918     0.00%
simulated annealing                352.32     0.0451     0.00%
gradient descent (steepest)        352.32     0.0007     0.00%
gap is measured against: best found = 352.32
```

## Method 1: Greedy algorithm (貪婪演算法)

**Principle.** Start at a city. From the current city, always travel to
the closest unvisited city, until all cities are used. The choices are
made locally and never reconsidered.

```python
def greedy(dist, start=0):
    tour, cur, unvisited = [start], start, set(range(n)) - {start}
    while unvisited:
        nxt = min(unvisited, key=lambda v: dist[cur][v])   # closest city
        tour.append(nxt); unvisited.remove(nxt); cur = nxt
    return tour
```

`greedy_all_starts` repeats this from every city and keeps the best
result (the default in `main.py`).

**Complexity.** O(n²) for one start, O(n³) for all starts.

**Strengths / weaknesses.** Instant, and a reasonable starting point.
But the last few edges are often terrible — the tour can be arbitrarily
far from optimal, and nothing is ever repaired. That is exactly what
the next four methods do.

## Method 2: Improvement method, 2-opt (改良法)

**Principle.** Start from an existing tour (here: the greedy tour) and
repeatedly apply the *first* 2-opt move found that shortens it, until a
full scan finds no improving move. Deterministic.

A **2-opt move** picks two positions `i < j` and reverses the segment
`tour[i+1 .. j]`. It replaces the two edges `(i, i+1)` and `(j, j+1)`
with `(i, j)` and `(i+1, j+1)`:

```
before:   i ---- i+1              after:    i ---------- j
           \     /                          |           |
            \   /                           |           |
             \ /                            |           |
             / \                            |           |
            /   \                           |           |
          j+1 -- j                       i+1 -------- j+1
```

If the two old edges cross, the new parallel edges are always shorter
(triangle inequality), so 2-opt removes crossings. Any crossing tour in
the plane can be improved, so the final tour is **crossing free**.

**Complexity.** One scan checks O(n²) moves at O(n) each = O(n³); only a
few scans are needed in practice.

**Strengths / weaknesses.** Cheap and effective — this is the classic
TSP heuristic. It stops at a *local optimum* of the 2-opt neighbourhood,
which is usually close to, but not always, the global optimum.

## Method 3: Hill climbing (爬山演算法)

**Principle.** Local search: from the current tour, try random moves and
accept a move only if it strictly lowers `E`. A single run climbs to the
nearest local optimum and gets stuck there, so we **restart** from many
random tours and keep the best local optimum found.

The default move is a plain swap of two positions (smallest possible
change). Its local optima are weak, which makes the "stuck in a local
optimum" trap very visible — that is the whole point of this method.

**Complexity.** Each scan is O(n²) moves x O(n) = O(n³); `restarts`
independent climbs are run.

**Experiment: neighbourhood strength.** On the n = 50 instance,
hill climbing with `restarts = 50`:

| move | tour length |
|---|---|
| swap (default) | 690.90 |
| 2-opt (`move="2opt"`) | 566.36 |

The same algorithm changes result by ~18% purely because of the
neighbourhood — local optima are defined *relative to the moves used*.

## Method 4: Simulated annealing (模擬退火法)

**Principle.** Hill climbing that is allowed to *worsen* the tour with
probability `exp(-ΔE / T)` (Metropolis criterion). The temperature `T`
starts high and cools geometrically (`T *= alpha`): while hot, the walk
jumps freely across the landscape and escapes local optima; while cold,
it settles into a deep basin. The best tour seen along the walk is
remembered and returned.

```python
if delta < 0 or random() < exp(-delta / t):   # Metropolis criterion
    tour, cur = cand, length
```

**Complexity.** O(iters · n) with `iters` attempted moves. Quality
depends on the schedule `t0 → tmin` and on `iters`.

**Strengths / weaknesses.** The strongest method here: started from a
random tour it still found the best result on every test instance. The
price is the tuning of `t0`, `tmin`, `iters`.

## Method 5: Gradient descent (梯度下降法) — adapted to a discrete problem

**Principle.** Classical gradient descent updates a continuous point
`x <- x - lr * grad f(x)`. A tour is a *permutation*, so `grad E` does
not exist in the usual sense. We use the standard discrete analogue:

1. the possible directions from a tour are the 2-opt moves;
2. the directional derivative along a direction is the **finite
   difference** `E(moved tour) - E(tour)`;
3. evaluating all O(n²) directions gives the full finite-difference
   gradient;
4. one gradient-descent step = move along the **most negative**
   direction (steepest descent), step size = one move;
5. stop when every directional derivative is `>= 0` — the exact
   discrete analogue of the stopping condition `grad f = 0`.

```python
while True:
    grad = {(i, j): E(two_opt(tour, i, j)) - E(tour)  for all i < j}  # finite differences
    best = min(grad, key=grad.get)
    if grad[best] >= 0: break           # local minimum: grad >= 0 everywhere
    tour = two_opt(tour, *best)         # step along -grad (steepest descent)
```

**Complexity.** Each iteration evaluates the whole gradient: O(n²)
directions x O(n) = **O(n³)**; a handful of iterations suffice.

**Contrast with Method 2.** Both use 2-opt moves, but the improvement
method takes the *first* downhill move it finds, while gradient descent
computes the *entire* gradient and steps in the steepest direction.
On the n = 50 instance the two converge to different local optima
(581.83 vs 571.81) — first-improvement vs steepest descent are genuinely
different algorithms.

**Notes.** A "learning rate" has no natural meaning on a discrete set,
so the step is one move. Truly *continuous* relaxations of TSP (soft
permutation matrices via Sinkhorn normalization, neural combinatorial
solvers) exist and use real gradient descent; they are beyond the scope
of this homework, but they start from the same idea: make the discrete
problem differentiable.

## Comparison

All runs on the same instance (seed = 42). Gap = excess over the best
tour found in that run. Times are approximate, on one machine.

**n = 20**

| method | length | gap | time (s) |
|---|---|---|---|
| greedy (all starts) | 353.78 | +0.42% | 0.0004 |
| improvement (2-opt, first) | 352.32 | 0.00% | 0.0003 |
| hill climbing (swap, 50 restarts) | 352.32 | 0.00% | 0.0918 |
| simulated annealing | 352.32 | 0.00% | 0.0451 |
| gradient descent (steepest) | **352.32** | 0.00% | 0.0007 |

**n = 50**

| method | length | gap | time (s) |
|---|---|---|---|
| greedy (all starts) | 598.06 | +4.59% | 0.0039 |
| improvement (2-opt, first) | 581.83 | +1.75% | 0.0150 |
| hill climbing (swap, 50 restarts) | 690.90 | +20.83% | 2.3324 |
| simulated annealing | 576.06 | +0.74% | 0.0722 |
| gradient descent (steepest) | **571.81** | 0.00% | 0.0165 |

**n = 100** (simulated annealing with 50000 iterations)

| method | length | gap | time (s) |
|---|---|---|---|
| greedy (all starts) | 915.92 | +12.79% | 0.0264 |
| improvement (2-opt, first) | 841.27 | +3.60% | 0.3920 |
| hill climbing (swap, 50 restarts) | 1143.50 | +40.82% | 24.3259 |
| simulated annealing | 831.68 | +2.42% | 0.3867 |
| gradient descent (steepest) | **812.03** | 0.00% | 0.4446 |

**Qualitative summary**

| method | speed | quality | escapes local optima? |
|---|---|---|---|
| greedy | ★★★★★ | ★★ | — (never improves itself) |
| improvement (2-opt) | ★★★★ | ★★★★ | no |
| hill climbing (swap) | ★★ | ★★ | only via random restarts |
| simulated annealing | ★★★ | ★★★★★ | yes (Boltzmann acceptance) |
| gradient descent (steepest) | ★★★ | ★★★★ | no |

## Verification

For small `n`, `main.py --optimal` runs brute force over all `(n-1)!`
tours so every heuristic can be checked against the true optimum.

`python main.py --n 8 --optimal`:

```
method                             length   time (s)       gap
---------------------------------------------------------------
greedy (all starts)                253.28     0.0001     0.00%
improvement (2-opt, first)         253.28     0.0000     0.00%
hill climbing                      253.28     0.0042     0.00%
simulated annealing                253.28     0.0337     0.00%
gradient descent (steepest)        253.28     0.0000     0.00%
optimal (brute force)              253.28     0.0039        --
```

All five methods find the optimum on the small instance. On larger
instances the differences above appear.

## Discussion

- **Exact vs heuristic.** Brute force is exact but exponential
  (`(n-1)!` tours); it is practical only to about `n = 11`. All five
  heuristics run in polynomial time, at the cost of only approximate
  optimality.
- **Neighbourhood defines local optima.** Hill climbing over swaps is
  the same *algorithm family* as the 2-opt methods, yet its results are
  much worse — because a swap-local optimum is a weaker guarantee than
  a 2-opt-local optimum. The move set matters as much as the algorithm.
- **Escaping local optima.** Only simulated annealing escapes local
  optima *during* a run (by accepting worse moves while hot); hill
  climbing escapes only by restarting. That is why annealing is the
  most reliable method here.
- **Greedy + improve.** The classic recipe — build with the greedy
  method, then polish with 2-opt — is what Methods 2 and 5 do, and it
  already gets within a few percent of the best result.
- **Gradient descent on discrete problems.** TSP has no derivatives, so
  gradient descent must be adapted: finite-difference gradient +
  steepest descent. The result is an excellent local search, but like
  all gradient methods it stops at the first local minimum.
