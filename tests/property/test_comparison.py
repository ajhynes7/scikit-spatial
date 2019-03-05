from hypothesis import given

from skspatial.objects import Line
from tests.property.strategies import st_point


@given(st_point(), st_point(), st_point())
def test_is_collinear(point_a, point_b, point_c):

    assert point_a.is_collinear(point_a, point_a)
    assert point_a.is_collinear(point_a, point_b)

    all_different = not (point_a.is_close(point_b) or point_b.is_close(point_c))

    if point_a.is_collinear(point_b, point_c) and all_different:

        line_ab = Line.from_points(point_a, point_b)
        line_bc = Line.from_points(point_b, point_c)

        assert line_ab.contains_point(point_c)
        assert line_bc.contains_point(point_a)

        assert line_ab.is_coplanar(line_bc)
