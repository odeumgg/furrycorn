# Furrycorn

Custom-made Battlerite API access framework.


## Rationale

Although the Madglory BattleRite API is built on the jsonapi standard, the
author of this library couldn't find an implementation he liked.

This library is an express opinion the best way to consume the BattleRite API.


## Type Fetishism

This library tries its hardest to ensure the main source of complexity is the
composition of types. Side effects (operations which are dangerous to repeat)
are kept obvious and at a minimum.

A note to readers of this code:

The author of this file (@onethirtyfive) has a bias for coding in a
functional style. Emphasis is put on:

1. Immutabie and domain-specific data types. Where built-in Python
   collection types like "dict" and "list" are used, the variable names are
   prefixed for explicitness. (Otherwise, assume a custom type is present
   for the value.) No prefix type-hinting is attempted for primitives like
   'int' and 'str'.
2. Composition of simpler types into more complex types.
3. Explicit optionality--if a value can be None, its name must start with
   "maybe\_". "null", or optional data, is a huge source of bugs in code.
4. No shared mutable state.

The code may not be as performant as conventional, stateful code, but it
will be easier to maintain.

There will be a conventional OO API for accessing high-level BR data.


## Usage

For now, see `examples/usage.py`.


More documentation forthcoming...
