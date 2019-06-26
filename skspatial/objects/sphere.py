"""Module for the Sphere class."""

import numpy as np

from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects.vector import Vector


class Sphere(_BaseSphere):

    def __init__(self, point, radius):

        super().__init__(point, radius)

    def surface_area(self):

        return 4 * np.pi * self.radius ** 2

    def volume(self):

        return 4 / 3 * np.pi * self.radius ** 3

    def intersect_line(self, line):

        vector_to_line = Vector.from_points(self.point, line.point)
        vector_unit = line.direction.unit()

        dot = vector_unit.dot(vector_to_line)

        discriminant = dot ** 2 - (vector_to_line.norm() ** 2 - self.radius ** 2)

        if discriminant < 0:
            raise ValueError("The line does not intersect the sphere.")

        pm = np.array([-1, 1])  # Array to compute plus/minus.
        distances = - dot + pm * np.sqrt(discriminant)

        point_a, point_b = line.point + distances.reshape(-1, 1) * vector_unit

        return point_a, point_b

    def plot_3d(self, ax, **kwargs):

        angles_a = np.linspace(0, np.pi, 30)
        angles_b = np.linspace(0, 2 * np.pi, 30)

        X = np.outer(np.sin(angles_a), np.sin(angles_b))
        Y = np.outer(np.sin(angles_a), np.cos(angles_b))
        Z = np.outer(np.cos(angles_a), np.ones_like(angles_b))

        ax.plot_surface(X, Y, Z, **kwargs)
