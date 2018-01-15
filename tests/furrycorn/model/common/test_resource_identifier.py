import pytest

from furrycorn import config
from furrycorn.model.common import resource_identifier


def test_mk(mocker):
    obj = { 'type': 'foo', 'id': '1234' } # mock
    cfg = config.mk('https://api', 'ABCDEF')

    result = resource_identifier.mk(obj, cfg)

    assert type(result) is resource_identifier.ResourceId

