import numpy as np
import pytest

from skspatial.objects import Point, Vector, Plane


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

    point_projected = plane.project_point(point)
    distance_signed = plane.distance_point(point)

    assert point_projected.is_close(point_expected)
    assert np.isclose(distance_signed, dist_expected)
