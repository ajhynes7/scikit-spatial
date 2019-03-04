import pytest
from skspatial.objects import Point, Vector, Line, Plane


@pytest.mark.parametrize(
    "line_a, line_b, point_expected",
    [
        (
            Line(Point([0, 0]), Vector([1, 0])),
            Line(Point([0, 0]), Vector([1, 1])),
            Point([0, 0]),
        ),
        (
            Line(Point([0, 0]), Vector([1, 0])),
            Line(Point([5, 5]), Vector([1, 1])),
            Point([0, 0]),
        ),
        (
            Line(Point([0, 0]), Vector([1, 0])),
            Line(Point([9, 0]), Vector([1, 1])),
            Point([9, 0]),
        ),
        (
            Line(Point([0, 0]), Vector([1, 1])),
            Line(Point([4, 0]), Vector([1, -1])),
            Point([2, 2]),
        ),
        (
            Line(Point([0, 0, 0]), Vector([1, 1, 1])),
            Line(Point([4, 4, 0]), Vector([-1, -1, 1])),
            Point([2, 2, 2]),
        ),
    ],
)
def test_intersect_lines(line_a, line_b, point_expected):

    point_intersection = line_a.intersect_line(line_b)
    assert point_intersection.is_close(point_expected)


@pytest.mark.parametrize(
    "line_a, line_b",
    [
        (Line(Point([0, 0]), Vector([1, 0])), Line(Point([0, 0]), Vector([1, 0]))),
        (Line(Point([0, 0]), Vector([1, 0])), Line(Point([5, 5]), Vector([1, 0]))),
        (Line(Point([0, 0]), Vector([0, 1])), Line(Point([0, 0]), Vector([0, 5]))),
        (Line(Point([0, 0]), Vector([1, 0])), Line(Point([0, 0]), Vector([-1, 0]))),
        (Line(Point([0, 0]), Vector([1, 0])), Line(Point([5, 5]), Vector([-1, 0]))),
        (
            Line(Point([0, 0]), Vector([1, 1, 1])),
            Line(Point([0, 1]), Vector([-1, 0, 0])),
        ),
    ],
)
def test_intersect_lines_failure(line_a, line_b):

    with pytest.raises(Exception):
        line_a.intersect_line(line_b)


@pytest.mark.parametrize(
    "line, plane, point_expected",
    [
        (
            Line(Point([0]), Vector([1, 0])),
            Plane(Point([0]), Vector([1, 0])),
            Point([0]),
        ),
        (
            Line(Point([0]), Vector([0, 0, 1])),
            Plane(Point([0]), Vector([0, 0, 1])),
            Point([0]),
        ),
        (
            Line(Point([5, -3]), Vector([0, 0, 1])),
            Plane(Point([0]), Vector([0, 0, 1])),
            Point([5, -3, 0]),
        ),
    ],
)
def test_intersect_line_plane(line, plane, point_expected):

    point_intersection = plane.intersect_line(line)
    assert point_intersection.is_close(point_expected)


@pytest.mark.parametrize(
    "line, plane",
    [
        (Line(Point([0]), Vector([1, 0, 0])), Plane(Point([0]), Vector([0, 0, 1]))),
        (Line(Point([0]), Vector([0, 0, 1])), Plane(Point([0]), Vector([1, 0, 0]))),
        (Line(Point([0]), Vector([0, 0, 1])), Plane(Point([0]), Vector([0, 1, 0]))),
    ],
)
def test_intersect_line_plane_failure(line, plane):

    with pytest.raises(Exception):
        plane.intersect_line(line)


@pytest.mark.parametrize(
    "plane_a, plane_b, line_expected",
    [
        (
            Plane(Point([0]), Vector([0, 0, 1])),
            Plane(Point([0]), Vector([1, 0, 0])),
            Line(Point([0]), Vector([0, 1])),
        ),
        (
            Plane(Point([0, 0, 0]), Vector([0, 0, 1])),
            Plane(Point([0, 0, 1]), Vector([1, 0, 1])),
            Line(Point([1]), Vector([0, 1])),
        ),
        (
            Plane(Point([0, 0, 0]), Vector([-1, 1, 0])),
            Plane(Point([8, 0, 0]), Vector([1, 1, 0])),
            Line(Point([4, 4, 0]), Vector([0, 0, -1])),
        ),
    ],
)
def test_intersect_planes(plane_a, plane_b, line_expected):

    line_intersection = plane_a.intersect_plane(plane_b)
    assert line_intersection.is_close(line_expected)


@pytest.mark.parametrize(
    "plane_a, plane_b",
    [
        (
            Plane(Point([0, 0, 0]), Vector([1, 0, 0])),
            Plane(Point([0, 0, 0]), Vector([1, 0, 0])),
        ),
        (
            Plane(Point([1, 0, 0]), Vector([1, 0, 0])),
            Plane(Point([0, 0, 0]), Vector([1, 0, 0])),
        ),
        (
            Plane(Point([0, 0, 5]), Vector([0, 0, 1])),
            Plane(Point([4, 2, 4]), Vector([0, 0, 3])),
        ),
        (
            Plane(Point([0, 0, -5]), Vector([0, 0, 1])),
            Plane(Point([4, 2, 4]), Vector([0, 0, 3])),
        ),
    ],
)
def test_intersect_planes_failure(plane_a, plane_b):

    with pytest.raises(Exception):
        plane_a.intersect_plane(plane_b)
