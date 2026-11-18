# AI usage: yes — code and README were produced with AI assistance.
"""Numerical calculus primitives for the HW11 demos.

The module keeps the numerical core small and reusable:

* :func:`derivative` -- central difference for one variable
* :func:`simpson`    -- composite Simpson rule for one variable
* :func:`gradient`   -- coordinate-wise central differences for n variables
* :func:`eval_1d` / :func:`eval_batch` -- adapt scalar or vectorised callables
* :func:`validate_box` -- common validation for integration boxes
"""

from __future__ import annotations

import math

import numpy as np

_EPS = float(np.finfo(float).eps)


def default_step(x: float) -> float:
    """Return ``eps**(1/3) * max(1, |x|)``, about ``6.06e-6`` for float64."""
    return _EPS ** (1.0 / 3.0) * max(1.0, abs(float(x)))


def _to_scalar(value) -> float:
    """Convert a size-one result to a Python float."""
    array = np.asarray(value, dtype=float)
    if array.size != 1:
        raise ValueError("the function must return one scalar for one point")
    return float(array.reshape(-1)[0])


def derivative(f, x: float, h: float | None = None) -> float:
    """Approximate ``f'(x)`` with the central difference.

    ``h`` defaults to :func:`default_step`; it can be supplied explicitly to
    study the truncation/round-off trade-off.
    """
    x = float(x)
    step = default_step(x) if h is None else float(h)
    if not math.isfinite(step) or step <= 0.0:
        raise ValueError("h must be a positive finite number")
    return (_to_scalar(f(x + step)) - _to_scalar(f(x - step))) / (2.0 * step)


def eval_1d(f, x: np.ndarray) -> np.ndarray:
    """Evaluate a one-variable function on a 1-D array.

    Vectorised functions are evaluated in one call.  Functions that only
    accept a Python float (for example :func:`math.sin`) are evaluated in a
    loop, so both styles work.
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    try:
        values = np.asarray(f(x), dtype=float)
    except (TypeError, ValueError):
        values = None
    if values is not None:
        if values.ndim > 0 and values.size == x.size:
            return values.reshape(-1)
        if values.ndim == 0 and x.size == 1:
            return values.reshape(1)
    return np.array([_to_scalar(f(float(t))) for t in x], dtype=float)


def eval_batch(f, points: np.ndarray) -> np.ndarray:
    """Evaluate ``f`` on points with shape ``(B, n)``.

    A vectorised ``f`` receives the whole ``(B, n)`` array and returns ``B``
    values.  A scalar-style ``f`` (one point per call) is handled by a loop.
    """
    points = np.asarray(points, dtype=float)
    if points.ndim != 2:
        raise ValueError("points must have shape (B, n)")
    count = points.shape[0]
    try:
        values = np.asarray(f(points), dtype=float)
    except (TypeError, ValueError):
        values = None
    if values is not None:
        if values.ndim > 0 and values.size == count:
            return values.reshape(-1)
        if values.ndim == 0 and count == 1:
            return values.reshape(1)
    if points.shape[1] == 1:
        return np.array([_to_scalar(f(float(row[0]))) for row in points], dtype=float)
    return np.array([_to_scalar(f(row)) for row in points], dtype=float)


def validate_box(low, high) -> tuple[np.ndarray, np.ndarray]:
    """Return validated 1-D ``low`` and ``high`` arrays for an n-D box."""
    low_array = np.atleast_1d(np.asarray(low, dtype=float)).reshape(-1)
    high_array = np.atleast_1d(np.asarray(high, dtype=float)).reshape(-1)
    if low_array.size != high_array.size:
        raise ValueError("low and high must have the same length")
    if low_array.size == 0:
        raise ValueError("low and high must not be empty")
    if not (np.isfinite(low_array).all() and np.isfinite(high_array).all()):
        raise ValueError("low and high must be finite")
    if np.any(low_array >= high_array):
        raise ValueError("every low[i] must be less than high[i]")
    return low_array, high_array


def simpson(f, a: float, b: float, n: int = 10_000) -> float:
    """Composite Simpson rule on ``[a, b]`` with ``n`` subintervals.

    ``n`` is rounded up to the next even number when necessary.
    """
    a = float(a)
    b = float(b)
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError("a and b must be finite")
    if b <= a:
        raise ValueError("b must be greater than a")
    n = int(n)
    if n < 2:
        raise ValueError("n must be at least 2")
    if n % 2:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = eval_1d(f, x)
    if y.size != x.size:
        raise ValueError("f returned the wrong number of values")
    h = (b - a) / n
    odd_sum = float(y[1:-1:2].sum())
    even_sum = float(y[2:-1:2].sum())
    return float(h / 3.0 * (y[0] + y[-1] + 4.0 * odd_sum + 2.0 * even_sum))


def gradient(f, x, h: float | None = None) -> np.ndarray:
    """Approximate the gradient of ``f`` with central differences."""
    x = np.asarray(x, dtype=float).reshape(-1)
    if x.size == 0:
        raise ValueError("x must contain at least one coordinate")
    result = np.empty_like(x)
    for index in range(x.size):
        step = default_step(x[index]) if h is None else float(h)
        if not math.isfinite(step) or step <= 0.0:
            raise ValueError("h must be a positive finite number")
        offset = np.zeros_like(x)
        offset[index] = step
        result[index] = (
            _to_scalar(f(x + offset)) - _to_scalar(f(x - offset))
        ) / (2.0 * step)
    return result
