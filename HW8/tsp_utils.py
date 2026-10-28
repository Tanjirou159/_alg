"""Shared helpers for the five TSP solvers in HW8.

Traveling Salesman Problem (TSP): given n cities in the plane, find the
shortest closed tour that visits every city exactly once and returns to
the start.

A tour is represented as a list of city indices, e.g. [0, 3, 1, 2] means
0 -> 3 -> 1 -> 2 -> 0.
"""

import itertools
import math
import random


def generate_cities(n, seed=42, box=100.0):
    """Return n random (x, y) city coordinates in a box x box square."""
    rng = random.Random(seed)
    return [(round(rng.uniform(0.0, box), 4), round(rng.uniform(0.0, box), 4))
            for _ in range(n)]


def distance_matrix(cities):
    """n x n symmetric matrix of Euclidean distances between cities."""
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = cities[i]
        for j in range(i + 1, n):
            xj, yj = cities[j]
            d = math.hypot(xj - xi, yj - yi)
            dist[i][j] = dist[j][i] = d
    return dist


def tour_length(tour, dist):
    """Length of the closed tour (includes the edge last -> first)."""
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))


def is_valid_tour(tour, n):
    """True if tour is a permutation of 0..n-1."""
    return len(tour) == n and set(tour) == set(range(n))


def swap_tour(tour, i, j):
    """Copy of tour with the cities at positions i and j exchanged."""
    t = tour[:]
    t[i], t[j] = t[j], t[i]
    return t


def two_opt_tour(tour, i, j):
    """2-opt move: reverse the segment tour[i+1 .. j] (requires i < j).

    Reversing a segment keeps the tour valid but replaces two edges with
    two others; in the Euclidean plane this removes crossings.
    """
    return tour[: i + 1] + tour[i + 1: j + 1][::-1] + tour[j + 1:]


def random_tour(n, rng):
    """A uniformly random permutation of 0..n-1."""
    t = list(range(n))
    rng.shuffle(t)
    return t


def nearest_neighbour(dist, start=0):
    """Greedy construction: from the current city, always visit the
    closest unvisited city. O(n^2) time."""
    n = len(dist)
    unvisited = set(range(n))
    unvisited.discard(start)
    tour = [start]
    cur = start
    while unvisited:
        nxt = min(unvisited, key=lambda v: dist[cur][v])
        tour.append(nxt)
        unvisited.discard(nxt)
        cur = nxt
    return tour


def brute_force(dist):
    """Exact optimum by enumerating all (n-1)! tours (city 0 fixed first).

    Only practical for n <= 11: (11-1)! = 3.6 million tours.
    """
    n = len(dist)
    best_tour = None
    best_len = math.inf
    for perm in itertools.permutations(range(1, n)):
        tour = (0,) + perm
        length = tour_length(tour, dist)
        if length < best_len:
            best_len = length
            best_tour = list(tour)
    return best_tour, best_len
