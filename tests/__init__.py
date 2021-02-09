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
COLORS = Color.opts["colors"].copy()
GREEN = "\u001b[0;32;40m"
RED = "\u001b[0;31;40m"
RESET = "\u001b[0;0m"
INSTANCES = ["fore", "effect", "back", "bold"] + COLORS.copy()
TEST_STR = "A simple string"
