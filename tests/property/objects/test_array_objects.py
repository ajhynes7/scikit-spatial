"""Test behaviour of points with vectors."""

from hypothesis import given

from skspatial.objects import Point, Vector
from tests.property.strategies import st_arrays


@given(st_arrays, st_arrays)
def test_add(array_a, array_b):

    # Add and subtract the array to obtain the same point.
    assert Point(array_a).add(array_b).subtract(array_b).is_close(array_a)


@given(st_arrays)
def test_is_close(array):

    vector = Vector(array)
    point = Point(array)

    assert point.size == vector.size

    assert point.is_close(vector)
    assert vector.is_close(point)

    assert point.is_close(array)
    assert vector.is_close(array)
