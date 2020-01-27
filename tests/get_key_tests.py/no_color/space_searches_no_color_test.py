#!/usr/bin/env python3
from object_colors import Color


def test_words_in_string(
    all_colors: Color, small_no_color_test_string, marked_word
) -> None:
    colored_keys = all_colors.red.get_key(
        small_no_color_test_string, "Cc:", "Business"
    )
    assert colored_keys == (
        "\u001b[0;31;40mCc:\u001b"
        "[0;0m My \u001b[0;31;40mBusiness\u001b[0;0m "
        "<me@mybusiness.com>;"
    )
