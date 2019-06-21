"""Module for the Sphere class."""

import numpy as np

from skspatial.objects._base_sphere import _BaseSphere


class Sphere(_BaseSphere):

    def __init__(self, point, radius):

        super().__init__(point, radius)

    def surface_area(self):

        return 4 * np.pi * self.radius ** 2

    def volume(self):

        return 4 / 3 * np.pi * self.radius ** 3
