"""
tests._test
===========
"""
from typing import Any, Tuple

import pytest

from object_colors import Color

from . import (
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ATTR_COLOR_EFFECT_EXCEED_INDEX,
    COLOR_INT_INDEX,
    COLORS,
    FORE_CODES,
    RESET,
    TEST_STR,
    TEST_TUPLE,
)


@pytest.mark.parametrize(
    "attr,pair,expected",
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ids=[f"{i[0]}-{i[1][0]}" for i in ATTR_COLOR_EFFECT_CODE_INDEX],
)
def test_get(attr: str, pair: Tuple[str, int], expected: str) -> None:
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


def test_set_static(color: Color) -> None:
    """Test that an existing instance attribute can be set with the
    ``set`` method.

    :param color: Instantiated ``Color`` object.
    """
    color.fore = "red"
    assert color.get(TEST_STR) == f"{FORE_CODES[1]}{TEST_STR}{RESET}"


def test_set_dynamic(color: Color) -> None:
    """Test that a subclass can be set with the ``set`` method.

    :param color: Instantiated ``Color`` object.
    """
    key = "the_name_is_up_to_the_user"
    setattr(color, key, {"fore": "red"})
    expected = f"{FORE_CODES[1]}{TEST_STR}{RESET}"
    assert getattr(color, key).get(TEST_STR) == expected


@pytest.mark.parametrize(
    "attr,pair,expected",
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ids=[f"{i[0]}-{i[1][0]}" for i in ATTR_COLOR_EFFECT_CODE_INDEX],
)
def test_print(
    attr: str, pair: Tuple[str, int], expected: str, capsys: Any
) -> None:
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


@pytest.mark.parametrize("name,idx", COLOR_INT_INDEX, ids=COLORS)
def test_populate_colors(populated_colors: Color, name: str, idx: int) -> None:
    """Test the string is as it is supposed to be when the ``get``
    method is used within a color subclass.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    :param name:                Name of attribute to test for.
    :param idx:                 Index of expected ANSI escape code.
    """
    result = getattr(populated_colors, name).get(TEST_STR)
    assert result == f"{FORE_CODES[idx]}{TEST_STR}{RESET}"


def test_repr(color: Color, capsys: Any) -> None:
    """Test output from ``__repr__``.

    :param color:   Instantiated ``Color`` object.
    :param capsys:  ``pytest`` fixture for capturing and returning
                    terminal output
    """
    print(color)
    captured = capsys.readouterr()
    assert (
        captured.out.strip() == "Color(effect=0, fore=7, back=None, objects())"
    )


def test_populate_err(color: Color) -> None:
    """Test attribute error is raised when invalid value is provided
    to populate.

    :param color: Instantiated ``Color`` object.
    """
    with pytest.raises(AttributeError) as err:
        color.populate("key")

    assert str(err.value) == f"'{type(color).__name__}' has no attribute 'key'"


def test_populate_colors_deprecated(color: Color) -> None:
    """Test the legacy ``populate_colors`` works as it should.

    :param color: Instantiated ``Color`` object.
    """
    color.populate_colors()
    for item in color.colors:
        assert hasattr(color, item)


def test_set_invalid(color: Color) -> None:
    """Test that a non-existing instance attribute will raise an
    ``AttributeError`` if attempting to be set.

    :param color: Instantiated ``Color`` object.
    """
    key = "not_a_key"
    kwargs = {key: "not_a_value"}
    with pytest.raises(TypeError) as err:
        color.set(**kwargs)

    expected = f"got an unexpected keyword argument '{key}'"
    assert str(err.value) == expected


def test_key_error(color: Color) -> None:
    """Test ``AttributeError`` is raised when invalid keyword arguments
    are provided as ``effect``, ``fore``, or ``back``

    :param color: Instantiated ``Color`` object.
    """
    with pytest.raises(AttributeError) as err:
        color.not_an_attr.print("Hello, world!")

    assert str(err.value) == "'Color' object has no attribute 'not_an_attr'"


@pytest.mark.parametrize(
    "key,idx",
    ATTR_COLOR_EFFECT_EXCEED_INDEX,
    ids=[f"{k}-exceed" for k in ATTR_COLOR_EFFECT_EXCEED_INDEX],
)
def test_index_error_kwargs(key: str, idx: int) -> None:
    """Test that ``IndexError`` and correct error message are raised
    when an out-of-range integer argument is supplied to ``Color``
    constructor.

    :param key: Keyword argument for constructor: ``effect``, ``fore``,
                or ``back``
    :param idx: Index exceeding the length of the key's respective
                tuple.
    """
    with pytest.raises(IndexError) as err:
        kwargs = {key: idx}
        Color(**kwargs)

    assert str(err.value) == "tuple index out of range"
