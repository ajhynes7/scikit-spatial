
==============
scikit-spatial 
==============

Spatial objects and computations in 3D
======================================


.. image:: https://img.shields.io/pypi/v/scikit-spatial.svg
         :target: https://pypi.python.org/pypi/scikit-spatial

.. image:: https://img.shields.io/travis/ajhynes7/scikit-spatial.svg
         :target: https://travis-ci.org/ajhynes7/scikit-spatial

.. image:: https://readthedocs.org/projects/scikit-spatial/badge/?version=latest
         :target: https://scikit-spatial.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ajhynes7/scikit-spatial/shield.svg
         :target: https://pyup.io/account/repos/github/ajhynes7/scikit-spatial/

.. image:: https://codecov.io/gh/ajhynes7/scikit-spatial/branch/master/graph/badge.svg
         :target: https://codecov.io/gh/ajhynes7/scikit-spatial



Introduction
------------

This package provides spatial objects in 3D (`Point`, `Vector`, `Line`, and `Plane`) based on NumPy arrays, as well as computations using these objects.

`Point` and `Vector` are subclasses of the NumPy `ndarray`, allowing them to be easily integrated with the `SciPy ecosystem <https://www.scipy.org/about.html>`_. The `Line` and `Plane` objects have `Point` and `Vector` objects as attributes.

The computations can be grouped into the following main categories:

   - Measurement
      - e.g.: Measure the angle between two vectors.
   - Comparison
      - e.g.: Check if two vectors are perpendicular.      
   - Projection
      - e.g.: Project a point onto a line.
   - Intersection
      - e.g.: Find the intersection of a line and a plane.


The package has been built using `contracts <https://github.com/deadpixi/contracts>`_ and is tested with `hypothesis <https://github.com/HypothesisWorks/hypothesis>`_ (see this `PyCon talk <https://www.youtube.com/watch?v=MYucYon2-lk>`_ for a good introduction to both libraries). The contracts prevent spatial computations that are undefined in Euclidean space, such as finding the intersection of two parallel lines.  



Installation
------------

The package can be installed via pip.

.. code-block:: bash

   $ pip install scikit-spatial



Example Usage
-------------

Measure the angle between two vectors.

>>> import numpy as np
>>> from skspatial.objects import Vector

>>> vector = Vector([1, 0])
>>> angle = vector.angle_between([1, 1])

>>> np.degrees(angle).round()
45.0


Project a point onto a line.

>>> from skspatial.objects import Line

>>> line = Line(point=[0, 0, 0], direction=[1, 1, 0])

>>> line.project_point([5, 6, 7])
Point([5.5, 5.5, 0. ])


An error is returned if the computation is undefined.

>>> line_a = Line([0, 0], [1, 0])
>>> line_b = Line([1, 0], [1, 0])

>>> line_a.intersect_line(line_b)
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The lines must not be parallel.


Acknowledgment
--------------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
