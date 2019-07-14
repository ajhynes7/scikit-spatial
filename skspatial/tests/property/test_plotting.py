from hypothesis import given
from hypothesis.strategies import integers, tuples

from .strategies import planes, spheres


limits = tuples(integers(-10, 10), integers(-10, 10))


@given(planes(dim=3), limits, limits)
def test_plane_points(plane, lims_x, lims_y):

    points = plane.to_points(lims_x, lims_y)

    # Test that all the points are on the plane.
    assert all(map(plane.contains_point, points))


@given(spheres(), integers(1, 30))
def test_sphere_points(sphere, n_angles):

    points = sphere.to_points(n_angles)

    # Test that all the points are on the plane.
    assert all(map(sphere.contains_point, points))
