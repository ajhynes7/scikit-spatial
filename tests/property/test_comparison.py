from hypothesis import given

from skspatial.constants import ATOL
from skspatial.objects import Point, Line
from tests.property.strategies import st_arrays


@given(st_arrays, st_arrays, st_arrays)
def test_is_collinear(array_a, array_b, array_c):

    point_a = Point(array_a)
    point_b = Point(array_b)

    assert point_a.is_collinear(array_a, array_a)
    assert point_a.is_collinear(array_a, array_b)

    all_different = not (
        point_a.is_close(array_b, atol=ATOL) or point_b.is_close(array_c, atol=ATOL)
    )

    if point_a.is_collinear(array_b, array_c) and all_different:

        line_ab = Line.from_points(array_a, array_b)
        line_bc = Line.from_points(array_b, array_c)

        assert line_ab.contains_point(array_c)
        assert line_bc.contains_point(array_a)

        assert line_ab.is_coplanar(line_bc)
