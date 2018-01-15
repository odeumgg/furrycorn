from collections import namedtuple

from .common import meta
from ..model import data, errors, included, jsonapi, links


class Root(namedtuple('Root', ['primary', 'maybe_either_data_or_errors',
                               'maybe_meta', 'maybe_jsonapi', 'maybe_links',
                               'maybe_included'])):
    """
    Representation of an entire response.

    'primary' can reference a Data *or* an Errors, but not both. Neither Data
    nor Errors is also acceptable. There can be always be a Meta. One of the
    three must be present.

    'primary' preferentially contains the Data, the Errors, or the Meta, in
    that order.
    """

    __slots__ = ()

    def __new__(cls, primary, maybe_either_data_or_errors=None, maybe_meta=None,
                maybe_jsonapi=None, maybe_links=None, maybe_included=None):
        return super(Root, cls).__new__(cls, primary,
                                        maybe_either_data_or_errors,
                                        maybe_meta, maybe_jsonapi, maybe_links,
                                        maybe_included)


def mk_maybe_data(obj, config):
    if 'data' in obj:
        return data.mk(obj['data'], config)
    else:
        return None


def mk_maybe_errors(obj, config):
    if 'errors' in obj:
        return errors.mk(obj['errors'], config)
    else:
        return None


def mk_maybe_jsonapi(obj, config):
    """Not yet implemented."""

    if 'jsonapi' in obj:
        return jsonapi.mk(obj['jsonapi'], config)
    else:
        return None


def mk_maybe_links(obj, config):
    if 'links' in obj:
        return links.mk(obj['links'], config)
    else:
        return None


def mk_maybe_included(obj, config):
    if 'included' in obj:
        return included.mk(obj['included'], config)
    else:
        return None


def build(obj, config):
    maybe_data     = mk_maybe_data(obj, config)
    maybe_errors   = mk_maybe_errors(obj, config)
    maybe_meta     = meta.mk_maybe(obj, config)
    maybe_jsonapi  = mk_maybe_jsonapi(obj, config)
    maybe_links    = mk_maybe_links(obj, config)
    maybe_included = mk_maybe_included(obj, config)

    if maybe_data and maybe_errors:
        raise RuntimeError('response cannot contain both data and errors')

    primary = maybe_data or maybe_errors or maybe_meta

    if not primary:
        raise RuntimeError('response must contain data, errors, or meta')

    maybe_either_data_or_errors = maybe_data or maybe_errors

    return Root(primary, maybe_either_data_or_errors, maybe_meta,
                maybe_jsonapi, maybe_links, maybe_included)

