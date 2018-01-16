Furrycorn: JSONAPI v1.0 Parser
==============================

Furrycorn is intended to make interacting with jsonapi-outputting APIs easier
to consume. It is opinionated but lienient when possible, failing fast when
things go awry.

To understand how to use this library, you will need some knowledge of the
`jsonapi v1.0 specification <http://jsonapi.org/format/>`_.

Furrycorn provides:

1. a URL abstraction for interacting with services hosting jsonapi APIs.
2. a DOM-like object model of entities in jsonapi response bodies.
3. a toolkit for relationship traversal and entity iteration.

*The core model is well-tested, but not the toolkit--furrycorn is still in
active development.*

Compatible with Python 3.6+. Will investigate other versions on request.


Installation
------------

``pip install furrycorn`` should do it for your projects.


Development
-----------

Requirement setup should be a breeze using `pipenv <https://docs.pipenv.org/>`_.

If you're using `nixos <https://nixos.org>`_, simply boot a ``nix-shell`` in the
project directory to get a development shell.

For the rest of the world:

1. Clone the directory and navigate to your local repo in a command line.
2. ``pipenv install --three``
3. ``pipenv shell``

You will need to set one or two environment variables to use the examples,
depending on the example. The methodology for doing this varies by OS.

For development, make sure ``PYTHONPATH`` includes the project root. Run tests
with ``py.test``.

Pleas submit changes by pull request on an *aptly named topic branch*.


Code Style
----------

The author of this library prefers a functional style of coding which centers
on "types". It's a lot easier to reason about types than logical steps, and
given the highly structured nature of jsonapi, it felt like a good fit.

Feel free to message with any questions you have. I'm happy to help and explain.


License
-------

This project is Copyright © 2018 odeum.gg and licensed under the MIT license.
View `the license <https://github.com/odeumgg/furrycorn/blob/master/LICENSE>`_
for details.

