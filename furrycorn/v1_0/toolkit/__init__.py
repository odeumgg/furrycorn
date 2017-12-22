from .directory import Directory
from . import document as doc
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
            return doc.Data(_directory, doc.DataCardinality.MANY,
                            any_data_or_errors_or_meta, maybe_meta,
                            maybe_jsonapi, maybe_links)
        elif type(either_entries_or_maybe_entry) in [Entry, type(None)]:
            return doc.Data(_directory, doc.DataCardinality.MAYBE_ONE,
                            any_data_or_errors_or_meta, maybe_meta,
                            maybe_jsonapi, maybe_links)
        else:
            msg = 'insanity: {0}'.format(str(either_entries_or_maybe_entry))
            raise RuntimeError(msg)
    elif type(any_data_or_errors_or_meta) is Errors:
        return doc.Errors(any_data_or_errors_or_meta, maybe_meta,
                          maybe_jsonapi, maybe_links)
    elif type(any_data_or_errors_or_meta) is Meta:
        return doc.Meta(any_data_or_errors_or_meta, maybe_jsonapi, maybe_links)
    else:
        msg = 'insanity: {0}'.format(any_data_or_errors_or_meta)
        raise RuntimeError(msg)

