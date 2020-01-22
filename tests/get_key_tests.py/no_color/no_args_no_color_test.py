#!/usr/bin/env python3
from object_colors import Color


class TestNoArgsNoColorNoColor:
    def test_exact_letter_in_string(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(small_no_color_test_string, "c")
        assert colored_keys == small_no_color_test_string

    def test_exact_word_in_string(
        self, all_colors: Color, small_no_color_test_string, marked_word: str
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "Cc:"
        )
        assert colored_keys == marked_word

    def test_exact_second_word_in_string(
        self,
        all_colors: Color,
        small_no_color_test_string,
        marked_second_word: str,
    ) -> None:
        colored_keys = all_colors.red.get_key(small_no_color_test_string, "My")
        assert colored_keys == marked_second_word

    def test_word_in_string(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "cc:"
        )
        assert colored_keys == small_no_color_test_string
