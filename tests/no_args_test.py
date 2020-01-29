#!/usr/bin/env python3
from object_colors import Color


class TestNoArgs:
    def test_exact_letter_in_colored_string(
        self, colors: Color, color_str: str, str_: str
    ) -> None:
        keys = colors.red.get_key(str_, "c")
        assert keys == str_
        colored_keys = colors.red.get_key(color_str, "c")
        assert colored_keys == color_str

    def test_exact_word_in_string(
        self,
        colors: Color,
        color_str: str,
        marked_color: str,
        str_: str,
        color_keys: str,
        marked: str,
    ) -> None:
        keys = colors.red.get_key(str_, "Cc:")
        assert keys == marked
        colored_keys = colors.red.get_key(color_str, "Cc:")
        assert colored_keys == marked_color

    def test_exact_second_word_in_string(
        self,
        colors: Color,
        color_str: str,
        marked_second_color: str,
        str_: str,
        marked_second: str,
    ) -> None:
        """verify indices are working (at least for some)"""
        keys = colors.red.get_key(str_, "My")
        assert keys == marked_second
        colored_keys = colors.red.get_key(color_str, "My")
        assert colored_keys == marked_second_color

    def test_dupe_words(
        self,
        colors: Color,
        colored_dupes: str,
        dupe_marked_color,
        dupes,
        dupe_marked,
    ) -> None:
        keys = colors.red.get_key(dupes, "one")
        assert keys == dupe_marked
        colored_keys = colors.red.get_key(colored_dupes, "one")
        assert colored_keys == dupe_marked_color

    def test_word_in_string(
        self, colors: Color, color_str: str, str_: str
    ) -> None:
        keys = colors.red.get_key(str_, "cc:")
        assert keys == str_
        colored_keys = colors.red.get_key(color_str, "cc:")
        assert colored_keys == color_str
