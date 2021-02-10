#!/usr/bin/env python3

from object_colors import Color


class TestMultiColor:
    def test_multi_values(self, color, colors, long_str):
        rb = color.multicolor(long_str)
        ansis = color.get_list(rb)
        for ansi in ansis:
            if Color.ansi_escape.match(ansi):
                for str_ in ansi:
                    if str_.isdigit():
                        assert int(str_) <= 7

    def test_multi_empty(self, long_str):
        color = Color()
        rb = color.multicolor(long_str)
        assert rb == long_str

    def test_multi_increment(self, colors):
        args = []
        color_class = Color()
        for count, color in enumerate(colors):
            color_class.set({color: {"text": color}})
            args.append(color)
            tups = tuple(args)
            for tup in tups:
                assert hasattr(color_class, tup)

    def test_none(self, long_str):
        color = Color(text="green")
        none = color.multicolor(long_str)
        print(none)
        assert none == long_str

    def test_green_and_none(self, long_str):
        color = Color()
        color.set(green={"text": "green"})
        green_and_none = color.multicolor(long_str)
        print(green_and_none)
        assert "0;32;40m" in green_and_none

    def test_green_red_none(self, long_str):
        color = Color()
        codes = ["0;31;40m", "0;32;40m"]
        color.set(green={"text": "green"})
        color.set(red={"text": "red"})
        green_red_none = color.multicolor(long_str)
        for code in codes:
            assert code in green_red_none

    def test_with_populated_colors(self, long_str, codes):
        populate = Color()
        populate.populate_colors()
        all_colors = populate.multicolor(long_str)
        for code in codes:
            assert code in all_colors
