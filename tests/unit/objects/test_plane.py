import numpy as np
import pytest

from skspatial.objects import Plane


@pytest.mark.parametrize(
    "point_a, point_b, point_c, plane_expected",
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
    "point_a, point_b, point_c",
    [
        # The points cannot be collinear.
        ([0, 0], [0, 0], [0, 0]),
        ([0, 0], [0, 1], [0, 2]),
        ([-2, 1], [0, 2], [2, 3]),
        ([0, 0, 0], [1, 1, 1], [-2, -2, -2]),
        ([0, 1, 2], [1, 2, 3], [4, 5, 6]),
    ],
)
def test_from_points_failure(point_a, point_b, point_c):

    with pytest.raises(Exception):
        Plane.from_points(point_a, point_b, point_c)


@pytest.mark.parametrize(
    "plane, coeffs_expected",
    [
        (Plane([-1, 2], [22, -3]), [22, -3, 0, 28]),
        (Plane([0, 0, 0], [0, 0, 1]), [0, 0, 1, 0]),
        (Plane([0, 0, 0], [0, 0, 25]), [0, 0, 25, 0]),
        (Plane([0, 0, 0], [0, 0, 25]), [0, 0, 25, 0]),
        (Plane([1, 2, 0], [5, 4, 6]), [5, 4, 6, -13]),
        (Plane([-4, 5, 8], [22, -3, 6]), [22, -3, 6, 55]),
    ],
)
def test_cartesian(plane, coeffs_expected):
    """Test the coefficients of the Cartesian plane equation."""

    a, b, c, d = plane.cartesian()

    assert np.allclose([a, b, c, d], coeffs_expected)
