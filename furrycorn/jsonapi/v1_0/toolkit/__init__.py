from .document import data, errors, meta

from .directory import Directory
from .. import config
from .. import model
from ..model.data import Data, Entry, Entries
from ..model.errors import Errors
from ..model.common.meta import Meta


def process(obj, maybe_config=None):
    _config = maybe_config or config.mk(config.Mode.LENIENT)
    root    = model.build(obj, _config)

    any_data_or_errors_or_meta, maybe_either_data_or_errors, maybe_meta, \
        maybe_jsonapi, maybe_links, maybe_included = root

    if type(any_data_or_errors_or_meta) is Data:
        _directory = Directory(any_data_or_errors_or_meta, maybe_included)

        either_entries_or_maybe_entry, = any_data_or_errors_or_meta
        if type(either_entries_or_maybe_entry) is Entries:
            return data.Data(_directory, data.Cardinality.MANY,
                             any_data_or_errors_or_meta, maybe_meta,
                             maybe_jsonapi, maybe_links)
        elif type(either_entries_or_maybe_entry) in [Entry, NoneType]:
            return data.Data(_directory, data.Cardinality.MAYBE_ONE,
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

