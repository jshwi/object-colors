#!/usr/bin/env python3
"""object-colors
The Python Color Dictionary

A simple to use class module designed to stylise output with minimal
setup and instantiation
"""
import re
from typing import Union, Any, Optional, Tuple, Dict, List, Pattern


class Color:
    """Instantiate object with all attributes or set attributes after
    instantiation
    Set class attributes for Color.print() or Color.get()
    """

    code = "\u001b"
    reset = f"{code}[0;0m"
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

    def __init__(self, *args: Union[str, int], **kwargs: Any) -> None:
        self.text = 7
        self.effect = 0
        self.background = 0
        self.set(*args, **kwargs)

    def __getattr__(self, item: str) -> str:
        return item

    def __dir__(self) -> List[str]:
        return [str(item) for item in self.__dict__]

    @staticmethod
    def __resolve_arg_type(arg: Union[str, int]) -> Union[str, int]:
        if isinstance(arg, int):
            for item in list(str(arg)):
                return int(item)
        return arg

    @staticmethod
    def __populate_passed(kwargs: Dict[str, bool]) -> bool:
        # if `populate` passed as argument, whether True or False return
        # if, otherwise return its default, False
        if "populate" in kwargs:
            return kwargs.pop("populate")
        return False

    @staticmethod
    def __opts(key: str) -> List[str]:
        # dictionary of values to represent ansi escape codes
        if key in Color.opts:
            return Color.opts[key]
        return Color.opts["colors"]

    @staticmethod
    def __str_obj(pos: List[int]) -> Dict[str, Union[str, int, bool]]:
        return {
            "freeze": 0,
            "applied": False,
            "letter": "",
            "pos": pos,
            "added": 0,
        }

    def __populate_colors(self, kwargs) -> None:
        # This will create a subclass for every available color when
        # colors" is called whilst instantiating self
        if self.__populate_passed(kwargs):
            for color in self.__opts("colors"):
                kwargs = {color: {"text": color}}
                self.__make_subclass((), kwargs)

    def __populate_defaults(self, kwargs: Dict[str, str]) -> Dict[str, str]:
        # Set any gaps in kwargs with the existing class values
        # (not subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]
        return kwargs

    def __process_args(self, args: Tuple[Any]) -> List[str]:
        # e.g. instead of text="red", effect="bold", background="blue"
        # 114 would get the same result
        args = list(args)
        for count, arg in enumerate(args):
            args[count] = self.__resolve_arg_type(arg)
        return args

    def __class_kwargs(
            self,
            args: Union[tuple, list],
            kwargs: Union[Dict[str, str], Dict[str, Dict[str, Any]]],
    ) -> None:
        if not self.__make_subclass(args, kwargs):
            kwargs = self.__get_processed(args, kwargs)
            self.__dict__.update(kwargs)

    def __get_processed(
            self, args: Tuple[Any], kwargs: Dict[str, str]
    ) -> Dict[str, str]:
        # Organise args and kwargs into a parsable dictionary
        for index_, key in enumerate(Color.keys):
            default = 7 if key == "text" else 0
            opts = self.__opts(key)
            kwargs = self.__within_range(index_, args, kwargs, key)
            kwargs = self.__resolve_kwargs(key, kwargs, opts, default)
        return kwargs

    def __set_class(
            self, key: str, value: Dict[str, Any], args: Tuple[str]
    ) -> None:
        value = self.__get_processed(args, value)
        color = Color(*args, **value)
        setattr(self, key, color)

    def __make_subclass(
            self, args: Tuple, kwargs: Dict[str, Dict[str, Any]]
    ) -> bool:
        # Returned list and dict will replace the arg and kwarg
        # parameters
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                self.__set_class(key, value, args)
                return True
        return False

    def __switch_bold(self) -> None:
        # Instantiate bold class object if bold is not set for more
        # flexible usage and less setting up when using this module
        text = (self.__dict__["text"],)
        back = (self.__dict__["background"],)
        kwargs = {"bold": {"text": text, "effect": "bold", "background": back}}
        self.__make_subclass((), kwargs)

    def __bold_null(self) -> None:
        if self.effect != 1:
            self.__switch_bold()

    def __args_tuple(
            self, args: Tuple[Union[str, int]], reset: str
    ) -> Tuple[Union[str, int]]:
        args = list(args)
        for count, arg in enumerate(args):
            args[count] = self.__color_str(arg, reset)
        return tuple(args)

    def __color_setting(self) -> str:
        return f"{Color.code}[{self.effect};3{self.text};4{self.background}m"

    def __color_str(self, str_: str, reset: str) -> str:
        reset = reset if reset else ""
        setting = self.__color_setting()
        return f"{setting}{str_}{reset}"

    @staticmethod
    def __get_index(key: str, switches: Dict[str, bool]) -> List[str]:
        # separate all characters into individual indices
        idx = []
        key = list(key)
        for letter in key:
            idx.append(letter)
            if switches["case"] and letter.isalnum():
                idx.append(letter.swapcase())
        return list(dict.fromkeys(idx))

    @staticmethod
    def __reverse_codes(
            word: str, helper: Dict[str, Union[str, int]]
    ) -> Dict[str, Union[str, int]]:
        codes = {"text": 5, "effect": 2, "background": 8}
        for key, value in codes.items():
            helper.update({key: int(word[value])})
        return helper

    def __populate_state_obj(
            self,
            word: str,
            state: Dict[str, Union[str, Dict[str, str]]],
            ansi_esc: Pattern[str],
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        if ansi_esc.match(word):
            if word != Color.reset:
                state["helper"] = self.__reverse_codes(word, {})
        else:
            state.update({"string": word})
        return state

    def __make_state_obj(
            self, str_: str
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        ansi_esc = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")
        words = re.split(ansi_esc, str_)
        filter_ = [word for word in words if word != ""]
        state = {"helper": {}}
        for word in filter_:
            state = self.__populate_state_obj(word, state, ansi_esc)
        return state

    @staticmethod
    def __within_range(index_, args, kwargs, key):
        if 0 <= index_ < len(args):
            kwargs.update({key: args[index_]})
        return kwargs

    @staticmethod
    def __assign_kw(key: str, kwargs: Dict[str, Any], opts: List[str]) -> bool:
        # returns kwargs as is if valid escape code provided
        if key in kwargs:
            return not isinstance(kwargs[key], int) or kwargs[key] > len(opts)
        return True

    @staticmethod
    def __alternate_opts(
            key: str,
            kwargs: Dict[str, Union[str, int]],
            opts: List[str],
            default: str,
    ) -> Dict[str, Union[str, int]]:
        # will assign the default value to kwargs if invalid value is
        # provided otherwise if keypair is string - but valid - value
        # will be converted to integer
        if key not in kwargs or key in kwargs and kwargs[key] not in opts:
            kwargs.update({key: default})
        elif kwargs[key] in opts:
            kwargs.update({key: opts.index(kwargs[key])})
        return kwargs

    def __resolve_kwargs(self, key, kwargs, opts, default):
        if self.__assign_kw(key, kwargs, opts):
            kwargs = self.__alternate_opts(key, kwargs, opts, default)
        return kwargs

    def __instantiate_state(self, str_: str) -> str:
        # separate ansi code from string, creating a Color subclass from
        # the pre-existing color, available in self, and returning the
        # bare string
        state = self.__make_state_obj(str_)
        if state["string"]:
            str_ = state.pop("string")
            self.__make_subclass((), state)
        return str_

    def __resolve_ansi_code(
            self, keys: Tuple[str], str_: str, switches: Dict[str, bool]
    ) -> str:
        str_ = self.__instantiate_state(str_)
        reset = self.helper.get("", reset=None)
        str_ = self.__manipulate_string(keys, str_, reset, switches)
        str_ = self.helper.get(str_)
        del self.__dict__["helper"]
        return str_

    @staticmethod
    def __scatter_pos(str_: str, idx: List[str], pos: List[int]) -> List[int]:
        # get the scattered position of searched keys within string
        for count, _ in enumerate(str_):
            letter = str_[count]
            for ours in idx:
                for theirs in letter:
                    if ours == theirs:
                        pos.append(count)
        return pos

    @staticmethod
    def __get_key_positions(
            str_: str, key: str, pos: List[int], switches: Dict[str, bool]
    ) -> List[int]:
        # get position of searched term as an integer within string
        if switches["case"]:
            str_ = str_.lower()
            key = key.lower()
        if f" {key} " in f" {str_} ":
            places = [p for p in range(len(str_)) if str_.find(key, p) == p]
            for place in places:
                pos.append(place)
        return pos

    def __mode_position(
            self, key: str, str_: str, pos: List[int], switches: Dict[str, bool]
    ) -> List[int]:
        if switches["any"]:
            idx = self.__get_index(key, switches)
            return self.__scatter_pos(str_, idx, pos)
        return self.__get_key_positions(str_, key, pos, switches)

    def __color_index(
            self,
            obj: Dict[str, Union[str, int, bool, List[str]]],
            str_: str,
            count: int,
    ) -> Dict[str, Union[str, int, bool, List[str]]]:
        whitespace = 1
        freeze = count - whitespace
        obj["letter"] = str_[count]
        letter = self.get(obj["letter"], reset=None)
        if obj["pos"] and count == obj["pos"][0]:
            obj.update({"freeze": freeze, "letter": letter, "applied": True})
            obj["pos"].pop(0)
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
            obj["letter"] += reset
            obj["applied"] = False
        return obj

    def __color_keys(
            self, str_: str, pos: List[int], reset: str, len_key: int
    ) -> str:
        # color the searched keys bases on their index within the string
        compile_ = []
        obj = self.__str_obj(pos)
        for count, _ in enumerate(str_):
            obj = self.__color_index(obj, str_, count)
            obj = self.__reset_index(obj, reset, len_key, count)
            letter = obj["letter"]
            compile_.append(letter)
        return "".join(compile_)

    def __manipulate_string(
            self,
            keys: Tuple[str],
            str_: str,
            reset: str,
            switches: Dict[str, bool],
    ) -> str:
        pos = []
        for key in keys:
            pos = self.__mode_position(key, str_, pos, switches)
            len_key = len(key) if not switches["any"] else 1
            str_ = self.__color_keys(str_, pos, reset, len_key)
        return str_

    def set(self, *args: Any, **kwargs: Any) -> None:
        """Call to change/update/add class values or add subclasses for
        new text, effects and backgrounds

        :param args:    Integer escape codes or strings to be converted
                        into escape codes
        :param kwargs:  More precise keyword arguments
        """
        self.__populate_colors(kwargs)
        kwargs = self.__populate_defaults(kwargs)
        args = self.__process_args(args)
        self.__class_kwargs(args, kwargs)
        self.__bold_null()

    def pop(self, str_: str) -> Optional[Any]:
        """Remove keypair from __dict__ and return to variable

        :param str_:  Key to remove
        :return:        Class dict or None
        """
        for key in list(self.__dict__):
            if str_ == key and key not in Color.keys:
                return self.__dict__.pop(key)
        return None

    def get(
            self, *args: Union[str, int], reset: Optional[str] = reset
    ) -> Union[str, Tuple[Union[str, Any], ...]]:
        """String can be returned as variable(s) for assorted color
        printing or can be printed directly by calling self.print()

        :param args:    Manipulate string(s)
        :param reset:   Variable reset code i.e. standard reset to white
                        text, previous set color, or nothing
        :return:        Colored string
        """
        if len(args) > 1:
            return self.__args_tuple(args, reset)
        return self.__color_str(args[0], reset)

    def get_key(
            self, str_: str, *keys: str, any_: bool = False, case: bool = False,
    ) -> str:
        """With the string as the first argument - and one or more
        searches following - add color to matched substring
        corresponding with *keys
        leave the reset untouched (Ansi escaped strings may be entered)

        :param str_:    String containing the key to color
        :param keys:    Key(s) within string to color
        :param any_:    Color key in any assortment
        :param case:    Ignore upper and lower cases
        :return:        String as it was with selected key colored
        """
        switches = {"any": any_, "case": case}
        if Color.code in str_:
            return self.__resolve_ansi_code(keys, str_, switches)
        return self.__manipulate_string(keys, str_, Color.reset, switches)

    def print(self, *args: Union[str, int], **kwargs: Dict[str, str]) -> None:
        """Enhanced print function for class and subclasses

        :param args:    Arbitrary number of strings or integers
        :param kwargs:  builtin print() kwargs
        """
        print(self.get(*args), **kwargs)
