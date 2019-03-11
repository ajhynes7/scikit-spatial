import numpy as np
import pytest
from hypothesis import assume, given

from skspatial.constants import ATOL
from skspatial.objects import Point, Vector
from tests.property.strategies import st_floats, st_arrays, st_arrays_nonzero


@given(st_arrays, st_arrays)
def test_from_points(array_a, array_b):

    vector_ab = Vector.from_points(array_a, array_b)

    assert Point(array_a).add(vector_ab).is_close(array_b)


@given(st_arrays_nonzero)
def test_unit(array):

    vector = Vector(array)
    vector_unit = vector.unit()

    assert np.isclose(vector_unit.magnitude, 1)
    assert (vector.magnitude * vector_unit).is_close(array)

    assert vector_unit.is_parallel(vector)

    angle = vector.angle_between(vector_unit)
    assert np.isclose(angle, 0, atol=ATOL)


@given(st_arrays)
def test_add_subtract(array):
    vector = Vector(array)
    assert vector.add(array).subtract(array).is_close(array)


@given(st_arrays_nonzero, st_floats)
def test_scale(array, scalar):

    assume(abs(scalar) > ATOL)

    vector = Vector(array)
    vector_scaled = scalar * vector

    assert vector_scaled.is_parallel(array, atol=ATOL)

    angle = np.degrees(vector_scaled.angle_between(array))

    if scalar > 0:
        assert np.isclose(angle, 0, atol=ATOL)
    else:
        assert np.isclose(angle, 180, atol=ATOL)


@given(st_arrays_nonzero, st_arrays_nonzero)
def test_two_vectors(array_a, array_b):

    vector_a = Vector(array_a)

    is_perpendicular = vector_a.is_perpendicular(array_b, atol=ATOL)
    is_parallel = vector_a.is_parallel(array_b, atol=ATOL)

    # Two non-zero vectors cannot be both perpendicular and parallel.
    assert not (is_perpendicular and is_parallel)

    angle = np.degrees(vector_a.angle_between(array_b))

    assert is_parallel == (np.isclose(angle, 0) or np.isclose(angle, 180))
    assert is_perpendicular == np.isclose(angle, 90)

    # The zero vector is perpendicular and parallel to any other vector.
    vector_zero = Vector([0])
    assert vector_a.is_perpendicular(vector_zero)
    assert vector_a.is_parallel(vector_zero)

    # The angle with the zero vector is undefined.
    with pytest.raises(Exception):
        vector_a.angle_between(vector_zero)

    # The projection of vector B onto A is parallel to A.
    vector_b_projected = vector_a.project(array_b)
    assert vector_a.is_parallel(vector_b_projected, atol=ATOL)

    # The projection is zero iff vectors A and B are perpendicular.
    assert vector_b_projected.is_zero() == is_perpendicular

    assert (vector_a.dot(array_b) > 0) == (angle < 90)
