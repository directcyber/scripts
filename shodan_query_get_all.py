#!/usr/bin/env python3
from shodan import Shodan
import os
import sys
import simplejson
import time
import urllib

api = Shodan(os.getenv('SHODAN_KEY'))

# Lookup an IP
# ipinfo = api.host('8.8.8.8')
# print(ipinfo)

time_now = int(time.time())

if len(sys.argv) < 1:
	print(f"usage: {sys.argv[0]} <search query>",file=sys.stderr)
	print(f"example: {sys.argv[0]} net:1.1.1.0/24", file=sys.stderr)
	exit(1)

q = sys.argv[1]
numres = 0

# each page is 100 results
filename = f'shodan_raw_response_{time_now}_{urllib.parse.quote_plus(q)}.json'
with open(filename, 'w') as f:
	for result in api.search_cursor(q):
		f.write(simplejson.dumps(result))
		# numres += len(result.get('matches'))
		numres += 1
		print(f"found {numres} results")


print("raw results written to", filename, file=sys.stderr)

