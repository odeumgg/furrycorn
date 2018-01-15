import simplejson

from requests import Request, Session

from furrycorn import model, toolkit


class Fetch:
    """
    Callable action performs HTTP request and invokes callback with response.
    """

    def __init__(self, config, resource):
        self.config   = config
        self.resource = resource

    def __call__(self, callback, maybe_session=None):
        url = ''.join([str(self.config.origin), str(self.resource)])

        headers = \
            {
                'Accept': 'application/vnd.api+json',
                'Authorization': 'Bearer {0}'.format(self.config.api_key)
            }
        request = Request('GET', url, headers=headers).prepare()

        if maybe_session is None:
            with Session() as session:
                response = session.send(request)
        else:
            response = maybe_session.send(request)

        root = model.build(response.json(), self.config)
        callback(toolkit.process(root))

        return None


def mk(config, resource):
    return Fetch(config, resource)
