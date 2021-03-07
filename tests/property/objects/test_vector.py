import math

import numpy as np
import pytest
from hypothesis import assume
from hypothesis import given

from skspatial.objects import Point
from skspatial.objects import Vector
from tests.property.constants import ATOL
from tests.property.strategies import arrays
from tests.property.strategies import arrays_fixed
from tests.property.strategies import arrays_fixed_nonzero
from tests.property.strategies import arrays_nonzero
from tests.property.strategies import consistent_dim
from tests.property.strategies import floats


@given(consistent_dim(2 * [arrays_fixed]))
def test_from_points(arrays):

    array_a, array_b = arrays

    point_a = Point(array_a)
    vector_ab = Vector.from_points(array_a, array_b)

    assert (point_a + vector_ab).is_close(array_b)


@given(arrays_nonzero)
def test_unit(array):

    vector = Vector(array)
    vector_unit = vector.unit()

    assert math.isclose(vector_unit.norm(), 1)
    assert (vector.norm() * vector_unit).is_close(array)

    assert vector_unit.is_parallel(vector)

    angle = vector.angle_between(vector_unit)
    assert math.isclose(angle, 0, abs_tol=ATOL)


@given(arrays)
def test_add_subtract(array):
    vector = Vector(array)
    assert (vector + array - array).is_close(array)


@given(arrays_nonzero, floats)
def test_scale(array, scalar):

    assume(abs(scalar) > ATOL)

    vector = Vector(array)
    vector_scaled = scalar * vector

    assert vector_scaled.is_parallel(array)

    angle = vector_scaled.angle_between(array)

    if scalar > 0:
        assert math.isclose(angle, 0, abs_tol=ATOL)
    else:
        assert math.isclose(angle, np.pi, rel_tol=1e-6)


@given(consistent_dim(2 * [arrays_fixed_nonzero]))
def test_two_vectors(arrays):

    array_a, array_b = arrays
    vector_a = Vector(array_a)

    is_perpendicular = vector_a.is_perpendicular(array_b)
    is_parallel = vector_a.is_parallel(array_b)

    # Two non-zero vectors cannot be both perpendicular and parallel.
    assert not (is_perpendicular and is_parallel)

    angle = vector_a.angle_between(array_b)

    if is_perpendicular:
        assert math.isclose(angle, np.pi / 2)

    if is_parallel:
        assert math.isclose(angle, 0, abs_tol=ATOL) or math.isclose(angle, np.pi, rel_tol=1e-6)

    # The zero vector is perpendicular and parallel to any other vector.
    vector_zero = np.zeros(vector_a.size)
    assert vector_a.is_perpendicular(vector_zero)
    assert vector_a.is_parallel(vector_zero)

    # The angle with the zero vector is undefined.
    message_expected = "The vectors must have non-zero magnitudes."

    with pytest.raises(ValueError, match=message_expected):
        vector_a.angle_between(vector_zero)

    # The projection of vector B onto A is parallel to A.
    vector_b_projected = vector_a.project_vector(array_b)
    assert vector_a.is_parallel(vector_b_projected)

    # The projection is zero if vectors A and B are perpendicular.
    if is_perpendicular:
        assert vector_b_projected.is_zero(abs_tol=ATOL)
