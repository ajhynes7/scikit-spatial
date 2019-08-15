"""Module for private parent class of Line and Plane."""

import inspect
from typing import Callable, Union

import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial._functions import _contains_point, _sum_squares
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector
from skspatial.plotting import _plotter
from skspatial.typing import array_like


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    def __init__(self, point: array_like, vector: array_like):

        self.point = Point(point)
        self.vector = Vector(vector)

        if self.point.dimension != self.vector.dimension:
            raise ValueError("The point and vector must have the same dimension.")

        if self.vector.is_zero(rel_tol=0, abs_tol=0):
            raise ValueError("The vector must not be the zero vector.")

        self.dimension = self.point.dimension

    def __repr__(self) -> str:

        name_class = type(self).__name__
        name_vector = inspect.getfullargspec(type(self)).args[-1]

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return f"{name_class}(point={repr_point}, {name_vector}={repr_vector})"

    def contains_point(self, point: array_like, **kwargs: float) -> bool:
        """Check if the line/plane contains a point."""
        return _contains_point(self, point, **kwargs)

    def is_close(self, other: array_like, **kwargs: float) -> bool:
        """
        Check if the line/plane is almost equivalent to another line/plane.

        The points must be close and the vectors must be parallel.

        Parameters
        ----------
        other : object
             Line or Plane.
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

        Returns
        -------
        bool
            True if the objects are almost equivalent; false otherwise.

        Raises
        ------
        TypeError
            If the input doesn't have the same type as the object.

        Examples
        --------
        >>> from skspatial.objects import Line, Plane

        >>> line_a = Line(point=[0, 0], direction=[1, 0])
        >>> line_b = Line(point=[0, 0], direction=[-2, 0])
        >>> line_a.is_close(line_b)
        True

        >>> line_b = Line(point=[50, 0], direction=[-4, 0])
        >>> line_a.is_close(line_b)
        True

        >>> line_b = Line(point=[50, 29], direction=[-4, 0])
        >>> line_a.is_close(line_b)
        False

        >>> plane_a = Plane(point=[0, 0, 0], normal=[0, 0, 5])
        >>> plane_b = Plane(point=[23, 45, 0], normal=[0, 0, -20])
        >>> plane_a.is_close(plane_b)
        True

        >>> line_a.is_close(plane_a)
        Traceback (most recent call last):
        ...
        TypeError: The input must have the same type as the object.

        """
        if not isinstance(other, type(self)):
            raise TypeError("The input must have the same type as the object.")

        contains_point = self.contains_point(other.point, **kwargs)
        is_parallel = self.vector.is_parallel(other.vector, **kwargs)

        return contains_point and is_parallel

    def sum_squares(self, points: array_like) -> np.float64:

        return _sum_squares(self, points)

    def plotter(self, **kwargs) -> Union[Callable[[Axes], None], Callable[[Axes3D], None]]:

        return _plotter(self, **kwargs)
