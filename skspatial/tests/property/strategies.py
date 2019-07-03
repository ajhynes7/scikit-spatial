"""Custom strategies for property tests."""

import hypothesis.strategies as st

from skspatial.objects import Point, Points, Vector, Line, Plane, Circle, Sphere
from .constants import ATOL, DIM_MIN, DIM_MAX


@st.composite
def st_array_fixed(draw, dim=2):
    """Generate an array with a fixed length."""
    return draw(st.lists(st_floats, min_size=dim, max_size=dim))


@st.composite
def st_array_fixed_nonzero(draw, dim=2):
    """Generate an array with a fixed length and not all zeros."""
    return draw(st_array_fixed(dim).filter(lambda x: any(x)))


@st.composite
def st_point(draw, dim):
    """Generate a Point object."""
    return Point(draw(st_array_fixed(dim)))


@st.composite
def st_vector(draw, dim):
    """Generate a Vector object."""
    return Vector(draw(st_array_fixed(dim)))


@st.composite
def st_vector_nonzero(draw, dim):
    """Generate a Vector that is not the zero vector."""
    return Vector(draw(st_array_fixed_nonzero(dim)))


@st.composite
def st_points(draw, dim):
    """Generate a Points object."""
    n_points = draw(st.integers(min_value=1, max_value=50))
    array_like_2d = [draw(st_array_fixed(dim)) for _ in range(n_points)]

    return Points(array_like_2d)


@st.composite
def st_line_plane(draw, LineOrPlane, dim):
    """Generate a Line or Plane object."""
    array_point = draw(st_array_fixed(dim))
    array_vector = draw(st_array_fixed_nonzero(dim))

    return LineOrPlane(array_point, array_vector)


@st.composite
def st_line(draw, dim):
    """Generate a Line object."""
    return draw(st_line_plane(Line, dim))


@st.composite
def st_plane(draw, dim):
    """Generate a Plane object."""
    return draw(st_line_plane(Plane, dim))


@st.composite
def st_circle(draw):
    """Generate a Circle object."""
    return Circle(draw(st_array_fixed(2)), draw(st_radii))


@st.composite
def st_sphere(draw):
    """Generate a Sphere object."""
    return Sphere(draw(st_array_fixed(3)), draw(st_radii))


@st.composite
def consistent_dim(draw, strategies, min_dim=DIM_MIN, max_dim=DIM_MAX):
    """Generate multiple spatial objects with the same dimension."""
    dim = draw(st.integers(min_value=min_dim, max_value=max_dim))

    return [draw(strategy(dim)) for strategy in strategies]


st_floats = st.floats(min_value=-1e4, max_value=1e4).filter(
    lambda x: x == 0 or abs(x) > ATOL
)

st_arrays = st.lists(st_floats, min_size=DIM_MIN, max_size=DIM_MAX)
st_arrays_nonzero = st_arrays.filter(lambda array: any(array))

st_radii = st.floats(min_value=0, max_value=1e4).filter(lambda x: x > ATOL)
