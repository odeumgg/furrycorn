import pytest

from furrycorn.v1_0 import config
from furrycorn.v1_0.model.common import meta, pagination, relationships, \
                                        resource_identifier


def test_mk_single_data_on_list(mocker):
    obj = [ {}, {}, {} ] # mock resource ids, not used. need 3
    cfg = config.mk('https://api', 'ABCDEF')

    fake_resource_identifier = resource_identifier.ResourceId('type', '123')

    mocker.patch('furrycorn.v1_0.model.common.resource_identifier.mk',
                 return_value=fake_resource_identifier, autospec=True)

    result = relationships.mk_single_data(obj, cfg)

    assert resource_identifier.mk.call_count == 3
    assert type(result.either_to_many_or_to_one) is relationships.ToMany


def test_mk_single_data_on_dict(mocker):
    obj = {} # mock resource id
    cfg = config.mk('https://api', 'ABCDEF')

    fake_resource_identifier = resource_identifier.ResourceId('type', '123')

    mocker.patch('furrycorn.v1_0.model.common.resource_identifier.mk',
                 return_value=fake_resource_identifier, autospec=True)

    result = relationships.mk_single_data(obj, cfg)

    assert resource_identifier.mk.call_count == 1
    assert type(result.either_to_many_or_to_one) is relationships.ToOne
    assert result.either_to_many_or_to_one.maybe_resource_id is not None


def test_mk_single_data_on_none(mocker):
    obj = None # mock, null resource id
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.v1_0.model.common.resource_identifier.mk')

    result = relationships.mk_single_data(obj, cfg)

    assert resource_identifier.mk.call_count == 0
    assert type(result.either_to_many_or_to_one) is relationships.ToOne
    assert result.either_to_many_or_to_one.maybe_resource_id is None


def test_mk_single_data_on_insanity(mocker):
    obj = 1 # mock, insane value
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.v1_0.model.common.resource_identifier.mk')

    with pytest.raises(RuntimeError):
        relationships.mk_single_data(obj, cfg)

    assert resource_identifier.mk.call_count == 0


def test_mk_single_maybe_data(mocker):
    obj = { 'data': 'fake' } # mock, with 'data'
    cfg = config.mk('https://api', 'ABCDEF')

    fake_data = relationships.Data(relationships.ToOne(None))
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_single_data',
                 return_value=fake_data, autospec=True)

    result = relationships.mk_single_maybe_data(obj, cfg)

    assert relationships.mk_single_data.call_count == 1
    assert type(result) is relationships.Data


def test_mk_single_maybe_data_on_none(mocker):
    obj = {} # mock, no 'data'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_single_data')

    result = relationships.mk_single_maybe_data(obj, cfg)

    assert relationships.mk_single_data.call_count == 0
    assert result is None


def test_mk_to_one_links(mocker):
    obj = { 'self': 'https://foo', 'related': 'https://bar' }
    cfg = config.mk('https://api', 'ABCDEF')

    result = relationships.mk_to_one_links(obj, cfg)

    assert type(result) == relationships.ToOneLinks
    assert result.maybe_self == 'https://foo'
    assert result.maybe_related == 'https://bar'


def test_mk_to_many_links(mocker):
    obj = { 'self': 'https://foo', 'related': 'https://bar' }
    cfg = config.mk('https://api', 'ABCDEF')

    fake_pagination = pagination.Pagination()
    mocker.patch('furrycorn.v1_0.model.common.pagination.mk',
                 return_value=fake_pagination, autospec=True)

    result = relationships.mk_to_many_links(obj, cfg)

    assert pagination.mk.call_count == 1
    assert type(result) == relationships.ToManyLinks
    assert type(result.pagination) == pagination.Pagination
    assert result.maybe_self == 'https://foo'
    assert result.maybe_related == 'https://bar'


def test_mk_single_maybe_links_on_to_one(mocker):
    maybe_data = relationships.Data(relationships.ToOne(None))
    obj        = { 'links': 'fake' } # mock, with 'links'
    cfg        = config.mk('https://api', 'ABCDEF')

    fake_to_one_links = relationships.ToOne(None)
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_to_one_links',
                 return_value=fake_to_one_links, autospec=True)

    result = relationships.mk_single_maybe_links(maybe_data, obj, cfg)

    assert relationships.mk_to_one_links.call_count == 1
    assert type(result) is relationships.ToOne


