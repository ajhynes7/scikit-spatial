"""Module for the Line class."""

import numpy as np

from skspatial.objects._base_line_plane import _BaseLinePlane
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.plotting import _connect_points_2d, _connect_points_3d
from skspatial.transformation import transform_coordinates


class Line(_BaseLinePlane):
    """
    A line in space.

    The line is defined by a point and a direction vector.

    Parameters
    ----------
    point : array_like
        Point on the line.
    direction : array_like
        Direction vector of the line.

    Attributes
    ----------
    point : Point
        Point on the line.
    direction : Vector
        Unit direction vector.
    vector : Vector
        Same as the direction.
    dimension : int
        Dimension of the line.

    Raises
    ------
    ValueError
        If the point and vector have different dimensions,
        or if the vector is all zeros.

    Examples
    --------
    >>> from skspatial.objects import Line

    >>> line = Line(point=[0, 0], direction=[3, 0])

    >>> line
    Line(point=Point([0, 0]), direction=Vector([3, 0]))

    >>> line.direction
    Vector([3, 0])

    The direction can also be accessed with the ``vector`` attribute.

    >>> line.vector
    Vector([3, 0])

    The line dimension is the dimension of the point and vector.

    >>> line.dimension
    2

    >>> Line([0, 0], [1, 0, 0])
    Traceback (most recent call last):
    ...
    ValueError: The point and vector must have the same dimension.

    >>> Line([1, 1], [0, 0])
    Traceback (most recent call last):
    ...
    ValueError: The vector must not be the zero vector.

    """

    def __init__(self, point, direction):

        super().__init__(point, direction)

        self.direction = self.vector

    @classmethod
    def from_points(cls, point_a, point_b):
        """
        Instantiate a line from two points.

        Parameters
        ----------
        point_a, point_b : array_like
            Two points defining the line.

        Returns
        -------
        Line
            Line containing the two input points.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> Line.from_points([0, 0], [1, 0])
        Line(point=Point([0, 0]), direction=Vector([1, 0]))

        The order of the points affects the line point and direction vector.

        >>> Line.from_points([1, 0], [0, 0])
        Line(point=Point([1, 0]), direction=Vector([-1,  0]))

        """
        vector_ab = Vector.from_points(point_a, point_b)

        return cls(point_a, vector_ab)

    @classmethod
    def from_slope(cls, slope, y_intercept):
        r"""
        Instantiate a 2D line from a slope and Y-intercept.

        A 2D line can be represented by the equation

        .. math:: y = mx + b

        where :math:`m` is the slope and :math:`p` is the Y-intercept.

        Parameters
        ----------
        slope : scalar
            Slope of the 2D line.
        y_intercept : scalar
            Y coordinate of the point where the line intersects the Y axis.

        Returns
        -------
        Line
            A 2D Line object.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> Line.from_slope(2, 0)
        Line(point=Point([0, 0]), direction=Vector([1, 2]))

        >>> Line.from_slope(-3, 5)
        Line(point=Point([0, 5]), direction=Vector([ 1, -3]))

        >>> line_a = Line.from_slope(1, 0)
        >>> line_b = Line.from_slope(0, 5)

        >>> line_a.intersect_line(line_b)
        Point([5., 5.])

        """
        point = [0, y_intercept]
        direction = [1, slope]

        return cls(point, direction)

    def is_coplanar(self, other, **kwargs):
        """
        Check if the line is coplanar with another.

        Parameters
        ----------
        other : Line
            Input line.
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        Returns
        -------
        bool
            True if the line is coplanar; false otherwise.

        Raises
        ------
        TypeError
            If input is not a line.

        References
        ----------
        http://mathworld.wolfram.com/Coplanar.html

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line_a = Line(point=[0, 0, 0], direction=[1, 0, 0])
        >>> line_b = Line([-5, 3, 0], [7, 1, 0])
        >>> line_c = Line([0, 0, 0], [0, 0, 1])

        >>> line_a.is_coplanar(line_b)
        True

        >>> line_a.is_coplanar(line_c)
        True

        >>> line_b.is_coplanar(line_c)
        False

        The input must be another line.

        >>> from skspatial.objects import Plane

        >>> line_a.is_coplanar(Plane(line_a.point, line_a.vector))
        Traceback (most recent call last):
        ...
        TypeError: The input must also be a line.

        """
        if not isinstance(other, type(self)):
            raise TypeError("The input must also be a line.")

        point_1 = self.point
        point_2 = self.to_point()
        point_3 = other.point
        point_4 = other.to_point()

        points = Points([point_1, point_2, point_3, point_4])

        return points.are_coplanar(**kwargs)

    def to_point(self, t=1):
        r"""
        Return a point along the line using a parameter `t`.

        Parameters
        ----------
        t : scalar
            Parameter that defines the new point along the line.

        Returns
        -------
        Point
            New point along the line.

        Notes
        -----
        The new point :math:`p` is computed as:

        .. math:: p = \mathtt{line.point} + t \cdot \mathtt{line.direction}

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line = Line(point=[0, 0], direction=[2, 0])

        >>> line.to_point()
        Point([2, 0])

        >>> line.to_point(t=2)
        Point([4, 0])

        """
        vector_along_line = t * self.direction

        return self.point + vector_along_line

    def project_point(self, point):
        """
        Project a point onto this line.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        Point
            Projection of the point onto the line.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line = Line(point=[0, 0], direction=[8, 0])
        >>> line.project_point([5, 5])
        Point([5., 0.])

        """
        # Vector from the point on the line to the point in space.
        vector_to_point = Vector.from_points(self.point, point)

        # Project the vector onto the line.
        vector_projected = self.direction.project_vector(vector_to_point)

        # Add the projected vector to the point on the line.
        return self.point + vector_projected

    def project_vector(self, vector):
        """Project a vector onto the line."""
        return self.direction.project_vector(vector)

    def side_point(self, point):
        """
        Find the side of the line where a point lies.

        The line and point must be 2D.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        scalar
            -1 if the point is left of the line.
            0 if the point is on the line.
            1 if the point is right of the line.

        Examples
        --------
        >>> from skspatial.objects import Line
        >>> line = Line([0, 0], [0, 1])

        >>> line.side_point([1, 1])
        1

        >>> line.side_point([1, -10])
        1

        >>> line.side_point([-4, 10])
        -1

        >>> line = Line([0, 0], [1, 1])
        >>> line.side_point([1, 5])
        -1

        """
        vector_to_point = Vector.from_points(self.point, point)

        return self.direction.side_vector(vector_to_point)

    def distance_line(self, other):
        """
        Return the shortest distance from an other line to self.

        Parameters
        ----------
        other : Line
            Input line.

        Returns
        -------
        scalar
            The distance between the lines.

        References
        ----------
        http://mathworld.wolfram.com/Line-LineDistance.html

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line_a = Line([0, 0], [1, 0])
        >>> line_b = Line([0, 1], [1, 0])
        >>> line_c = Line([0, 1], [1, 1])

        The lines are parallel.

        >>> line_a.distance_line(line_b)
        1.0

        The lines are coplanar and not parallel.

        >>> line_a.distance_line(line_c)
        0.0

        The lines are skew.

        >>> line_a = Line([0, 0, 0], [1, 0, 0])
        >>> line_b = Line([0, 5, 0], [0, 0, 1])
        >>> line_a.distance_line(line_b)
        5.0

        """
        if self.direction.is_parallel(other.direction):
            # The lines are parallel.
            # The distance between the lines is the distance from line point B to line A.
            distance = self.distance_point(other.point)

        elif self.is_coplanar(other):
            # The lines must intersect, since they are coplanar and not parallel.
            distance = np.float64(0)

        else:
            # The lines are skew.
            vector_ab = Vector.from_points(self.point, other.point)
            vector_perpendicular = self.direction.cross(other.direction)

            distance = (
                abs(vector_ab.dot(vector_perpendicular)) / vector_perpendicular.norm()
            )

        return distance

    def intersect_line(self, other):
        """
        Return the intersection of a line with self.

        The lines must be coplanar and not parallel.

        Parameters
        ----------
        other : Line
            Input line.

        Returns
        -------
        Point
            The point at the intersection.

        Raises
        ------
        ValueError
            If the lines are parallel or are not coplanar.

        References
        ----------
        http://mathworld.wolfram.com/Line-LineIntersection.html

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line_a = Line([0, 0], [1, 0])
        >>> line_b = Line([5, 5], [0, 1])

        >>> line_a.intersect_line(line_b)
        Point([5., 0.])

        >>> line_b = Line([0, 1], [2, 0])
        >>> line_a.intersect_line(line_b)
        Traceback (most recent call last):
        ...
        ValueError: The lines must not be parallel.

        >>> line_a = Line([1, 2, 3], [-4, 1, 1])
        >>> line_b = Line([4, 5, 6], [3, 1, 5])

        >>> line_a.intersect_line(line_b)
        Traceback (most recent call last):
        ...
        ValueError: The lines must be coplanar.

        >>> line_a = Line([0, 0, 0], [1, 1, 1])
        >>> line_b = Line([5, 5, 0], [0, 0, -8])

        >>> line_a.intersect_line(line_b)
        Point([5., 5., 5.])

        """
        if self.direction.is_parallel(other.direction):
            raise ValueError("The lines must not be parallel.")

        if not self.is_coplanar(other):
            raise ValueError("The lines must be coplanar.")

        # Vector from line A to line B.
        vector_ab = Vector.from_points(self.point, other.point)

        # Vector perpendicular to both lines.
        vector_perpendicular = self.direction.cross(other.direction)

        num = vector_ab.cross(other.direction).dot(vector_perpendicular)
        denom = vector_perpendicular.norm() ** 2

        # Vector along line A to the intersection point.
        vector_a_scaled = num / denom * self.direction

        return self.point + vector_a_scaled

    @classmethod
    def best_fit(cls, points):
        """
        Return the line of best fit for a set of points.

        Parameters
        ----------
        points : array_like
             Input points.

        Returns
        -------
        Line
            The line of best fit.

        Raises
        ------
        ValueError
            If the points are concurrent.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> points = ([1, 0], [2, 0], [3, 0])
        >>> line = Line.best_fit(points)

        >>> line.point
        Point([2., 0.])

        >>> line.direction
        Vector([1., 0.])

        """
        points = Points(points)

        if points.are_concurrent(tol=0):
            raise ValueError("The points must not be concurrent.")

        points_centered, centroid = points.mean_center()

        _, _, vh = np.linalg.svd(points_centered)
        direction = vh[0, :]

        return cls(centroid, direction)

    def transform_points(self, points):
        """
        Transform points to a one-dimensional coordinate system defined by a line.

        The point on the line acts as the origin of the coordinate system.

        This is analogous is projecting the points onto the line,
        then computing the signed distance from the line point to the projections.

        Parameters
        ----------
        points : (N, D) array_like
            Array of N points with dimension D.

        Returns
        -------
        ndarray
            (N,) array of N coordinates.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line = Line(point=[0, 0, 0], direction=[1, 0, 0])
        >>> points = [[10, 2, 0], [3, 4, 0], [-5, 5, 0]]

        >>> line.transform_points(points)
        array([10.,  3., -5.])

        """
        # Basis vector of the subspace (the line).
        vectors_basis = [self.direction.unit()]

        column = transform_coordinates(points, self.point, vectors_basis)

        return column.flatten()

    def plot_2d(self, ax_2d, t_1=0, t_2=1, **kwargs):
        """
        Plot a 2D line.

        The line is plotted by connecting two 2D points.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        t_1, t_2 : scalar
            Parameters to determine points 1 and 2 along the line.
            These are passed to :meth:`Line.to_point`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.plot`.

        """
        point_1 = self.to_point(t_1)
        point_2 = self.to_point(t_2)

        _connect_points_2d(ax_2d, point_1, point_2, **kwargs)

    def plot_3d(self, ax_3d, t_1=0, t_2=1, **kwargs):
        """
        Plot a 3D line.

        The line is plotted by connecting two 3D points.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        t_1, t_2 : scalar
            Parameters to determine points 1 and 2 along the line.
            These are passed to :meth:`Line.to_point`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Line

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> line = Line([1, 2, 3], [0, 1, 1])

            >>> line.plot_3d(ax, c='k')
            >>> line.point.plot_3d(ax, s=100)

        """
        point_1 = self.to_point(t_1)
        point_2 = self.to_point(t_2)

        _connect_points_3d(ax_3d, point_1, point_2, **kwargs)
