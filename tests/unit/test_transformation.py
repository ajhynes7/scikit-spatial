import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from skspatial.transformation import mean_center


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

    points = np.array(array_points)
    points_centered, centroid = mean_center(points)

    assert_array_almost_equal(points_centered, array_centered_expected)
    assert_array_almost_equal(centroid, centroid_expected)
