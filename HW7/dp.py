"""C(n,k) -- DP solution: bottom-up Pascal's triangle with a rolling array.

Idea:
    Row i of Pascal's triangle holds C(i, 0), C(i, 1), ..., C(i, i).
    Row i is built from row i-1 with the same recurrence, but each
    subproblem is computed EXACTLY ONCE and stored for reuse.

    dp[j] = C(i, j) after row i has been processed.

    We only keep one row at a time (a rolling array), and thanks to the
    symmetry C(n,k) = C(n,n-k) we only need columns up to min(k, n-k).

The update runs j from right to left so that dp[j-1] still holds the
value from the PREVIOUS row when it is read.

Time:  O(n*k)
Space: O(k)
"""


def comb_dp(n: int, k: int) -> int:
    """Return C(n,k) using bottom-up dynamic programming."""
    if k < 0 or k > n:
        return 0

    # Symmetry: C(n,k) = C(n,n-k). Use the smaller one to do less work.
    k = min(k, n - k)

    # dp[j] will hold C(i, j) for the current row i.
    dp = [0] * (k + 1)
    dp[0] = 1  # row 0: C(0,0) = 1

    for i in range(1, n + 1):
        # Columns only go up to min(i, k); update right-to-left.
        for j in range(min(i, k), 0, -1):
            dp[j] = dp[j] + dp[j - 1]

    return dp[k]
