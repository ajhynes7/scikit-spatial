

.. figure:: images/logo.svg
         :align: left
         :width: 70%


Introduction
~~~~~~~~~~~~

``scikit-spatial`` is a Python library that provides spatial objects and computations between them. The basic objects -- points and vectors -- are subclasses of the NumPy :class:`~numpy.ndarray`. Other objects such as lines, planes, and circles have points and/or vectors as attributes. 


Computations can be performed after instantiating a spatial object. For example, a point can be projected onto a plane.

>>> from skspatial.objects import Plane

>>> plane = Plane(point=[0, 0, 0], normal=[1, 1, 1])

>>> plane.project_point([0, 5, 10])
Point([-5.,  0.,  5.])


Most of the computations fall into the following categories:

- Measurement
- Comparison
- Projection
- Intersection
- Fitting
- Transformation

The spatial objects can also be visualized on 2D or 3D plots using `matplotlib <https://matplotlib.org/>`_. See :ref:`plotting` for a brief introduction and the :ref:`sphx_glr_gallery` for full examples with code.

The library has four main objectives:

1. Provide an intuitive, object-oriented API for spatial computations.
2. Provide efficient computations by leveraging NumPy functionality whenever possible.
3. Integrate seamlessly with other libraries in the `scientific Python ecosystem <https://www.scipy.org/about.html>`_.
4. Facilitate the visualization of spatial objects in 2D or 3D space.


Installation
~~~~~~~~~~~~

The package can be installed via pip.

.. code-block:: bash

   $ pip install scikit-spatial



Contents
~~~~~~~~

.. toctree::
   :maxdepth: 1

   objects/toc
   computations/toc
   plotting
   gallery/index
   api_reference/toc
