import os
from pprint import pprint

from furrycorn.jsonapi import v1_0
from furrycorn.jsonapi.v1_0.data import Data
from furrycorn.toolkit.top_level_data import Directory
from furrycorn.transport import mk_access, mk_fetch, api_url_to_resource


api_key  = os.environ['FURRYCORN_API_KEY']
api_url  = 'https://api.dc01.gamelockerapp.com/shards/global/matches'
resource = api_url_to_resource(api_url, '/shards/global')
access   = mk_access(api_key, resource)


def then_print(response):
    config = v1_0.mk_config(v1_0.Mode.LENIENT) 
    root   = v1_0.parse(response.json(), config)

    # Cool thing about tuples--you can deconstruct them into local vars.
    any_data_or_errors_or_meta, _, _, _, _, maybe_included = root

    if type(any_data_or_errors_or_meta) is not Data:
        raise RuntimeError("oops, your response had no data")

    directory = Directory(any_data_or_errors_or_meta, maybe_included)
    pprint(directory.produce_all_types())


fetch = mk_fetch(access)
fetch(then_print)

