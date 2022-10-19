"""Private functions for some spatial computations."""
from __future__ import annotations

import math
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional

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
    def wrapper(*args, **kwargs):
        return np.float64(func(*args, **kwargs))

    return wrapper


def _solve_quadratic(a: float, b: float, c: float, n_digits: Optional[int] = None) -> np.ndarray:
    """
    Solve a quadratic equation.

    The equation has the form

    .. math:: ax^2 + bx + c = 0

    Parameters
    ----------
    a, b, c : float
        Coefficients of the quadratic equation.
    n_digits : int, optional
        Additional keyword passed to :func:`round` (default None).

    Returns
    -------
    np.ndarray
        Array containing the two solutions to the quadratic.

    Raises
    ------
    ValueError
        If the coefficient `a` is zero.
        If the discriminant is negative.

    Examples
    --------
    >>> from skspatial._functions import _solve_quadratic

    >>> _solve_quadratic(-1, 1, 1).round(3)
    array([ 1.618, -0.618])

    >>> _solve_quadratic(0, 1, 1)
    Traceback (most recent call last):
    ...
    ValueError: The coefficient `a` must be non-zero.

    >>> _solve_quadratic(1, 1, 1)
    Traceback (most recent call last):
    ...
    ValueError: The discriminant must not be negative.

    """
    if n_digits:
        a = round(a, n_digits)
        b = round(b, n_digits)
        c = round(c, n_digits)

    if a == 0:
        raise ValueError("The coefficient `a` must be non-zero.")

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        raise ValueError("The discriminant must not be negative.")

    pm = np.array([-1, 1])  # Array to compute minus/plus.

    X = (-b + pm * math.sqrt(discriminant)) / (2 * a)

    return X


_allclose = np.vectorize(math.isclose)
