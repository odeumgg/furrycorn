from collections import namedtuple

from . import meta, pagination, resource_identifier


class ToOneLinks(namedtuple('ToOneLinks', ['maybe_self', 'maybe_related'])):
    """
    Representation of links for a to-one relationship anywhere in a response.
    """

    __slots__ = ()

    def __new__(cls, pagination, maybe_self=None, maybe_related=None):
        return super(ToOneLinks, cls).__new__(cls, maybe_self, maybe_related)


class ToManyLinks(namedtuple('ToManyLinks', ['pagination', 'maybe_self',
                                             'maybe_related'])):
    """
    Representation of links for a to-many relationship anywhere in a response.
    """

    __slots__ = ()

    def __new__(cls, pagination, maybe_self=None, maybe_related=None):
        return super(ToManyLinks, cls).__new__(cls, pagination, maybe_self,
                                               maybe_related)


class ToOne(namedtuple('ToOne', ['maybe_resource_id'])):
    """Representation of a to-one relationship."""

    __slots__ = ()

    def __new__(cls, maybe_resource_id=None):
        return super(ToOne, cls).__new__(cls, maybe_resource_id)


class ToMany(namedtuple('ToMany', ['list_resource_ids'])):
    """Representation of at to-many relationship."""

    __slots__ = ()

    def __new__(cls, list_resource_ids):
        return super(ToMany, cls).__new__(cls, list_resource_ids)


class Data(namedtuple('Data', ['either_to_many_or_to_one'])):
    """Representation of "data" section of relationships."""

    __slots__ = ()

    def __new__(cls, either_to_many_or_to_one):
        return super(Data, cls).__new__(cls, either_to_many_or_to_one)


class Relationship(namedtuple(
    'Relationship',
    ['name', 'any_data_or_links_or_meta', 'maybe_data',
     'maybe_either_to_one_links_or_to_many_links', 'maybe_meta'])):
    """Representation of a relationship in a relationships lookup."""

    __slots__ = ()

    def __new__(cls, name, any_data_or_links_or_meta, maybe_data=None,
                maybe_either_to_one_links_or_to_many_links=None,
                maybe_meta=None):
        return \
            super(Relationship, cls).__new__(
                cls, name, any_data_or_links_or_meta, maybe_data,
                maybe_either_to_one_links_or_to_many_links, maybe_meta
            )


class Relationships(namedtuple('Relationships', ['dict_relationships'])):
    """Representation of a relationships lookup anywhere in a response."""

    __slots__ = ()

    def __new__(cls, dict_relationships):
        return super(Relationships, cls).__new__(cls, dict_relationships)


def mk_data(obj, config):
    if type(obj) is list:
        list_resource_ids = []

        for obj_resource_id in obj:
            resource_id = resource_identifier.mk(obj_resource_id, config)
            list_resource_ids.append(resource_id)

        return Data(ToMany(list_resource_ids))
    elif type(obj) is dict:
        return Data(ToOne(resource_identifier.mk(obj, config)))
    elif not obj:
        return Data(ToOne(None))

    msg = "relationships['data'] is unintelligible: {0}".format(str(obj))
    raise RuntimeError(msg)


def mk_to_one_links(obj, config):
    maybe_self    = obj.get(   'self', None)
    maybe_related = obj.get('related', None)

    return ToOneLinks(maybe_self, maybe_related)


def mk_to_many_links(obj, config):
    pagination    = pagination.mk(obj, config)
    maybe_self    = obj.get(   'self', None)
    maybe_related = obj.get('related', None)

    return ToManyLinks(pagination, maybe_self, maybe_related)


def mk(obj, config):
    dict_relationships = {}

    for name, obj_relationship in obj.items():
        if 'data' not in obj_relationship and 'links' not in obj_relationship and \
           'meta' not in obj_relationship:
            msg = 'relationships must contain data, links, or meta (1)'
            raise RuntimeError(msg)

        if 'data' in obj_relationship:
            maybe_data = mk_data(obj_relationship['data'], config)
        else:
            maybe_data = None

        if 'links' in obj_relationship:
            if type(maybe_data) in [ToOne, None]:
                maybe_either_to_one_links_or_to_many_links = \
                    mk_to_one_links(obj_relationship['links'], config)
            elif type(maybe_data) is ToMany:
                maybe_either_to_one_links_or_to_many_links = \
                    mk_to_many_links(obj_relationship['links'], config)
            else:
                raise RuntimeError('insanity: {0}'.format(str(maybe_data)))
        else:
            maybe_either_to_one_links_or_to_many_links = None

        if 'meta' in obj_relationship:
            maybe_meta = meta.mk(obj_relationship['meta'], config)
        else:
            maybe_meta = None

        any_data_or_links_or_meta = maybe_data or maybe_links or maybe_meta

        if not any_data_or_links_or_meta:
            raise RuntimeError('response must contain data, links, or meta (2)')

        relationship = Relationship(name, any_data_or_links_or_meta,
                                    maybe_data,
                                    maybe_either_to_one_links_or_to_many_links,
                                    maybe_meta)

        dict_relationships[name] = relationship

    return Relationships(dict_relationships)

