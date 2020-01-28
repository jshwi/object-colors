#!/usr/bin/env python3
from object_colors import Color


def test_words_in_string_color(colors, color_str) -> None:
    colored_keys = colors.red.get_key(color_str, "Cc:", "Business")
    assert colored_keys == (
        "\u001b[0;32;40m\u001b[0;31;40mCc:\u001b[0;32;40m My "
        "\u001b[0;31;40mBusiness\u001b[0;32;40m "
        "<me@mybusiness.com>;\u001b[0;0m"
    )
