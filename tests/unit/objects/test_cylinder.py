from math import isclose
from math import pi
from math import sqrt

import pytest

from skspatial.objects import Cylinder
from skspatial.objects import Line
from skspatial.objects import Point
from skspatial.objects import Points

LINE_DOES_NOT_INTERSECT_CYLINDER = "The line does not intersect the cylinder."
LINE_MUST_BE_3D = "The line must be 3D."


@pytest.mark.parametrize(
    ("point", "vector", "radius", "message_expected"),
    [
        ([0, 0], [1, 0, 0], 1, "The point must be 3D."),
        ([0, 0, 0], [1, 0], 1, "The vector must be 3D."),
        ([0, 0, 0], [0, 0, 0], 1, "The vector must not be the zero vector."),
        ([0, 0, 0], [0, 0, 1], 0, "The radius must be positive."),
    ],
)
def test_failure(point, vector, radius, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Cylinder(point, vector, radius)


@pytest.mark.parametrize(
    ("array_a", "array_b", "radius", "cylinder_expected"),
    [
        ([0, 0, 0], [0, 0, 1], 1, Cylinder([0, 0, 0], [0, 0, 1], 1)),
        ([0, 0, 1], [0, 0, 2], 1, Cylinder([0, 0, 1], [0, 0, 1], 1)),
        ([0, 0, 0], [1, 1, 1], 1, Cylinder([0, 0, 0], [1, 1, 1], 1)),
        ([2, 2, 2], [1, 1, 1], 5, Cylinder([2, 2, 2], [-1, -1, -1], 5)),
    ],
)
def test_from_points(array_a, array_b, radius, cylinder_expected):

    cylinder_from_points = Cylinder.from_points(array_a, array_b, radius)

    assert cylinder_from_points.vector.is_close(cylinder_expected.vector)
    assert cylinder_from_points.point.is_close(cylinder_expected.point)
    assert cylinder_from_points.radius == cylinder_expected.radius


@pytest.mark.parametrize(
    ("cylinder", "length_expected", "volume_expected"),
    [
        (Cylinder([0, 0, 0], [0, 0, 1], 1), 1, pi),
        (Cylinder([0, 0, 0], [0, 0, 1], 2), 1, 4 * pi),
        (Cylinder([0, 0, 0], [0, 0, 2], 1), 2, 2 * pi),
        (Cylinder([0, 0, 0], [0, 0, 2], 2), 2, 8 * pi),
        (Cylinder([1, 1, 1], [0, 0, 2], 2), 2, 8 * pi),
        (Cylinder([0, 0, 0], [0, 1, 1], 1), sqrt(2), sqrt(2) * pi),
        (Cylinder([0, 0, 0], [1, 1, 1], 1), sqrt(3), sqrt(3) * pi),
        (Cylinder([0, 0, 0], [5, 5, 5], 2), 5 * sqrt(3), 20 * sqrt(3) * pi),
    ],
)
def test_properties(cylinder, length_expected, volume_expected):

    assert isclose(cylinder.length(), length_expected)
    assert isclose(cylinder.volume(), volume_expected)


@pytest.mark.parametrize(
    ("cylinder", "lateral_surface_area_expected", "surface_area_expected"),
    [
        (Cylinder([0, 0, 0], [0, 0, 1], 1), 2 * pi, 4 * pi),
        (Cylinder([0, 0, 0], [0, 0, 2], 1), 4 * pi, 6 * pi),
        (Cylinder([0, 0, 0], [0, 0, 1], 2), 4 * pi, 12 * pi),
        (Cylinder([0, 0, 0], [0, 0, 2], 2), 8 * pi, 16 * pi),
        (Cylinder([0, 0, 0], [0, 0, -2], 2), 8 * pi, 16 * pi),
    ],
)
def test_surface_area(cylinder, lateral_surface_area_expected, surface_area_expected):

    assert isclose(cylinder.lateral_surface_area(), lateral_surface_area_expected)
    assert isclose(cylinder.surface_area(), surface_area_expected)


@pytest.mark.parametrize(
    ("cylinder", "point", "bool_expected"),
    [
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [0, 0, 0], True),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [0, 0, 1], True),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [0, 0, 0.9], True),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [0, 0, 1.1], False),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [0, 0, -0.1], False),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [1, 0, 0], True),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [2, 0, 0], False),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [-1, 0, 0], True),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [-2, 0, 0], False),
        (Cylinder([0, 0, 0], [0, 0, 1], 1), [1, 1, 0], False),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            [sqrt(2) / 2, sqrt(2) / 2, 0],
            True,
        ),
    ],
)
def test_cylinder_is_point_within(cylinder, point, bool_expected):

    assert cylinder.is_point_within(point) == bool_expected


