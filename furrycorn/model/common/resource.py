from collections import namedtuple

from . import meta, relationships


class Links(namedtuple('Links', [])):
    """Representation of a resource's links in a response."""

    __slots__ = ()

    def __new__(cls):
        return super(Links, cls).__new__(cls)


class Resource(namedtuple('Resource', ['resource_id', 'maybe_dict_attrs',
                                       'maybe_relationships', 'maybe_links',
                                       'maybe_meta'])):
    """Representation of a full resource in a response."""

    __slots__ = ()

    def __new__(cls, resource_id, maybe_dict_attrs=None,
            maybe_relationships=None, maybe_links=None, maybe_meta=None):
        return super(Resource, cls).__new__(cls, resource_id, maybe_dict_attrs,
                                            maybe_relationships, maybe_links,
                                            maybe_meta)


def mk_links(obj, config):
    """Not yet implemented."""

    pass


def mk_maybe_dict_attrs(obj, config):
    return obj.get('attributes', None)


def mk_maybe_relationships(obj, config):
    if 'relationships' in obj:
        return relationships.mk(obj['relationships'], config)
    else:
        return None


def mk_maybe_links(obj, config):
    if 'links' in obj:
        return mk_links(obj['links'], config)
    else:
        return None


def mk(resource_id, obj, config):
    maybe_dict_attrs    = mk_maybe_dict_attrs(obj, config)
    maybe_relationships = mk_maybe_relationships(obj, config)
    maybe_links         = mk_maybe_links(obj, config)
    maybe_meta          = meta.mk_maybe(obj, config)

    return Resource(resource_id, maybe_dict_attrs, maybe_relationships,
                    maybe_links, maybe_meta)

