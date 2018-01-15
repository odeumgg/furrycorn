import pytest

from furrycorn import config
from furrycorn.model.common import pagination


def test_mk(mocker):
    obj = {} # mock, doesn't matter
    cfg = config.mk('https://api', 'ABCDEF')

    result = pagination.mk(obj, config)

    assert type(result) is pagination.Pagination

