"""
tests._test
===========
"""
import pytest

from object_colors import Color

from . import ATTRS, CODES, INSTANCES, RESET, TEST_STR, TEST_TUPLE


@pytest.mark.parametrize("fore,expected", [("red", 1), ("green", 2)])
def test_color_string(fore, expected):
    """Test a simple string."""
    color = Color(fore=fore)
    assert color.get(TEST_STR) == f"{CODES[expected]}{TEST_STR}{RESET}"


def test__getattr__(color):
    """Test __getattr__.

    :param color: Instantiated ``Color`` object.
    """
    for attr in ATTRS:
        assert hasattr(color, attr)


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


def test_str_args():
    """Test for the correct ANSI codes for color, effect, and
    background.
    """
    color = Color(fore="red", effect="bold", back="green")
    assert color.fore == 1
    assert color.effect == 1
    assert color.back == 2


def test_tuple_return(populated_colors):
    """Test that a tuple supplied as arguments gets returned as a tuple
    and not just a concatenated string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    tup = populated_colors.red.get("t", "u", "p")
    assert tup == (
        "\u001b[0;31mt\u001b[0;0m",
        "\u001b[0;31mu\u001b[0;0m",
        "\u001b[0;31mp\u001b[0;0m",
    )


def test_color_print(capsys, populated_colors):
    """Test the string is as it is supposed to be when the print
    function is used.

    :param capsys:              ``pytest`` fixture to capture output.
    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    populated_colors.red.print(TEST_STR)
    captured = capsys.readouterr()
    assert captured.out == f"{CODES[1]}{TEST_STR}{RESET}\n"
    populated_colors.red.print(*TEST_TUPLE)
    captured = capsys.readouterr()
    assert captured.out == f"{CODES[1]}{' '.join(TEST_TUPLE)}{RESET}\n"


def test_repr(color, capsys) -> None:
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


def test_set_subclass(capsys):
    """Test that a color subclass can be set within the main
    instance.
    """
    color = Color()
    color.set(the_name_is_up_to_the_user={"fore": "red"})
    color.the_name_is_up_to_the_user.print(TEST_STR)
    captured = capsys.readouterr()
    assert captured.out == f"{CODES[1]}{TEST_STR}{RESET}\n"


def test_set_regular_attr(capsys):
    """Test that an attr can be set with the ``set`` method too
    instance.
    """
    color = Color()
    assert color.fore == 7
    color.set(fore="red")
    assert color.fore == 1
    color.print(TEST_STR)
    captured = capsys.readouterr()
    assert captured.out == f"{CODES[1]}{TEST_STR}{RESET}\n"
