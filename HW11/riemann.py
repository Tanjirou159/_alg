# AI usage: yes — code and README were produced with AI assistance.
"""Riemann integration in n dimensions (midpoint rule)."""

from __future__ import annotations

import numpy as np

from numerical import eval_batch, validate_box

# A hard safety cap for an accidentally huge explicit grid.  The automatic
# choice of m is already bounded by max_points (one million by default).
MAX_GRID_POINTS = 100_000_000


def choose_subdivisions(n: int, max_points: int = 1_000_000) -> int:
    """Return the largest ``m`` such that ``m**n <= max_points``."""
    n = int(n)
    max_points = int(max_points)
    if n < 1:
        raise ValueError("n must be at least 1")
    if max_points < 1:
        raise ValueError("max_points must be at least 1")
    m = max(1, int(max_points ** (1.0 / n)))
    while (m + 1) ** n <= max_points:
        m += 1
    while m ** n > max_points:
        m -= 1
    return m


def _cell_centres(low, h, m, n, start, stop):
    """Cell centres for flat cell indices ``start:stop``.

    Mixed-radix decoding avoids creating an n-dimensional NumPy array:
    NumPy supports at most 64 array dimensions, while n can be 100 here.
    """
    flat = np.arange(start, stop, dtype=np.int64)
    quotient = flat.copy()
    digits = np.empty((flat.size, n), dtype=float)
    for axis in range(n):
        digits[:, axis] = quotient % m
        quotient //= m
    return low + (digits + 0.5) * h


def integral(f, low, high, subdiv=None, max_points: int = 1_000_000) -> float:
    """Integrate ``f`` over the n-D box ``[low, high]`` with a midpoint rule.

    Parameters
    ----------
    f:
        Callable evaluated on an ``(B, n)`` array of points.  It should return
        ``B`` values; :func:`numerical.eval_batch` also supports functions that
        only accept one point per call.
    low, high:
        Box corners; both must be 1-D arrays (or scalars) of length n.
    subdiv:
        Optional number of cells per axis.  When omitted, the largest m with
        ``m**n <= max_points`` is used.
    max_points:
        Evaluation budget for the automatic choice of ``m``.

    Returns
    -------
    float
        ``(product of cell widths) * sum(f(centres))``.
    """
    low_array, high_array = validate_box(low, high)
    n = int(low_array.size)
    m = choose_subdivisions(n, max_points) if subdiv is None else int(subdiv)
    if m < 1:
        raise ValueError("subdiv must be at least 1")
    total = m ** n
    if total > MAX_GRID_POINTS:
        raise ValueError(
            f"the grid has {total} points ({m} per axis in {n} dimensions); "
            f"the safety limit is {MAX_GRID_POINTS}. "
            "Use a smaller subdiv or a smaller max_points."
        )
    h = (high_array - low_array) / float(m)
    cell_volume = float(np.prod(h))
    chunk = max(1, 2_000_000 // n)
    total_sum = 0.0
    for start in range(0, total, chunk):
        stop = min(start + chunk, total)
        points = _cell_centres(low_array, h, m, n, start, stop)
        total_sum += float(np.sum(eval_batch(f, points)))
    return cell_volume * total_sum
