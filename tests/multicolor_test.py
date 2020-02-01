#!/usr/bin/env python3
from typing import List

from object_colors import Color


class TestMultiColor:

    def test_multi_values(
            self, color: Color, colors: List[str], for_multiple_colors: str
    ) -> None:
        rb = color.multicolor(for_multiple_colors)
        ansis = color.get_list(rb)
        for ansi in ansis:
            if Color.ansi_escape.match(ansi):
                for str_ in ansi:
                    if str_.isdigit():
                        assert int(str_) <= 7

    def test_multi_empty(self, for_multiple_colors):
        color = Color()
        rb = color.multicolor(for_multiple_colors)
        assert rb == for_multiple_colors

    def test_multi_increment(self, colors):
        args = []
        color_class = Color()
        for count, color in enumerate(colors):
            color_class.set({color: {"text": color}})
            args.append(color)
            tups = tuple(args)
            for tup in tups:
                assert hasattr(color_class, tup)
