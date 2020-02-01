#!/usr/bin/env python3
"""object-colors
The Python Color Dictionary

A simple to use class module designed to stylise output with minimal
setup and instantiation
"""
from __future__ import annotations

import re
from random import randint
from typing import Union, Any, Optional, Tuple, Dict, List


class Color:
    """
    Instantiate object with attributes to use...

    >>> from object_colors import Color

    >>> str_ = "Sample string"

    >>> color = Color(text="green")

    >>> color_str = color.get(str_)
    >>> print(color_str)
    \u001b[0;32;40mSample string\u001b[0;0m

    ...or set attributes after instantiation

    >>> color.set(subclass={"text": "red"})

    >>> substr = color.subclass.get_key(str_, "Sample")
    >>> print(substr)
    \u001b[0;31;40mSample\u001b[0;0m string

    >>> green_substr = color.subclass.get_key(color_str, "Sample")
    >>> print(green_substr)  # doctest +ELLIPSIS
    \u001b[0;32;40m\u001b[0;31;40mSample\u001b[0;32;40m string\u001b[...


    Pop objects from `color.__dict__`

    >>> subclass = color.pop("subclass")

    >>> substr = subclass.get_key(str_, "Sample")
    >>> print(substr)
    \u001b[0;31;40mSample\u001b[0;0m string

    Print colored strings directly

    >>> color.print(str_)
    \u001b[0;32;40mSample string\u001b[0;0m

    >>> color.print_key(str_, "string")
    Sample \u001b[0;32;40mstring\u001b[0;0m

    Set attributes in instance with flexible arguments

    >>> # keywords
    >>> color.set(text="blue", effect="bold", background="red")
    >>> print(color.__dict__)  # doctest +ELLIPSIS
    {'text': 4, 'effect': 1, 'background': 1, 'bold': <object_colors...}

    >>> # args (string)
    >>> color.set("blue", "bold", "red")
    >>> print(color.__dict__)  # doctest +ELLIPSIS
    {'text': 4, 'effect': 1, 'background': 1, 'bold': <object_colors...}

    >>> # args (tuple)
    >>> color.set(4, 1, 1)
    >>> print(color.__dict__)  # doctest +ELLIPSIS
    {'text': 4, 'effect': 1, 'background': 1, 'bold': <object_colors...}

    >>> # args (integer)
    >>> color.set(411)
    >>> print(color.__dict__)  # doctest +ELLIPSIS
    {'text': 4, 'effect': 1, 'background': 1, 'bold': <object_colors...}

    Set attributes in object instance's subclasses

    >>> color.set(red={"text": "red", "effect": "bold"})
    >>> color.red.print("Red string")
    \u001b[1;31;40mRed string\u001b[0;0m

    >>> color.set(blue={"text": "blue", "effect": "bold"})
    >>> color.blue.print("Blue string")
    \u001b[1;34;40mBlue string\u001b[0;0m

    Populate instance with subclasses for all colors

    >>> color.populate_colors()

    >>> color.green.print("Green string")
    \u001b[0;32;40mGreen string\u001b[0;0m

    >>> color.cyan.print("Cyan string")
    \u001b[0;36;40mCyan string\u001b[0;0m
    >>> # etc...

    Easily switch between bold text

    >>> color.purple.bold.print("Bold purple string")
    \u001b[1;35;40mBold purple string\u001b[0;0m

    :cvar code:         Ansi escape code
    :type code:         str
    :cvar reset:        Default reset code to switch off color for str
    :type reset:        str
    :cvar ansi_escape:  Regex for finding ansi escape codes in strings
    :type ansi_escape:  Pattern[str]
    """

    __keys = ["text", "effect", "background"]
    __opts = {
        "colors": [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "purple",
            "cyan",
            "white",
        ],
        "effect": ["none", "bold", "bright", "underline", "negative"],
    }

    code = "\u001b"
    reset = f"{code}[0;0m"
    ansi_escape = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")

    def __init__(self, *args: Union[str, int], **kwargs: Any) -> None:
        self.text = 7
        self.effect = 0
        self.background = 0
        self.set(*args, **kwargs)

    def __getattr__(self, item: str) -> str:
        # look up dynamic subclasses
        return item

    def __dir__(self) -> List[str]:
        # primarily here so linters know that the subclass calling
        # methods are not strings strings attempting to call attributes
        return [str(item) for item in self.__dict__]

    @staticmethod
    def __collect_values(
            value: Union[int, Color],
            key: str,
            colors: Dict[str, List[Union[Color, int]]],
    ) -> Dict[str, List[Union[Color, int]]]:
        # determine that value is a subclass before adding it to the
        # object to avoid TypeErrors
        if not isinstance(value, int) and key not in ("bold", "black"):
            colors["classes"].append(value)
            colors["code"].append(value.text)
        return colors

    def __dummy_subclass(self) -> Color:
        # populate class with white subclass
        kwargs = {"white": {"text": 7}}
        self.__make_subclass((), kwargs)
        return self.__dict__["white"]

    def __get_default(
            self, colors: Union[
                Dict[str, list], Dict[str, List[Union[Color, int]]]
            ]
    ) -> Union[Dict[str, list], Dict[str, List[Union[Color, int]]]]:
        # if no white class is present, or no classes are present at
        # all, add to dictionary to keep multicolor method running with
        # some variance for lower numbers of classes
        if "white" not in colors["classes"]:
            white = self.__dummy_subclass()
            colors["classes"].append(white)
            colors["code"].append(white.text)
        return colors

    def __get_multi_object(self) -> Dict[str, Union[str, list]]:
        # get an object consisting of available color codes to be
        # randomized and available subclasses to match against
        # randomized codes
        colors = {"code": [], "classes": []}
        for key, value in self.__dict__.items():
            colors = self.__collect_values(value, key, colors)
        colors = self.__get_default(colors)
        colors["code"] = list(dict.fromkeys(colors["code"]))
        return colors

    @staticmethod
    def __validate_code(
            colors: Union[Dict[str, list], Dict[str, List[Union[Color, int]]]],
            code: int,
            letter: str,
            full_str: List[str]
    ) -> List[str]:
        # match the ansi escape code against randomized number to be
        # used to color string index
        for class_ in colors["classes"]:
            if class_.text == code:
                idx = class_.get(letter)
                full_str.append(idx)
                break
        return full_str

    def __get_multi_str(
            self, str_: str, colors: Dict[str, Union[str, list]]
    ) -> str:
        # compile and return the string colored by a randomized
        # assortment of colors present with the available subclasses
        full_str = []
        if len(colors["classes"]) == 1:
            return str_
        max_ = len(colors["code"]) - 1
        for count, _ in enumerate(str_):
            letter = str_[count]
            idx = randint(0, max_)
            code = colors["code"][idx]
            full_str = self.__validate_code(colors, code, letter, full_str)
        return "".join(full_str)

    def __get_colored_tuple(
            self, args: Tuple[Union[str, int]], reset: str
    ) -> Tuple[Union[str, int]]:
        args = list(args)
        # replace tuples containing strings with corresponding colored
        # strings
        for count, arg in enumerate(args):
            args[count] = self.__get_colored_str(arg, reset)
        return tuple(args)

    def __color_settings(self) -> str:
        # get the colored string with ansi-escape code settings added
        return f"{Color.code}[{self.effect};3{self.text};4{self.background}m"

    def __get_colored_str(self, str_: str, reset: str) -> str:
        # set desired reset code and return colored string
        reset = reset if reset else ""
        setting = self.__color_settings()
        return f"{setting}{str_}{reset}"

    @staticmethod
    def __extract_codes(
            word: str, helper: Dict[str, Union[str, int]]
    ) -> Dict[str, Union[str, int]]:
        # ints represent the ansi code index within the string
        # This function looks to retrieve an ansi code - rather than
        # create one - to be used again later in the `helper` subclass
        codes = {"text": 5, "effect": 2, "background": 8}
        for key, value in codes.items():
            helper.update({key: int(word[value])})
        return helper

    def __populate_state_object(
            self,
            word: str,
            name_: str,
            state: Dict[str, Union[Dict[str, str], List[str]]],
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        # separate ansi codes from string and return a dict of both to
        # be used individually later
        if Color.ansi_escape.match(word):
            if word != Color.reset:
                codes = self.__extract_codes(word, {})
                state[name_].update(codes)
        else:
            state["str_"].append(word)
        return state

    def __get_state_object(
            self, words: List[str], name_: str
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        # iterate string split up by ansi escape codes to populate
        # object to organise them
        state = {name_: {}, "str_": []}
        for word in words:
            state = self.__populate_state_object(word, name_, state)
        state["str_"] = "".join(state["str_"])
        return state

    @staticmethod
    def __get_opts(key: str) -> List[str]:
        # get list of values to represent ansi escape codes whether
        # colors are needed or effects are needed
        if key in Color.__opts:
            return Color.__opts[key]
        return Color.__opts["colors"]

    def __resolve_ansi_code(
            self, keys: Tuple[str], str_: str, switches: Dict[str, bool]
    ) -> str:
        # separate ansi escape codes from ansi coded string
        # create the `helper` subclass and return the bare string
        # reset code will return strings after the colored keys as their
        # original ansi code color
        # color the keywords entered as *args
        # surround the string with its original color
        # remove the helper function and return colored string
        str_ = self.set_str(str_)
        reset = self.helper.get("", reset=None)
        str_ = self.__process_str(keys, str_, reset, switches)
        str_ = self.helper.get(str_)
        del self.__dict__["helper"]
        return str_

    @staticmethod
    def __get_swapped_index(
            switches: Dict[str, bool], letter: str, idx: List[str]
    ) -> List[str]:
        # add additional swapped case of string index for scatter mode
        # to catch all instances of occurring substring when ignore case
        # is also active
        if switches["case"] and letter.isalnum():
            idx.append(letter.swapcase())
        return idx

    def __get_str_indices(
            self, key: str, switches: Dict[str, bool]
    ) -> List[str]:
        # separate all characters into individual indices to be
        # individually run against main string for substrings
        idx = []
        key = list(key)
        for letter in key:
            idx.append(letter)
            idx = self.__get_swapped_index(switches, letter, idx)
        return list(dict.fromkeys(idx))

    @staticmethod
    def __normalize_strs(
            key: str, str_: str, switches: Dict[str, bool]
    ) -> Dict[str, str]:
        # ignore case of the searched string by searching lowercase
        # substring in lowercase string
        strs = {"str_": str_, "key": key}
        if switches["case"]:
            strs.update({"str_": str_.lower(), "key": key.lower()})
        return strs

    @staticmethod
    def __get_multiple_positions(
            key: str, str_: str, pos: List[int]
    ) -> List[int]:
        # generator will be needed if there are multiple positions of a
        # single substring
        places = [p for p in range(len(str_)) if str_.find(key, p) == p]
        for place in places:
            pos.append(place)
        return pos

    def __find_key_positions(
            self, strs: Dict[str, str], pos: List[int]
    ) -> List[int]:
        # find the position of keywords(s) and return list of results
        key = strs["key"]
        str_ = strs["str_"]
        if f" {key} " in f" {str_} ":
            pos = self.__get_multiple_positions(key, str_, pos)
        return pos

    @staticmethod
    def __iterate_theirs(
            letter: str, ours: str, pos: List[int], count: int
    ) -> List[int]:
        # iterate through either a full string or just once against a
        # single index and check whether the search is successful
        # if it is then append the count (index) of the main string to
        # the list of index positions
        for theirs in letter:
            if ours == theirs:
                pos.append(count)
        return pos

    def __iterate_ours(
            self, idx: List[str], str_: str, pos: List[int], count: int
    ) -> List[int]:
        # get letter of string according to enumeration in main loop
        # and iterate string we want to search with string we are
        # searching against
        letter = str_[count]
        for ours in idx:
            pos = self.__iterate_theirs(letter, ours, pos, count)
        return pos

    def __get_scattered_positions(
            self, str_: str, idx: List[str], pos: List[int]
    ) -> List[int]:
        # get the scattered position of searched keys within string
        for count, _ in enumerate(str_):
            pos = self.__iterate_ours(idx, str_, pos, count)
        return pos

    @staticmethod
    def __update_str_object(
            freeze: int,
            letter: str,
            obj: Dict[str, Union[int, str, bool, List[str]]]
    ) -> Dict[str, Union[int, str, bool, List[str]]]:
        # update the object keeping track of various statuses through
        # the color string iteration
        obj.update({"freeze": freeze, "letter": letter, "applied": True})
        obj["pos"].pop(0)
        return obj

    def __get_key_positions(
            self,
            str_: str,
            key: str,
            pos: List[int],
            switches: Dict[str, bool]
    ) -> List[int]:
        # get position(s) of searched term as an integer within string
        strs = self.__normalize_strs(key, str_, switches)
        return self.__find_key_positions(strs, pos)

    def __normalize_position(
            self,
            key: str,
            str_: str,
            pos: List[int],
            switches: Dict[str, bool]
    ) -> List[int]:
        # return list of search positions for scattered keys if
        # `scatter` is True or return colored full words if False
        if switches["any"]:
            idx = self.__get_str_indices(key, switches)
            return self.__get_scattered_positions(str_, idx, pos)
        return self.__get_key_positions(str_, key, pos, switches)

    @staticmethod
    def __str_object(pos: List[int]) -> Dict[str, Union[str, int, bool]]:
        # dictionary of values to resolve index of substrings to color
        return {
            "freeze": 0,
            "applied": False,
            "letter": "",
            "pos": pos,
            "added": 0,
        }

    def __process_index(
            self,
            obj: Dict[str, Union[str, int, bool, List[str]]],
            str_: str,
            count: int,
    ) -> Dict[str, Union[str, int, bool, List[str]]]:
        # use the list of key positions within string to color the keys
        freeze = count - 1  # minus 1 for whitespace
        obj["letter"] = str_[count]
        letter = self.get(obj["letter"], reset=None)
        if obj["pos"] and count == obj["pos"][0]:
            obj = self.__update_str_object(freeze, letter, obj)
        return obj

    @staticmethod
    def __reset_index(
            obj: Dict[str, Union[str, int, bool]],
            reset: str,
            len_key: int,
            count: int,
    ) -> Dict[str, Union[str, int, bool]]:
        # index of string has reached position of search key
        # add the length of the search key to the frozen count
        # needs to pass over an entire word if the search was a word
        # otherwise this will just skip over a single index as per
        # usual
        obj["added"] = len_key + obj["freeze"]
        if (count == obj["added"] or len_key == 1) and obj["applied"]:
            obj.update({"letter": obj["letter"] + reset, "applied": False})
        return obj

    def __process_keys(
            self, str_: str, pos: List[int], reset: str, len_key: int
    ) -> str:
        # color the searched keys bases on their index within the string
        compile_ = []
        obj = self.__str_object(pos)
        for count, _ in enumerate(str_):
            obj = self.__process_index(obj, str_, count)
            obj = self.__reset_index(obj, reset, len_key, count)
            letter = obj["letter"]
            compile_.append(letter)
        return "".join(compile_)

    def __process_str(
            self,
            keys: Tuple[str],
            str_: str,
            reset: str,
            switches: Dict[str, bool],
    ) -> str:
        # process arguments provided to color the string accordingly
        pos = []
        for key in keys:
            pos = self.__normalize_position(key, str_, pos, switches)
            len_key = len(key) if not switches["any"] else 1
            str_ = self.__process_keys(str_, pos, reset, len_key)
        return str_

    def __populate_defaults(self, kwargs: Dict[str, str]) -> Dict[str, str]:
        # Set any gaps in kwargs with the existing class values
        # (not subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.__keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]
        return kwargs

    @staticmethod
    def __resolve_arg_type(arg: Union[str, int]) -> Union[str, int]:
        # if codes are entered all together e.g.
        # >>> color = Color(112)
        # {"text": "red", "effect": "bold", "background": "green"}
        # then separate them to be used as individual arguments
        # otherwise return as is
        if isinstance(arg, int):
            for item in list(str(arg)):
                return int(item)
        return arg

    def __process_args(self, args: Tuple[Any]) -> List[str]:
        # e.g. instead of text="red", effect="bold", background="blue"
        # 114 would get the same result
        args = list(args)
        for count, arg in enumerate(args):
            args[count] = self.__resolve_arg_type(arg)
        return args

    @staticmethod
    def __kwargs_in_range(
            index_: int, args: Tuple[Any], kwargs: Dict[str, int], key: str
    ) -> Dict[str, int]:
        # the index is good to use if the value is not None and is less
        # than the length of the arguments given
        if 0 <= index_ < len(args):
            kwargs.update({key: args[index_]})
        return kwargs

    @staticmethod
    def __keywords_not_ready(
            key: str, kwargs: Dict[str, Any], opts: List[str]
    ) -> bool:
        # determine whether keyword arguments provided aren't valid
        # check whether the args given are not integers or are not
        # within the length of opts that can be used
        # return positive value if kwargs will need to be resolved
        if key in kwargs:
            return not isinstance(kwargs[key], int) or kwargs[key] > len(opts)
        return True

    @staticmethod
    def __resolve_alternate_opts(
            key: str,
            kwargs: Dict[str, Union[str, int]],
            opts: List[str],
            default: int,
    ) -> Dict[str, Union[str, int]]:
        # will assign the default value to kwargs if invalid value is
        # provided otherwise if keypair is string - but valid - value
        # will be converted to integer
        if key not in kwargs or key in kwargs and kwargs[key] not in opts:
            kwargs.update({key: default})
        elif kwargs[key] in opts:
            kwargs.update({key: opts.index(kwargs[key])})
        return kwargs

    def __resolve_kwargs(
            self, key: str, kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        # if kwargs are not able to be used as they are then run methods
        # which convert kwargs from alternative values to integer codes
        default = 7 if key == "text" else 0
        opts = self.__get_opts(key)
        if self.__keywords_not_ready(key, kwargs, opts):
            kwargs = self.__resolve_alternate_opts(key, kwargs, opts, default)
        return kwargs

    def __get_processed(
            self, args: Tuple[Any], kwargs: Dict[str, str]
    ) -> Dict[str, str]:
        # organise args and kwargs into a parsable dictionary
        # ensure values given are withing the range of values that can
        # be used and if they aren't instantiate with default values
        # check whether keywords are good to go or need to be resolved
        # first
        for index_, key in enumerate(Color.__keys):
            kwargs = self.__kwargs_in_range(index_, args, kwargs, key)
            kwargs = self.__resolve_kwargs(key, kwargs)
        return kwargs

    def __set_subclass(
            self, key: str, value: Dict[str, Any], args: Tuple[str]
    ) -> None:
        # set subclass as an instance attribute so dynamic names are
        # recognised as correct attributes belonging to class
        value = self.__get_processed(args, value)
        color = Color(*args, **value)
        setattr(self, key, color)

    def __make_subclass(
            self, args: Tuple, kwargs: Dict[str, Dict[str, Any]]
    ) -> bool:
        # make subclass attribute and return boolean value so method
        # calling this method can determine whether subclass has
        # successfully been made
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                self.__set_subclass(key, value, args)
                return True
        return False

    def __set_class_attrs(
            self,
            args: Union[tuple, list],
            kwargs: Union[Dict[str, str], Dict[str, Dict[str, Any]]],
    ) -> None:
        # if not making a subclass then process args and kwargs and add
        # compiled dict to masterclass
        if not self.__make_subclass(args, kwargs):
            params = self.__get_processed(args, kwargs)
            self.__dict__.update(params)

    def __set_bold_attr(self) -> None:
        # Instantiate bold class object if bold is not set for more
        # flexible usage and less setting up when using this module to
        # manipulate particular colored strings
        bold = {
            "bold": {
                "text": self.__dict__["text"],
                "effect": "bold",
                "background": self.__dict__["background"],
            }
        }
        self.__make_subclass((), bold)

    def __bold_switch(self) -> None:
        # bold switch:
        # - if used in a class instantiated as bold, switch bold off
        # - if used in a class instantiated without bold, switch bold on
        if self.effect != 1:
            self.__set_bold_attr()

    def set(self, *args: Any, **kwargs: Any) -> None:
        """Call to set new instance values

        colors:
          - black:        0
          - red:          1
          - green:        2
          - yellow:       3
          - blue:         4
          - purple:       5
          - cyan:         6
          - white:        7

        effects:
          - None:         0
          - bold:         1
          - bright:       2
          - underline:    3
          - negative:     4

        :param args:    Colors or effects as integers or strings

                        Without keywords args are positional like so:

                        >>> color = Color("text", "effect", "background")

                        >>> color.set(2, 1, 1)
                        >>> print(color.__dict__)  # doctest +ELLIPSIS
                        {'text': 2, 'effect': 1, 'background': 1, 'b...}

                          - text:       green
                          - effect:     bold
                          - background: red

        :param kwargs:  More precise keyword arguments

                        >>> color = Color()

                        >>> # instance attributes
                        >>> color.set(
                        ...     text="green",
                        ...     effect="bold",
                        ...     background="red"
                        ... )
                        >>> print(color.__dict__)  # doctest +ELLIPSIS
                        {'text': 2, 'effect': 1, 'background': 1, 'b...}

                        >>> # subclasses -  set like those for
                        >>> # original class only keyword arguments
                        >>> # are expressed as dictionary
                        >>> color.set(
                        ...     sub_color={
                        ...         "text": "green",
                        ...         "effect": "bold",
                        ...         "background": "red"
                        ...     }
                        ... )
                        >>> print(color.sub_color.__dict__)
                        {'text': 2, 'effect': 1, 'background': 1}

        """
        kwargs = self.__populate_defaults(kwargs)
        args = self.__process_args(args)
        self.__set_class_attrs(args, kwargs)
        self.__bold_switch()

    def populate_colors(self) -> None:
        """This will create a subclass for every available color

        >>> color = Color()
        >>> color.populate_colors()
        >>> print(color.__dict__)  # doctest +ELLIPSIS
        {'text': 7, 'effect': 0, 'background': 0, 'bold': <object_co...}
        """
        for color in self.__get_opts("colors"):
            kwargs = {color: {"text": color}}
            self.__make_subclass((), kwargs)

    def get(
            self, *args: Union[str, int], reset: Optional[str] = reset
    ) -> Union[str, Tuple[Union[str, Any], ...]]:
        """Return colored string

        >>> color = Color(
        ...     text="red", effect="bold", background="green"
        ... )
        >>> str_ = color.get("red, bold, green background")
        >>> print(str_)
        \u001b[1;31;42mred, bold, green background\u001b[0;0m

        :param args:    Manipulate string(s)
        :param reset:   Variable reset code i.e. standard reset to white
                        text, previous set color, or nothing
        :return:        Colored string
        """
        if len(args) > 1:
            return self.__get_colored_tuple(args, reset)
        return self.__get_colored_str(args[0], reset)

    def get_key(
            self,
            str_: str,
            *search: str,
            scatter: bool = False,
            ignore_case: bool = False,
    ) -> str:
        """With the string as the first argument - and one or more
        searches following - add color to corresponding matched keys

        >>> color = Color(text="red")

        >>> str_ = color.get_key("str to color", "str")
        >>> print(str_)
        \u001b[0;31;40mstr\u001b[0;0m to color

        (Ansi escaped strings may be entered)

        >>> str_ = "\u001b[0;32;40mstr to color\u001b[0;0m"
        >>> str_ = color.get_key(str_, "str")
        >>> print(str_)  # doctest +ELLIPSIS
        \u001b[0;32;40m\u001b[0;31;40mstr\u001b[0;32;40m to color...

        :param str_:        String containing the key(s) to color
        :param search:      Key(s) within string to color
        :param scatter:     Color key(s) in any assortment
        :param ignore_case: Ignore upper and lower cases
        :return:            String with selected key(s) colored
        """
        switches = {"any": scatter, "case": ignore_case}
        if Color.code in str_:
            return self.__resolve_ansi_code(search, str_, switches)
        return self.__process_str(search, str_, Color.reset, switches)

    def multicolor(self, str_: str) -> str:
        """Return string colored with an assortment of all colors
        instantiated in subclass instances

        >>> # only white will be used
        >>> color = Color(text="green")
        >>> none = color.multicolor("multicolored string")
        >>> print(none)
        multicolored string

        >>> # only green and white will be used
        >>> color.set(green={"text": "green"})
        >>> green_and_none = color.multicolor("multicolored string")
        >>> assert "0;32;40m" in green_and_none

        >>> # only green, red and white will be used
        >>> codes = ["0;31;40m", "0;32;40m"]
        >>> color.set(red={"text": "red"})
        >>> green_red_none = color.multicolor("multicolored string")
        >>> for code in codes:
        ...     assert code in green_red_none

        >>> # all colors will be used
        >>> codes = [
        ...     "0;31;40m",
        ...     "0;32;40m",
        ...     "0;33;40m"
        ...     "0;34;40m",
        ...     "0;35;40m",
        ...     "0;36;40m",
        ...     "0;37;40m"
        ... ]
        >>> populate = Color()
        >>> populate.populate_colors()
        >>> all_colors = populate.multicolor("multicolored string")


        :param str_:    String to color
        :return:        Colored string
        """
        colors = self.__get_multi_object()
        return self.__get_multi_str(str_, colors)

    def set_str(self, str_: str, name_: str = "helper") -> str:
        """Separate ansi code from string, creating a Color subclass
        from the pre-existing color, available in self, and return the
        bare string

        :param str_:    String containing ansi escape codes to
                        instantiate class from its codes
        :param name_:   Name of subclass
        :return:        String stripped of ansi codes
        """
        state = self.get_object(str_, name_)
        if state["str_"]:
            str_ = state.pop("str_")
            self.__make_subclass((), state)
        return str_

    def pop(self, str_: str) -> Optional[Any]:
        """Retrieve attr present with class instance

        >>> color = Color(subclass={"text": "red"})
        >>> red = color.pop("subclass")
        >>> print(red.__dict__)  # doctest +ELLIPSIS
        {'text': 1, 'effect': 0, 'background': 0, 'bold': <objec...}

        :param str_:    Key to remove
        :return:        Class dict or None
        """
        for key in list(self.__dict__):
            if str_ == key and key not in Color.__keys:
                return self.__dict__.pop(key)
        return None

    def get_object(
            self, str_: str, name_: str = "helper"
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """Split ansi codes and string and populate the object
        representing the string and its color before they were
        separated to restore its state later

        .. todo::
            - Make this work for multicolor which consists of more than
              just one code
            - Currently the only code captured will be the first one
            - This will also include changes to self.get_key() which
              will need to iterate through several items in object and
              put them back in the right place

        :param str_:    String containing ansi escape codes
        :param name_:   Name of the subclass to be created
        :return:        Dictionary containing separated escape codes and
                        str
        """
        words = self.get_list(str_)
        return self.__get_state_object(words, name_)

    @staticmethod
    def get_list(str_: str) -> List[str]:
        """Split string up by ansi escape codes and return list of all
        sections of the string

        :param str_:    String containing ansi escape codes
        :return:        List of ordered escape codes and substrings
        """
        words = re.split(Color.ansi_escape, str_)
        return [word for word in words if word != ""]

    def print(
            self,
            *args: Union[str, int],
            multi: bool = False,
            **kwargs: Dict[str, str],
    ) -> None:
        """Print colored strings straight to stdout
        builtin print() kwargs valid keyword arguments

        >>> color = Color("red", "bold", "green")
        >>> color.print("red, bold, green background")
        \u001b[1;31;42mred, bold, green background\u001b[0;0m

        :param args:    Arbitrary number of strings or integers
        :param multi:   Boolean value to return multicolored string
        :param kwargs:  builtin print() kwargs
        """
        if multi:
            str_ = self.multicolor(*args)
        else:
            str_ = self.get(*args)
        print(str_, **kwargs)

    def print_key(
            self,
            str_: str,
            *args: str,
            scatter: bool = False,
            ignore_case: bool = False,
            **kwargs: Any,
    ) -> None:
        """Search for and then color key-words

        >>> color = Color(1)
        >>> color.print_key("str to color", "str")
        \u001b[0;31;40mstr\u001b[0;0m to color

        :param str_:        String to be printed
        :param args:        Words to be colored
        :param ignore_case: Ignore case if True
        :param scatter:     Search letters and not just words if True
        :param kwargs:      builtin print() kwargs
        """
        str_ = self.get_key(
            str_, *args, scatter=scatter, ignore_case=ignore_case
        )
        print(str_, **kwargs)
