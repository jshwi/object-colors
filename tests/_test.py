"""
tests._test
===========
"""
from object_colors import Color

from . import (
    ATTRS,
    CODES,
    COLORED_DUPES,
    DUPE_MARKED,
    DUPE_MARKED_COLOR,
    DUPES,
    EXACT_INDEX_COLOR,
    GREEN,
    INSTANCES,
    LONG_STRING,
    MARKED,
    MARKED_COLOR,
    MARKED_SECOND,
    MARKED_SECOND_COLOR,
    RED,
    RESET,
    SPACED_WORDS,
    SPACED_WORDS_COLOR,
    TEST_STR,
)


def test_color_string():
    """Test a simple string."""
    color = Color(text="green")
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
    assert color.text == 1
    assert color.effect == 1
    assert color.background == 2


def test_str_args():
    """Test for the correct ANSI codes for color, effect, and
    background
    """
    _color = Color("red", "bold", "green")
    assert _color.text == 1
    assert _color.effect == 1
    assert _color.background == 2


def test_str_ints():
    """Test the correct ANSI code integers are produced."""
    _color = Color(1, 1, 2)
    assert _color.text == 1
    assert _color.effect == 1
    assert _color.background == 2


def test_int_dict():
    """Test for a non-existing color and assert it will default to
    white instead of raising an error."""
    _color = Color(orange=1)
    assert _color.text == 7


def test_exact_letter_in_colored_string(populated_colors):
    """For multicolored string assert the exact letter is the correct
    color.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "c")
    assert keys == TEST_STR
    colored_keys = populated_colors.red.get_key(color_str, "c")
    assert colored_keys == color_str


def test_exact_word_in_string(populated_colors):
    """Test the exact word selected to color is the appropriate
    color.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "Cc:")
    assert keys == MARKED
    colored_keys = populated_colors.red.get_key(color_str, "Cc:")
    assert colored_keys == MARKED_COLOR


def test_exact_second_word_in_string(populated_colors):
    """verify indices are working (at least for some)

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "My")
    assert keys == MARKED_SECOND
    colored_keys = populated_colors.red.get_key(color_str, "My")
    assert colored_keys == MARKED_SECOND_COLOR


def test_dupe_words(populated_colors):
    """Test the correct output is produced when there are duplicate
    words in the string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    keys = populated_colors.red.get_key(DUPES, "one")
    assert keys == DUPE_MARKED
    colored_keys = populated_colors.red.get_key(COLORED_DUPES, "one")
    assert colored_keys == DUPE_MARKED_COLOR


def test_word_in_string(populated_colors):
    """Test a colored word exists in string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "cc:")
    assert keys == TEST_STR
    colored_keys = populated_colors.red.get_key(color_str, "cc:")
    assert colored_keys == color_str


def test_words_in_string(populated_colors):
    """Test colored words exist in string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "Cc:", "Business")
    assert keys == SPACED_WORDS
    colored_keys = populated_colors.red.get_key(color_str, "Cc:", "Business")
    assert colored_keys == SPACED_WORDS_COLOR


def test_exact_letter_in_string(populated_colors):
    """Test exact letter exists in string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    colored_keys = populated_colors.red.get_key(
        color_str, "c", ignore_case=True, scatter=True
    )
    assert colored_keys == EXACT_INDEX_COLOR


def test_exact_word_in_string_ignore_case(populated_colors):
    """Test word is in string, whether letters are a mixture of upper
    and lower case, or not.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "Cc:", ignore_case=True)
    assert keys == MARKED
    colored_keys = populated_colors.red.get_key(
        color_str, "Cc:", ignore_case=True
    )
    assert colored_keys == MARKED_COLOR


def test_word_in_string_ignore_case(populated_colors):
    """Test word is in string, whether letters are a mixture of upper
    and lower case, or not.
    """
    color_str = populated_colors.green.get(TEST_STR)
    keys = populated_colors.red.get_key(TEST_STR, "cc:", ignore_case=True)
    assert keys == MARKED
    colored_keys = populated_colors.red.get_key(
        color_str, "cc:", ignore_case=True
    )
    assert colored_keys == MARKED_COLOR


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


def test_multi_values(populated_colors):
    """Test multiple ANSI and color values at once.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    multi = populated_colors.multicolor(LONG_STRING)
    ansis = populated_colors.get_list(multi)
    for ansi in ansis:
        if Color.ansi_escape.match(ansi):
            for string in ansi:
                if string.isdigit():
                    assert int(string) <= 7


def test_none():
    """Test the correct string is returned when no keyword is used for
    multicolor.
    """
    _color = Color(text="GREEN")
    none = _color.multicolor(LONG_STRING)
    assert none == LONG_STRING


def test_with_populated_colors(populated_colors):
    """Test all the colors can be populated at once.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    all_colors = populated_colors.multicolor(LONG_STRING)
    for code in CODES:
        assert code in all_colors


def test_pop_result(populated_colors):
    """Test colors can be removed from the instance.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    """
    assert hasattr(populated_colors, "red")
    red = populated_colors.pop("red")
    assert "red" not in populated_colors.__dict__
    red_string = red.get("This is red")
    assert red_string == "\u001b[0;31;40mThis is red\u001b[0;0m"


def test_pop_no_result(color):
    """Test that error goes by silently if item does not exist."""
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
    populated_colors.red.print("This stdout is red")
    captured = capsys.readouterr()
    assert captured.out == f"{RED}This stdout is red{RESET}\n"


def test_print_multi(capsys, populated_colors):
    """Test printing with multi-colored string.

    :param populated_colors:    Instantiated ``Color`` object where
                                ``populate_colors`` has been called.
    :param capsys:              ``pytest`` fixture to capture output.
    """
    populated_colors.print(LONG_STRING, multi=True)
    captured = capsys.readouterr()
    for code in CODES:
        assert code in captured.out
