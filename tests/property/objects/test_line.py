from hypothesis import given

from skspatial.objects import Point, Line
from tests.property.strategies import st_arrays, st_arrays_nonzero, st_line


@given(st_arrays, st_arrays_nonzero)
def test_line_creation(array_point, array_vector):

    line_1 = Line(array_point, array_vector)

    point_1 = Point(array_point)
    point_2 = point_1.add(array_vector)

    line_2 = Line.from_points(point_1, point_2)

    assert line_1.is_close(line_2)


@given(st_line(), st_line())
def test_two_lines(line_a, line_b):

    are_parallel = line_a.direction.is_parallel(line_b.direction)
    are_coplanar = line_a.is_coplanar(line_b)

    if are_parallel:
        assert are_coplanar

    elif are_coplanar:
        assert line_a.distance_line(line_b) == 0
