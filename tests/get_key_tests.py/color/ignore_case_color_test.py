#!/usr/bin/env python3
from object_colors import Color


class TestIgnoreCaseColor:
    def test_exact_word_in_string_ignore_case_color(
        self,
        all_colors: Color,
        small_color_test_string,
        marked_word_color: str,
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_color_test_string, "Cc:", case=True
        )
        assert colored_keys == marked_word_color

    def test_word_in_string_ignore_case_color(
        self,
        all_colors: Color,
        small_color_test_string,
        marked_word_color: str,
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_color_test_string, "cc:", case=True
        )
        assert colored_keys == marked_word_color
