#!/usr/bin/env python3
from object_colors import Color


def test_words_in_string(colors, str_, marked) -> None:
    colored_keys = colors.red.get_key(str_, "Cc:", "Business")
    assert colored_keys == (
        "\u001b[0;31;40mCc:\u001b"
        "[0;0m My \u001b[0;31;40mBusiness\u001b[0;0m "
        "<me@mybusiness.com>;"
    )
