import os
import sys

sys.path.append(os.getcwd())

from furrycorn import config, fetch
from furrycorn.location import to_origin, to_resource
from furrycorn.toolkit.document import Data, Errors, Meta


config = \
    config.mk(to_origin('https://api.dc01.gamelockerapp.com/shards/global'),
              os.environ['FURRYCORN_API_KEY'])


def inspect(document):
    if type(document) is Data:
        for match in document:
            print('match id "{0}"'.format(match.resource_id.r_id))

            # We know before the 'assets' has one entry--the telmetry. But...
            # madglory exposes this (oddly) as 'to many', so we dig.
            for asset in match.traverse('assets'):
                if asset.maybe_dict_attrs.get('name', None):
                    url = asset.maybe_dict_attrs['URL']
                    print('  telemetry at: {0}'.format(url))

            # Let's see how many rounds happened this match:
            round_ct = len(match.traverse('rounds'))
            print('  round count: {0}'.format(round_ct))

            # And let's peek at the first roster's attributes:
            first_roster = match.traverse('rosters')[0]
            print('  roster #1 attrs: {0}'.format(first_roster.maybe_dict_attrs))
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


fetch = fetch.mk(config, to_resource('/matches'))
fetch(inspect)

