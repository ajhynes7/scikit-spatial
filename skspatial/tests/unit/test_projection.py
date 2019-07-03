import numpy as np
import pytest

from skspatial.objects import Vector, Line, Plane


@pytest.mark.parametrize(
    "point, point_line, vector_line, point_expected, dist_expected",
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
def test_project_point_line(
    point, point_line, vector_line, point_expected, dist_expected
):
    line = Line(point_line, vector_line)

    point_projected = line.project_point(point)
    distance = line.distance_point(point)

    assert point_projected.is_close(point_expected)
    assert np.isclose(distance, dist_expected)


@pytest.mark.parametrize(
    "point, point_plane, normal_plane, point_expected, dist_expected",
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
def test_project_point_plane(
    point, point_plane, normal_plane, point_expected, dist_expected
):
    plane = Plane(point_plane, normal_plane)

    point_projected = plane.project_point(point)
    distance_signed = plane.distance_point_signed(point)

    assert point_projected.is_close(point_expected)
    assert np.isclose(distance_signed, dist_expected)


@pytest.mark.parametrize(
    "vector_u, vector_v, vector_expected",
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
def test_project_vector(vector_u, vector_v, vector_expected):
    """Test projecting vector u onto vector v."""

    vector_u_projected = Vector(vector_v).project_vector(vector_u)

    assert vector_u_projected.is_close(vector_expected)


@pytest.mark.parametrize(
    "line, vector, vector_expected",
    [
        (Line([0, 0], [1, 0]), [1, 1], [1, 0]),
        (Line([-56, 72], [1, 0]), [1, 1], [1, 0]),
        (Line([-56, 72], [200, 0]), [5, 9], [5, 0]),
        (Line([-56, 72], [200, 0]), [-5, 9], [-5, 0]),
    ],
)
def test_project_vector_line(line, vector, vector_expected):

    vector_projected = line.project_vector(vector)
    assert vector_projected.is_close(vector_expected)


@pytest.mark.parametrize(
    "plane, vector, vector_expected",
    [
        (Plane([0, 0, 0], [0, 0, 1]), [1, 1, 0], [1, 1, 0]),
        (Plane([0, 0, 0], [0, 0, 1]), [1, 1, 1], [1, 1, 0]),
        (Plane([0, 0, 0], [0, 0, 1]), [7, -5, 20], [7, -5, 0]),
        (Plane([0, 0, 0], [0, 0, -10]), [7, -5, 20], [7, -5, 0]),
    ],
)
def test_project_vector_plane(plane, vector, vector_expected):

    vector_projected = plane.project_vector(vector)
    assert vector_projected.is_close(vector_expected)
