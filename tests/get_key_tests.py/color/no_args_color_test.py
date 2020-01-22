#!/usr/bin/env python3
from object_colors import Color


class TestNoArgsColor:
    def test_exact_letter_in_colored_string_color(
        self, all_colors: Color, small_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(small_color_test_string, "c")
        assert colored_keys == small_color_test_string

    def test_exact_word_in_string_color(
        self, all_colors: Color, small_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(small_color_test_string, "Cc:")
        assert colored_keys == (
            "\u001b[0;32;40m\u001b[0;31;40mCc:\u001b[0;32;40m My Business "
            "<me@mybusiness.com>;\u001b[0;0m"
        )

    def test_word_in_string_color(
        self, all_colors: Color, small_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(small_color_test_string, "cc:")
        assert colored_keys == small_color_test_string
