#!/usr/bin/env python3
from object_colors import Color


class TestIgnoreCaseAndScatter:
    def test_exact_letter_in_string(
        self,
        colors: Color,
        color_str: str,
        exact_idx_color: str,
        all_cs_color: str,
    ) -> None:
        colored_keys = colors.red.get_key(
            color_str, "c", ignore_case=True, scatter=True
        )
        assert colored_keys == exact_idx_color

    def test_exact_word_in_string(
        self, colors: Color, color_str: str, marked: str, all_cs_color: str,
    ) -> None:
        colored_keys = colors.red.get_key(
            color_str, "Cc:", ignore_case=True, scatter=True
        )
        assert colored_keys == all_cs_color

    def test_word_in_string(
        self, colors: Color, color_str: str, all_cs_color: str,
    ) -> None:
        colored_keys = colors.red.get_key(
            color_str, "cc:", ignore_case=True, scatter=True
        )
        assert colored_keys == all_cs_color
