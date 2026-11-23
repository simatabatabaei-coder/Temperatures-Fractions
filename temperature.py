import math
from types import NotImplementedType


class Temperature:
    """Represent a temperature in Celsius, Fahrenheit, or Kelvin."""

    TOLERANCE: float = 1e-9

    def __init__(self, value: float, unit: str = "C") -> None:
        """Initialise a temperature, rejecting invalid units and values."""
        unit = unit.upper()

        if unit not in ("C", "F", "K"):
            raise ValueError("Unit must be C, F, or K.")

        value = float(value)

        if not math.isfinite(value):
            raise ValueError("Temperature must be a finite number.")

        absolute_zero = {
            "C": -273.15,
            "F": -459.67,
            "K": 0.0,
        }

        if value < absolute_zero[unit]:
            raise ValueError("Temperature cannot be below absolute zero.")

        self._value = value
        self._unit = unit

    @property
    def value(self) -> float:
        """Return the temperature value as a read-only property."""
        return self._value

    @property
    def unit(self) -> str:
        """Return the temperature unit as a read-only property."""
        return self._unit

    def to_celsius(self) -> float:
        """Return the temperature in Celsius."""
        if self.unit == "C":
            return self.value
        elif self.unit == "F":
            return (self.value - 32) * 5 / 9
        else:
            return self.value - 273.15

    def to_fahrenheit(self) -> float:
        """Return the temperature in Fahrenheit."""
        if self.unit == "F":
            return self.value
        elif self.unit == "C":
            return self.value * 9 / 5 + 32
        else:
            return (self.value - 273.15) * 9 / 5 + 32

    def to_kelvin(self) -> float:
        """Return the temperature in Kelvin."""
        if self.unit == "K":
            return self.value
        elif self.unit == "C":
            return self.value + 273.15
        else:
            return (self.value - 32) * 5 / 9 + 273.15

    def convert_to(self, target_unit: str) -> "Temperature":
        """Return a new Temperature object in the requested unit."""
        target_unit = target_unit.upper()

        if target_unit == "C":
            value = self.to_celsius()
        elif target_unit == "F":
            value = self.to_fahrenheit()
        elif target_unit == "K":
            value = self.to_kelvin()
        else:
            raise ValueError("Unit must be C, F, or K.")

        # Correct tiny conversion errors at the absolute-zero boundary.
        minimum = {"C": -273.15, "F": -459.67, "K": 0.0}[target_unit]
        if value < minimum and math.isclose(
            value, minimum, abs_tol=self.TOLERANCE, rel_tol=0
        ):
            value = minimum

        return Temperature(value, target_unit)

    def __str__(self) -> str:
        """Return a readable temperature with two decimal places."""
        symbol = "K" if self.unit == "K" else f"°{self.unit}"
        return f"{self.value:.2f} {symbol}"

    def __repr__(self) -> str:
        """Return a representation showing the stored value and unit."""
        return f"Temperature({self.value!r}, {self.unit!r})"

    def __eq__(self, other: object) -> bool | NotImplementedType:
        """Check equality across units using an absolute tolerance."""
        if not isinstance(other, Temperature):
            return NotImplemented

        # Compare in Kelvin so both objects use the same scale.
        return math.isclose(
            self.to_kelvin(),
            other.to_kelvin(),
            abs_tol=self.TOLERANCE,
            rel_tol=0,
        )

    def __ne__(self, other: object) -> bool | NotImplementedType:
        """Check whether two temperatures differ beyond the tolerance."""
        if not isinstance(other, Temperature):
            return NotImplemented

        return not self == other

    def __lt__(self, other: object) -> bool | NotImplementedType:
        """Check whether this temperature is strictly lower."""
        if not isinstance(other, Temperature):
            return NotImplemented

        # Temperatures equal within tolerance are not strictly ordered.
        return self.to_kelvin() < other.to_kelvin() and self != other

    def __le__(self, other: object) -> bool | NotImplementedType:
        """Check whether this temperature is lower or approximately equal."""
        if not isinstance(other, Temperature):
            return NotImplemented

        return self < other or self == other

    def __gt__(self, other: object) -> bool | NotImplementedType:
        """Check whether this temperature is strictly higher."""
        if not isinstance(other, Temperature):
            return NotImplemented

        return self.to_kelvin() > other.to_kelvin() and self != other

    def __ge__(self, other: object) -> bool | NotImplementedType:
        """Check whether this temperature is higher or approximately equal."""
        if not isinstance(other, Temperature):
            return NotImplemented

        return self > other or self == other


# Run these examples only when the file is executed directly.
if __name__ == "__main__":
    temperature = Temperature(25, "c")

    print("Fahrenheit:", temperature.to_fahrenheit())
    print("Celsius:", temperature.to_celsius())
    print("Kelvin:", temperature.to_kelvin())

    print("Converted:", temperature.convert_to("F"))
    print("Readable:", str(temperature))
    print("Representation:", repr(temperature))

    print("Equal:", Temperature(0, "C") == Temperature(32, "F"))
    print("Lower:", Temperature(0, "C") < Temperature(300, "K"))

    # Convert through all three units and back to Celsius.
    round_trip = temperature.convert_to("F").convert_to("K").convert_to("C")
    print("Round trip:", round_trip)
    print("Matches original:", round_trip == temperature)
    