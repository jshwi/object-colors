"""tests.conftest."""
import pytest

from object_colors import Color

from . import FORE


@pytest.fixture(name="color")
def fixture_color() -> Color:
    """Instantiated ``Color`` object."""
    return Color()


@pytest.fixture(name="populated_colors")
def fixture_populated_colors(color: Color) -> Color:
    """Instantiated ``Color`` object with ``populate_colors`` executed.

    :param color: Instantiated ``Color`` object.
    """
    color.populate(FORE)
    return color
