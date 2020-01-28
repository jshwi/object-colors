#!/usr/bin/env python3
from object_colors import Color


class TestScatterColor:
    def test_exact_letter_in_string(
        self,
        colors: Color,
        color_str: str,
        all_cs_color: str,
        all_cs: str,
        str_: str,
    ) -> None:
        keys = colors.red.get_key(str_, "c", any_=True)
        assert keys == all_cs
        colored_keys = colors.red.get_key(color_str, "c", any_=True)
        assert colored_keys == all_cs_color

    def test_exact_word_in_string(
        self,
        colors: Color,
        color_str: str,
        marked: str,
        scatter_cs_color: str,
        str_: str,
        scatter_cs: str,
    ) -> None:
        keys = colors.red.get_key(str_, "Cc:", any_=True)
        assert keys == scatter_cs
        colored_keys = colors.red.get_key(color_str, "Cc:", any_=True)
        assert colored_keys == scatter_cs_color

    def test_word_in_string(
        self,
        colors: Color,
        color_str: str,
        scatter_cs_exact_color: str,
        str_: str,
        scatter_cs_exact: str,
    ) -> None:
        keys = colors.red.get_key(str_, "cc:", any_=True)
        assert keys == scatter_cs_exact
        colored_keys = colors.red.get_key(color_str, "cc:", any_=True)
        assert colored_keys == scatter_cs_exact_color
