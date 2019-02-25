"""Private parent classes for spatial objects."""

import numpy as np
from dpcontracts import require, ensure, types


class _BaseArray:
    """Private base class for Point and Vector classes."""

    @require(
        "The input length must be one to three.",
        lambda args: len(args.arr) in [1, 2, 3],
    )
    @require(
        "The input array must only contain finite numbers.",
        lambda args: np.all(np.isfinite(args.arr)),
    )
    @ensure(
        "The output array must be 3D.", lambda args, result: args.self.array.size == 3
    )
    def __init__(self, arr):
        """Convert the array to 3D by appending zeros."""
        n_dimensions = len(arr)
        array_padding = np.zeros(3 - n_dimensions)

        self.array = np.concatenate((np.array(arr), array_padding))

    def __eq__(self, other):

        return isinstance(self, type(other)) and np.all(self.array == other.array)

    @require(
        "The input must have the same type as the object.",
        lambda args: isinstance(args.self, type(args.other)),
    )
    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self.array, other.array, **kwargs)


class _Point(_BaseArray):
    """Private parent class for Point."""

    def __init__(self, arr):
        super().__init__(arr)


class _Vector(_BaseArray):
    """Private parent class for Vector."""

    def __init__(self, arr):
        super().__init__(arr)


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @types(point=_Point, vector=_Vector)
    def __init__(self, point, vector):

        self.point = point
        self.vector = vector.unit()

    def __eq__(self, other):

        return vars(self) == vars(other)

    @require(
        "The input must have the same type as the object.",
        lambda args: isinstance(args.other, type(args.self)),
    )
    def is_close(self, other, **kwargs):

        close_point = self.point.is_close(other.point, **kwargs)
        close_vector = self.vector.is_close(other.vector, **kwargs)

        return close_point and close_vector

    @types(point=_Point)
    @ensure("The output must zero or greater.", lambda _, result: result >= 0)
    def distance(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project(point)

        return point.distance(point_projected)
