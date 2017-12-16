import os

from furrycorn.transport import mk_access, mk_fetch, api_url_to_resource
from furrycorn.jsonapi.v1_0 import config, parsing

api_key  = os.environ['FURRYCORN_API_KEY']
api_url  = 'https://api.dc01.gamelockerapp.com/shards/global/matches'
resource = api_url_to_resource(api_url, '/shards/global')
access   = mk_access(api_key, resource)

config = config.mk_config(config.Mode.LENIENT)

def then_print(response):
    # print(response.content)
    print(parsing.mk_top_level(response.json(), config))

fetch = mk_fetch(access)
fetch(then_print)

