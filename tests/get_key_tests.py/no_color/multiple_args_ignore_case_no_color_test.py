#!/usr/bin/env python3
from object_colors import Color


class TestMultipleArgsNoColor:
    def test_exact_word_in_string_ignore_case(
        self, all_colors: Color, small_no_color_test_string, marked_word: str
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["C", "c", ":"], case=True
        )
        assert colored_keys == marked_word

    def test_word_in_string_ignore_case(
        self, all_colors: Color, small_no_color_test_string, marked_word: str
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["c", "c", ":"], case=True
        )
        assert colored_keys == marked_word
