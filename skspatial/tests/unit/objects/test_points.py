import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Points


@pytest.mark.parametrize(
    "array",
    [
        # The array cannot be empty.
        [],
        [[]],
        [[], []],
        # The array cannot be 1D.
        [0],
        [5],
        [0, 1],
        [0, 1, 2],
        # The points cannot have different lengths.
        [[0, 1], [0, 1, 0]],
    ],
)
def test_failure(array):

    with pytest.raises(Exception):
        Points(array)


@pytest.mark.parametrize(
    "points, dim_expected",
    [
        (Points([[0, 0], [1, 1]]), 2),
        (Points([[0, 0], [0, 0], [0, 0]]), 2),
        (Points([[0, 0, 1], [1, 2, 1]]), 3),
        (Points([[4, 3, 9, 1], [3, 7, 8, 1]]), 4),
    ],
)
def test_dimension(points, dim_expected):

    assert points.dimension == dim_expected


@pytest.mark.parametrize(
    "points, dim, points_expected",
    [
        (Points([[0, 0], [1, 1]]), 3, Points([[0, 0, 0], [1, 1, 0]])),
        (Points([[0, 0], [1, 1]]), 4, Points([[0, 0, 0, 0], [1, 1, 0, 0]])),
        # The same dimension is allowed (nothing is changed).
        (Points([[0, 0, 0], [1, 1, 1]]), 3, Points([[0, 0, 0], [1, 1, 1]])),
        # The dimension cannot be lower than the current one.
        (Points(np.zeros((3, 1))), 0, None),
        (Points(np.zeros((3, 2))), 1, None),
        (Points(np.zeros((3, 3))), 2, None),
    ],
)
def test_set_dimension(points, dim, points_expected):

    if points_expected is None:
        with pytest.raises(
            ValueError,
            match="The desired dimension cannot be less than the current dimension.",
        ):
            points.set_dimension(dim)

    else:
        assert_array_equal(points.set_dimension(dim), points_expected)
