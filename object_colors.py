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
        # the processed args list and assign ordered list indices to each
        # key
        # Kwargs will be Color’s kwargs argument for class instance
        # subclass
        ints = {}
        for index_, sub_key in enumerate(Color.keys):
            if 0 <= index_ < len(args):
                ints.update({sub_key: args[index_]})
            kwargs[key] = ints
        return kwargs

    @staticmethod
    def __normalize_old(key: str, ignore_case: bool) -> str:
        # when `ignore_case` is True make all words lower case to
        # properly match them
        return key.lower() if ignore_case else key

    @staticmethod
    def __replace_keyword(word: str, keyword: str, rep_string: str) -> str:
        if word == keyword:
            return rep_string
        return word

    def __mark_word(self, string: str, keyword: str, rep_string: str) -> str:
        compiled = []
        words = string.split(" ")
        # split for split in splits if split != ""
        for word in words:
            word = self.__replace_keyword(word, keyword, rep_string)
            compiled.append(word)
        return " ".join(compiled) if compiled else string

    def __mark_words(self, key: str, string: str, ignore_case: bool) -> str:
        re_mode = re.IGNORECASE if ignore_case else 0
        for keyword in key:
            if re.search(r"\b" + re.escape(keyword) + r"\b", string, re_mode):
                rep_string = f"{Color.start}{keyword}{Color.stop}"
                if rep_string not in string:
                    return self.__mark_word(string, keyword, rep_string)
        return string

    def __manipulate_word(self, word: str) -> str:
        decoded = word[1:-1]
        colored = self.__resolve_code(decoded, start=True, colored=False)
        return f"{colored}{self.helper.get('', reset=None)}"

    def __color_words(self, string: str) -> str:
        resolved = []
        words = string.split(" ")
        for word in words:
            if word and word[0] == Color.start:
                word = self.__manipulate_word(word)
            resolved.append(word)
        return " ".join(resolved) if resolved else string

    def __resolve_code(self, char: str, start: bool, colored: bool) -> str:
        # get formatted enter and exit codes
        char = self.__get_enter_code(char, start)
        if char != Color.stop or not colored:
            return char
        return self.helper.get("", reset=None)

    @staticmethod
    def __split_regex(string: str, ansi_escape: Pattern[str]) -> List[str]:
        # split string by ansi escape codes
        splits = re.split(ansi_escape, string)
        return [split for split in splits if split != ""]

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

    def __kwargs_dict(self, kwargs: Dict[str, str]) -> Dict[str, str]:
        # Set any gaps in kwargs with the existing class values (not
        # subclasses) so as not to override them with the defaults
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]
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

    def __class_kwargs(
        self,
        args: Union[tuple, list],
        kwargs: Union[Dict[str, str], Dict[str, Dict[str, Any]]],
    ) -> None:
        if not self.__make_subclass(args, kwargs):
            kwargs = self.__get_processed(args, kwargs)
            self.__dict__.update(kwargs)

    @staticmethod
    def __sort_replacements(replacements: Dict[str, str]) -> List[str]:
        # place longer ones first to keep shorter substrings from
        # matching where the longer ones should take place
        # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'}
        # against the string 'hey abc', it should produce 'hey ABC' and
        # not 'hey ABc'
        replacements = {key: val for key, val in replacements.items()}
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
    def __populate_passed(kwargs: Dict[str, bool]) -> bool:
        # if `populate` passed as argument, whether True or False return
        # if, otherwise return its default, False
        return kwargs.pop("populate") if "populate" in kwargs else False

    def __get_enter_code(self, char: str, start: bool) -> str:
        # if `start` is True the preceding character to this letter
        # has indicated that this is to be colored
        return self.key_marker.get(char, reset=None) if start else char

    @staticmethod
    def __get_indices(key: str) -> List[str]:
        # get list of letters of a string
        string_list = []
        for item in key:
            for index_ in item:
                string_list.append(index_)
        return string_list

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
        return "".join(chars) if chars else string

    def __find_word(self, key, string, ignore):
        split_string = string.split()
        for sub in split_string:
            var_sub = self.__normalize_old(sub, ignore)
            if var_sub == key or sub == key:
                return sub
        return None

    def __mark_string(self, case, indices, string, scatter, ignore):
        match = False
        if not scatter:
            case_str = "".join(indices)
            case = self.__find_word(case_str, string, ignore)
            if case:
                match = True
            else:
                case = case_str
        if scatter or match:
            rep_string = f"{Color.start}{case}{Color.stop}"
            return self.__rep_sub(string, {case: rep_string})
        return string

    def __mark_indices(
        self, indices: List[str], string: str, scatter: bool, ignore: bool
    ) -> str:
        for key in indices:
            for item in key:
                cases = [item.upper(), item.lower()] if ignore else [indices]
                for case in cases:
                    string = self.__mark_string(
                        case, indices, string, scatter, ignore
                    )
        return string

    def __resolve_mode(
        self,
        key: str,
        string: str,
        scatter: bool,
        ignore_case: bool,
        colored: bool,
    ) -> str:
        indices = self.__get_indices(key)
        marked = self.__mark_indices(indices, string, scatter, ignore_case)
        return self.__color_indices(marked, colored)

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

    def print(self, *args: Union[str, int], **kwargs: Dict[str, str]) -> None:
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows
                        Method behaves just like builtin print()
        :param kwargs:  builtin print() kwargs
        """
        print(self.get(*args), **kwargs)

    def set(self, *args: Any, **kwargs: Any) -> None:
        """Call to change/update/add class values or add subclasses for
        new text, effects and backgrounds

        :param args:    Integer escape codes or strings to be converted
                        into escape codes
        :param kwargs:  More precise keyword arguments
        """
        if self.__populate_passed(kwargs):
            self.__populate_colors()
        kwargs = self.__kwargs_dict(kwargs)
        kwargs = self.__class_ints(kwargs)
        args = self.__process_args(args)
        self.__class_kwargs(args, kwargs)
        if self.effect != 1:
            self.__switch_bold()

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
        string: str,
        key: Union[str, List[str]],
        color: Union[int, str] = 1,
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
        :param color:
        :return:            String containing individual colored words
        """
        self.__make_subclass((), {"key_marker": {"text": color}})
        ansi_escape = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")
        colored = Color.esc in string
        if colored:
            words = self.__split_regex(string, ansi_escape)
            save_state = self.__separate_ansi(words, ansi_escape)
            string = (
                save_state.pop("string") if "string" in save_state else string
            )
            self.__make_subclass((), save_state)
        string = self.__resolve_mode(
            key, string, scatter, ignore_case, colored
        )
        del self.__dict__["key_marker"]
        if colored:
            string = self.helper.get(string)
            del self.__dict__["helper"]
        return string
