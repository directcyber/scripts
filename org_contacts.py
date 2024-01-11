#!/usr/bin/env python3

import sys
import subprocess
import requests

'''
script to find security reporting contact emails for a domain
'''

if len(sys.argv) < 2:
	print("usage: %s <domain>" % sys.argv[0])

domain = sys.argv[1]

got_security_txt = False

print("checking /.well-known/security.txt")

# check security.txt
r = requests.get(f'https://{domain}/.well-known/security.txt', allow_redirects=True)
if r.status_code != 404 and r.headers['Content-Type'] == 'text/plain' and len(r.text) < 3000:
	print("got security.txt:", r.text)
	got_security_txt = True

if not got_security_txt:
	r = requests.get(f'http://{domain}/.well-known/security.txt', allow_redirects=True)
	if r.status_code != 404 and r.headers['Content-Type'] == 'text/plain' and len(r.text) < 3000:
		print(r.text)

print("checking WHOIS")
whois = subprocess.check_output(["whois", domain], shell=False).decode()
for line in whois.split("\n"):
	if 'contact' in line.lower() or "@" in line:
		print(line)

