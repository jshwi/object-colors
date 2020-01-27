#!/usr/bin/env python3
from object_colors import Color


def test_words_in_string_color(
    all_colors: Color, small_color_test_string
) -> None:
    colored_keys = all_colors.red.get_key(
        small_color_test_string, "Cc:", "Business"
    )
    assert colored_keys == (
        "\u001b[0;32;40m\u001b[0;31;40mCc:\u001b[0;32;40m My "
        "\u001b[0;31;40mBusiness\u001b[0;32;40m "
        "<me@mybusiness.com>;\u001b[0;0m"
    )
