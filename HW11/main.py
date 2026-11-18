# AI usage: yes — code and README were produced with AI assistance.
"""Demo runner for HW11: numerical calculus and Monte Carlo integration."""

from __future__ import annotations

import argparse
import platform
import time

import numpy as np

from monte_carlo import mc_integral, mc_integral_1d
from numerical import derivative, gradient, simpson
from riemann import choose_subdivisions, integral


def square(x):
    return x * x


def sum_of_squares(points):
    return np.sum(np.asarray(points, dtype=float) ** 2, axis=-1)


def exact_integral(n: int) -> float:
    return n / 3.0


def time_call(function):
    start = time.perf_counter()
    value = function()
    return value, time.perf_counter() - start


def print_derivative_demo() -> None:
    print("\n1. Single-variable numerical derivative")
    print("   f(x) = x^2, central difference, h = eps^(1/3) * max(1, |x|)")
    print(
        f"   {'x':>5} {'exact':>14} {'numerical':>16} "
        f"{'abs error':>12} {'rel error':>12}"
    )
    for x in (0.5, 1.0, 2.0, 3.0):
        exact = 2.0 * x
        value = derivative(square, x)
        abs_error = abs(value - exact)
        rel_error = abs_error / abs(exact)
        print(
            f"   {x:5.1f} {exact:14.10f} {value:16.10f} "
            f"{abs_error:12.3e} {rel_error:12.3e}"
        )

    print("\n   h sweep at x = 3 for f(x) = exp(x):")
    print(f"   {'h':>10} {'numerical':>18} {'abs error':>12}")
    for h in (1e-3, 1e-5, 1e-6, 1e-7, 1e-9):
        value = derivative(np.exp, 3.0, h=h)
        print(f"   {h:10.1e} {value:18.10f} {abs(value - np.exp(3.0)):12.3e}")


def print_single_integral_demo(samples: int, points: int, seed: int) -> None:
    print("\n2. Single-variable numerical integration")
    print("   f(x) = x^2 on [0, 1], exact = 1/3")
    exact = 1.0 / 3.0

    simpson_value, simpson_time = time_call(lambda: simpson(square, 0.0, 1.0))
    riemann_value, riemann_time = time_call(
        lambda: integral(square, [0.0], [1.0], max_points=points)
    )
    mc_result, mc_time = time_call(
        lambda: mc_integral_1d(square, 0.0, 1.0, n_samples=samples, seed=seed)
    )

    simpson_name = "Simpson (n=10,000)"
    riemann_name = f"Riemann midpoint (m={points:,})"
    mc_name = f"Monte Carlo (N={samples:,})"

    print(
        f"   {'method':<32} {'estimate':>18} {'abs error':>12} "
        f"{'rel error':>12} {'time (s)':>10}"
    )
    for name, value, elapsed in (
        (simpson_name, simpson_value, simpson_time),
        (riemann_name, riemann_value, riemann_time),
    ):
        print(
            f"   {name:<32} {value:18.12f} {abs(value - exact):12.3e} "
            f"{abs(value - exact) / exact:12.3e} {elapsed:10.4f}"
        )
    print(
        f"   {mc_name:<32} {mc_result.value:18.12f} "
        f"{abs(mc_result.value - exact):12.3e} "
        f"{abs(mc_result.value - exact) / exact:12.3e} {mc_time:10.4f}"
    )
    print(f"   Monte Carlo standard error: {mc_result.stderr:.3e}")


def print_gradient_demo(dims) -> None:
    print("\n3. n-D numerical gradient")
    print("   f(x) = sum(x_i^2), x_i = (i+1)/(n+1), exact gradient = 2x")
    print(
        f"   {'n':>4} {'max abs error':>15} {'max rel error':>15} "
        f"{'f evals':>8} {'time (s)':>10}"
    )
    for n in dims:
        point = np.arange(1, n + 1, dtype=float) / (n + 1)
        value, elapsed = time_call(
            lambda point=point: gradient(sum_of_squares, point)
        )
        exact = 2.0 * point
        abs_error = float(np.max(np.abs(value - exact)))
        rel_error = float(np.max(np.abs(value - exact) / np.abs(exact)))
        print(
            f"   {n:4d} {abs_error:15.3e} {rel_error:15.3e} "
            f"{2 * n:8d} {elapsed:10.4f}"
        )


