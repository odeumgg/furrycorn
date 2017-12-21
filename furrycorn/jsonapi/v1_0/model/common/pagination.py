from collections import namedtuple


class Pagination(namedtuple('Pagination', ['maybe_first', 'maybe_last',
                                           'maybe_prev', 'maybe_next'])):
    """
    Representation of pagination links subset in any "links" section.
    """

    __slots__ = ()

    def __new__(cls, maybe_first=None, maybe_last=None, maybe_prev=None,
                maybe_next=None):
        return super(Pagination, cls).__new__(cls, maybe_first, maybe_last,
                                              maybe_prev, maybe_next)


def mk(obj, config):
    maybe_first    = obj.get(   'first', None)
    maybe_last     = obj.get(    'last', None)
    maybe_previous = obj.get('previous', None)
    maybe_next     = obj.get(    'next', None)

    return Pagination(maybe_first, maybe_last, maybe_previous, maybe_next)

