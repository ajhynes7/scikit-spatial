import numpy as np
from hypothesis import given

from skspatial.objects import Point, Vector
from skspatial.tests.property.strategies import consistent_dim, st_array_fixed


@given(consistent_dim(2 * [st_array_fixed]))
def test_add_subtract(arrays):

    array_point, array_vector = arrays

    point = Point(array_point)
    vector = Vector(array_vector)

    point_2 = point + array_vector
    assert np.isclose(point.distance_point(point_2), vector.norm())

    point_3 = point_2 - array_vector
    assert point.is_close(point_3)
