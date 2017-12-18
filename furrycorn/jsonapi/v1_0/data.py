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


class Entries(namedtuple('ListEntries', ['list_entries'])):
    """Representation of a list of entries in "data"."""

    __slots__ = ()

    def __new__(cls, list_entries):
        return super(Entries, cls).__new__(cls, list_entries)


class Data(namedtuple('Data', ['either_list_entries_or_maybe_entry'])):
    """Representation of the top-level "data" section of a response."""

    __slots__ = ()

    def __new__(cls, either_list_entries_or_maybe_entry):
        return super(Data, cls).__new__(cls,
                                        either_list_entries_or_maybe_entry)


def mk_list_entries(obj, config):
    list_entries = []

    for obj_entry in obj:
        list_entries.append(mk_entry(obj_entry, config))

    return Entries(list_entries)


def mk_entry(obj, config):
    maybe_meta = mk_meta(obj['meta'], config) if 'meta' in obj else None

    resource_id = resource_identifier.mk(obj, config)

    if 'attributes' in obj or 'relationships' in obj or 'links' in obj:
        return Entry(resource.mk(resource_id, obj, config))
    else:
        return Entry(resource_id)


def mk(obj, config):
    if type(obj) is list:
        value = mk_list_entries(obj, config) 
    else:
        if obj:
            value = mk_entry(obj, config)
        else:
            value = None

    return Data(value)

