"""Test functionality of objects based on a single 1D NumPy array (Point and Vector)."""

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Point, Vector


@pytest.mark.parametrize(
    "line_or_plane, repr_expected",
    [
        (Point([0, 0]), "Point([0., 0.])"),
        (Vector([0, 0]), "Vector([0., 0.])"),
        (Point([-11, 0]), "Point([-11.,   0.])"),
        (Vector([-11, 0]), "Vector([-11.,   0.])"),
    ],
)
def test_repr(line_or_plane, repr_expected):

    assert repr(line_or_plane) == repr_expected


@pytest.mark.parametrize(
    "array", [[1, 0], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
)
def test_equality(array):

    assert_array_equal(array, Point(array))
    assert_array_equal(array, Vector(array))
    assert_array_equal(array, np.array(array))


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize(
    "array",
    [
        [],
        [0],
        [5],
        [np.nan, 0],
        [1, 1, np.nan],
        [1, 1, np.inf],
        [[1], [1]],
        [[1, 2], [1, 2]],
    ],
)
def test_failure(class_spatial, array):

    with pytest.raises(Exception):
        class_spatial(array)


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize(
    "array, dim_expected",
    [([0, 0], 2), ([0, 0, 0], 3), ([0, 0, 0, 0], 4), ([-6, 3, 8, 9], 4)],
)
def test_get_dimension(class_spatial, array, dim_expected):

    object_spatial = class_spatial(array)
    assert object_spatial.get_dimension() == dim_expected


@pytest.mark.parametrize("class_spatial", [Point, Vector])
@pytest.mark.parametrize(
    "array, dim, array_expected",
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
