import numpy as np
from hypothesis import given

from skspatial.measurement import area_triangle, volume_tetrahedron
from tests.property.strategies import st_point, st_line


@given(st_point(), st_point(), st_point())
def test_area_triangle(point_a, point_b, point_c):

    area = area_triangle(point_a, point_b, point_c)

    assert np.isclose(area, 0) == point_a.is_collinear(point_b, point_c)


@given(st_line(), st_line())
def test_volume_tetrahedron(line_1, line_2):

    point_a = line_1.point
    point_b = line_1.to_point()

    point_c = line_2.point
    point_d = line_2.to_point()

    volume = volume_tetrahedron(point_a, point_b, point_c, point_d)

    assert np.isclose(volume, 0) == line_1.is_coplanar(line_2)
