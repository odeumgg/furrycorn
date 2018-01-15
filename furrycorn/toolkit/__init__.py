from furrycorn.model import data, errors
from furrycorn.model.common import meta
from furrycorn.toolkit import document


def process(root):
    if type(root.primary) is data.Data:
        _data, _, maybe_meta, maybe_jsonapi, maybe_links, maybe_included = root
        return document.mk_data(_data, maybe_meta, maybe_jsonapi, maybe_links,
                                maybe_included)

    if type(root.primary) is errors.Errors:
        _errors, _, maybe_meta, maybe_jsonapi, maybe_links, _ = root
        return document.mk_errors(_errors, maybe_meta, maybe_jsonapi,
                                  maybe_links)

    if type(root.primary) is meta.Meta:
        _meta, _, _,  maybe_jsonapi, maybe_links, _ = root
        return document.mk_meta(_meta, maybe_jsonapi, maybe_links)

    msg = 'insanity: {0}'.format(str(root.primary))
    raise RuntimeError(msg)

