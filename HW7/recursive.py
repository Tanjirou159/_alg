"""C(n,k) -- non-DP solution: naive recursion.

Recurrence:
    C(n,k) = C(n-1, k-1) + C(n-1, k)
Base cases:
    C(n,0) = 1  and  C(n,n) = 1

Every value is computed from scratch each time it is needed, so the same
subproblems are recomputed over and over again (a combinatorial explosion).

Time:  O(C(n,k))  -- exponential in min(k, n-k)
Space: O(n)       -- recursion stack depth
"""

# Counts how many times comb_recursive is called (for the demo).
_calls = 0


def _reset_calls():
    global _calls
    _calls = 0


def call_count():
    """Number of recursive calls made by the last comb_recursive run."""
    return _calls


def comb_recursive(n: int, k: int) -> int:
    """Return C(n,k) using naive recursion (non-DP)."""
    global _calls
    _calls += 1

    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return comb_recursive(n - 1, k - 1) + comb_recursive(n - 1, k)
