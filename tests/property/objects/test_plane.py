import pytest
from hypothesis import given

from skspatial.objects import Points, Plane
from tests.property.strategies import st_arrays


@given(st_arrays, st_arrays, st_arrays)
def test_from_points_failure(array_a, array_b, array_c):

    if Points([array_a, array_b, array_c]).are_collinear():
        with pytest.raises(Exception):
            Plane.from_points(array_a, array_b, array_c)
