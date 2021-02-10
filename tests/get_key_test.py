#!/usr/bin/env python3
from object_colors import Color


class TestNoArgs:
    def test_exact_letter_in_colored_string(
        self, color: Color, color_str: str, str_: str
    ) -> None:
        keys = color.red.get_key(str_, "c")
        assert keys == str_
        colored_keys = color.red.get_key(color_str, "c")
        assert colored_keys == color_str

    def test_exact_word_in_string(
        self,
        color: Color,
        color_str: str,
        marked_color: str,
        str_: str,
        color_keys: str,
        marked: str,
    ) -> None:
        keys = color.red.get_key(str_, "Cc:")
        assert keys == marked
        colored_keys = color.red.get_key(color_str, "Cc:")
        assert colored_keys == marked_color

    def test_exact_second_word_in_string(
        self,
        color: Color,
        color_str: str,
        marked_second_color: str,
        str_: str,
        marked_second: str,
    ) -> None:
        """verify indices are working (at least for some)"""
        keys = color.red.get_key(str_, "My")
        assert keys == marked_second
        colored_keys = color.red.get_key(color_str, "My")
        assert colored_keys == marked_second_color

    def test_dupe_words(
        self,
        color: Color,
        colored_dupes: str,
        dupe_marked_color: str,
        dupes: str,
        dupe_marked: str,
    ) -> None:
        keys = color.red.get_key(dupes, "one")
        assert keys == dupe_marked
        colored_keys = color.red.get_key(colored_dupes, "one")
        assert colored_keys == dupe_marked_color

    def test_word_in_string(
        self, color: Color, color_str: str, str_: str
    ) -> None:
        keys = color.red.get_key(str_, "cc:")
        assert keys == str_
        colored_keys = color.red.get_key(color_str, "cc:")
        assert colored_keys == color_str

    def test_words_in_string(
        self,
        color: Color,
        color_str: str,
        spaced_words_color: str,
        str_: str,
        spaced_words: str,
    ) -> None:
        keys = color.red.get_key(str_, "Cc:", "Business")
        assert keys == spaced_words
        colored_keys = color.red.get_key(color_str, "Cc:", "Business")
        assert colored_keys == spaced_words_color


class TestIgnoreCaseAndScatter:
    def test_exact_letter_in_string(
        self,
        color: Color,
        color_str: str,
        exact_idx_color: str,
        all_cs_color: str,
    ) -> None:
        colored_keys = color.red.get_key(
            color_str, "c", ignore_case=True, scatter=True
        )
        assert colored_keys == exact_idx_color

    def test_exact_word_in_string(
        self,
        color: Color,
        color_str: str,
        marked: str,
        all_cs_color: str,
    ) -> None:
        colored_keys = color.red.get_key(
            color_str, "Cc:", ignore_case=True, scatter=True
        )
        assert colored_keys == all_cs_color

    def test_word_in_string(
        self,
        color: Color,
        color_str: str,
        all_cs_color: str,
    ) -> None:
        colored_keys = color.red.get_key(
            color_str, "cc:", ignore_case=True, scatter=True
        )
        assert colored_keys == all_cs_color


class TestIgnoreCase:
    def test_exact_word_in_string_ignore_case(
        self,
        color: Color,
        color_str: str,
        marked_color: str,
        marked: str,
        str_: str,
    ) -> None:
        keys = color.red.get_key(str_, "Cc:", ignore_case=True)
        assert keys == marked
        colored_keys = color.red.get_key(color_str, "Cc:", ignore_case=True)
        assert colored_keys == marked_color

    def test_word_in_string_ignore_case(
        self,
        color: Color,
        color_str: str,
        marked_color: str,
        str_: str,
        marked: str,
    ) -> None:
        keys = color.red.get_key(str_, "cc:", ignore_case=True)
        assert keys == marked
        colored_keys = color.red.get_key(color_str, "cc:", ignore_case=True)
        assert colored_keys == marked_color


class TestScatter:
    def test_exact_letter_in_string(
        self,
        color: Color,
        color_str: str,
        str_: str,
        scatter_cs_exact_color: str,
        scatter_cs_exact: str,
    ) -> None:
        keys = color.red.get_key(str_, "c", scatter=True)
        assert keys == scatter_cs_exact
        colored_keys = color.red.get_key(color_str, "c", scatter=True)
        assert colored_keys == scatter_cs_exact_color

    def test_exact_word_in_string(
        self,
        color: Color,
        color_str: str,
        marked: str,
        scatter_cs_color: str,
        str_: str,
        scatter_cs: str,
    ) -> None:
        keys = color.red.get_key(str_, "Cc:", scatter=True)
        assert keys == scatter_cs
        colored_keys = color.red.get_key(color_str, "Cc:", scatter=True)
        assert colored_keys == scatter_cs_color

    def test_word_in_string(
        self,
        color: Color,
        color_str: str,
        all_cs_no_caps,
        all_cs_no_caps_color,
        str_: str,
    ) -> None:
        keys = color.red.get_key(str_, "cc:", scatter=True)
        assert keys == all_cs_no_caps
        colored_keys = color.red.get_key(color_str, "cc:", scatter=True)
        assert colored_keys == all_cs_no_caps_color
