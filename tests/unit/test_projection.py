import numpy as np
import pytest

from skspatial.objects import Point, Vector, Line, Plane


@pytest.mark.parametrize(
    "array_u, array_v, array_expected",
    [
        ([1, 1], [1, 0], [1, 0]),
        ([1, 5], [1, 0], [1, 0]),
        ([5, 5], [1, 0], [5, 0]),
        # Scaling v by a non-zero scalar doesn't change the projection.
        ([0, 1], [0, 1], [0, 1]),
        ([0, 1], [0, -5], [0, 1]),
        ([0, 1], [0, 15], [0, 1]),
        # The projection is the zero vector if u and v are perpendicular.
        ([1, 0], [0, 1], [0, 0]),
        ([5, 0], [0, 9], [0, 0]),
        # The projection of the zero vector onto v is the zero vector.
        ([0, 0], [0, 1], [0, 0]),
    ],
)
def test_project_vector(array_u, array_v, array_expected):
    """Test projecting vector u onto vector v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)
    vector_expected = Vector(array_expected)

    vector_u_projected = vector_v.project(vector_u)

    assert vector_u_projected.is_close(vector_expected)


@pytest.mark.parametrize(
    "array_point, array_point_line, array_vector_line, \
     array_point_expected, dist_expected",
    [
        ([0, 5], [0, 0], [0, 1], [0, 5], 0),
        ([0, 5], [0, 0], [0, 100], [0, 5], 0),
        ([1, 5], [0, 0], [0, 100], [0, 5], 1),
        ([0, 1], [0, 0], [1, 1], [0.5, 0.5], np.sqrt(2) / 2),
        ([1, 0], [0, 0], [1, 1], [0.5, 0.5], np.sqrt(2) / 2),
        ([0, 2], [0, 0], [1, 1], [1, 1], np.sqrt(2)),
        ([-15, 5], [0, 0], [0, 100], [0, 5], 15),
        ([50, 10], [1, -5], [0, 3], [1, 10], 49),
    ],
)
def test_point_line(
    array_point,
    array_point_line,
    array_vector_line,
    array_point_expected,
    dist_expected,
):
    """Test functions related to a point and a line."""
    point = Point(array_point)
    point_expected = Point(array_point_expected)

    line = Line(Point(array_point_line), Vector(array_vector_line))

    point_projected = line.project(point)
    distance = line.distance(point)

    assert point_projected.is_close(point_expected)
    assert np.isclose(distance, dist_expected)


@pytest.mark.parametrize(
    "array_point, array_point_plane, array_normal_plane, \
     array_point_expected, dist_expected",
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
def test_point_plane(
    array_point,
    array_point_plane,
    array_normal_plane,
    array_point_expected,
    dist_expected,
):
    """Test functions related to a point and a plane."""
    point = Point(array_point)
    point_expected = Point(array_point_expected)

    plane = Plane(Point(array_point_plane), Vector(array_normal_plane))

    point_projected = plane.project(point)
    distance_signed = plane.distance_signed(point)

    assert point_projected.is_close(point_expected)
    assert np.isclose(distance_signed, dist_expected)
