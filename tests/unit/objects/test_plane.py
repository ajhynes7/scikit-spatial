import pytest

from skspatial.objects import Point, Vector, Plane


@pytest.mark.parametrize(
    "point_a, point_b, point_c, plane_expected",
    [
        (
            Point([0, 0]),
            Point([1, 0]),
            Point([0, 1]),
            Plane(Point([0, 0]), Vector([0, 0, 1])),
        ),
        # The spacing between the points is irrelevant.
        (
            Point([0, 0]),
            Point([9, 0]),
            Point([0, 9]),
            Plane(Point([0, 0]), Vector([0, 0, 1])),
        ),
        # The first point is used as the plane point.
        (
            Point([0, 0.1]),
            Point([1, 0]),
            Point([0, 1]),
            Plane(Point([0, 0.1]), Vector([0, 0, 1])),
        ),
        # The order of points is relevant.
        (
            Point([0, 0]),
            Point([0, 1]),
            Point([1, 0]),
            Plane(Point([0, 0]), Vector([0, 0, -1])),
        ),
    ],
)
def test_from_points(point_a, point_b, point_c, plane_expected):

    assert Plane.from_points(point_a, point_b, point_c) == plane_expected


@pytest.mark.parametrize(
    "point_a, point_b, point_c",
    [
        # The points cannot be collinear.
        (Point([0]), Point([0]), Point([0])),
        (Point([0]), Point([1]), Point([2])),
        (Point([-2, 1]), Point([0, 2]), Point([2, 3])),
        # The points cannot be vectors.
        (Vector([-2, 1]), Point([0, 2]), Point([2, 3])),
    ],
)
def test_from_points_failure(point_a, point_b, point_c):

    with pytest.raises(Exception):
        Plane.from_points(point_a, point_b, point_c)
