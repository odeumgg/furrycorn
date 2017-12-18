import os

from furrycorn.transport import mk_access, mk_fetch, api_url_to_resource
from furrycorn.jsonapi import v1_0


api_key  = os.environ['FURRYCORN_API_KEY']
api_url  = 'https://api.dc01.gamelockerapp.com/shards/global/matches'
resource = api_url_to_resource(api_url, '/shards/global')
access   = mk_access(api_key, resource)

def then_print(response):
    config = v1_0.mk_config(v1_0.Mode.LENIENT) 
    model  = v1_0.parse(response.json(), config)
    print(model)

fetch = mk_fetch(access)
fetch(then_print)

