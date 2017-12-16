from collections import namedtuple

# A note to readers of this code:
#
#  The author of this file (@onethirtyfive) has a bias for coding in a
#  functional style. Emphasis is put on:
#
#    1. Immutabie and domain-specific data types. Where built-in Python
#       collection types like "dict" and "list" are used, the variable names are
#       prefixed for explicitness. (Otherwise, assume a custom type is present
#       for the value.) No prefix type-hinting is attempted for primitives like
#       'int' and 'str'.
#    2. Composition of simpler types into more complex types.
#    3. Explicit optionality--if a value can be None, its name must start with
#       "maybe_". "null", or optional data, is a huge source of bugs in code.
#    4. No shared mutable state.
#
#  The code may not be as performant as conventional, stateful code, but it
#  will be easier to maintain.
#
#  Data will be exposed in a more object-oriented way in a separate interface.


class ResourceId(namedtuple('ResourceId', ['r_type', 'r_id', 'maybe_meta'])):
    """Representation of a resource identifier in a response."""

    __slots__ = ()

    def __new__(cls, r_type, r_id, maybe_meta):
        return super(ResourceId, cls).__new__(cls, r_type, r_id, maybe_meta)


class Resource(namedtuple('Resource', ['resource_id', 'maybe_dict_attrs',
                                       'maybe_relationships', 'maybe_links'])):
    """Representation of a full resource in a response."""

    __slots__ = ()

    def __new__(cls, resource_id, maybe_dict_attrs=None,
            maybe_relationships=None, maybe_links=None):
        return super(Resource, cls).__new__(cls, resource_id, maybe_dict_attrs,
                                            maybe_relationships, maybe_links)


class Entry(namedtuple('Entry', ['either_resource_or_resource_id'])):
    """
    Representation of either a resource or a resource identifier in a response.
    """

    __slots__ = ()

    def __new__(cls, either_resource_or_resource_id):
        return super(Entry, cls).__new__(cls, either_resource_or_resource_id)


class Entries(namedtuple('ListEntries', ['list_entries'])):
    """Representation of a list of entries in a response."""

    __slots__ = ()

    def __new__(cls, list_entries):
        return super(Entries, cls).__new__(cls, list_entries)


class Data(namedtuple('Data', ['either_list_entries_or_maybe_entry'])):
    """Representation of the top-level "data" section of a response."""

    __slots__ = ()

    def __new__(cls, either_list_entries_or_maybe_entry):
        return super(Data, cls).__new__(cls, either_list_entries_or_maybe_entry)


class Error(namedtuple('Error', ['maybe_id', 'maybe_links', 'maybe_status',
                                 'maybe_code', 'maybe_title', 'maybe_detail',
                                 'maybe_source', 'maybe_meta'])):
    """Representation of a single error from a list of errors in a response."""

    __slots__ = ()

    def __new__(cls, maybe_id=None, maybe_links=None, maybe_status=None,
                maybe_code=None, maybe_title=None, maybe_detail=None,
                maybe_source=None, maybe_meta=None):
        return super(Error, cls).__new__(cls, maybe_id, maybe_links,
                                         maybe_status, maybe_code,
                                         maybe_title, maybe_detail,
                                         maybe_source, maybe_meta)


class Errors(namedtuple('Errors', ['list_errors'])):
    """Representation of the top-level "errors" section of a response."""

    __slots__ = ()

    def __new__(cls, list_errors):
        return super(Errors, cls).__new__(cls, list_errors)


class Meta(namedtuple('Meta', ['dict_attrs'])):
    """
    Representation of freeform metadata anywhere appropriate in a response.
    """

    __slots__ = ()

    def __new__(cls, dict_attrs):
        return super(Meta, cls).__new__(cls, dict_attrs)


class LinksPagination(namedtuple('LinksPagination', ['maybe_first',
                                                     'maybe_last',
                                                     'maybe_prev',
                                                     'maybe_next'])):
    """
    Representation of pagination links anywhere appropriate in a response.
    """

    __slots__ = ()

    def __new__(cls, maybe_first=None, maybe_last=None, maybe_prev=None,
                maybe_next=None):
        return super(LinksPagination, cls).__new__(cls, maybe_first,
                                                   maybe_last, maybe_prev,
                                                   maybe_next)


class LinksTopLevel(namedtuple('LinksTopLevel', ['links_pagination',
                                                 'maybe_self',
                                                 'maybe_related'])):
    """Representation of links in top-level of a response."""

    __slots__ = ()

    def __new__(cls, links_pagination, maybe_self=None, maybe_related=None):
        return super(LinksTopLevel, cls).__new__(cls, links_pagination,
                                                 maybe_self, maybe_related)


