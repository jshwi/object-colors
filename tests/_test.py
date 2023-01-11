"""
tests._test
===========
"""
from typing import Any, Tuple

import pytest

import object_colors
from object_colors import Color

from . import (
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ATTR_COLOR_EFFECT_EXCEED_INDEX,
    ATTR_COLOR_EFFECT_TYPE_ERROR,
    ATTR_COLOR_EFFECT_UNMATCHED_INDEX,
    BACK,
    COLOR_INT_INDEX,
    COLORS,
    EFFECT,
    FORE,
    FORE_CODES,
    RESET,
    TEST_STR,
    TEST_TUPLE,
    VERSION,
)


@pytest.mark.parametrize(
    "attr,pair,expected",
    ATTR_COLOR_EFFECT_CODE_INDEX,
    ids=[f"{i[0]}-{i[1][0]}" for i in ATTR_COLOR_EFFECT_CODE_INDEX],
)
def test_get(attr: str, pair: Tuple[str, int], expected: str) -> None:
    """Test returning a simple string with effects and colors.

    :param attr: Attribute belonging to ``Color`` constructor call.
    :param pair: A pair containing a str and an int or an int and int.
    :param expected: Expected escape codes ordered in indexed order by
        their integer value.
    """
    color = Color(**{attr: pair[0]})
    assert color.get(TEST_STR) == f"{expected}{TEST_STR}{RESET}"
    assert color.get(*TEST_TUPLE) == (
        f"{expected}{TEST_TUPLE[0]}{RESET}",
        f"{expected}{TEST_TUPLE[1]}{RESET}",
        f"{expected}{TEST_TUPLE[2]}{RESET}",
    )


def test_set_static(color: Color) -> None:
    """Test existing instance attribute can be set with  ``set``.

    :param color: Instantiated ``Color`` object.
    """
    color.fore = "red"
    assert color.get(TEST_STR) == f"{FORE_CODES[1]}{TEST_STR}{RESET}"


def test_set_dynamic(color: Color) -> None:
    """Test a subclass can be set with ``set``.

    :param color: Instantiated ``Color`` object.
    """
    key = "the_name_is_up_to_the_user"
    setattr(color, key, {FORE: "red"})
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

    :param attr: Attribute belonging to ``Color`` constructor call.
    :param pair: A pair containing a str and an int or an int and int.
    :param expected: Expected escape codes ordered in indexed order by
        their integer value.
    :param capsys: Capture sys stdout and stderr.
    """
    color = Color(**{attr: pair[0]})
    color.print(TEST_STR)
    captured = capsys.readouterr()
    assert captured.out == f"{expected}{TEST_STR}{RESET}\n"
    color.print(*TEST_TUPLE)
    captured = capsys.readouterr()
    assert captured.out == f"{expected}{' '.join(TEST_TUPLE)}{RESET}\n"


@pytest.mark.parametrize("name,idx", COLOR_INT_INDEX, ids=COLORS)
def test_populate_colors(color: Color, name: str, idx: int) -> None:
    """Test for expected str when ``get`` is used within color subclass.

    :param color: Instantiated ``Color`` object.
    :param name: Name of attribute to test for.
    :param idx: Index of expected ANSI escape code.
    """
    color.populate_colors()
    result = getattr(color, name).get(TEST_STR)
    assert result == f"{FORE_CODES[idx]}{TEST_STR}{RESET}"


def test_repr(color: Color, capsys: Any) -> None:
    """Test output from ``__repr__``.

    :param color: Instantiated ``Color`` object.
    :param capsys: Capture sys stdout and stderr.
    """
    print(color)
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "Color(effect=None, fore=None, back=None, objects())"
    )


def test_populate_err(color: Color) -> None:
    """Test ``AttributeError`` raised for invalid value to ``populate``.

    :param color: Instantiated ``Color`` object.
    """
    with pytest.raises(AttributeError) as err:
        color.populate("key")

    assert str(err.value) == f"'{type(color).__name__}' has no attribute 'key'"


def test_populate_colors_deprecated(color: Color) -> None:
    """Test ``populate_colors`` properly sets attributes.

    :param color: Instantiated ``Color`` object.
    """
    color.populate_colors()
    for item in color.colors:
        assert hasattr(color, item)


def test_set_invalid(color: Color) -> None:
    """Test ``AttributeError`` raised for non-existing attribute.

    :param color: Instantiated ``Color`` object.
    """
    key = "not_a_key"
    kwargs = {key: "not_a_value"}
    with pytest.raises(TypeError) as err:
        color.set(**kwargs)

    expected = f"got an unexpected keyword argument '{key}'"
    assert str(err.value) == expected


def test_key_error(color: Color) -> None:
    """Test ``AttributeError`` raised for invalid keyword arguments.

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
    """Test ``IndexError`` raised for out-of-range integer.

    :param key: Keyword argument for constructor: ``effect``, ``fore``,
        or ``back``
    :param idx: Index exceeding the length of the key's respective
        tuple.
    """
    with pytest.raises(IndexError) as err:
        kwargs = {key: idx}
        Color(**kwargs)

    assert str(err.value) == "tuple index out of range"


