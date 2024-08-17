"""Module for the Elipse class."""
import future_annotations as annotations

import math
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from skspatial._functions import np_float
from skspatial.objects._base_sphere import _BaseSpatial
from skspatial.objects.circle3D import Circle3D
from skspatial.objects.line import Line
from skspatial.objects.plane import Plane
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Elipse3D(_BaseSpatial):

    def __init__(self, point: Point, ab: array_like, plane: Plane):
        self.a = ab[0]
        self.b = ab[1]
        self.plane = plane
        self.point = point

        if self.point.dimension != 3:
            raise ValueError("The point must be 3D.")

        if not self.a > 0:
            raise ValueError("Major axis length 'a' must be positive.")

        if not self.b > 0:
            raise ValueError("Minor axis length 'b' must be positive.")

        self.dimension = self.point.dimension

    def __repr__(self) -> str:
        return f"Cylinder(point={self.point}, plane={self.plane}, major,minor axis length={self.a, self.b})"


    def intersect_circle(self, circle: Circle3D):
        """Find the intersection between a circle and a elipse on a 2D plane"""
        # TODO Check if same plane


        def rotX(phi):
                rotx = np.array([
                    [1,     0    ,    0    ],
                    [0,  np.cos(phi), -np.sin(phi)],
                    [0,  np.sin(phi), np.cos(phi)] ])
                return rotx

        def rotY(theta):    
            roty = np.array([
                [np.cos(theta), 0, np.sin(theta) ],
                [0         , 1,     0       ],
                [-np.sin(theta), 0,  np.cos(theta) ] ])   
            return roty
            
        def rotZ(psi):    
            rotz = np.array([
                [ np.cos(psi), -np.sin(psi), 0 ],
                [np.sin(psi), np.cos(psi), 0 ],
                [   0        ,     0      , 1 ] ])   
            return rotz


        r = circle.radius
        x0 = np.linalg.norm(circle.point)
        a = self.a
        b = self.b
        c = 1-(b/a)**2

        A = 1
        B = -2*x0/c
        C = -(r**2-b**2-x0**2)/c
        X1 = (-B + np.sqrt(B**2 - 4*A*C))/(2*A)
        X2 = (-B - np.sqrt(B**2 - 4*A*C))/(2*A)
        Y1 = np.sqrt(r**2-(X1-x0)**2)
        Y2 = np.sqrt(r**2-(X2-x0)**2)

        print(f"r={r}, x0={x0}, a={a}, b={b}, X1={X1}, X2={X2}, Y1={Y1}, Y2={Y2}")
        P1 = np.array([X2, Y2, 0])
        P2 = np.array([X2,-Y2, 0])

        # x1 = -(+np.sqrt((r**2-b**2-x0**2)/c + (x0/c)**2) + x0/c)
        # x2 = -(-np.sqrt((r**2-b**2-x0**2)/c + (x0/c)**2) + x0/c)
        # y1 = np.sqrt(r**2-(x1-x0)**2)
        # y2 = np.sqrt(r**2-(x2-x0)**2)
        # print(f"x1={x1}, x2={x2}, y1={y1}, y2={y2}")
        # P1 = np.array([x2, y2, 0])
        # P2 = np.array([x2,-y2, 0])

        # x = np.max(np.array([x1, x2]))
        # print(f"x={x}, x1={x1}, x2={x2}")
        # y = np.sqrt(r**2-(x-x0)**2)
        # P1 = np.array([x, y, 0])
        # P2 = np.array([x,-y, 0])


        angle = self.plane.normal.angle_between(Vector([0, 0, 1]))
        P1 = np.matmul(rotY(angle), P1)
        P2 = np.matmul(rotY(angle), P2)
        P1 = self.point + Point(P1)
        P2 = self.point + Point(P2)
        return P1, P2

        # print(angle)
