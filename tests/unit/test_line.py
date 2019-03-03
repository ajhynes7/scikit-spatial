import pytest

from skspatial.objects import Point, Vector, Line


@pytest.mark.parametrize(
    "point, vector, line_expected",
    [
        (Point([0, 0]), Vector([1, 0]), Line(Point([0, 0]), Vector([1, 0]))),
        (Point([0, 0]), Vector([1, 1]), Line(Point([0, 0]), Vector([1, 1]))),
        (Point([0, 0]), Vector([5, 5]), Line(Point([0, 0]), Vector([1, 1]))),
    ],
)
def test_creation(point, vector, line_expected):

    assert Line(point, vector) == line_expected


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
