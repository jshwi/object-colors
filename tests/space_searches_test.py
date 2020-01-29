#!/usr/bin/env python3
from object_colors import Color


def test_words_in_string(
    colors: Color,
    color_str: str,
    spaced_words_color: str,
    str_: str,
    spaced_words: str,
) -> None:
    keys = colors.red.get_key(str_, "Cc:", "Business")
    assert keys == spaced_words
    colored_keys = colors.red.get_key(color_str, "Cc:", "Business")
    assert colored_keys == spaced_words_color
