import pytest

from furrycorn import location


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


def test_resource_str_with_query(mocker):
    path  = location.Path('matches', '1234')

    dict_filters    = { 'foo': 1, 'bar': 2 }
    dict_pagination = { 'next': 'baz', 'prev': 'bat' }
    sort            = 'order'
    query = location.Query(dict_filters, dict_pagination, sort)

    resource = location.Resource(path, query)

    assert str(resource) == '/matches/1234' + \
                            '?filter%5Bfoo%5D=1&filter%5Bbar%5D=2&' + \
                            'page%5Bnext%5D=baz&page%5Bprev%5D=bat&sort=order'


def test_resource_str_with_no_query(mocker):
    path     = location.Path('matches', '1234')
    resource = location.Resource(path)

    assert str(resource) == '/matches/1234'


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


def test_to_origin(mocker):
    head   = 'https://api.com:3000/v1'
    result = location.to_origin(head)

    assert result.scheme == 'https'
    assert result.host == 'api.com'
    assert result.maybe_port == 3000
    assert result.script_name == '/v1'


def test_unbox_params(mocker):
    expr = location.PATT_FILTER_QP # /^filter\[(.*)\]$/
    src  = { 'filter[foo]': 'bar', 'page[next]': 'baz' }

    result = location.unbox_params(src, expr)

    assert ('foo', 'bar') in result.items()
    assert ('page', 'next') not in result.items()


def test_derive_query_with_sort(mocker):
    parsed_qs = { 'filter[foo]': 'bar', 'page[next]': 'baz', 'sort': 'order' }

    result = location.derive_query(parsed_qs)

    assert result.dict_filters == { 'foo': 'bar' }
    assert result.dict_pagination == { 'next': 'baz' }
    assert result.maybe_sort == 'order'


def test_derive_query_with_no_sort(mocker):
    parsed_qs = { 'filter[foo]': 'bar', 'page[next]': 'baz' }

    result = location.derive_query(parsed_qs)

    assert result.dict_filters == { 'foo': 'bar' }
    assert result.dict_pagination == { 'next': 'baz' }
    assert result.maybe_sort is None


def test_to_resource_with_query(mocker):
    tail   = '/matches/1234?filters[foo]=bar'
    result = location.to_resource(tail)

    assert result.path.name == 'matches'
    assert result.path.maybe_identifier == '1234'
    assert result.maybe_query is not None

    tail   = '/matches?filters[foo]=bar'
    result = location.to_resource(tail)

    assert result.path.name == 'matches'
    assert result.path.maybe_identifier is None
    assert result.maybe_query is not None

    tail   = '/matches?unusual=bar'
    result = location.to_resource(tail)

    assert result.path.name == 'matches'
    assert result.path.maybe_identifier is None
    assert result.maybe_query is not None


def test_to_resource_with_no_query(mocker):
    tail   = '/matches/1234'
    result = location.to_resource(tail)

    assert result.path.name == 'matches'
    assert result.path.maybe_identifier == '1234'
    assert result.maybe_query is None

    tail   = '/matches'
    result = location.to_resource(tail)

    assert result.path.name == 'matches'
    assert result.path.maybe_identifier is None
    assert result.maybe_query is None


def test_to_resource_on_insanity(mocker):
    tail = '/matches/1234/OH-NO-THIS-WONT-WORK'

    with pytest.raises(RuntimeError) as e_info:
        location.to_resource(tail)


def test_to_url(mocker):
    origin   = location.to_origin('https://api.com/v1')
    resource = location.to_resource('/matches/1234')

    result = location.to_url(origin, resource)

    assert result == 'https://api.com/v1/matches/1234'

