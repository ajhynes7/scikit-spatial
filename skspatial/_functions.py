"""Private functions for some spatial computations."""

from typing import Any, Sequence
from functools import wraps
from typing import Any, Callable, Sequence

import numpy as np


def _contains_point(obj: Any, point: Sequence, **kwargs: float) -> bool:
    """Check if the object contains a point."""
    distance = obj.distance_point(point)

    return np.isclose(distance, 0, **kwargs)


def _sum_squares(obj: Any, points: Sequence) -> np.float64:

    distances_squared = np.apply_along_axis(obj.distance_point, 1, points) ** 2

    return distances_squared.sum()


def _mesh_to_points(X: Sequence, Y: Sequence, Z: Sequence) -> np.ndarray:
    """Convert a mesh into an (N, 3) array of N points."""
    return np.vstack([*map(np.ravel, [X, Y, Z])]).T


def np_float(func) -> Callable[..., np.float64]:
    """
    Cast the output type as np.float64.

    Outputs with type np.float64 have a useful round() method.

    """
    # wraps() is needed so that sphinx generates
    # the docstring of functions with this decorator.
    @wraps(func)
    def wrapper(*args):
        return np.float64(func(*args))

    return wrapper


_allclose = np.vectorize(math.isclose)
