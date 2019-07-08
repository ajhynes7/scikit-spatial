"""Private functions for some spatial computations."""

from typing import Sequence

import numpy as np


def _contains_point(self, point: Sequence, **kwargs) -> bool:
    """Check if the object contains a point."""
    distance = self.distance_point(point)

    return np.isclose(distance, 0, **kwargs)


def _sum_squares(self, points: Sequence) -> np.float64:

    distances_squared = np.apply_along_axis(self.distance_point, 1, points) ** 2

    return distances_squared.sum()
