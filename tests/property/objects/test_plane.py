from hypothesis import given

from skspatial.constants import ATOL
from skspatial.objects import Point, Points, Plane
from tests.property.strategies import consistent_dim, st_array_fixed


@given(consistent_dim(3 * [st_array_fixed], max_dim=3))
def test_from_points(arrays):

    if not Points(arrays).are_collinear(tol=ATOL):

        # The plane must contain each point.
        plane = Plane.from_points(*arrays)

        for array in arrays:

            point = Point(array).set_dimension(plane.get_dimension())
            assert plane.contains_point(point)
