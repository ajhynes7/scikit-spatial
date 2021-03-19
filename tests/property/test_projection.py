import math

import hypothesis.strategies as st
import pytest
from hypothesis import assume
from hypothesis import given

from skspatial.objects import Vector
from tests.property.constants import ATOL
from tests.property.constants import DIM_MAX
from tests.property.constants import DIM_MIN
from tests.property.strategies import arrays_fixed
from tests.property.strategies import circles
from tests.property.strategies import lines
from tests.property.strategies import planes
from tests.property.strategies import spheres


@pytest.mark.parametrize('lines_or_planes', [lines, planes])
@given(data=st.data())
def test_project_point(lines_or_planes, data):
    """Test projecting a point onto a line or plane."""

    dim = data.draw(st.integers(min_value=DIM_MIN, max_value=DIM_MAX))

    array = data.draw(arrays_fixed(dim))
    line_or_plane = data.draw(lines_or_planes(dim))

    point_projected = line_or_plane.project_point(array)

    # The projected point should lie on the line/plane.
    assert line_or_plane.contains_point(point_projected, abs_tol=ATOL)

    # The vector from the point to its projection
    # should be perpendicular to the line/plane.
    vector_projection = Vector.from_points(array, point_projected)

    # The distance from the point to its projection
    # should equal the distance to the line/plane.
    distance_projection = vector_projection.norm()
    distance_to_object = abs(line_or_plane.distance_point(array))
    assert math.isclose(distance_to_object, distance_projection, rel_tol=0.1)

    # The distance of the projection should be the
    # shortest distance from the point to the object.
    distance_points = line_or_plane.point.distance_point(array)
    assert distance_projection < distance_points or math.isclose(distance_projection, distance_points)


@pytest.mark.parametrize('circles_or_spheres', [circles, spheres])
@given(data=st.data())
def test_project_point_circle_sphere(circles_or_spheres, data):

    circle_or_sphere = data.draw(circles_or_spheres())
    array_point = data.draw(arrays_fixed(circle_or_sphere.dimension))

    assume(not circle_or_sphere.point.is_close(array_point))

    point_projected = circle_or_sphere.project_point(array_point)

    assert math.isclose(circle_or_sphere.point.distance_point(point_projected), circle_or_sphere.radius)
