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

    @staticmethod
    def __normalize_old(key: str, ignore_case: bool) -> str:
        # when `ignore_case` is True make all words lower case to
        # properly match them
        return key.lower() if ignore_case else key

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

    @staticmethod
    def __separate_key(key: str) -> List[str]:
        # separate the key given into individual letters so that:
        #   - if ignore_case is given as an argument upper and lower
        #     letters can be searched without changing the stdout to
        #     lower cases
        #   - scatter can easily be given as an argument no matter what
        #     the search parameters given
        indices = []
        for item in key:
            for index_ in item:
                indices.append(index_)
        return indices

    @staticmethod
    def __ignore_case_indices(indices: List[str]) -> List[str]:
        # if ignore_case is True then normalize all strings into lower
        # case to test against a string.lower() variable
        for count, index in enumerate(indices):
            indices[count] = index.lower()
        return indices

    @staticmethod
    def __string_regex(string: str, case: str) -> str:
        # e.g. ["C", "c", ":"], ["Cc:"], ["cc:"]
        # case == "<ansi red>C<reset>" etc...
        rep_string = f"{Color.start}{case}{Color.stop}"

        # replacements = {"C": "<ansi red>C<reset>"
        replacements = {case: rep_string}
        rep_sorted = sorted(replacements, key=len, reverse=True)
        rep_escaped = map(re.escape, rep_sorted)
        pattern = re.compile("|".join(rep_escaped))
        return pattern.sub(
            lambda match_: replacements[match_.group(0)], string
        )

    def __consume_helper(self, string: str) -> str:
        string = self.helper.get(string)
        del self.__dict__["helper"]
        return string

    def __convert_string(self, reset: str, string: str) -> str:
        chars = []
        start = False
        for char in string:
            if char == Color.start:
                start = True
            else:
                if start:
                    char = self.get(char, reset=None)
                    start = False
                if char == Color.stop:
                    chars.append(reset)
                    continue
                chars.append(char)
        return "".join(chars) if chars else string

    @staticmethod
    def __get_case_indices(index_values: List[str]) -> List[str]:
        indices = []
        for key in index_values:
            for item in key:
                indices.append(item)
                if item.isalnum():
                    indices.append(item.swapcase())
        return indices

    @staticmethod
    def __match_ignore_case(
        word: str, key: str, match_word: List[str], case: str
    ) -> Tuple[Any, bool]:
        for letter in word:
            for index_ in key:
                if letter in (index_, index_.swapcase()):
                    match_word.append(letter)
                    break
        if "".join(match_word) == word:
            return word, True
        return case, False

    def __match_exact(self, word: str, case: str) -> Tuple[Any, bool]:
        var_sub = self.__normalize_old(word, False)
        if case in (var_sub, word):
            return word, True
        return case, False

    def __get_match(
        self, key: str, words: List[str], case: str, ignore_case: bool
    ) -> Tuple[Any, bool]:
        match_word = []
        for word in words:
            if ignore_case:
                return self.__match_ignore_case(word, key, match_word, case)
            return self.__match_exact(word, case)
        return case, False

    @staticmethod
    def __preserve(
        ansi_escape: Pattern[str], word: str, save_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        if ansi_escape.match(word):
            if word != Color.reset:
                save_state["helper"].update(
                    {
                        "text": int(word[5]),
                        "effect": int(word[2]),
                        "background": int(word[8]),
                    }
                )
        else:
            save_state.update({"string": word})
        return save_state

    def __mark_match(
        self,
        key: str,
        string: str,
        indices: List[str],
        scatter: bool,
        ignore_case: bool,
    ):
        for case in indices:
            match = False
            if not scatter:
                case = "".join(indices)
                split_string = string.split()
                case, match = self.__get_match(
                    key, split_string, case, ignore_case
                )
            if scatter or match:
                string = self.__string_regex(string, case)
        return string

    def __preserve_string_color(self, string: str) -> Dict[str, Any]:
        save_state = {"helper": {}}
        ansi_esc = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")
        splits = re.split(ansi_esc, string)
        filtered = [split for split in splits if split != ""]
        for word in filtered:
            save_state = self.__preserve(ansi_esc, word, save_state)
        return save_state

    def __get_indices(
        self, key: str, scatter: bool, ignore_case: bool
    ) -> List[str]:
        indices = self.__separate_key(key)
        if ignore_case:
            indices = self.__get_case_indices(indices)
        if scatter:
            indices = list(dict.fromkeys(indices))
        return indices

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
        if Color.start in key or Color.stop in key:
            return string
        reset = Color.reset
        colored = Color.esc in string
        if colored:
            save_state = self.__preserve_string_color(string)
            if save_state["string"]:
                string = save_state.pop("string")
            self.__make_subclass((), save_state)
            reset = self.helper.get("", reset=None)
        indices = self.__get_indices(key, scatter, ignore_case)
        matched = self.__mark_match(key, string, indices, scatter, ignore_case)
        converted = self.__convert_string(reset, matched)
        return self.__consume_helper(converted) if colored else converted

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
