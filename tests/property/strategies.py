"""Custom strategies for propert tests."""

import hypothesis.strategies as st

from skspatial.objects import Point, Vector, Line, Plane


@st.composite
def st_point(draw):
    """Strategy to generate a Point object."""
    return Point(draw(st_arrays_allowed))


@st.composite
def st_vector(draw):
    """Strategy to generate a Vector object."""
    return Vector(draw(st_arrays_allowed))


@st.composite
def st_vector_nonzero(draw):
    """Strategy to generate a Vector object that is not the zero vector."""
    st_arrays_nonzero = st_arrays_allowed.filter(lambda array: any(array))

    return Vector(draw(st_arrays_nonzero))


@st.composite
def st_line(draw):
    """Strategy to generate a Line object."""
    return Line(draw(st_point()), draw(st_vector_nonzero()))


@st.composite
def st_plane(draw):
    """Strategy to generate a Line object."""
    return Plane(draw(st_point()), draw(st_vector_nonzero()))


# Absolute tolerance for np.isclose and np.allclose functions.
TOLERANCE = 0.01

st_floats = st.floats(min_value=-1e6, max_value=1e6).filter(
    lambda x: x == 0 or abs(x) > TOLERANCE
)

st_arrays = st.lists(st_floats, min_size=1, max_size=10)
st_arrays_allowed = st.lists(st_floats, min_size=1, max_size=3)
