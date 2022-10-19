import math

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Vector


@pytest.mark.parametrize(
    ("array_a", "array_b", "vector_expected"),
    [
        ([0, 0], [1, 0], Vector([1, 0])),
        ([1, 0], [1, 0], Vector([0, 0])),
        ([1, 0], [2, 0], Vector([1, 0])),
        ([8, 3, -5], [3, 7, 1], Vector([-5, 4, 6])),
        ([5, 7, 8, 9], [2, 5, 3, -4], Vector([-3, -2, -5, -13])),
    ],
)
def test_from_points(array_a, array_b, vector_expected):

    assert_array_equal(Vector.from_points(array_a, array_b), vector_expected)


@pytest.mark.parametrize(
    ("array", "array_unit_expected"),
    [
        ([1, 0], [1, 0]),
        ([2, 0], [1, 0]),
        ([-1, 0], [-1, 0]),
        ([0, 0, 5], [0, 0, 1]),
        ([1, 1], [math.sqrt(2) / 2, math.sqrt(2) / 2]),
        ([1, 1, 1], [math.sqrt(3) / 3, math.sqrt(3) / 3, math.sqrt(3) / 3]),
        ([2, 0, 0, 0], [1, 0, 0, 0]),
        ([3, 3, 0, 0], [math.sqrt(2) / 2, math.sqrt(2) / 2, 0, 0]),
    ],
)
def test_unit(array, array_unit_expected):

    assert Vector(array).unit().is_close(array_unit_expected)


@pytest.mark.parametrize(
    "array",
    [[0], [0, 0], [0, 0, 0]],
)
def test_unit_failure(array):

    with pytest.raises(ValueError, match="The magnitude must not be zero."):
        Vector(array).unit()


@pytest.mark.parametrize(
    ("array", "kwargs", "bool_expected"),
    [
        ([0, 0], {}, True),
        ([0, 0, 0], {}, True),
        ([0, 1], {}, False),
        # The tolerance affects the output.
        ([0, 0, 1e-4], {}, False),
        ([0, 0, 1e-4], {'abs_tol': 1e-3}, True),
        ([0, 0, 0, 0], {}, True),
        ([7, 0, 2, 0], {}, False),
    ],
)
def test_is_zero(array, kwargs, bool_expected):

    assert Vector(array).is_zero(**kwargs) == bool_expected


@pytest.mark.parametrize(
    ("array_u", "array_v", "similarity_expected"),
    [
        ([1, 0], [1, 0], 1),
        ([1, 0], [0, 1], 0),
        ([1, 0], [-1, 0], -1),
        ([1, 0], [0, -1], 0),
        ([1, 0], [1, 1], math.sqrt(2) / 2),
        ([1, 0], [-1, 1], -math.sqrt(2) / 2),
        ([1, 0], [-1, -1], -math.sqrt(2) / 2),
        ([1, 0], [1, -1], math.sqrt(2) / 2),
        ([1, 0], [0.5, math.sqrt(3) / 2], 0.5),
        ([1, 0], [math.sqrt(3) / 2, 0.5], math.sqrt(3) / 2),
    ],
)
def test_cosine_similarity(array_u, array_v, similarity_expected):

    similarity = Vector(array_u).cosine_similarity(array_v)
    assert math.isclose(similarity, similarity_expected)


@pytest.mark.parametrize(
    ("array_u", "array_v"),
    [
        ([1, 1], [0, 0]),
        ([0, 0], [1, 1]),
    ],
)
def test_cosine_similarity_failure(array_u, array_v):
    with pytest.raises(ValueError, match="The vectors must have non-zero magnitudes."):
        Vector(array_u).cosine_similarity(array_v)


@pytest.mark.parametrize(
    ("array_u", "array_v", "angle_expected"),
    [
        ([1, 0], [1, 0], 0),
        ([1, 0], [math.sqrt(3) / 2, 0.5], np.pi / 6),
        ([1, 0], [1, 1], np.pi / 4),
        ([1, 0], [0, 1], np.pi / 2),
        ([1, 0], [0, -1], np.pi / 2),
        ([1, 0], [-1, 0], np.pi),
        ([1, 0, 0], [0, 1, 0], np.pi / 2),
    ],
)
def test_angle_between(array_u, array_v, angle_expected):
    """Test finding the angle between vectors u and v."""

    angle = Vector(array_u).angle_between(array_v)
    assert math.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    ("array_u", "array_v", "angle_expected"),
    [
        ([1, 0], [1, 0], 0),
        ([1, 0], [1, 1], np.pi / 4),
        ([1, 0], [0, 1], np.pi / 2),
        ([1, 0], [-1, 1], 3 * np.pi / 4),
        ([1, 0], [-1, 0], np.pi),
        ([1, 0], [-1, -1], -3 * np.pi / 4),
        ([1, 0], [0, -1], -np.pi / 2),
        ([1, 0], [1, -1], -np.pi / 4),
        ([1, 1], [0, 1], np.pi / 4),
        ([1, 1], [1, 0], -np.pi / 4),
    ],
)
def test_angle_signed(array_u, array_v, angle_expected):

    angle = Vector(array_u).angle_signed(array_v)
    assert math.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    ("array_u", "array_v"),
    [
        ([0], [0]),
        ([1, 1, 1], [1, 0, 0]),
        (np.ones(4), np.ones(4)),
    ],
)
def test_angle_signed_failure(array_u, array_v):

    with pytest.raises(ValueError, match="The vectors must be 2D."):
        Vector(array_u).angle_signed(array_v)


