# AI usage: yes — code and README were produced with AI assistance.
"""Monte Carlo integration for one or many variables."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from numerical import eval_1d, eval_batch, validate_box


@dataclass(frozen=True)
class MCResult:
    """Result of a Monte Carlo integral."""

    value: float
    stderr: float
    n_samples: int
    volume: float


def mc_integral(
    f, low, high, n_samples: int = 1_000_000, seed: int = 42
) -> MCResult:
    """Estimate the n-D integral of ``f`` over ``[low, high]``.

    Samples are drawn uniformly from the box in memory-bounded chunks.  The
    estimate is ``volume * mean(f)`` and ``stderr`` is ``volume * s/sqrt(N)``.
    """
    low_array, high_array = validate_box(low, high)
    n_samples = int(n_samples)
    if n_samples < 2:
        raise ValueError("n_samples must be at least 2")
    n = int(low_array.size)
    volume = float(np.prod(high_array - low_array))
    rng = np.random.default_rng(seed)
    chunk = max(1, 2_000_000 // n)
    total = 0.0
    total_square = 0.0
    done = 0
    while done < n_samples:
        batch = min(chunk, n_samples - done)
        points = rng.uniform(low_array, high_array, size=(batch, n))
        values = eval_batch(f, points)
        total += float(values.sum())
        total_square += float(np.dot(values, values))
        done += batch
    mean = total / n_samples
    variance = max(
        0.0, (total_square - n_samples * mean * mean) / (n_samples - 1)
    )
    stderr = volume * math.sqrt(variance / n_samples)
    return MCResult(
        value=volume * mean,
        stderr=stderr,
        n_samples=n_samples,
        volume=volume,
    )


def mc_integral_1d(
    f, a: float, b: float, n_samples: int = 1_000_000, seed: int = 42
) -> MCResult:
    """One-variable convenience wrapper around the same Monte Carlo estimator."""
    a = float(a)
    b = float(b)
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError("a and b must be finite")
    if b <= a:
        raise ValueError("b must be greater than a")
    n_samples = int(n_samples)
    if n_samples < 2:
        raise ValueError("n_samples must be at least 2")
    rng = np.random.default_rng(seed)
    x = rng.uniform(a, b, size=n_samples)
    values = eval_1d(f, x)
    mean = float(values.mean())
    variance = float(values.var(ddof=1))
    volume = b - a
    return MCResult(
        value=volume * mean,
        stderr=volume * math.sqrt(variance / n_samples),
        n_samples=n_samples,
        volume=volume,
    )
