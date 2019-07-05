import numpy as np
from hypothesis import given

from skspatial.objects import Line
from ..constants import ATOL
from ..strategies import consistent_dim, st_line, st_point, st_vector_nonzero


@given(consistent_dim([st_point, st_vector_nonzero]))
def test_from_points(objs):

    point_a, vector = objs
    point_b = point_a + vector

    line = Line(point_a, vector)
    line_from_points = Line.from_points(point_a, point_b)

    assert line.is_close(line_from_points, atol=ATOL)

    # The line of best fit should be the same
    # as the line from two points.
    line_fit = Line.best_fit([point_a, point_b])
    assert line_fit.is_close(line_from_points)


@given(consistent_dim(2 * [st_line]))
def test_two_lines(lines):

    line_a, line_b = lines

    if line_a.direction.is_parallel(line_b.direction, atol=0, rtol=0):
        assert line_a.is_coplanar(line_b)

    elif line_a.is_coplanar(line_b):
        # The lines are coplanar but not parallel, so they must intersect.
        distance = line_a.distance_line(line_b)
        assert np.isclose(distance, 0)
