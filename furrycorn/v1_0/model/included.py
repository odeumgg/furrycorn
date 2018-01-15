from collections import namedtuple

from .common import resource
from .common import resource_identifier


class Included(namedtuple('Included', ['list_resources'])):
    """Representation of the top-level "included" section of a response."""

    __slots__ = ()

    def __new__(cls, list_resources):
        return super(Included, cls).__new__(cls, list_resources)


def mk_single(obj, config):
    resource_id = resource_identifier.mk(obj, config)

    return resource.mk(resource_id, obj, config)


def mk(obj, config):
    list_resources = [mk_single(obj_resource, config) for obj_resource in obj]

    return Included(list_resources)

