import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from skspatial.objects import Point
from skspatial.objects import Points


@pytest.mark.parametrize(
    "array",
    [
        [0],
        [5],
        [0, 1],
        [0, 1, 2],
    ],
)
def test_failure(array):

    message_expected = "The array must be 2D."

    with pytest.raises(ValueError, match=message_expected):
        Points(array)


@pytest.mark.parametrize(
    ("points", "dim_expected"),
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
    ("points", "dim", "points_expected"),
    [
        (Points([[0, 0], [1, 1]]), 3, Points([[0, 0, 0], [1, 1, 0]])),
        (Points([[0, 0], [1, 1]]), 4, Points([[0, 0, 0, 0], [1, 1, 0, 0]])),
        # The same dimension is allowed (nothing is changed).
        (Points([[0, 0, 0], [1, 1, 1]]), 3, Points([[0, 0, 0], [1, 1, 1]])),
    ],
)
def test_set_dimension(points, dim, points_expected):

    assert_array_equal(points.set_dimension(dim), points_expected)


def test_dimension_of_slice():

    points = Points([[0, 0, 0], [0, 0, 0]])

    assert points.dimension == 3
    assert points[:, :3].dimension == 3
    assert points[:, :2].dimension == 2
    assert points[:, :1].dimension == 1

    assert points[:0, :].dimension == 3
    assert points[:1, :].dimension == 3
    assert points[:2, :].dimension == 3

    # The dimension value is None here because the points are no longer a 2D array,
    # so the normal method of finding the dimension fails.
    assert points[:, 0].dimension is None
    assert points[0, :].dimension is None


@pytest.mark.parametrize(
    ("array_points", "array_centered_expected", "centroid_expected"),
    [
        ([[0, 1]], [[0, 0]], [0, 1]),
        ([[1, 1], [2, 2]], [[-0.5, -0.5], [0.5, 0.5]], [1.5, 1.5]),
        ([[0, 0], [2, 2]], [[-1, -1], [1, 1]], [1, 1]),
        (
            [[1, 2], [-1.3, 11], [24, 5], [7, 3]],
            [[-6.675, -3.25], [-8.975, 5.75], [16.325, -0.25], [-0.675, -2.25]],
            [7.675, 5.25],
        ),
        ([[-2, 0, 2, 5], [4, 1, -3, 2.1]], [[-3, -0.5, 2.5, 1.45], [3, 0.5, -2.5, -1.45]], [1, 0.5, -0.5, 3.55]),
    ],
)
def test_mean_center(array_points, array_centered_expected, centroid_expected):

    points = Points(array_points)
    points_centered, centroid = points.mean_center(return_centroid=True)

    assert isinstance(points_centered, Points)
    assert isinstance(centroid, Point)

    assert_array_almost_equal(points_centered, array_centered_expected)
    assert_array_almost_equal(centroid, centroid_expected)


@pytest.mark.parametrize(
    ("array_points", "array_points_expected"),
    [
        ([[0, 0], [1, 0]], [[0, 0], [1, 0]]),
        ([[0, 0], [1, 1]], [[0, 0], np.sqrt(2) / 2 * np.ones(2)]),
        ([[0, 0], [5, 0], [-1, 0]], [[0, 0], [1, 0], [-0.2, 0]]),
        (9 * np.ones((3, 3)), np.sqrt(3) / 3 * np.ones((3, 3))),
    ],
)
def test_normalize_distance(array_points, array_points_expected):

    points_normalized = Points(array_points).normalize_distance()

    assert_array_almost_equal(points_normalized, array_points_expected)


@pytest.mark.parametrize(
    ("points", "bool_expected"),
    [
        ([[0, 0], [0, 0], [0, 0]], True),
        ([[1, 0], [1, 0], [1, 0]], True),
        ([[0, 0], [0, 1], [0, 2]], True),
        ([[0, 0], [0, 1], [1, 2]], False),
        ([[0, 1], [0, 0], [0, 2]], True),
        ([[0, 0], [-1, 0], [10, 0]], True),
        ([[0, 0], [1, 1], [2, 2], [-4, -4], [5, 5]], True),
        ([[0, 0, 0], [1, 1, 1], [2, 2, 2]], True),
        ([[0, 0, 0], [1, 1, 1], [2, 2, 2.5]], False),
        ([[0, 0, 0], [1, 1, 0], [2, 2, 0], [-4, -4, 10], [5, 5, 0]], False),
    ],
)
def test_are_collinear(points, bool_expected):
    """Test checking if multiple points are collinear."""

    assert Points(points).are_collinear() == bool_expected
