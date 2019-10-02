#!/usr/bin/env python3
"""object_colors

This is a simple to use module designed to print to the terminal in
color with minimal setup and instantiation
"""
from typing import Union, Any
__author__ = "Stephen Whitlock"
__copyright__ = "Copyright 2019, Stephen Whitlock"
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Stephen Whitlock"
__email__ = "stephen@jshwisolutions.com"
__status__ = "Production"


class Color:
    """Instantiate with escape codes, values or key-values and get or
    print processed arguments
    """
    def __init__(self, *args: Any, **kwargs: Union[str, int, dict]):
        """Set class attributes for Color.print() or Color.get()

        keys:
            "color", "effect", "background"
        effects:
            None, "bold", "underline", "negative"
        colors:
            "black", "red", "green", "yellow", "blue", "purple", "cyan"

        :param args:    Codes can be entered in any number of arguments
                        The first three integers/strings will be used
        :param kwargs:  Three specific keys can be used
                        color, effect, background for class kwargs,
                        though subclasses can also be added
        """
        self.color = 9
        self.effect = 0
        self.background = 9
        self.set(*args, **kwargs)

    def __getattr__(self, item: str) -> str:
        return item

    def __dir__(self) -> list:
        """Override the __dir__ method to resolve dynamic attributes
        Especially useful when using an IDE like  PyCharm

        :return:    list of attributes - dynamic and static
        """
        return [str(item) for item in self.__dict__]

    def set(self, *args: Any, **kwargs: Union[str, int, dict]):
        """Call to change class values, or add new subclasses of
        separate colors, effects and backgrounds

        :param args:    Integer escape codes or strings to be converted
                        into escape codes
        :param kwargs:  Be more precise with keyword arguments
        """
        keys = ["color", "effect", "background"]
        self.process_args_kwargs(keys, args, kwargs)

    def get(self, string: str) -> str:
        """String can be return as variables for mixed printing or can
        be printed directly by calling Color.print() instead of
        Color.get()

        :param string:  User args to be processed
        :return:        Colored string
        """
        esc = "\033["
        reset = f"{esc}0;0m"
        text = f"3{self.color}"
        background = f"4{self.background}"
        setting = f"{esc}{self.effect};{text};{background}m"
        return setting + string + reset

    def print(self, *args: Any, **kwargs: Union[str, int]):
        """Enhanced print function for class and subclasses

        :param args:    Variable number of strings can be entered if
                        syntax allows so this method behaves just like
                        the __builtin__
        :param kwargs:  Keyword arguments for print() function
        """
        print(self.get(" ".join(str(string) for string in args)), **kwargs)

    def pop(self, select: str) -> Union[str, dict, None]:
        """Delete key and value from list and return them to a variable,
        if that's what you want to do...

        :param select:  Key selection to delete
        :return:        Dictionary item if removing class, str if a
                        keypair and None if there was nothing to remove
        """
        for key in list(self.__dict__):
            if select == key:
                popped = self.__dict__[key]
                del self.__dict__[key]
                if isinstance(popped, Color):
                    return {key: popped.__dict__}
                return popped
        return

    def class_ints(self, keys: list, kwargs: dict) -> dict:
        """Resolves values which may not be entered as tuples, and
        therefore will confuse the class methods which are expecting
        args

        :param keys:    Valid keys for kwargs
        :param kwargs:  Subclass dictionary
        :return:        Subclass dictionary with processed tuple as args
        """
        for key, value in list(kwargs.items()):
            if (not isinstance(value, dict) and not isinstance(value, tuple)
                    and key not in keys):
                args = self.process_args((value,))
                ints = {}
                for index_, sub_key in enumerate(keys):
                    if 0 <= index_ < len(args):
                        ints.update({sub_key: args[index_]})
                    kwargs[key] = ints
        return kwargs

    def process_args_kwargs(self, keys: list, args: Any, kwargs: dict) -> None:
        """Compile the dictionary to be used as values for get and print

        :param keys:
        :param args:    Class arguments
        :param kwargs:  Class keyword-arguments
                        Returned list and dict will replace the arg and
                        kwarg parameters
        :return:        Validated dictionary for class __dict__
        """
        kwargs = self.class_ints(keys, kwargs)
        args = self.process_args(args)
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                value = self.process_kwargs(keys, args, value)
                color = Color(*args, **value)
                setattr(self, key, color)
                return
        kwargs = self.process_kwargs(keys, args, kwargs)
        self.__dict__.update(kwargs)
        return

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
    def process_kwargs(keys: list, args: Any, kwargs: dict) -> dict:
        """Organise arguments and keyword arguments into a valid
        dictionary

        :param keys:    Allow keys for kwargs
        :param args:    User defined arguments: list(s) of integers or
                        tuple of strings
        :param kwargs:  Keyword arguments for class attributes or new
                        subclass attributes
        :return:        Dictionary for class attributes
        """
        effects = [None, "bold", "underline", "negative"]
        colors = ["black", "red", "green", "yellow", "blue", "purple", "cyan"]
        for index_, key in enumerate(keys):
            opts = effects if key == "effect" else colors
            value = 0 if key == "effect" else 9
            if 0 <= index_ < len(args):
                value = args[index_]
            elif key in kwargs and kwargs[key] in opts:
                value = kwargs[key]
            elif key in kwargs and 0 <= index_ < len(opts):
                # keypair will be assigned default values if incorrect
                # value is given or value will be maintained if key
                # was not an argument to avoid a key error below
                if isinstance(kwargs[key], str):
                    kwargs[key] = value
                continue
            value = opts.index(value) if isinstance(value, str) else value
            kwargs.update({key: value})
        return kwargs
