import pytest

from furrycorn.v1_0 import config
from furrycorn.v1_0.model import links


def test_mk(mocker):
    obj = {}
    cfg = config.mk('https://api', 'ABCDEF')

    result = links.mk(obj, cfg)

    assert type(result) is links.Links

