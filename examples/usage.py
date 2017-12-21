import os

from furrycorn.jsonapi.v1_0 import parsing
from furrycorn.jsonapi.v1_0 import toolkit
from furrycorn.jsonapi.v1_0.parsing.data import Data
from furrycorn.jsonapi.v1_0.toolkit.directory import Directory
from furrycorn.transport import mk_access, mk_fetch, api_url_to_resource


api_key  = os.environ['FURRYCORN_API_KEY']
api_url  = 'https://api.dc01.gamelockerapp.com/shards/global/matches'
resource = api_url_to_resource(api_url, '/shards/global')
access   = mk_access(api_key, resource)


def then_print(http_response):
    config = parsing.mk_config(parsing.Mode.LENIENT) 
    root   = parsing.parse(http_response.json(), config)

    # Cool thing about tuples--you can deconstruct them into local vars.
    any_data_or_errors_or_meta, _, _, _, _, maybe_included = root

    if type(any_data_or_errors_or_meta) is not Data:
        raise RuntimeError("oops, your response had no data")

    directory   = Directory(any_data_or_errors_or_meta, maybe_included)
    tk_document = toolkit.process(directory, root)

    maybe_contents = tk_document.produce_maybe_contents()

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

