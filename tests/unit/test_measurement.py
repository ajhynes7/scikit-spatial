import numpy as np
import pytest

from skspatial.measurement import area_triangle, volume_tetrahedron
from skspatial.objects import Point, Vector, Line, Plane


@pytest.mark.parametrize(
    "array_u, array_v, angle_expected",
    [
        ([1, 0], [1, 0], 0),
        ([1, 0], [np.sqrt(3) / 2, 0.5], np.pi / 6),
        ([1, 0], [1, 1], np.pi / 4),
        ([1, 0], [0, 1], np.pi / 2),
        ([1, 0], [0, -1], np.pi / 2),
        ([1, 0], [-1, 0], np.pi),
        ([1, 0, 0], [0, 1, 0], np.pi / 2),
    ],
)
def test_angle_between(array_u, array_v, angle_expected):
    """Test finding the angle between vectors u and v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)

    angle = vector_u.angle_between(vector_v)
    assert np.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    "point_a, point_b, dist_expected",
    [
        (Point([0, 0]), Point([0, 0]), 0),
        (Point([0, 0]), Point([1, 0]), 1),
        (Point([0, 0]), Point([-1, 0]), 1),
        (Point([0, 0]), Point([1, 1]), np.sqrt(2)),
        (Point([0, 0]), Point([5, 5]), 5 * np.sqrt(2)),
        (Point([0, 0]), Point([-5, 5]), 5 * np.sqrt(2)),
        (Point([1, 5, 3]), Point([1, 5, 4]), 1),
    ],
)
def test_distance_points(point_a, point_b, dist_expected):

    assert np.isclose(point_a.distance_point(point_b), dist_expected)


@pytest.mark.parametrize(
    "point, line, dist_expected",
    [
        (Point([0, 0]), Line(Point([0, 0]), Vector([1, 0])), 0),
        (Point([8, 7]), Line(Point([0, 0]), Vector([1, 0])), 7),
        (Point([20, -3]), Line(Point([0, 0]), Vector([1, 0])), 3),
        (Point([20, -3, 1]), Line(Point([0, 0]), Vector([1, 0])), np.sqrt(10)),
    ],
)
def test_distance_point_line(point, line, dist_expected):

    assert np.isclose(line.distance_point(point), dist_expected)


@pytest.mark.parametrize(
    "point, plane, dist_signed_expected",
    [
        (Point([0, 0]), Plane(Point([0, 0]), Vector([0, 0, 1])), 0),
        (Point([50, -67]), Plane(Point([0, 0]), Vector([0, 0, 1])), 0),
        (Point([50, -67]), Plane(Point([0, 0, 1]), Vector([0, 0, 1])), -1),
        (Point([5, 3, 8]), Plane(Point([0, 0]), Vector([0, 0, 1])), 8),
        (Point([5, 3, 7]), Plane(Point([0, 0]), Vector([0, 0, -50])), -7),
        (Point([5, 3, -8]), Plane(Point([0, 0]), Vector([0, 0, 1])), -8),
    ],
)
def test_distance_point_plane(point, plane, dist_signed_expected):

    assert np.isclose(plane.distance_point_signed(point), dist_signed_expected)
    assert np.isclose(plane.distance_point(point), abs(dist_signed_expected))


@pytest.mark.parametrize(
    "line_a, line_b, dist_expected",
    [
        # The lines intersect.
        (
            Line(Point([10, 2]), Vector([1, 1])),
            Line(Point([5, -3]), Vector([-1, 0])),
            0,
        ),
        (Line(Point([0, 0]), Vector([1, 1])), Line(Point([1, 0]), Vector([1, 2])), 0),
        # The lines are parallel.
        (Line(Point([0, 0]), Vector([1, 0])), Line(Point([0, 0]), Vector([-1, 0])), 0),
        (Line(Point([0, 0]), Vector([1, 0])), Line(Point([0, 0]), Vector([1, 0])), 0),
        (
            Line(Point([24, 0]), Vector([0, 1])),
            Line(Point([3, 0]), Vector([0, -5])),
            21,
        ),
        (
            Line(Point([0, 0]), Vector([1, 1])),
            Line(Point([1, 0]), Vector([1, 1])),
            np.sqrt(2) / 2,
        ),
        # The lines are skew.
        (
            Line(Point([0, 0, 0]), Vector([0, 1, 0])),
            Line(Point([1, 0, 0]), Vector([0, -4, 13])),
            1,
        ),
    ],
)
def test_distance_lines(line_a, line_b, dist_expected):

    assert np.isclose(line_a.distance_line(line_b), dist_expected)


@pytest.mark.parametrize(
    "array_a, array_b, array_c, area_expected",
    [
        ([0, 0], [1, 0], [0, 1], 0.5),
        ([0, 0], [1, 1], [2, 0], 1),
        ([0, 0], [1, 10], [2, 0], 10),
        ([0, 0], [1, 0], [2, 0], 0),
        ([0, 0], [-5, -2], [5, 2], 0),
        ([1, 0, 0], [0, 1, 0], [0, 0, 1], np.sin(np.pi / 3)),
        ([2, 0, 0], [0, 2, 0], [0, 0, 2], 4 * np.sin(np.pi / 3)),
    ],
)
def test_area_triangle(array_a, array_b, array_c, area_expected):

    point_a = Point(array_a)
    point_b = Point(array_b)
    point_c = Point(array_c)

    area = area_triangle(point_a, point_b, point_c)

    assert np.isclose(area, area_expected)


@pytest.mark.parametrize(
    "array_a, array_b, array_c, array_d, volume_expected",
    [
        ([0, 0], [2, 0], [1, 1], [10, -7], 0),
        ([0, 0], [2, 0], [1, 1], [0, 0, 1], 1 / 3),
        ([0, 0], [2, 0], [1, 1], [0, 0, -1], 1 / 3),
        ([0, 0], [2, 0], [1, 1], [0, 0, 2], 2 / 3),
        ([0, 0], [2, 0], [1, 1], [0, 0, 3], 1),
        ([0, 0], [2, 0], [1, 1], [-56, 10, 3], 1),
        ([0, 1, 1], [0, 1, 5], [0, -5, 7], [0, 5, 2], 0),
    ],
)
def test_volume_tetrahedron(array_a, array_b, array_c, array_d, volume_expected):

    point_a = Point(array_a)
    point_b = Point(array_b)
    point_c = Point(array_c)
    point_d = Point(array_d)

    volume = volume_tetrahedron(point_a, point_b, point_c, point_d)

    assert np.isclose(volume, volume_expected)
