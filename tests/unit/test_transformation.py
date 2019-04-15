import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from skspatial.objects import Points, Line


@pytest.mark.parametrize(
    "array_points, array_centered_expected, centroid_expected",
    [
        ([[0, 1]], [[0, 0]], [0, 1]),
        ([[1, 1], [2, 2]], [[-0.5, -0.5], [0.5, 0.5]], [1.5, 1.5]),
        ([[0, 0], [2, 2]], [[-1, -1], [1, 1]], [1, 1]),
        (
            [[1, 2], [-1.3, 11], [24, 5], [7, 3]],
            [[-6.675, -3.25], [-8.975, 5.75], [16.325, -0.25], [-0.675, -2.25]],
            [7.675, 5.25],
        ),
        (
            [[-2, 0, 2, 5], [4, 1, -3, 2.1]],
            [[-3, -0.5, 2.5, 1.45], [3, 0.5, -2.5, -1.45]],
            [1, 0.5, -0.5, 3.55],
        ),
    ],
)
def test_mean_center(array_points, array_centered_expected, centroid_expected):

    points = Points(array_points)
    points_centered, centroid = points.mean_center()

    assert_array_almost_equal(points_centered, array_centered_expected)
    assert_array_almost_equal(centroid, centroid_expected)


@pytest.mark.parametrize(
    "line, points, coords_expected",
    [
        (Line([0, 0], [1, 0]), [[1, 0], [2, 0], [3, 0], [4, 0]], [1, 2, 3, 4]),
        # The point on the line acts as the origin.
        (Line([3, 0], [1, 0]), [[1, 0], [2, 0], [3, 0], [4, 0]], [-2, -1, 0, 1]),
        (
            Line([0, 0], [1, 1]),
            [[1, 0], [2, 0], [3, 0], [0, 1], [0, 2], [0, 3]],
            np.sqrt(2) * np.array([0.5, 1, 1.5, 0.5, 1, 1.5]),
        ),
        # The magnitude of the direction vector is irrelevant.
        (
            Line([0, 0], [3, 3]),
            [[1, 0], [2, 0], [3, 0], [0, 1], [0, 2], [0, 3]],
            np.sqrt(2) * np.array([0.5, 1, 1.5, 0.5, 1, 1.5]),
        ),
        (
            Line([0, 0, 0], [1, 0, 0]),
            [[1, 20, 3], [2, -5, 8], [3, 59, 100], [4, 0, 14]],
            [1, 2, 3, 4],
        ),
        (
            Line([0, 0, 0], [0, 1, 0]),
            [[1, 20, 3], [2, -5, 8], [3, 59, 100], [4, 0, 14]],
            [20, -5, 59, 0],
        ),
    ],
)
def test_transform_points_line(line, points, coords_expected):

    coordinates = line.transform_points(points)
    assert_array_almost_equal(coordinates, coords_expected)
