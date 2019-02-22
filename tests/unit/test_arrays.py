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


def test_length():
    """The length of an input array should be one to three."""
    point_1 = Point([1])
    point_2 = Point([1, 2])
    point_3 = Point([1, 1, 2])

    vector_1 = Vector(point_1.array)
    vector_2 = Vector(point_2.array)
    vector_3 = Vector(point_3.array)

    # The output point/vector is 3D.
    assert all(x.array.size == 3 for x in [point_1, point_2, point_3])
    assert all(x.array.size == 3 for x in [vector_1, vector_2, vector_3])

    with pytest.raises(Exception):
        Point([])

    with pytest.raises(Exception):
        Vector([])

    with pytest.raises(Exception):
        Point([1, 1, 1, 1])

    with pytest.raises(Exception):
        Vector([1, 1, 1, 1])


@pytest.mark.parametrize(
    "array, array_unit_expected",
    [
        ([1, 0], [1, 0]),
        ([2, 0], [1, 0]),
        ([-1, 0], [-1, 0]),
        ([0, 0, 5], [0, 0, 1]),
        ([1, 1], [np.sqrt(2) / 2, np.sqrt(2) / 2]),
        ([1, 1, 1], [np.sqrt(3) / 3, np.sqrt(3) / 3, np.sqrt(3) / 3]),
    ],
)
def test_unit_vector(array, array_unit_expected):
    """Test computing the unit vector from a vector."""
    vector = Vector(array)
    vector_unit_expected = Vector(array_unit_expected)

    assert np.allclose(vector.unit().array, vector_unit_expected.array)
