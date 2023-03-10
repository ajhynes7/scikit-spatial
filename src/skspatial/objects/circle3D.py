"""Module for the Circle class."""
from __future__ import annotations

import math
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from skspatial._functions import np_float
from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects.circle import Circle
from skspatial.objects.line import Line
from skspatial.objects.plane import Plane
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Circle3D(_BaseSphere):
    """
    A circle in 3D space.

    The circle is defined by a 3D point, a radius and a plane.

    Parameters
    ----------
    point : (3,) array_like
        Center of the circle.
    radius : {int, float}
        Radius of the circle/
    plane : (3,2) array_like
        Plane that circle inhabits

    Attributes
    ----------
    point : (3,) array_like
        Center of the circle.
    radius : {int, float}
        Radius of the circle.
    plane : (3,2) array_like
        Plane that circle inhabits
    dimension : int
        Dimension of the circle.

    Raises
    ------
    ValueError
        If the radius is not positive.
        If the point is not 3D.

    Examples
    --------

    sphere = Sphere([3, 2, 1], 4)
    plane = Plane([0, 0, 0], [1, 0, 1])
    circle3D = sphere.intersect_plane(plane)

    """

    def __init__(self, point: array_like, radius: float, plane: Plane):

        super().__init__(point, radius)
        self.plane = plane

        if self.point.dimension != 3:
            raise ValueError("The point must be 3D.")

    # @classmethod
    # def from_points(cls, point_a: array_like, point_b: array_like, point_c: array_like, **kwargs) -> Circle:
    #     """
    #     Instantiate a circle from three points.

    #     Parameters
    #     ----------
    #     point_a, point_b, point_c: array_like
    #         Three points defining the circle. The points must be 2D.
    #     kwargs: dict, optional
    #         Additional keywords passed to :meth:`Points.are_collinear`.

    #     Returns
    #     -------
    #     Circle
    #         Circle containing the three input points.

    #     Raises
    #     ------
    #     ValueError
    #         If the points are not 2D.
    #         If the points are collinear.

    #     Examples
    #     --------
    #     >>> from skspatial.objects import Circle

    #     >>> Circle.from_points([-1, 0], [0, 1], [1, 0])
    #     Circle(point=Point([-0.,  0.]), radius=1.0)

    #     >>> Circle.from_points([1, 0, 0], [0, 1], [1, 0])
    #     Traceback (most recent call last):
    #     ...
    #     ValueError: The points must be 2D.

    #     >>> Circle.from_points([0, 0], [1, 1], [2, 2])
    #     Traceback (most recent call last):
    #     ...
    #     ValueError: The points must not be collinear.

    #     """

    #     def _minor(array, i: int, j: int):
    #         subarray = array[
    #             np.array(list(range(i)) + list(range(i + 1, array.shape[0])))[:, np.newaxis],
    #             np.array(list(range(j)) + list(range(j + 1, array.shape[1]))),
    #         ]
    #         return np.linalg.det(subarray)

    #     point_a = Point(point_a)
    #     point_b = Point(point_b)
    #     point_c = Point(point_c)

    #     if any(point.dimension != 2 for point in [point_a, point_b, point_c]):
    #         raise ValueError("The points must be 2D.")

    #     if Points([point_a, point_b, point_c]).are_collinear(**kwargs):
    #         raise ValueError("The points must not be collinear.")

    #     x_a, y_a = point_a
    #     x_b, y_b = point_b
    #     x_c, y_c = point_c

    #     matrix = np.array(
    #         [
    #             [0, 0, 0, 1],
    #             [x_a**2 + y_a**2, x_a, y_a, 1],
    #             [x_b**2 + y_b**2, x_b, y_b, 1],
    #             [x_c**2 + y_c**2, x_c, y_c, 1],
    #         ],
    #     )

    #     M_00 = _minor(matrix, 0, 0)
    #     M_01 = _minor(matrix, 0, 1)
    #     M_02 = _minor(matrix, 0, 2)
    #     M_03 = _minor(matrix, 0, 3)

    #     x = 0.5 * M_01 / M_00
    #     y = -0.5 * M_02 / M_00

    #     radius = math.sqrt(x**2 + y**2 + M_03 / M_00)

    #     return cls([x, y], radius)

    # @np_float
    # def circumference(self) -> float:
    #     r"""
    #     Return the circumference of the circle.

    #     The circumference :math:`C` of a circle with radius :math:`r` is

    #     .. math:: C = 2 \pi r

    #     Returns
    #     -------
    #     np.float64
    #         Circumference of the circle.

    #     Examples
    #     --------
    #     >>> from skspatial.objects import Circle

    #     >>> Circle([0, 0], 1).area().round(2)
    #     3.14

    #     >>> Circle([0, 0], 2).area().round(2)
    #     12.57

    #     """
    #     return 2 * np.pi * self.radius

    # @np_float
    # def area(self) -> float:
    #     r"""
    #     Return the area of the circle.

    #     The area :math:`A` of a circle with radius :math:`r` is

    #     .. math:: A = \pi r ^ 2

    #     Returns
    #     -------
    #     np.float64
    #         Area of the circle.

    #     Examples
    #     --------
    #     >>> from skspatial.objects import Circle

    #     >>> Circle([0, 0], 1).area().round(2)
    #     3.14

    #     >>> Circle([0, 0], 2).area().round(2)
    #     12.57

    #     """
    #     return np.pi * self.radius**2

    # TODO Need to check if belongs on same plane
    # def intersect_circle(self, other: Circle) -> Tuple[Point, Point]:
    #     """
    #     Intersect the circle with another circle.

    #     A circle intersects a circle at two points.

    #     Parameters
    #     ----------
    #     other : Circle
    #         Other circle.

    #     Returns
    #     -------
    #     point_a, point_b : Point
    #         The two points of intersection.

    #     Raises
    #     ------
    #     ValueError
    #         If the centres of the circles are coincident.
    #         If the circles are separate.
    #         If one circle is contained within the other.

    #     References
    #     ----------
    #     http://paulbourke.net/geometry/circlesphere/

    #     Examples
    #     --------
    #     >>> from skspatial.objects import Circle

    #     >>> circle_a = Circle([0, 0], 1)
    #     >>> circle_b = Circle([2, 0], 1)

    #     >>> circle_a.intersect_circle(circle_b)
    #     (Point([1., 0.]), Point([1., 0.]))

    #     >>> circle_a.intersect_circle(Circle([0, 0], 2))
    #     Traceback (most recent call last):
    #     ...
    #     ValueError: The centres of the circles are coincident.

    #     >>> circle_a.intersect_circle(Circle([3, 0], 1))
    #     Traceback (most recent call last):
    #     ...
    #     ValueError: The circles do not intersect. These circles are separate.

    #     >>> Circle([0, 0], 3).intersect_circle(Circle([1, 0], 1))
    #     Traceback (most recent call last):
    #     ...
    #     ValueError: The circles do not intersect. One circle is contained within the other.

    #     """

    #     # From my own repository: https://github.com/Yeok-c/Stewart_Py/blob/main/src/stewart_controller.py
    #     def _rotX(phi):
    #         rotx = np.array([
    #             [1,     0    ,    0    ],
    #             [0,  np.cos(phi), -np.sin(phi)],
    #             [0,  np.sin(phi), np.cos(phi)] ])
    #         return rotx

    #     def _rotY(theta):    
    #         roty = np.array([
    #             [np.cos(theta), 0, np.sin(theta) ],
    #             [0         , 1,     0       ],
    #             [-np.sin(theta), 0,  np.cos(theta) ] ])   
    #         return roty
            
    #     def _rotZ(psi):    
    #         rotz = np.array([
    #             [ np.cos(psi), -np.sin(psi), 0 ],
    #             [np.sin(psi), np.cos(psi), 0 ],
    #             [   0        ,     0      , 1 ] ])   
    #         return rotz

    #     # From https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python


    #     def _angle_between(v1, v2):
    #         def _unit_vector(vector):       
    #             return vector / np.linalg.norm(vector)
    #         v1_u = _unit_vector(v1)
    #         v2_u = _unit_vector(v2)
    #         return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    #     # Rotate to 2D plane first
    #     angle = _angle_between([0, 0, 1], self.plane)
    #     R = np.matmul( np.matmul(_rotZ(rotation[2]), _rotY(rotation[1])), _rotX(rotation[0]) )

    #     d = self.point.distance_point(other.point)

    #     if d == 0:
    #         raise ValueError("The centres of the circles are coincident.")

    #     if d > self.radius + other.radius:
    #         raise ValueError("The circles do not intersect. These circles are separate.")

    #     if d < abs(self.radius - other.radius):
    #         raise ValueError("The circles do not intersect. One circle is contained within the other.")

    #     a = (self.radius**2 - other.radius**2 + d**2) / (2 * d)

    #     h = math.sqrt(self.radius**2 - a**2)

    #     point_middle = self.point + a * Vector.from_points(self.point, other.point) / d

    #     pm = np.array([1, -1])

    #     X = point_middle[0] + pm * h * (self.point[1] - other.point[1]) / d
    #     Y = point_middle[1] - pm * h * (self.point[0] - other.point[0]) / d

    #     point_a = Point([X[0], Y[0]])
    #     point_b = Point([X[1], Y[1]])

    #     return point_a, point_b

    # # TODO Need to check if belongs on same plane
    # def intersect_line(self, line: Line) -> Tuple[Point, Point]:
    #     """
    #     Intersect the circle with a line.

    #     A line intersects a circle at two points.

    #     Parameters
    #     ----------
    #     line : Line
    #         Input line.

    #     Returns
    #     -------
    #     point_a, point_b : Point
    #         The two points of intersection.

    #     Raises
    #     ------
    #     ValueError
    #         If the line does not intersect the circle.

    #     References
    #     ----------
    #     http://mathworld.wolfram.com/Circle-LineIntersection.html

    #     Examples
    #     --------
    #     >>> from skspatial.objects import Circle, Line

    #     >>> circle = Circle([0, 0], 1)

    #     >>> circle.intersect_line(Line(point=[0, 0], direction=[1, 0]))
    #     (Point([-1.,  0.]), Point([1., 0.]))

    #     >>> point_a, point_b = circle.intersect_line(Line(point=[0, 0], direction=[1, 1]))

    #     >>> point_a.round(3)
    #     Point([-0.707, -0.707])

    #     >>> point_b.round(3)
    #     Point([0.707, 0.707])

    #     >>> circle.intersect_line(Line(point=[1, 2], direction=[1, 1]))
    #     (Point([-1.,  0.]), Point([0., 1.]))

    #     If the line is tangent to the circle, the two intersection points are the same.

    #     >>> circle.intersect_line(Line(point=[1, 0], direction=[0, 1]))
    #     (Point([1., 0.]), Point([1., 0.]))

    #     The circle does not have to be centered on the origin.

    #     >>> point_a, point_b = Circle([2, 3], 5).intersect_line(Line([1, 1], [2, 3]))

    #     >>> point_a.round(3)
    #     Point([-0.538, -1.308])

    #     >>> point_b.round(3)
    #     Point([5., 7.])

    #     >>> circle.intersect_line(Line(point=[5, 0], direction=[1, 1]))
    #     Traceback (most recent call last):
    #     ...
    #     ValueError: The line does not intersect the circle.

    #     """
    #     # Two points on the line.
    #     point_1 = line.point
    #     point_2 = point_1 + line.direction.unit()

    #     # Translate the points on the line to mimic the circle being centered on the origin.
    #     point_translated_1 = point_1 - self.point
    #     point_translated_2 = point_2 - self.point

    #     x_1, y_1 = point_translated_1
    #     x_2, y_2 = point_translated_2

    #     d_x = x_2 - x_1
    #     d_y = y_2 - y_1

    #     # Pre-compute variables common to x and y equations.
    #     d_r_squared = d_x**2 + d_y**2
    #     determinant = x_1 * y_2 - x_2 * y_1
    #     discriminant = self.radius**2 * d_r_squared - determinant**2

    #     if discriminant < 0:
    #         raise ValueError("The line does not intersect the circle.")

    #     root = math.sqrt(discriminant)

    #     mp = np.array([-1, 1])  # Array to compute minus/plus.
    #     sign = -1 if d_y < 0 else 1

    #     coords_x = (determinant * d_y + mp * sign * d_x * root) / d_r_squared
    #     coords_y = (-determinant * d_x + mp * abs(d_y) * root) / d_r_squared

    #     point_translated_a = Point([coords_x[0], coords_y[0]])
    #     point_translated_b = Point([coords_x[1], coords_y[1]])

    #     # Translate the intersection points back from origin circle to real circle.
    #     point_a = point_translated_a + self.point
    #     point_b = point_translated_b + self.point

    #     return point_a, point_b

    def plot_3d(self, ax_3d: Axes, **kwargs) -> None:
        """
        Plot the circle in 3D.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        kwargs : dict, optional
            Additional keywords passed to :class:`matplotlib.patches.Circle`.

        Examples
        --------
        .. plot::
            :include-source:

            from skspatial.objects import Plane, Sphere, Circle, Circle3D
            from skspatial.plotting import plot_3d

            sphere = Sphere([3, 2, 1], 4)
            plane = Plane([0, 0, 0], [1, 0, 1])

            circle3D = sphere.intersect_plane(plane)

            plot_3d(
                plane.plotter(alpha=0.2),
                sphere.plotter(alpha=0.2),
                circle3D.plotter(),
            )

        """
        # Solution based on
        # https://stackoverflow.com/questions/3461869/plot-a-plane-based-on-a-normal-vector-and-a-point-in-matlab-or-matplotlib
        from mpl_toolkits.mplot3d import axes3d
        from matplotlib.patches import Circle as circle_patch
        import matplotlib.pyplot as plt
        from matplotlib.transforms import Affine2D
        from mpl_toolkits.mplot3d import art3d
        import numpy as np

        def rotation_matrix(d):
            sin_angle = np.linalg.norm(d)
            if sin_angle == 0:
                return np.identity(3)
            d /= sin_angle
            eye = np.eye(3)
            ddt = np.outer(d, d)
            skew = np.array([[0, d[2], -d[1]], [-d[2], 0, d[0]], [d[1], -d[0], 0]], dtype=np.float64)

            M = ddt + np.sqrt(1 - sin_angle**2) * (eye - ddt) + sin_angle * skew
            return M

        def pathpatch_2d_to_3d(pathpatch, z, normal):
            if type(normal) is str:  # Translate strings to normal vectors
                index = "xyz".index(normal)
                normal = np.roll((1.0, 0, 0), index)
            normal = normal.astype(float)
            normal /= np.linalg.norm(normal)  # Make sure the vector is normalised
            path = pathpatch.get_path()  # Get the path and the associated transform
            trans = pathpatch.get_patch_transform()

            path = trans.transform_path(path)  # Apply the transform

            pathpatch.__class__ = art3d.PathPatch3D  # Change the class
            pathpatch._code3d = path.codes  # Copy the codes
            pathpatch._facecolor3d = pathpatch.get_facecolor  # Get the face color

            verts = path.vertices  # Get the vertices in 2D

            d = np.cross(normal, (0, 0, 1))  # Obtain the rotation vector
            M = rotation_matrix(d)  # Get the rotation matrix

            pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + (0, 0, z) for x, y in verts])

        def pathpatch_translate(pathpatch, delta):
            pathpatch._segment3d += delta

        def plot_Circle3D(ax, point, normal, size=10, color='y', fill=False):
            p = circle_patch((0, 0), size, facecolor=color, alpha=0.5, fill=fill)
            ax.add_patch(p)
            pathpatch_2d_to_3d(p, z=0, normal=normal)
            pathpatch_translate(p, (point[0], point[1], point[2]))
            return ax
            
        circle = plot_Circle3D(ax_3d, self.point, self.plane.normal, size=self.radius, color='y', fill=False) # **kwargs)
        # ax_3d.add_artist(circle)
        # ax_3d.set_aspect('equal')


                
        ax_3d.set_aspect('equal')
        
        ax_3d.set_xlim([-80, 80])
        ax_3d.set_ylim([-80, 80])
        ax_3d.set_zlim([-80, 80])
        ax_3d.view_init(elev=16, azim=45, roll=0)
            # ax_3d.view_init(elev=10, azim=150, roll=0)
