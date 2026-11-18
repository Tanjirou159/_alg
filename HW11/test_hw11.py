# AI usage: yes — code and README were produced with AI assistance.
"""Unit tests for HW11."""

from __future__ import annotations

import math
import unittest

import numpy as np

from monte_carlo import mc_integral, mc_integral_1d
from numerical import derivative, gradient, simpson
from riemann import choose_subdivisions, integral


def square(x):
    return x * x


def sum_of_squares(points):
    return np.sum(np.asarray(points, dtype=float) ** 2, axis=-1)


class TestDerivative(unittest.TestCase):
    def test_quadratic(self):
        for x in (0.5, 1.0, 3.0):
            self.assertAlmostEqual(derivative(square, x), 2.0 * x, places=8)

    def test_sine(self):
        self.assertAlmostEqual(
            derivative(math.sin, 0.5), math.cos(0.5), places=8
        )

    def test_invalid_step(self):
        with self.assertRaises(ValueError):
            derivative(square, 1.0, h=0.0)


class TestSimpson(unittest.TestCase):
    def test_quadratic_is_exact(self):
        self.assertAlmostEqual(
            simpson(square, 0.0, 1.0), 1.0 / 3.0, places=12
        )

    def test_scalar_only_function(self):
        self.assertAlmostEqual(
            simpson(math.sin, 0.0, math.pi, n=1000), 2.0, places=9
        )

    def test_odd_interval_count(self):
        self.assertAlmostEqual(
            simpson(square, 0.0, 1.0, n=999), 1.0 / 3.0, places=12
        )

    def test_invalid_interval(self):
        with self.assertRaises(ValueError):
            simpson(square, 1.0, 0.0)


class TestGradient(unittest.TestCase):
    def test_gradient(self):
        for n in (1, 2, 5):
            point = np.arange(1, n + 1, dtype=float) / (n + 1)
            value = gradient(sum_of_squares, point)
            np.testing.assert_allclose(value, 2.0 * point, atol=1e-8)

    def test_invalid_point(self):
        with self.assertRaises(ValueError):
            gradient(sum_of_squares, [])


class TestRiemann(unittest.TestCase):
    def test_subdivision_choice(self):
        self.assertEqual(choose_subdivisions(1), 1_000_000)
        self.assertEqual(choose_subdivisions(2), 1_000)
        self.assertEqual(choose_subdivisions(5), 15)
        self.assertEqual(choose_subdivisions(100), 1)

    def test_1d(self):
        value = integral(square, [0.0], [1.0])
        self.assertLess(abs(value - 1.0 / 3.0), 1e-9)

    def test_2d(self):
        value = integral(sum_of_squares, [0.0, 0.0], [1.0, 1.0])
        self.assertLess(abs(value - 2.0 / 3.0), 1e-5)

    def test_5d(self):
        value = integral(sum_of_squares, [0.0] * 5, [1.0] * 5)
        self.assertLess(
            abs(value - 5.0 / 3.0) / (5.0 / 3.0), 5e-3
        )

    def test_100d_single_cell(self):
        value = integral(sum_of_squares, np.zeros(100), np.ones(100))
        self.assertAlmostEqual(value, 25.0, places=12)

    def test_scalar_function_fallback(self):
        def scalar_f(point):
            return point[0] ** 2 + point[1] ** 2

        value = integral(
            scalar_f, [0.0, 0.0], [1.0, 1.0], subdiv=100
        )
        self.assertLess(abs(value - 2.0 / 3.0), 1e-4)

    def test_invalid_box(self):
        with self.assertRaises(ValueError):
            integral(square, [1.0], [0.0])
        with self.assertRaises(ValueError):
            integral(square, [0.0, 0.0], [1.0])


class TestMonteCarlo(unittest.TestCase):
    def test_1d(self):
        result = mc_integral_1d(
            square, 0.0, 1.0, n_samples=200_000, seed=42
        )
        self.assertLess(
            abs(result.value - 1.0 / 3.0), 5.0 * result.stderr
        )

    def test_1d_scalar_only_function(self):
        result = mc_integral_1d(
            math.sin, 0.0, math.pi, n_samples=200_000, seed=7
        )
        self.assertLess(abs(result.value - 2.0), 5.0 * result.stderr)

    def test_100d(self):
        result = mc_integral(
            sum_of_squares,
            np.zeros(100),
            np.ones(100),
            n_samples=200_000,
            seed=42,
        )
        self.assertLess(
            abs(result.value - 100.0 / 3.0), 5.0 * result.stderr
        )

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            mc_integral_1d(square, 1.0, 0.0)
        with self.assertRaises(ValueError):
            mc_integral(square, [0.0], [1.0], n_samples=1)


if __name__ == "__main__":
    unittest.main()
