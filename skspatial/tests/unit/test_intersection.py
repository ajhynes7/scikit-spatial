import numpy as np
import pytest

from skspatial.objects import Line, Plane, Circle, Sphere


@pytest.mark.parametrize(
    "line_a, line_b, array_expected",
    [
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 1]), [0, 0]),
        (Line([0, 0], [1, 0]), Line([5, 5], [1, 1]), [0, 0]),
        (Line([0, 0], [1, 0]), Line([9, 0], [1, 1]), [9, 0]),
        (Line([0, 0], [1, 1]), Line([4, 0], [1, -1]), [2, 2]),
        (Line([0, 0, 0], [1, 1, 1]), Line([4, 4, 0], [-1, -1, 1]), [2, 2, 2]),
    ],
)
def test_intersect_lines(line_a, line_b, array_expected):

    point_intersection = line_a.intersect_line(line_b)
    assert point_intersection.is_close(array_expected)


@pytest.mark.parametrize(
    "line_a, line_b",
    [
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 0])),
        (Line([0, 0], [1, 0]), Line([5, 5], [1, 0])),
        (Line([0, 0], [0, 1]), Line([0, 0], [0, 5])),
        (Line([0, 0], [1, 0]), Line([0, 0], [-1, 0])),
        (Line([0, 0], [1, 0]), Line([5, 5], [-1, 0])),
        (Line([0, 0, 0], [1, 1, 1]), Line([0, 1, 0], [-1, 0, 0])),
    ],
)
def test_intersect_lines_failure(line_a, line_b):

    with pytest.raises(Exception):
        line_a.intersect_line(line_b)


@pytest.mark.parametrize(
    "line, plane, array_expected",
    [
        (Line([0, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [1, 0, 0]), [0, 0, 0]),
        (Line([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, 1]), [0, 0, 0]),
        (Line([5, -3, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, 1]), [5, -3, 0]),
    ],
)
def test_intersect_line_plane(line, plane, array_expected):

    point_intersection = plane.intersect_line(line)
    assert point_intersection.is_close(array_expected)


@pytest.mark.parametrize(
    "line, plane",
    [
        (Line([0, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [0, 0, 1])),
        (Line([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [1, 0, 0])),
        (Line([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 1, 0])),
    ],
)
def test_intersect_line_plane_failure(line, plane):

    with pytest.raises(Exception):
        plane.intersect_line(line)


@pytest.mark.parametrize(
    "plane_a, plane_b, line_expected",
    [
        (
            Plane([0, 0, 0], [0, 0, 1]),
            Plane([0, 0, 0], [1, 0, 0]),
            Line([0, 0, 0], [0, 1, 0]),
        ),
        (
            Plane([0, 0, 0], [0, 0, 1]),
            Plane([0, 0, 1], [1, 0, 1]),
            Line([1, 0, 0], [0, 1, 0]),
        ),
        (
            Plane([0, 0, 0], [-1, 1, 0]),
            Plane([8, 0, 0], [1, 1, 0]),
            Line([4, 4, 0], [0, 0, -1]),
        ),
    ],
)
def test_intersect_planes(plane_a, plane_b, line_expected):

    line_intersection = plane_a.intersect_plane(plane_b)
    assert line_intersection.is_close(line_expected)


@pytest.mark.parametrize(
    "plane_a, plane_b",
    [
        (Plane([0, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [1, 0, 0])),
        (Plane([1, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [1, 0, 0])),
        (Plane([0, 0, 5], [0, 0, 1]), Plane([4, 2, 4], [0, 0, 3])),
        (Plane([0, 0, -5], [0, 0, 1]), Plane([4, 2, 4], [0, 0, 3])),
    ],
)
def test_intersect_planes_failure(plane_a, plane_b):

    with pytest.raises(Exception):
        plane_a.intersect_plane(plane_b)


@pytest.mark.parametrize(
    "circle, line, point_a_expected, point_b_expected",
    [
        (Circle([0, 0], 1), Line([0, 0], [1, 0]), [-1, 0], [1, 0]),
        (Circle([0, 0], 1), Line([0, 0], [0, 1]), [0, -1], [0, 1]),
        (Circle([0, 0], 1), Line([0, 1], [1, 0]), [0, 1], [0, 1]),
        (
            Circle([0, 0], 1),
            Line([0, 0.5], [1, 0]),
            [-np.sqrt(3) / 2, 0.5],
            [np.sqrt(3) / 2, 0.5],
        ),
        (Circle([1, 0], 1), Line([0, 0], [1, 0]), [0, 0], [2, 0]),
    ],
)
def test_intersect_circle_line(circle, line, point_a_expected, point_b_expected):

    point_a, point_b = circle.intersect_line(line)

    assert point_a.is_close(point_a_expected)
    assert point_b.is_close(point_b_expected)


@pytest.mark.parametrize(
    "circle, line",
    [
        # The circle does not intersect the line.
        (Circle([0, 0], 1), Line([0, 2], [1, 0])),
        (Circle([0, 0], 1), Line([0, -2], [1, 0])),
        (Circle([0, 0], 1), Line([2, 0], [0, 1])),
        (Circle([0, 0], 1), Line([3, 0], [1, 1])),
        (Circle([1.5, 0], 1), Line([0, 0], [1, 0])),
    ],
)
def test_intersect_circle_line_failure(circle, line):

    with pytest.raises(Exception):
        circle.intersect_line(line)


@pytest.mark.parametrize(
    "sphere, line, point_a_expected, point_b_expected",
    [
        (Sphere([0, 0, 0], 1), Line([0, 0, 0], [1, 0, 0]), [-1, 0, 0], [1, 0, 0]),
        (
            Sphere([0, 0, 0], 1),
            Line([0, 0, 0], [1, 1, 0]),
            -np.sqrt(2) / 2 * np.array([1, 1, 0]),
            np.sqrt(2) / 2 * np.array([1, 1, 0]),
        ),
        (
            Sphere([0, 0, 0], 1),
            Line([0, 0, 0], [1, 1, 1]),
            -np.sqrt(3) / 3 * np.ones(3),
            np.sqrt(3) / 3 * np.ones(3),
        ),
        (Sphere([1, 0, 0], 1), Line([0, 0, 0], [1, 0, 0]), [0, 0, 0], [2, 0, 0]),
        (Sphere([0, 0, 0], 1), Line([1, 0, 0], [0, 0, 1]), [1, 0, 0], [1, 0, 0]),
    ],
)
def test_intersect_sphere_line(sphere, line, point_a_expected, point_b_expected):

    point_a, point_b = sphere.intersect_line(line)

    assert point_a.is_close(point_a_expected)
    assert point_b.is_close(point_b_expected)


@pytest.mark.parametrize(
    "sphere, line",
    [
        (Sphere([0, 0, 0], 1), Line([0, 0, 2], [1, 0, 0])),
        (Sphere([0, 0, 0], 1), Line([0, 0, -2], [1, 0, 0])),
        (Sphere([0, 2, 0], 1), Line([0, 0, 0], [1, 0, 0])),
        (Sphere([0, -2, 0], 1), Line([0, 0, 0], [1, 0, 0])),
        (Sphere([5, 0, 0], 1), Line([0, 0, 0], [1, 1, 1])),
    ],
)
def test_intersect_sphere_line_failure(sphere, line):

    with pytest.raises(Exception):
        sphere.intersect_line(line)
