import math

import pytest

from skspatial._functions import _allclose
from skspatial.objects import Line
from skspatial.objects import Plane
from skspatial.objects import Points


@pytest.mark.parametrize(
    ("array_point", "array_a", "array_b", "plane_expected"),
    [
        ([0, 0], [1, 0], [0, 1], Plane([0, 0, 0], [0, 0, 1])),
        ([1, 2], [1, 0], [0, 1], Plane([1, 2, 0], [0, 0, 1])),
        ([0, 0], [0, 1], [1, 0], Plane([0, 0, 0], [0, 0, -1])),
        ([0, 0], [2, 0], [0, 1], Plane([0, 0, 0], [0, 0, 2])),
        ([0, 0], [2, 0], [0, 2], Plane([0, 0, 0], [0, 0, 4])),
        ([1, 2, 3], [2, 0], [0, 2], Plane([1, 2, 3], [0, 0, 4])),
        ([-3, 2, 6], [1, 4, 6], [-1, 5, 8], Plane([-3, 2, 6], [2, -14, 9])),
    ],
)
def test_from_vectors(array_point, array_a, array_b, plane_expected):

    plane = Plane.from_vectors(array_point, array_a, array_b)

    assert plane.is_close(plane_expected)

    # Also ensure that the vector is exactly as expected.
    assert plane.vector.is_close(plane_expected.vector)


@pytest.mark.parametrize(
    ("array_point", "array_a", "array_b"),
    [
        ([0, 0], [1, 0], [1, 0]),
        ([2, 3], [1, 0], [1, 0]),
        ([0, 0], [0, 1], [0, 1]),
        ([0, 0], [1, 1], [-1, -1]),
        ([0, 0], [5, 3], [-5, -3]),
        ([0, 0, 0], [1, 0, 0], [1, 0, 0]),
    ],
)
def test_from_vectors_failure(array_point, array_a, array_b):

    message_expected = "The vectors must not be parallel."

    with pytest.raises(ValueError, match=message_expected):
        Plane.from_vectors(array_point, array_a, array_b)


@pytest.mark.parametrize(
    ("point_a", "point_b", "point_c", "plane_expected"),
    [
        ([0, 0], [1, 0], [0, 1], Plane([0, 0, 0], [0, 0, 1])),
        # The spacing between the points is irrelevant.
        ([0, 0], [9, 0], [0, 9], Plane([0, 0, 0], [0, 0, 1])),
        # The first point is used as the plane point.
        ([0, 0.1], [1, 0], [0, 1], Plane([0, 0.1, 0], [0, 0, 1])),
        # The order of points is relevant.
        ([0, 0], [0, 1], [1, 0], Plane([0, 0, 0], [0, 0, -1])),
    ],
)
def test_from_points(point_a, point_b, point_c, plane_expected):

    plane = Plane.from_points(point_a, point_b, point_c)

    assert plane.point.is_close(plane_expected.point)
    assert plane.is_close(plane_expected)


@pytest.mark.parametrize(
    ("point_a", "point_b", "point_c"),
    [
        ([0, 0], [0, 0], [0, 0]),
        ([0, 0], [0, 1], [0, 2]),
        ([-2, 1], [0, 2], [2, 3]),
        ([0, 0, 0], [1, 1, 1], [-2, -2, -2]),
        ([0, 1, 2], [1, 2, 3], [4, 5, 6]),
    ],
)
def test_from_points_failure(point_a, point_b, point_c):

    message_expected = "The points must not be collinear."

    with pytest.raises(ValueError, match=message_expected):
        Plane.from_points(point_a, point_b, point_c)


@pytest.mark.parametrize(
    ("plane", "coeffs_expected"),
    [
        (Plane([-1, 2], [22, -3]), [22, -3, 0, 28]),
        (Plane([0, 0, 0], [0, 0, 1]), [0, 0, 1, 0]),
        (Plane([0, 0, 0], [0, 0, 25]), [0, 0, 25, 0]),
        (Plane([1, 2, 0], [5, 4, 6]), [5, 4, 6, -13]),
        (Plane([-4, 5, 8], [22, -3, 6]), [22, -3, 6, 55]),
    ],
)
def test_cartesian(plane, coeffs_expected):
    """Test the coefficients of the Cartesian plane equation."""

    assert _allclose(plane.cartesian(), coeffs_expected).all()


