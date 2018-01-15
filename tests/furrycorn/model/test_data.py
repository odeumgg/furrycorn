import pytest

from furrycorn import config
from furrycorn.model import data
from furrycorn.model.common import resource, resource_identifier


def test_mk_entry_on_resource(mocker):
    obj = { 'attributes': 'whatever' } # presence of key indicates resource
    cfg = config.mk('https://api', 'ABCDEF')

    fake_resource_id = resource_identifier.ResourceId('type', '1234')
    mocker.patch('furrycorn.model.common.resource_identifier.mk',
                 return_value=fake_resource_id, autospec=True)
    fake_resource = resource.Resource(fake_resource_id)
    mocker.patch('furrycorn.model.common.resource.mk',
                 return_value=fake_resource, autospec=True)

    result = data.mk_entry(obj, config)

    assert resource_identifier.mk.call_count == 1
    assert resource.mk.call_count == 1
    assert type(result) is data.Entry
    assert type(result.either_resource_or_resource_id) is resource.Resource


def test_mk_entry_on_resource_identifier(mocker):
    obj = {} # absence of certain keys indicates resource identifier
    cfg = config.mk('https://api', 'ABCDEF')

    fake_resource_id = resource_identifier.ResourceId('type', '1234')
    mocker.patch('furrycorn.model.common.resource_identifier.mk',
                 return_value=fake_resource_id, autospec=True)
    mocker.patch('furrycorn.model.common.resource.mk')

    result = data.mk_entry(obj, config)

    assert resource_identifier.mk.call_count == 1
    assert resource.mk.call_count == 0
    assert type(result) is data.Entry
    assert type(result.either_resource_or_resource_id) is resource_identifier.ResourceId


def test_mk_entries(mocker):
    obj = [ {}, {}, {} ] # mock, need 3
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.data.mk_entry')

    result = data.mk_entries(obj, config)

    assert data.mk_entry.call_count == 3
    assert type(result) is data.Entries


def test_mk_on_list(mocker):
    obj = [] # mock
    cfg = config.mk('https://api', 'ABCDEF')

    fake_entries = data.Entries([])
    mocker.patch('furrycorn.model.data.mk_entries',
                 return_value=fake_entries, autospec=True)

    result = data.mk(obj, config)

    assert data.mk_entries.call_count == 1
    assert type(result) is data.Data
    assert type(result.either_entries_or_maybe_entry) is data.Entries


def test_mk_on_object(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    fake_entry = data.Entry(resource_identifier.ResourceId('type', '1234'))
    mocker.patch('furrycorn.model.data.mk_entry',
                 return_value=fake_entry, autospec=True)

    result = data.mk(obj, config)

    assert data.mk_entry.call_count == 1
    assert type(result) is data.Data
    assert type(result.either_entries_or_maybe_entry) is data.Entry


def test_mk_on_none(mocker):
    obj = None # mock
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.data.mk_entries')
    mocker.patch('furrycorn.model.data.mk_entry')

    result = data.mk(obj, config)

    assert data.mk_entries.call_count == 0
    assert data.mk_entry.call_count == 0
    assert type(result) is data.Data
    assert result.either_entries_or_maybe_entry is None

