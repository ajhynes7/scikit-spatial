import pytest

from skspatial.objects import Plane


@pytest.mark.parametrize(
    "point_a, point_b, point_c, plane_expected",
    [
        (
            [0, 0], [1, 0], [0, 1],
            Plane([0, 0], [0, 0, 1]),
        ),
        # The spacing between the points is irrelevant.
        (
            [0, 0], [9, 0], [0, 9],
            Plane([0, 0], [0, 0, 1]),
        ),
        # The first point is used as the plane point.
        (
            [0, 0.1], [1, 0], [0, 1],
            Plane([0, 0.1], [0, 0, 1]),
        ),
        # The order of points is relevant.
        (
            [0, 0], [0, 1], [1, 0],
            Plane([0, 0], [0, 0, -1]),
        ),
    ],
)
def test_from_points(point_a, point_b, point_c, plane_expected):

    assert Plane.from_points(point_a, point_b, point_c).is_close(plane_expected)


@pytest.mark.parametrize(
    "point_a, point_b, point_c",
    [
        # The points cannot be collinear.
        ([0], [0], [0]),
        ([0], [1], [2]),
        ([-2, 1], [0, 2], [2, 3]),
        ([0, 0, 0], [1, 1, 1], [-2, -2, -2]),
        ([0, 1, 2], [1, 2, 3], [4, 5, 6]),
    ],
)
def test_from_points_failure(point_a, point_b, point_c):

    with pytest.raises(Exception):
        Plane.from_points(point_a, point_b, point_c)
