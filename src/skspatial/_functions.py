"""Private functions for some spatial computations."""

import math
from functools import wraps
from typing import Any, Callable

import numpy as np

from skspatial.typing import array_like


def _contains_point(obj: Any, point: array_like, **kwargs: float) -> bool:
    """
    Check if the object contains a point.

    Returns True if the distance from the point to the object is close to zero.

    Parameters
    ----------
    obj: Object
        Spatial object (e.g. Line).
    point : array_like
        Input point.
    kwargs : dict, optional
        Additional keywords passed to :func:`math.isclose`.

    Returns
    -------
    bool
        True if the spatial object contains the input point.

    Notes
    -----
    Setting an absolute tolerance is useful when comparing a value to zero.

    """
    distance = obj.distance_point(point)

    return math.isclose(distance, 0, **kwargs)


def _sum_squares(obj: Any, points: array_like) -> np.float64:
    """Return the sum of squared distances from points to a spatial object."""
    distances_squared = np.apply_along_axis(obj.distance_point, 1, points) ** 2

    return distances_squared.sum()


def _mesh_to_points(X: array_like, Y: array_like, Z: array_like) -> np.ndarray:
    """Convert a mesh into an (N, 3) array of N points."""
    return np.vstack([*map(np.ravel, [X, Y, Z])]).T


def np_float(func: Callable) -> Callable[..., np.float64]:
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
