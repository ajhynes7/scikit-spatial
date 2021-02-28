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
        ([0], None),
        ([0, 0], None),
        ([0, 0, 0], None),
    ],
)
def test_unit(array, array_unit_expected):

    if array_unit_expected is None:
        with pytest.raises(ValueError, match="The magnitude must not be zero."):
            Vector(array).unit()

    else:
        assert Vector(array).unit().is_close(array_unit_expected)


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
        ([1, 1], [0, 0], None),
        ([0, 0], [1, 1], None),
    ],
)
def test_cosine_similarity(array_u, array_v, similarity_expected):

    if similarity_expected is None:
        with pytest.raises(ValueError, match="The vectors must have non-zero magnitudes."):
            Vector(array_u).cosine_similarity(array_v)

    else:
        similarity = Vector(array_u).cosine_similarity(array_v)
        assert math.isclose(similarity, similarity_expected)


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
        ([0], [0], None),
        ([1, 1, 1], [1, 0, 0], None),
        (np.ones(4), np.ones(4), None),
    ],
)
def test_angle_signed(array_u, array_v, angle_expected):

    if angle_expected is None:
        with pytest.raises(ValueError, match="The vectors must be 2D."):
            Vector(array_u).angle_signed(array_v)

    else:
        angle = Vector(array_u).angle_signed(array_v)
        assert math.isclose(angle, angle_expected)


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
