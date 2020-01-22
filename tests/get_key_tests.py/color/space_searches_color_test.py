#!/usr/bin/env python3
from object_colors import Color


class TestSpacedSearchesColor:
    def test_exact_word_in_string_color(
        self,
        all_colors: Color,
        small_color_test_string,
        marked_word_color: str,
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_color_test_string, ["C", "c", ":"]
        )
        assert colored_keys == marked_word_color

    def test_word_in_string_color(
        self, all_colors: Color, small_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_color_test_string, ["c", "c", ":"]
        )
        assert colored_keys == small_color_test_string

    def test_word_in_string_ignore_case_color(
        self, all_colors: Color, small_color_test_string, marked_word_color
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_color_test_string, ["c", "c", ":"], case=True
        )
        assert colored_keys == marked_word_color

    def test_words_in_string_color(
        self, all_colors: Color, small_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_color_test_string, ["Cc:", "Business"]
        )
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b"
            "[0;0m My \u001b[0;31;40mBusiness\u001b[0;0m "
            "<me@mybusiness.com>;"
        )