@pytest.mark.parametrize(
    "key,value", ATTR_COLOR_EFFECT_TYPE_ERROR, ids=[EFFECT, FORE, BACK]
)
def test_type_error_kwargs(key: str, value: Any) -> None:
    """Test ``TypeError`` raised when for invalid type.

    :param key: Keyword argument for constructor: ``effect``, ``fore``,
        or ``back``
    :param value: A type not valid for attribute.
    """
    with pytest.raises(TypeError) as err:
        kwargs = {key: value}
        Color(**kwargs)

    assert f"not {type(value).__name__}" in str(err.value)


@pytest.mark.parametrize("key,value", ATTR_COLOR_EFFECT_UNMATCHED_INDEX)
def test_value_error_kwargs(key: str, value: str) -> None:
    """Test ``ValueError`` raised for invalid keyword argument.

    :param key: Keyword argument for constructor: ``effect``, ``fore``,
        or ``back``
    :param value: Value NOT belonging to any of the above keys.
    """
    with pytest.raises(ValueError) as err:
        kwargs = {key: value}
        Color(**kwargs)

    assert str(err.value) == f"'{value}' cannot be assigned to '{key}'"


def test_all_fields(color: Color) -> None:
    """Test fields are properly returned with semicolon for str.

    :param color: Instantiated ``Color`` object.
    """
    color.set(effect=1, fore=1, back=1)
    assert color.get("Hello, world!") == "\x1b[1;3141mHello, world!\x1b[0;0m"


def test_get_no_key(color: Color) -> None:
    """Test ``AttributeError`` raised for invalid value to ``get``.

    :param color: Instantiated ``Color`` object.
    """
    with pytest.raises(AttributeError) as err:
        color.r.get()

    assert str(err.value) == "'Color' object has no attribute 'r'"


def test_len(color: Color) -> None:
    """Test correct length of ``color._objects`` is returned.

    :param color: Instantiated ``Color`` object.
    """
    assert len(color) == 0
    color.populate(FORE)
    assert len(color) == 8


def test_print_nothing(color: Color) -> None:
    """Test no error is raised when printing nothing.

    :param color: Instantiated ``Color`` object.
    """
    color.print()


def test_print_non_str(capsys: pytest.CaptureFixture, color: Color) -> None:
    """Test printing of any objects.

    :param capsys: Capture sys stdout and stderr.
    :param color: Instantiated ``Color`` object.
    """
    color.print(None)
    assert capsys.readouterr()[0].strip() == "None"
    color.print(None, color)
    assert (
        capsys.readouterr()[0].strip()
        == "None Color(effect=None, fore=None, back=None, objects())"
    )


def test_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test ``object_colors.__version__``.

    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr("object_colors.__version__", VERSION)
    assert object_colors.__version__ == VERSION