def print_riemann_demo(dims, points: int) -> None:
    print("\n4. n-D Riemann integral (midpoint rule)")
    print("   f(x) = sum(x_i^2) on [0, 1]^n, exact = n/3")
    print(
        f"   {'n':>4} {'m':>8} {'grid points':>14} {'estimate':>16} "
        f"{'exact':>16} {'rel error':>12} {'time (s)':>10}"
    )
    for n in dims:
        low = np.zeros(n)
        high = np.ones(n)
        m = choose_subdivisions(n, max_points=points)
        value, elapsed = time_call(
            lambda low=low, high=high: integral(
                sum_of_squares, low, high, max_points=points
            )
        )
        exact = exact_integral(n)
        print(
            f"   {n:4d} {m:8d} {m ** n:14d} {value:16.10f} {exact:16.10f} "
            f"{abs(value - exact) / exact:12.3e} {elapsed:10.4f}"
        )


def print_monte_carlo_demo(dims, samples: int, seed: int) -> None:
    print("\n5. n-D Monte Carlo integral")
    print("   f(x) = sum(x_i^2) on [0, 1]^n, exact = n/3")
    print(
        f"   {'n':>4} {'samples':>10} {'estimate':>16} {'exact':>16} "
        f"{'stderr':>12} {'rel error':>12} {'time (s)':>10}"
    )
    for n in dims:
        low = np.zeros(n)
        high = np.ones(n)
        result, elapsed = time_call(
            lambda low=low, high=high: mc_integral(
                sum_of_squares, low, high, n_samples=samples, seed=seed
            )
        )
        exact = exact_integral(n)
        print(
            f"   {n:4d} {samples:10,d} {result.value:16.10f} {exact:16.10f} "
            f"{result.stderr:12.3e} {abs(result.value - exact) / exact:12.3e} "
            f"{elapsed:10.4f}"
        )


def print_convergence_demo(quick: bool, seed: int) -> None:
    print("\n6. Convergence checks")

    print("\n   Riemann midpoint in 2-D (f = x1^2 + x2^2), error should fall ~4x")
    print(
        f"   {'m':>6} {'grid points':>12} {'estimate':>16} "
        f"{'abs error':>12} {'ratio':>8}"
    )
    exact_2d = exact_integral(2)
    previous = None
    for m in (10, 20, 40, 100, 200):
        value = integral(
            sum_of_squares, [0.0, 0.0], [1.0, 1.0], subdiv=m
        )
        error = abs(value - exact_2d)
        ratio_text = f"{'-':>8}" if previous is None else f"{previous / error:8.2f}"
        print(
            f"   {m:6d} {m * m:12d} {value:16.10f} {error:12.3e} "
            f"{ratio_text}"
        )
        previous = error

    print("\n   Monte Carlo in 100-D (f = sum x_i^2), error ~ 1/sqrt(N)")
    print(
        f"   {'N':>10} {'estimate':>16} {'abs error':>12} "
        f"{'stderr':>12} {'|err|/stderr':>13}"
    )
    exact_100d = exact_integral(100)
    low = np.zeros(100)
    high = np.ones(100)
    sample_counts = (
        (100, 400, 1600, 6400)
        if quick
        else (1_000, 10_000, 100_000, 1_000_000)
    )
    for n_samples in sample_counts:
        result = mc_integral(
            sum_of_squares, low, high, n_samples=n_samples, seed=seed
        )
        error = abs(result.value - exact_100d)
        print(
            f"   {n_samples:10,d} {result.value:16.10f} {error:12.3e} "
            f"{result.stderr:12.3e} {error / result.stderr:13.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Numerical differentiation/integration and Monte Carlo "
            "integration in n dimensions."
        )
    )
    parser.add_argument(
        "--dims",
        type=int,
        nargs="+",
        default=[1, 2, 5, 100],
        help="dimensions to test (default: 1 2 5 100)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=1_000_000,
        help="Monte Carlo samples (default: 1000000)",
    )
    parser.add_argument(
        "--points",
        type=int,
        default=1_000_000,
        help="Riemann grid budget (default: 1000000)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="random seed (default: 42)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="use 10,000 samples/points for a fast run",
    )
    args = parser.parse_args()

    if args.quick:
        args.samples = 10_000
        args.points = 10_000

    if any(n < 1 for n in args.dims):
        parser.error("--dims values must be positive")
    if args.samples < 2:
        parser.error("--samples must be at least 2")
    if args.points < 1:
        parser.error("--points must be at least 1")

    print("HW11 - Numerical differentiation/integration and Monte Carlo")
    print(f"Python {platform.python_version()}, NumPy {np.__version__}")
    print(
        f"dimensions={args.dims}, samples={args.samples:,}, "
        f"Riemann budget={args.points:,}, seed={args.seed}"
    )

    print_derivative_demo()
    print_single_integral_demo(args.samples, args.points, args.seed)
    print_gradient_demo(args.dims)
    print_riemann_demo(args.dims, args.points)
    print_monte_carlo_demo(args.dims, args.samples, args.seed)
    print_convergence_demo(args.quick, args.seed)


if __name__ == "__main__":
    main()
