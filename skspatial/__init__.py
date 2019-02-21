"""Initalize scikit-spatial package."""

from .objects.array import Point, Vector
from .objects.line import Line
from .objects.plane import Plane

__all__ = ['Point', 'Vector', 'Line', 'Plane']
