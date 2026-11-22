class Temperature:
    """Represent a temperature in Celsius, Fahrenheit, or Kelvin."""

    def __init__(self, value, unit="C"):
        unit = unit.upper()

        if unit not in ("C", "F", "K"):
            raise ValueError("Unit must be C, F, or K.")

        value = float(value)

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
    def value(self):
        """Return the temperature value."""
        return self._value

    @property
    def unit(self):
        """Return the temperature unit."""
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


# Example usage
if __name__ == "__main__":
    temperature = Temperature(25, "c")
    print(temperature.value)
    print(temperature.unit)
    print("Fahrenheit:", temperature.to_fahrenheit())
    print("Celsius:", temperature.to_celsius())
    print("Kelvin:", temperature.to_kelvin())
