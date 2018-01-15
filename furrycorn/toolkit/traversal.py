from enum import Enum

from ..model.common.relationships import Relationships, Data, \
                                           ToMany, ToOne
from ..model.common.resource import Resource
from ..model.common.resource_identifier import ResourceId


def resolve(directory, either_resource_or_resource_id):
    if type(either_resource_or_resource_id) is Resource:
        return either_resource_or_resource_id
    elif type(either_resource_or_resource_id) is ResourceId:
        return directory.fetch(either_resource_or_resource_id)
    else:
        msg = 'insanity: {0}'.format(either_resource_or_resource_id)
        raise RuntimeError(msg)


class ResourceProxy:
    def __init__(self, directory, resource):
        self.directory = directory
        self.resource  = resource
        self._cache_all_relationships = None
        self._cache_relationships     = dict()


    def __repr__(self):
        return repr(self.resource)


    def __getattr__(self, attr):
        if attr in self.resource._fields:
            return getattr(self.resource, attr)
        else:
            return self.__getattribute__(attr)


    def produce_all_relationships(self):
        if self._cache_all_relationships:
            return self._cache_all_relationships
        else:
            maybe_relationships = self.resource.maybe_relationships

            if type(maybe_relationships) is Relationships:
                dict_relationships, = maybe_relationships
                self._cache_all_relationships = list(dict_relationships.keys())

                return self._cache_all_relationships
            elif maybe_relationships is None:
                self._cache_all_relationships = []
                return self._cache_all_relationships
            else:
                msg = 'insanity: {0}'.format(str(maybe_relationships))
                raise RuntimeError(msg)


    def traverse(self, target):
        if target in self._cache_relationships:
            return self._cache_relationships[target]
        else:
            maybe_relationships = self.resource.maybe_relationships

            if maybe_relationships:
                dict_relationships, = maybe_relationships

                if target not in dict_relationships:
                    msg = 'no "{0}" relationship specified'.format(target)
                    raise RuntimeError(msg)

                relationship = dict_relationships[target]

                any_data_or_links_or_meta = \
                    relationship.any_data_or_links_or_meta

                if type(any_data_or_links_or_meta) is not Data:
                    msg = 'rel unspecified'.format(str(maybe_relationships))
                    raise RuntimeError(msg)

                either_to_many_or_to_one, = any_data_or_links_or_meta

                if type(either_to_many_or_to_one) is ToMany:
                    self._cache_relationships[target] = \
                        RelationshipProxy(self.directory, relationship)
                    return self._cache_relationships[target]
                elif type(either_to_many_or_to_one) is ToOne:
                    self._cache_relationships[target] = \
                        RelationshipProxy(self.directory, relationship)
                    return self._cache_relationships[target]
                else:
                    msg = 'insanity: {0}'.format(str(either_to_many_or_to_one))
                    raise RuntimeError(msg)


class RelationshipProxy:
    def __init__(self, directory, relationship):
        self.directory       = directory
        self.relationship    = relationship
        self._cache_contents = dict()


    def __iter__(self):
        if self.produce_maybe_contents():
            return iter(self.produce_maybe_contents())
        else:
            return iter([])


    def __len__(self):
        maybe_contents = self.produce_maybe_contents()

        if type(maybe_contents) is list:
            return len(maybe_contents)
        elif maybe_contents:
            return 1
        else:
            return 0


    def __getitem__(self, index):
        maybe_contents = self.produce_maybe_contents()

        if type(maybe_contents) is not list:
            name = self.relationship.name
            msg  = '"{0}" is "to one"--indexing disabled.'.format(name)
            raise IndexError(msg)

        return maybe_contents[index]


    def __getattr__(self, attr):
        if attr in self.relationship._fields:
            return getattr(self.relationship, attr)
        else:
            return self.__getattribute__(attr)


    def __repr__(self):
        return repr(self.relationship)


    def produce_maybe_contents(self):
        if self._cache_contents:
            return self._cache_contents
        else:
            any_data_or_links_or_meta = \
                self.relationship.any_data_or_links_or_meta

            cardinality, = any_data_or_links_or_meta

            if type(cardinality) is ToMany:
                list_resource_ids, = cardinality
                list_resources     = []

                for resource_id in list_resource_ids:
                    resource = resolve(self.directory, resource_id)
                    proxy    = ResourceProxy(self.directory, resource)

                    list_resources.append(proxy)

                self._cache_contents = list_resources

                return self._cache_contents
            elif type(cardinality) is ToOne:
                maybe_resource_id, = cardinality

                if type(maybe_resource_id) is ResourceId:
                    resource = resolve(self.directory, maybe_resource_id)
                    proxy    = ResourceProxy(self.directory, resource)

                    self._cache_contents = proxy

                    return self._cache_contents
                else:
                    msg = 'insanity: {0}'.format(str(maybe_resource_id))
                    raise RuntimeError(msg)
            else:
                msg = 'insanity: {0}'.format(str(cardinality))
                raise RuntimeError(msg)