class TopLevel(namedtuple('TopLevel', ['any_data_or_errors_or_meta',
                                       'maybe_either_data_or_errors',
                                       'maybe_meta', 'maybe_jsonapi',
                                       'maybe_top_level_links',
                                       'maybe_included'])):
    """
    Representation of the top level of a response.

    There can be *either* an Data or Errors, not both. Or neither.
    There can be always be a Meta.
    There must be one of the three.

    'any_data_or_errors_or_meta' preferentially contains the Data or Errors;
    otherwise, the Meta. It must be a value other than None.
    """

    __slots__ = ()

    def __new__(cls, any_data_or_errors_or_meta,
                maybe_either_data_or_errors=None, maybe_meta=None,
                maybe_jsonapi=None, maybe_top_level_links=None,
                maybe_included=None):
        return super(TopLevel, cls).__new__(cls, any_data_or_errors_or_meta,
                                            maybe_either_data_or_errors,
                                            maybe_meta, maybe_jsonapi,
                                            maybe_top_level_links,
                                            maybe_included)


def mk_meta(obj, config):
    if obj:
        return Meta(obj)
    else:
        return None


def mk_resource_relationships(obj, config):
    pass


def mk_resource_links(obj, config):
    pass


def mk_entry(obj, config):
    if obj:
        r_type     = obj['type']
        r_id       = obj['id']
        maybe_meta = mk_meta(obj['meta'], config) if 'meta' in obj else None

        resource_id = ResourceId(r_type, r_id, maybe_meta)

        if 'attributes' in obj or 'relationships' in obj or 'links' in obj:
            maybe_dict_attrs = obj['attributes'] \
                if 'attributes' in obj else None

            maybe_relationships = \
                mk_resource_relationships(obj['relationships'], config) \
                    if 'relationships' in obj else None

            maybe_links = mk_resource_links(obj['links'], config) \
                if 'links' in obj else None

            resource = Resource(resource_id, maybe_dict_attrs,
                                maybe_relationships, maybe_links)

            return Entry(resource)
        else:
            return Entry(resource_id)
    else:
        return None


def mk_entries(obj, config):
    list_entries = []

    for obj_entry in obj:
        list_entries.append(mk_entry(obj_entry, config))

    return Entries(list_entries)


def mk_links_pagination(obj, config):
    maybe_first    = obj.get(   'first', None)
    maybe_last     = obj.get(    'last', None)
    maybe_previous = obj.get('previous', None)
    maybe_next     = obj.get(    'next', None)

    return LinksPagination(maybe_first, maybe_last, maybe_previous, maybe_next)


def mk_top_level_links(obj, config):
    maybe_self    = obj.get(   'self', None)
    maybe_related = obj.get('related', None)

    return LinksTopLevel(mk_links_pagination(obj, config), maybe_self,
                         maybe_related)


def mk_top_level_jsonapi(obj, config):
    pass


def mk_top_level_included(obj, config):
    pass


def mk_top_level(obj, config):
    if 'data' in obj and 'errors' in obj:
        raise RuntimeError('response cannot contain both data and errors')

    if 'data' not in obj and 'errors' not in obj and 'meta' not in obj:
        raise RuntimeError('response must contain data, errors, or meta (1)')

    maybe_data = mk_data(obj['data'], config) if 'data' in obj else None
    maybe_errors = mk_errors(obj['errors'], config) \
        if 'errors' in obj else None
    maybe_meta = mk_meta(obj['meta'], config) if 'meta' in obj else None
    maybe_jsonapi = mk_jsonapi(obj['jsonapi'], config) \
        if 'jsonapi' in obj else None
    maybe_top_level_links = mk_top_level_links(obj['links'], config) \
        if 'links' in obj else None
    maybe_included = mk_top_level_included(obj['included'], config) \
        if 'included' in obj else None

    if maybe_data:
        any_data_or_errors_or_meta = maybe_data
    elif maybe_errors:
        any_data_or_errors_or_meta = maybe_errors
    elif maybe_meta:
        any_data_or_errors_or_meta = maybe_meta
    else:
        raise RuntimeError('response must contain data, errors, or meta (2)')

    maybe_either_data_or_errors = maybe_data or maybe_errors

    return TopLevel(any_data_or_errors_or_meta, maybe_either_data_or_errors,
                    maybe_meta, maybe_jsonapi, maybe_top_level_links,
                    maybe_included)


def mk_data(obj, config):
    container = mk_entries(obj, config) \
        if type(obj) is list else mk_entry(obj, config)
    return Data(container)


def mk_errors(obj, config):
    list_errors = []

    for obj_error in obj:
        maybe_id     = obj_error.get(    'id', None)
        maybe_links  = obj_error.get( 'links', None)
        maybe_status = obj_error.get('status', None)
        maybe_code   = obj_error.get(  'code', None)
        maybe_title  = obj_error.get( 'title', None)
        maybe_detail = obj_error.get('detail', None)
        maybe_source = obj_error.get('source', None)
        maybe_meta   = obj_error.get(  'meta', None)

        error = Error(maybe_id, maybe_links, maybe_status, maybe_code,
                      maybe_title, maybe_detail, maybe_source, maybe_meta)

        list_errors.append(error)

    return Errors(list_errors)

