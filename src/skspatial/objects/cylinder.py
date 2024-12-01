"""Module for the Cylinder class."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import minimize

from skspatial._functions import _solve_quadratic
from skspatial.objects._base_spatial import _BaseSpatial
from skspatial.objects._mixins import _ToPointsMixin
from skspatial.objects.line import Line
from skspatial.objects.plane import Plane
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Cylinder(_BaseSpatial, _ToPointsMixin):
    """
    A cylinder in space.

    The cylinder is defined by a point at its base, a vector along its axis, and a radius.

    Parameters
    ----------
    point : array_like
        Centre of the cylinder base.
    vector : array_like
        Normal vector of the cylinder base (the vector along the cylinder axis).
        The length of the cylinder is the length of this vector.
    radius : {int, float}
        Radius of the cylinder.
        This is the radius of the circular base.

    Attributes
    ----------
    point : Point
        Centre of the cylinder base.
    vector : Vector
        Normal vector of the cylinder base.
    radius : {int, float}
        Radius of the cylinder.
    dimension : int
        Dimension of the cylinder.

    Raises
    ------
    ValueError
        If the point or vector are not 3D.
        If the vector is all zeros.
        If the radius is zero.

    Examples
    --------
    >>> from skspatial.objects import Cylinder

    >>> Cylinder([0, 0], [1, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The point must be 3D.

    >>> Cylinder([0, 0, 0], [1, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The vector must be 3D.

    >>> Cylinder([0, 0, 0], [0, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The vector must not be the zero vector.

    >>> Cylinder([0, 0, 0], [0, 0, 1], 0)
    Traceback (most recent call last):
    ...
    ValueError: The radius must be positive.

    >>> cylinder = Cylinder([0, 0, 0], [0, 0, 1], 1)

    >>> cylinder
    Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 1]), radius=1)

    >>> cylinder.point
    Point([0, 0, 0])
    >>> cylinder.vector
    Vector([0, 0, 1])
    >>> cylinder.radius
    1
    >>> cylinder.dimension
    3

    """

    def __init__(self, point: array_like, vector: array_like, radius: float):
        self.point = Point(point)
        self.vector = Vector(vector)

        if self.point.dimension != 3:
            raise ValueError("The point must be 3D.")

        if self.vector.dimension != 3:
            raise ValueError("The vector must be 3D.")

        if self.vector.is_zero():
            raise ValueError("The vector must not be the zero vector.")

        if not radius > 0:
            raise ValueError("The radius must be positive.")

        self.radius = radius

        self.dimension = self.point.dimension

    def __repr__(self) -> str:
        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return f"Cylinder(point={repr_point}, vector={repr_vector}, radius={self.radius})"

    @classmethod
    def from_points(cls, point_a: array_like, point_b: array_like, radius: float) -> Cylinder:
        """
        Instantiate a cylinder from two points and a radius.

        Parameters
        ----------
        point_a, point_b : array_like
            The centres of the two circular ends.
        radius : float
            The cylinder radius.

        Returns
        -------
        Cylinder
            The cylinder defined by the two points and the radius.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder.from_points([0, 0, 0], [0, 0, 1], 1)
        Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 1]), radius=1)

        >>> Cylinder.from_points([0, 0, 0], [0, 0, 2], 1)
        Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 2]), radius=1)

        """
        vector_ab = Vector.from_points(point_a, point_b)

        return cls(point_a, vector_ab, radius)

    def length(self) -> np.float64:
        """
        Return the length of the cylinder.

        This is the length of the vector used to initialize the cylinder.

        Returns
        -------
        np.float64
            Length of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder([0, 0, 0], [0, 0, 1], 1).length()
        np.float64(1.0)

        >>> Cylinder([0, 0, 0], [0, 0, 2], 1).length()
        np.float64(2.0)

        >>> Cylinder([0, 0, 0], [1, 1, 1], 1).length().round(3)
        np.float64(1.732)

        """
        return self.vector.norm()

    def lateral_surface_area(self) -> np.float64:
        """
        Return the lateral surface area of the cylinder.

        Returns
        -------
        np.float64
            Lateral surface area of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder([0, 0, 0], [0, 0, 1], 1).lateral_surface_area().round(3)
        np.float64(6.283)

        >>> Cylinder([0, 0, 0], [0, 0, 1], 2).lateral_surface_area().round(3)
        np.float64(12.566)

        >>> Cylinder([0, 0, 0], [0, 0, 2], 2).lateral_surface_area().round(3)
        np.float64(25.133)

        """
        return 2 * np.pi * self.radius * self.length()

    def surface_area(self) -> np.float64:
        """
        Return the total surface area of the cylinder.

        This is the lateral surface area plus the area of the two circular caps.

        Returns
        -------
        np.float64
            Total surface area of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder([0, 0, 0], [0, 0, 1], 1).surface_area().round(3)
        np.float64(12.566)

        >>> Cylinder([0, 0, 0], [0, 0, 1], 2).surface_area().round(3)
        np.float64(37.699)

        >>> Cylinder([0, 0, 0], [0, 0, 2], 2).surface_area().round(3)
        np.float64(50.265)

        """
        return self.lateral_surface_area() + 2 * np.pi * self.radius**2

    def volume(self) -> np.float64:
        r"""
        Return the volume of the cylinder.

        The volume :math:`V` of a cylinder with radius :math:`r` and length :math:`l` is

        .. math:: V = \pi r^2 l

        Returns
        -------
        np.float64
            Volume of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder([0, 0, 0], [0, 0, 1], 1).volume().round(5)
        np.float64(3.14159)

        The length of the vector sets the length of the cylinder.

        >>> Cylinder([0, 0, 0], [0, 0, 2], 1).volume().round(5)
        np.float64(6.28319)

        """
        return np.pi * self.radius**2 * self.length()

    def is_point_within(self, point: array_like) -> bool:
        """
        Check if a point is within the cylinder.

        This also includes a point on the surface.

        Parameters
        ----------
        point : array_like
            Input point

        Returns
        -------
        bool
            True if the point is within the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> cylinder = Cylinder([0, 0, 0], [0, 0, 1], 1)

        >>> cylinder.is_point_within([0, 0, 0])
        True
        >>> cylinder.is_point_within([0, 0, 1])
        True
        >>> cylinder.is_point_within([0, 0, 2])
        False
        >>> cylinder.is_point_within([0, 0, -1])
        False
        >>> cylinder.is_point_within([1, 0, 0])
        True
        >>> cylinder.is_point_within([0, 1, 0])
        True
        >>> cylinder.is_point_within([1, 1, 0])
        False

        """
        line_axis = Line(self.point, self.vector)
        distance_to_axis = line_axis.distance_point(point)

        within_radius = distance_to_axis <= self.radius

        between_cap_planes = _between_cap_planes(self, point)

        return bool(within_radius and between_cap_planes)

    def intersect_line(
        self,
        line: Line,
        n_digits: Optional[int] = None,
        infinite: bool = True,
    ) -> Tuple[Point, Point]:
        """
        Intersect the cylinder with a 3D line.

        By default, this method treats the cylinder as infinite along its axis (i.e., without caps).

        Parameters
        ----------
        line : Line
            Input 3D line.
        n_digits : int, optional
            Additional keywords passed to :func:`round`.
            This is used to round the coefficients of the quadratic equation.
        infinite : bool
            If True, the cylinder is treated as infinite along its axis (i.e., without caps).

        Returns
        -------
        point_a, point_b: Point
            The two intersection points of the line with the cylinder, if they exist.

        Raises
        ------
        ValueError
            If the line is not 3D.
            If the line does not intersect the cylinder at one or two points.

        References
        ----------
        https://mrl.cs.nyu.edu/~dzorin/rendering/lectures/lecture3/lecture3.pdf

        Examples
        --------
        >>> from skspatial.objects import Line, Cylinder

        >>> cylinder = Cylinder([0, 0, 0], [0, 0, 1], 1)
        >>> line = Line([0, 0, 0], [1, 0, 0])


        Intersection with an infinite cylinder.

        >>> cylinder.intersect_line(line)
        (Point([-1.,  0.,  0.]), Point([1., 0., 0.]))

        >>> line = Line([1, 2, 3], [1, 2, 3])

        >>> point_a, point_b = cylinder.intersect_line(line)

        >>> point_a.round(3)
        Point([-0.447, -0.894, -1.342])
        >>> point_b.round(3)
        Point([0.447, 0.894, 1.342])

        >>> cylinder.intersect_line(Line([0, 0], [1, 2]))
        Traceback (most recent call last):
        ...
        ValueError: The line must be 3D.

        >>> cylinder.intersect_line(Line([0, 0, 2], [0, 0, 1]))
        Traceback (most recent call last):
        ...
        ValueError: The line does not intersect the cylinder.

        >>> cylinder.intersect_line(Line([2, 0, 0], [0, 1, 1]))
        Traceback (most recent call last):
        ...
        ValueError: The line does not intersect the cylinder.


        Intersection with a finite cylinder.

        >>> point_a, point_b = cylinder.intersect_line(Line([0, 0, 0], [0, 0, 1]), infinite=False)

        >>> point_a
        Point([0., 0., 0.])
        >>> point_b
        Point([0., 0., 1.])

        >>> cylinder = Cylinder([0, 0, 0], [0, 0, 5], 1)

        >>> point_a, point_b = cylinder.intersect_line(Line([0, 0, 0], [1, 0, 1]), infinite=False)

        >>> point_a
        Point([0., 0., 0.])
        >>> point_b
        Point([1., 0., 1.])

        """
        if line.dimension != 3:
            raise ValueError("The line must be 3D.")

        if infinite:
            return _intersect_line_with_infinite_cylinder(self, line, n_digits)

        return _intersect_line_with_finite_cylinder(self, line, n_digits)

    def to_mesh(self, n_along_axis: int = 100, n_angles: int = 30) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Return coordinate matrices for the 3D surface of the cylinder.

        Parameters
        ----------
        n_along_axis : int
            Number of intervals along the axis of the cylinder.
        n_angles : int
            Number of angles distributed around the circle.

        Returns
        -------
        X, Y, Z: (n_angles, n_angles) ndarray
            Coordinate matrices.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> X, Y, Z = Cylinder([0, 0, 0], [0, 0, 1], 1).to_mesh(2, 4)

        >>> X.round(3)
        array([[-1. , -1. ],
               [ 0.5,  0.5],
               [ 0.5,  0.5],
               [-1. , -1. ]])

        >>> Y.round(3)
        array([[ 0.   ,  0.   ],
               [ 0.866,  0.866],
               [-0.866, -0.866],
               [-0.   , -0.   ]])

        >>> Z.round(3)
        array([[0., 1.],
               [0., 1.],
               [0., 1.],
               [0., 1.]])

        """
        # Unit vector along the cylinder axis.
        v_axis = self.vector.unit()

        # Arbitrary unit vector in a direction other than the axis.
        # This is used to get a vector perpendicular to the axis.
        v_different_direction = v_axis.different_direction()

        # Two unit vectors that are mutually perpendicular
        # and perpendicular to the cylinder axis.
        # These are used to define the points on the cylinder surface.
        u_1 = v_axis.cross(v_different_direction).unit()
        u_2 = v_axis.cross(u_1).unit()

        # The cylinder surface ranges over t from 0 to length of axis,
        # and over theta from 0 to 2 * pi.
        t = np.linspace(0, self.length(), n_along_axis)
        theta = np.linspace(0, 2 * np.pi, n_angles)

        # use meshgrid to make 2d arrays
        t, theta = np.meshgrid(t, theta)

        X, Y, Z = [
            self.point[i] + v_axis[i] * t + self.radius * np.sin(theta) * u_1[i] + self.radius * np.cos(theta) * u_2[i]
            for i in range(3)
        ]

        return X, Y, Z

    @classmethod
    def best_fit(cls, points: array_like) -> Cylinder:
        """
        Return the cylinder of best fit for a set of 3D points.

        The points are assumed to lie close to the cylinder surface. The algorithm is not guaranteed to produce a
        meaningful solution with random points.

        Parameters
        ----------
        points : array_like
             Input 3D points. At least six points must be provided.

        Returns
        -------
        Cylinder
            The cylinder of best fit.

        Raises
        ------
        ValueError
            If the points are not 3D.
            If there are fewer than six points.
            If the points are coplanar.

        References
        ----------
        https://www.geometrictools.com/Documentation/LeastSquaresFitting.pdf
        https://github.com/xingjiepan/cylinder_fitting
        https://github.com/CristianoPizzamiglio/py-cylinder-fitting

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> points = [[0, 2, 0], [0, -2, 0], [0, 0, 2], [5, 2, 0], [5, -2, 0], [5, 0, 2]]
        >>> cylinder = Cylinder.best_fit(points)

        >>> cylinder.point.round()
        Point([0., 0., 0.])

        >>> cylinder.vector.round()
        Vector([5., 0., 0.])

        >>> cylinder.radius
        np.float64(2.0)

        """

        def _best_fit(points_centered: Points, centroid: Point) -> Tuple[Vector, Point, float, float]:
            """Return the cylinder of best fit for a set of 3D points."""
            best_fit = minimize(
                lambda x: _compute_g(_spherical_to_cartesian(_SphericalCoordinates(x[0], x[1])), points_centered),
                x0=_compute_initial_direction(points_centered),
                method="Powell",
            )

            direction = _spherical_to_cartesian(_SphericalCoordinates(best_fit.x[0], best_fit.x[1]))
            center = cast(Point, _compute_center(direction, points_centered) + centroid)

            return direction, center, _compute_radius(direction, points_centered), best_fit.fun

        def _compute_initial_direction(points: Points) -> np.ndarray:
            """Compute the initial direction as the best fit line."""
            line_best_fit = cast(Line, Line.best_fit(points))

            initial_direction = line_best_fit.vector.unit()
            spherical_coordinates = _cartesian_to_spherical(*initial_direction)

            return np.array([spherical_coordinates.theta, spherical_coordinates.phi])

        def _compute_projection_matrix(direction: Vector) -> np.ndarray:
            return np.identity(3) - np.dot(np.reshape(direction, (3, 1)), np.reshape(direction, (1, 3)))

        def _compute_skew_matrix(direction: Vector) -> np.ndarray:
            return np.array(
                [
                    [0.0, -direction[2], direction[1]],
                    [direction[2], 0.0, -direction[0]],
                    [-direction[1], direction[0], 0.0],
                ],
            )

        def _compute_a_matrix(input_samples: List[np.ndarray]) -> np.ndarray:
            return sum(np.dot(np.reshape(sample, (3, 1)), np.reshape(sample, (1, 3))) for sample in input_samples)

        def _compute_a_hat_matrix(a_matrix: np.ndarray, skew_matrix: np.ndarray) -> np.ndarray:
            return np.dot(skew_matrix, np.dot(a_matrix, np.transpose(skew_matrix)))

        def _compute_g(direction: Vector, points: Points) -> float:
            projection_matrix = _compute_projection_matrix(direction)
            skew_matrix = _compute_skew_matrix(direction)
            input_samples = [np.dot(projection_matrix, x) for x in points]
            a_matrix = _compute_a_matrix(input_samples)
            a_hat_matrix = _compute_a_hat_matrix(a_matrix, skew_matrix)

            u = sum(np.dot(sample, sample) for sample in input_samples) / len(points)
            v = np.dot(a_hat_matrix, sum(np.dot(sample, sample) * sample for sample in input_samples)) / np.trace(
                np.dot(a_hat_matrix, a_matrix),
            )
            return sum((np.dot(sample, sample) - u - 2 * np.dot(sample, v)) ** 2 for sample in input_samples)

        def _compute_center(direction: Vector, points: Points) -> Point:
            projection_matrix = _compute_projection_matrix(direction)
            skew_matrix = _compute_skew_matrix(direction)
            input_samples = [np.dot(projection_matrix, x) for x in points]
            a_matrix = _compute_a_matrix(input_samples)
            a_hat_matrix = _compute_a_hat_matrix(a_matrix, skew_matrix)

            return Point(
                np.dot(a_hat_matrix, sum(np.dot(sample, sample) * sample for sample in input_samples))
                / np.trace(
                    np.dot(a_hat_matrix, a_matrix),
                ),
            )

        def _compute_radius(direction: Vector, points) -> float:
            projection_matrix = _compute_projection_matrix(direction)
            center = _compute_center(direction, points)
            return np.sqrt(
                sum(np.dot(center - point, np.dot(projection_matrix, center - point)) for point in points)
                / len(points),
            )

        def _cartesian_to_spherical(x: float, y: float, z: float) -> _SphericalCoordinates:
            """Convert cartesian to spherical coordinates."""
            theta = np.arccos(z / np.sqrt(x**2 + y**2 + z**2))

            if math.isclose(x, 0.0, abs_tol=1e-9) and math.isclose(y, 0.0, abs_tol=1e-9):
                phi = 0.0
            else:
                phi = np.sign(y) * np.arccos(x / np.sqrt(x**2 + y**2))
            return _SphericalCoordinates(theta, phi)

        def _spherical_to_cartesian(spherical_coordinates: _SphericalCoordinates) -> Vector:
            """Convert spherical to cartesian coordinates."""
            theta = spherical_coordinates.theta
            phi = spherical_coordinates.phi
            return Vector([np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta)])

        points = Points(points)

        if points.dimension != 3:
            raise ValueError("The points must be 3D.")

        if points.shape[0] < 6:
            raise ValueError("There must be at least 6 points.")

        if points.are_coplanar():
            raise ValueError("The points must not be coplanar.")

        points_centered, centroid = points.mean_center(return_centroid=True)
        unit_vector, center, radius, _ = _best_fit(points_centered, centroid)
        axis = Line(point=center, direction=unit_vector)
        points_1d = axis.transform_points(points)
        point_a = axis.project_point(points[np.argmin(points_1d)])
        length = point_a.distance_point(center) * 2
        vector_ab = unit_vector * length

        return cls(point_a, vector_ab, radius)

    def plot_3d(self, ax_3d: Axes3D, n_along_axis: int = 100, n_angles: int = 30, **kwargs) -> None:
        """
        Plot a 3D cylinder.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        n_along_axis : int
            Number of intervals along the axis of the cylinder.
        n_angles : int
            Number of angles distributed around the circle.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Cylinder

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> cylinder = Cylinder([5, 3, 1], [1, 0, 1], 2)

            >>> cylinder.plot_3d(ax, alpha=0.2)
            >>> cylinder.point.plot_3d(ax, s=100)

        """
        X, Y, Z = self.to_mesh(n_along_axis, n_angles)

        ax_3d.plot_surface(X, Y, Z, **kwargs)


