"""Custom strategies for propert tests."""

import hypothesis.strategies as st

from skspatial.constants import ATOL
from skspatial.objects import Line, Plane


st_floats = st.floats(min_value=-1e4, max_value=1e4).filter(
    lambda x: x == 0 or abs(x) > ATOL
)

st_arrays = st.lists(st_floats, min_size=1, max_size=3)
st_arrays_nonzero = st_arrays.filter(lambda array: any(array))


@st.composite
def st_line(draw):
    """Strategy to generate a Line object."""
    return Line(draw(st_arrays), draw(st_arrays_nonzero))


@st.composite
def st_plane(draw):
    """Strategy to generate a Plane object."""
    return Plane(draw(st_arrays), draw(st_arrays_nonzero))
