"""Module for the Plane class."""
from __future__ import annotations

from typing import Optional
from typing import Tuple

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from skspatial.objects._base_line_plane import _BaseLinePlane
from skspatial.objects._mixins import _ToPointsMixin
from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Plane(_BaseLinePlane, _ToPointsMixin):
    """
    A plane in space.

    The plane is defined by a point and a normal vector.

    Parameters
    ----------
    point : array_like
        Point on the plane.
    direction : array_like
        Normal vector of the plane.
    kwargs : dict, optional
        Additional keywords passed to :meth:`Vector.is_zero`.
        This method is used to ensure that the normal vector is not the zero vector.

    Attributes
    ----------
    point : Point
        Point on the plane.
    normal : Vector
        Unit normal vector.
    vector : Vector
        Same as the normal.
    dimension : int
        Dimension of the plane.

    Raises
    ------
    ValueError
        If the point and vector have different dimensions.
        If the vector is all zeros.

    Examples
    --------
    >>> from skspatial.objects import Plane

    >>> plane = Plane(point=[0, 0, 0], normal=[0, 0, 5])

    >>> plane
    Plane(point=Point([0, 0, 0]), normal=Vector([0, 0, 5]))

    >>> plane.normal
    Vector([0, 0, 5])

    The normal can also be accessed with the ``vector`` attribute.

    >>> plane.vector
    Vector([0, 0, 5])

    The plane dimension is the dimension of the point and vector.

    >>> plane.dimension
    3

    >>> Plane([0, 0], [1, 0, 0])
    Traceback (most recent call last):
    ...
    ValueError: The point and vector must have the same dimension.

    >>> Plane([1, 1], [0, 0])
    Traceback (most recent call last):
    ...
    ValueError: The vector must not be the zero vector.

    """

    def __init__(self, point: array_like, normal: array_like):

        super().__init__(point, normal)
        self.normal = self.vector

    @classmethod
    def from_vectors(cls, point: array_like, vector_a: array_like, vector_b: array_like, **kwargs) -> Plane:
        """
        Instantiate a plane from a point and two vectors.

        The two vectors span the plane.

        Parameters
        ----------
        point : array_like
            Point on the plane.
        vector_a, vector_b : array_like
            Input vectors.
        kwargs : dict, optional
            Additional keywords passed to :meth:`Vector.is_parallel`.

        Returns
        -------
        Plane
            Plane containing input point and spanned by the two input vectors.

        Raises
        ------
        ValueError
            If the vectors are parallel.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> Plane.from_vectors([0, 0], [1, 0], [0, 1])
        Plane(point=Point([0, 0, 0]), normal=Vector([0, 0, 1]))

        >>> Plane.from_vectors([0, 0], [1, 0], [2, 0])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must not be parallel.

        """
        vector_a = Vector(vector_a)

        if vector_a.is_parallel(vector_b, **kwargs):
            raise ValueError("The vectors must not be parallel.")

        # The cross product returns a 3D vector.
        vector_normal = vector_a.cross(vector_b)

        # Convert the point to 3D so that it matches the vector dimension.
        point = Point(point).set_dimension(3)

        return cls(point, vector_normal)

    @classmethod
    def from_points(cls, point_a: array_like, point_b: array_like, point_c: array_like, **kwargs) -> Plane:
        """
        Instantiate a plane from three points.

        The three points lie on the plane.

        Parameters
        ----------
        point_a, point_b, point_c: array_like
            Three points defining the plane.
        kwargs: dict, optional
            Additional keywords passed to :meth:`Points.are_collinear`.

        Returns
        -------
        Plane
            Plane containing the three input points.

        Raises
        ------
        ValueError
            If the points are collinear.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> Plane.from_points([0, 0], [1, 0], [3, 3])
        Plane(point=Point([0, 0, 0]), normal=Vector([0, 0, 3]))

        The order of the points affects the direction of the normal vector.

        >>> Plane.from_points([0, 0], [3, 3], [1, 0])
        Plane(point=Point([0, 0, 0]), normal=Vector([ 0,  0, -3]))

        >>> Plane.from_points([0, 0], [0, 1], [0, 3])
        Traceback (most recent call last):
        ...
        ValueError: The points must not be collinear.

        """
        if Points([point_a, point_b, point_c]).are_collinear(**kwargs):
            raise ValueError("The points must not be collinear.")

        vector_ab = Vector.from_points(point_a, point_b)
        vector_ac = Vector.from_points(point_a, point_c)

        return Plane.from_vectors(point_a, vector_ab, vector_ac)

    def cartesian(self) -> Tuple[np.number, np.number, np.number, np.number]:
        """
        Return the coefficients of the Cartesian equation of the plane.

        The equation has the form ax + by + cz + d = 0.

        Returns
        -------
        tuple
            Coefficients a, b, c, d.

        Raises
        ------
        ValueError
            If the plane dimension is higher than 3.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> Plane(point=[1, 1], normal=[1, 0]).cartesian()
        (1, 0, 0, -1)

        >>> Plane(point=[1, 2, 0], normal=[0, 0, 1]).cartesian()
        (0, 0, 1, 0)

        >>> Plane(point=[1, 2, 8], normal=[0, 0, 5]).cartesian()
        (0, 0, 5, -40)

        >>> Plane(point=[4, 9, -1], normal=[10, 2, 4]).cartesian()
        (10, 2, 4, -54)

        >>> Plane([0, 0, 0, 0], [1, 0, 0, 0]).cartesian()
        Traceback (most recent call last):
        ...
        ValueError: The plane dimension must be <= 3.

        """
        if self.dimension > 3:
            raise ValueError("The plane dimension must be <= 3.")

        # The normal must be 3D to extract the coefficients.
        a, b, c = self.normal.set_dimension(3)

        d = -self.normal.dot(self.point)

        return a, b, c, d

    def project_point(self, point: array_like) -> Point:
        """
        Project a point onto the plane.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        Point
            Projection of the point onto the plane.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> plane = Plane(point=[0, 0, 0], normal=[0, 0, 2])

        >>> plane.project_point([10, 2, 5])
        Point([10.,  2.,  0.])

        >>> plane.project_point([5, 9, -3])
        Point([5., 9., 0.])

        """
        # Vector from the point in space to the point on the plane.
        vector_to_plane = Vector.from_points(point, self.point)

        # Perpendicular vector from the point in space to the plane.
        vector_projected = self.normal.project_vector(vector_to_plane)

        return Point(point) + vector_projected

    def project_vector(self, vector: array_like) -> Vector:
        """
        Project a vector onto the plane.

        Parameters
        ----------
        vector : array_like
            Input vector.

        Returns
        -------
        Vector
            Projection of the vector onto the plane.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> plane = Plane([0, 4, 0], [0, 1, 1])

        >>> plane.project_vector([2, 4, 8])
        Vector([ 2., -2.,  2.])

        """
        point_in_space = self.point + vector
        point_on_plane = self.project_point(point_in_space)

        return Vector.from_points(self.point, point_on_plane)

    def project_line(self, line: Line, **kwargs: float) -> Line:
        """
        Project a line onto the plane.

        This method can also handle the case where the line is parallel to the plane.

        Parameters
        ----------
        line : Line
            Input line.
        kwargs : dict, optional
            Additional keywords passed to :meth:`Vector.is_perpendicular`,
            which is used to check if the line is parallel to the plane
            (i.e., the line direction is perpendicular to the plane normal).

        Returns
        -------
        Line
            Projection of the line onto the plane.

        Examples
        --------
        >>> from skspatial.objects import Line, Plane

        >>> plane = Plane([0, 0, 0], [0, 0, 1])
        >>> line = Line([0, 0, 0], [1, 1, 1])

        >>> plane.project_line(line)
        Line(point=Point([0., 0., 0.]), direction=Vector([1., 1., 0.]))

        The line is parallel to the plane.

        >>> line = Line([0, 0, 5], [1, 0, 0])

        >>> plane.project_line(line)
        Line(point=Point([0., 0., 0.]), direction=Vector([1, 0, 0]))

        """
        if self.normal.is_parallel(line.vector, **kwargs):
            raise ValueError("The line and plane must not be perpendicular.")

        point_projected = self.project_point(line.point)

        if self.normal.is_perpendicular(line.vector, **kwargs):
            return Line(point_projected, line.vector)

        vector_projected = self.project_vector(line.vector)

        return Line(point_projected, vector_projected)

    def distance_point_signed(self, point: array_like) -> np.float64:
        """
        Return the signed distance from a point to the plane.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        np.float64
            Signed distance from the point to the plane.

        References
        ----------
        http://mathworld.wolfram.com/Point-PlaneDistance.html

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> plane = Plane([0, 0, 0], [0, 0, 1])

        >>> plane.distance_point_signed([5, 2, 0])
        0.0

        >>> plane.distance_point_signed([5, 2, 1])
        1.0

        >>> plane.distance_point([5, 2, -4])
        4.0
        >>> plane.distance_point_signed([5, 2, -4])
        -4.0

        """
        vector_to_point = Vector.from_points(self.point, point)

        return self.normal.scalar_projection(vector_to_point)

    def distance_point(self, point: array_like) -> np.float64:
        """
        Return the distance from a point to the plane.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        np.float64
            Distance from the point to the plane.

        References
        ----------
        http://mathworld.wolfram.com/Point-PlaneDistance.html

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> plane = Plane([0, 0, 0], [0, 0, 1])

        >>> plane.distance_point([5, 2, 0])
        0.0

        >>> plane.distance_point([5, 2, 1])
        1.0

        >>> plane.distance_point([5, 2, -4])
        4.0

        """
        return abs(self.distance_point_signed(point))

    def side_point(self, point: array_like) -> int:
        """
        Find the side of the plane where a point lies.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        int
            -1 if the point is behind the plane.
            0 if the point is on the plane.
            1 if the point is in front of the plane.

        Examples
        --------
        >>> from skspatial.objects import Plane
        >>> plane = Plane([0, 0, 0], [0, 0, 1])

        The point is in on the plane.

        >>> plane.side_point([2, 5, 0])
        0

        The point is in front of the plane.

        >>> plane.side_point([1, -5, 6])
        1

        The point is behind the plane.

        >>> plane.side_point([5, 8, -4])
        -1

        Higher dimensions are supported.

        >>> plane = Plane([0, 0, 0, 0], [0, 1, 0, 1])
        >>> plane.side_point([0, -10, 4, 1])
        -1

        """
        return int(np.sign(self.distance_point_signed(point)))

    def intersect_line(self, line: Line, **kwargs) -> Point:
        """
        Intersect the plane with a line.

        The line and plane must not be parallel.

        Parameters
        ----------
        line : Line
            Input line.
        kwargs : dict, optional
            Additional keywords passed to :meth:`Vector.is_perpendicular`.

        Returns
        -------
        Point
            The point of intersection.

        Raises
        ------
        ValueError
            If the line and plane are parallel.

        References
        ----------
        http://geomalgorithms.com/a05-_intersect-1.html

        Examples
        --------
        >>> from skspatial.objects import Line, Plane

        >>> line = Line([0, 0, 0], [0, 0, 1])
        >>> plane = Plane([0, 0, 0], [0, 0, 1])

        >>> plane.intersect_line(line)
        Point([0., 0., 0.])

        >>> plane = Plane([2, -53, -7], [0, 0, 1])
        >>> plane.intersect_line(line)
        Point([ 0.,  0., -7.])

        >>> line = Line([0, 1, 0], [1, 0, 0])
        >>> plane.intersect_line(line)
        Traceback (most recent call last):
        ...
        ValueError: The line and plane must not be parallel.

        """
        if self.normal.is_perpendicular(line.direction, **kwargs):
            raise ValueError("The line and plane must not be parallel.")

        vector_plane_line = Vector.from_points(self.point, line.point)

        num = -self.normal.dot(vector_plane_line)
        denom = self.normal.dot(line.direction)

        # Vector along the line to the intersection point.
        vector_line_scaled = num / denom * line.direction

        return line.point + vector_line_scaled

    def intersect_plane(self, other: Plane, **kwargs) -> Line:
        """
        Intersect the plane with another.

        The planes must not be parallel.

        Parameters
        ----------
        other : Plane
            Other plane.
        kwargs : dict, optional
            Additional keywords passed to :meth:`Vector.is_parallel`.

        Returns
        -------
        Line
            The line of intersection.

        Raises
        ------
        ValueError
            If the planes are parallel.

        References
        ----------
        http://tbirdal.blogspot.com/2016/10/a-better-approach-to-plane-intersection.html

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> plane_a = Plane([0, 0, 0], [0, 0, 1])
        >>> plane_b = Plane([0, 0, 0], [1, 0, 0])

        >>> plane_a.intersect_plane(plane_b)
        Line(point=Point([0., 0., 0.]), direction=Vector([0, 1, 0]))

        >>> plane_b = Plane([5, 16, -94], [1, 0, 0])
        >>> plane_a.intersect_plane(plane_b)
        Line(point=Point([5., 0., 0.]), direction=Vector([0, 1, 0]))

        >>> plane_b = Plane([0, 0, 1], [1, 0, 1])
        >>> plane_a.intersect_plane(plane_b)
        Line(point=Point([1., 0., 0.]), direction=Vector([0, 1, 0]))

        >>> plane_b = Plane([0, 0, 5], [0, 0, -8])
        >>> plane_a.intersect_plane(plane_b)
        Traceback (most recent call last):
        ...
        ValueError: The planes must not be parallel.

        """
        if self.normal.is_parallel(other.normal, **kwargs):
            raise ValueError("The planes must not be parallel.")

        array_normals_stacked = np.vstack((self.normal, other.normal))

        # Construct a matrix for a linear system.
        array_00 = 2 * np.eye(3)
        array_01 = array_normals_stacked.T
        array_10 = array_normals_stacked
        array_11 = np.zeros((2, 2))
        matrix = np.block([[array_00, array_01], [array_10, array_11]])

        dot_a = np.dot(self.point, self.normal)
        dot_b = np.dot(other.point, other.normal)
        array_y = np.array([0, 0, 0, dot_a, dot_b])

        # Solve the linear system.
        solution = np.linalg.solve(matrix, array_y)

        point_line = Point(solution[:3])
        direction_line = self.normal.cross(other.normal)

        return Line(point_line, direction_line)

    @classmethod
    def best_fit(cls, points: array_like, tol: Optional[float] = None, **kwargs) -> Plane:
        """
        Return the plane of best fit for a set of 3D points.

        Parameters
        ----------
        points : array_like
             Input 3D points.
        tol : float | None, optional
            Keyword passed to :meth:`Points.are_collinear` (default None).
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.svd`

        Returns
        -------
        Plane
            The plane of best fit.

        Raises
        ------
        ValueError
            If the points are collinear or are not 3D.

        References
        ----------
        Using SVD for some fitting problems
        Inge Söderkvist
        Algorithm 3.1
        https://www.ltu.se/cms_fs/1.51590!/svd-fitting.pdf

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        >>> plane = Plane.best_fit(points)

        The point on the plane is the centroid of the points.

        >>> plane.point
        Point([0.25, 0.25, 0.25])

        The plane normal is a unit vector.

        >>> plane.normal.round(3)
        Vector([-0.577, -0.577, -0.577])

        >>> points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]]

        >>> Plane.best_fit(points)
        Plane(point=Point([0.5, 0.5, 0. ]), normal=Vector([0., 0., 1.]))

        >>> Plane.best_fit(points, full_matrices=False)
        Plane(point=Point([0.5, 0.5, 0. ]), normal=Vector([0., 0., 1.]))

        """
        points = Points(points)

        if points.dimension != 3:
            raise ValueError("The points must be 3D.")

        if points.are_collinear(tol=tol):
            raise ValueError("The points must not be collinear.")

        points_centered, centroid = points.mean_center(return_centroid=True)

        u, _, _ = np.linalg.svd(points_centered.T, **kwargs)
        normal = Vector(u[:, 2])

        return cls(centroid, normal)

    def to_mesh(
        self,
        lims_x: array_like = (-1, 1),
        lims_y: array_like = (-1, 1),
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Return coordinate matrices for the 3D surface of the plane.

        Parameters
        ----------
        lims_x, lims_y : (2,) tuple
            x and y limits of the plane.
            Tuple of form (min, max). The default is (-1, 1).
            The point on the plane is used as the origin.

        Returns
        -------
        X, Y, Z: ndarray
            Coordinate matrices.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> X, Y, Z = Plane([0, 0, 0], [0, 0, 1]).to_mesh()

        >>> X
        array([[-1,  1],
               [-1,  1]])

        >>> Y
        array([[-1, -1],
               [ 1,  1]])

        >>> Z
        array([[0., 0.],
               [0., 0.]])

        """
        a, b, c, d = self.cartesian()
        x_center, y_center = self.point[:2]

        values_x = x_center + lims_x
        values_y = y_center + lims_y

        X, Y = np.meshgrid(values_x, values_y)

        if c != 0:
            Z = -(a * X + b * Y + d) / c

        elif b != 0:
            Z = -(a * X + c * Y + d) / b
            X, Y, Z = X, Z, Y

        else:
            Z = -(b * X + c * Y + d) / a
            X, Y, Z = Z, X, Y

        return X, Y, Z

    def plot_3d(self, ax_3d: Axes3D, lims_x: array_like = (-1, 1), lims_y: array_like = (-1, 1), **kwargs) -> None:
        """
        Plot a 3D plane.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        lims_x, lims_y : (2,) tuple
            x and y limits of the plane.
            Tuple of form (min, max). The default is (-1, 1).
            The point on the plane is used as the origin.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Plane

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> plane = Plane([5, 3, 1], [1, 0, 1])

            >>> plane.plot_3d(ax, alpha=0.2)
            >>> plane.point.plot_3d(ax, s=100)

        """
        X, Y, Z = self.to_mesh(lims_x, lims_y)

        ax_3d.plot_surface(X, Y, Z, **kwargs)
