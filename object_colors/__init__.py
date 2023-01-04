"""Object-oriented library for stylizing terminal output."""
from __future__ import annotations

import builtins as _builtins
import typing as _t

import colorama as _colorama

__version__ = "2.2.0"

EffectTuple = _t.Tuple[str, str, str, str, str, str, str, str, str, str]
ColorTuple = _t.Tuple[str, str, str, str, str, str, str, str]


class Color:
    """Color object.

    Args passed to constructor call may be strings or integers. There
    are a defined set of options for each.

    The list of options referenced below are the string form.

    The integer that can be called is the index of the list item
    beginning.

    The two types of attributes to set are the object's instance
    attributes, and the dynamic object attributes.

    Standard attributes can be either int, str, or None.

    Object values can only be a dict to create a new object.

    All int values correspond to the index of the color or effect and
    their respective ANSI code.

    All str values will be converted to their index integer.

    Ensure int passed as parameter does not exceed the length of the
    key's index.

    Ensure str is one of the specific strings matching the key's index.

    If a key does not match ``effect``, ``fore``, or ``back`` it must be
    a dict which can be instantiated to create a new named object.

    @DynamicAttrs

    :param effect: Effect applied to text output. Select from the
        following :py:attr:`Color.effects`.
    :param fore: Foreground color applied to text output. Select from
        the following :py:attr:`Color.colors`.
    :param back: Background color applied to text output. Select from
        the following :py:attr:`Color.colors`.
    """

    effects: EffectTuple = (
        "none",
        "bold",
        "dim",
        "italic",
        "underline",
        "blink",
        "blinking",
        "negative",
        "empty",
        "strikethrough",
    )
    colors: ColorTuple = (
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    )
    _opts: _t.Dict[str, _t.Union[EffectTuple, ColorTuple]] = dict(
        effect=effects, fore=colors, back=colors
    )
    _colorama.init()

    def __init__(
        self,
        effect: _t.Optional[_t.Union[int, str]] = None,
        fore: _t.Optional[_t.Union[int, str]] = None,
        back: _t.Optional[_t.Union[int, str]] = None,
    ) -> None:
        self.effect = effect
        self.fore = fore
        self.back = back

        #: prevents infinite recursion when set
        super().__setattr__("_objects", {})

    def __setattr__(
        self,
        key: str,
        value: _t.Optional[_t.Union[int, str, _t.Dict[str, _t.Any]]],
    ) -> None:
        if key in self._opts:
            if isinstance(value, int):
                if value > len(self._opts[key]):
                    raise IndexError("tuple index out of range")

            elif isinstance(value, str):
                try:
                    value = self._opts[key].index(value)

                except ValueError as err:
                    raise ValueError(
                        f"'{value}' cannot be assigned to '{key}'"
                    ) from err

            elif value is not None:
                raise TypeError(
                    "expected int, str, or NoneType, not {}".format(
                        type(value).__name__
                    )
                )

            super().__setattr__(key, value)
        else:
            if not isinstance(value, dict):
                raise TypeError(f"got an unexpected keyword argument '{key}'")

            self._objects[key] = self.__class__(**value)

    def __getattribute__(self, key: str) -> _t.Any:
        """Attempt to return the attribute matching the key.

        If no attribute can be found search ``_objects`` for objects.

        If neither of the above can yield a result then raise
        ``AttributeError`` error.

        :param key: The attribute to get.
        :raises AttributeError: Raise if no instance attribute or
            objects can be returned with the given key.
        :return: The retrieved attribute.
        """
        try:
            return super().__getattribute__(key)

        except AttributeError as err:
            try:
                return self._objects[key]

            except KeyError:
                raise AttributeError(err) from err

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                f"{k}={v}"
                if not isinstance(v, dict)
                else "objects({})".format(", ".join(v))
                for k, v in vars(self).items()
            ),
        )

    def __len__(self) -> int:
        return len(self._objects)

    def _color_str(self, string: str) -> str:
        """Compile and return ANSI escaped str.

        If parameters are not provided return a regular str.

        :param string: Regular ``str`` object.
        :return: str with escape codes added or the regular str if None
            provided.
        """
        sequence: _t.List[str] = []
        keys = tuple(self._opts.keys())
        for count, key in enumerate(keys):
            attr = getattr(self, key)
            last = count == len(keys) - 1
            if attr is not None:
                if not sequence:
                    sequence.extend(["\u001b[", "\u001b[0;0m"])

                elif not last:
                    sequence.insert(len(sequence) - 1, ";")

                prefix = count + 2 if count > 0 else ""
                sequence.insert(len(sequence) - 1, f"{prefix}{attr}")

            if last and sequence:
                sequence.insert(len(sequence) - 1, "m")

        sequence.insert(len(sequence) - 1, string)
        return "".join(str(i) for i in sequence)

    def populate(self, elem: str) -> None:
        """Create an object for every available selection.

        :param elem: Attribute to fill with available options.
        :raises AttributeError: If element does not exist.
        """
        kwargs = {k: v for k, v in vars(self).items() if not k.startswith("_")}
        try:
            for item in self._opts[elem]:
                kwargs[elem] = item
                setattr(self, item, kwargs)

        except KeyError as err:
            raise AttributeError(
                f"'{type(self).__name__}' has no attribute '{elem}'"
            ) from err

    def populate_colors(self) -> None:
        """Create an object for every available foreground color.

        Deprecated.
        """
        self.populate("fore")
        for color in self.colors:
            getattr(self, color).populate("effect")

    def set(self, **kwargs: _t.Union[str, int, _t.Dict[str, _t.Any]]) -> None:
        """Call to set new instance values.

        If not making a subclass then process args and kwargs and add
        compiled dict to masterclass.

        :key effect: Text effect to use.
        :key fore: Color of text foreground.
        :key back: Color of text background.
        :key dict: If ``**kwargs`` are provided then any keyword can
            be provided.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, *args: _t.Any, **kwargs: bool) -> _t.Any:
        """Return colored str or tuple depending on the arg passed.

        :param args: Manipulate string(s).
        :key format: Return a string instead of a tuple if strings are
            passed as tuple.
        :return: Colored string or None.
        """
        if len(args) > 1:
            if kwargs.get("format", False):
                return self._color_str(" ".join(str(i) for i in args))

            return tuple(self._color_str(i) for i in list(args))

        if len(args) == 1:
            return self._color_str(args[0])

        return None

    def print(self, *args: _t.Any, **kwargs: _t.Any) -> None:
        """Print colored strings using the builtin ``print`` function.

        :param args: String(s) to print.
        :key file: A file-like object (stream); defaults to the current
            sys.stdout.
        :key sep: String inserted between values, default a space.
        :key end: String appended after the last value, default a
            newline.
        :key flush: Whether to forcibly flush the stream.
        """
        args = self.get(*args, format=True)
        if args is not None:
            _builtins.print(args, **kwargs)