@pytest.mark.parametrize(
    "plane",
    [
        Plane([0, 0, 0, 0], [1, 2, 3, 4]),
        Plane([1, 2, 3, 4], [1, 2, 3, 4]),
    ],
)
def test_cartesian_failure(plane):

    with pytest.raises(ValueError, match="The plane dimension must be <= 3."):
        plane.cartesian()


@pytest.mark.parametrize(
    ("point", "point_plane", "normal_plane", "point_expected", "dist_expected"),
    [
        ([0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0], 0),
        ([0, 0, 0], [0, 0, 0], [0, 0, -1], [0, 0, 0], 0),
        ([0, 0, 1], [0, 0, 0], [0, 0, 1], [0, 0, 0], 1),
        ([0, 0, 1], [0, 0, 0], [0, 0, -1], [0, 0, 0], -1),
        ([0, 0, 1], [0, 0, 0], [0, 0, 50], [0, 0, 0], 1),
        ([0, 0, 1], [0, 0, 0], [0, 0, -50], [0, 0, 0], -1),
        ([0, 0, 5], [0, 0, 0], [0, 0, 50], [0, 0, 0], 5),
        ([0, 0, 5], [0, 0, 0], [0, 0, -50], [0, 0, 0], -5),
        ([5, -4, 1], [0, 0, 0], [0, 0, 1], [5, -4, 0], 1),
    ],
)
def test_project_point(point, point_plane, normal_plane, point_expected, dist_expected):
    plane = Plane(point_plane, normal_plane)

    point_projected = plane.project_point(point)
    distance_signed = plane.distance_point_signed(point)

    assert point_projected.is_close(point_expected)
    assert math.isclose(distance_signed, dist_expected)


@pytest.mark.parametrize(
    ("plane", "vector", "vector_expected"),
    [
        (Plane([0, 0, 0], [0, 0, 1]), [1, 1, 0], [1, 1, 0]),
        (Plane([0, 0, 0], [0, 0, 1]), [1, 1, 1], [1, 1, 0]),
        (Plane([0, 0, 0], [0, 0, 1]), [7, -5, 20], [7, -5, 0]),
        (Plane([0, 0, 0], [0, 0, -10]), [7, -5, 20], [7, -5, 0]),
    ],
)
def test_project_vector(plane, vector, vector_expected):

    vector_projected = plane.project_vector(vector)
    assert vector_projected.is_close(vector_expected)


@pytest.mark.parametrize(
    ("plane", "line", "line_expected"),
    [
        (
            Plane([0, 0, 0], [0, 0, 1]),
            Line([0, 0, 0], [1, 0, 0]),
            Line([0, 0, 0], [1, 0, 0]),
        ),
        (
            Plane([0, 0, 0], [0, 0, 1]),
            Line([0, 0, 5], [1, 0, 0]),
            Line([0, 0, 0], [1, 0, 0]),
        ),
        (
            Plane([0, 0, 0], [0, 0, 1]),
            Line([2, 3, -5], [1, 0, 0]),
            Line([2, 3, 0], [1, 0, 0]),
        ),
        (
            Plane([0, 0, 0], [1, 0, 0]),
            Line([1, 0, 0], [0, 1, 0]),
            Line([0, 0, 0], [0, 1, 0]),
        ),
        (
            Plane([0, 0, 0], [0, -1, 1]),
            Line([0, 0, 0], [0, 1, 0]),
            Line([0, 0, 0], [0, 0.5, 0.5]),
        ),
        (
            Plane([0, 1, 0], [0, 1, 0]),
            Line([0, -1, 0], [1, -2, 0]),
            Line([0, 1, 0], [1, 0, 0]),
        ),
    ],
)
def test_project_line(plane, line, line_expected):

    line_projected = plane.project_line(line)

    assert line_projected.point.is_close(line_expected.point)
    assert line_projected.vector.is_close(line_expected.vector)


@pytest.mark.parametrize(
    ("plane", "line"),
    [
        (
            Plane([0, 0, 0], [0, 0, 1]),
            Line([0, 0, 0], [0, 0, 1]),
        ),
        (
            Plane([0, 0, 5], [-1, 0, 0]),
            Line([0, 0, 0], [5, 0, 0]),
        ),
        (
            Plane([1, 2, 3], [1, 2, 4]),
            Line([4, 5, 6], [-2, -4, -8]),
        ),
    ],
)
def test_project_line_failure(plane, line):

    message_expected = "The line and plane must not be perpendicular."

    with pytest.raises(ValueError, match=message_expected):
        plane.project_line(line)


