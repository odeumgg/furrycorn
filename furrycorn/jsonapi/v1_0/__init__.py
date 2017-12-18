from collections import namedtuple
from enum import Enum

from .common import meta
from . import data, errors, included, jsonapi, links


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


class Root(namedtuple('Root', ['any_data_or_errors_or_meta',
                               'maybe_either_data_or_errors', 'maybe_meta',
                               'maybe_jsonapi', 'maybe_links',
                               'maybe_included'])):
    """
    Representation of an entire response.

    There can be *either* an RootData or RootErrors, not both. Or
    neither. There can be always be a Meta. There must be one of the three.

    'any_data_or_errors_or_meta' preferentially contains the RootData or
    RootErrors; otherwise, the Meta. It must be a value other than None.
    """

    __slots__ = ()

    def __new__(cls, any_data_or_errors_or_meta,
                maybe_either_data_or_errors=None, maybe_meta=None,
                maybe_jsonapi=None, maybe_links=None, maybe_included=None):
        return super(Root, cls).__new__(cls, any_data_or_errors_or_meta,
                                        maybe_either_data_or_errors,
                                        maybe_meta, maybe_jsonapi, maybe_links,
                                        maybe_included)


def mk_config(mode, maybe_logger=None):
    return Config(mode, maybe_logger)


def parse(obj, config):
    if 'data' in obj and 'errors' in obj:
        raise RuntimeError('response cannot contain both data and errors')

    if 'data' not in obj and 'errors' not in obj and 'meta' not in obj:
        raise RuntimeError('response must contain data, errors, or meta (1)')

    maybe_data = data.mk(obj['data'], config) if 'data' in obj else None

    if 'errors' in obj:
        maybe_errors = errors.mk(obj['errors'], config)
    else:
        maybe_errors = None

    maybe_meta = meta.mk(obj['meta'], config) if 'meta' in obj else None

    if 'jsonapi' in obj:
        maybe_jsonapi = jsonapi.mk(obj['jsonapi'], config)
    else:
        maybe_jsonapi = None

    maybe_links = links.mk(obj['links'], config) if 'links' in obj else None

    if 'included' in obj:
        maybe_included = included.mk(obj['included'], config)
    else:
        maybe_included = None

    any_data_or_errors_or_meta = maybe_data or maybe_errors or maybe_meta

    if not any_data_or_errors_or_meta:
        raise RuntimeError('response must contain data, errors, or meta (2)')

    maybe_either_data_or_errors = maybe_data or maybe_errors

    return Root(any_data_or_errors_or_meta, maybe_either_data_or_errors,
                maybe_meta, maybe_jsonapi, maybe_links, maybe_included)

