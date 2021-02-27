import math

from hypothesis import given

from skspatial.objects import Point
from skspatial.objects import Vector
from tests.property.strategies import arrays_fixed
from tests.property.strategies import consistent_dim


@given(consistent_dim(2 * [arrays_fixed]))
def test_add_subtract(arrays):

    array_point, array_vector = arrays

    point = Point(array_point)
    vector = Vector(array_vector)

    point_2 = point + array_vector
    assert math.isclose(point.distance_point(point_2), vector.norm())

    point_3 = point_2 - array_vector
    assert point.is_close(point_3)
