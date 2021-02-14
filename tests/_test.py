"""
tests._test
===========
"""
import pytest

from object_colors import Color

from . import (
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ATTR_COLOR_EFFECT_INDEX,
    ATTRS,
    COLOR_INT_INDEX,
    COLORS,
    FORE_CODES,
    INSTANCES,
    RESET,
    TEST_STR,
    TEST_TUPLE,
)


@pytest.mark.parametrize(
    "attr,pair",
    ATTR_COLOR_EFFECT_INDEX,
    ids=[f"{i[0]}-{i[1][0]}" for i in ATTR_COLOR_EFFECT_INDEX],
)
def test_getattr(attr, pair):
    """Test the value of ``Color`` attributes are what they are supposed
    to be when instantiating with a ``str`` or an ``int``.

    :param attr:    Attribute belonging to ``Color`` constructor call.
    :param pair:    A pair containing a str and an int or an int and and
                    int
    """
    arg, idx = pair
    color = Color(**{attr: arg})
    assert getattr(color, attr) == idx


@pytest.mark.parametrize(
    "attr,pair,expected",
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ids=[f"{i[0]}-{i[1][0]}" for i in ATTR_COLOR_EFFECT_CODE_INDEX],
)
def test_get(attr, pair, expected):
    """Test returning a simple string with effects and colors.

    :param attr:        Attribute belonging to ``Color`` constructor
                        call.
    :param pair:        A pair containing a str and an int or an int and
                        and int.
    :param expected:    Expected escape codes ordered in indexed order
                        by their integer value.
    """
    color = Color(**{attr: pair[0]})
    assert color.get(TEST_STR) == f"{expected}{TEST_STR}{RESET}"
    assert color.get(*TEST_TUPLE) == (
        f"{expected}{TEST_TUPLE[0]}{RESET}",
        f"{expected}{TEST_TUPLE[1]}{RESET}",
        f"{expected}{TEST_TUPLE[2]}{RESET}",
    )


@pytest.mark.parametrize(
    "attr,pair,expected",
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ids=[f"{i[0]}-{i[1][0]}" for i in ATTR_COLOR_EFFECT_CODE_INDEX],
)
def test_print(attr, pair, expected, capsys):
    """Test printing a simple string with effects and colors.

    :param attr:        Attribute belonging to ``Color`` constructor
                        call.
    :param pair:        A pair containing a str and an int or an int and
                        and int.
    :param expected:    Expected escape codes ordered in indexed order
                        by their integer value.
    :param capsys:      ``pytest`` fixture for capturing and returning
                        terminal output
    """
    color = Color(**{attr: pair[0]})
    color.print(TEST_STR)
    captured = capsys.readouterr()
    assert captured.out == f"{expected}{TEST_STR}{RESET}\n"
    color.print(*TEST_TUPLE)
    captured = capsys.readouterr()
    assert captured.out == f"{expected}{' '.join(TEST_TUPLE)}{RESET}\n"


def test__getattr__(populated_colors):
    """Test __getattr__.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    for attr in ATTRS:
        assert hasattr(populated_colors, attr)


def test__dir__(populated_colors):
    """Test __dir__.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_instances = populated_colors.__dir__()
    assert color_instances == INSTANCES
    color = Color(fore="red", effect="bold", back="green")
    assert color.fore == 1
    assert color.effect == 1
    assert color.back == 2


def test_set_static(color):
    """Test that an existing instance attribute can be set with the
    ``set`` method.

    :param color: Instantiated ``Color`` object.
    """
    color.set(fore="red")
    assert color.get(TEST_STR) == f"{FORE_CODES[1]}{TEST_STR}{RESET}"


def test_set_dynamic(color):
    """Test that a subclass can be set with the ``set`` method.

    :param color: Instantiated ``Color`` object.
    """
    key = "the_name_is_up_to_the_user"
    color.set(**{key: {"fore": "red"}})
    expected = f"{FORE_CODES[1]}{TEST_STR}{RESET}"
    assert getattr(color, key).get(TEST_STR) == expected


@pytest.mark.parametrize("name,idx", COLOR_INT_INDEX, ids=COLORS)
def test_populate_colors(populated_colors, name, idx):
    """Test the string is as it is supposed to be when the ``get``
    method is used within a color subclass.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    :param name:                Name of attribute to test for.
    :param idx:                 Index of expected ANSI escape code.
    """
    result = getattr(populated_colors, name).get(TEST_STR)
    assert result == f"{FORE_CODES[idx]}{TEST_STR}{RESET}"


def test_repr(color, capsys):
    """Test output from ``__repr__``.

    :param color:   Instantiated ``Color`` object.
    :param capsys:  ``pytest`` fixture for capturing and returning
                    terminal output
    """
    print(color)
    captured = capsys.readouterr()
    assert captured.out.strip() == (
        "Color(effect=0, fore=7, back=None, bold=Color(effect=1, fore=7, "
        "back=None))"
    )
