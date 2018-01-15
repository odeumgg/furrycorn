import pytest

from furrycorn import config


def test_mk(mocker):
    result = config.mk(None, None) # mock

    assert type(result) is config.Config

