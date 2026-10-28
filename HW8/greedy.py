"""TSP method 1: greedy algorithm (貪婪演算法).

Always travel to the closest unvisited city. Simple and fast, but every
choice is local and the tour is never repaired later, so the result can
be far from optimal.
"""

from tsp_utils import nearest_neighbour, tour_length


def greedy(dist, start=0):
    """Nearest-neighbour tour starting at city `start`. O(n^2) time."""
    return nearest_neighbour(dist, start)


def greedy_all_starts(dist):
    """Run nearest neighbour from every city and keep the best tour.

    O(n) starts x O(n^2) each = O(n^3) time -- still cheap, and it
    removes most of the bad luck of a single fixed start.
    """
    best = None
    best_len = float("inf")
    for s in range(len(dist)):
        tour = greedy(dist, s)
        length = tour_length(tour, dist)
        if length < best_len:
            best, best_len = tour, length
    return best
