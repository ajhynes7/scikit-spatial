from math import isclose
from math import sqrt

import pytest

from skspatial.objects import Point


@pytest.mark.parametrize(
    ("array_a", "array_b", "dist_expected"),
    [
        ([0], [-5], 5),
        ([0], [5], 5),
        ([0, 0], [0, 0], 0),
        ([0, 0], [1, 0], 1),
        ([0, 0], [-1, 0], 1),
        ([0, 0], [1, 1], sqrt(2)),
        ([0, 0], [5, 5], 5 * sqrt(2)),
        ([0, 0], [-5, 5], 5 * sqrt(2)),
        ([0, 0, 0], [1, 1, 1], sqrt(3)),
        ([0, 0, 0], [5, 5, 5], 5 * sqrt(3)),
        ([1, 5, 3], [1, 5, 4], 1),
        (4 * [0], 4 * [1], sqrt(4)),
    ],
)
def test_distance_point(array_a, array_b, dist_expected):

    point_a = Point(array_a)
    assert isclose(point_a.distance_point(array_b), dist_expected)
