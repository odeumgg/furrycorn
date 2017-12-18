from collections import namedtuple


class Error(namedtuple('Error', ['maybe_id', 'maybe_links', 'maybe_status',
                                 'maybe_code', 'maybe_title', 'maybe_detail',
                                 'maybe_source', 'maybe_meta'])):
    """Representation of a single error from a list of errors in "errors"."""

    __slots__ = ()

    def __new__(cls, maybe_id=None, maybe_links=None, maybe_status=None,
                maybe_code=None, maybe_title=None, maybe_detail=None,
                maybe_source=None, maybe_meta=None):
        return super(Error, cls).__new__(cls, maybe_id, maybe_links,
                                         maybe_status, maybe_code, maybe_title,
                                         maybe_detail, maybe_source, maybe_meta)


class Errors(namedtuple('Errors', ['list_errors'])):
    """Representation of the top-level "errors" section of a response."""

    __slots__ = ()

    def __new__(cls, list_errors):
        return super(Errors, cls).__new__(cls, list_errors)


def mk(obj, config):
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

