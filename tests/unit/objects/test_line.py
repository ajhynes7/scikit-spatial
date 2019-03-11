import pytest

from skspatial.objects import Point, Vector, Line, Plane


@pytest.mark.parametrize(
    "point_a, point_b, line_expected",
    [
        ([0, 0], [1, 0], Line([0, 0], [1, 0])),
        ([0, 0], [1, 1], Line([0, 0], [1, 1])),
        ([5, 2], [9, 2], Line([5, 2], [1, 0])),
        ([1, 1], [0, 0], Line([1, 1], [-1, -1])),
        ([0, 0], [5, 0], Line([0, 0], [1, 0])),
    ],
)
def test_from_points(point_a, point_b, line_expected):

    assert Line.from_points(point_a, point_b).is_close(line_expected)


@pytest.mark.parametrize(
    "point_a, point_b",
    [
        # The zero vector cannot be used.
        (Point([0]), Point([0])),
        (Point([1, 5]), Point([1, 5])),
        (Point([-1, 5]), Vector([-1, 5])),
    ],
)
def test_from_points_failure(point_a, point_b):

    with pytest.raises(Exception):
        Line.from_points(point_a, point_b)


@pytest.mark.parametrize(
    "point, vector",
    [
        # The zero vector cannot be used.
        (Point([0]), Vector([0])),
        (Point([1]), Vector([0])),
    ],
)
@pytest.mark.parametrize("class_spatial", [Line, Plane])
def test_init_failure(point, vector, class_spatial):

    with pytest.raises(Exception):
        class_spatial(point, vector)
