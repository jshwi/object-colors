#!/usr/bin/env python3
from object_colors import Color


class TestIgnoreCase:
    def test_exact_word_in_string_ignore_case(
        self,
        colors: Color,
        color_str: str,
        marked_color: str,
        marked: str,
        str_: str,
    ) -> None:
        keys = colors.red.get_key(str_, "Cc:", ignore_case=True)
        assert keys == marked
        colored_keys = colors.red.get_key(color_str, "Cc:", ignore_case=True)
        assert colored_keys == marked_color

    def test_word_in_string_ignore_case(
        self,
        colors: Color,
        color_str: str,
        marked_color: str,
        str_: str,
        marked: str,
    ) -> None:
        keys = colors.red.get_key(str_, "cc:", ignore_case=True)
        assert keys == marked
        colored_keys = colors.red.get_key(color_str, "cc:", ignore_case=True)
        assert colored_keys == marked_color
