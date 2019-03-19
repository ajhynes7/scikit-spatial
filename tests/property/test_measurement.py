import numpy as np
from hypothesis import given, settings

from skspatial.constants import ATOL
from skspatial.measurement import area_triangle, volume_tetrahedron
from skspatial.objects import Points
from tests.property.strategies import st_arrays_multiple


@settings(deadline=None)
@given(st_arrays_multiple(n_arrays=3))
def test_area_triangle(arrays):

    area = area_triangle(*arrays)
    assert np.isclose(area, 0, atol=ATOL) == Points(arrays).are_collinear(tol=ATOL)


@settings(deadline=None)
@given(st_arrays_multiple(n_arrays=4))
def test_volume_tetrahedron(arrays):

    volume = volume_tetrahedron(*arrays)
    assert np.isclose(volume, 0, atol=ATOL) == Points(arrays).are_coplanar(tol=ATOL)
