import pytest

from furrycorn.v1_0 import config
from furrycorn.v1_0.model import jsonapi


def test_mk(mocker):
    """Not yet implemented."""
    obj = {}
    cfg = config.mk('https://api', 'ABCDEF')

    result = jsonapi.mk(obj, cfg)

