"""Test functionality of objects based on a single NumPy array (Point and Vector)."""

import numpy as np
import pytest

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

    assert point_a == point_b

    vector_a = Vector(point_a.array)
    vector_b = Vector(point_b.array)

    assert vector_a == vector_b

    assert not point_a == vector_a
    assert not point_b == vector_b


@pytest.mark.parametrize("PointOrVector", [Point, Vector])
def test_length(PointOrVector):
    """The output point/vector is always 3D."""
    object_1 = PointOrVector([1])
    object_2 = PointOrVector([1, 1])
    object_3 = PointOrVector([1, 1, 1])

    assert all(x.array.size == 3 for x in [object_1, object_2, object_3])


@pytest.mark.parametrize(
    "array", [[], [1, 1, 1, 1], [np.nan], [1, 1, np.nan], [1, 1, np.inf]]
)
@pytest.mark.parametrize("class_", [Point, Vector])
def test_failure(class_, array):

    with pytest.raises(Exception):
        class_(array)
