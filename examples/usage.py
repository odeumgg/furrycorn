import os

from furrycorn.transport import api_url_to_resource, resource_to_api_url,  \
                                Access, Resource, Origin, Document, Query, \
                                Fetch
from furrycorn.jsonapi import v1

api_key  = os.environ['FURRYCORN_API_KEY']
api_url  = 'https://api.dc01.gamelockerapp.com/shards/global/matches'
resource = api_url_to_resource(api_url, '/shards/global')
access   = Access(api_key, resource)

def then_print(response):
    print(v1.mk_top_level(response.json()))

fetch = Fetch(access)
fetch(then_print)
