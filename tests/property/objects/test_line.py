import numpy as np
from hypothesis import given

from skspatial.constants import ATOL
from skspatial.objects import Line
from tests.property.strategies import (
    consistent_dim,
    st_line,
    st_point,
    st_vector_nonzero,
)


@given(consistent_dim([st_point, st_vector_nonzero]))
def test_from_points(objs):

    point, vector = objs

    line_1 = Line(point, vector)
    line_2 = Line.from_points(point, point + vector)

    assert line_1.is_close(line_2, atol=ATOL)


@given(consistent_dim(2 * [st_line]))
def test_two_lines(lines):

    line_a, line_b = lines

    if line_a.direction.is_parallel(line_b.direction):

        assert line_a.is_coplanar(line_b, tol=ATOL)

    elif line_a.is_coplanar(line_b):
        # The lines are coplanar but not parallel, so they must intersect.
        distance = line_a.distance_line(line_b)
        assert np.isclose(distance, 0)
