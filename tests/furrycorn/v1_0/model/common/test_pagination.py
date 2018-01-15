import pytest

from furrycorn.v1_0 import config
from furrycorn.v1_0.model.common import pagination


def test_mk(mocker):
    obj = {} # mock, doesn't matter
    cfg = config.mk('https://api', 'ABCDEF')

    result = pagination.mk(obj, config)

    assert type(result) is pagination.Pagination

