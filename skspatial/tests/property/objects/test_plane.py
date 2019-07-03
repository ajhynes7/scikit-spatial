from hypothesis import assume, given

from skspatial.objects import Points, Plane
from ..constants import ATOL
from ..strategies import consistent_dim, st_array_fixed


@given(consistent_dim(3 * [st_array_fixed], max_dim=3))
def test_from_points(arrays):

    points = Points(arrays)
    assume(not points.are_collinear(tol=ATOL))

    # The plane must contain each point.
    plane = Plane.from_points(*points)

    points = points.set_dimension(plane.dimension)

    for point in points:
        assert plane.contains_point(point)

    # The plane of best fit should be the same
    # as the plane from three points.
    plane_fit = Plane.best_fit(points)
    assert plane_fit.is_close(plane)
