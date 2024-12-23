=======
History
=======

8.1.0 (2024-12-23)
------------------

Features
~~~~~~~~
- Add optiont to return error for line and plane of best fit.


8.0.0 (2024-10-03)
------------------

Features
~~~~~~~~
- Support NumPy 2.0.


7.2.2 (2024-03-27)
------------------

Fixes
~~~~~
- Change reference in `Plane.best_fit` docstring as the previous link was broken.
- Change `README.rst` to `README.md` as GitHub was not rendering the former well.


7.2.1 (2024-02-17)
------------------

Docs
~~~~
Include new methods in the documentation:
  - `Line.project_points`
  - `Line.distance_points`
  - `Plane.project_points`
  - `Plane.distance_points`


7.2.0 (2024-02-12)
------------------

Features
~~~~~~~~
- Add new methods:
  - `Line.project_points`
  - `Line.distance_points`
  - `Plane.project_points`
  - `Plane.distance_points`


7.1.1 (2024-01-29)
------------------

Fixes
~~~~~
- Restore import of `importlib_metadata`.


7.1.0 (2024-01-28)
------------------

Features
~~~~~~~~
- Add support for Python 3.12.


7.0.0 (2023-03-26)
------------------

Breaking Changes
~~~~~~~~~~~~~~~~
- Drop support for Python 3.7.
- Increase minimum NumPy version to 1.17.3 (to be compatible with the new dependency SciPy).

Features
~~~~~~~~
- Add `Cylinder.best_fit` method.


6.8.1 (2023-03-07)
------------------

Fixes
~~~~~
- Add missing `plotter` method to `LineSegment`.


6.8.0 (2023-01-28)
------------------

Features
~~~~~~~~
- Add `Circle.from_points` method.
- Add `check_coplanar` kwarg to `Line.intersect_line`.
- Lower minimum NumPy version to 1.16.


6.7.0 (2022-12-28)
------------------

Features
~~~~~~~~
- Add `Circle.intersect_circle` method.


6.6.0 (2022-11-20)
------------------

Features
~~~~~~~~
- Add `Vector.angle_signed_3d` method.


6.5.0 (2022-09-05)
------------------

Features
~~~~~~~~
- Add `LineSegment` class.

Docs
~~~~
- Add plot of Cylinder-Line Intersection to the gallery.


6.4.1 (2022-06-21)
------------------

Fixes
~~~~~
- Update the `dimension` value of a slice, instead of using the value of the original array.
- Fix the output radius of `Cylinder.to_mesh`.


6.4.0 (2022-04-07)
------------------

Features
~~~~~~~~
- Add `Plane.project_line` method to project a line onto a plane.


6.3.0 (2022-02-26)
------------------

Features
~~~~~~~~
- Add `Circle.best_fit` method to fit a circle to 2D points.
- Add `area_signed` function to compute the signed area of a polygon using the shoelace algorithm.


6.2.1 (2022-01-08)
------------------

Fixes
~~~~~
- Allow for versions of `importlib-metadata` above 1.


6.2.0 (2021-10-06)
------------------

Features
~~~~~~~~
- Add `infinite` keyword argument to `Cylinder.intersect_line` with a default value of `True`.
  Now the line can be intersected with a finite cylinder by passing `infinite=False`.

Fixes
~~~~~
- Fix the return type hint of `Plane.intersect_line` (from Plane to Point).


6.1.1 (2021-09-11)
------------------

Fixes
~~~~~
- Add code to `skspatial.__init__.py` to keep the __version__ attribute in sync with the version in `pyproject.toml`.


6.1.0 (2021-07-25)
------------------

Features
~~~~~~~~
- Add `lateral_surface_area` and `surface_area` methods to `Cylinder`.

Improvements
~~~~~~~~~~~~
- Remove unnecessary `np.copy` from `Circle.intersect_line`.
- Complete the docstring for `Line.distance_point`.


6.0.1 (2021-03-25)
------------------

Fixes
~~~~~
* Wrap `filterwarnings("error")` in a `catch_warnings` context manager, in `__BaseArray.__new__()`.
  Now the warning level is reset at the end of the context manager.


6.0.0 (2021-03-21)
------------------

Breaking changes
~~~~~~~~~~~~~~~~
* Require NumPy >= 1.20 to make use of the static types introduced in 1.20.
  Now numpy-stubs doesn't need to be installed for static type checking.
* Move tests outside of package, and move package under ``src`` directory.
  This ensures that tox is running the tests with the installed package.
* Switch from ``setup.py`` to ``pyproject.toml``.
* Add more ValueErrors for clarity, such as "The lines must have the same dimension"
  ValueError in ``Line.intersect_line``.

Features
~~~~~~~~
* Add ``Cylinder`` class.
* Add ``Vector.different_direction`` method.
* Add ``Sphere.best_fit`` method.

Refactoring
~~~~~~~~~~~
* Delete ``Vector.dot`` method. The ``dot`` method is already inherited from NumPy.


5.2.0 (2020-12-19)
------------------
* Add keyword arguments to ``Plane.best_fit`` and ``Line.best_fit``.
  These are passed to ``np.linalg.svd``.


5.1.0 (2020-12-07)
------------------
* Edit type annotations to support Python 3.6.
* CI now tests Python versions 3.6-3.9.


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
    * It is symmetric (isclose(a, b) == isclose(b, a)).
    * It has a default absolute tolerance of zero.
    * It does not correlate the absolute and relative tolerances.
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
