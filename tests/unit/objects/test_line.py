import pytest
from numpy.testing import assert_array_equal

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


@pytest.mark.parametrize(
    "line, param, array_expected",
    [
        (Line([0, 0], [1, 0]), 0, [0, 0]),
        (Line([0, 0], [1, 0]), 1, [1, 0]),
        (Line([0, 0], [1, 0]), 5, [5, 0]),
        (Line([0, 0], [1, 0]), -8, [-8, 0]),
        (Line([5, 2, 1], [0, 2, 0]), 0, [5, 2, 1]),
        (Line([5, 2, 1], [0, 9, 0]), 1, [5, 3, 1]),
        (Line([5, 2, 1], [0, -9, 0]), 1, [5, 1, 1]),
    ],
)
def test_to_point(line, param, array_expected):

    point = line.to_point(t=param)

    assert_array_equal(point, Point(array_expected))
