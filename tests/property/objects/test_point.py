import numpy as np
from hypothesis import given

from skspatial.objects import Point, Vector
from tests.property.strategies import st_arrays


@given(st_arrays, st_arrays)
def test_add_subtract(array_point, array_vector):

    point = Point(array_point)
    vector = Vector(array_vector)

    point_2 = point.add(array_vector)
    assert np.isclose(point.distance_point(point_2), vector.norm())

    point_3 = point_2.subtract(array_vector)
    assert point.is_close(point_3)
