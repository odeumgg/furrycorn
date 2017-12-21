from . import data, errors, meta

from furrycorn.jsonapi.v1_0.data import Data, Entry, Entries
from furrycorn.jsonapi.v1_0.errors import Errors
from furrycorn.jsonapi.v1_0.common.meta import Meta


def mk(directory, root):
    any_data_or_errors_or_meta, maybe_either_data_or_errors, maybe_meta, \
        maybe_jsonapi, maybe_links, _ = root

    if type(any_data_or_errors_or_meta) is Data:
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

