from collections import namedtuple

from .common import pagination


class Links(namedtuple('Links', ['links_pagination', 'maybe_self',
                                 'maybe_related'])):
    """Representation of the top-level "links" section of a response."""

    __slots__ = ()

    def __new__(cls, links_pagination, maybe_self=None, maybe_related=None):
        return super(Links, cls).__new__(cls, links_pagination, maybe_self,
                                         maybe_related)


def mk(obj, config):
    maybe_self    = obj.get(   'self', None)
    maybe_related = obj.get('related', None)

    return Links(pagination.mk(obj, config), maybe_self, maybe_related)