@pytest.mark.parametrize(
    ("array_u", "array_v", "direction_positive", "angle_expected"),
    [
        ([1, 0, 0], [1, 0, 0], [1, 2, 3], 0),
        ([1, 0, 0], [-1, 0, 0], [1, 2, 3], np.pi),
        ([-1, 0, 0], [1, 0, 0], [1, 2, 3], np.pi),
        ([3, 0, 0], [0, 2, 0], [0, 0, -4], -np.pi / 2),
        ([3, 0, 0], [0, 2, 0], [0, 0, 5], np.pi / 2),
        ([-4, 0, 0], [1, 1, 0], [0, 0, 2], -3 * np.pi / 4),
    ],
)
def test_angle_signed_3d(array_u, array_v, direction_positive, angle_expected):

    angle = Vector(array_u).angle_signed_3d(array_v, direction_positive)
    assert math.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    ("array_u", "array_v", "direction_positive", "message_expected"),
    [
        ([1, 0], [1, 0], [0, 0, 3], "The vectors must be 3D."),
        ([2, -1, 0], [0, 2, 0], [1, 1], "The vectors must be 3D."),
        (np.ones(4), np.ones(4), np.ones(4), "The vectors must be 3D."),
        (
            [3, 0, 0],
            [0, 2, 0],
            [0, 1, 1],
            "The positive direction vector must be perpendicular to the plane formed by the two main input vectors.",
        ),
    ],
)
def test_angle_signed_3d_failure(array_u, array_v, direction_positive, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Vector(array_u).angle_signed_3d(array_v, direction_positive)


@pytest.mark.parametrize(
    ("array_u", "array_v", "bool_expected"),
    [
        ([1, 0], [0, 1], True),
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

    assert vector_u.is_perpendicular(array_v) == bool_expected


@pytest.mark.parametrize(
    ("array_u", "array_v", "bool_expected"),
    [
        ([0, 1], [0, 1], True),
        ([1, 0], [0, 1], False),
        ([0, 1], [4, 0], False),
        ([0, 1], [0, 5], True),
        ([1, 1], [-1, -1], True),
        ([1, 1], [-5, -5], True),
        ([0, 1], [0, -1], True),
        ([0.1, 5, 4], [3, 2, 0], False),
        ([1, 1, 1, 1], [-2, -2, -2, 4], False),
        ([1, 1, 1, 1], [-2, -2, -2, -2], True),
        ([5, 0, -6, 7], [0, 1, 6, 3], False),
        ([6, 0, 1, 0], [-12, 0, -2, 0], True),
        # The zero vector is parallel to all vectors.
        ([0, 0], [1, 1], True),
        ([5, 2], [0, 0], True),
        ([5, -3, 2, 6], [0, 0, 0, 0], True),
    ],
)
def test_is_parallel(array_u, array_v, bool_expected):
    """Test checking if vector u is parallel to vector v."""
    vector_u = Vector(array_u)

    assert vector_u.is_parallel(array_v) == bool_expected


@pytest.mark.parametrize(
    ("array_a", "array_b", "value_expected"),
    [
        ([0, 0], [0, 0], 0),
        ([0, 0], [0, 1], 0),
        ([0, 0], [1, 1], 0),
        ([0, 1], [0, 1], 0),
        ([0, 1], [0, 9], 0),
        ([0, 1], [0, -20], 0),
        ([0, 1], [1, 1], 1),
        ([0, 1], [38, 29], 1),
        ([0, 1], [1, 0], 1),
        ([0, 1], [1, -100], 1),
        ([0, 1], [-1, 1], -1),
        ([0, 1], [-1, 20], -1),
        ([0, 1], [-1, -20], -1),
        ([0, 1], [-5, 50], -1),
    ],
)
def test_side_vector(array_a, array_b, value_expected):

    assert Vector(array_a).side_vector(array_b) == value_expected


@pytest.mark.parametrize(
    ("array_a", "array_b"),
    [
        ([0], [1]),
        ([0, 0, 0], [1, 1, 1]),
        ([0, 0, 0, 0], [1, 1, 1, 1]),
    ],
)
def test_side_vector_failure(array_a, array_b):

    message_expected = "The vectors must be 2D."

    with pytest.raises(ValueError, match=message_expected):
        Vector(array_a).side_vector(array_b)


@pytest.mark.parametrize(
    ("vector_u", "vector_v", "vector_expected"),
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
def test_project_vector(vector_u, vector_v, vector_expected):
    """Test projecting vector u onto vector v."""

    vector_u_projected = Vector(vector_v).project_vector(vector_u)

    assert vector_u_projected.is_close(vector_expected)


@pytest.mark.parametrize(
    ("array", "array_expected"),
    [
        ([1], [-1]),
        ([5], [-1]),
        ([-5], [1]),
        ([0, 1], [1, 0]),
        ([1, 0], [0, 1]),
        ([2, 0], [0, 1]),
        ([5, 0], [0, 1]),
        ([0, 2], [1, 0]),
        ([0, 5], [1, 0]),
        ([0, 0, 1], [1, 0, 0]),
        ([1, 0, 0], [0, 1, 0]),
        ([1, 0, 1], [1, 0, 0]),
        ([1, 1, 0], [1, 0, 0]),
        ([0, 0, 1, 1], [1, 0, 0, 0]),
        ([5, 0, 1, 1], [1, 0, 0, 0]),
    ],
)
def test_different_direction(array, array_expected):

    vector = Vector(array)
    vector_expected = Vector(array_expected)

    assert vector.different_direction().is_equal(vector_expected)


@pytest.mark.parametrize(
    "array",
    [
        ([0]),
        ([0] * 2),
        ([0] * 3),
        ([0] * 4),
    ],
)
def test_different_direction_failure(array):

    message_expected = "The vector must not be the zero vector."

    with pytest.raises(ValueError, match=message_expected):
        Vector(array).different_direction()
