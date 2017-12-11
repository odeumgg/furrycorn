import re

from collections import namedtuple
from requests import Request, Response, Session
from urllib.parse import urlencode, parse_qs
from urllib3.util.url import parse_url

PATT_FILTER_QP = re.compile('^filter\[(.*)\]$')
PATT_PAGE_QP   = re.compile('^page\[(.*)\]$')
PATT_SORT_QP   = re.compile('^sort$')


def _param_subset(src, expr):
    relevant = {}

    for key, value in src.items():
        match = expr.match(key)
        if match is not None:
            relevant[match.group(1)] = value[0] # only first from query string

    return relevant


def _derived_query(parsed_qs):
    if 'sort' in parsed_qs:
        return Query(_param_subset(parsed_qs, PATT_FILTER_QP),
                     _param_subset(parsed_qs, PATT_PAGE_QP),
                     parsed_qs.get('sort')[0])
    else:
        return Query(_param_subset(parsed_qs, PATT_FILTER_QP),
                     _param_subset(parsed_qs, PATT_PAGE_QP),
                     None)


def resource_to_api_url(resource):
    return str(resource)


def api_url_to_resource(api_url, script_name):
    "Convert SLS API url to Resource type instance."

    sn_re     = re.compile('^{0}\/(.*)$'.format(re.escape(script_name)))
    url       = parse_url(api_url)
    path_info = sn_re.match(url.path)

    if not path_info:
        msg = 'api_url/script_name mismatch: {0}'.format(api_url)
        raise RuntimeError(msg)

    path_info_components = path_info.group(1).split('/')

    if len(path_info_components) not in [1, 2]:
        msg = 'api_url has unintelligible document: {0}'.format(api_url)
        raise RuntimeError(msg)

    if url.query is None:
        return Resource(Origin(url.scheme, url.host, url.port, script_name),
                        Document(*path_info_components))
    else:
        return Resource(Origin(url.scheme, url.host, url.port, script_name),
                        Document(*path_info_components),
                        _derived_query(parse_qs(url.query)))


class Fetch:
    """
    Callable action performs HTTP request and invokes callback with response.
    """

    def __init__(self, access):
        self.api_key, self.resource = access

    def __call__(self, callback, maybe_session=None):
        api_url = resource_to_api_url(self.resource)
        headers = \
            {
                'Accept': 'application/vnd.api+json',
                'Authorization': 'Bearer %s' % self.api_key
            }
        request = Request('GET', api_url, headers=headers).prepare()

        if maybe_session is None:
            with Session() as session:
                response = session.send(request)
        else:
            response = maybe_session.send(request)

        callback(response)

        return None


class Access(namedtuple('Request', ['api_key', 'resource'])):
    """
    Immutably describe combination of auth key and target URI.

    This is the type used by Transport to issue requests.
    """

    __slots__ = ()

    def __new__(cls, api_key, resource):
        return super(Access, cls).__new__(cls, api_key, resource)


class Resource(namedtuple('Resource', ['origin', 'document', 'maybe_query'])):
    "Immutably describe entire SLS API URL."

    __slots__ = ()

    def __new__(cls, origin, document, maybe_query=None):
        return super(Resource, cls).__new__(cls, origin, document, maybe_query)

    def __str__(self):
        if self.maybe_query is None:
            query = Query()
        else:
            query = self.maybe_query

        return '{0}{1}{2}'.format(self.origin, self.document, query)


class Origin(namedtuple('Origin', ['scheme', 'host', 'maybe_port',
                                   'script_name'])):
    """
    Immutably describe 'host' part of SLS API URL.

    Given a URL:
      https://foo.com/v1/matches/1234?query=something

    This data structure contains state describing:
      https://foo.com/v1
    """

    __slots__ = ()

    def __new__(cls, scheme, host, maybe_port, script_name):
        return super(Origin, cls).__new__(cls, scheme, host, maybe_port,
                                          script_name)

    def __str__(self):
        if self.maybe_port is None:
            return '{0}://{1}{2}'.format(self.scheme, self.host,
                                         self.script_name)
        else:
            return '{0}://{1}:{2}{3}'.format(self.scheme, self.host,
                                             self.maybe_port, self.script_name)
            

class Document(namedtuple('Document', ['name', 'maybe_identifier'])):
    """
    Immutably describe 'document' part of SLS API URL.

    Given a URL:
      https://foo.com/v1/matches/1234?query=something

    This data structure contains state describing:
      /matches/1234
    """

    __slots__ = ()

    def __new__(cls, name, identifier=None):
        return super(Document, cls).__new__(cls, name, identifier)

    def __str__(self):
        compacted = filter(None, [self.name, self.maybe_identifier])
        if not compacted:
            return ''
        else:
            return '/{0}'.format('/'.join(compacted))


class Query(namedtuple('Query', ['map_filters', 'map_pagination',
                                 'maybe_sort'])):
    """
    Immutably describe 'document' part of SLS API URL.

    Given a URL:
      https://foo.com/v1/matches?filter[playerName]=hi&sort=time&page[offset]=5

    This data structure contains state describing:
      ?filter[playerName]=hi&sort=time&page[offset]=5
    """

    __slots__ = ()

    def __new__(cls, map_filters={}, map_pagination={}, sort=None):
        return super(Query, cls).__new__(cls, map_filters, map_pagination,
                                         sort)
    def __str__(self):
        flattened = self.flatten()
        if not bool(flattened):
            return ''
        else:
            return '?{0}'.format(urlencode(flattened))

    def flatten(self):
        "Mash all the disparate params together into one dict."

        renamed_filters = {}
        for key, value in self.map_filters.items():
            renamed_filters['filter[{0}]'.format(key)] = value

        renamed_pagination = {}
        for key, value in self.map_pagination.items():
            renamed_pagination['page[{0}]'.format(key)] = value

        merged = { **renamed_filters, **renamed_pagination }

        if self.maybe_sort is not None:
            merged['sort'] = self.maybe_sort

        return merged

