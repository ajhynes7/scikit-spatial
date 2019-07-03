import numpy as np
import pytest
from hypothesis import assume, given

from skspatial.objects import Point, Vector
from ..constants import ATOL
from ..strategies import (
    consistent_dim,
    st_array_fixed,
    st_array_fixed_nonzero,
    st_arrays,
    st_arrays_nonzero,
    st_floats,
)


@given(consistent_dim(2 * [st_array_fixed]))
def test_from_points(arrays):

    array_a, array_b = arrays

    point_a = Point(array_a)
    vector_ab = Vector.from_points(array_a, array_b)

    assert (point_a + vector_ab).is_close(array_b)


@given(st_arrays_nonzero)
def test_unit(array):

    vector = Vector(array)
    vector_unit = vector.unit()

    assert np.isclose(vector_unit.norm(), 1)
    assert (vector.norm() * vector_unit).is_close(array)

    assert vector_unit.is_parallel(vector, atol=ATOL)

    angle = vector.angle_between(vector_unit)
    assert np.isclose(angle, 0, atol=ATOL)


@given(st_arrays)
def test_add_subtract(array):
    vector = Vector(array)
    assert (vector + array - array).is_close(array)


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


@given(consistent_dim(2 * [st_array_fixed_nonzero]))
def test_two_vectors(arrays):

    array_a, array_b = arrays
    vector_a = Vector(array_a)

    is_perpendicular = vector_a.is_perpendicular(array_b)
    is_parallel = vector_a.is_parallel(array_b)

    # Two non-zero vectors cannot be both perpendicular and parallel.
    assert not (is_perpendicular and is_parallel)

    angle = vector_a.angle_between(array_b)

    if is_perpendicular:
        assert np.isclose(angle, np.pi / 2, atol=ATOL)

    if is_parallel:
        assert np.isclose(angle, 0, atol=ATOL) or np.isclose(angle, np.pi, atol=ATOL)

    # The zero vector is perpendicular and parallel to any other vector.
    vector_zero = np.zeros(vector_a.size)
    assert vector_a.is_perpendicular(vector_zero)
    assert vector_a.is_parallel(vector_zero)

    # The angle with the zero vector is undefined.
    with pytest.raises(Exception):
        vector_a.angle_between(vector_zero)

    # The projection of vector B onto A is parallel to A.
    vector_b_projected = vector_a.project_vector(array_b)
    assert vector_a.is_parallel(vector_b_projected, atol=ATOL)

    # The projection is zero if vectors A and B are perpendicular.
    if is_perpendicular:
        assert vector_b_projected.is_zero(atol=ATOL)
