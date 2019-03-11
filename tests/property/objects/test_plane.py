import pytest
from hypothesis import given

from skspatial.objects import Point, Plane
from tests.property.strategies import st_arrays


@given(st_arrays, st_arrays, st_arrays)
def test_from_points_failure(array_a, array_b, array_c):

    if Point(array_a).is_collinear(array_b, array_c):
        with pytest.raises(Exception):
            Plane.from_points(array_a, array_b, array_c)
