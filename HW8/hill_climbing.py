"""TSP method 3: hill climbing (爬山演算法).

Local search that accepts a move only when it strictly improves the
tour. A single run climbs to the nearest local optimum and stops there,
so we restart from many random tours and keep the best local optimum
found.

The default move is a plain swap of two tour positions -- the smallest
possible change to a tour. Its local optima are weak, which makes the
"stuck in a local optimum" behaviour of hill climbing very visible.
Pass move="2opt" to use 2-opt moves instead: the climbs become stronger
(and slower), and the results get much closer to the 2-opt methods.
"""

import random

from tsp_utils import random_tour, swap_tour, tour_length, two_opt_tour


def _move(tour, i, j, kind):
    return two_opt_tour(tour, i, j) if kind == "2opt" else swap_tour(tour, i, j)


def hill_climb_once(dist, start_tour, rng, move):
    """First-improvement hill climbing from one tour.

    Shuffle all candidate moves, apply the first improving one, repeat;
    stop when a full scan finds nothing better (local optimum).
    """
    n = len(dist)
    tour = start_tour[:]
    cur = tour_length(tour, dist)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    while True:
        rng.shuffle(pairs)
        moved = False
        for i, j in pairs:
            cand = _move(tour, i, j, move)
            length = tour_length(cand, dist)
            if length < cur:
                tour, cur, moved = cand, length, True
                break
        if not moved:
            return tour


def hill_climbing(dist, restarts=50, seed=42, move="swap"):
    """Random-restart hill climbing: keep the best local optimum found.

    `restarts` random starting tours, one climb each. More restarts cost
    more time but raise the chance of hitting a good basin.
    """
    rng = random.Random(seed)
    n = len(dist)
    best = None
    best_len = float("inf")
    for _ in range(restarts):
        tour = hill_climb_once(dist, random_tour(n, rng), rng, move)
        length = tour_length(tour, dist)
        if length < best_len:
            best, best_len = tour, length
    return best
