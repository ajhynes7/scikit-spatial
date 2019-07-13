from hypothesis import given

from .strategies import st_plane


@given(st_plane(3))
def test_plane_points(plane):

    points = plane.to_points()

    # Test that all the points are on the plane.
    assert all(map(plane.contains_point, points))
