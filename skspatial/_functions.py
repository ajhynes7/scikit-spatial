"""Private functions for some spatial computations."""

from typing import Any, Sequence

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
