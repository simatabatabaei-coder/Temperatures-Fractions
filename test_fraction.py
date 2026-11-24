import operator

import pytest

from fraction import Fraction


@pytest.mark.parametrize(
    "numerator, denominator, expected_numerator, expected_denominator",
    [
        (1, 2, 1, 2),
        (2, 4, 1, 2),
        (-6, 8, -3, 4),
        (0, 5, 0, 1),
        (8, 4, 2, 1),
        (7, 3, 7, 3),
    ],
)
def test_initialization(
    numerator: int,
    denominator: int,
    expected_numerator: int,
    expected_denominator: int,
) -> None:
    """Check that fractions are stored in simplified form."""
    fraction = Fraction(numerator, denominator)

    assert fraction.numerator == expected_numerator
    assert fraction.denominator == expected_denominator


@pytest.mark.parametrize("denominator", [0, -1, -5])
def test_invalid_denominator(denominator: int) -> None:
    """Check that zero and negative denominators are rejected."""
    with pytest.raises(ValueError):
        Fraction(1, denominator)


@pytest.mark.parametrize(
    "numerator, denominator",
    [
        (1.5, 2),
        (1, 2.5),
        ("1", 2),
        (1, "2"),
        (True, 2),
        (1, False),
        (None, 2),
        (1, None),
    ],
)
def test_non_integer_inputs(numerator: object, denominator: object) -> None:
    """Check that both inputs must be integers."""
    with pytest.raises(TypeError):
        Fraction(numerator, denominator)


def test_read_only_properties() -> None:
    """Check that public properties cannot be reassigned."""
    fraction = Fraction(1, 2)

    with pytest.raises(AttributeError):
        fraction.numerator = 3

    with pytest.raises(AttributeError):
        fraction.denominator = 0


@pytest.mark.parametrize(
    "operation, first_pair, second_pair, expected_pair",
    [
        (operator.add, (1, 2), (1, 3), (5, 6)),
        (operator.add, (-1, 2), (1, 2), (0, 1)),
        (operator.add, (0, 1), (2, 3), (2, 3)),
        (operator.sub, (1, 2), (1, 3), (1, 6)),
        (operator.sub, (1, 3), (1, 2), (-1, 6)),
        (operator.sub, (2, 3), (2, 3), (0, 1)),
        (operator.mul, (1, 2), (1, 3), (1, 6)),
        (operator.mul, (-2, 3), (3, 4), (-1, 2)),
        (operator.mul, (0, 1), (3, 4), (0, 1)),
        (operator.truediv, (1, 2), (1, 3), (3, 2)),
        (operator.truediv, (1, 2), (-1, 3), (-3, 2)),
        (operator.truediv, (-1, 2), (-1, 3), (3, 2)),
        (operator.truediv, (0, 1), (1, 3), (0, 1)),
    ],
)
def test_arithmetic(
    operation,
    first_pair: tuple[int, int],
    second_pair: tuple[int, int],
    expected_pair: tuple[int, int],
) -> None:
    """Check arithmetic results, simplification, and unchanged operands."""
    first = Fraction(*first_pair)
    second = Fraction(*second_pair)
    first_before = (first.numerator, first.denominator)
    second_before = (second.numerator, second.denominator)

    # operator.add(a, b), for example, performs a + b.
    result = operation(first, second)

    assert isinstance(result, Fraction)
    assert (result.numerator, result.denominator) == expected_pair
    assert result.denominator > 0

    # Arithmetic must return a separate object and preserve both operands.
    assert result is not first
    assert result is not second
    assert (first.numerator, first.denominator) == first_before
    assert (second.numerator, second.denominator) == second_before


def test_division_by_zero() -> None:
    """Check that dividing by a zero fraction raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0, 5)


@pytest.mark.parametrize(
    "first_pair, second_pair",
    [
        ((1, 2), (2, 4)),
        ((-1, 2), (-3, 6)),
        ((0, 3), (0, 7)),
    ],
)
def test_equal_comparisons(
    first_pair: tuple[int, int],
    second_pair: tuple[int, int],
) -> None:
    """Check all comparisons for equivalent fractions."""
    first = Fraction(*first_pair)
    second = Fraction(*second_pair)

    assert first == second
    assert not (first != second)
    assert first <= second
    assert first >= second
    assert not (first < second)
    assert not (first > second)


@pytest.mark.parametrize(
    "lower_pair, higher_pair",
    [
        ((1, 3), (1, 2)),
        ((-3, 4), (-1, 2)),
        ((-1, 2), (0, 1)),
        ((0, 1), (1, 2)),
        ((3, 2), (7, 4)),
        # These differ too little for reliable float-based comparison.
        ((10**20, 1), (10**20 + 1, 1)),
    ],
)
def test_ordering(
    lower_pair: tuple[int, int],
    higher_pair: tuple[int, int],
) -> None:
    """Check exact ordering for positive, negative, and large fractions."""
    lower = Fraction(*lower_pair)
    higher = Fraction(*higher_pair)

    assert lower < higher
    assert lower <= higher
    assert higher > lower
    assert higher >= lower
    assert lower != higher
    assert not (lower == higher)

    assert not (higher < lower)
    assert not (higher <= lower)
    assert not (lower > higher)
    assert not (lower >= higher)


@pytest.mark.parametrize(
    "method_name",
    [
        "__add__",
        "__sub__",
        "__mul__",
        "__truediv__",
        "__eq__",
        "__ne__",
        "__lt__",
        "__le__",
        "__gt__",
        "__ge__",
    ],
)
def test_unsupported_type(method_name: str) -> None:
    """Check that methods return NotImplemented for unsupported operands."""
    fraction = Fraction(1, 2)

    # Direct calls let us inspect the special methods' return values.
    method = getattr(fraction, method_name)
    assert method(2) is NotImplemented


@pytest.mark.parametrize(
    "operation",
    [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv,
        operator.lt,
        operator.le,
        operator.gt,
        operator.ge,
    ],
)
def test_unsupported_operator(operation) -> None:
    """Check that unsupported arithmetic and ordering raise TypeError."""
    with pytest.raises(TypeError):
        operation(Fraction(1, 2), 2)


@pytest.mark.parametrize(
    "numerator, denominator, expected",
    [
        (2, 4, "1/2"),
        (-6, 8, "-3/4"),
        (0, 5, "0/1"),
        (8, 4, "2/1"),
    ],
)
def test_str(numerator: int, denominator: int, expected: str) -> None:
    """Check readable formatting of simplified fractions."""
    assert str(Fraction(numerator, denominator)) == expected


@pytest.mark.parametrize(
    "numerator, denominator, expected",
    [
        (2, 4, "Fraction(1, 2)"),
        (-6, 8, "Fraction(-3, 4)"),
        (0, 5, "Fraction(0, 1)"),
    ],
)
def test_repr(numerator: int, denominator: int, expected: str) -> None:
    """Check the representation of simplified fractions."""
    assert repr(Fraction(numerator, denominator)) == expected
    