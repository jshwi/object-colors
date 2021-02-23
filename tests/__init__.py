"""
tests
=====
"""
from typing import Any, Dict, List, Tuple, Union

from object_colors import Color

COLORS: Tuple[str, ...] = Color.colors
EFFECTS: Tuple[str, ...] = Color.effects
BACK_CODES: Tuple[str, ...] = tuple(
    [f"\u001b[0;37;4{i}m" for i in range(len(COLORS))]
)
EFFECT_CODES: Tuple[str, ...] = tuple(
    [f"\u001b[{i};37m" for i in range(len(EFFECTS))]
)
FORE_CODES: Tuple[str, ...] = tuple(
    [f"\u001b[0;3{i}m" for i in range(len(COLORS))]
)
CODE_OBJ: Dict[str, Tuple[str, ...]] = {
    "effect": EFFECT_CODES,
    "fore": FORE_CODES,
    "back": BACK_CODES,
}
COLOR_INT_INDEX: Tuple[Tuple[str, int], ...] = tuple(
    (s, c) for c, s in enumerate(COLORS)
)
EFFECT_INT_INDEX: Tuple[Tuple[str, int], ...] = tuple(
    (s, c) for c, s in enumerate(EFFECTS)
)
ATTR_KEY_VALUES: Dict[str, Tuple[Tuple[str, int], ...]] = {
    "effect": EFFECT_INT_INDEX,
    "fore": COLOR_INT_INDEX,
    "back": COLOR_INT_INDEX,
}
ATTR_COLOR_EFFECT_CODE_INDEX: Tuple[
    Tuple[str, Tuple[Any, int], Any], ...
] = tuple(
    [
        (s, (t[i], t[1]), CODE_OBJ[s][t[1]])
        for i in (0, 1)
        for s, v in ATTR_KEY_VALUES.items()
        for t in v
    ]
)
RESET: str = "\u001b[0;0m"
TEST_STR: str = "A simple string"
TEST_TUPLE: Tuple[str, ...] = ("A", "simple", "tuple")
MATCHED_VALUES: Dict[str, Tuple[str, ...]] = {
    "effect": EFFECTS,
    "fore": COLORS,
    "back": COLORS,
}
UNMATCHED_VALUES: Dict[str, Tuple[str, ...]] = {
    "effect": COLORS,
    "fore": EFFECTS,
    "back": EFFECTS,
}
ATTR_COLOR_EFFECT_UNMATCHED_INDEX: Tuple[Tuple[str, str], ...] = tuple(
    [(k, i) for k, v in UNMATCHED_VALUES.items() for i in v]
)
ATTR_COLOR_EFFECT_EXCEED_INDEX: Tuple[Tuple[str, int], ...] = tuple(
    [(k, len(v) + 1) for k, v in MATCHED_VALUES.items()]
)
ATTR_COLOR_EFFECT_TYPE_ERROR: Tuple[
    Union[Tuple[str, float], Tuple[str, Tuple[str]], Tuple[str, List[str]]],
    ...,
] = tuple([("effect", 1.1), ("fore", ("tuple",)), ("back", ["list"])])
