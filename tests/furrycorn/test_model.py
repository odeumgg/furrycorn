import pytest

from furrycorn import config, model
from furrycorn.model import data, errors, jsonapi, included, links
from furrycorn.model.common import meta


def test_mk_maybe_data(mocker):
    obj = { 'data': 'fake' } # mock, with 'data'
    cfg = config.mk('https://api', 'ABCDEF')

    fake_data = data.Data(None)
    mocker.patch('furrycorn.model.data.mk', return_value=fake_data,
                 autospec=True)

    result = model.mk_maybe_data(obj, config)

    assert data.mk.call_count == 1
    assert type(result) is data.Data


def test_mk_maybe_data_on_none(mocker):
    obj = {} # mock, no 'data'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.data.mk')

    result = model.mk_maybe_data(obj, config)

    assert data.mk.call_count == 0
    assert result is None


def test_mk_maybe_errors(mocker):
    obj = { 'errors': 'fake' } # mock, with 'errors'
    cfg = config.mk('https://api', 'ABCDEF')

    fake_errors = errors.Errors([])
    mocker.patch('furrycorn.model.errors.mk', return_value=fake_errors,
                 autospec=True)

    result = model.mk_maybe_errors(obj, config)

    assert errors.mk.call_count == 1
    assert type(result) is errors.Errors


def test_mk_maybe_errors_on_none(mocker):
    obj = {} # mock, no 'errors'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.errors.mk')

    result = model.mk_maybe_errors(obj, config)

    assert errors.mk.call_count == 0
    assert result is None


def test_mk_maybe_jsonapi(mocker):
    """Not yet implemented."""

    obj = { 'jsonapi': 'fake' } # mock, with 'errors'
    cfg = config.mk('https://api', 'ABCDEF')

    # fake_jsonapi = jsonapi.Errors([])
    # mocker.patch('furrycorn.model.errors.mk', return_value=fake_errors,
    #              autospec=True)

    result = model.mk_maybe_jsonapi(obj, config)


def test_mk_maybe_jsonapi_on_none(mocker):
    obj = {} # mock, no 'jsonapi'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.jsonapi.mk')

    result = model.mk_maybe_jsonapi(obj, config)

    assert jsonapi.mk.call_count == 0
    assert result is None


def test_mk_maybe_links(mocker):
    obj = { 'links': 'fake' } # mock, with 'links'
    cfg = config.mk('https://api', 'ABCDEF')

    fake_links = links.Links([])
    mocker.patch('furrycorn.model.links.mk', return_value=fake_links,
                 autospec=True)

    result = model.mk_maybe_links(obj, config)

    assert links.mk.call_count == 1
    assert type(result) is links.Links


def test_mk_maybe_links_on_none(mocker):
    obj = {} # mock, no 'links'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.links.mk')

    result = model.mk_maybe_links(obj, config)

    assert links.mk.call_count == 0
    assert result is None


def test_mk_maybe_included(mocker):
    obj = { 'included': 'fake' } # mock, with 'included'
    cfg = config.mk('https://api', 'ABCDEF')

    fake_included = included.Included([])
    mocker.patch('furrycorn.model.included.mk',return_value=fake_included,
                 autospec=True)

    result = model.mk_maybe_included(obj, config)

    assert included.mk.call_count == 1
    assert type(result) is included.Included


def test_mk_maybe_included_on_none(mocker):
    obj = {} # mock, no 'included'
    cfg = config.mk('https://api', 'ABCDEF')

    mocker.patch('furrycorn.model.included.mk')

    result = model.mk_maybe_included(obj, config)

    assert included.mk.call_count == 0
    assert result is None


def test_build(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    fake_data = data.Data(None)
    mocker.patch('furrycorn.model.mk_maybe_data', return_value=fake_data,
                 autospec=True)
    mocker.patch('furrycorn.model.mk_maybe_errors', return_value=None)
    mocker.patch('furrycorn.model.common.meta.mk_maybe')
    mocker.patch('furrycorn.model.mk_maybe_jsonapi')
    mocker.patch('furrycorn.model.mk_maybe_links')
    mocker.patch('furrycorn.model.mk_maybe_included')

    result = model.build(obj, config)

    assert model.mk_maybe_data.call_count == 1
    assert model.mk_maybe_errors.call_count == 1
    assert meta.mk_maybe.call_count == 1
    assert model.mk_maybe_jsonapi.call_count == 1
    assert model.mk_maybe_links.call_count == 1
    assert model.mk_maybe_included.call_count == 1
    assert type(result) is model.Root


def test_build_on_insanity_data_and_errors(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    # insanity here is that both data and errors are present
    fake_data = data.Data(None)
    mocker.patch('furrycorn.model.mk_maybe_data', return_value=fake_data,
                 autospec=True)
    fake_errors = errors.Errors([])
    mocker.patch('furrycorn.model.mk_maybe_errors',
                 return_value=fake_errors, autospec=True)
    mocker.patch('furrycorn.model.common.meta.mk_maybe')
    mocker.patch('furrycorn.model.mk_maybe_jsonapi')
    mocker.patch('furrycorn.model.mk_maybe_links')
    mocker.patch('furrycorn.model.mk_maybe_included')

    with pytest.raises(RuntimeError) as e_info:
        model.build(obj, config)


def test_build_on_insanity_not_any(mocker):
    obj = {} # mock
    cfg = config.mk('https://api', 'ABCDEF')

    # insanity here is all patched methods return None, so neither data nor
    # errors nor meta are present
    mocker.patch('furrycorn.model.mk_maybe_data', return_value=None)
    mocker.patch('furrycorn.model.mk_maybe_errors', return_value=None)
    mocker.patch('furrycorn.model.common.meta.mk_maybe', return_value=None)
    mocker.patch('furrycorn.model.mk_maybe_jsonapi')
    mocker.patch('furrycorn.model.mk_maybe_links')
    mocker.patch('furrycorn.model.mk_maybe_included')

    with pytest.raises(RuntimeError) as e_info:
        model.build(obj, config)

