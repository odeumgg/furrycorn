import pytest

from furrycorn.v1_0 import config, model, toolkit
from furrycorn.v1_0.model import data, errors
from furrycorn.v1_0.model.common import meta
from furrycorn.v1_0.toolkit import document


def test_process_on_data(mocker):
    fake_root     = model.Root(data.Data(None)) # mock
    fake_document = document.Data(fake_root.primary)
    mocker.patch('furrycorn.v1_0.toolkit.document.mk_data',
                 return_value=fake_document, autospec=True)

    result = toolkit.process(fake_root)

    assert document.mk_data.call_count == 1
    assert type(result) is document.Data


def test_process_on_errors(mocker):
    fake_root     = model.Root(errors.Errors([])) # mock
    fake_document = document.Errors(fake_root.primary)
    mocker.patch('furrycorn.v1_0.toolkit.document.mk_errors',
                 return_value=fake_document, autospec=True)

    result = toolkit.process(fake_root)

    assert document.mk_errors.call_count == 1
    assert type(result) is document.Errors


def test_process_on_meta(mocker):
    fake_root     = model.Root(meta.Meta([])) # mock
    fake_document = document.Meta(fake_root.primary)
    mocker.patch('furrycorn.v1_0.toolkit.document.mk_meta',
                 return_value=fake_document, autospec=True)

    result = toolkit.process(fake_root)

    assert document.mk_meta.call_count == 1
    assert type(result) is document.Meta


def test_process_on_insanity(mocker):
    fake_root     = model.Root(1) # mock, insane
    fake_document = document.Meta(fake_root.primary)
    mocker.patch('furrycorn.v1_0.toolkit.document.mk_data')
    mocker.patch('furrycorn.v1_0.toolkit.document.mk_errors')
    mocker.patch('furrycorn.v1_0.toolkit.document.mk_meta')

    with pytest.raises(RuntimeError):
        toolkit.process(fake_root)

    assert document.mk_data.call_count == 0
    assert document.mk_errors.call_count == 0
    assert document.mk_meta.call_count == 0

