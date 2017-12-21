from collections import namedtuple

from .common import resource
from .common import resource_identifier


class Included(namedtuple('Included', ['list_resources'])):
    """Representation of the top-level "included" section of a response."""

    __slots__ = ()

    def __new__(cls, list_resources):
        return super(Included, cls).__new__(cls, list_resources)


def mk(obj, config):
    list_resources = []

    for obj_resource in obj:
        _resource_id = resource_identifier.mk(obj_resource, config)
        _resource    = resource.mk(_resource_id, obj_resource, config)
        list_resources.append(_resource)

    return Included(list_resources)

