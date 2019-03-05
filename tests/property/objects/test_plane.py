import pytest
from hypothesis import given

from skspatial.objects import Plane
from tests.property.strategies import st_point


@given(st_point(), st_point(), st_point())
def test_from_points_failure(point_a, point_b, point_c):

    if point_a.is_collinear(point_b, point_c):
        with pytest.raises(Exception):
            Plane.from_points(point_a, point_b, point_c)
