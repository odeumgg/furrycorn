import os

from furrycorn.jsonapi.v1_0 import toolkit
from furrycorn.transport import mk_access, mk_fetch, api_url_to_resource


api_key  = os.environ['FURRYCORN_API_KEY']
api_url  = 'https://api.dc01.gamelockerapp.com/shards/global/matches'
resource = api_url_to_resource(api_url, '/shards/global')
access   = mk_access(api_key, resource)


def then_print(http_response):
    document       = toolkit.process(http_response.json())
    maybe_contents = document.produce_maybe_contents()

    # This doesn't do anything but show you how the API works.
    if maybe_contents:
        for resource in maybe_contents:
            resource_id = resource.resource_id
            rosters = resource.relate('rosters')
            for roster in rosters:
                resource_id = roster.resource_id
    else:
        print("No content in document.")


fetch = mk_fetch(access)
fetch(then_print)

