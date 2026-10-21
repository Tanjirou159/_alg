"""C(n,k): recursion (non-DP) vs dynamic programming -- runner.

Usage:
    python main.py n k           compute C(n,k) both ways and verify
    python main.py --bench N     benchmark both up to n = N, k = n//2

Both results are checked against Python's math.comb.
"""

import argparse
import math
import time

from dp import comb_dp
from recursive import comb_recursive, call_count, _reset_calls


def run_one(n: int, k: int) -> None:
    expected = math.comb(n, k)

    _reset_calls()
    t0 = time.perf_counter()
    r = comb_recursive(n, k)
    t1 = time.perf_counter()
    d = comb_dp(n, k)
    t2 = time.perf_counter()

    print(f"C({n},{k}) = {expected}")
    print(f"  recursive (non-DP): {r}")
    print(f"    calls  : {call_count()}")
    print(f"    time   : {t1 - t0:.6f} s")
    print(f"  DP (rolling array): {d}")
    print(f"    time   : {t2 - t1:.6f} s")

    ok_r = r == expected
    ok_d = d == expected
    print(f"  correctness: recursive {'OK' if ok_r else 'FAIL'}, "
          f"DP {'OK' if ok_d else 'FAIL'}")


def bench(max_n: int) -> None:
    print(f"{'n':>4} {'k':>4} | {'recursive s':>12} {'DP s':>12} {'calls':>12}")
    print("-" * 52)
    for n in range(5, max_n + 1):
        k = n // 2  # worst case for the naive recursion

        _reset_calls()
        t0 = time.perf_counter()
        comb_recursive(n, k)
        t1 = time.perf_counter()
        comb_dp(n, k)
        t2 = time.perf_counter()

        print(f"{n:>4} {k:>4} | {t1 - t0:>12.6f} {t2 - t1:>12.6f} "
              f"{call_count():>12}")


def main() -> None:
    parser = argparse.ArgumentParser(description="C(n,k): recursion vs DP")
    parser.add_argument("n", nargs="?", type=int, help="total items n")
    parser.add_argument("k", nargs="?", type=int, help="items chosen k")
    parser.add_argument("--bench", type=int, metavar="N",
                        help="benchmark up to n = N instead")
    args = parser.parse_args()

    if args.bench is not None:
        bench(args.bench)
    elif args.n is not None and args.k is not None:
        run_one(args.n, args.k)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
