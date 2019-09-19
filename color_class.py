#!/usr/bin/env python3
"""color_class

This is a simple to use module designed to print to the terminal in
color with minimal setup and instantiation
"""
from json import dumps
from typing import Union, Any


class Color:
    """Instantiate with escape codes, values or key-values and get or
    print processed arguments
    """

    def __init__(self, *args: Union[str, int], **kwargs: Union[str, int]):
        """Set desired attributes for Color.print() or Color.get()

        :param args:    Codes can be entered in any number of arguments
                        The first three integers/strings will be used
        :param kwargs:  Three specific keys can be used
                        color, effect, background
        """
        self.__dict__ = self.process_args_kwargs(args, kwargs)

    @staticmethod
    def process_args(args) -> list:
        """e.g. instead of color="red", effect="bold", background="blue"
        114 will get the same result

        :param args:    Integer list or individual args
        :return:        List to be iterated through for arguments
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
    def get_opts(key: str) -> list:
        """Match against args then convert to int for escape codes

        :param key: Keyword to match with list of valid arguments
        :return:    List to validate argument
        """
        if key == 'effect':
            return [None, "bold", "underline", "negative"]
        return ["black", "red", "green", "yellow", "blue", "purple", "cyan"]

    def process_args_kwargs(self, args: Any, kwargs: dict) -> dict:
        """Compile the dictionary to be used as values for get and print

        :param args:    Class arguments
        :param kwargs   Class keyword-arguments
                        returned list and dict will replace the arg and
                        kwarg parameters
        :return:        validated dictionary for class __dict__
        """
        args = self.process_args(args)
        keys = ["color", "effect", "background"]
        for idx, key in enumerate(keys):
            opts = self.get_opts(key)
            default = 9 if key == "effect" else 0
            if key in kwargs and kwargs[key] in opts:
                val = kwargs[key]
            elif 0 <= idx < len(args):
                val = args[idx]
            elif key in kwargs and 0 <= idx < len(opts):
                # valid value already set
                continue
            else:
                val = default
            val = opts.index(val) if isinstance(val, str) else val
            if not val or val >= len(opts):
                val = default
            kwargs.update({key: val})
        return kwargs

    def get(self, string: str) -> str:
        """String can be return as variables for mixed printing or can
        be printed directly by calling Color.print() instead of
        Color.get()

        :param string:  User args to be processed
        :return:        Colored string
        """
        kwargs = self.process_args_kwargs([], self.__dict__)
        color = f"3{kwargs['color']}"
        effect = kwargs["effect"]
        background = f"4{kwargs['background']}"
        return f"\033[{effect};{color};{background}m{string}\033[0;0m"

    def print(self, *args: Any, **kwargs: Union[str, int]):
        """

        :param args:    Variable number of strings can be entered if
                        syntax allows so this method behaves just like
                        the __builtin__
        :param kwargs:  Keyword arguments for print() function
        """
        print(self.get(" ".join(str(string) for string in args)), **kwargs)

    def vals(self):
        """Used for debugging: Print class dict as json"""
        key_values = {}
        for key in self.__dict__:
            opts = self.get_opts(key)
            try:
                value = opts[self.__dict__[key]]
            except TypeError:
                value = self.__dict__[key]
            except IndexError:
                value = None
            key_values[key] = value
        self.print(dumps(key_values, indent=4, sort_keys=True))
