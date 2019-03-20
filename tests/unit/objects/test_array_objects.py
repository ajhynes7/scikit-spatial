"""Test functionality of objects based on a single 1D NumPy array (Point and Vector)."""

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Point, Vector


@pytest.mark.parametrize(
    "array", [[1, 0], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
)
def test_equality(array):

    assert_array_equal(array, Point(array))
    assert_array_equal(array, Vector(array))
    assert_array_equal(array, np.array(array))


@pytest.mark.parametrize(
    "array",
    [
        [],
        [0],
        [5],
        [np.nan, 0],
        [1, 1, np.nan],
        [1, 1, np.inf],
        [[1], [1]],
        [[1, 2], [1, 2]],
    ],
)
@pytest.mark.parametrize("class_spatial", [Point, Vector])
def test_failure(class_spatial, array):

    with pytest.raises(Exception):
        class_spatial(array)
