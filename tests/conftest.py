"""
tests.conftest
"""
import pytest

from object_colors import Color


@pytest.fixture(name="color")
def fixture_color():
    """Instantiated ``Color`` object."""
    return Color()


@pytest.fixture(name="populated_colors")
def fixture_populated_colors(color):
    """Instantiated ``Color`` object with ``populate_colors``
    executed.

    :param color: Instantiated ``Color`` object.
    """
    color.populate_colors()
    return color
