#!/usr/bin/env python3

from object_colors import Color


class TestPopulateColors:
    def test_populated(self, colors):
        color = Color()
        color.populate_colors()
        contents = color.__dict__
        result = False
        bool_list = []
        colors.pop(0)
        for count, color in enumerate(colors):
            for key in contents:
                result = key == color
            if result:
                bool_list.append(result)
        for result in bool_list:
            assert result
