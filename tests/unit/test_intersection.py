from math import sqrt

import numpy as np
import pytest

from skspatial.objects import Circle
from skspatial.objects import Cylinder
from skspatial.objects import Line
from skspatial.objects import Plane
from skspatial.objects import Point
from skspatial.objects import Sphere


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
            [-sqrt(3) / 2, 0.5],
            [sqrt(3) / 2, 0.5],
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
            -sqrt(2) / 2 * np.array([1, 1, 0]),
            sqrt(2) / 2 * np.array([1, 1, 0]),
        ),
        (
            Sphere([0, 0, 0], 1),
            Line([0, 0, 0], [1, 1, 1]),
            -sqrt(3) / 3 * np.ones(3),
            sqrt(3) / 3 * np.ones(3),
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


@pytest.mark.parametrize(
    "cylinder, line, array_expected_a, array_expected_b",
    [
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 0, 0], [1, 0, 0]),
            [-1, 0, 0],
            [1, 0, 0],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 0, 0.5], [1, 0, 0]),
            [-1, 0, 0.5],
            [1, 0, 0.5],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 2),
            Line([0, 0, 0], [1, 0, 0]),
            [-2, 0, 0],
            [2, 0, 0],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 5], 1),
            Line([0, 0, 0], [1, 0, 0]),
            [-1, 0, 0],
            [1, 0, 0],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 0, 0], [1, 1, 0]),
            [-sqrt(2) / 2, -sqrt(2) / 2, 0],
            [sqrt(2) / 2, sqrt(2) / 2, 0],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 0, 0], [1, 1, 1]),
            3 * [-sqrt(2) / 2],
            3 * [sqrt(2) / 2],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, -1, 0], [1, 0, 0]),
            [0, -1, 0],
            [0, -1, 0],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 1, 0], [1, 0, 0]),
            [0, 1, 0],
            [0, 1, 0],
        ),
        (
            Cylinder([1, 0, 0], [0, 0, 1], 1),
            Line([0, -1, 0], [1, 0, 0]),
            [1, -1, 0],
            [1, -1, 0],
        ),
    ],
)
def test_intersect_cylinder_line(cylinder, line, array_expected_a, array_expected_b):

    point_a, point_b = cylinder.intersect_line(line, n_digits=9)

    point_expected_a = Point(array_expected_a)
    point_expected_b = Point(array_expected_b)

    assert point_a.is_close(point_expected_a)
    assert point_b.is_close(point_expected_b)


@pytest.mark.parametrize(
    "cylinder, line",
    [
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, -2, 0], [1, 0, 0]),
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, -2, 0], [1, 0, 1]),
        ),
        (
            Cylinder([3, 10, 4], [-1, 2, -3], 3),
            Line([0, -2, 0], [1, 0, 1]),
        ),
    ],
)
def test_intersect_cylinder_line_failure(cylinder, line):

    message_expected = "The line does not intersect the cylinder."

    with pytest.raises(ValueError, match=message_expected):
        cylinder.intersect_line(line)
