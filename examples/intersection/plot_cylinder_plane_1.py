
from skspatial.objects import Elipse3D, Point, Vector, Plane, Circle3D
from skspatial.plotting import plot_3d
import numpy as np

elipse = Elipse3D(Point([0,0,0]), [3,1], Plane(Point([0,0,0]), Vector([0,0,1])))
circle = Circle3D(Point([5,0,0]), 3, Plane(Point([0,0,0]), Vector([0,0,1])))

print(elipse)
print(circle)


print(elipse.intersect_circle(circle))