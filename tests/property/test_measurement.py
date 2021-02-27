import math

from hypothesis import given

from skspatial.measurement import area_triangle
from skspatial.measurement import volume_tetrahedron
from skspatial.objects import Points
from tests.property.constants import ATOL
from tests.property.strategies import arrays_fixed
from tests.property.strategies import consistent_dim


@given(consistent_dim(3 * [arrays_fixed], max_dim=3))
def test_area_triangle(arrays):

    area = area_triangle(*arrays)

    if math.isclose(area, 0):
        assert Points(arrays).are_collinear(tol=ATOL)


@given(consistent_dim(4 * [arrays_fixed], max_dim=3))
def test_volume_tetrahedron(arrays):

    volume = volume_tetrahedron(*arrays)

    if math.isclose(volume, 0):
        assert Points(arrays).are_coplanar(tol=ATOL)
