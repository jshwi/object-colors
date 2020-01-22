#!/usr/bin/env python3

"""object-colors
     A Python Color Dictionary

A simple to use class module designed to stylise output with minimal
setup and instantiation
"""
import re
from typing import Union, Any, Optional, Tuple, Dict, List


class Color:
    """Instantiate object with all attributes or set attributes after
    instantiation
    Set class attributes for Color.print() or Color.get()
    """

    esc = "\u001b"
    reset = esc + "[0;0m"
    keys = ["text", "effect", "background"]

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
    def __get_nested(
        key: str,
        args: List[str],
        kwargs: Dict[str, Union[str, Dict[str, str]]],
    ) -> Dict[str, str]:
        # Run through corresponding allowed keys against the length of
        # the processed args list and assign ordered list indices to
        # each key
        # Kwargs will be Color’s kwargs argument for class instance
        # subclass
        ints = {}
        for index_, sub_key in enumerate(Color.keys):
            if 0 <= index_ < len(args):
                ints.update({sub_key: args[index_]})
            kwargs[key] = ints
        return kwargs

    @staticmethod
    def __process_args(args: Tuple[Any]) -> List[str]:
        # e.g. instead of text="red", effect="bold", background="blue"
        # 114 would get the same result
        values = []
        for arg in args:
            if isinstance(arg, int):
                items = list(str(arg))
                for item in items:
                    values.append(int(item))
            else:
                values.append(arg)
        return values

    def __class_ints(self, kwargs: Dict[str, str]) -> Dict[str, str]:
        # Resolves values which may not be entered as tuples, and
        # therefore will confuse the class methods which are expecting
        # args
        for key, value in list(kwargs.items()):
            if not isinstance(value, dict) and key not in Color.keys:
                if not isinstance(value, tuple):
                    value = (value,)
                args = self.__process_args(value)
                kwargs = self.__get_nested(key, args, kwargs)
        return kwargs

    def __kwargs_dict(self, kwargs: Dict[str, str]) -> Dict[str, str]:
        # Set any gaps in kwargs with the existing class values (not
        # subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]
        return kwargs

    def __class_kwargs(
        self,
        args: Union[tuple, list],
        kwargs: Union[Dict[str, str], Dict[str, Dict[str, Any]]],
    ) -> None:
        if not self.__make_subclass(args, kwargs):
            kwargs = self.__get_processed(args, kwargs)
            self.__dict__.update(kwargs)

    def __switch_bold(self) -> None:
        # Instantiate bold class object if bold is not set for more
        # flexible usage and less setting up when using this module
        kwargs = {
            "bold": {
                "text": self.__dict__["text"],
                "effect": "bold",
                "background": self.__dict__["background"],
            }
        }
        self.__make_subclass((), kwargs)

    def __populate_colors(self) -> None:
        # This will create a subclass for every available color when
        # colors" is called whilst instantiating self
        for color in self.__opts("colors"):
            kwargs = {color: {"text": color}}
            self.__make_subclass((), kwargs)

    @staticmethod
    def __populate_passed(kwargs: Dict[str, bool]) -> bool:
        # if `populate` passed as argument, whether True or False return
        # if, otherwise return its default, False
        return kwargs.pop("populate") if "populate" in kwargs else False

    def set(self, *args: Any, **kwargs: Any) -> None:
        """Call to change/update/add class values or add subclasses for
        new text, effects and backgrounds

        :param args:    Integer escape codes or strings to be converted
                        into escape codes
        :param kwargs:  More precise keyword arguments
        """
        passed = self.__populate_passed(kwargs)
        if passed:
            self.__populate_colors()
        dict_ = self.__kwargs_dict(kwargs)
        dict_ints = self.__class_ints(dict_)
        args = self.__process_args(args)
        self.__class_kwargs(args, dict_ints)
        if self.effect != 1:
            self.__switch_bold()

    def pop(self, select: str) -> Optional[Any]:
        """Remove keypair from __dict__ and return to variable

        :param select:  Key to remove
        :return:        Class dict or None
        """
        for key in list(self.__dict__):
            if select == key and key not in Color.keys:
                popped = self.__dict__[key]
                del self.__dict__[key]
                return popped
        return None

    @staticmethod
    def __opts(key: str) -> List[str]:
        # dictionary of values to represent ansi escape codes
        opts = {
            "effect": ["none", "bold", "bright", "underline", "negative"],
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
        }
        return opts[key] if key in opts else opts["colors"]

    @staticmethod
    def __assign_kw(
        key: str, kwargs: Dict[str, Any], opts: List[str], default: int
    ) -> Dict[str, str]:
        # returns kwargs as is if valid escape code provided
        if (
            key in kwargs
            and isinstance(kwargs[key], int)
            and kwargs[key] <= len(opts)
        ):
            return kwargs
        # will assign the default value to kwargs if invalid value is
        # provided
        if key not in kwargs or key in kwargs and kwargs[key] not in opts:
            kwargs.update({key: default})
        # if keypair is string - but valid - value will be converted to
        # integer
        elif kwargs[key] in opts:
            kwargs.update({key: opts.index(kwargs[key])})
        return kwargs

    def __get_processed(
        self, args: Tuple[Any], kwargs: Dict[str, str]
    ) -> Dict[str, str]:
        # Organise args and kwargs into a parsable dictionary
        for index_, key in enumerate(Color.keys):
            default = 7 if key == "text" else 0
            opts = self.__opts(key)
            if 0 <= index_ < len(args):
                kwargs.update({key: args[index_]})
            kwargs = self.__assign_kw(key, kwargs, opts, default)
        return kwargs

    def __make_subclass(
        self, args: Tuple, kwargs: Dict[str, Dict[str, Any]]
    ) -> bool:
        # Returned list and dict will replace the arg and kwarg parameters
        sub = False
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                value = self.__get_processed(args, value)
                color = Color(*args, **value)
                setattr(self, key, color)
                sub = True
        return sub

    def __save_state(self, string: str) -> str:
        state = {"helper": {}}
        ansi_esc = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")
        words = re.split(ansi_esc, string)
        filter_ = [word for word in words if word != ""]
        for word in filter_:
            if ansi_esc.match(word):
                if word != Color.reset:
                    state["helper"].update(
                        {
                            "text": int(word[5]),
                            "effect": int(word[2]),
                            "background": int(word[8]),
                        }
                    )
            else:
                state.update({"string": word})
        if state["string"]:
            string = state.pop("string")
            self.__make_subclass((), state)
        return string

    @staticmethod
    def __get_index(key, any_: bool, case: bool) -> List[str]:
        idx = []
        key = list(key)
        for key in key:
            for letter in key:
                idx.append(letter)
                if case and letter.isalnum():
                    idx.append(letter.swapcase())
        if any_:
            return list(dict.fromkeys(idx))
        return idx

    @staticmethod
    def __scatter_positions(
        ours: str, letter: str, pos: List[int], count: int
    ) -> List[int]:
        for theirs in letter:
            if ours == theirs:
                pos.append(count)
        return pos

    def __get_key_positions(
        self, str_: str, idx: List[str], any_: bool, pos: List[str]
    ) -> List[int]:
        word = []
        for count in range(len(str_)):
            letter = str_[count]
            for ours in idx:
                if any_:
                    pos = self.__scatter_positions(ours, letter, pos, count)
                else:
                    if ours == letter:
                        word.append(letter)
                    theirs = "".join(word)
                    # match full word and then start again
                    if ours == theirs:
                        pos.append(0)
                        word.clear()
            word.append(letter)
        return pos

    def __color_keys(
        self, key: str, str_: str, pos: List[int], reset: str, any_: bool
    ) -> str:
        freeze = 0
        compile_ = []
        len_key = len(key) if not any_ else 1
        single = len_key == 1
        applied = False
        for count in range(len(str_)):
            letter = str_[count]
            if pos and count == pos[0]:
                freeze = count - 1
                letter = self.get(letter, reset=None)
                applied = True
                pos.pop(0)
            added = freeze + len_key
            if (count == added or single) and applied:
                letter += reset
                applied = False
            compile_.append(letter)
        return "".join(compile_)

    @staticmethod
    def __extract_args(*args: str) -> Union[str, List[str]]:
        keys = []
        for arg in args:
            if len(args) > 1:
                keys.append(arg)
            return arg
        return keys

    def get(
        self, *args: Union[str, int], reset: Optional[str] = reset
    ) -> Union[Tuple[str], str]:
        """String can be returned as variable(s) for assorted color
        printing or can be printed directly by calling self.print()

        :param args:    Manipulate string(s)
        :param reset:   Variable reset code i.e. standard reset to white
                        text, previous set color, or nothing
        :return:        Colored string
        """
        arg_list = []
        reset = reset if reset else ""
        setting = f"{Color.esc}[{self.effect};3{self.text};4{self.background}m"
        if len(args) == 1:
            return setting + args[0] + reset
        for arg in args:
            arg_list.append(setting + arg + reset)
        return tuple(arg_list)

    def get_key(
        self,
        str_: str,
        *keys: str,
        any_: bool = False,
        case: bool = False,
    ) -> str:
        reset = Color.reset
        color = Color.esc in str_
        if color:
            str_ = self.__save_state(str_)
            reset = self.helper.get("", reset=None)
        pos = []
        for key in keys:
            if any_ or case:
                key = self.__get_index(key, any_, case)
            pos = self.__get_key_positions(str_, key, any_, pos)
            str_ = self.__color_keys(key, str_, pos, reset, any_)
        if color:
            str_ = self.helper.get(str_)
            del self.__dict__["helper"]
        return str_

    def print(self, *args: Union[str, int], **kwargs: Dict[str, str]) -> None:
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows
                        Method behaves just like builtin print()
        :param kwargs:  builtin print() kwargs
        """
        print(self.get(*args), **kwargs)
