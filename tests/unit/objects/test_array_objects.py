"""Test functionality of objects based on a single NumPy array (Point and Vector)."""

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Point, Vector


@pytest.mark.parametrize(
    "point_a, point_b",
    [
        (Point([1]), Point([1])),
        (Point([1]), Point([1, 0])),
        (Point([1]), Point([1, 0, 0])),
        (Point([1, 0]), Point((1, 0))),
        (Point([1, 0]), Point(np.array([1, 0]))),
    ],
)
def test_equality(point_a, point_b):

    assert_array_equal(point_a, point_b)

    vector_a = Vector(point_a)
    vector_b = Vector(point_b)

    assert_array_equal(vector_a, vector_b)

    assert_array_equal(point_a, vector_a)
    assert_array_equal(point_b, vector_b)


@pytest.mark.parametrize("class_spatial", [Point, Vector])
def test_length(class_spatial):
    """The output point/vector is always 3D."""
    object_1 = class_spatial([1])
    object_2 = class_spatial([1, 1])
    object_3 = class_spatial([1, 1, 1])

    assert all(x.size == 3 for x in [object_1, object_2, object_3])


@pytest.mark.parametrize(
    "array",
    [
        [],
        [1, 1, 1, 1],
        [np.nan],
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
