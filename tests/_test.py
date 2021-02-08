"""
tests._test
===========
"""
from object_colors import Color


def test_color_string(str_, green, color_str, reset):
    assert color_str == f"{green}{str_}{reset}"


def test__getattr__(attrs):
    color = Color()
    for attr in attrs:
        assert hasattr(color, attr)


def test__dir__(color, instances):
    color_instances = color.__dir__()
    assert color_instances == instances


def test_str_args():
    color = Color("red", "bold", "green")
    assert color.text == 1
    assert color.effect == 1
    assert color.background == 2


def test_str_ints():
    color = Color(1, 1, 2)
    assert color.text == 1
    assert color.effect == 1
    assert color.background == 2


def test_int_dict():
    color = Color(orange=1)
    assert color.text == 7


def test_exact_letter_in_colored_string(color, color_str, str_):
    keys = color.red.get_key(str_, "c")
    assert keys == str_
    colored_keys = color.red.get_key(color_str, "c")
    assert colored_keys == color_str


def test_exact_word_in_string(color, color_str, marked_color, str_, marked):
    keys = color.red.get_key(str_, "Cc:")
    assert keys == marked
    colored_keys = color.red.get_key(color_str, "Cc:")
    assert colored_keys == marked_color


def test_exact_second_word_in_string(
    color, color_str, marked_second_color, str_, marked_second
):
    """verify indices are working (at least for some)"""
    keys = color.red.get_key(str_, "My")
    assert keys == marked_second
    colored_keys = color.red.get_key(color_str, "My")
    assert colored_keys == marked_second_color


def test_dupe_words(
    color, colored_dupes, dupe_marked_color, dupes, dupe_marked
):
    keys = color.red.get_key(dupes, "one")
    assert keys == dupe_marked
    colored_keys = color.red.get_key(colored_dupes, "one")
    assert colored_keys == dupe_marked_color


def test_word_in_string(color, color_str, str_):
    keys = color.red.get_key(str_, "cc:")
    assert keys == str_
    colored_keys = color.red.get_key(color_str, "cc:")
    assert colored_keys == color_str


def test_words_in_string(
    color, color_str, spaced_words_color, str_, spaced_words
):
    keys = color.red.get_key(str_, "Cc:", "Business")
    assert keys == spaced_words
    colored_keys = color.red.get_key(color_str, "Cc:", "Business")
    assert colored_keys == spaced_words_color


def test_exact_letter_in_string(color, color_str, exact_idx_color):
    colored_keys = color.red.get_key(
        color_str, "c", ignore_case=True, scatter=True
    )
    assert colored_keys == exact_idx_color


def test_exact_word_in_string_ignore_case(
    color, color_str, marked_color, marked, str_
):
    keys = color.red.get_key(str_, "Cc:", ignore_case=True)
    assert keys == marked
    colored_keys = color.red.get_key(color_str, "Cc:", ignore_case=True)
    assert colored_keys == marked_color


def test_word_in_string_ignore_case(
    color, color_str, marked_color, str_, marked
):
    keys = color.red.get_key(str_, "cc:", ignore_case=True)
    assert keys == marked
    colored_keys = color.red.get_key(color_str, "cc:", ignore_case=True)
    assert colored_keys == marked_color


def test_tuple_return(color):
    tup = color.red.get("t", "u", "p")
    assert tup == (
        "\u001b[0;31;40mt\u001b[0;0m",
        "\u001b[0;31;40mu\u001b[0;0m",
        "\u001b[0;31;40mp\u001b[0;0m",
    )


def test_multi_values(color, long_str):
    rb = color.multicolor(long_str)
    ansis = color.get_list(rb)
    for ansi in ansis:
        if Color.ansi_escape.match(ansi):
            for str_ in ansi:
                if str_.isdigit():
                    assert int(str_) <= 7


def test_multi_empty(long_str):
    color = Color()
    rb = color.multicolor(long_str)
    assert rb == long_str


def test_multi_increment(colors):
    args = []
    color_class = Color()
    for color in colors:
        color_class.set({color: {"text": color}})
        args.append(color)
        tups = tuple(args)
        for tup in tups:
            assert hasattr(color_class, tup)


def test_none(long_str):
    color = Color(text="green")
    none = color.multicolor(long_str)
    print(none)
    assert none == long_str


def test_green_and_none(long_str):
    color = Color()
    color.set(green={"text": "green"})
    green_and_none = color.multicolor(long_str)
    print(green_and_none)
    assert "0;32;40m" in green_and_none


def test_green_red_none(long_str):
    color = Color()
    codes = ["0;31;40m", "0;32;40m"]
    color.set(green={"text": "green"})
    color.set(red={"text": "red"})
    green_red_none = color.multicolor(long_str)
    for code in codes:
        assert code in green_red_none


def test_with_populated_colors(long_str, codes):
    populate = Color()
    populate.populate_colors()
    all_colors = populate.multicolor(long_str)
    for code in codes:
        assert code in all_colors


def test_pop_result(color):
    assert hasattr(color, "red")
    red = color.pop("red")
    assert "red" not in color.__dict__
    red_string = red.get("This is red")
    assert red_string == "\u001b[0;31;40mThis is red\u001b[0;0m"


def test_pop_no_result():
    color = Color()
    assert "red" not in color.__dict__
    red = color.pop("red")
    assert red is None


def test_populated(colors):
    color = Color()
    color.populate_colors()
    contents = color.__dict__
    result = False
    bool_list = []
    colors.pop(0)
    for color in colors:
        for key in contents:
            result = key == color
        if result:
            bool_list.append(result)
    for result in bool_list:
        assert result


def test_color_print(color, red, capsys, reset):
    color.red.print("This stdout is red")
    captured = capsys.readouterr()
    assert captured.out == f"{red}This stdout is red{reset}\n"


def test_print_multi(capsys, long_str, codes):
    color = Color()
    color.populate_colors()
    color.print(long_str, multi=True)
    captured = capsys.readouterr()
    for code in codes:
        assert code in captured.out
