"""
tests._test
===========
"""
from object_colors import Color

from . import ATTRS, GREEN, INSTANCES, RED, RESET, TEST_STR


def test_color_string():
    """Test a simple string."""
    color = Color(fore="green")
    assert color.get(TEST_STR) == f"{GREEN}{TEST_STR}{RESET}"


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
    color = Color("red", "bold", "green")
    assert color.fore == 1
    assert color.effect == 1
    assert color.back == 2


def test_str_args():
    """Test for the correct ANSI codes for color, effect, and
    background.
    """
    color = Color("red", "bold", "green")
    assert color.fore == 1
    assert color.effect == 1
    assert color.back == 2


def test_str_ints():
    """Test the correct ANSI code integers are produced."""
    color = Color(1, 1, 2)
    assert color.fore == 1
    assert color.effect == 1
    assert color.back == 2


def test_int_dict():
    """Test for a non-existing color and assert it will default to
    white instead of raising an error."""
    color = Color(orange=1)
    assert color.fore == 7


def test_tuple_return(populated_colors):
    """Test that a tuple supplied as arguments gets returned as a tuple
    and not just a concatenated string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    tup = populated_colors.red.get("t", "u", "p")
    assert tup == (
        "\u001b[0;31;40mt\u001b[0;0m",
        "\u001b[0;31;40mu\u001b[0;0m",
        "\u001b[0;31;40mp\u001b[0;0m",
    )


def test_pop_result(populated_colors):
    """Test colors can be removed from the instance.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    assert hasattr(populated_colors, "red")
    red = populated_colors.pop("red")
    assert "red" not in populated_colors.__dict__
    red_string = red.get(TEST_STR)
    assert red_string == f"\u001b[0;31;40m{TEST_STR}\u001b[0;0m"


def test_pop_no_result(color):
    """Test that error goes by silently if item does not exist.

    :param color: Instantiated ``Color`` object.
    """
    assert "red" not in color.__dict__
    red = color.pop("red")
    assert red is None


def test_color_print(capsys, populated_colors):
    """Test the string is as it is supposed to be when the print
    function is used.

    :param capsys:              ``pytest`` fixture to capture output.
    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    populated_colors.red.print(TEST_STR)
    captured = capsys.readouterr()
    assert captured.out == f"{RED}{TEST_STR}{RESET}\n"
