"""Mixin classes."""
from typing import Callable
from typing import Tuple

import numpy as np

from skspatial._functions import _mesh_to_points
from skspatial.objects.points import Points


class _ToPointsMixin:

    to_mesh: Callable[..., Tuple[np.ndarray, np.ndarray, np.ndarray]]

    def to_points(self, **kwargs) -> Points:
        """
        Return points on the surface of the object.

        Parameters
        ----------
        kwargs: dict, optional
            Additional keywords passed to the `to_mesh` method of the class.

        Returns
        -------
        Points
            Points on the surface of the object.

        Examples
        --------
        >>> from skspatial.objects import Sphere

        >>> sphere = Sphere([0, 0, 0], 1)

        >>> sphere.to_points(n_angles=3).round().unique()
        Points([[ 0., -1.,  0.],
                [ 0.,  0., -1.],
                [ 0.,  0.,  1.],
                [ 0.,  1.,  0.]])

        >>> sphere.to_points(n_angles=4).round(3).unique()
        Points([[-0.75 , -0.433, -0.5  ],
                [-0.75 , -0.433,  0.5  ],
                [ 0.   ,  0.   , -1.   ],
                [ 0.   ,  0.   ,  1.   ],
                [ 0.   ,  0.866, -0.5  ],
                [ 0.   ,  0.866,  0.5  ],
                [ 0.75 , -0.433, -0.5  ],
                [ 0.75 , -0.433,  0.5  ]])

        """
        X, Y, Z = self.to_mesh(**kwargs)
        points = _mesh_to_points(X, Y, Z)

        return Points(points)
