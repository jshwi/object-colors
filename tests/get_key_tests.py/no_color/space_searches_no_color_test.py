#!/usr/bin/env python3
from object_colors import Color


class TestSpacedSearchesNoColor:
    def test_exact_word_in_string(
        self, all_colors: Color, small_no_color_test_string, marked_word: str
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["C", "c", ":"]
        )
        assert colored_keys == marked_word

    def test_word_in_string(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["c", "c", ":"]
        )
        assert colored_keys == small_no_color_test_string

    def test_word_in_string_ignore_case(
        self, all_colors: Color, small_no_color_test_string, marked_word
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["c", "c", ":"], case=True
        )
        assert colored_keys == marked_word

    def test_words_in_string(
        self, all_colors: Color, small_no_color_test_string, marked_word
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, ["Cc:", "Business"]
        )
        assert colored_keys == (
            "\u001b[0;31;40mCc:\u001b"
            "[0;0m My \u001b[0;31;40mBusiness\u001b[0;0m "
            "<me@mybusiness.com>;"
        )
