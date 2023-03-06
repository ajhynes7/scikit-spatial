"""
Sphere-plane Intersection
========================

"""
from skspatial.objects import Plane, Sphere, Circle3D
from skspatial.plotting import plot_3d

sphere = Sphere([3, 2, 1], 4)
plane = Plane([0, 0, 0], [1, 0, 1])

circle3D = sphere.intersect_plane(plane)

plot_3d(
    plane.plotter(alpha=0.2),
    sphere.plotter(alpha=0.2),
    circle3D.plotter(),
)

