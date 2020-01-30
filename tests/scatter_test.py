#!/usr/bin/env python3
from object_colors import Color


class TestScatter:
    def test_exact_letter_in_string(
        self,
        colors: Color,
        color_str: str,
        str_: str,
        scatter_cs_exact_color,
        scatter_cs_exact,
    ) -> None:
        keys = colors.red.get_key(str_, "c", scatter=True)
        assert keys == scatter_cs_exact
        colored_keys = colors.red.get_key(color_str, "c", scatter=True)
        assert colored_keys == scatter_cs_exact_color

    def test_exact_word_in_string(
        self,
        colors: Color,
        color_str: str,
        marked: str,
        scatter_cs_color: str,
        str_: str,
        scatter_cs: str,
    ) -> None:
        keys = colors.red.get_key(str_, "Cc:", scatter=True)
        assert keys == scatter_cs
        colored_keys = colors.red.get_key(color_str, "Cc:", scatter=True)
        assert colored_keys == scatter_cs_color

    def test_word_in_string(
        self,
        colors: Color,
        color_str: str,
        all_cs_no_caps,
        all_cs_no_caps_color,
        str_: str,
    ) -> None:
        keys = colors.red.get_key(str_, "cc:", scatter=True)
        assert keys == all_cs_no_caps
        colored_keys = colors.red.get_key(color_str, "cc:", scatter=True)
        assert colored_keys == all_cs_no_caps_color
