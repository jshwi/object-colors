"""
tests.conftest
==============
"""
import pytest

from object_colors import Color


@pytest.fixture(name="color")
def fixture_color() -> Color:
    """Instantiated ``Color`` object.

    :return: Instantiated ``Color`` object.
    """
    return Color()
