from collections import defaultdict
from functools import reduce

from furrycorn.jsonapi.v1_0.data import Entries, Entry, Data
from furrycorn.jsonapi.v1_0.included import Included
from furrycorn.jsonapi.v1_0.common.resource import Resource
from furrycorn.jsonapi.v1_0.common.resource_identifier import ResourceId


def jsonapi_entries_to_list(jsonapi_entries):
    if type(jsonapi_entries) is Entries:
        return jsonapi_entries.list_entries
    else:
        raise RuntimeError('insanity: {0}'.format(str(jsonapi_entries)))


def jsonapi_entry_to_list(jsonapi_entry):
    if type(jsonapi_entry) is Entry:
        return [jsonapi_entry]
    else:
        raise RuntimeError('insanity: {0}'.format(str(maybe_jsonapi_entry)))


def process_jsonapi_data(jsonapi_data):
    either_entries_or_maybe_entry, = jsonapi_data

    if type(either_entries_or_maybe_entry) is Entries:
        return jsonapi_entries_to_list(either_entries_or_maybe_entry)
    elif type(either_entries_or_maybe_entry) is Entry:
        return jsonapi_entry_to_list(either_entries_or_maybe_entry)
    elif type(either_entries_or_maybe_entry) is None:
        return []
    else:
        msg = 'insanity: {0}'.format(str(either_entries_or_maybe_entry))
        raise RuntimeError(msg)


def jsonapi_entry_contains_resource(jsonapi_entry):
    either_resource_or_resource_id, = jsonapi_entry

    if type(either_resource_or_resource_id) is Resource:
        return True
    elif type(either_resource_or_resource_id) is ResourceId:
        return False
    else:
        msg = 'insanity: {0}'.format(str(either_resource_or_resource_id))
        raise RuntimeError(msg)


def find_data_resources(list_jsonapi_entries):
    filtered = filter(jsonapi_entry_contains_resource, list_jsonapi_entries)
    return list(map(lambda r: r.either_resource_or_resource_id, filtered))


def process_maybe_jsonapi_included(maybe_jsonapi_included=None):
    if type(maybe_jsonapi_included) is Included:
        list_jsonapi_resources, = maybe_jsonapi_included
        return list_jsonapi_resources
    elif type(maybe_jsonapi_included) is None:
        return []
    else:
        msg = 'insanity: {0}'.format(str(maybe_jsonapi_included))
        raise RuntimeError(msg)


class Directory:
    def __init__(self, jsonapi_data, maybe_jsonapi_included=None):
        list_data_entries = process_jsonapi_data(jsonapi_data)

        from_data     = find_data_resources(list_data_entries)
        from_included = process_maybe_jsonapi_included(maybe_jsonapi_included)

        list_resources = from_data + from_included

        self._directory       = { r.resource_id: r for r in list_resources }
        self._cache_all_types = None
        self._cache_by_type   = defaultdict(list)


    def produce_all_types(self):
        if self._cache_all_types:
            return self._cache_all_types
        else:
            list_types = \
                map(
                    lambda resource_id: resource_id.r_type,
                    self._directory.keys()
                )
            self._cache_all_types = set(list_types)

            return self._cache_all_types


    def fetch(self, resource_id):
        return self._directory[resource_id]


    def fetch_all_of_type(self, _type):
        if _type in self._cache_by_type:
            return self._cache_by_type[_type]
        else:
            def _f(resource):
                return resource.resource_id.r_type == _type

            self._cache_by_type[_type] = \
                list(filter(_f, self._directory.values()))

            return self._cache_by_type[_type]

