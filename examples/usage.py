import os

from furrycorn import config
from furrycorn import fetch
from furrycorn.location import to_origin, to_resource


config = \
    config.mk(to_origin('https://api.dc01.gamelockerapp.com/shards/global'),
              os.environ['FURRYCORN_API_KEY'])


def then_print(document):
    maybe_contents = document.produce_maybe_contents()

    # This doesn't do anything but show you how the API works.
    if maybe_contents:
        for resource in maybe_contents:
            resource_id = resource.resource_id
            rosters = resource.relate('rosters')
            for roster in rosters:
                resource_id = roster.resource_id
                print(resource_id)
    else:
        print("No content in document.")


fetch = fetch.mk(config, to_resource('/matches'))
fetch(then_print)

