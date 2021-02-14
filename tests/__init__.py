"""
tests
=====
"""
from object_colors import Color

ATTRS = (
    "get",
    "set",
    "get",
    "get_key",
    "print",
    "print_key",
    "pop",
    "multicolor",
    "populate_colors",
)
CODES = tuple([f"\u001b[0;3{i}m" for i in range(7)])
COLORS = Color.colors
INSTANCES = tuple(["effect", "fore", "back", "bold"] + list(COLORS))
RESET = "\u001b[0;0m"
TEST_STR = "A simple string"
TEST_TUPLE = ("A", "simple", "tuple")
