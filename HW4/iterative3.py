"""
iterative3.py
-------------
Solves f(x) = x^3 - x - 2 = 0 using Newton-Raphson iteration
by importing and invoking the general framework in `iter_framework.py`.
"""

from iter_framework import solve_iterative


def f(x: float) -> float:
    """Target function f(x)."""
    return x**3 - x - 2


def df(x: float) -> float:
    """First derivative f'(x)."""
    return 3 * (x**2) - 1


def newton_step(x: float) -> float:
    """
    Newton-Raphson update step g(x) = x - f(x)/f'(x).
    """
    derivative = df(x)
    if abs(derivative) < 1e-12:
        raise ZeroDivisionError("Derivative near zero. Newton iteration undefined.")
    return x - f(x) / derivative


def main():
    print("==================================================")
    print("   Problem Solver: Root Finding via Newton-Raphson")
    print("   Target Equation: f(x) = x^3 - x - 2 = 0")
    print("==================================================\n")

    initial_guess = 1.5
    tolerance = 1e-8
    max_steps = 50

    # Invoke generic framework solver
    result = solve_iterative(
        step_func=newton_step,
        x0=initial_guess,
        tol=tolerance,
        max_iter=max_steps,
        criterion="absolute",
        verbose=True
    )

    # Print Final Summary
    print("\n=== Execution Summary ===")
    print(f"Converged Solution (x*) : {result['solution']:.10f}")
    print(f"Residual Value f(x*)    : {f(result['solution']):.10e}")
    print(f"Total Iteration Count   : {result['iterations']}")
    print(f"Convergence Achieved    : {result['converged']}")


if __name__ == "__main__":
    main()