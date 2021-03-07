from math import isclose
from math import sqrt

import pytest

from skspatial._functions import _solve_quadratic

A_MUST_BE_NON_ZERO = "The coefficient `a` must be non-zero."
DISCRIMINANT_MUST_NOT_BE_NEGATIVE = "The discriminant must not be negative."


@pytest.mark.parametrize(
    ("a", "b", "c", "x1_expected", "x2_expected"),
    [
        (1, 0, 0, 0, 0),
        (-1, 0, 0, 0, 0),
        (-1, 1, 0, 1, 0),
        (1, -1, -1, (1 - sqrt(5)) / 2, (1 + sqrt(5)) / 2),
    ],
)
def test_solve_quadratic(a, b, c, x1_expected, x2_expected):

    x1, x2 = _solve_quadratic(a, b, c)

    assert isclose(x1, x1_expected)
    assert isclose(x2, x2_expected)


@pytest.mark.parametrize(
    ("a", "b", "c", "message_expected"),
    [
        (0, 0, 0, A_MUST_BE_NON_ZERO),
        (0, 1, 1, A_MUST_BE_NON_ZERO),
        (1, 0, 1, DISCRIMINANT_MUST_NOT_BE_NEGATIVE),
        (1, 2, 2, DISCRIMINANT_MUST_NOT_BE_NEGATIVE),
        (1, -2, 2, DISCRIMINANT_MUST_NOT_BE_NEGATIVE),
        (-1, 0, -1, DISCRIMINANT_MUST_NOT_BE_NEGATIVE),
    ],
)
def test_solve_quadratic_failure(a, b, c, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        _solve_quadratic(a, b, c)
