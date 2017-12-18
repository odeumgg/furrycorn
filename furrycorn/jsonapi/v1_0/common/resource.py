from collections import namedtuple

from . import meta, relationships


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
    pass


def mk(resource_id, obj, config):
    maybe_dict_attrs = obj['attributes'] if 'attributes' in obj else None

    if 'relationships' in obj:
        maybe_relationships = relationships.mk(obj['relationships'], config)
    else:
        maybe_relationships = None

    maybe_links = mk_links(obj['links'], config) if 'links' in obj else None

    maybe_meta = meta.mk(obj['meta']) if 'meta' in obj else None

    return Resource(resource_id, maybe_dict_attrs, maybe_relationships,
                    maybe_links, maybe_meta)

