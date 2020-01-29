#!/usr/bin/env python3
from pytest import fixture

from object_colors import Color


@fixture
def colors():
    return Color(populate=True)


@fixture
def color_str(colors, str_):
    return colors.green.get(str_)


@fixture
def str_():
    return "Cc: My Business <me@mybusiness.com>;"


@fixture
def marked(red, reset):
    return f"{red}Cc:{reset} My Business <me@mybusiness.com>;"


@fixture
def marked_color(green, red, reset):
    return f"{green}{red}Cc:{green} My Business <me@mybusiness.com>;{reset}"


@fixture
def marked_second(red, reset):
    return f"Cc: {red}My{reset} Business <me@mybusiness.com>;"


@fixture
def marked_second_color(green, red, reset):
    return f"{green}Cc: {red}My{green} Business <me@mybusiness.com>;{reset}"


@fixture
def all_cs(red, reset):
    return (
        f"{red}C{reset}{red}c{reset}{red}:{reset} My "
        f"Business <me@mybusiness.{red}c{reset}om>;"
    )


@fixture
def dupe_marked_color(green, red, reset):
    """do dupe fixture but with ignore"""
    return (
        f"{green}This is a string that says {red}one{green} several times. "
        f"It says {red}one{green} in this sentence. And {red}one{green} in "
        f"this sentence. This sentence also has {red}one{green} in it. Lastly "
        f"this sentence will also say {red}one{green}{reset}"
    )


@fixture
def dupe_marked(green, red, reset):
    """do dupe fixture but with ignore"""
    return (
        f"This is a string that says {red}one{reset} several times. It says "
        f"{red}one{reset} in this sentence. And {red}one{reset} in this "
        f"sentence. This sentence also has {red}one{reset} in it. Lastly this "
        f"sentence will also say {red}one{reset}"
    )


@fixture
def all_cs_color(red, green, reset):
    return (
        f"{green}{red}C{green}{red}c{green}{red}:{green} My "
        f"Business <me@mybusiness.{red}c{green}om>;{reset}"
    )


@fixture
def all_cs_no_caps(red, reset):
    return (
        f"C{red}c{reset}{red}:{reset} My "
        f"Business <me@mybusiness.{red}c{reset}om>;"
    )


@fixture
def all_cs_no_caps_color(red, green, reset):
    return (
        f"{green}C{red}c{green}{red}:{green} My "
        f"Business <me@mybusiness.{red}c{green}om>;{reset}"
    )


@fixture
def exact_idx(red, reset):
    return (
        f"{red}C{reset}{red}c{reset}: My Business "
        f"<me@mybusiness.{red}c{reset}om>;"
    )


@fixture
def exact_idx_color(green, red, reset):
    return (
        f"{green}{red}C{green}{red}c{green}: My Business "
        f"<me@mybusiness.{red}c{green}om>;{reset}"
    )


@fixture
def dupes():
    return (
        "This is a string that says one several times. It says one in this "
        "sentence. And one in this sentence. This sentence also has one in "
        "it. Lastly this sentence will also say one"
    )


@fixture
def colored_dupes():
    return (
        "\u001b[0;32;40mThis is a string that says one several times. It says "
        "one in this sentence. And one in this sentence. This sentence also "
        "has one in it. Lastly this sentence will also say one\u001b[0;0m"
    )


@fixture
def scatter_cs(green, red, reset):
    return (
        f"{red}C{reset}{red}c{reset}{red}:{reset} My Business "
        f"<me@mybusiness.{red}c{reset}om>;"
    )


@fixture
def scatter_cs_color(green, red, reset):
    return (
        f"{green}{red}C{green}{red}c{green}{red}:{green} My Business "
        f"<me@mybusiness.{red}c{green}om>;{reset}"
    )


@fixture
def scatter_cs_exact(green, red, reset):
    return (
        f"C{red}c{reset}: My Business <me@mybusiness.{red}c"
        f"{reset}om>;"
    )


@fixture
def scatter_cs_exact_color(green, red, reset):
    return (
        f"{green}C{red}c{green}: My Business "
        f"<me@mybusiness.{red}c{green}om>;{reset}"
    )


@fixture
def spaced_words(green, red, reset):
    return f"{red}Cc:{reset} My {red}Business{reset} <me@mybusiness.com>;"


@fixture
def spaced_words_color(green, red, reset):
    return (
        f"{green}{red}Cc:{green} My {red}Business{green} "
        f"<me@mybusiness.com>;{reset}"
    )


@fixture
def green():
    return "\u001b[0;32;40m"


@fixture
def red():
    return "\u001b[0;31;40m"


@fixture
def reset():
    return "\u001b[0;0m"


@fixture
def color_keys(colors, str_):
    return colors.red.get_key(str_, "c", case=True, any_=True)
