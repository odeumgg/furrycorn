from collections import defaultdict
from functools import reduce

from ..model.data import Entries, Entry, Data
from ..model.included import Included
from ..model.common.resource import Resource
from ..model.common.resource_identifier import ResourceId


def entries_to_list(entries):
    if type(entries) is Entries:
        return entries.list_entries
    else:
        raise RuntimeError('insanity: {0}'.format(str(entries)))


def entry_to_list(entry):
    if type(entry) is Entry:
        return [entry]
    else:
        raise RuntimeError('insanity: {0}'.format(str(maybe_entry)))


def process_data(data):
    either_entries_or_maybe_entry, = data

    if type(either_entries_or_maybe_entry) is Entries:
        return entries_to_list(either_entries_or_maybe_entry)
    elif type(either_entries_or_maybe_entry) is Entry:
        return entry_to_list(either_entries_or_maybe_entry)
    elif either_entries_or_maybe_entry is None:
        return []
    else:
        msg = 'insanity: {0}'.format(str(either_entries_or_maybe_entry))
        raise RuntimeError(msg)


def entry_contains_resource(entry):
    either_resource_or_resource_id, = entry

    if type(either_resource_or_resource_id) is Resource:
        return True
    elif type(either_resource_or_resource_id) is ResourceId:
        return False
    else:
        msg = 'insanity: {0}'.format(str(either_resource_or_resource_id))
        raise RuntimeError(msg)


def find_data_resources(list_entries):
    filtered = filter(entry_contains_resource, list_entries)
    return list(map(lambda r: r.either_resource_or_resource_id, filtered))


def process_maybe_included(maybe_included=None):
    if type(maybe_included) is Included:
        list_resources, = maybe_included
        return list_resources
    elif maybe_included is None:
        return []
    else:
        raise RuntimeError('insanity: {0}'.format(str(maybe_included)))


class Directory:
    def __init__(self, data, maybe_included=None):
        list_data_entries = process_data(data)

        from_data      = find_data_resources(list_data_entries)
        from_included  = process_maybe_included(maybe_included)
        list_resources = from_data + from_included

        self._resources       = { r.resource_id: r for r in list_resources }
        self._cache_all_types = None
        self._cache_by_type   = defaultdict(list)


    def produce_all_types(self):
        if self._cache_all_types:
            return self._cache_all_types
        else:
            list_types = \
                map(
                    lambda resource_id: resource_id.r_type,
                    self._resources.keys()
                )
            self._cache_all_types = set(list_types)

            return self._cache_all_types


    def fetch(self, resource_id):
        return self._resources[resource_id]


    def fetch_all_of_type(self, _type):
        if _type in self._cache_by_type:
            return self._cache_by_type[_type]
        else:
            def _fetch_all_of_type(resource):
                return resource.resource_id.r_type == _type

            self._cache_by_type[_type] = \
                list(filter(_fetch_all_of_type, self._resources.values()))

            return self._cache_by_type[_type]

