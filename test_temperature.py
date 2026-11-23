import pytest

from temperature import Temperature


# The five reference temperatures specified in the assignment.
REFERENCE_POINTS = [
    (-273.15, -459.67, 0.0),
    (-40.0, -40.0, 233.15),
    (0.0, 32.0, 273.15),
    (37.0, 98.6, 310.15),
    (100.0, 212.0, 373.15),
]


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
    [(-274, "C"), (-460, "F"), (-1, "K")],
)
def test_below_absolute_zero(value: float, unit: str) -> None:
    """Check that temperatures below absolute zero are rejected."""
    with pytest.raises(ValueError):
        Temperature(value, unit)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_non_finite_value(value: float) -> None:
    """Check that NaN and infinite values are rejected."""
    with pytest.raises(ValueError):
        Temperature(value)


@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
@pytest.mark.parametrize("unit", ["C", "F", "K"])
def test_conversions(
    celsius: float,
    fahrenheit: float,
    kelvin: float,
    unit: str,
) -> None:
    """Check all conversion methods from each starting unit."""
    reference_values = {"C": celsius, "F": fahrenheit, "K": kelvin}
    temperature = Temperature(reference_values[unit], unit)

    # Disable relative tolerance to enforce the required absolute tolerance.
    assert temperature.to_celsius() == pytest.approx(
        celsius, abs=1e-9, rel=0
    )
    assert temperature.to_fahrenheit() == pytest.approx(
        fahrenheit, abs=1e-9, rel=0
    )
    assert temperature.to_kelvin() == pytest.approx(
        kelvin, abs=1e-9, rel=0
    )


@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
@pytest.mark.parametrize("source_unit", ["C", "F", "K"])
@pytest.mark.parametrize("target_unit", ["C", "c", "F", "f", "K", "k"])
def test_convert_to(
    celsius: float,
    fahrenheit: float,
    kelvin: float,
    source_unit: str,
    target_unit: str,
) -> None:
    """Check conversion between units without changing the original."""
    reference_values = {"C": celsius, "F": fahrenheit, "K": kelvin}
    original = Temperature(reference_values[source_unit], source_unit)

    converted = original.convert_to(target_unit)

    assert isinstance(converted, Temperature)
    assert converted.unit == target_unit.upper()
    assert converted.value == pytest.approx(
        reference_values[target_unit.upper()], abs=1e-9, rel=0
    )

    # A separate object must be returned, even for the same unit.
    assert converted is not original
    assert original.value == reference_values[source_unit]
    assert original.unit == source_unit


@pytest.mark.parametrize("target_unit", ["X", "", "Celsius"])
def test_convert_to_invalid_unit(target_unit: str) -> None:
    """Check that an unsupported target unit raises ValueError."""
    with pytest.raises(ValueError):
        Temperature(25).convert_to(target_unit)


@pytest.mark.parametrize("value", [-273.15, -40.0, 0.0, 25.0, 37.0, 100.0])
def test_round_trip(value: float) -> None:
    """Check that C -> F -> K -> C reproduces the original."""
    original = Temperature(value, "C")

    converted = original.convert_to("F").convert_to("K").convert_to("C")

    assert converted.unit == "C"
    assert converted.value == pytest.approx(value, abs=1e-9, rel=0)
    assert converted == original


@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
def test_cross_unit_equality(
    celsius: float, fahrenheit: float, kelvin: float
) -> None:
    """Check equality and inclusive comparisons across different units."""
    temperatures = [
        Temperature(celsius, "C"),
        Temperature(fahrenheit, "F"),
        Temperature(kelvin, "K"),
    ]

    for first in temperatures:
        for second in temperatures:
            assert first == second
            assert not (first != second)
            assert first <= second
            assert first >= second
            assert not (first < second)
            assert not (first > second)


@pytest.mark.parametrize(
    "lower_value, lower_unit, higher_value, higher_unit",
    [
        (0.0, "C", 300.0, "K"),
        (32.0, "F", 37.0, "C"),
        (233.15, "K", 32.0, "F"),
    ],
)
def test_cross_unit_ordering(
    lower_value: float,
    lower_unit: str,
    higher_value: float,
    higher_unit: str,
) -> None:
    """Check all six comparisons for unequal temperatures."""
    lower = Temperature(lower_value, lower_unit)
    higher = Temperature(higher_value, higher_unit)

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
    "difference, expected_equal",
    [(0.0, True), (0.5e-9, True), (2e-9, False)],
)
def test_comparison_tolerance(
    difference: float, expected_equal: bool
) -> None:
    """Check comparison behavior inside and outside the tolerance."""
    lower = Temperature(1.0, "K")
    higher = Temperature(1.0 + difference, "K")

    assert (lower == higher) == expected_equal
    assert (lower != higher) == (not expected_equal)
    assert (lower < higher) == (not expected_equal)
    assert (higher > lower) == (not expected_equal)
    assert lower <= higher
    assert higher >= lower
    assert (higher <= lower) == expected_equal
    assert (lower >= higher) == expected_equal


@pytest.mark.parametrize(
    "method_name",
    ["__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__"],
)
def test_unsupported_comparison(method_name: str) -> None:
    """Check that comparison methods return NotImplemented for other types."""
    temperature = Temperature(25)

    # Direct calls are intentional here to inspect the required return value.
    method = getattr(temperature, method_name)
    assert method(25) is NotImplemented


@pytest.mark.parametrize(
    "value, unit, expected",
    [
        (25.0, "C", "25.00 °C"),
        (77.0, "F", "77.00 °F"),
        (298.15, "K", "298.15 K"),
        (-40.0, "C", "-40.00 °C"),
        (25.126, "C", "25.13 °C"),
    ],
)
def test_str(value: float, unit: str, expected: str) -> None:
    """Check readable formatting, unit symbols, and rounding."""
    assert str(Temperature(value, unit)) == expected


@pytest.mark.parametrize(
    "value, unit, expected",
    [
        (25.0, "C", "Temperature(25.0, 'C')"),
        (77.0, "f", "Temperature(77.0, 'F')"),
        (0.0, "K", "Temperature(0.0, 'K')"),
    ],
)
def test_repr(value: float, unit: str, expected: str) -> None:
    """Check that the representation shows the stored value and unit."""
    assert repr(Temperature(value, unit)) == expected
    