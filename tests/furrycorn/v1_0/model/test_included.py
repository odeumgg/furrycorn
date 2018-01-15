import pytest

from furrycorn.v1_0 import config
from furrycorn.v1_0.model import included
from furrycorn.v1_0.model.common import resource, resource_identifier


def test_mk_single(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    fake_resource_identifier = resource_identifier.ResourceId('test', '1234')
    mocker.patch('furrycorn.v1_0.model.common.resource_identifier.mk',
                 return_value=fake_resource_identifier, autospec=True)
    fake_resource = resource.Resource(fake_resource_identifier)
    mocker.patch('furrycorn.v1_0.model.common.resource.mk',
                 return_value=fake_resource, autospec=True)

    result = included.mk_single(obj, cfg)

    assert resource_identifier.mk.call_count == 1
    assert resource.mk.call_count == 1
    assert type(result) is resource.Resource



def test_mk(mocker):
    obj = [ {}, {}, {} ] # mock
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.v1_0.model.included.mk_single')

    result = included.mk(obj, cfg)

    assert included.mk_single.call_count == 3
    assert type(result) is included.Included

