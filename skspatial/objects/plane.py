"""Module for the Plane class."""

import numpy as np
from dpcontracts import require, ensure

from skspatial.objects._base_line_plane import _BaseLinePlane
from skspatial.objects.line import Line
from skspatial.objects.point import Point, Points
from skspatial.objects.vector import Vector


class Plane(_BaseLinePlane):
    """
    Plane in space.

    The plane is defined by a point and a normal vector.

    Parameters
    ----------
    point : array_like
        Point on the plane.
    direction : array_like
        Normal vector of the plane.

    Attributes
    ----------
    point : Point
        Point on the plane.
    normal : Vector
        Unit normal vector.
    vector : Vector
        Same as the normal.

    Examples
    --------
    >>> from skspatial.objects import Plane

    >>> plane = Plane(point=[0, 0, 0], normal=[0, 0, 5])

    >>> plane
    Plane(point=Point([0., 0., 0.]), normal=Vector([0., 0., 5.]))

    >>> plane.normal
    Vector([0., 0., 5.])

    The normal can also be accessed with the ``vector`` attribute.

    >>> plane.vector
    Vector([0., 0., 5.])

    """

    def __init__(self, point, normal):

        super().__init__(point, normal)
        self.normal = self.vector

    @classmethod
    @require(
        "The vectors must not be parallel.",
        lambda args: not Vector(args.vector_a).is_parallel(args.vector_b, rtol=0, atol=0),
    )
    @ensure("The output must be a plane.", lambda _, result: isinstance(result, Plane))
    def from_vectors(cls, point, vector_a, vector_b):
        """
        Instantiate a plane from a point and two vectors.

        The two vectors span the plane.

        Parameters
        ----------
        point : array_like
            Point on the plane.
        vector_a : array_like
            Input vector A.
        vector_b : array_like
            Input vector B.

        Returns
        -------
        Plane
            Plane containing input point and spanned by the two vectors.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> Plane.from_vectors([0, 0], [1, 0], [0, 1])
        Plane(point=Point([0., 0., 0.]), normal=Vector([0., 0., 1.]))

        >>> Plane.from_vectors([0, 0], [1, 0], [2, 0])
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The vectors must not be parallel.

        """
        # The cross product returns a 3D vector.
        vector_normal = Vector(vector_a).cross(vector_b)

        # Convert the point to 3D so that it matches the vector dimension.
        point = Point(point).set_dimension(3)

        return cls(point, vector_normal)

    @classmethod
    @require(
        "The points must not be collinear.",
        lambda args: not Points([args.point_a, args.point_b, args.point_c]).are_collinear(tol=0),
    )
    @ensure("The output must be a plane.", lambda _, result: isinstance(result, Plane))
    def from_points(cls, point_a, point_b, point_c):
        """
        Instantiate a plane from three points.

        The three points lie on the plane.

        Parameters
        ----------
        point_a, point_b, point_c: array_like
            Three points defining the plane.

        Returns
        -------
        Plane
            Plane containing the three input points.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> Plane.from_points([0, 0], [1, 0], [3, 3])
        Plane(point=Point([0., 0., 0.]), normal=Vector([0., 0., 3.]))

        The order of the points affects the direction of the normal vector.

        >>> Plane.from_points([0, 0], [3, 3], [1, 0])
        Plane(point=Point([0., 0., 0.]), normal=Vector([ 0.,  0., -3.]))

        >>> Plane.from_points([0, 0], [0, 1], [0, 3])
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The points must not be collinear.

        """
        vector_ab = Vector.from_points(point_a, point_b)
        vector_ac = Vector.from_points(point_a, point_c)

        return Plane.from_vectors(point_a, vector_ab, vector_ac)

    def cartesian(self):
        """
        Return the coefficients of the Cartesian equation of the plane.

        The equation has the form ax + by + cz + d = 0.

        Returns
        -------
        tuple
            Coefficients a, b, c, d.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> Plane(point=[1, 2, 0], normal=[0, 0, 1]).cartesian()
        (0.0, 0.0, 1.0, -0.0)

        >>> Plane(point=[1, 2, 8], normal=[0, 0, 5]).cartesian()
        (0.0, 0.0, 5.0, -40.0)

        >>> Plane(point=[4, 9, -1], normal=[10, 2, 4]).cartesian()
        (10.0, 2.0, 4.0, -54.0)

        """
        # The point and normal must be 3D to extract the coefficients.
        self = self.set_dimension(3)

        a, b, c = self.normal
        d = -self.normal.dot(self.point)

        return a, b, c, d

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def project_point(self, point):
        """
        Project a point onto self.

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

        """
        # Vector from the point in space to the point on the plane.
        vector_to_plane = Vector.from_points(point, self.point)

        # Perpendicular vector from the point in space to the plane.
        vector_projected = self.normal.project_vector(vector_to_plane)

        return Point(point).add(vector_projected)

    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    def project_vector(self, vector):
        """Project a vector onto the plane."""
        point_in_space = self.point.add(vector)
        point_on_plane = self.project_point(point_in_space)

        return Vector.from_points(self.point, point_on_plane)

    @ensure("The output must be a NumPy scalar.", lambda _, result: isinstance(result, np.number))
    def distance_point_signed(self, point):
        """
        Return the signed distance from a point to self.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        float
            Signed distance from the point to plane.

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

        References
        ----------
        http://mathworld.wolfram.com/Point-PlaneDistance.html

        """
        vector_to_point = Vector.from_points(self.point, point)

        return self.normal.scalar_projection(vector_to_point)

    @ensure("The output must be in the set {-1, 0, 1}.", lambda _, result: result in {-1, 0, 1})
    def side_point(self, point):
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

        >>> plane.side_point([2, 5, 0])
        0

        >>> plane.side_point([1, -5, 6])
        1

        >>> plane.side_point([5, 8, -4])
        -1

        >>> plane = Plane([0, 0, 0, 0], [0, 0, -1, 1])
        >>> plane.side_point([0, 0, 5, 1])
        -1

        """
        return np.sign(self.distance_point_signed(point)).astype(int)

    @require(
        "The line and plane must not be parallel.",
        lambda args: not args.self.normal.is_perpendicular(args.line.direction),
    )
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    @ensure("The point must be on the plane.", lambda args, result: args.self.contains_point(result))
    @ensure("The point must be on the line.", lambda args, result: args.line.contains_point(result))
    def intersect_line(self, line):
        """
        Return the intersection of self with a line.

        The line and plane must not be parallel.

        Parameters
        ----------
        line : Line
            Input line.

        Returns
        -------
        Point
            The point at the intersection.

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
        dpcontracts.PreconditionError: The line and plane must not be parallel.

        References
        ----------
        http://geomalgorithms.com/a05-_intersect-1.html

        """
        vector_plane_line = Vector.from_points(self.point, line.point)

        num = -self.normal.dot(vector_plane_line)
        denom = self.normal.dot(line.direction)

        # Vector along the line to the intersection point.
        vector_line_scaled = num / denom * line.direction

        return line.point.add(vector_line_scaled)

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
    @require("The planes must not be parallel.", lambda args: not args.self.normal.is_parallel(args.other.normal))
    @ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
    @ensure(
        "The point on the line must be on both planes.",
        lambda args, result: args.self.contains_point(result.point) and args.other.contains_point(result.point),
    )
    def intersect_plane(self, other):
        """
        Return the intersection of two planes.

        The planes must not be parallel.

        Parameters
        ----------
        other : Plane
            Input plane B.

        Returns
        -------
        Line
            The line of intersection.

        Examples
        --------
        >>> from skspatial.objects import Plane

        >>> plane_a = Plane([0, 0, 0], [0, 0, 1])
        >>> plane_b = Plane([0, 0, 0], [1, 0, 0])

        >>> plane_a.intersect_plane(plane_b)
        Line(point=Point([0., 0., 0.]), direction=Vector([0., 1., 0.]))

        >>> plane_b = Plane([5, 16, -94], [1, 0, 0])
        >>> plane_a.intersect_plane(plane_b)
        Line(point=Point([5., 0., 0.]), direction=Vector([0., 1., 0.]))

        >>> plane_b = Plane([0, 0, 1], [1, 0, 1])
        >>> plane_a.intersect_plane(plane_b)
        Line(point=Point([1., 0., 0.]), direction=Vector([0., 1., 0.]))

        >>> plane_b = Plane([0, 0, 5], [0, 0, -8])
        >>> plane_a.intersect_plane(plane_b)
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The planes must not be parallel.

        References
        ----------
        http://tbirdal.blogspot.com/2016/10/a-better-approach-to-plane-intersection.html

        """
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
    @require("The points cannot be collinear.", lambda args: not Points(args.points).are_collinear(tol=0))
    @ensure("The output must be a plane.", lambda _, result: isinstance(result, Plane))
    def best_fit(cls, points):
        """
        Return the plane of best fit for a set of points.

        The points must not have a higher dimension than 3D.

        Parameters
        ----------
        points : array_like
             Input points.

        Returns
        -------
        Plane
            The plane of best fit.

        Examples
        --------
        >>> import numpy as np
        >>> from skspatial.objects import Plane

        >>> points = ([0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0])

        >>> Plane.best_fit(points)
        Plane(point=Point([0.5, 0.5, 0. ]), normal=Vector([0., 0., 1.]))

        """
        points = Points(points)

        if points.get_dimension() < 3:
            points = points.set_dimension(3)

        points_centered, centroid = points.mean_center()

        u, s, vh = np.linalg.svd(points_centered.T)
        normal = Vector(u[:, -1])

        return cls(centroid, normal)

    @require("The plane must be 3D.", lambda args: args.self.get_dimension() == 3)
    def plot_3d(self, ax_3d, lims_x=(-1, 1), lims_y=(-1, 1), **kwargs):
        """
        Plot a 3D plane.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        lims_x, lims_y : tuple
            The x or y limits of the plane.
            Tuple of form (min, max).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`.

        """
        a, b, c, d = self.cartesian()
        x_center, y_center = self.point[:2]

        range_x = np.arange(*lims_x)
        range_y = np.arange(*lims_y)

        grid_x, grid_y = np.meshgrid(range_x, range_y)
        grid_z = -(a * grid_x + b * grid_y + d) / c

        ax_3d.plot_surface(grid_x, grid_y, grid_z, **kwargs)
