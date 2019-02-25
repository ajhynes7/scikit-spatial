import numpy as np
import pytest

from skspatial.objects import Point, Vector


@pytest.mark.parametrize(
    "array_u, array_v, angle_expected",
    [
        ([1, 0], [1, 0], 0),
        ([1, 0], [np.sqrt(3) / 2, 0.5], np.pi / 6),
        ([1, 0], [1, 1], np.pi / 4),
        ([1, 0], [0, 1], np.pi / 2),
        ([1, 0], [0, -1], np.pi / 2),
        ([1, 0], [-1, 0], np.pi),
        ([1, 0, 0], [0, 1, 0], np.pi / 2),
    ],
)
def test_angle_between(array_u, array_v, angle_expected):
    """Test finding the angle between vectors u and v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)

    angle = vector_u.angle_between(vector_v)
    assert np.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    "array_u, array_v, bool_expected",
    [
        ([1, 0], [0, 1], True),
        ([0, 1], [-1, 0], True),
        ([0, 1], [-1, 0], True),
        ([-1, 0], [0, -1], True),
        ([1, 1], [-1, -1], False),
        ([1, 1], [1, 1], False),
        # The zero vector is perpendicular to all vectors.
        ([0, 0], [-1, 5], True),
        ([0, 0, 0], [1, 1, 1], True),
    ],
)
def test_is_perpendicular(array_u, array_v, bool_expected):
    """Test checking if vector u is perpendicular to vector v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)

    assert vector_u.is_perpendicular(vector_v) == bool_expected


@pytest.mark.parametrize(
    "array_u, array_v, bool_expected",
    [
        ([0, 1], [0, 1], True),
        ([0, 1], [0, 5], True),
        ([1, 1], [-1, -1], True),
        ([1, 1], [-5, -5], True),
        ([0, 1], [0, -1], True),
        ([0, 1], [4, 0], False),
        ([0.1, 5, 4], [3, 2, 0], False),
        # The zero vector is parallel to all vectors.
        ([0, 0], [-1, 5], True),
        ([0, 0, 0], [1, 1, 1], True),
    ],
)
def test_is_parallel(array_u, array_v, bool_expected):
    """Test checking if vector u is parallel to vector v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)

    assert vector_u.is_parallel(vector_v) == bool_expected


@pytest.mark.parametrize(
    "array_a, array_b, array_c, bool_expected",
    [
        ([0, 0], [0, 1], [0, 2], True),
        ([0, 1], [0, 0], [0, 2], True),
        ([0, 0], [-1, 0], [10, 0], True),
        ([0, 0], [0, 1], [1, 2], False),
        ([0, 0, 0], [1, 1, 1], [2, 2, 2], True),
        ([0, 0, 0], [1, 1, 1], [2, 2, 2.5], False),
    ],
)
def test_is_collinear(array_a, array_b, array_c, bool_expected):
    """Test checking if three points are collinear."""
    point_a = Point(array_a)
    point_b = Point(array_b)
    point_c = Point(array_c)

    assert point_a.is_collinear(point_b, point_c) == bool_expected
