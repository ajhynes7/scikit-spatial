"""Custom strategies for property tests."""

import hypothesis.strategies as st

from skspatial.constants import ATOL
from skspatial.objects import Point, Vector, Line, Plane


DIM_MIN, DIM_MAX = 2, 10


@st.composite
def st_array_fixed(draw, dim=2):
    """Generate an array with a fixed length."""
    return draw(st.lists(st_floats, min_size=dim, max_size=dim))


@st.composite
def st_array_fixed_nonzero(draw, dim=2):
    """Generate an array with a fixed length and not all zeros."""
    return draw(st_array_fixed(dim).filter(lambda x: any(x)))


@st.composite
def st_line_plane(draw, LineOrPlane, dim):

    array_point = draw(st_array_fixed(dim))
    array_vector = draw(st_array_fixed_nonzero(dim))

    return LineOrPlane(array_point, array_vector)


@st.composite
def st_point(draw, dim):

    return Point(draw(st_array_fixed(dim)))


@st.composite
def st_vector(draw, dim):

    return Vector(draw(st_array_fixed(dim)))


@st.composite
def st_vector_nonzero(draw, dim):

    return Vector(draw(st_array_fixed_nonzero(dim)))


@st.composite
def st_line(draw, dim):

    return draw(st_line_plane(Line, dim))


@st.composite
def st_plane(draw, dim):

    return draw(st_line_plane(Plane, dim))


@st.composite
def consistent_dim(draw, strategies, min_dim=DIM_MIN, max_dim=DIM_MAX):

    dim = draw(st.integers(min_value=min_dim, max_value=max_dim))

    return [draw(strategy(dim)) for strategy in strategies]


st_floats = st.floats(min_value=-1e4, max_value=1e4).filter(
    lambda x: x == 0 or abs(x) > ATOL
)

st_arrays = st.lists(st_floats, min_size=DIM_MIN, max_size=DIM_MAX)
st_arrays_nonzero = st_arrays.filter(lambda array: any(array))
