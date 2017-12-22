from enum import Enum

from . import directory
from .traversal import resolve, ResourceProxy
from ..model.data import Entries, Entry
from ..model.common.resource import Resource


class DataCardinality(Enum):
    MANY      = 1
    MAYBE_ONE = 2


class Data:
    def __init__(self, directory, cardinality, data, maybe_meta=None,
                 maybe_jsonapi=None, maybe_links=None):
        self.directory       = directory
        self.cardinality     = cardinality
        self.data            = data
        self.maybe_meta      = maybe_meta
        self.maybe_jsonapi   = maybe_jsonapi
        self.maybe_links     = maybe_links
        self._cache_contents = None


    def __iter__(self):
        maybe_contents = self.produce_maybe_contents()

        if maybe_contents:
            if type(maybe_contents) is list:
                return iter(maybe_contents)
            else:
                return iter([maybe_contents])
        else:
            return iter([])


    def produce_maybe_contents(self):
        # n.b. because self._cache_contents can be legitimately None when
        #      cardinality is one and maybe_entry is None, this cache strategy
        #      will fail repeatedly for that one case.
        if self._cache_contents:
            return self._cache_contents
        else:
            if self.cardinality == DataCardinality.MANY:
                entries, = self.data

                if type(entries) is not Entries:
                    raise RuntimeError('insanity: {0}'.format(str(entries)))

                list_entries   = directory.entries_to_list(entries)
                list_resources = []

                for entry in list_entries:
                    either_resource_or_resource_id, = entry
                    resource = \
                        resolve(self.directory, either_resource_or_resource_id)
                    list_resources.append(
                        ResourceProxy(self.directory, resource)
                    )

                self._cache_contents = list_resources

                return self._cache_contents
            elif self.cardinality == DataCardinality.MAYBE_ONE:
                maybe_entry, = self.data

                if type(maybe_entry) is Entry:
                    either_resource_or_resource_id, = maybe_entry
                    resource = \
                        resolve(self.directory, either_resource_or_resource_id)

                    self._cache_contents = \
                        ResourceProxy(self.directory, resource)

                    return self._cache_contents
                elif maybe_entry is None:
                    return None
                else:
                    raise RuntimeError('insanity: {0}'.format(str(entry)))
            else:
                raise RuntimeError('insanity: {0}', str(self.cardinality))


class Errors:
    def __init__(self, errors, maybe_meta=None, maybe_jsonapi=None,
                 maybe_links=None):
        self.errors        = errors
        self.maybe_meta    = maybe_meta
        self.maybe_jsonapi = maybe_jsonapi
        self.maybe_links   = maybe_links


    def produce_errors(self):
        list_errors, = self.errors
        return list_errors


    def produce_maybe_meta(self):
        return self.maybe_meta


    def produce_maybe_jsonapi(self):
        return self.maybe_jsonapi


    def produce_maybe_links(self):
        return self.maybe_links


class Meta:
    def __init__(self, meta, maybe_jsonapi=None, maybe_links=None):
        self.meta          = meta
        self.maybe_jsonapi = maybe_jsonapi
        self.maybe_links   = maybe_links


    def produce_meta(self):
        return self.meta


    def produce_maybe_jsonapi(self):
        return self.maybe_jsonapi


    def produce_maybe_links(self):
        return self.maybe_links