@pytest.mark.parametrize(
    ("point", "plane", "dist_signed_expected"),
    [
        ([0, 0, 0], Plane([0, 0, 0], [0, 0, 1]), 0),
        ([50, -67, 0], Plane([0, 0, 0], [0, 0, 1]), 0),
        ([50, -67, 0], Plane([0, 0, 1], [0, 0, 1]), -1),
        ([5, 3, 8], Plane([0, 0, 0], [0, 0, 1]), 8),
        ([5, 3, 7], Plane([0, 0, 0], [0, 0, -50]), -7),
        ([5, 3, -8], Plane([0, 0, 0], [0, 0, 1]), -8),
    ],
)
def test_distance_point(point, plane, dist_signed_expected):

    assert math.isclose(plane.distance_point_signed(point), dist_signed_expected)
    assert math.isclose(plane.distance_point(point), abs(dist_signed_expected))


@pytest.mark.parametrize(
    ("plane", "point", "value_expected"),
    [
        (Plane([0, 0], [1, 1]), [2, 2], 1),
        (Plane([0, 0], [1, 1]), [0, 0], 0),
        (Plane([0, 1], [1, 1]), [0, 0], -1),
        (Plane([0, 0, 0], [1, 0, 0]), [0, 0, 0], 0),
        (Plane([0, 0, 0], [1, 0, 0]), [1, 0, 0], 1),
        (Plane([0, 0, 0], [1, 0, 0]), [-1, 0, 0], -1),
        (Plane([0, 0, 0], [1, 0, 0]), [25, 53, -105], 1),
        (Plane([0, 0, 0], [1, 0, 0]), [-2, 53, -105], -1),
        (Plane([0, 0, 0], [1, 0, 0]), [0, 38, 19], 0),
        (Plane([0, 0, 0], [1, 0, 0]), [0, 101, -45], 0),
        (Plane([0, 0, 0], [-1, 0, 0]), [1, 0, 0], -1),
        (Plane([5, 0, 0], [1, 0, 0]), [1, 0, 0], -1),
    ],
)
def test_side_point(plane, point, value_expected):

    assert plane.side_point(point) == value_expected


