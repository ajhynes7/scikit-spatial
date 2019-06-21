"""Module for base class of composite spatial objects."""

from copy import deepcopy

import numpy as np

from skspatial.objects._base_array import _BaseArray1D


class _BaseComposite:
    """Private parent class for composite spatial objects."""

    def __getitem__(self, name_item):

        return getattr(self, name_item)

    def __setitem__(self, name_item, value):

        return setattr(self, name_item, value)

    def set_dimension(self, dim):

        obj_new = deepcopy(self)

        for name_item in vars(self):

            attribute = self[name_item]

            if isinstance(attribute, _BaseArray1D):
                obj_new[name_item] = attribute.set_dimension(dim)

        return obj_new

    def distance_point(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project_point(point)

        return point_projected.distance_point(point)

    def contains_point(self, point, **kwargs):
        """Check if this spatial object contains a point."""
        distance = self.distance_point(point)

        return np.isclose(distance, 0, **kwargs)

    def sum_squares(self, points):

        distances_squared = np.apply_along_axis(self.distance_point, 1, points) ** 2

        return distances_squared.sum()

    def plotter(self, **kwargs):
        """Return a function that plots the object when passed a matplotlib axes."""

        if self.dimension == 2:

            if not hasattr(self, 'plot_2d'):
                raise ValueError("The object cannot be plotted in 2D.")

            return lambda ax: self.plot_2d(ax, **kwargs)

        elif self.dimension == 3:

            if not hasattr(self, 'plot_3d'):
                raise ValueError("The object cannot be plotted in 3D.")

            return lambda ax: self.plot_3d(ax, **kwargs)

        else:
            raise ValueError("The dimension must be 2 or 3.")
