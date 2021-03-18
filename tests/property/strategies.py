"""Custom strategies for property tests."""
import hypothesis.strategies as st
from hypothesis import assume

from skspatial.objects import Circle
from skspatial.objects import Line
from skspatial.objects import Plane
from skspatial.objects import Point
from skspatial.objects import Points
from skspatial.objects import Sphere
from skspatial.objects import Triangle
from skspatial.objects import Vector
from tests.property.constants import DIM_MAX
from tests.property.constants import DIM_MIN
from tests.property.constants import FLOAT_MIN


floats = st.floats(min_value=-1e4, max_value=1e4).filter(lambda x: x == 0 or abs(x) > FLOAT_MIN)

arrays = st.lists(floats, min_size=DIM_MIN, max_size=DIM_MAX)
arrays_nonzero = arrays.filter(lambda array: any(array))

radii = floats.filter(lambda x: x > 0)


@st.composite
def arrays_fixed(draw, dim=2):
    """
    Return a strategy which generates 1D arrays with a fixed length.

    Parameters
    ----------
    dim : int, optional
        Dimension (length) of the array (default is 2).

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from tests.property.strategies import arrays_fixed

    >>> find(arrays_fixed(2), lambda x: True)
    [0.0, 0.0]

    >>> find(arrays_fixed(5), lambda x: True)
    [0.0, 0.0, 0.0, 0.0, 0.0]

    """
    return draw(st.lists(floats, min_size=dim, max_size=dim))


@st.composite
def arrays_fixed_nonzero(draw, dim=2):
    """
    Return a strategy which generates nonzero 1D arrays with a fixed length.

    Parameters
    ----------
    dim : int, optional
        Dimension (length) of the array (default is 2).

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    """
    return draw(arrays_fixed(dim).filter(lambda x: any(x)))


@st.composite
def points(draw, dim):
    """
    Return a strategy which generates Point objects.

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
    >>> from tests.property.strategies import points

    >>> find(points(3), lambda x: True)
    Point([0., 0., 0.])

    """
    return Point(draw(arrays_fixed(dim)))


@st.composite
def vectors(draw, dim):
    """
    Return a strategy which generates Vector objects.

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
    >>> from tests.property.strategies import vectors

    >>> find(vectors(2), lambda x: True)
    Vector([0., 0.])

    """
    return Vector(draw(arrays_fixed(dim)))


@st.composite
def vectors_nonzero(draw, dim):
    """
    Return a strategy which generates nonzero Vector objects.

    Parameters
    ----------
    dim : int
        Dimension of the object.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    """
    return Vector(draw(arrays_fixed_nonzero(dim)))


@st.composite
def multi_points(draw, dim):
    """
    Return a strategy which generates Points objects.

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
    >>> from tests.property.strategies import multi_points

    >>> find(multi_points(2), lambda x: len(x) == 3)
    Points([[0., 0.],
            [0., 0.],
            [0., 0.]])

    """
    n_points = draw(st.integers(min_value=1, max_value=50))
    array_like_2d = [draw(arrays_fixed(dim)) for _ in range(n_points)]

    return Points(array_like_2d)


@st.composite
def lines_or_planes(draw, LineOrPlane, dim):
    """
    Return a strategy which generates Line or Plane objects.

    Parameters
    ----------
    LineOrPlane : class
        Line or Plane class.
    dim : int
        Dimension of the object.

    Returns
    -------
    LazyStrategy
        Hypothesis strategy.

    Examples
    --------
    >>> from hypothesis import find
    >>> from tests.property.strategies import lines_or_planes

    >>> find(lines_or_planes(Line, 2), lambda x: True)
    Line(point=Point([0., 0.]), direction=Vector([0.   , 0.001]))

    >>> find(lines_or_planes(Plane, 3), lambda x: True)
    Plane(point=Point([0., 0., 0.]), normal=Vector([0.   , 0.   , 0.001]))

    """
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
    >>> from tests.property.strategies import lines

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
    >>> from tests.property.strategies import planes

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
    >>> from tests.property.strategies import circles

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
    >>> from tests.property.strategies import spheres

    >>> sphere = find(spheres(), lambda x: x.radius >= 1)
    >>> round(sphere.radius)
    1

    """
    return Sphere(draw(arrays_fixed(3)), draw(radii))


@st.composite
def triangles(draw, dim):
    """
    Return a strategy which generates Triangle objects.

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
    >>> from tests.property.strategies import triangles

    >>> find(triangles(dim=2), lambda x: True)
    Triangle(point_a=Point([0., 0.]), point_b=Point([0.   , 0.001]), point_c=Point([0.001, 0.   ]))

    """
    point_a = draw(arrays_fixed(dim))
    point_b = draw(arrays_fixed(dim))
    point_c = draw(arrays_fixed(dim))

    assume(not Points([point_a, point_b, point_c]).are_collinear(tol=1))

    return Triangle(point_a, point_b, point_c)


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
    >>> from tests.property.strategies import vectors, lines, planes, consistent_dim

    >>> find(consistent_dim([vectors, planes], min_dim=3), lambda x: True)
    [Vector([0., 0., 0.]), Plane(point=Point([0., 0., 0.]), normal=Vector([0.   , 0.   , 0.001]))]

    >>> find(consistent_dim(3 * [vectors], min_dim=3), lambda x: True)
    [Vector([0., 0., 0.]), Vector([0., 0., 0.]), Vector([0., 0., 0.])]

    """
    dim = draw(st.integers(min_value=min_dim, max_value=max_dim))

    return [draw(strategy(dim)) for strategy in strategies]
