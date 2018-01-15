from collections import namedtuple


class Config(namedtuple('Config', ['origin', 'api_key', 'maybe_logger'])):
    """Configuration for interacting with SLS API."""

    __slots__ = ()

    def __new__(cls, origin, api_key, maybe_logger=None):
        return super(Config, cls).__new__(cls, origin, api_key,
                                          maybe_logger=None)


def mk(origin, api_key, maybe_config=None):
    return Config(origin, api_key, maybe_config)

