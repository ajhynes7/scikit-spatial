=======
History
=======

0.1.0 (2019-02-27)
------------------

* First release on PyPI.


1.0.0 (2019-03-26)
------------------

* Vector and Point classes are now subclasses of the NumPy `ndarray`.
* All spatial objects accept `array_like` inputs, such as a list or tuple.
* The dimension of the objects is no longer automatically set to 3D. Points and vectors can be 2D and up.
* Added Points class to represent multiple points in space. This is also an `ndarray` subclass.
