import pytest

from skspatial.objects import Plane


@pytest.mark.parametrize(
    "plane, points_expected",
    [
        (Plane([0, 0, 0], [0, 0, 1]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([1, 0, 0], [0, 0, 1]), [[0, -1, 0], [2, -1, 0], [0, 1, 0], [2, 1, 0]]),
        (Plane([0, 0, 0], [0, 0, -1]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([0, 0, 0], [0, 0, 5]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([0, 0, 0], [0, 1, 0]), [[-1, 0, -1], [1, 0, -1], [-1, 0, 1], [1, 0, 1]]),
        (Plane([0, 0, 0], [1, 0, 0]), [[0, -1, -1], [0, 1, -1], [0, -1, 1], [0, 1, 1]]),
        (Plane([0, 0, 0], [1, 1, 0]), [[-1, 1, -1], [1, -1, -1], [-1, 1, 1], [1, -1, 1]]),
    ],
)
def test_plane_points(plane, points_expected):

    points = plane.to_points()

    assert points.is_close(points_expected)
