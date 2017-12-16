from collections import namedtuple
from enum import Enum


class Mode(Enum):
    """
    Describes parsing methodology. All modes will fail with exceptions on
    irredeemably bad input. For less bad input:

    LENIENT:   Recommended for non-comformant APIs. Logs WARN messages on
               unexpected input. Logging requires logger instance in Config.
               Output may cause unexpected problems when used in toolkit.
    STRICT:    Recommended for conformant APIs. Raises on unexpected input.
               Output should always work when used in toolkit.
    """
    LENIENT   = 1
    STRICT    = 2


class Config(namedtuple('Config', ['mode', 'maybe_logger'])):
    """Library configuration used for parsing and toolkit."""

    __slots__ = ()

    def __new__(cls, mode, maybe_logger):
        return super(Config, cls).__new__(cls, mode, maybe_logger)


def mk_config(mode, maybe_logger=None):
    return Config(mode, maybe_logger)

