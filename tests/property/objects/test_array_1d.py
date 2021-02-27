"""Test behaviour of points with vectors."""
from hypothesis import given

from skspatial.objects import Point
from skspatial.objects import Vector
from tests.property.strategies import arrays
from tests.property.strategies import arrays_fixed
from tests.property.strategies import consistent_dim


@given(consistent_dim(2 * [arrays_fixed]))
def test_add(arrays):

    array_a, array_b = arrays

    # Add and subtract the array to obtain the same point.
    assert (Point(array_a) + array_b - array_b).is_close(array_a)


@given(arrays)
def test_is_close(array):

    vector = Vector(array)
    point = Point(array)

    assert point.size == vector.size

    assert point.is_close(vector)
    assert vector.is_close(point)

    assert point.is_close(array)
    assert vector.is_close(array)
