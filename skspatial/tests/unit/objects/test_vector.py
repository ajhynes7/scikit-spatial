import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Vector


@pytest.mark.parametrize(
    "array_a, array_b, vector_expected",
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
    "array, array_unit_expected",
    [
        ([1, 0], [1, 0]),
        ([2, 0], [1, 0]),
        ([-1, 0], [-1, 0]),
        ([0, 0, 5], [0, 0, 1]),
        ([1, 1], [np.sqrt(2) / 2, np.sqrt(2) / 2]),
        ([1, 1, 1], [np.sqrt(3) / 3, np.sqrt(3) / 3, np.sqrt(3) / 3]),
        ([2, 0, 0, 0], [1, 0, 0, 0]),
        ([3, 3, 0, 0], [np.sqrt(2) / 2, np.sqrt(2) / 2, 0, 0]),
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
    "array, kwargs, bool_expected",
    [
        ([0, 0], {}, True),
        ([0, 0, 0], {}, True),
        ([0, 1], {}, False),
        # The tolerance affects the output.
        ([0, 0, 1e-4], {}, False),
        ([0, 0, 1e-4], {'atol': 1e-3}, True),
        ([0, 0, 0, 0], {}, True),
        ([7, 0, 2, 0], {}, False),
    ],
)
def test_is_zero(array, kwargs, bool_expected):

    assert Vector(array).is_zero(**kwargs) == bool_expected
