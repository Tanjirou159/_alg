"""TSP method 2: improvement method (改良法), aka 2-opt.

Start from an existing tour (here: the greedy tour) and repeatedly apply
the *first* 2-opt move found that shortens it, rescanning from the top
each time, until a full scan finds nothing better. Fully deterministic.

A 2-opt move picks two positions i < j and reverses the segment between
them. In the Euclidean plane this removes crossings: any tour that
crosses itself can always be shortened, so the final tour is crossing
free.

Contrast with `gradient_descent.py`: the improvement method takes the
first downhill move it sees, while gradient descent evaluates *all*
moves (the full finite-difference gradient) and takes the steepest one.
"""

from tsp_utils import nearest_neighbour, tour_length, two_opt_tour


def two_opt_improve(dist, init=None):
    """First-improvement 2-opt local search (classic TSP improvement).

    Time: each full scan checks O(n^2) moves at O(n) each = O(n^3);
    usually only a few scans are needed.
    """
    tour = list(init) if init is not None else nearest_neighbour(dist)
    n = len(dist)
    while True:
        cur = tour_length(tour, dist)
        moved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                cand = two_opt_tour(tour, i, j)
                if tour_length(cand, dist) < cur:   # first improvement
                    tour = cand
                    moved = True
                    break
            if moved:
                break
        if not moved:                  # full scan found nothing -> done
            return tour
