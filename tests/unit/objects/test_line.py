import pytest

from skspatial.objects import Point, Vector, Line, Plane


@pytest.mark.parametrize(
    "point_a, point_b, line_expected",
    [
        (Point([0, 0]), Point([1, 0]), Line(Point([0, 0]), Vector([1, 0]))),
        (Point([0, 0]), Point([1, 1]), Line(Point([0, 0]), Vector([1, 1]))),
        (Point([5, 2]), Point([9, 2]), Line(Point([5, 2]), Vector([1, 0]))),
        (Point([1, 1]), Point([0, 0]), Line(Point([1, 1]), Vector([-1, -1]))),
        (Point([0, 0]), Point([5, 0]), Line(Point([0, 0]), Vector([1, 0]))),
    ],
)
def test_from_points(point_a, point_b, line_expected):

    assert Line.from_points(point_a, point_b) == line_expected


@pytest.mark.parametrize(
    "point_a, point_b",
    [
        (Point([0]), Point([0])),
        (Point([1, 5]), Point([1, 5])),
        (Point([0, 0]), Vector([1, 1])),
    ],
)
def test_from_points_failure(point_a, point_b):

    with pytest.raises(Exception):
        Line.from_points(point_a, point_b)


@pytest.mark.parametrize(
    "point, vector",
    [
        # A point and vector are not interchangeable.
        (Point([1]), Point([1])),
        (Vector([1]), Point([1])),
        (Vector([1]), Vector([1])),
        # The zero vector cannot be used.
        (Point([0]), Vector([0])),
        (Point([1]), Vector([0])),
    ],
)
@pytest.mark.parametrize("LineOrPlane", [Line, Plane])
def test_init_failure(point, vector, LineOrPlane):

    with pytest.raises(Exception):
        LineOrPlane(point, vector)
