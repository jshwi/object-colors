<!--
This file is auto-generated and any changes made to it will be overwritten
-->
# tests

## tests._test


### All fields(color: [object colors.color]

Test fields are properly returned with semicolon for str.


### Get

Test returning a simple string with effects and colors.


### Get no key(color: [object colors.color]

Test `AttributeError` raised for invalid value to `get`.


### Index error kwargs

Test `IndexError` raised for out-of-range integer.


### Key error(color: [object colors.color]

Test `AttributeError` raised for invalid keyword arguments.


### Len(color: [object colors.color]

Test correct length of `color._objects` is returned.


### Populate colors(color: [object colors.color]

Test for expected str when `get` is used within color subclass.


### Populate colors deprecated(color: [object colors.color]

Test `populate_colors` properly sets attributes.


### Populate err(color: [object colors.color]

Test `AttributeError` raised for invalid value to `populate`.


### Print

Test printing a simple string with effects and colors.


### Print non str(capsys:  pytest.capture.capturefixture, color: [object colors.color]

Test printing of any objects.


### Print nothing(color: [object colors.color]

Test no error is raised when printing nothing.


### Repr(color: [object colors.color]

Test output from `__repr__`.


### Set dynamic(color: [object colors.color]

Test a subclass can be set with `set`.


### Set invalid(color: [object colors.color]

Test `AttributeError` raised for non-existing attribute.


### Set static(color: [object colors.color]

Test existing instance attribute can be set with  `set`.


### Type error kwargs

Test `TypeError` raised when for invalid type.


### Value error kwargs

Test `ValueError` raised for invalid keyword argument.


