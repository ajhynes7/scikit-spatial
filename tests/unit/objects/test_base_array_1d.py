"""Test functionality of objects based on a single 1D NumPy array (Point and Vector)."""
import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Point
from skspatial.objects import Vector


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize("array", [[1, 0], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]])
def test_equality(class_spatial, array):

    assert_array_equal(array, class_spatial(array))


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize(
    "array",
    [
        [[0]],
        [[0], [0]],
        [[0, 0], [0, 0]],
        [[1, 2, 3]],
    ],
)
def test_failure(class_spatial, array):

    message_expected = "The array must be 1D."

    with pytest.raises(ValueError, match=message_expected):
        class_spatial(array)


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize(
    ("array", "dim", "array_expected"),
    [
        ([0, 0], 2, [0, 0]),
        ([0, 0], 3, [0, 0, 0]),
        ([0, 0], 5, [0, 0, 0, 0, 0]),
        ([6, 3, 7], 4, [6, 3, 7, 0]),
    ],
)
def test_set_dimension(class_spatial, array, dim, array_expected):

    object_spatial = class_spatial(array).set_dimension(dim)
    assert object_spatial.is_close(array_expected)


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize(
    ("array", "dimension"),
    [
        (np.zeros(3), 2),
        (np.zeros(2), 1),
        (np.zeros(1), 0),
    ],
)
def test_dimension_failure(class_spatial, array, dimension):

    message_expected = "The desired dimension cannot be less than the current dimension."

    object_spatial = class_spatial(array)

    with pytest.raises(ValueError, match=message_expected):
        object_spatial.set_dimension(dimension)


@pytest.mark.parametrize("class_spatial", [Point, Vector])
def test_dimension_of_slice(class_spatial):

    object_spatial = class_spatial([0, 0, 0])

    assert object_spatial.dimension == 3
    assert object_spatial[:3].dimension == 3
    assert object_spatial[:2].dimension == 2
    assert object_spatial[:1].dimension == 1
