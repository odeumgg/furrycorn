from collections import namedtuple

from .common import resource
from .common import resource_identifier


class Entry(namedtuple('Entry', ['either_resource_or_resource_id'])):
    """
    Representation of either a resource or a resource identifier in "data".
    """

    __slots__ = ()

    def __new__(cls, either_resource_or_resource_id):
        return super(Entry, cls).__new__(cls, either_resource_or_resource_id)


class Entries(namedtuple('Entries', ['list_entries'])):
    """Representation of a list of entries in "data"."""

    __slots__ = ()

    def __new__(cls, list_entries):
        return super(Entries, cls).__new__(cls, list_entries)


class Data(namedtuple('Data', ['either_entries_or_maybe_entry'])):
    """Representation of the top-level "data" section of a response."""

    __slots__ = ()

    def __new__(cls, either_entries_or_maybe_entry):
        return super(Data, cls).__new__(cls,
                                        either_entries_or_maybe_entry)


def mk_entry(obj, config):
    resource_id = resource_identifier.mk(obj, config)

    if 'attributes' in obj or 'relationships' in obj or 'links' in obj:
        return Entry(resource.mk(resource_id, obj, config))
    else:
        return Entry(resource_id)


def mk_entries(obj, config):
    list_entries = [mk_entry(obj_entry, config) for obj_entry in obj]

    return Entries(list_entries)


def mk(obj, config):
    if type(obj) is list:
        value = mk_entries(obj, config)
    else:
        if obj is not None:
            value = mk_entry(obj, config)
        else:
            value = None

    return Data(value)

