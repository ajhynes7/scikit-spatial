from hypothesis import given
from hypothesis.strategies import integers
from hypothesis.strategies import tuples

from tests.property.constants import ATOL
from tests.property.strategies import planes
from tests.property.strategies import spheres


limits = tuples(integers(-10, 10), integers(-10, 10))


@given(planes(dim=3), limits, limits)
def test_plane_points(plane, lims_x, lims_y):

    points = plane.to_points(lims_x=lims_x, lims_y=lims_y)

    # Test that all the points are on the plane.
    assert all(plane.contains_point(point, abs_tol=ATOL) for point in points)


@given(spheres(), integers(1, 30))
def test_sphere_points(sphere, n_angles):

    points = sphere.to_points(n_angles=n_angles)

    # Test that all the points are on the plane.
    assert all(sphere.contains_point(point, abs_tol=ATOL) for point in points)
