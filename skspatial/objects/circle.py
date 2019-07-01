"""Module for the Circle class."""

import matplotlib.pyplot as plt
import numpy as np

from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects.point import Point, Vector


class Circle(_BaseSphere):

    def __init__(self, point, radius):

        super().__init__(point, radius)

    def diameter(self):

        return 2 * self.radius

    def circumference(self):

        return 2 * np.pi * self.radius

    def area(self):

        return np.pi * self.radius ** 2

    def intersect_line(self, line):

        # Two points defining a line.
        # The points on the line are translated to mimic the circle being centered on the origin.
        vector_to_line = Vector.from_points(self.point, line.point)

        """
        # Two points on the line.
        point_1 = line.point
        point_2 = point_1 + line.direction.unit()

        # Translate the points on the line to mimic the circle being centered on the origin.
        point_1 -= self.point
        point_2 -= self.point

        x_1, y_1 = point_1
        x_2, y_2 = point_2

        d_x = x_2 - x_1
        d_y = y_2 - y_1

        # Pre-compute variables common to x and y equations.
        d_r_squared = d_x ** 2 + d_y ** 2
        determinant = x_1 * y_2 - x_2 * y_1
        discriminant = self.radius ** 2 * d_r_squared - determinant ** 2

        if discriminant < 0:
            raise ValueError("The line does not intersect the circle.")

        root = np.sqrt(discriminant)

        pm = np.array([-1, 1])  # Array to compute plus/minus.
        sign = -1 if d_y < 0 else 1

        coords_x = (determinant * d_y + pm * sign * d_x * root) / d_r_squared
        coords_y = (-determinant * d_x + pm * abs(d_y) * root) / d_r_squared

        point_a = Point([coords_x[0], coords_y[0]])
        point_b = Point([coords_x[1], coords_y[1]])

        # Translate the intersection points back from origin circle to real circle.
        point_a += self.point
        point_b += self.point

        return point_a, point_b

    def plot_2d(self, ax, **kwargs):

        circle = plt.Circle(self.point, self.radius, **kwargs)

        ax.add_artist(circle)
