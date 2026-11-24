from math import gcd
from types import NotImplementedType


class Fraction:
    """Represent a simplified fraction with a positive denominator."""

    def __init__(self, numerator: int, denominator: int) -> None:
        """Initialise a fraction using integers and a positive denominator."""
        # Reject booleans, which Python otherwise treats as integers.
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("Numerator and denominator must be integers.")

        if denominator <= 0:
            raise ValueError("Denominator must be strictly positive.")

        # Simplify while preserving integer values.
        divisor = gcd(numerator, denominator)
        self._numerator = numerator // divisor
        self._denominator = denominator // divisor

    @property
    def numerator(self) -> int:
        """Return the simplified numerator as a read-only property."""
        return self._numerator

    @property
    def denominator(self) -> int:
        """Return the simplified denominator as a read-only property."""
        return self._denominator

    def __str__(self) -> str:
        """Return a readable fraction."""
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        """Return a representation showing how to recreate the fraction."""
        return f"Fraction({self.numerator}, {self.denominator})"

    def __add__(self, other: object) -> "Fraction | NotImplementedType":
        """Return the sum of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented

        numerator = (
            self.numerator * other.denominator
            + other.numerator * self.denominator
        )
        denominator = self.denominator * other.denominator

        return Fraction(numerator, denominator)

    def __sub__(self, other: object) -> "Fraction | NotImplementedType":
        """Return the difference between two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented

        numerator = (
            self.numerator * other.denominator
            - other.numerator * self.denominator
        )
        denominator = self.denominator * other.denominator

        return Fraction(numerator, denominator)

    def __mul__(self, other: object) -> "Fraction | NotImplementedType":
        """Return the product of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented

        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator

        return Fraction(numerator, denominator)

    def __truediv__(self, other: object) -> "Fraction | NotImplementedType":
        """Return the quotient of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented

        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by a zero fraction.")

        # Divide by multiplying by the other fraction's reciprocal.
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator

        # A negative divisor can produce a negative denominator.
        # Move the sign to the numerator before creating the result.
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        return Fraction(numerator, denominator)

    def __eq__(self, other: object) -> bool | NotImplementedType:
        """Check whether two simplified fractions are equal."""
        if not isinstance(other, Fraction):
            return NotImplemented

        return (
            self.numerator == other.numerator
            and self.denominator == other.denominator
        )

    def __ne__(self, other: object) -> bool | NotImplementedType:
        """Check whether two fractions are unequal."""
        if not isinstance(other, Fraction):
            return NotImplemented

        return not self == other

    def __lt__(self, other: object) -> bool | NotImplementedType:
        """Check whether this fraction is smaller."""
        if not isinstance(other, Fraction):
            return NotImplemented

        # Cross multiplication avoids floating-point rounding errors.
        return (
            self.numerator * other.denominator
            < other.numerator * self.denominator
        )

    def __le__(self, other: object) -> bool | NotImplementedType:
        """Check whether this fraction is smaller or equal."""
        if not isinstance(other, Fraction):
            return NotImplemented

        return (
            self.numerator * other.denominator
            <= other.numerator * self.denominator
        )

    def __gt__(self, other: object) -> bool | NotImplementedType:
        """Check whether this fraction is greater."""
        if not isinstance(other, Fraction):
            return NotImplemented

        return (
            self.numerator * other.denominator
            > other.numerator * self.denominator
        )

    def __ge__(self, other: object) -> bool | NotImplementedType:
        """Check whether this fraction is greater or equal."""
        if not isinstance(other, Fraction):
            return NotImplemented

        return (
            self.numerator * other.denominator
            >= other.numerator * self.denominator
        )


# Run these examples only when the file is executed directly.
if __name__ == "__main__":
    first = Fraction(1, 2)
    second = Fraction(1, 3)

    print("First:", first)
    print("Second:", second)
    print("Sum:", first + second)
    print("Difference:", first - second)
    print("Product:", first * second)
    print("Quotient:", first / second)
    print("Equal:", first == second)
    print("Greater:", first > second)
    print("Representation:", repr(first))
    