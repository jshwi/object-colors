"""
object-colors
=============

Object-oriented library for stylizing terminal output.
"""
import builtins

import colorama

__version__ = "1.0.8"


class Color:
    """Color object. Args passed to constructor call may be strings or
    integers. There are a defined set of options for each. The list
    of options referenced below are the string form. The integer that
    can be called is the index of the list item beginning with 0.

    :param effect:  Effect applied to text output. Select from the
                    following :py:attr:`Color.effects`.
    :param fore:    Foreground color applied to text output. Select from
                    the following :py:attr:`Color.colors`.
    :param back:    Background color applied to text output. Select from
                    the following :py:attr:`Color.colors`.
    """

    effects = ("none", "bold", "bright", "underline", "negative")
    colors = (
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    )
    _opts = dict(effect=effects, fore=colors, back=colors)
    colorama.init()

    def __init__(self, effect=0, fore=7, back=None):
        self.effect = effect
        self.fore = fore
        self.back = back
        self.set(effect=self.effect, fore=self.fore, back=self.back)

    def __setattr__(self, key, value):
        """The two types of attributes to set are the object's instance
        attributes, and the dynamic object attributes. Standard
        attributes can be either ``int``, ``str``, or ``NoneType``.
        Object values can only be a ``dict`` i.e. ``**kwargs`` to create
        a new object. All ``int`` values correspond to the index of the
        color or effect and their respective ANSI code. All ``str``
        values will be converted to their index integer.

        :param key:         The attribute to set.
        :param value:       The value of the attribute to set.
        :raises ValueError: If ``str`` does not a match a ``str`` in the
                            corresponding tuple.
        """
        if isinstance(value, str):
            value = self._opts[key].index(value)

        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        """Look up dynamic subclasses.

        :param item: Item to lookup and return.
        """
        return item

    def __dir__(self):
        """Primarily here so linters know that the subclass calling
        methods are not strings attempting to call attributes.
        """
        return tuple([str(item) for item in self.__dict__])

    def __repr__(self):
        """View the containing attributes within the ``str``
        representation.

        :return:  ``str`` representation of this class.
        """
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                "{}={}".format(k, v)
                if not isinstance(v, dict)
                else "objects({})".format(", ".join(v))
                for k, v in vars(self).items()
            ),
        )

    def _get_colored_str(self, _str):
        """Compile and return ANSI escaped string.

        :param _str:    Regular ``str`` object.
        :return:        ``str`` with escape codes added.
        """
        return "\u001b[{};3{}{}m{}\u001b[0;0m".format(
            self.effect,
            self.fore,
            f";4{self.back}" if self.back is not None else "",
            _str,
        )

    def _make_subclass(self, **kwargs):
        """Make subclass attribute and return boolean value so method.
        Calling this method can determine whether subclass has
        successfully been made. Set subclass as an instance attribute so
        dynamic names are recognised as correct attributes belonging to
        class.

        :key effect:    Text effect to use.
        :key fore:      Color of text foreground.
        :key back:      Color of text background.
        :key dict:      A subset of the above arguments assigned to a
                        key that they subclass will be named after.
        :return:        bool: Whether the ``if`` condition below
                        succeeded.
        """
        for key, value in list(kwargs.items()):
            if isinstance(value, dict):
                color = Color(**value)
                setattr(self, key, color)
                return True

        return False

    def populate_colors(self):
        """This will create a subclass for every available color"""
        for color in self.colors:
            kwargs = {color: {"fore": color}}
            self._make_subclass(**kwargs)

    def set(self, **kwargs):
        """Call to set new instance values. If not making a subclass
        then process args and kwargs and add compiled dict to
        masterclass.

        :key effect:    Text effect to use.
        :key fore:      Color of text foreground.
        :key back:      Color of text background.
        :key ``dict``:  If ``**kwargs`` are provided then any keyword
                        can be provided.
        """
        if not self._make_subclass(**kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        # bold switch:
        # - if used in a class instantiated as bold, switch bold off
        # - if used in a class instantiated without bold, switch bold on
        if self.effect != 1:

            # Instantiate bold class object if bold is not set for more
            # flexible usage and less setting up when using this module
            # to manipulate particular colored strings
            self._make_subclass(
                bold={
                    "fore": self.__dict__["fore"],
                    "effect": "bold",
                    "back": self.__dict__["back"],
                }
            )

    def get(self, *args, **kwargs):
        """Return colored ``str`` or ``tuple`` depending on the arg
        passed to method.

        :param args:    Manipulate string(s).
        :key format:    Return a string instead of a tuple if strings
                        are passed as tuple.
        :return:        Colored string.
        """
        if len(args) > 1:
            if kwargs.get("format", False):
                return self._get_colored_str(" ".join(args))

            return tuple(self._get_colored_str(i) for i in list(args))

        return self._get_colored_str(args[0])

    def print(self, *args, **kwargs):
        """Print colored strings using the builtin ``print`` function.

        :param args:    String(s) to print.
        :key file:      A file-like object (stream); defaults to the
                        current sys.stdout.
        :key sep:       String inserted between values, default a space.
        :key end:       String appended after the last value, default a
                        newline.
        :key flush:     Whether to forcibly flush the stream.
        """
        builtins.print(self.get(*args, format=True), **kwargs)
