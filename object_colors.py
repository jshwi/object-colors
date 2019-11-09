#!/usr/bin/env python3

"""object-colors
     A Python Color Dictionary

A simple to use class module designed to stylise output with minimal
setup and instantiation

The philosophy behind object-colors is more terminal for less code
"""
__author__ = "Stephen Whitlock"
__copyright__ = "Copyright 2019, Stephen Whitlock"
__license__ = "MIT"
__version__ = "1.0.4"
__maintainer__ = "Stephen Whitlock"
__email__ = "stephen@jshwisolutions.com"
__status__ = "Production"

from typing import Union, Any


class Color(object):
    """Instantiate object with all attributes or set later"""

    keys = ["text", "effect", "background"]

    def __init__(
        self,
        *args: Union[int, str],
        **kwargs: Union[int, str, None, tuple, dict],
    ) -> None:
        """Set class attributes for Color.print() or Color.get()

        effects:
            'none', "bold", 'bright', "underline", "negative"
        colors:
            "black", "red", "green", "yellow",
            "blue", "purple", "cyan", "white"

        :param args:    Single digit ANSI Escape code (second) or string
                        arguments
                        Codes can be entered in any number of arguments
                        - ordered - and the first three integers/strings
                        will be used
                        args take precedence over kwargs
        :param kwargs:  Three specific keys can be used for class
                        attributes: text, effect or background
                        Subclasses of any name can be defined
        """
        self.text = 7
        self.effect = 0
        self.background = 0
        self.set(*args, **kwargs)

    def __getattr__(self, item: str) -> str:
        return item

    def __dir__(self) -> list:
        return [str(item) for item in self.__dict__]

    def pop(self, select: str) -> Any:
        """Remove keypair from __dict__ and return to variable

        :param select:  Key to remove
        :return:        Class dict or None
        """
        for key in list(self.__dict__):
            if select == key and key not in Color.keys:
                popped = self.__dict__[key]
                del self.__dict__[key]
                return popped
        return

    def print(self, *args: Union[str, int], **kwargs: str) -> None:
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows
                        Method behaves just like builtin print()
        :param kwargs:  builtin print() kwargs
        """
        print(self.get(*args), **kwargs)

    def get(self, *args: Union[str, int]) -> Union[str, tuple]:
        """String can be returned as variable(s) for assorted color
        printing or can be printed directly by calling self.print()

        :param args:    Manipulate string(s)
        :return:        Colored string
        """
        esc = "\u001b["
        text = f"3{self.text}"
        background = f"4{self.background}"
        setting = f"{esc}{self.effect};{text};{background}m"
        reset = f"{esc}0;0m"
        if len(args) == 1:
            return setting + args[0] + reset
        arg_list = []
        for arg in args:
            arg_list.append(setting + arg + reset)
        return tuple(arg_list)

    @staticmethod
    def opts(key: str) -> list:
        """Get allowed values paired with text, effect and background

        :param key: Specific key for allowed values
        :return:    effects for effect and colors for text and
                    background
        """
        effects = ["none", "bold", "bright", "underline", "negative"]
        colors = [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "purple",
            "cyan",
            "white",
        ]
        return effects if key == "effect" else colors

    def kwargs__dict__(self, kwargs: dict):
        """Set any gaps in kwargs with the existing class values (not
        subclasses) so as not to override them with the defaults

        :param kwargs:  New kwargs
        :return:        Kwargs with existing attributes for keys not
                        given a value
        """
        for key in self.__dict__:
            if key in Color.keys and key not in kwargs:
                kwargs[key] = self.__dict__[key]
        return kwargs

    @staticmethod
    def assign_kw(key: str, kwargs: dict, opts: list, default: int) -> dict:
        """First statement returns kwargs as is if valid escape code
        provided
        The second will assign the default value to kwargs if invalid
        value is provided
        Otherwise, if keypair is string - but valid - value will be
        converted to integer

        :param key:     Allowed keys: text, effect, background
        :param kwargs:  Original user defined kwargs or empty dict
        :param opts:    Valid options corresponding with key
        :param default: Default integer value if arg invalid or not
                        entered
        :return:        kwargs with default values, original args or
                        string converted to an integer
        """
        if (
            key in kwargs
            and isinstance(kwargs[key], int)
            and kwargs[key] <= len(opts)
        ):
            return kwargs
        if key not in kwargs or key in kwargs and kwargs[key] not in opts:
            kwargs.update({key: default})
        elif kwargs[key] in opts:
            kwargs.update({key: opts.index(kwargs[key])})
        return kwargs

    def get_processed(self, args: tuple, kwargs: dict) -> dict:
        """Organise args and kwargs into a parsable dictionary

        :param args:    User defined arguments: list(s) of integers or
                        tuple of strings
        :param kwargs:  Keyword arguments for class attributes or subclass
                        attributes
        :return:        Dictionary for class attributes
        """
        for index_, key in enumerate(Color.keys):
            default = 7 if key == "text" else 0
            opts = self.opts(key)
            if 0 <= index_ < len(args):
                kwargs.update({key: args[index_]})
            kwargs = self.assign_kw(key, kwargs, opts, default)
        return kwargs

    def make_subclass(self, args: tuple, kwargs: dict) -> bool:
        """Compile the dictionary to be used as values for new class
        Returned list and dict will replace the arg and kwarg parameters

        :param args:    Class args for Color subclass
        :param kwargs:  Class kwargs for Color subclass
        :return:        Validated dictionary for class __dict__
        """
        sub = False
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                value = self.get_processed(args, value)
                color = Color(*args, **value)
                setattr(self, key, color)
                sub = True
        return sub

    def switch_bold(self):
        """Instantiate bold class object if bold is not set for more
        flexible usage and less setting up when using this module
        """
        kwargs = {
            "bold": {
                "text": self.__dict__["text"],
                "effect": "bold",
                "background": self.__dict__["background"],
            }
        }
        self.make_subclass((), kwargs)

    def class_kwargs(self, args: Union[tuple, list], kwargs: dict) -> None:
        if not self.make_subclass(args, kwargs):
            kwargs = self.get_processed(args, kwargs)
            self.__dict__.update(kwargs)

    @staticmethod
    def process_args(args: Any) -> list:
        """e.g. instead of text="red", effect="bold", background="blue"
        114 would get the same result

        :param args:    Integer list or individual args
        :return:        List to later be iterated through for arguments
        """
        values = []
        for arg in args:
            if isinstance(arg, int):
                items = list(str(arg))
                for item in items:
                    values.append(int(item))
            else:
                values.append(arg)
        return values

    @staticmethod
    def get_nest_dict(key: str, args: list, kwargs: dict) -> dict:
        """Run through corresponding allowed keys against the length of
        the processed args list and assign ordered list indices to each
        key
        Kwargs will be Color’s kwargs argument for class instance
        subclass

        :param key:     Allowed keys: text, effect, background
        :param args:    Validated user arguments
        :param kwargs:  Kwargs dict[key] to add nested subclass dict to
        :return:        Kwargs for subclass __dict__
        """
        ints = {}
        for index_, sub_key in enumerate(Color.keys):
            if 0 <= index_ < len(args):
                ints.update({sub_key: args[index_]})
            kwargs[key] = ints
        return kwargs

    def class_ints(self, kwargs: dict) -> dict:
        """Resolves values which may not be entered as tuples, and
        therefore will confuse the class methods which are expecting
        args

        :param kwargs:  Subclass dictionary
        :return:        Subclass dictionary with processed tuple as args
        """
        for key, value in list(kwargs.items()):
            if not isinstance(value, dict) and key not in Color.keys:
                if not isinstance(value, tuple):
                    value = (value,)
                args = self.process_args(value)
                kwargs = self.get_nest_dict(key, args, kwargs)
        return kwargs

    def set(self, *args: Any, **kwargs: Any) -> None:
        """Call to change/update/add class values or add subclasses for
        new text, effects and backgrounds

        :param args:    Integer escape codes or strings to be converted
                        into escape codes
        :param kwargs:  More precise keyword arguments
        """
        kwargs = self.kwargs__dict__(kwargs)
        kwargs = self.class_ints(kwargs)
        args = self.process_args(args)
        self.class_kwargs(args, kwargs)
        if self.effect != 1:
            self.switch_bold()
