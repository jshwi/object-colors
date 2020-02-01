#!/usr/bin/env python3
from pytest import fixture

from object_colors import Color


class TestPrint:

    def test_color_print(
            self, color: Color, red: str, capsys: fixture, reset: str
    ) -> None:
        color.red.print("This stdout is red")
        captured = capsys.readouterr()
        assert captured.out == f"{red}This stdout is red{reset}\n"

    def test_print_multi(self, capsys, long_str, codes):
        color = Color()
        color.populate_colors()
        color.print(long_str, multi=True)
        captured = capsys.readouterr()
        for code in codes:
            assert code in captured.out
