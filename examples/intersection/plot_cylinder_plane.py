
from skspatial.objects import Elipse3D, Point, Vector, Plane
from skspatial.plotting import plot_3d

elipse = Elipse3D(Point(0,0,0), 2, 1, Plane(Point(0,0,0), Vector(0,0,1)))
plot_3d(
    elipse.plotter(fill=False),
)