"""
object-colors
=============

Object-oriented library for stylizing terminal output.
"""
import re
from random import randint
from typing import Optional

import colorama

__version__ = "1.0.8"


class Color:
    """Color object."""

    keys = ["text", "effect", "background"]
    opts = {
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
    colorama.init()

    def __init__(self, *args, **kwargs):
        self.text = 7
        self.effect = 0
        self.background = 0
        self.set(*args, **kwargs)

    def __getattr__(self, item):
        # look up dynamic subclasses
        return item

    def __dir__(self):
        # primarily here so linters know that the subclass calling
        # methods are not strings strings attempting to call attributes
        return [str(item) for item in self.__dict__]

    @staticmethod
    def _collect_values(value, key, colors):
        # determine that value is a subclass before adding it to the
        # object to avoid TypeErrors
        if not isinstance(value, int) and key not in ("bold", "black"):
            colors["classes"].append(value)
            colors["code"].append(value.text)

        return colors

    def _dummy_subclass(self):
        # populate class with white subclass
        kwargs = {"white": {"text": 7}}
        self._make_subclass((), kwargs)
        return self.__dict__["white"]

    def _get_default(self, colors):
        # if no white class is present, or no classes are present at
        # all, add to dictionary to keep multicolor method running with
        # some variance for lower numbers of classes
        if "white" not in colors["classes"]:
            white = self._dummy_subclass()
            colors["classes"].append(white)
            colors["code"].append(white.text)

        return colors

    def _get_multi_object(self):
        # get an object consisting of available color codes to be
        # randomized and available subclasses to match against
        # randomized codes
        colors = {"code": [], "classes": []}
        for key, value in self.__dict__.items():
            colors = self._collect_values(value, key, colors)

        colors = self._get_default(colors)
        colors["code"] = list(dict.fromkeys(colors["code"]))
        return colors

    @staticmethod
    def _validate_code(colors, code, letter, full_str):
        # match the ansi escape code against randomized number to be
        # used to color string index
        for class_ in colors["classes"]:
            if class_.text == code:
                idx = class_.get(letter)
                full_str.append(idx)
                break

        return full_str

    def _get_multi_str(self, _str, colors):
        # compile and return the string colored by a randomized
        # assortment of colors present with the available subclasses
        full_str = []
        if len(colors["classes"]) == 1:
            return _str

        max_ = len(colors["code"]) - 1
        for count, _ in enumerate(_str):
            letter = _str[count]
            idx = randint(0, max_)
            code = colors["code"][idx]
            full_str = self._validate_code(colors, code, letter, full_str)

        return "".join(full_str)

    def _get_colored_tuple(self, args, reset):
        args = list(args)
        # replace tuples containing strings with corresponding colored
        # strings
        for count, arg in enumerate(args):
            args[count] = self._get_colored_str(arg, reset)

        return tuple(args)

    def _color_settings(self):
        # get the colored string with ansi-escape code settings added
        return f"{Color.code}[{self.effect};3{self.text};4{self.background}m"

    def _get_colored_str(self, _str, reset):
        # set desired reset code and return colored string
        reset = reset if reset else ""
        setting = self._color_settings()
        return f"{setting}{_str}{reset}"

    @staticmethod
    def _extract_codes(word, helper):
        # ints represent the ansi code index within the string
        # This function looks to retrieve an ansi code - rather than
        # create one - to be used again later in the `helper` subclass
        codes = {"text": 5, "effect": 2, "background": 8}
        for key, value in codes.items():
            helper.update({key: int(word[value])})

        return helper

    def _populate_state_object(self, word, name_, state):
        # separate ansi codes from string and return a dict of both to
        # be used individually later
        if Color.ansi_escape.match(word):
            if word != Color.reset:
                codes = self._extract_codes(word, {})
                state[name_].update(codes)
        else:
            state["_str"].append(word)

        return state

    def _get_state_object(self, words, name_):
        # iterate string split up by ansi escape codes to populate
        # object to organise them
        state = {name_: {}, "_str": []}
        for word in words:
            state = self._populate_state_object(word, name_, state)

        state["_str"] = "".join(state["_str"])
        return state

    @staticmethod
    def _get_opts(key):
        # get list of values to represent ansi escape codes whether
        # colors are needed or effects are needed
        if key in Color.opts:
            return Color.opts[key]

        return Color.opts["colors"]

    def _resolve_ansi_code(self, keys, _str, switches):
        # separate ansi escape codes from ansi coded string
        # create the `helper` subclass and return the bare string
        # reset code will return strings after the colored keys as their
        # original ansi code color
        # color the keywords entered as *args
        # surround the string with its original color
        # remove the helper function and return colored string
        _str = self.set_str(_str)
        reset = self.helper.get("", reset=None)
        _str = self._process_str(keys, _str, reset, switches)
        _str = self.helper.get(_str)
        del self.__dict__["helper"]
        return _str

    @staticmethod
    def _get_swapped_index(switches, letter, idx):
        # add additional swapped case of string index for scatter mode
        # to catch all instances of occurring substring when ignore case
        # is also active
        if switches["case"] and letter.isalnum():
            idx.append(letter.swapcase())

        return idx

    def _get_str_indices(self, key, switches):
        # separate all characters into individual indices to be
        # individually run against main string for substrings
        idx = []
        key = list(key)
        for letter in key:
            idx.append(letter)
            idx = self._get_swapped_index(switches, letter, idx)

        return list(dict.fromkeys(idx))

    @staticmethod
    def _normalize_strs(key, _str, switches):
        # ignore case of the searched string by searching lowercase
        # substring in lowercase string
        strs = {"_str": _str, "key": key}
        if switches["case"]:
            strs.update({"_str": _str.lower(), "key": key.lower()})

        return strs

    @staticmethod
    def _get_multiple_positions(key, _str, pos):
        # generator will be needed if there are multiple positions of a
        # single substring
        places = [p for p in range(len(_str)) if _str.find(key, p) == p]
        for place in places:
            pos.append(place)

        return pos

    def _find_key_positions(self, strs, pos):
        # find the position of keywords(s) and return list of results
        key = strs["key"]
        _str = strs["_str"]
        if f" {key} " in f" {_str} ":
            pos = self._get_multiple_positions(key, _str, pos)

        return pos

    @staticmethod
    def _iterate_theirs(letter, ours, pos, count):
        # iterate through either a full string or just once against a
        # single index and check whether the search is successful
        # if it is then append the count (index) of the main string to
        # the list of index positions
        for theirs in letter:
            if ours == theirs:
                pos.append(count)

        return pos

    def _iterate_ours(self, idx, _str, pos, count):
        # get letter of string according to enumeration in main loop
        # and iterate string we want to search with string we are
        # searching against
        letter = _str[count]
        for ours in idx:
            pos = self._iterate_theirs(letter, ours, pos, count)

        return pos

    def _get_scattered_positions(self, _str, idx, pos):
        # get the scattered position of searched keys within string
        for count, _ in enumerate(_str):
            pos = self._iterate_ours(idx, _str, pos, count)

        return pos

    @staticmethod
    def _update_str_object(freeze, letter, obj):
        # update the object keeping track of various statuses through
        # the color string iteration
        obj.update({"freeze": freeze, "letter": letter, "applied": True})
        obj["pos"].pop(0)
        return obj

    def _get_key_positions(self, _str, key, pos, switches):
        # get position(s) of searched term as an integer within string
        strs = self._normalize_strs(key, _str, switches)
        return self._find_key_positions(strs, pos)

    def _normalize_position(self, key, _str, pos, switches):
        # return list of search positions for scattered keys if
        # `scatter` is True or return colored full words if False
        if switches["any"]:
            idx = self._get_str_indices(key, switches)
            return self._get_scattered_positions(_str, idx, pos)

        return self._get_key_positions(_str, key, pos, switches)

    @staticmethod
    def _str_object(pos):
        # dictionary of values to resolve index of substrings to color
        return {
            "freeze": 0,
            "applied": False,
            "letter": "",
            "pos": pos,
            "added": 0,
        }

    def _process_index(self, obj, _str, count):
        # use the list of key positions within string to color the keys
        freeze = count - 1  # minus 1 for whitespace
        obj["letter"] = _str[count]
        letter = self.get(obj["letter"], reset=None)
        if obj["pos"] and count == obj["pos"][0]:
            obj = self._update_str_object(freeze, letter, obj)

        return obj

    @staticmethod
    def _reset_index(obj, reset, len_key, count):
        # index of string has reached position of search key
        # add the length of the search key to the frozen count
        # needs to pass over an entire word if the search was a word
        # otherwise this will just skip over a single index as per
        # usual
        obj["added"] = len_key + obj["freeze"]
        if (count == obj["added"] or len_key == 1) and obj["applied"]:
            obj.update({"letter": obj["letter"] + reset, "applied": False})

        return obj

    def _process_keys(self, _str, pos, reset, len_key):
        # color the searched keys bases on their index within the string
        compile_ = []
        obj = self._str_object(pos)
        for count, _ in enumerate(_str):
            obj = self._process_index(obj, _str, count)
            obj = self._reset_index(obj, reset, len_key, count)
            letter = obj["letter"]
            compile_.append(letter)

        return "".join(compile_)

    def _process_str(self, keys, _str, reset, switches):
        # process arguments provided to color the string accordingly
        pos = []
        for key in keys:
            pos = self._normalize_position(key, _str, pos, switches)
            len_key = len(key) if not switches["any"] else 1
            _str = self._process_keys(_str, pos, reset, len_key)

        return _str

    def _populate_defaults(self, kwargs):
        # Set any gaps in kwargs with the existing class values
        # (not subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]

        return kwargs

    @staticmethod
    def _resolve_arg_type(arg):
        # if codes are entered all together e.g.
        # >>> color = Color(112)
        # {"text": "red", "effect": "bold", "background": "green"}
        # then separate them to be used as individual arguments
        # otherwise return as is
        if isinstance(arg, int):
            for item in list(str(arg)):
                return int(item)

        return arg

    def _process_args(self, args):
        # e.g. instead of text="red", effect="bold", background="blue"
        # 114 would get the same result
        args = list(args)
        for count, arg in enumerate(args):
            args[count] = self._resolve_arg_type(arg)

        return args

    @staticmethod
    def _kwargs_in_range(index_, args, kwargs, key):
        # the index is good to use if the value is not None and is less
        # than the length of the arguments given
        if 0 <= index_ < len(args):
            kwargs.update({key: args[index_]})

        return kwargs

    @staticmethod
    def _keywords_not_ready(key, kwargs, opts):
        # determine whether keyword arguments provided aren't valid
        # check whether the args given are not integers or are not
        # within the length of opts that can be used
        # return positive value if kwargs will need to be resolved
        if key in kwargs:
            return not isinstance(kwargs[key], int) or kwargs[key] > len(opts)

        return True

    @staticmethod
    def _resolve_alternate_opts(key, kwargs, opts, default):
        # will assign the default value to kwargs if invalid value is
        # provided otherwise if keypair is string - but valid - value
        # will be converted to integer
        if key not in kwargs or key in kwargs and kwargs[key] not in opts:
            kwargs.update({key: default})

        elif kwargs[key] in opts:
            kwargs.update({key: opts.index(kwargs[key])})

        return kwargs

    def _resolve_kwargs(self, key, kwargs):
        # if kwargs are not able to be used as they are then run methods
        # which convert kwargs from alternative values to integer codes
        default = 7 if key == "text" else 0
        opts = self._get_opts(key)
        if self._keywords_not_ready(key, kwargs, opts):
            kwargs = self._resolve_alternate_opts(key, kwargs, opts, default)

        return kwargs

    def _get_processed(self, args, kwargs):
        # organise args and kwargs into a parsable dictionary
        # ensure values given are withing the range of values that can
        # be used and if they aren't instantiate with default values
        # check whether keywords are good to go or need to be resolved
        # first
        for index_, key in enumerate(Color.keys):
            kwargs = self._kwargs_in_range(index_, args, kwargs, key)
            kwargs = self._resolve_kwargs(key, kwargs)

        return kwargs

    def _set_subclass(self, key, value, args):
        # set subclass as an instance attribute so dynamic names are
        # recognised as correct attributes belonging to class
        value = self._get_processed(args, value)
        color = Color(*args, **value)
        setattr(self, key, color)

    def _make_subclass(self, args, kwargs):
        # make subclass attribute and return boolean value so method
        # calling this method can determine whether subclass has
        # successfully been made
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                self._set_subclass(key, value, args)
                return True

        return False

    def _set_class_attrs(self, args, kwargs):
        # if not making a subclass then process args and kwargs and add
        # compiled dict to masterclass
        if not self._make_subclass(args, kwargs):
            params = self._get_processed(args, kwargs)
            self.__dict__.update(params)

    def _set_bold_attr(self):
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
        self._make_subclass((), bold)

    def _bold_switch(self):
        # bold switch:
        # - if used in a class instantiated as bold, switch bold off
        # - if used in a class instantiated without bold, switch bold on
        if self.effect != 1:
            self._set_bold_attr()

    def populate_colors(self):
        """This will create a subclass for every available color"""
        for color in self._get_opts("colors"):
            kwargs = {color: {"text": color}}
            self._make_subclass((), kwargs)

    def set(self, *args, **kwargs):
        """Call to set new instance values

        :param args:    Colors or effects as integers or strings
        :param kwargs:  More precise keyword arguments
        """
        kwargs = self._populate_defaults(kwargs)
        args = self._process_args(args)
        self._set_class_attrs(args, kwargs)
        self._bold_switch()

    def get(self, *args, reset: Optional[str] = reset):
        """Return colored string

        :param args:    Manipulate string(s)
        :param reset:   Variable reset code i.e. standard reset to white
                        text, previous set color, or nothing
        :return:        Colored string
        """
        if len(args) > 1:
            return self._get_colored_tuple(args, reset)

        return self._get_colored_str(args[0], reset)

    def get_key(self, _str, *search, scatter=False, ignore_case=False):
        """With the string as the first argument - and one or more
        searches following - add color to corresponding matched keys

        :param _str:        String containing the key(s) to color
        :param search:      Key(s) within string to color
        :param scatter:     Color key(s) in any assortment
        :param ignore_case: Ignore upper and lower cases
        :return:            String with selected key(s) colored
        """
        switches = {"any": scatter, "case": ignore_case}
        if Color.code in _str:
            return self._resolve_ansi_code(search, _str, switches)

        return self._process_str(search, _str, Color.reset, switches)

    def multicolor(self, _str):
        """Return string colored with an assortment of all colors
        instantiated in subclass instances

        :param _str:    String to color
        :return:        Colored string
        """
        colors = self._get_multi_object()
        return self._get_multi_str(_str, colors)

    def set_str(self, _str, name_="helper"):
        """Separate ansi code from string, creating a Color subclass
        from the pre-existing color, available in self, and return the
        bare string

        :param _str:    String containing ansi escape codes to
                        instantiate class from its codes
        :param name_:   Name of subclass
        :return:        String stripped of ansi codes
        """
        state = self.get_object(_str, name_)
        if state["_str"]:
            _str = state.pop("_str")
            self._make_subclass((), state)

        return _str

    def pop(self, _str):
        """Retrieve attr present with class instance

        :param _str:    Key to remove
        :return:        Class dict or None
        """
        for key in list(self.__dict__):
            if _str == key and key not in Color.keys:
                return self.__dict__.pop(key)

        return None

    def get_object(self, _str, name_="helper"):
        """Split ansi codes and string and populate the object
        representing the string and its color before they were
        separated to restore its state later

        :param _str:    String containing ansi escape codes
        :param name_:   Name of the subclass to be created
        :return:        Dictionary containing separated escape codes and
                        str
        """
        words = self.get_list(_str)
        return self._get_state_object(words, name_)

    @staticmethod
    def get_list(_str):
        """Split string up by ansi escape codes and return list of all
        sections of the string

        :param _str:    String containing ansi escape codes
        :return:        List of ordered escape codes and substrings
        """
        words = re.split(Color.ansi_escape, _str)
        return [word for word in words if word != ""]

    def print(self, *args, multi=False, **kwargs):
        """Print colored strings straight to stdout
        builtin print() kwargs valid keyword arguments

        :param args:    Arbitrary number of strings or integers
        :param multi:   Boolean value to return multicolored string
        :param kwargs:  builtin print() kwargs
        """
        if multi:
            _str = self.multicolor(*args)
        else:
            _str = self.get(*args)

        print(_str, **kwargs)
