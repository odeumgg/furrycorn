import pytest

from furrycorn import config
from furrycorn.model import links


def test_mk(mocker):
    obj = {}
    cfg = config.mk('https://api', 'ABCDEF')

    result = links.mk(obj, cfg)

    assert type(result) is links.Links

