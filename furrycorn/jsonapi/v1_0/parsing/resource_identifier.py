from collections import namedtuple


class ResourceId(namedtuple('ResourceId', ['r_type', 'r_id'])):
    """Representation of a resource identifier in a response."""

    __slots__ = ()

    def __new__(cls, r_type, r_id):
        return super(ResourceId, cls).__new__(cls, r_type, r_id)


def mk(obj, config):
    return ResourceId(obj['type'], obj['id'])

