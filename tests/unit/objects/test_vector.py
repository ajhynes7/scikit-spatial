import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Vector


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

    assert_array_equal(Vector.from_points(array_a, array_b), vector_expected)


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

    assert vector.unit().is_close(vector_unit_expected)


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

    vector_scaled = scalar * Vector(array)
    assert vector_scaled.is_close(vector_expected)