@dataclass
class _SphericalCoordinates:
    """
    Spherical coordinates.

    Attributes
    ----------
    theta : float
        Inclination in radians.
    phi : float
        Azimuth in radians.

    """

    theta: float
    phi: float


def _between_cap_planes(cylinder: Cylinder, point: array_like) -> bool:
    """Check if a point lies between the cylinder cap planes."""
    plane_base = Plane(cylinder.point, cylinder.vector)
    distance_point_signed = plane_base.distance_point_signed(point)

    return bool(0 <= distance_point_signed <= distance_point_signed <= cylinder.length())


def _intersect_line_with_infinite_cylinder(
    cylinder: Cylinder,
    line: Line,
    n_digits: Optional[int],
) -> Tuple[Point, Point]:
    p_c = cylinder.point
    v_c = cylinder.vector.unit()
    r = cylinder.radius

    p_l = line.point
    v_l = line.vector.unit()

    delta_p = Vector.from_points(p_c, p_l)

    a = (v_l - v_l.dot(v_c) * v_c).norm() ** 2
    b = 2 * (v_l - v_l.dot(v_c) * v_c).dot(delta_p - delta_p.dot(v_c) * v_c)
    c = (delta_p - delta_p.dot(v_c) * v_c).norm() ** 2 - r**2

    try:
        X = _solve_quadratic(a, b, c, n_digits=n_digits)
    except ValueError as error:
        raise ValueError("The line does not intersect the cylinder.") from error

    point_a, point_b = p_l + X.reshape(-1, 1) * v_l

    return Point(point_a), Point(point_b)


