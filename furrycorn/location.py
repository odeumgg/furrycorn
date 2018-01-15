import re

from collections import namedtuple
from requests import Request, Response, Session
from urllib.parse import urlencode, parse_qs
from urllib3.util.url import parse_url


PATT_FILTER_QP = re.compile('^filter\[(.*)\]$')
PATT_PAGE_QP   = re.compile('^page\[(.*)\]$')
PATT_SORT_QP   = re.compile('^sort$')


class Origin(namedtuple('Origin', ['scheme', 'host', 'script_name',
                                   'maybe_port'])):
    """
    Description of 'host' part of SLS API URL.

    Given a URL:
      https://foo.com/v1/matches/1234?query=something

    This data structure contains state describing:
      https://foo.com/v1
    """

    __slots__ = ()

    def __new__(cls, scheme, host, script_name, maybe_port=None):
        return super(Origin, cls).__new__(cls, scheme, host, script_name,
                                          maybe_port)

    def __str__(self):
        if self.maybe_port is None:
            return '{0}://{1}{2}'.format(self.scheme, self.host,
                                         self.script_name)
        else:
            return '{0}://{1}:{2}{3}'.format(self.scheme, self.host,
                                             self.maybe_port, self.script_name)


class Path(namedtuple('Path', ['name', 'maybe_identifier'])):
    """
    Description of 'path' part of SLS API URL.

    Given a url path:
      /matches/1234?query=something

    This data structure contains state describing:
      /matches/1234
    """

    __slots__ = ()

    def __new__(cls, name, identifier=None):
        return super(Path, cls).__new__(cls, name, identifier)

    def __str__(self):
        components = list(filter(None, [self.name, self.maybe_identifier]))

        if components:
            return '/{0}'.format('/'.join(components))
        else:
            return ''


class Query(namedtuple('Query', ['dict_filters', 'dict_pagination',
                                 'maybe_sort'])):
    """
    Description of 'query' part of SLS API URL.

    Given a url path:
      /matches?filter[playerName]=hi&sort=time&page[offset]=5

    This data structure contains state describing:
      ?filter[playerName]=hi&sort=time&page[offset]=5
    """

    __slots__ = ()

    def __new__(cls, dict_filters, dict_pagination, maybe_sort=None):
        return super(Query, cls).__new__(cls, dict_filters, dict_pagination,
                                         maybe_sort)

    def __str__(self):
        boxed = box_params(self.dict_filters, self.dict_pagination,
                           self.maybe_sort)
        return '?{0}'.format(urlencode(boxed)) if boxed else ''


class Resource(namedtuple('Resource', ['path', 'maybe_query'])):
    """
    Description of 'resource' part of SLS API URL.

    Given a url path:
      /matches?filter[playerName]=hi&sort=time&page[offset]=5

    This data structure contains state describing:
      /matches?filter[playerName]=hi&sort=time&page[offset]=5
    """

    __slots__ = ()

    def __new__(cls, path, maybe_query=None):
        return super(Resource, cls).__new__(cls, path, maybe_query)

    def __str__(self):
        if self.maybe_query is None:
            query = Query({}, {})
        else:
            query = self.maybe_query

        return '{0}{1}'.format(self.path, query)


def box_params(dict_filters, dict_pagination, maybe_sort=None):
    """Mash all the disparate params together into one dict."""

    boxed_filters = {}
    for key, value in dict_filters.items():
        boxed_filters['filter[{0}]'.format(key)] = value

    boxed_pagination = {}
    for key, value in dict_pagination.items():
        boxed_pagination['page[{0}]'.format(key)] = value

    boxed = { **boxed_filters, **boxed_pagination }

    if maybe_sort is not None:
        boxed['sort'] = maybe_sort

    return boxed


def to_origin(head):
    url = parse_url(head)
    return Origin(url.scheme, url.host, url.path, maybe_port=url.port)


def unbox_params(src, expr):
    relevant = {}

    for key, value in src.items():
        match = expr.match(key)
        if match is not None:
            relevant[match.group(1)] = value

    return relevant


def derive_query(parsed_qs):
    if 'sort' in parsed_qs:
        return Query(unbox_params(parsed_qs, PATT_FILTER_QP),
                     unbox_params(parsed_qs, PATT_PAGE_QP),
                     parsed_qs.get('sort'))
    else:
        return Query(unbox_params(parsed_qs, PATT_FILTER_QP),
                     unbox_params(parsed_qs, PATT_PAGE_QP),
                     None)


def to_resource(tail):
    """Convert SLS API path to Resource type instance."""

    components = tail.split('?')
    path_info  = components[0]

    try:
        maybe_query = components[1]
    except IndexError:
        maybe_query = None

    path_info_components = path_info.split('/')[1:]

    if len(path_info_components) not in [1, 2]:
        msg = 'resource has indiscernable path: {0}'.format(tail)
        raise RuntimeError(msg)

    if maybe_query is None:
        return Resource(Path(*path_info_components))
    else:
        return Resource(Path(*path_info_components),
                        derive_query(parse_qs(maybe_query)))


def to_url(origin, resource):
    return ''.join([str(origin), str(resource)])

