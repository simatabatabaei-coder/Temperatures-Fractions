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

    # Assigning to a property without a setter must raise AttributeError.
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