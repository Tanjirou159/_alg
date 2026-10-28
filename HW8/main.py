"""TSP: run the five algorithms on the same instance and compare them.

Usage:
    python main.py                          # 20 random cities, all methods
    python main.py --n 8 --optimal          # small case + brute-force optimum
    python main.py --n 50 --restarts 200 --anneal-iters 40000
    python main.py --seed 7 --csv tour.csv
"""

import argparse
import time

from tsp_utils import (brute_force, distance_matrix, generate_cities,
                       is_valid_tour, nearest_neighbour, tour_length)
from greedy import greedy_all_starts
from improvement import two_opt_improve
from hill_climbing import hill_climbing
from simulated_annealing import simulated_annealing
from gradient_descent import gradient_descent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=20, help="number of cities")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for the cities")
    ap.add_argument("--restarts", type=int, default=50,
                    help="hill-climbing random restarts")
    ap.add_argument("--anneal-iters", type=int, default=20000,
                    help="simulated-annealing iterations")
    ap.add_argument("--t0", type=float, default=100.0,
                    help="simulated-annealing start temperature")
    ap.add_argument("--tmin", type=float, default=0.01,
                    help="simulated-annealing final temperature")
    ap.add_argument("--single-start", action="store_true",
                    help="greedy: use one start (city 0) instead of all starts")
    ap.add_argument("--optimal", action="store_true",
                    help="also run brute force (only for n <= 11)")
    ap.add_argument("--csv", metavar="FILE", help="write cities + best tour to CSV")
    args = ap.parse_args()

    cities = generate_cities(args.n, args.seed)
    dist = distance_matrix(cities)
    print(f"TSP instance: n = {args.n} cities, seed = {args.seed}")

    # (method name, tour) collected for the comparison table
    results = []

    def run(name, fn, *fn_args):
        t0 = time.perf_counter()
        tour = fn(dist, *fn_args)
        secs = time.perf_counter() - t0
        assert is_valid_tour(tour, args.n), f"{name}: invalid tour!"
        results.append((name, tour, secs))
        return tour

    if args.single_start:
        greedy_tour = run("greedy (single start)", nearest_neighbour)
    else:
        greedy_tour = run("greedy (all starts)", greedy_all_starts)
    # classic pipeline: build a tour with greedy, then improve it
    run("improvement (2-opt, first)", two_opt_improve, greedy_tour)
    run("hill climbing", hill_climbing, args.restarts, args.seed)
    run("simulated annealing", simulated_annealing, None,
        args.anneal_iters, args.t0, args.tmin, args.seed)
    run("gradient descent (steepest)", gradient_descent, greedy_tour)

    opt_len = None
    opt_secs = None
    if args.optimal:
        if args.n > 11:
            import math
            tours = math.factorial(args.n - 1) if args.n < 60 else "huge"
            print(f"note: --optimal skipped, n = {args.n} is too large for "
                  f"brute force (needs {tours} tours)")
        else:
            t0 = time.perf_counter()
            _, opt_len = brute_force(dist)
            opt_secs = time.perf_counter() - t0

    ref = opt_len if opt_len is not None else min(r[1] and tour_length(r[1], dist) for r in results)
    ref_name = "optimal" if opt_len is not None else "best found"

    print(f"\n{'method':<28} {'length':>12} {'time (s)':>10} {'gap':>9}")
    print("-" * 63)
    for name, tour, secs in results:
        length = tour_length(tour, dist)
        gap = (length - ref) / ref * 100.0
        print(f"{name:<28} {length:>12.2f} {secs:>10.4f} {gap:>8.2f}%")
    if opt_len is not None:
        print(f"{'optimal (brute force)':<28} {opt_len:>12.2f} {opt_secs:>10.4f} {'--':>9}")

    print(f"\ngap is measured against: {ref_name} = {ref:.2f}")

    if args.csv:
        best_name, best_tour, _ = min(
            results, key=lambda r: tour_length(r[1], dist))
        with open(args.csv, "w", encoding="utf-8") as f:
            f.write("index,x,y,order\n")
            for pos, city in enumerate(best_tour):
                x, y = cities[city]
                f.write(f"{city},{x},{y},{pos}\n")
        print(f"\nbest tour ({best_name}) written to {args.csv}")


if __name__ == "__main__":
    main()
