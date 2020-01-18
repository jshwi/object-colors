#!/usr/bin/env python3

"""object-colors
     A Python Color Dictionary

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

    esc = "\u001b"
    reset = esc + "[0;0m"
    keys = ["text", "effect", "background"]
    start, stop = "`", "~"

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

    def __get_enter_code(self, char: str, start: bool) -> str:
        # if `start` is True the preceding character to this letter
        # has indicated that this is to be colored
        return self.get(char, reset=None) if start else char

    def __resolve_code(self, char: str, start: bool, colored: bool) -> str:
        # get formatted enter and exit codes
        char = self.__get_enter_code(char, start)
        if char != Color.stop or not colored:
            return char
        helper = self.helper.get("", reset=None)
        return helper

    def __color_indices(self, string: str, colored: bool) -> str:
        chars = []
        start = False
        for char in string:
            if char != Color.start:
                char = self.__resolve_code(char, start, colored)
                if char == Color.stop:
                    char = Color.reset
                chars.append(char)
                start = False
            else:
                start = True
        joined = "".join(chars) if chars else string
        return joined

    @staticmethod
    def __sort_replacements(replacements: Dict[str, str]) -> List[str]:
        # place longer ones first to keep shorter substrings from
        # matching where the longer ones should take place
        # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'}
        # against the string 'hey abc', it should produce 'hey ABC' and
        # not 'hey ABc'
        return sorted(replacements, key=len, reverse=True)

    @staticmethod
    def __get_pattern(rep_sorted: List[str]) -> Pattern[str]:
        # if case insensitive, we need to normalize the old string so
        # that later a replacement can be found. For instance with
        # {"HEY": "lol"} we should match and find a replacement for
        # "hey", "HEY", "hEy", etc.
        rep_escaped = map(re.escape, rep_sorted)
        return re.compile("|".join(rep_escaped))

    def __rep_sub(self, string: str, replacements: Dict[str, str],) -> str:
        # *** courtesy of bgusach: gist at bgusach/multireplace.py ***
        # given a string and a replacement map, it returns the replaced
        # string.
        rep_sorted = self.__sort_replacements(replacements)
        # Create a big OR regex that matches any of the substrings to
        # replace
        pattern = self.__get_pattern(rep_sorted)
        # For each match, look up the new string in the replacements,
        # being the key the normalized old string
        return pattern.sub(lambda match: replacements[match.group(0)], string)

    @staticmethod
    def __normalize_old(key: str, ignore_case: bool) -> str:
        # when `ignore_case` is True make all words lower case to
        # properly match them
        return key.lower() if ignore_case else key

    def __find_word(
        self, key: str, string: str, ignore: bool
    ) -> Optional[str]:
        split_string = string.split()
        for sub in split_string:
            var_sub = self.__normalize_old(sub, ignore)
            if key in (var_sub, sub):
                return sub
        return None

    def __mark_string(
        self,
        case: str,
        indices: List[str],
        string: str,
        scatter: bool,
        ignore: bool,
        count: int,
    ) -> str:
        match = False
        # if not scatter attempt to find a match
        if not scatter:
            case_str = "".join(indices)
            case = self.__find_word(case_str, string, ignore)
            if case:
                match = True
            else:
                case = case_str
        # if scatter case does not need to be redeclared
        if scatter or match:
            if scatter and not ignore:
                case = case[count]
            rep_string = f"{Color.start}{case}{Color.stop}"
            return self.__rep_sub(string, {case: rep_string})
        return string

    @staticmethod
    def __alphanumeric(item):
        if item.isalnum():
            return [item.upper(), item.lower()]
        return [item]

    @staticmethod
    def __ignore_case_indices(ignore, indices):
        if ignore:
            for count, index in enumerate(indices):
                indices[count] = index.lower()
        return indices

    def __mark_indices(
        self, indices: List[str], string: str, scatter: bool, ignore: bool
    ) -> str:
        indices = self.__ignore_case_indices(ignore, indices)
        if scatter:
            indices = list(dict.fromkeys(indices))
        for count, key in enumerate(indices):
            for item in key:
                if ignore:
                    cases = self.__alphanumeric(item)
                else:
                    cases = [indices]
                for case in cases:
                    string = self.__mark_string(
                        case, indices, string, scatter, ignore, count
                    )
        return string

    @staticmethod
    def __get_indices(key: str) -> List[str]:
        # get list of letters of a string
        string_list = []
        for item in key:
            for index_ in item:
                string_list.append(index_)
        return string_list

    @staticmethod
    def __populate_codes(
        split, save_state: Dict[str, Union[Dict[str, int], str]]
    ):
        # return a dictionary of ansi codes to be reapplied later
        if split != Color.reset:
            save_state["helper"].update(
                {
                    "text": int(split[5]),
                    "effect": int(split[2]),
                    "background": int(split[8]),
                }
            )
        return save_state

    def __separate_ansi(
        self, splits: List[str], ansi_escape: Pattern[str]
    ) -> Dict[str, Dict[str, Any]]:
        # add ansi codes and string with codes removed to a dictionary
        # to manipulate separately
        save_state = {"helper": {}}
        for split in splits:
            if ansi_escape.match(split):
                save_state = self.__populate_codes(split, save_state)
            else:
                save_state.update({"string": split})
        return save_state

    @staticmethod
    def __split_regex(string: str, ansi_escape: Pattern[str]) -> List[str]:
        # split string by ansi escape codes
        splits = re.split(ansi_escape, string)
        return [split for split in splits if split != ""]

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

    def __pre_colored(self, string):
        # if string is colored then escape codes need to be removed
        # save color to `save_state` so that it may be added after key
        # search has commenced
        ansi_escape = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")
        words = self.__split_regex(string, ansi_escape)
        save_state = self.__separate_ansi(words, ansi_escape)
        string = save_state.pop("string") if "string" in save_state else string
        self.__make_subclass((), save_state)
        return string

    def get_key(
        self,
        string: str,
        key: Union[str, List[str]],
        scatter: bool = False,
        ignore_case: bool = False,
    ) -> str:
        """remove ansi codes so they don't clash with search items
        if the string is not already without ansi codes save it as the
        bare string created during separation of ansi codes
        make the `self.helper` subclass from preserved ansi codes
        color letters / words based on the ignore boolean passed
        recolor the string

        :param string:      Parent string containing substrings
        :param key:         word to search and color
        :param scatter:     True will turn off case sensitive searching
        :param ignore_case:
        :return:            String containing individual colored words
        """
        colored = Color.esc in string
        if colored:
            string = self.__pre_colored(string)
        indices = self.__get_indices(key)
        marked = self.__mark_indices(indices, string, scatter, ignore_case)
        string = self.__color_indices(marked, colored)
        if colored:
            string = self.helper.get(string)
            del self.__dict__["helper"]
        return string

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

    def print(self, *args: Union[str, int], **kwargs: Dict[str, str]) -> None:
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows
                        Method behaves just like builtin print()
        :param kwargs:  builtin print() kwargs
        """
        print(self.get(*args), **kwargs)
