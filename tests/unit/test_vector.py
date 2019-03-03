import numpy as np
import pytest

from skspatial.objects import Point, Vector


@pytest.mark.parametrize(
    "array_a, array_b, vector_expected",
    [
        ([0], [1], Vector([1])),
        ([1, 0], [1, 0], Vector([0])),
        ([1, 0], [2, 0], Vector([1, 0])),
        ([0], [5, 0, 3], Vector([5, 0, 3])),
        ([8, 3, -5], [3, 7, 1], Vector([-5, 4, 6])),
    ],
)
def test_from_points(array_a, array_b, vector_expected):

    point_a = Point(array_a)
    point_b = Point(array_b)

    assert Vector.from_points(point_a, point_b)


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
def test_unit(array, array_unit_expected):

    vector = Vector(array)
    vector_unit_expected = Vector(array_unit_expected)

    assert np.allclose(vector.unit().array, vector_unit_expected.array)


@pytest.mark.parametrize(
    "array, vector_expected",
    [
        ([0], Vector([0])),
        ([1], Vector([-1])),
        ([1, 2, 3], Vector([-1, -2, -3])),
        ([5, -4, 10], Vector([-5, 4, -10])),
    ],
)
def test_reverse(array, vector_expected):

    vector_reversed = Vector(array).reverse()
    assert vector_reversed.is_close(vector_expected)


@pytest.mark.parametrize(
    "array, kwargs, bool_expected",
    [
        ([0], {}, True),
        ([0, 0], {}, True),
        ([0, 0, 0], {}, True),
        ([0, 1], {}, False),
        # The tolerance affects the output.
        ([0, 0, 1e-4], {}, False),
        ([0, 0, 1e-4], {'atol': 1e-3}, True),
    ],
)
def test_is_zero(array, kwargs, bool_expected):

    assert Vector(array).is_zero(**kwargs) == bool_expected


@pytest.mark.parametrize(
    "array, scalar, vector_expected",
    [
        ([0], 5, Vector([0])),
        ([1], 10, Vector([10])),
        ([1, 2, 3], 3, Vector([3, 6, 9])),
        ([5, -4, 10], -2, Vector([-10, 8, -20])),
    ],
)
def test_scale(array, scalar, vector_expected):

    vector_scaled = Vector(array).scale(scalar)
    assert vector_scaled.is_close(vector_expected)


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
    "array_u, array_v, array_expected",
    [
        ([1, 1], [1, 0], [1, 0]),
        ([1, 5], [1, 0], [1, 0]),
        ([5, 5], [1, 0], [5, 0]),
        # Scaling v by a non-zero scalar doesn't change the projection.
        ([0, 1], [0, 1], [0, 1]),
        ([0, 1], [0, -5], [0, 1]),
        ([0, 1], [0, 15], [0, 1]),
        # The projection is the zero vector if u and v are perpendicular.
        ([1, 0], [0, 1], [0, 0]),
        ([5, 0], [0, 9], [0, 0]),
        # The projection of the zero vector onto v is the zero vector.
        ([0, 0], [0, 1], [0, 0]),
    ],
)
def test_project_vector(array_u, array_v, array_expected):
    """Test projecting vector u onto vector v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)
    vector_expected = Vector(array_expected)

    vector_u_projected = vector_v.project_vector(vector_u)

    assert vector_u_projected.is_close(vector_expected)
