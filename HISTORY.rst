=======
History
=======


5.0.0 (2020-11-23)
------------------
* Return regular ``ndarray`` from inherited NumPy functions, e.g. ``vector.sum()``
  - This prevents getting spatial objects with disallowed dimensions, such as a 0-D vector.
  - This fixes broken examples in the README.
* Test README examples with doctest.
* Replace tox with Docker.
  - Docker multi-stage builds are a convenient feature for isolating test environments.
* Organize requirements into multiple files.
  - This makes it easy to install only what's needed for each test environment.


4.0.1 (2020-02-01)
------------------
* Fix to replace Python 3.6 with 3.8 in the setup.py file.


4.0.0 (2020-02-01)
------------------
* Drop support for Python 3.6 (this allows for postponed evaluation of type annotations, introduced in Python 3.7).
* Add Triangle class.


3.0.0 (2019-11-02)
------------------
* Add `Points.normalize_distance` method to fit points inside a unit sphere.
* Change `Points.mean_center` to only return the centroid of the points if specified. 
  This allows for chaining with other transformations on points, like `normalize_distance`.
* Add `to_array` method to convert an array based object to a regular NumPy array.


2.0.1 (2019-08-15)
------------------
* Use installation of numpy-stubs from its GitHub repository instead of a custom numpy stubs folder.
* Introduce 'array_like' type annotation as the union of np.ndarray and Sequence.
* Add py.typed file so that annotations can be used when scikit-spatial is installed.


2.0.0 (2019-07-20)
------------------
* Replace some NumPy functions with ones from Python math module. The math functions are faster than NumPy when the inputs are scalars.
  The tolerances for isclose are now rel_tol and abs_tol instead of rtol and atol. 
  The math.isclose function is preferable to np.isclose for three main reasons:
   - It is symmetric (isclose(a, b) == isclose(b, a)).
   - It has a default absolute tolerance of zero.
   - It does not correlate the absolute and relative tolerances.
* Add type annotations to methods and run mypy in Travis CI.
* Add round method to array objects (Point, Points and Vector). Now a Vector is returned when a Vector is rounded.
* Add methods to return coordinates on the surface of a Plane or Sphere. The coordinates are used for 3D plotting.
* Improve Plane plotting so that vertical planes can be plotted.


1.5.0 (2019-07-04)
------------------
* Add Circle and Sphere spatial objects.
* Add scalar keyword argument to Vector plot methods.
* Improve plotting of Plane. The x and y limits now treat the plane point as the origin.


1.4.2 (2019-06-21)
------------------
* Extra release because regex for version tags was incorrect in Travis.


1.4.1 (2019-06-21)
------------------
* Extra release because Travis did not deploy the last one.


1.4.0 (2019-06-21)
------------------
* Add functions `plot_2d` and `plot_3d` to facilitate plotting multiple spatial objects.
* Change `_plotting` module name to `plotting`, because it now contains some public functions.


1.3.0 (2019-06-19)
------------------
* Remove dpcontracts as a dependency. The contracts were causing performance issues.
* Add 'dimension' attribute to all spatial objects.
* Add Vector.angle_signed method.
* Add Line.from_slope method.


1.2.0 (2019-06-11)
------------------
* Move tests into skspatial directory. This allows for importing custom hypothesis strategies for testing other projects.
* Drop support for Python 3.5 (matplotlib requires >= 3.6).


1.1.0 (2019-05-04)
------------------
* Add methods for 2D and 3D plotting. 
* Rename private modules and functions to include leading underscore.


1.0.1 (2019-03-29)
------------------
* Support Python versions 3.5-3.7. 


1.0.0 (2019-03-26)
------------------
* Change Vector and Point to be subclasses of the NumPy `ndarray`.
* Change all spatial objects to accept `array_like` inputs, such as a list or tuple.
* Add the Points class to represent multiple points in space. This is also an `ndarray` subclass.
* The dimension of the objects is no longer automatically set to 3D. Points and vectors can be 2D and up.


0.1.0 (2019-02-27)
------------------
* First release on PyPI.
