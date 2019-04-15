
Transformation
==============

Mean-Center Points
------------------

Mean-center a set of points.


The centroid of the points is treated as the origin of the new coordinate system.

>>> from skspatial.objects import Points

>>> points = Points([[6, 3], [7, 8], [5, -2]])
>>> points_centered, centroid = points.mean_center()

>>> points_centered
Points([[ 0.,  0.],
        [ 1.,  5.],
        [-1., -5.]])


The original centroid is returned as well.

>>> centroid 
Point([6., 3.])


The centroid of the centered points is the origin.

>>> points_centered.centroid()
Point([0., 0.])


Points to Line Coordinates
--------------------------

Transform points in space to coordinates along a line.

This is analogous is projecting the points onto the line, then computing the signed distance from the line point to the projections.


>>> from skspatial.objects import Line

>>> points = [[-1, 1], [0, 1], [1, 1], [2, 1]]

>>> Line([0, 0], [1, 0]).transform_points(points)
array([-1.,  0.,  1.,  2.])


The point on the line acts as the origin of the coordinates.

>>> Line([1, 0], [1, 0]).transform_points(points)
array([-2., -1.,  0.,  1.])


The sign of the coordinates depends on the direction of the line.

>>> Line([0, 0], [-1, 0]).transform_points(points)
array([ 1.,  0., -1., -2.])


The magnitude of the direction vector is irrelevant.

>>> Line([0, 0], [5, 0]).transform_points(points)
array([-1.,  0.,  1.,  2.])