def test_mk_single_maybe_links_on_to_many(mocker):
    maybe_data = relationships.Data(relationships.ToMany([]))
    obj        = { 'links': {} } # mock, with 'links'
    cfg        = config.mk('https://api', 'ABCDEF')

    fake_to_many_links = relationships.ToMany([])
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_to_many_links',
                 return_value=fake_to_many_links, autospec=True)

    result = relationships.mk_single_maybe_links(maybe_data, obj, cfg)

    assert relationships.mk_to_many_links.call_count == 1
    assert type(result) is relationships.ToMany


def test_mk_single_maybe_links_on_insanity(mocker):
    maybe_data = relationships.Data(1) # mock, insanity
    obj        = { 'links': 'fake' }   # mock, with 'links'
    cfg        = config.mk('https://api', 'ABCDEF')

    fake_to_one_links = relationships.ToOne(None)
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_to_one_links')
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_to_many_links')

    with pytest.raises(RuntimeError) as e_info:
        relationships.mk_single_maybe_links(maybe_data, obj, cfg)

    assert relationships.mk_to_one_links.call_count == 0
    assert relationships.mk_to_many_links.call_count == 0


def test_mk_single_maybe_links_on_none(mocker):
    maybe_data = None # mock, not used
    obj        = {}  # mock, no 'links'
    cfg        = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_to_one_links')
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_to_many_links')

    result = relationships.mk_single_maybe_links(maybe_data, obj, cfg)

    assert relationships.mk_to_one_links.call_count == 0
    assert relationships.mk_to_many_links.call_count == 0
    assert result is None


def test_mk_single_maybe_meta(mocker):
    obj = { 'meta': 'fake' } # mock, with 'meta'
    cfg = config.mk('https://api', 'ABCDEF')

    fake_meta = meta.Meta({})
    mocker.patch('furrycorn.v1_0.model.common.meta.mk',
                 return_value=fake_meta, autospec=True)

    result = relationships.mk_single_maybe_meta(obj, cfg)

    assert meta.mk.call_count == 1
    assert type(result) is meta.Meta


def test_mk_single_maybe_meta_on_none(mocker):
    obj = {} # mock, no 'meta'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.v1_0.model.common.meta.mk')

    result = relationships.mk_single_maybe_meta(obj, cfg)

    assert meta.mk.call_count == 0
    assert result is None


def test_mk_single(mocker):
    obj = {} # mock, doesn't matter
    cfg = config.mk('https://api', 'ABCDEF')

    patch1 = 'furrycorn.v1_0.model.common.relationships.mk_single_maybe_data'
    patch2 = 'furrycorn.v1_0.model.common.relationships.mk_single_maybe_links'
    patch3 = 'furrycorn.v1_0.model.common.relationships.mk_single_maybe_meta'

    mocker.patch(patch1)
    mocker.patch(patch2)
    mocker.patch(patch3)

    result = relationships.mk_single('name', obj, cfg)

    assert relationships.mk_single_maybe_data.call_count == 1
    assert relationships.mk_single_maybe_links.call_count == 1
    assert relationships.mk_single_maybe_meta.call_count == 1
    assert type(result) is relationships.Relationship


def test_mk(mocker):
    obj = { 'relationship1': {}, 'relationship2': {}, 'relationship3': {} }
    cfg = config.mk('https://api', 'ABCDEF')

    fake_data         = relationships.Data(relationships.ToMany([]))
    fake_relationship = relationships.Relationship('rel', fake_data)
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_single',
                 return_value=fake_relationship, autospec=True)

    result = relationships.mk(obj, cfg)

    assert relationships.mk_single.call_count == 3
    assert type(result) is relationships.Relationships
    assert len(result.dict_relationships) == 3


def test_mk_on_insanity(mocker):
    obj = { 'relationship1': {}, 'relationship2': {}, 'relationship3': {} }
    cfg = config.mk('https://api', 'ABCDEF')

    # The "insanity" part here is that the `any_data_or_links_or_meta` field of the
    # relationship is None. This will cause an exception.
    fake_relationship = relationships.Relationship('rel', None)
    mocker.patch('furrycorn.v1_0.model.common.relationships.mk_single',
                 return_value=fake_relationship, autospec=True)

    with pytest.raises(RuntimeError) as e_info:
        relationships.mk(obj, cfg)

