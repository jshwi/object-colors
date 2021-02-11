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
CODES = (
    "0;31;40m",
    "0;32;40m",
    "0;33;40m",
    "0;34;40m",
    "0;35;40m",
    "0;36;40m",
    "0;37;40m",
)
COLORED_DUPES = (
    "\u001b[0;32;40mThis is a string that says one several times. It says "
    "one in this sentence. And one in this sentence. This sentence also "
    "has one in it. Lastly this sentence will also say one\u001b[0;0m"
)
COLORS = Color.opts["colors"].copy()
DUPES = (
    "This is a string that says one several times. It says one in this "
    "sentence. And one in this sentence. This sentence also has one in "
    "it. Lastly this sentence will also say one"
)
GREEN = "\u001b[0;32;40m"
RED = "\u001b[0;31;40m"
RESET = "\u001b[0;0m"
DUPE_MARKED = (
    f"This is a string that says {RED}one{RESET} several times. It says "
    f"{RED}one{RESET} in this sentence. And {RED}one{RESET} in this "
    f"sentence. This sentence also has {RED}one{RESET} in it. Lastly this "
    f"sentence will also say {RED}one{RESET}"
)
DUPE_MARKED_COLOR = (
    f"{GREEN}This is a string that says {RED}one{GREEN} several times. "
    f"It says {RED}one{GREEN} in this sentence. And {RED}one{GREEN} in "
    f"this sentence. This sentence also has {RED}one{GREEN} in it. Lastly "
    f"this sentence will also say {RED}one{GREEN}{RESET}"
)
EXACT_INDEX_COLOR = (
    f"{GREEN}{RED}C{GREEN}{RED}c{GREEN}: My Business "
    f"<me@mybusiness.{RED}c{GREEN}om>;{RESET}"
)
INSTANCES = ["text", "effect", "background", "bold"] + COLORS.copy()
LONG_STRING = (
    "Beautiful is better than ugly."
    "Explicit is better than implicit."
    "Simple is better than complex."
    "Complex is better than complicated."
    "Flat is better than nested."
    "Sparse is better than dense."
    "Readability counts."
    "Special cases aren't special enough to break the rules."
    "Although practicality beats purity."
    "Errors should never pass silently."
    "Unless explicitly silenced."
    "In the face of ambiguity, refuse the temptation to guess."
    "There should be one-- and preferably only one --obvious way to do it."
    "Although that way may not be obvious at first unless you're Dutch."
    "Now is better than never."
    "Although never is often better than *right* now."
    "If the implementation is hard to explain, it's a bad idea."
    "If the implementation is easy to explain, it may be a good idea."
    "Namespaces are one honking great idea -- let's do more of those!"
)
MARKED = f"{RED}Cc:{RESET} My Business <me@mybusiness.com>;"
MARKED_COLOR = (
    f"{GREEN}{RED}Cc:{GREEN} My Business <me@mybusiness.com>;{RESET}"
)
MARKED_SECOND = f"Cc: {RED}My{RESET} Business <me@mybusiness.com>;"
MARKED_SECOND_COLOR = (
    f"{GREEN}Cc: {RED}My{GREEN} Business <me@mybusiness.com>;{RESET}"
)
SPACED_WORDS = f"{RED}Cc:{RESET} My {RED}Business{RESET} <me@mybusiness.com>;"
SPACED_WORDS_COLOR = (
    f"{GREEN}{RED}Cc:{GREEN} My {RED}Business{GREEN} "
    f"<me@mybusiness.com>;{RESET}"
)
TEST_STR = "Cc: My Business <me@mybusiness.com>;"
