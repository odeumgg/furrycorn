import pytest

from furrycorn import config
from furrycorn.model import jsonapi


def test_mk(mocker):
    """Not yet implemented."""
    obj = {}
    cfg = config.mk('https://api', 'ABCDEF')

    result = jsonapi.mk(obj, cfg)