def _intersect_line_with_caps(cylinder: Cylinder, line: Line) -> Tuple[Optional[Point], Optional[Point]]:
    """Find the intersection points of the line with the cylinder caps."""

    def _intersect_cap(plane_cap: Plane) -> Optional[Point]:
        try:
            point_intersection = plane_cap.intersect_line(line)
        except ValueError:
            return None

        return point_intersection if point_intersection.distance_point(plane_cap.point) <= cylinder.radius else None

    # The planes containing the circular caps of the cylinder.
    plane_base = Plane(point=cylinder.point, normal=cylinder.vector)
    plane_top = Plane(point=cylinder.point + cylinder.vector, normal=cylinder.vector)

    point_base = _intersect_cap(plane_base)
    point_top = _intersect_cap(plane_top)

    return point_base, point_top


def _intersect_line_with_finite_cylinder(
    cylinder: Cylinder,
    line: Line,
    n_digits: Optional[int],
) -> Tuple[Point, Point]:
    """Find intersection points of a line with a cylinder, including the cylinder caps."""
    point_base, point_top = _intersect_line_with_caps(cylinder, line)

    if point_base is not None and point_top is not None:
        return point_base, point_top

    point_a, point_b = _intersect_line_with_infinite_cylinder(cylinder, line, n_digits)

    if not _between_cap_planes(cylinder, point_a):
        point_a = cast(Point, point_base if point_base is not None else point_top)

    if not _between_cap_planes(cylinder, point_b):
        point_b = cast(Point, point_base if point_base is not None else point_top)

    if point_a is None or point_b is None:
        raise ValueError("The line does not intersect the cylinder.")

    return point_a, point_b
