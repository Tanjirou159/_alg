"""Exercise 2: solve recurrence equations and report exact / Big O complexity.

Recurrences
1. T(n) =   T(n-1) + 8, T(1) = 1   ->  T(n) = 8n - 7            = O(n)
2. T(n) = 2 T(n-1) + 9, T(1) = 1   ->  T(n) = 10*2^(n-1) - 9    = O(2^n)
3. T(n) = 2 T(n/2) + 1, T(1) = 1   ->  T(n) = 2n - 1            = O(n)
4. T(n) =   T(n/2) + 1, T(1) = 1   ->  T(n) = log2(n) + 1       = O(log n)
"""

import math

RECURRENCES = {
    "T(n) = T(n-1) + 8": {
        "kind": "decrease",
        "factor": 1,
        "add": 8,
        "big_o": "O(n)",
        "closed_form": "8n - 7",
    },
    "T(n) = 2 T(n-1) + 9": {
        "kind": "decrease",
        "factor": 2,
        "add": 9,
        "big_o": "O(2^n)",
        "closed_form": "10 * 2^(n-1) - 9",
    },
    "T(n) = 2 T(n/2) + 1": {
        "kind": "divide",
        "factor": 2,
        "add": 1,
        "big_o": "O(n)",
        "closed_form": "2n - 1",
    },
    "T(n) = T(n/2) + 1": {
        "kind": "divide",
        "factor": 1,
        "add": 1,
        "big_o": "O(log n)",
        "closed_form": "log2(n) + 1",
    },
}


def closed_form_decrease(factor, add, n):
    """Closed form of T(n) = factor * T(n-1) + add, T(1) = 1."""
    if factor == 1:
        return 1 + add * (n - 1)
    return (1 + add) * factor ** (n - 1) - add


def closed_form_divide(factor, add, n):
    """Closed form of T(n) = factor * T(n/2) + add, T(1) = 1, n = 2^k."""
    k = int(math.log2(n))
    if factor == 1:
        return 1 + add * k
    return (1 + add) * n - add


def closed_form(recurrence, n):
    spec = RECURRENCES[recurrence]
    if spec["kind"] == "decrease":
        return closed_form_decrease(spec["factor"], spec["add"], n)
    return closed_form_divide(spec["factor"], spec["add"], n)


def iterative_simulate(recurrence, n):
    """Evaluate the recurrence step by step starting from T(1) = 1."""
    spec = RECURRENCES[recurrence]
    value = 1
    if spec["kind"] == "decrease":
        for m in range(2, n + 1):
            value = spec["factor"] * value + spec["add"]
    else:
        assert n & (n - 1) == 0, "n must be a power of 2 for the divide case"
        m = 1
        while m < n:
            m *= 2
            value = spec["factor"] * value + spec["add"]
    return value


def format_row(recurrence, n):
    exact = closed_form(recurrence, n)
    simulated = iterative_simulate(recurrence, n)
    assert exact == simulated, (
        f"{recurrence} at n={n}: closed form {exact} != simulated {simulated}"
    )
    return (
        f"{recurrence:18s}  T({n:<4d}) = {exact:<9d}  "
        f"{RECURRENCES[recurrence]['big_o']}"
    )


def demo():
    print("Exact values and Big O complexity:\n")
    decrease_n = [1, 2, 3, 4, 5, 8, 16, 32]
    divide_n = [1, 2, 4, 8, 16, 32, 64, 1024]
    for recurrence in RECURRENCES:
        print(f"{recurrence}  ->  Big O: {RECURRENCES[recurrence]['big_o']}")
        print(f"    closed form: T(n) = {RECURRENCES[recurrence]['closed_form']}")
        ns = decrease_n if RECURRENCES[recurrence]["kind"] == "decrease" else divide_n
        print("    " + ", ".join(f"T({n})={closed_form(recurrence, n)}" for n in ns))
        print()


if __name__ == "__main__":
    demo()
