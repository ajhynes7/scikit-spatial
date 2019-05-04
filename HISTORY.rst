=======
History
=======

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
