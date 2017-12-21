from .document import data, errors, meta

from .directory import Directory
from .. import parsing
from ..parsing.data import Data, Entry, Entries
from ..parsing.errors import Errors
from ..parsing.common.meta import Meta


def process(obj, maybe_config=None):
    config = maybe_config or parsing.mk_config(parsing.Mode.LENIENT)
    root   = parsing.process(obj, config)

    any_data_or_errors_or_meta, maybe_either_data_or_errors, maybe_meta, \
        maybe_jsonapi, maybe_links, maybe_included = root

    if type(any_data_or_errors_or_meta) is Data:
        directory = Directory(any_data_or_errors_or_meta, maybe_included)

        either_entries_or_maybe_entry, = any_data_or_errors_or_meta
        if type(either_entries_or_maybe_entry) is Entries:
            return data.Data(directory, data.Cardinality.MANY,
                             any_data_or_errors_or_meta, maybe_meta,
                             maybe_jsonapi, maybe_links)
        elif type(either_entries_or_maybe_entry) in [Entry, None]:
            return data.Data(directory, data.Cardinality.MAYBE_ONE,
                             any_data_or_errors_or_meta, maybe_meta,
                             maybe_jsonapi, maybe_links)
        else:
            msg = 'insanity: {0}'.format(str(either_entries_or_maybe_entry))
            raise RuntimeError(msg)
    elif type(any_data_or_errors_or_meta) is Errors:
        return errors.Errors(directory, errors, maybe_meta, maybe_jsonapi,
                             maybe_links)
    elif type(any_data_or_errors_or_meta) is Meta:
        return meta.Meta(directory, meta, maybe_jsonapi, maybe_links)
    else:
        msg = 'insanity: {0}'.format(any_data_or_errors_or_meta)
        raise RuntimeError(msg)

