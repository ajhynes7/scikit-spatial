from hypothesis import given

from skspatial.constants import ATOL
from skspatial.objects import Points, Plane
from tests.property.strategies import consistent_dim, st_array_fixed


@given(consistent_dim(3 * [st_array_fixed], max_dim=3))
def test_from_points(arrays):

    points = Points(arrays)

    if not points.are_collinear(tol=ATOL):

        # The plane must contain each point.
        plane = Plane.from_points(*points)

        points = points.set_dimension(plane.get_dimension())

        for point in points:
            assert plane.contains_point(point)
