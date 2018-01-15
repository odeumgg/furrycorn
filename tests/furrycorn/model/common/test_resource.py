import pytest

from furrycorn import config
from furrycorn.model.common import meta, relationships, resource, \
                                        resource_identifier


def test_mk_links(mocker):
    """Not yet implemented."""
    obj = { 'attributes': {} } # mock
    cfg = config.mk('https://api', 'ABCDEF')

    resource.mk_links(obj, config)


def test_mk_maybe_dict_attrs(mocker):
    obj = { 'attributes': {} } # mock
    cfg = config.mk('https://api', 'ABCDEF')

    result = resource.mk_maybe_dict_attrs(obj, cfg)

    assert type(result) is dict


def test_mk_maybe_dict_attrs_none(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    result = resource.mk_maybe_dict_attrs(obj, cfg)

    assert result is None


def test_mk_maybe_relationships(mocker):
    obj = { 'relationships': {} } # mock
    cfg = config.mk('https://api', 'ABCDEF')

    fake_relationships = relationships.Relationships({})
    mocker.patch('furrycorn.model.common.relationships.mk',
                 return_value=fake_relationships, autospec=True)

    result = resource.mk_maybe_relationships(obj, cfg)

    assert relationships.mk.call_count == 1
    assert type(result) is relationships.Relationships


def test_mk_maybe_relationships_none(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.common.relationships.mk')

    result = resource.mk_maybe_relationships(obj, cfg)

    assert relationships.mk.call_count == 0
    assert result is None


def test_mk_maybe_links(mocker):
    obj = { 'links': {} } # mock
    cfg = config.mk('https://api', 'ABCDEF')

    fake_links = resource.Links()
    mocker.patch('furrycorn.model.common.resource.mk_links',
                 return_value=fake_links, autospec=True)

    result = resource.mk_maybe_links(obj, cfg)

    assert resource.mk_links.call_count == 1
    assert type(result) is resource.Links


def test_mk_maybe_links_none(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.common.resource.mk_links')

    result = resource.mk_maybe_links(obj, cfg)

    assert resource.mk_links.call_count == 0
    assert result is None


def test_mk(mocker):
    fake_resource_id = resource_identifier.ResourceId('type', '123')
    obj              = {} # mock
    cfg              = config.mk('https://api', 'ABCDEF')

    patch1 = 'furrycorn.model.common.resource.mk_maybe_dict_attrs'
    patch2 = 'furrycorn.model.common.resource.mk_maybe_relationships'
    patch3 = 'furrycorn.model.common.resource.mk_maybe_links'
    patch4 = 'furrycorn.model.common.meta.mk_maybe'

    mocker.patch(patch1)
    mocker.patch(patch2)
    mocker.patch(patch3)
    mocker.patch(patch4)

    result = resource.mk(fake_resource_id, obj, cfg)

    assert resource.mk_maybe_dict_attrs.call_count == 1
    assert resource.mk_maybe_relationships.call_count == 1
    assert resource.mk_maybe_links.call_count == 1
    assert meta.mk_maybe.call_count == 1
    assert type(result) is resource.Resource

