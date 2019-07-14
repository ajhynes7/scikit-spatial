"""Custom strategies for property tests."""

import hypothesis.strategies as st

from skspatial.objects import Point, Points, Vector, Line, Plane, Circle, Sphere
from .constants import ATOL, DIM_MIN, DIM_MAX


floats = st.floats(min_value=-1e4, max_value=1e4).filter(lambda x: x == 0 or abs(x) > ATOL)

arrays = st.lists(floats, min_size=DIM_MIN, max_size=DIM_MAX)
arrays_nonzero = arrays.filter(lambda array: any(array))

radii = st.floats(min_value=0, max_value=1e4).filter(lambda x: x > ATOL)


@st.composite
def arrays_fixed(draw, dim=2):
    """Return a strategy which generates 1D arrays with a fixed length."""
    return draw(st.lists(floats, min_size=dim, max_size=dim))


@st.composite
def arrays_fixed_nonzero(draw, dim=2):
    """Return a strategy which generates nonzero 1D arrays with a fixed length."""
    return draw(arrays_fixed(dim).filter(lambda x: any(x)))


@st.composite
def points(draw, dim):
    """Return a strategy which generates Point objects."""
    return Point(draw(arrays_fixed(dim)))


@st.composite
def vectors(draw, dim):
    """Return a strategy which generates Vector objects."""
    return Vector(draw(arrays_fixed(dim)))


@st.composite
def vectors_nonzero(draw, dim):
    """Return a strategy which generates nonzero Vector objects."""
    return Vector(draw(arrays_fixed_nonzero(dim)))


@st.composite
def multi_points(draw, dim):
    """Return a strategy which generates Points objects."""
    n_points = draw(st.integers(min_value=1, max_value=50))
    array_like_2d = [draw(arrays_fixed(dim)) for _ in range(n_points)]

    return Points(array_like_2d)


@st.composite
def lines_or_planes(draw, LineOrPlane, dim):
    """Return a strategy which generates Line or Plane objects."""
    array_point = draw(arrays_fixed(dim))
    array_vector = draw(arrays_fixed_nonzero(dim))

    return LineOrPlane(array_point, array_vector)


@st.composite
def lines(draw, dim):
    """
    Return a strategy which generates Line objects.

    Parameters
    ----------
    dim : int
        Dimension of the object.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from .strategies import lines

    >>> find(lines(dim=4), lambda x: x.direction.min() <= -1)
    Line(point=Point([0., 0., 0., 0.]), direction=Vector([ 0.,  0.,  0., -1.]))

    """
    return draw(lines_or_planes(Line, dim))


@st.composite
def planes(draw, dim):
    """
    Return a strategy which generates Plane objects.

    Parameters
    ----------
    dim : int
        Dimension of the object.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from .strategies import planes

    >>> find(planes(dim=3), lambda x: x.normal.norm() >= 5)
    Plane(point=Point([0., 0., 0.]), normal=Vector([0., 0., 5.]))

    """
    return draw(lines_or_planes(Plane, dim))


@st.composite
def circles(draw):
    """
    Return a strategy which generates circles.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from .strategies import circles

    >>> circle = find(circles(), lambda x: x.radius >= 1)
    >>> round(circle.radius)
    1

    """
    return Circle(draw(arrays_fixed(2)), draw(radii))


@st.composite
def spheres(draw):
    """
    Return a strategy which generates Circle objects.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from .strategies import spheres

    >>> sphere = find(spheres(), lambda x: x.radius >= 1)
    >>> round(sphere.radius)
    1

    """
    return Sphere(draw(arrays_fixed(3)), draw(radii))


@st.composite
def consistent_dim(draw, strategies, min_dim=DIM_MIN, max_dim=DIM_MAX):
    """
    Return a strategy which generates multiple spatial objects with the same dimension.

    Parameters
    ----------
    strategies: sequence
        Sequence of functions that return strategies for spatial objects.
        The functions must take a dimension argument.
    min_dim, max_dim: int
        Min and max dimension of the spatial objects.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from .strategies import vectors, lines, planes, consistent_dim

    >>> find(consistent_dim([vectors, planes], min_dim=3), lambda x: True)
    [Vector([0., 0., 0.]), Plane(point=Point([0., 0., 0.]), normal=Vector([0.  , 0.  , 0.01]))]

    >>> find(consistent_dim(3 * [vectors], min_dim=3), lambda x: True)
    [Vector([0., 0., 0.]), Vector([0., 0., 0.]), Vector([0., 0., 0.])]
    
    """
    dim = draw(st.integers(min_value=min_dim, max_value=max_dim))

    return [draw(strategy(dim)) for strategy in strategies]