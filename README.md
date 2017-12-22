# Furrycorn

Easily navigate [jsonapi](http://jsonapi.org/) responses.

(Compatible with Battlerite API!)


## Status

At a high level, this library provides:

1. a DOM-like runtime representation of jsonapi response bodies.
2. a toolkit for interpreting these structures and traversing relationships.
3. a URL abstraction for interacting with services hosting jsonapi APIs.

Heavy testing is needed before we publish to PyPI.

Developed exclusively on Python 3.6. Compatibility with other versions to be
investigated later.

## Installing

Installation should be a breeze using [pipenv](https://docs.pipenv.org/).

If you're one of the three people using [nixos](https://nixos.org), you can
simply boot a `nix-shell` to be off to the races.

For the rest of the world:

1. Clone the directory and navigate to your local repo in a command line.
2. `pipenv intall --three` (tested only with Python 3!)
3. `pipenv shell`

You will need to set one environment variable to see the example run:

`FURRYCORN_API_KEY` must be set to your [Battlerite Developer Portal](https://developer.battlerite.com) account's
API key.

We had no luck doing this on the command line in Windows. The var needed
to be added via "My Computer > Properties > Advanced > Environment Variables".
There's a graphical interface for adding them.

In Linux/Unix systems, you can simply do:

`export FURRYCORN_API_KEY="PASTEYOURKEYHERE"`

After that's taken care of, in your project dir, simply:

`python examples/battlerite.py`


## A Note About Code Style

The author of this library prefers a functional style of coding which centers
on exploding the set of "types" defined in the system. This project makes only
limited use of the object-oriented capabilities of Python.

It's a lot easier to reason about types than it is logical steps, and given
the highly structured nature of jsonapi, it felt like a good fit.

Feel free to message `/u/onethirtysix` on reddit with any questions or concerns
you have. I'm happy to help if you get stuck on anything while "grokking" or
contributing.

Cheers!


## License

This project is Copyright © 2017 odeum.gg and licensed under the MIT license.
View LICENSE.md for details.

