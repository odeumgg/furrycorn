import pytest

from furrycorn.v1_0 import config
from furrycorn.v1_0.model.common import meta


def test_mk_maybe(mocker):
    obj = { 'meta': {} } # mock
    cfg = config.mk('https://api', 'ABCDEF')

    result = meta.mk_maybe(obj, config)

    assert type(result) is meta.Meta


def test_mk_maybe_none(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    result = meta.mk_maybe(obj, config)

    assert result is None


def test_mk(mocker):
    obj = {} # mock, doesn't matter
    cfg = config.mk('https://api', 'ABCDEF')

    result = meta.mk(obj, config)

    assert type(result) is meta.Meta

