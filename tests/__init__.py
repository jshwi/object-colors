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
COLORS = Color.colors
GREEN = "\u001b[0;32;40m"
INSTANCES = tuple(["effect", "fore", "back", "bold"] + list(COLORS))
RED = "\u001b[0;31;40m"
RESET = "\u001b[0;0m"
TEST_STR = "A simple string"
