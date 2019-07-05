"""Module for the Sphere class."""

import numpy as np

from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects.vector import Vector


class Sphere(_BaseSphere):
    """
    A sphere in 3D space.

    The sphere is defined by a 3D point and a radius.

    Parameters
    ----------
    point : (3,) array_like
        Center of the sphere.
    radius : {int, float}
        Radius of the sphere.

    Attributes
    ----------
    point : (3,) Point
        Center of the circle.
    radius : {int, float}
        Radius of the sphere.
    dimension : int
        Dimension of the sphere.

    Raises
    ------
    ValueError
        If the radius is not positive, or if the point is not 3D.

    Examples
    --------
    >>> from skspatial.objects import Sphere

    >>> sphere = Sphere([1, 2, 3], 5)

    >>> sphere
    Sphere(point=Point([1, 2, 3]), radius=5)

    >>> sphere.dimension
    3

    >>> sphere.surface_area().round(2)
    314.16

    >>> Sphere([0, 0], 0)
    Traceback (most recent call last):
    ...
    ValueError: The radius must be positive.

    >>> Sphere([0, 0, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The point must be 3D.

    """

    def __init__(self, point, radius):

        super().__init__(point, radius)

        if self.point.dimension != 3:
            raise ValueError("The point must be 3D.")

    def surface_area(self):
        r"""
        Return the surface area of the sphere.

        The surface area :math:`A` of a sphere with radius :math:`r` is

        .. math:: A = 4 \pi r ^ 2

        Returns
        -------
        np.float64
            Surface area of the sphere.

        Examples
        --------
        >>> from skspatial.objects import Sphere

        >>> Sphere([0, 0, 0], 1).surface_area().round(2)
        12.57

        >>> Sphere([0, 0, 0], 2).surface_area().round(2)
        50.27

        """
        return np.float64(4 * np.pi * self.radius ** 2)

    def volume(self):
        r"""
        Return the volume of the sphere.

        The volume :math:`V` of a sphere with radius :math:`r` is

        .. math:: V = \frac{4}{3} \pi r ^ 3

        Returns
        -------
        np.float64
            Volume of the sphere.

        Examples
        --------
        >>> from skspatial.objects import Sphere

        >>> Sphere([0, 0, 0], 1).volume().round(2)
        4.19

        >>> Sphere([0, 0, 0], 2).volume().round(2)
        33.51

        """
        return np.float64(4 / 3 * np.pi * self.radius ** 3)

    def intersect_line(self, line):
        """
        Intersect the sphere with a line.

        A line intersects a sphere at two points.

        Parameters
        ----------
        line : Line
            Input line.

        Returns
        -------
        point_a, point_b : Point
            The two points of intersection.

        Examples
        --------
        >>> from skspatial.objects import Sphere, Line

        >>> sphere = Sphere([0, 0, 0], 1)

        >>> sphere.intersect_line(Line([0, 0, 0], [1, 0, 0]))
        (Point([-1.,  0.,  0.]), Point([1., 0., 0.]))

        >>> sphere.intersect_line(Line([0, 0, 1], [1, 0, 0]))
        (Point([0., 0., 1.]), Point([0., 0., 1.]))

        >>> sphere.intersect_line(Line([0, 0, 2], [1, 0, 0]))
        Traceback (most recent call last):
        ...
        ValueError: The line does not intersect the sphere.

        """
        vector_to_line = Vector.from_points(self.point, line.point)
        vector_unit = line.direction.unit()

        dot = vector_unit.dot(vector_to_line)

        discriminant = dot ** 2 - (vector_to_line.norm() ** 2 - self.radius ** 2)

        if discriminant < 0:
            raise ValueError("The line does not intersect the sphere.")

        pm = np.array([-1, 1])  # Array to compute plus/minus.
        distances = -dot + pm * np.sqrt(discriminant)

        point_a, point_b = line.point + distances.reshape(-1, 1) * vector_unit

        return point_a, point_b

    def plot_3d(self, ax_3d, **kwargs):
        """
        Plot the sphere in 3D.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Sphere

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> sphere = Sphere([1, 2, 3], 2)

            >>> sphere.plot_3d(ax, alpha=0.2)
            >>> sphere.point.plot_3d(ax, s=100)

        """
        angles_a = np.linspace(0, np.pi, 30)
        angles_b = np.linspace(0, 2 * np.pi, 30)

        X = self.point[0] + self.radius * np.outer(np.sin(angles_a), np.sin(angles_b))
        Y = self.point[1] + self.radius * np.outer(np.sin(angles_a), np.cos(angles_b))
        Z = self.point[2] + self.radius * np.outer(
            np.cos(angles_a), np.ones_like(angles_b)
        )

        ax_3d.plot_surface(X, Y, Z, **kwargs)