@pytest.mark.parametrize(
    ("line", "plane", "array_expected"),
    [
        (Line([0, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [1, 0, 0]), [0, 0, 0]),
        (Line([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, 1]), [0, 0, 0]),
        (Line([5, -3, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, 1]), [5, -3, 0]),
    ],
)
def test_intersect_line(line, plane, array_expected):

    point_intersection = plane.intersect_line(line)
    assert point_intersection.is_close(array_expected)


@pytest.mark.parametrize(
    ("line", "plane"),
    [
        (Line([0, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [0, 0, 1])),
        (Line([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [1, 0, 0])),
        (Line([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 1, 0])),
    ],
)
def test_intersect_line_failure(line, plane):

    message_expected = "The line and plane must not be parallel."

    with pytest.raises(ValueError, match=message_expected):
        plane.intersect_line(line)


@pytest.mark.parametrize(
    ("plane_a", "plane_b", "line_expected"),
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
def test_intersect_plane(plane_a, plane_b, line_expected):

    line_intersection = plane_a.intersect_plane(plane_b)
    assert line_intersection.is_close(line_expected)


@pytest.mark.parametrize(
    ("plane_a", "plane_b"),
    [
        (Plane([0, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [1, 0, 0])),
        (Plane([1, 0, 0], [1, 0, 0]), Plane([0, 0, 0], [1, 0, 0])),
        (Plane([0, 0, 5], [0, 0, 1]), Plane([4, 2, 4], [0, 0, 3])),
        (Plane([0, 0, -5], [0, 0, 1]), Plane([4, 2, 4], [0, 0, 3])),
    ],
)
def test_intersect_plane_failure(plane_a, plane_b):

    message_expected = "The planes must not be parallel."

    with pytest.raises(Exception, match=message_expected):
        plane_a.intersect_plane(plane_b)


@pytest.mark.parametrize(
    ("plane", "points", "error_expected"),
    [
        (Plane([0, 0, 0], [0, 0, 1]), [[25, 3, 0], [-6, 5, 0]], 0),
        (Plane([25, 9, 0], [0, 0, 1]), [[25, 3, 0], [-6, 5, 0]], 0),
        (Plane([25, 9, -2], [0, 0, 1]), [[25, 3, 0], [-6, 5, 0]], 8),
        (Plane([0, 0, 0], [0, 0, 1]), [[25, 3, 2], [-6, 5, 0]], 4),
        (Plane([0, 0, 0], [0, 0, 5]), [[25, 3, 2], [-6, 5, 0]], 4),
        (Plane([0, 0, 0], [0, 0, -5]), [[25, 3, 2], [-6, 5, 0]], 4),
    ],
)
def test_sum_squares_plane(plane, points, error_expected):

    error = plane.sum_squares(points)
    assert math.isclose(error, error_expected)


@pytest.mark.parametrize(
    ("points", "plane_expected"),
    [
        # The points are coplanar.
        ([[0, 0], [1, 1], [0, 2]], Plane([1 / 3, 1, 0], [0, 0, 1])),
        ([[0, 0], [0, 1], [1, 0], [1, 1]], Plane([0.5, 0.5, 0], [0, 0, 1])),
        ([[0, 0, 0], [1, 0, 0], [0, 0, 1]], Plane([1 / 3, 0, 1 / 3], [0, 1, 0])),
        (
            [[1, 0, 0], [-1, 0, 0], [1, 1, 1], [-1, 1, 1]],
            Plane([0, 0.5, 0.5], [0, 1, -1]),
        ),
        (
            [[1, 0, 1], [1, 1, 1], [-1, 0, -1], [-1, 1, -1]],
            Plane([0, 0.5, 0], [1, 0, -1]),
        ),
        (
            [[1, 0, 1], [1, 1, 1], [-1, 0, -1], [-1, 1, -1], [0, 0, 0]],
            Plane([0, 0.4, 0], [1, 0, -1]),
        ),
        # The points are not coplanar.
        (
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
            Plane([0.25, 0.25, 0.25], [1, 1, 1]),
        ),
        (
            [
                [0, 0, 0],
                [1, 0, 0],
                [2, 0, 0],
                [0, 1, 0],
                [1, 1, 0],
                [2, 1, 0],
                [0, 2, 0],
                [1, 2, 0],
                [2, 2, 0],
                [0, 0, 1],
                [1, 0, 1],
                [2, 0, 1],
                [0, 1, 1],
                [1, 1, 1],
                [2, 1, 1],
                [0, 2, 1],
                [1, 2, 1],
                [2, 2, 1],
            ],
            Plane([1, 1, 0.5], [0, 0, 1]),
        ),
    ],
)
def test_best_fit(points, plane_expected):

    points = Points(points).set_dimension(3)
    plane_fit = Plane.best_fit(points)

    assert plane_fit.is_close(plane_expected)
    assert plane_fit.point.is_close(plane_expected.point)


@pytest.mark.parametrize(
    ("points", "message_expected"),
    [
        ([[0, 0], [1, 0]], "The points must be 3D."),
        ([[0, 0], [2, 5]], "The points must be 3D."),
        (
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            "The points must not be collinear.",
        ),
        (
            [[0, 0, 0], [1, 1, 1], [-10, -10, -10]],
            "The points must not be collinear.",
        ),
    ],
)
def test_best_fit_failure(points, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Plane.best_fit(points)


@pytest.mark.parametrize(
    ("plane", "points_expected"),
    [
        (Plane([0, 0, 0], [0, 0, 1]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([1, 0, 0], [0, 0, 1]), [[0, -1, 0], [2, -1, 0], [0, 1, 0], [2, 1, 0]]),
        (
            Plane([0, 0, 0], [0, 0, -1]),
            [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]],
        ),
        (Plane([0, 0, 0], [0, 0, 5]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([0, 0, 0], [0, 1, 0]), [[-1, 0, -1], [1, 0, -1], [-1, 0, 1], [1, 0, 1]]),
        (Plane([0, 0, 0], [1, 0, 0]), [[0, -1, -1], [0, 1, -1], [0, -1, 1], [0, 1, 1]]),
        (
            Plane([0, 0, 0], [1, 1, 0]),
            [[-1, 1, -1], [1, -1, -1], [-1, 1, 1], [1, -1, 1]],
        ),
    ],
)
def test_to_points(plane, points_expected):

    points = plane.to_points()

    assert points.is_close(points_expected)
