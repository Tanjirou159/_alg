"""TSP method 5: gradient descent (梯度下降法), adapted to a discrete problem.

Classic gradient descent updates  x <- x - lr * grad f(x)  on a
*continuous* function f. A tour, however, is a permutation -- a discrete
object -- so the ordinary derivative of the tour length E does not exist.

We use the standard discrete analogue of the gradient:

  * the possible "directions" from a tour are the 2-opt moves
    (reversing a segment between two positions);
  * the directional derivative of E along a direction is the finite
    difference  E(moved tour) - E(tour);
  * evaluating all O(n^2) directions gives the full finite-difference
    gradient;
  * a gradient-descent step moves along the most negative direction
    (steepest descent), with step size = one move.

The process stops when every directional derivative is >= 0, i.e. when
the tour is a local minimum of the 2-opt neighbourhood. That is exactly
the continuous stopping condition  grad f = 0.

Contrast with `improvement.py`: the improvement method applies the first
downhill move it finds; gradient descent computes the entire gradient
first and then steps in the steepest descent direction.
"""

from tsp_utils import nearest_neighbour, tour_length, two_opt_tour


def two_opt_gradient(tour, dist):
    """Finite-difference gradient of E over all 2-opt directions.

    Returns {(i, j): delta} where delta = E(2-opt(i,j) applied) - E(tour).
    A negative delta means "E decreases in this direction".
    """
    n = len(dist)
    cur = tour_length(tour, dist)
    grad = {}
    for i in range(n - 1):
        for j in range(i + 2, n):
            cand = two_opt_tour(tour, i, j)
            grad[(i, j)] = tour_length(cand, dist) - cur
    return grad


def gradient_descent(dist, init=None):
    """Steepest descent on the finite-difference gradient.

    Each iteration evaluates the whole gradient (O(n^3): n^2/2 directions
    x O(n) evaluation) and applies the move with the most negative delta.
    Stops at a local minimum of the 2-opt neighbourhood.

    The step size is fixed at one move per iteration; a "learning rate"
    has no natural meaning on a discrete set, which is itself an
    interesting difference from continuous gradient descent.
    """
    tour = list(init) if init is not None else nearest_neighbour(dist)
    n = len(dist)
    while True:
        cur = tour_length(tour, dist)
        best_delta = 0.0
        best_move = None
        for i in range(n - 1):
            for j in range(i + 2, n):
                cand = two_opt_tour(tour, i, j)
                delta = tour_length(cand, dist) - cur
                if delta < best_delta:
                    best_delta, best_move = delta, (i, j)
        if best_move is None:      # grad >= 0 in every direction
            return tour
        tour = two_opt_tour(tour, *best_move)
