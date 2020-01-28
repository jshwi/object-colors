#!/usr/bin/env python3

from object_colors import Color


class TestIgnoreCaseAndScatter:
    def test_exact_letter_in_string(
        self,
        colors: Color,
        str_,
        color_str: str,
        all_cs: str,
        exact_idx: str,
        exact_idx_color: str,
    ) -> None:
        keys = colors.red.get_key(str_, "c", case=True, any_=True)
        color_keys = colors.red.get_key(color_str, "c", case=True, any_=True)
        assert keys == exact_idx
        assert color_keys == exact_idx_color

    def test_exact_word_in_string(
        self,
        colors: Color,
        str_: str,
        marked: str,
        all_cs: str,
        color_str: str,
        all_cs_color: str,
    ) -> None:
        keys = colors.red.get_key(str_, "Cc:", case=True, any_=True)
        color_keys = colors.red.get_key(color_str, "Cc:", case=True, any_=True)
        assert keys == all_cs
        assert color_keys == all_cs_color

    def test_word_in_string(
        self,
        colors: Color,
        str_: str,
        color_str: str,
        all_cs: str,
        all_cs_color: str,
    ) -> None:
        keys = colors.red.get_key(str_, "cc:", case=True, any_=True)
        assert keys == all_cs
        colored_keys = colors.red.get_key(
            color_str, "cc:", case=True, any_=True
        )
        assert colored_keys == all_cs_color
