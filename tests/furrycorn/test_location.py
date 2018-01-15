import pytest

from furrycorn import location
from urllib.parse import parse_qs


def test_origin_str_with_port(mocker):
    origin = location.Origin('https', 'f.co', '/api/v1', '3000')

    assert str(origin) == 'https://f.co:3000/api/v1'


def test_origin_str_with_no_port(mocker):
    origin = location.Origin('https', 'f.co', '/api/v1')

    assert str(origin) == 'https://f.co/api/v1'


def test_path_str_with_components(mocker):
    path = location.Path('matches', '1234')
    assert str(path) == '/matches/1234'

    path = location.Path('matches')
    assert str(path) == '/matches'


def test_path_str_with_empty_components(mocker):
    path = location.Path('')

    assert str(path) == ''


def test_query_str_with_sort(mocker):
    dict_filters    = { 'foo': 1, 'bar': 2 }
    dict_pagination = { 'next': 'baz', 'prev': 'bat' }
    sort            = 'order'

    query = location.Query(dict_filters, dict_pagination, sort)

    assert str(query) == '?filter%5Bfoo%5D=1&filter%5Bbar%5D=2&' + \
                         'page%5Bnext%5D=baz&page%5Bprev%5D=bat&sort=order'


def test_query_str_with_no_sort(mocker):
    dict_filters    = { 'foo': 1, 'bar': 2 }
    dict_pagination = { 'next': 'baz', 'prev': 'bat' }

    query = location.Query(dict_filters, dict_pagination)

    assert str(query) == '?filter%5Bfoo%5D=1&filter%5Bbar%5D=2&' + \
                         'page%5Bnext%5D=baz&page%5Bprev%5D=bat'


def test_box_params_with_sort(mocker):
    dict_filters    = { 'foo': 'bar' }
    dict_pagination = { 'next': 'baz' }
    sort            = 'order'

    result = location.box_params(dict_filters, dict_pagination, sort)

    assert ('filter[foo]', 'bar') in result.items()
    assert ('page[next]', 'baz') in result.items()
    assert ('sort', 'order') in result.items()


def test_box_params_with_no_sort(mocker):
    dict_filters    = { 'foo': 'bar' }
    dict_pagination = { 'next': 'baz' }

    result = location.box_params(dict_filters, dict_pagination)

    assert ('filter[foo]', 'bar') in result.items()
    assert ('page[next]', 'baz') in result.items()
    assert 'sort' not in result


def test_unbox_params(mocker):
    expr = location.PATT_FILTER_QP # /^filter\[(.*)\]$/
    src  = { 'filter[foo]': 'bar', 'page[next]': 'baz' }

    result = location.unbox_params(src, expr)

    assert ('foo', 'bar') in result.items()
    assert ('page', 'next') not in result.items()


def test_mk_origin(mocker):
    result = location.mk_origin('https', 'api.com', '/v1', 3000)

    assert result.scheme == 'https'
    assert result.host == 'api.com'
    assert result.maybe_port == 3000
    assert result.script_name == '/v1'


def test_mk_path(mocker):
    result = location.mk_path('/matches/1234')

    assert result.name == 'matches'
    assert result.maybe_identifier == '1234'

    result = location.mk_path('/matches')

    assert result.name == 'matches'
    assert result.maybe_identifier is None


def test_mk_path_on_insanity(mocker):
    with pytest.raises(RuntimeError) as e_info:
        location.mk_path('/matches/1234/OH-NO-THIS-WONT-WORK')


def test_mk_query_with_sort(mocker):
    parsed_qs = { 'filter[foo]': 'bar', 'page[next]': 'baz', 'sort': 'order' }

    result = location.mk_query(parsed_qs)

    assert result.dict_filters == { 'foo': 'bar' }
    assert result.dict_pagination == { 'next': 'baz' }
    assert result.maybe_sort == 'order'


def test_mk_query_with_no_sort(mocker):
    parsed_qs = { 'filter[foo]': ['bar', 'baz'], 'page[next]': 'bat' }

    result = location.mk_query(parsed_qs)

    assert result.dict_filters == { 'foo': 'bar,baz' }
    assert result.dict_pagination == { 'next': 'bat' }
    assert result.maybe_sort is None


def test_to_url(mocker):
    origin   = location.mk_origin('https', 'api.com', '/v1')
    path     = location.mk_path('/matches/1234')

    result = location.to_url(origin, path)

    assert result == 'https://api.com/v1/matches/1234'

