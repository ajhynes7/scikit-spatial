import pytest
from hypothesis import given

from skspatial.objects import Line
from tests.property.strategies import st_point, st_vector_nonzero, st_line


@given(st_point(), st_vector_nonzero())
def test_line_creation(point, vector):

    line_1 = Line(point, vector)

    point_2 = point.add(vector)
    line_2 = Line.from_points(point, point_2)

    assert line_1.is_close(line_2)

    # A point and vector are not interchangeable.
    with pytest.raises(Exception):
        Line(vector, point)


@given(st_line(), st_line())
def test_two_lines(line_a, line_b):

    are_parallel = line_a.direction.is_parallel(line_b.direction)
    are_coplanar = line_a.is_coplanar(line_b)

    if are_parallel:
        assert are_coplanar

    elif are_coplanar:
        assert line_a.distance_line(line_b) == 0