@pytest.mark.parametrize(
    ("cylinder", "line", "array_expected_a", "array_expected_b"),
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
    ("cylinder", "line", "array_expected_a", "array_expected_b"),
    [
        # The line is parallel to the cylinder axis.
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 0, 0], [0, 0, 1]),
            [0, 0, 0],
            [0, 0, 1],
        ),
        # The line is perpendicular to the cylinder axis.
        (
            Cylinder([0, 0, 0], [0, 0, 2], 1),
            Line([0, 0, 1], [1, 0, 0]),
            [-1, 0, 1],
            [1, 0, 1],
        ),
        # The line touches the rim of one cylinder cap.
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([1, 0, 0], [1, 0, 1]),
            [1, 0, 0],
            [1, 0, 0],
        ),
        # The line touches the edge of the lateral surface.
        (
            Cylinder([0, 0, 0], [0, 0, 2], 1),
            Line([-1, 0, 1], [0, 1, 0]),
            [-1, 0, 1],
            [-1, 0, 1],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 2], 1),
            Line([-1, 0, 1], [0, 1, 1]),
            [-1, 0, 1],
            [-1, 0, 1],
        ),
        # The line intersects one cap and the lateral surface.
        (
            Cylinder([0, 0, 0], [0, 0, 5], 1),
            Line([0, 0, 0], [1, 0, 1]),
            [0, 0, 0],
            [1, 0, 1],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 5], 1),
            Line([0, 0, 5], [1, 0, -1]),
            [0, 0, 5],
            [1, 0, 4],
        ),
    ],
)
def test_intersect_cylinder_line_with_caps(cylinder, line, array_expected_a, array_expected_b):

    point_a, point_b = cylinder.intersect_line(line, infinite=False)

    point_expected_a = Point(array_expected_a)
    point_expected_b = Point(array_expected_b)

    assert point_a.is_close(point_expected_a)
    assert point_b.is_close(point_expected_b)


@pytest.mark.parametrize(
    ("cylinder", "line", "message_expected"),
    [
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, -2, 0], [1, 0, 0]),
            LINE_DOES_NOT_INTERSECT_CYLINDER,
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, -2, 0], [1, 0, 1]),
            LINE_DOES_NOT_INTERSECT_CYLINDER,
        ),
        (
            Cylinder([3, 10, 4], [-1, 2, -3], 3),
            Line([0, -2, 0], [1, 0, 1]),
            LINE_DOES_NOT_INTERSECT_CYLINDER,
        ),
        (
            Cylinder([3, 10, 4], [-1, 2, -3], 3),
            Line([0, 0], [1, 0]),
            LINE_MUST_BE_3D,
        ),
        (
            Cylinder([3, 10, 4], [-1, 2, -3], 3),
            Line(4 * [0], [1, 0, 0, 0]),
            LINE_MUST_BE_3D,
        ),
    ],
)
def test_intersect_cylinder_line_failure(cylinder, line, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        cylinder.intersect_line(line)


@pytest.mark.parametrize(
    ("cylinder", "line"),
    [
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            Line([0, 0, -1], [1, 0, 0]),
        ),
    ],
)
def test_intersect_cylinder_line_with_caps_failure(cylinder, line):

    message_expected = "The line does not intersect the cylinder."

    with pytest.raises(ValueError, match=message_expected):
        cylinder.intersect_line(line, infinite=False)


@pytest.mark.parametrize(
    ("cylinder", "n_along_axis", "n_angles", "points_expected"),
    [
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            1,
            1,
            [[-1, 0, 0]],
        ),
        (
            Cylinder([0, 0, 0], [0, 0, 1], 1),
            3,
            2,
            [[-1, 0, 0], [-1, 0, 0.5], [-1, 0, 1]],
        ),
        (
            Cylinder([0, 0, 0], [0.707, 0.707, 0], 1),
            1,
            3,
            [[-0.707, 0.707, 0], [0.707, -0.707, -0]],
        ),
    ],
)
def test_to_points(cylinder, n_along_axis, n_angles, points_expected):

    array_rounded = cylinder.to_points(n_along_axis=n_along_axis, n_angles=n_angles).round(3)
    points_unique = Points(array_rounded).unique()

    assert points_unique.is_close(points_expected)
