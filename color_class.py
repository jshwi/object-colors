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
    def __init__(self, *args: Any, **kwargs: Union[str, int, dict]):
        """Set desired attributes for Color.print() or Color.get()

        :param args:    Codes can be entered in any number of arguments
                        The first three integers/strings will be used
        :param kwargs:  Three specific keys can be used
                        color, effect, background
        """
        self.add(*args, **kwargs)

    def add(self, *args: Any, **kwargs: Union[str, int, dict]):
        """

        :param args:
        :param kwargs:
        """
        self.__dict__ = self.process_args_kwargs(args, kwargs)

    @staticmethod
    def process_args(args: Any) -> list:
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
        value = {}
        data = self.__dict__
        for key, val in list(kwargs.items()):
            if isinstance(val, dict):
                val = self.process_kwargs(args, val)
                value[key] = Color(*args, **val)
                data.update({key: value[key]})
            else:
                data.update(self.process_kwargs(args, kwargs))
        return data

    def process_kwargs(self, args: Any, kwargs: dict) -> dict:
        """Organise arguments and keyword arguments into a valid
        dictionary

        :param args:    User defined arguments: list(s) of integers or
                        tuple of strings
        :param kwargs:  Keyword arguments for class attributes or new
                        subclass attributes
        :return:        Dictionary for class attributes
        """
        args = self.process_args(args)
        keys = ["color", "effect", "background"]
        for idx, key in enumerate(keys):
            opts = self.get_opts(key)
            # set default value
            val = 0 if key == "effect" else 9
            if 0 <= idx < len(args):
                val = args[idx]  # valid argument
            elif key in kwargs and kwargs[key] in opts:
                val = kwargs[key]  # valid keyword argument
            elif key in kwargs and 0 <= idx < len(opts):
                continue  # valid value already set
            # if val is a string return its index value for escape code
            val = opts.index(val) if isinstance(val, str) else val
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
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows so this method behaves just like
                        the __builtin__
        :param kwargs:  Keyword arguments for print() function
        """
        print(self.get(" ".join(str(string) for string in args)), **kwargs)

    def get_key_values(self) -> dict:
        """Resolve type errors for the various types that the class may
        contain so that they may be printed as a string

        :return: Temporary key values to be printed in a readable form
        """
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
        return key_values

    def vals(self):
        """Used for debugging: Print class dict as json"""
        key_values = self.get_key_values()
        while True:
            try:
                print(dumps(key_values, indent=4, sort_keys=True))
                break
            except TypeError:
                for key, value in key_values.items():
                    try:
                        value = value.__dict__
                        key_values[key] = value
                    except AttributeError:
                        continue
