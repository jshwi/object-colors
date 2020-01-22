#!/usr/bin/env python3
from object_colors import Color


class TestScatterNoColor:
    def test_exact_letter_in_string(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "c", any_=True
        )
        assert colored_keys == (
            "C\u001b[0;31;40mc\u001b[0;0m: My Business "
            "<me@mybusiness.\u001b[0;31;40mc\u001b[0;0mom>;"
        )

    def test_exact_word_in_string(
        self, all_colors: Color, small_no_color_test_string, marked_word: str
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "Cc:", any_=True
        )
        assert colored_keys == (
            "\u001b[0;31;40mC\u001b[0;0m\u001b[0;31;40mc\u001b[0;0m"
            "\u001b[0;31;40m:\u001b[0;0m My Business <me@mybusiness."
            "\u001b[0;31;40mc\u001b[0;0mom>;"
        )

    def test_word_in_string(
        self, all_colors: Color, small_no_color_test_string
    ) -> None:
        colored_keys = all_colors.red.get_key(
            small_no_color_test_string, "cc:", any_=True
        )
        assert colored_keys == (
            "C\u001b[0;31;40mc\u001b[0;0m"
            "\u001b[0;31;40m:\u001b[0;0m My Business <me@mybusiness."
            "\u001b[0;31;40mc\u001b[0;0mom>;"
        )
