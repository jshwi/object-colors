#!/usr/bin/env python3


class TestGet:
    def test_tuple_return(self, color):
        tup = color.red.get("t", "u", "p")
        assert tup == (
            "\u001b[0;31;40mt\u001b[0;0m",
            "\u001b[0;31;40mu\u001b[0;0m",
            "\u001b[0;31;40mp\u001b[0;0m",
        )
