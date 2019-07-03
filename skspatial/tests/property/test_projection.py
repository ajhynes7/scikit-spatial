import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import assume, given

from skspatial.objects import Vector
from .constants import ATOL
from .strategies import (
    DIM_MAX,
    DIM_MIN,
    st_array_fixed,
    st_circle,
    st_line,
    st_plane,
    st_sphere,
)


@pytest.mark.parametrize('st_line_or_plane', [st_line, st_plane])
@given(data=st.data())
def test_project_point(st_line_or_plane, data):
    """Test projecting a point onto a line or plane."""

    dim = data.draw(st.integers(min_value=DIM_MIN, max_value=DIM_MAX))

    array = data.draw(st_array_fixed(dim))
    line_or_plane = data.draw(st_line_or_plane(dim))

    point_projected = line_or_plane.project_point(array)

    # The projected point should lie on the line/plane.
    assert line_or_plane.contains_point(point_projected, atol=ATOL)

    # The vector from the point to its projection
    # should be perpendicular to the line/plane.
    vector_projection = Vector.from_points(array, point_projected)

    # The distance from the point to its projection
    # should equal the distance to the line/plane.
    distance_projection = vector_projection.norm()
    distance_to_object = abs(line_or_plane.distance_point(array))
    assert np.isclose(distance_to_object, distance_projection)

    # The distance of the projection should be the
    # shortest distance from the point to the object.
    distance_points = line_or_plane.point.distance_point(array)
    assert distance_projection < distance_points or np.isclose(
        distance_projection, distance_points
    )


@pytest.mark.parametrize('st_circle_or_sphere', [st_circle, st_sphere])
@given(data=st.data())
def test_project_point_circle_sphere(st_circle_or_sphere, data):

    circle_or_sphere = data.draw(st_circle_or_sphere())
    array_point = data.draw(st_array_fixed(circle_or_sphere.dimension))

    assume(not circle_or_sphere.point.is_close(array_point))

    point_projected = circle_or_sphere.project_point(array_point)

    assert np.isclose(
        circle_or_sphere.point.distance_point(point_projected), circle_or_sphere.radius
    )
