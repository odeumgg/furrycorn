from enum import Enum

from ..model.common.relationships import Relationships, Data, \
                                           ToMany, ToOne
from ..model.common.resource import Resource
from ..model.common.resource_identifier import ResourceId


class Cardinality(Enum):
    MANY      = 1
    MAYBE_ONE = 2
    NONE      = 3


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
            raise AttributeError(attr)


    def produce_all_relationships(self):
        if self._cache_all_relationships:
            return self._cache_all_relationships
        else:
            maybe_relationships = self.resource.maybe_relationships

            if type(maybe_relationships) is Relationships:
                dict_relationships, = maybe_relationships
                self._cache_all_relationships = list(dict_relationships.keys())

                return self._cache_all_relationships
            elif type(maybe_relationships) is None:
                self._cache_all_relationships = []
                return self._cache_all_relationships
            else:
                msg = 'insanity: {0}'.format(str(maybe_relationships))
                raise RuntimeError(msg)


    def relate(self, target):
        if target in self._cache_relationships:
            return self._cache_content[target]
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
                        RelationshipProxy(self.directory, Cardinality.MANY,
                                          relationship)
                    return self._cache_relationships[target]
                elif type(either_to_many_or_to_one) is ToOne:
                    self._cache_relationships[target] = \
                        RelationshipProxy(self.directory, Cardinality.MAYBE_ONE,
                                          relationship)
                    return self._cache_relationships[target]
                else:
                    msg = 'insanity: {0}'.format(str(either_to_many_or_to_one))
                    raise RuntimeError(msg)


class RelationshipProxy:
    def __init__(self, directory, cardinality, relationship):
        self.directory    = directory
        self.cardinality  = cardinality
        self.relationship = relationship

        self._cache_contents = dict()


    def __iter__(self):
        if self.produce_maybe_contents():
            return iter(self.produce_maybe_contents())
        else:
            return iter([])


    def __getattr__(self, attr):
        if attr in self.relationship._fields:
            return getattr(self.relationship, attr)
        else:
            raise AttributeError(attr)


    def __repr__(self):
        return repr(self.relationship)


    def produce_maybe_contents(self):
        if self._cache_contents:
            return self._cache_contents
        else:
            any_data_or_links_or_meta = \
                self.relationship.any_data_or_links_or_meta

            if self.cardinality == Cardinality.MANY:
                to_many, = any_data_or_links_or_meta
                list_resource_ids, = to_many

                if type(to_many) is not ToMany:
                    raise RuntimeError('insanity: {0}'.format(str(to_many)))

                list_resources = []

                for resource_id in list_resource_ids:
                    resource = resolve(self.directory, resource_id)
                    list_resources.append(
                        ResourceProxy(self.directory, resource)
                    )

                self._cache_contents = list_resources

                return self._cache_contents
            elif self.cardinality == Cardinality.MAYBE_ONE:
                to_one, = any_data_or_links_or_meta

                if type(to_one) is not ToOne:
                    raise RuntimeError('insanity: {0}'.format(str(to_one)))

                maybe_resource_id, = to_one

                if type(maybe_resource_id) is ResourceId:
                    resource = resolve(self.directory, maybe_resource_id)
                    self._cache_contents = \
                        ResourceProxy(self.directory, resource)
                else:
                    msg = 'insanity: {0}'.format(str(maybe_resource_id))
                    raise RuntimeError(msg)
            elif self.cardinality == Cardinality.NONE:
                return None
            else:
                msg = 'insanity: {0}'.format(str(cardinality))
                raise RuntimeError(msg)

