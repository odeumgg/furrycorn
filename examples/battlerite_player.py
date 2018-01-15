import os
import simplejson
import sys
from requests import Request, Session
from urllib.parse import parse_qs, quote, urlencode
from urllib3.util.url import parse_url

sys.path.append(os.getcwd())

from furrycorn import config, model, toolkit
from furrycorn.location import mk_origin, mk_path, mk_query, to_url
from furrycorn.toolkit.document import Data, Errors, Meta


# Set the BATTLERITE_PLAYER_NAME environment variable to a list of
# comma-separated names to get information from the API.
api_key          = os.environ['BATTLERITE_API_KEY']
player_names     = os.environ['BATTLERITE_PLAYER_NAME']
each_player_name = player_names.split(',')
player_names     = list(map(lambda n: quote(n), each_player_name))

origin  = mk_origin('https', 'api.dc01.gamelockerapp.com', '/shards/global')
headers = { 'Accept': 'application/vnd.api+json',
            'Authorization': 'Bearer {0}'.format(api_key) }
url     = to_url(origin, mk_path('/players'),
                 mk_query({ 'filter[playerNames]': player_names }))
request = Request('GET', url, headers=headers).prepare()


with Session() as session:
    response = session.send(request)
    root     = model.build(response.json(), config.mk(origin, api_key))
    document = toolkit.process(root)

    if type(document) is Data:
        for player in document:
            from pprint import pprint
            pprint(player.maybe_dict_attrs)
    elif type(document) is Errors:
        print("Your request produced a document with errors:")
        from pprint import pprint
        pprint(document.produce_errors())
    elif type(document) is Meta:
        print("Your request produced a document with only metadata:")
        from pprint import pprint
        pprint(document.produce_meta())
    else:
        print("Buy a lottery ticket. There's no way this can happen.")

