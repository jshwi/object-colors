"""
tests
=====
"""
from object_colors import Color

COLORS = Color.colors
EFFECTS = Color.effects
BACK_CODES = tuple([f"\u001b[0;37;4{i}m" for i in range(len(COLORS))])
EFFECT_CODES = tuple([f"\u001b[{i};37m" for i in range(len(EFFECTS))])
FORE_CODES = tuple([f"\u001b[0;3{i}m" for i in range(len(COLORS))])
CODE_OBJ = {"effect": EFFECT_CODES, "fore": FORE_CODES, "back": BACK_CODES}
COLOR_INT_INDEX = tuple((s, c) for c, s in enumerate(COLORS))
EFFECT_INT_INDEX = tuple((s, c) for c, s in enumerate(EFFECTS))
ATTR_KEY_VALUES = {
    "effect": EFFECT_INT_INDEX,
    "fore": COLOR_INT_INDEX,
    "back": COLOR_INT_INDEX,
}
ATTR_COLOR_EFFECT_CODE_INDEX = [
    (s, (t[i], t[1]), CODE_OBJ[s][t[1]])
    for i in (0, 1)
    for s, v in ATTR_KEY_VALUES.items()
    for t in v
]
RESET = "\u001b[0;0m"
TEST_STR = "A simple string"
TEST_TUPLE = ("A", "simple", "tuple")
