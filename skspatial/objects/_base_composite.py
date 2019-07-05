"""Module for base class of composite spatial objects."""

import numpy as np


class _BaseComposite:
    """Private parent class for composite spatial objects."""

    def distance_point(self, point):
        """
        Return the distance from a point to the object.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        float
            Distance from the point to the object.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line = Line(point=[1, 2, 0], direction=[2, 4, 1])

        >>> line.distance_point([9, -3, -2]).round(3)
        9.554

        >>> from skspatial.objects import Plane

        >>> point = [5, 7, -2]
        >>> plane = Plane(point=[0, 0, 0], normal=[0, 0, 1])

        >>> plane.distance_point(point)
        2.0

        """
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

        if self.dimension == 3:

            if not hasattr(self, 'plot_3d'):
                raise ValueError("The object cannot be plotted in 3D.")

            return lambda ax: self.plot_3d(ax, **kwargs)

        raise ValueError("The dimension must be 2 or 3.")
