"""TSP method 4: simulated annealing (模擬退火法).

Hill climbing that is allowed to *worsen* the tour with probability
exp(-delta / T) (the Metropolis criterion). The temperature T starts
high and cools geometrically toward tmin, so early on the search jumps
freely across the landscape and later settles into a deep local optimum.
The best tour seen along the whole walk is remembered and returned.
"""

import math
import random

from tsp_utils import random_tour, tour_length, two_opt_tour


def simulated_annealing(dist, init=None, iters=20000, t0=100.0,
                        tmin=0.01, seed=42):
    """Metropolis simulated annealing with 2-opt moves.

    Parameters
    ----------
    iters : number of attempted moves
    t0    : starting temperature
    tmin  : final temperature (cooling is geometric: t = t0 * alpha**k)
    """
    rng = random.Random(seed)
    n = len(dist)
    tour = list(init) if init is not None else random_tour(n, rng)
    cur = tour_length(tour, dist)
    best, best_len = tour[:], cur
    if n < 4:          # no nontrivial 2-opt move exists for n <= 3
        return best

    alpha = (tmin / t0) ** (1.0 / iters)   # geometric cooling schedule
    t = t0
    for _ in range(iters):
        i = rng.randrange(n - 2)
        j = rng.randrange(i + 2, n)        # any valid 2-opt move
        cand = two_opt_tour(tour, i, j)
        length = tour_length(cand, dist)
        delta = length - cur
        # Metropolis criterion: always take improvements, sometimes take
        # worse moves -- more often when hot, almost never when cold.
        if delta < 0 or rng.random() < math.exp(-delta / t):
            tour, cur = cand, length
            if cur < best_len:
                best, best_len = tour[:], cur
        t *= alpha
    return best
