import pytest

from temperature import Temperature


def test_default_unit() -> None:
    """Check that Celsius is the default unit."""
    temperature = Temperature(25)

    assert temperature.value == 25.0
    assert temperature.unit == "C"


@pytest.mark.parametrize("unit", ["c", "f", "k", "C", "F", "K"])
def test_case_insensitive_units(unit: str) -> None:
    """Check that uppercase and lowercase units are accepted."""
    temperature = Temperature(25, unit)

    assert temperature.unit == unit.upper()


def test_read_only_properties() -> None:
    """Check that public properties cannot be reassigned."""
    temperature = Temperature(25, "C")

    # Properties without setters must reject assignment.
    with pytest.raises(AttributeError):
        temperature.value = 30

    with pytest.raises(AttributeError):
        temperature.unit = "F"


@pytest.mark.parametrize("unit", ["X", "", "Celsius"])
def test_invalid_unit(unit: str) -> None:
    """Check that unsupported units raise ValueError."""
    with pytest.raises(ValueError):
        Temperature(25, unit)


@pytest.mark.parametrize(
    "value, unit",
    [
        (-274, "C"),
        (-460, "F"),
        (-1, "K"),
    ],
)
def test_below_absolute_zero(value: float, unit: str) -> None:
    """Check that temperatures below absolute zero are rejected."""
    with pytest.raises(ValueError):
        Temperature(value, unit)


@pytest.mark.parametrize(
    "celsius, fahrenheit, kelvin",
    [
        (-273.15, -459.67, 0.0),  # Absolute zero.
        (-40.0, -40.0, 233.15),   # Celsius–Fahrenheit crossover.
        (0.0, 32.0, 273.15),     # Freezing point of water.
        (37.0, 98.6, 310.15),     # Human body temperature.
        (100.0, 212.0, 373.15),   # Boiling point of water.
    ],
)
@pytest.mark.parametrize("unit", ["C", "F", "K"])
def test_conversions(
    celsius: float,
    fahrenheit: float,
    kelvin: float,
    unit: str,
) -> None:
    """Check every conversion method from each starting unit."""
    reference_values = {
        "C": celsius,
        "F": fahrenheit,
        "K": kelvin,
    }
    temperature = Temperature(reference_values[unit], unit)

    # Allow small floating-point errors using an absolute tolerance.
    assert temperature.to_celsius() == pytest.approx(
        celsius, abs=1e-9, rel=0
    )
    assert temperature.to_fahrenheit() == pytest.approx(
        fahrenheit, abs=1e-9, rel=0
    )
    assert temperature.to_kelvin() == pytest.approx(
        kelvin, abs=1e-9, rel=0
    )


@pytest.mark.parametrize(
    "target_unit, expected_value",
    [
        ("C", 25.0),
        ("c", 25.0),
        ("F", 77.0),
        ("f", 77.0),
        ("K", 298.15),
        ("k", 298.15),
    ],
)
def test_convert_to(target_unit: str, expected_value: float) -> None:
    """Check that conversion returns a new object in the requested unit."""
    original = Temperature(25, "C")

    converted = original.convert_to(target_unit)

    assert isinstance(converted, Temperature)
    assert converted.unit == target_unit.upper()
    assert converted.value == pytest.approx(
        expected_value, abs=1e-9, rel=0
    )

    # Even conversion to the same unit must create a separate object.
    assert converted is not original

    # Conversion must preserve the original object's value and unit.
    assert original.value == 25.0
    assert original.unit == "C"


@pytest.mark.parametrize("target_unit", ["X", "", "Celsius"])
def test_convert_to_invalid_unit(target_unit: str) -> None:
    """Check that conversion to an unsupported unit raises ValueError."""
    temperature = Temperature(25, "C")

    with pytest.raises(ValueError):
        temperature.convert_to(target_unit)
        