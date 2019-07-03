import numpy as np
import pytest

from skspatial.measurement import area_triangle, volume_tetrahedron
from skspatial.objects import Point, Vector, Line, Plane


@pytest.mark.parametrize(
    "array_u, array_v, similarity_expected",
    [
        ([1, 0], [1, 0], 1),
        ([1, 0], [0, 1], 0),
        ([1, 0], [-1, 0], -1),
        ([1, 0], [0, -1], 0),
        ([1, 0], [1, 1], np.sqrt(2) / 2),
        ([1, 0], [-1, 1], -np.sqrt(2) / 2),
        ([1, 0], [-1, -1], -np.sqrt(2) / 2),
        ([1, 0], [1, -1], np.sqrt(2) / 2),
        ([1, 0], [0.5, np.sqrt(3) / 2], 0.5),
        ([1, 0], [np.sqrt(3) / 2, 0.5], np.sqrt(3) / 2),
        ([1, 1], [0, 0], None),
        ([0, 0], [1, 1], None),
    ],
)
def test_cosine_similarity(array_u, array_v, similarity_expected):

    if similarity_expected is None:
        with pytest.raises(
            ValueError, match="The vectors must have non-zero magnitudes."
        ):
            Vector(array_u).cosine_similarity(array_v)

    else:
        similarity = Vector(array_u).cosine_similarity(array_v)
        assert np.isclose(similarity, similarity_expected)


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

    angle = Vector(array_u).angle_between(array_v)
    assert np.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    "array_u, array_v, angle_expected",
    [
        ([1, 0], [1, 0], 0),
        ([1, 0], [1, 1], np.pi / 4),
        ([1, 0], [0, 1], np.pi / 2),
        ([1, 0], [-1, 1], 3 * np.pi / 4),
        ([1, 0], [-1, 0], np.pi),
        ([1, 0], [-1, -1], -3 * np.pi / 4),
        ([1, 0], [0, -1], -np.pi / 2),
        ([1, 0], [1, -1], -np.pi / 4),
        ([1, 1], [0, 1], np.pi / 4),
        ([1, 1], [1, 0], -np.pi / 4),
        ([0], [0], None),
        ([1, 1, 1], [1, 0, 0], None),
        (np.ones(4), np.ones(4), None),
    ],
)
def test_angle_signed(array_u, array_v, angle_expected):

    if angle_expected is None:
        with pytest.raises(ValueError, match="The vectors must be 2D."):
            Vector(array_u).angle_signed(array_v)

    else:
        angle = Vector(array_u).angle_signed(array_v)
        assert np.isclose(angle, angle_expected)


@pytest.mark.parametrize(
    "array_a, array_b, dist_expected",
    [
        ([0, 0], [0, 0], 0),
        ([0, 0], [1, 0], 1),
        ([0, 0], [-1, 0], 1),
        ([0, 0], [1, 1], np.sqrt(2)),
        ([0, 0], [5, 5], 5 * np.sqrt(2)),
        ([0, 0], [-5, 5], 5 * np.sqrt(2)),
        ([1, 5, 3], [1, 5, 4], 1),
    ],
)
def test_distance_points(array_a, array_b, dist_expected):

    point_a = Point(array_a)
    assert np.isclose(point_a.distance_point(array_b), dist_expected)


@pytest.mark.parametrize(
    "array_point, line, dist_expected",
    [
        ([0, 0], Line([0, 0], [1, 0]), 0),
        ([8, 7], Line([0, 0], [1, 0]), 7),
        ([20, -3], Line([0, 0], [1, 0]), 3),
        ([20, -3, 1], Line([0, 0, 0], [1, 0, 0]), np.sqrt(10)),
    ],
)
def test_distance_point_line(array_point, line, dist_expected):

    assert np.isclose(line.distance_point(array_point), dist_expected)


@pytest.mark.parametrize(
    "point, plane, dist_signed_expected",
    [
        ([0, 0, 0], Plane([0, 0, 0], [0, 0, 1]), 0),
        ([50, -67, 0], Plane([0, 0, 0], [0, 0, 1]), 0),
        ([50, -67, 0], Plane([0, 0, 1], [0, 0, 1]), -1),
        ([5, 3, 8], Plane([0, 0, 0], [0, 0, 1]), 8),
        ([5, 3, 7], Plane([0, 0, 0], [0, 0, -50]), -7),
        ([5, 3, -8], Plane([0, 0, 0], [0, 0, 1]), -8),
    ],
)
def test_distance_point_plane(point, plane, dist_signed_expected):

    assert np.isclose(plane.distance_point_signed(point), dist_signed_expected)
    assert np.isclose(plane.distance_point(point), abs(dist_signed_expected))


@pytest.mark.parametrize(
    "line_a, line_b, dist_expected",
    [
        # The lines intersect.
        (Line([10, 2], [1, 1]), Line([5, -3], [-1, 0]), 0),
        (Line([0, 0], [1, 1]), Line([1, 0], [1, 2]), 0),
        # The lines are parallel.
        (Line([0, 0], [1, 0]), Line([0, 0], [-1, 0]), 0),
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 0]), 0),
        (Line([24, 0], [0, 1]), Line([3, 0], [0, -5]), 21),
        (Line([0, 0], [1, 1]), Line([1, 0], [1, 1]), np.sqrt(2) / 2),
        # The lines are skew.
        (Line([0, 0, 0], [0, 1, 0]), Line([1, 0, 0], [0, -4, 13]), 1),
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

    area = area_triangle(array_a, array_b, array_c)
    assert np.isclose(area, area_expected)


@pytest.mark.parametrize(
    "array_a, array_b, array_c, array_d, volume_expected",
    [
        ([0, 0], [2, 0], [1, 1], [10, -7], 0),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 1], 1 / 3),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, -1], 1 / 3),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 2], 2 / 3),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 3], 1),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [-56, 10, 3], 1),
        ([0, 1, 1], [0, 1, 5], [0, -5, 7], [0, 5, 2], 0),
    ],
)
def test_volume_tetrahedron(array_a, array_b, array_c, array_d, volume_expected):

    volume = volume_tetrahedron(array_a, array_b, array_c, array_d)
    assert np.isclose(volume, volume_expected)
