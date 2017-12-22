from collections import namedtuple


class Config(namedtuple('Config', ['origin', 'api_key'])):
    """Configuration for interacting with SLS API."""

    __slots__ = ()

    def __new__(cls, origin, api_key):
        return super(Config, cls).__new__(cls, origin, api_key)


def mk(origin, api_key):
    return Config(origin, api_key)

