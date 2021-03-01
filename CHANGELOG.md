# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased](https://github.com/jshwi/object_colors/compare/v1.0.8...HEAD)
------------------------------------------------------------------------
### Added
- Adds ``colorama`` for ``Windows`` systems
- Overrides ``__repr__``
- Adds string formatter to ``get``
- Adds ``populate`` for all elements
- Raises ``TypeError`` if setting invalid attribute name
- Raises ``IndexError`` if setting of range ``int`` attributes
- Raises ``TypeError`` if setting invalid attribute type

### Changed
- Renames: `` text`` -> ``fore``,  ``background`` -> ``back``
- Renames: `` purple`` -> ``magenta``
- Moves: ``_get_processed`` -> ``__setattr__``

### Deprecated
- ``populate_colors`` is deprecated in favour of ``populate("fore")``

### Removed
- Removes multicolor feature
- Removes ``pop`` method
- Removes functionality to pass single {1,2,3} digit number as {1,2,3} arg(s)

### Fixed
- Fixes ``print`` method to mirror builtin
- Removes default black background for none
- Adds all effects
- Objects can be properly added with ``__setattr__``

[v1.0.8](https://github.com/jshwi/object_colors/releases/tag/v1.0.8)  - 2020-02-02
------------------------------------------------------------------------
### Added
- Adds method to get multicoloured strings
- Makes some methods & variables public for more manual configuration
  
### Changed
- Updates README.rst 

[v1.0.7](https://github.com/jshwi/object_colors/releases/tag/v1.0.7) - 2020-01-31
------------------------------------------------------------------------
### Added
- Adds ignore-case / scatter search
- Adds Individual word coloring
- All characters (including tildes / backslashes) searchable

### Removed
- Removes get_nested() method (now useless)

### Fixed
- "Ignore_case" fully functional 

[v1.0.6](https://github.com/jshwi/object_colors/releases/tag/v1.0.6) - 2019-12-07
------------------------------------------------------------------------
### Changed
- Change ``populate_colors`` arg: "colors" -> populate=True 

[v1.0.5](https://github.com/jshwi/object_colors/releases/tag/v1.0.5) - 2019-11-10
------------------------------------------------------------------------
#### Added
- Adds ``populate_colors`` method

[v1.0.4](https://github.com/jshwi/object_colors/releases/tag/v1.0.4) - 2019-11-09
------------------------------------------------------------------------
### Added
- Adds additional bold switch for more flexible use
- Adds unpack tuple feature to self.get() 
- Adds full pop() return test module 

### Changed
- Updates docs structure 

[v1.0.3](https://github.com/jshwi/object_colors/releases/tag/v1.0.3) - 2019-10-08
------------------------------------------------------------------------
### Fix
- New Python unicode characters no longer cause build to fail

[v1.0.2](https://github.com/jshwi/object_colors/releases/tag/v1.0.2)  - 2019-10-07
------------------------------------------------------------------------
### Added
- Can now instantiate several subclasses at once
- Uses set() without overwriting previous values 
- Made keys list global (class scope) 
- Adds subclass tests

### Changed
- Updates docs

### Fixed
- Valid integers no longer missed in main loop 

[v1.0.1](https://github.com/jshwi/object_colors/releases/tag/v1.0.1) - 2019-10-03
------------------------------------------------------------------------
### Added
- Adds delete keypair method
- Adds docs
- Adds setup.py
- Can now create separate color objects and add new ones 
- Adds test suite

### Changed
- Updates README.md

### Fixed
- Resolves unresolved references/attributes 
